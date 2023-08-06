import traceback

import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import threading
import pandas as pd
import numpy as np
import pyarrow as pa

from coinlib.data.DataTable import DataTable
from coinlib.logics.LogicBasicWorker import LogicBasicWorker
from coinlib.logics.manager.LogicManager import LogicManager
from coinlib.logics.manager.PortfolioModel import PortfolioModel
from coinlib.logics.offlineManager.LogicOfflineJobFakeBroker import LogicOfflineJobFakeBroker
from coinlib.helper import log
import asyncio
import simplejson as json
from coinlib.WorkerJobProcess import WorkerJobProcess
from coinlib.Registrar import Registrar
from coinlib.logics.LogicOfflineJob import LogicOfflineJob
from coinlib.logics.offlineManager.LogicOfflineJobFakeFutureBroker import LogicOfflineJobFakeFutureBroker
from coinlib.logics.offlineManager.LogicOfflineJobFakeSpotBroker import LogicOfflineJobFakeSpotBroker

from coinlib.logics.manager.PortfolioModel import PortfolioModel

class LogicOfflineWorker(LogicBasicWorker):
    _portfolio: PortfolioModel

    def initialize(self):
        super().initialize()
        self.logicInterface = stats.LogicRunnerOfflineServiceStub(self.getChannel())
        logicInfoFullData = self.logicInterface.GetConfig(self.workerJob)
        self.logicConfig = logicInfoFullData.logicInfo
        self.advancedDataInfo = json.loads(logicInfoFullData.advancedDataInfo)
        self._portfolio = PortfolioModel.from_stats_model(self.logicConfig.portfolio)
        self.startDate = pd.Timestamp(self.logicConfig.startDate)  # .tz_localize(None)
        self.endDate = pd.Timestamp(self.logicConfig.endDate) #  .tz_localize(None)

        self.chartConfigData = logicInfoFullData.chartData
        pass

    def onLogicRunnerError(self, job, error):

        statsError = statsModel.LogicRunnerOfflineWorkerError()
        statsError.error.message = str(error)
        statsError.worker.CopyFrom(self.workerJob)

        self.logicInterface.OnRunnerErrorOccured(statsError)

        return False


    def broadcastCurrentPercentage(self, percentage, manager):
        partiallyData = statsModel.LogicRunnerOfflineWorkerPartiallyData()
        partiallyData.percentage = percentage
        partiallyData.signalData = json.dumps({"keys": manager.getSignalData()}, ensure_ascii=False).encode('gbk')
        partiallyData.worker.CopyFrom(self.workerJob)

        broker : LogicOfflineJobFakeBroker = manager.broker
        partiallyData.statistic.CopyFrom( broker.getStatistics() )

        data = self.logicInterface.OnRunnerPartiallyData(partiallyData)


    def runOfflineLogicForTimerange(self):

        try:
            index = 0
            lastPercentage = 0
            rowLength = len(self.dataFrame.index)
            startDate = self.startDate
            endDate = self.endDate
            self.parameterTable = self.logicConfig.parameterTable

            # special case lets unset all "old" logic results
            self.dataFrame = self.dataFrame.loc[:,~self.dataFrame.columns.str.contains('^result.', case=False)]

            if self.dataFrame.shape[0] > 0:
                rowIndexZero = self.dataFrame.index[0]
                if rowIndexZero.tzinfo is None:
                    startDate = startDate.tz_localize(None)
                    endDate = endDate.tz_localize(None)

            self.generateLogicComponentsInfo()

            fakeManager = LogicManager("name of trader", self.logicConfig, self.logicConfig.brokerAccount, self._portfolio, advancedInfo=self.advancedDataInfo)
            fakeManager.resetLastValue()
            self.manager = fakeManager
            if self.logicConfig.brokerAccount.brokerType == self.logicConfig.brokerAccount.BrokerType.FUTURE:
                fakeManager.setBroker(LogicOfflineJobFakeFutureBroker(fakeManager))
            elif self.logicConfig.brokerAccount.brokerType == self.logicConfig.brokerAccount.BrokerType.SPOT:
                fakeManager.setBroker(LogicOfflineJobFakeSpotBroker(fakeManager))


            table = DataTable()
            table.from_df(self.dataFrame)

            minimumPeriod = 40
            index = 0
            columns = self.dataFrame.columns.to_list()
            setdf = []
            infoBlock = {}
            ##for row in self.dataFrame.itertuples(index=True, name='Pandas'):
            for row in table.rows():
                index = index + 1

                index_date = row[table.col["datetime"]]

                percentage = index / rowLength
                if percentage-0.05 > lastPercentage:

                    lastPercentage = percentage

                    threading.Thread(target=self.broadcastCurrentPercentage, args=[lastPercentage, fakeManager], daemon=True).start()

                if startDate and index_date > startDate and index > minimumPeriod:

                    lastindex = index-minimumPeriod if index-minimumPeriod > 0 else 0
                    subTable = table.subTable(lastindex, minimumPeriod)

                    fakeManager.setTable(subTable)
                    fakeManager.broker.setTable(subTable)
                    fakeManager.updateCurrentIndexToLast()
                    fakeManager.resetChanges()

                    # first we run this and then the next one
                    fakeManager.broker.runOrderCalculation()

                    self.runLogicComponents(subTable, fakeManager)

                    fakeManager.broker.calculateStatistics()
                    if fakeManager.hasChanged():
                        fakeManager.savePortfolio()

                    infoBlock[index-1] = fakeManager.getLastStorageRow()


                else:
                    infoBlock[index - 1] = {}


        except Exception as e:
            tb = traceback.format_exc()
            log.error(tb)
            self.onLogicRunnerError(None, e)
            return False

        self.extractLogicInfosFromManagerData(infoBlock)

        self.onLogicRunningFinished()

        return True

    def generateJob(self, table, logicComponentInfo, logic, inputs, fakeManager):
        return LogicOfflineJob(table, logicComponentInfo, logic, inputs, fakeManager, self)

    def run(self):

        t = threading.Thread(target=self.runOfflineLogicForTimerange, args=[], daemon=True)
        t.start()

        try:
            t.join()
        except Exception as e:
            pass

        finishedData = statsModel.LogicRunnerOfflineWorkerFinishedData()
        finishedData.signalData = json.dumps({"keys": self.manager.getSignalData()}, ensure_ascii=False).encode('gbk')
        finishedData.worker.CopyFrom(self.workerJob)

        finishedData.statistic.CopyFrom(self.manager.broker.getStatistics())

        self.logicInterface.OnRunnerFinishedComplete(finishedData)

        return True
