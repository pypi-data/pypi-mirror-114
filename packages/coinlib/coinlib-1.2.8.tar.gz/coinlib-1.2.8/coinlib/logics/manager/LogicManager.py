from coinlib.BasicJobSessionStorage import BasicJobSessionStorage
from coinlib.data.DataTable import DataTable
from coinlib.helper import log
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import pandas as pd

from coinlib.logics.manager.PortfolioModel import PortfolioModel, PriceInterface


class LogicManager(BasicJobSessionStorage):
    logicConfig: statsModel.LogicRunnerLogic
    brokerAccount: statsModel.BrokerAccountModel
    _portfolio: PortfolioModel

    def __init__(self, name, logicConfig: statsModel.LogicRunnerLogic, brokerAccount: statsModel.BrokerAccountModel=statsModel.BrokerAccountModel(),
                 portfolio: PortfolioModel = None, infoStorage = None, advancedInfo = None):
        super(LogicManager, self).__init__(infoStorage)
        self.table: DataTable = DataTable()
        self.broker = None
        self.advancedInfo = advancedInfo
        if portfolio is None:
            portfolio = PortfolioModel()
        self._portfolio = portfolio
        self.brokerAccount = brokerAccount
        self.name = name
        self.logicConfig = logicConfig

        pass

    def updatePortfolio(self, newPortfolio: PortfolioModel):
        self._portfolio = newPortfolio

    def getSymbolForChart(self, chartId):
        if self.advancedInfo is not None:
            if chartId in self.advancedInfo["chartToAssetMap"]:
                return self.advancedInfo["chartToAssetMap"][chartId]["symbols"]
        return None

    def getChartInfo(self):
        return self.advancedInfo["chartToAssetMap"]

    def getAssets(self):
        return self.portfolio.asset

    def getAsset(self, assetName: str) -> statsModel.BrokerPortfolioAsset:
        for a in self.portfolio.asset:
            if a.base.lower() == assetName.lower():
                return a

        return None

    def getMoney(self, assetName: str) -> float:
        a = self.getAsset(assetName)
        if a is not None:
            return a.available
        return None

    def updateCurrentIndexToLast(self):
        self.setCurrentIndex(self.table.index[-1], True)

    def getTable(self):
        return self.table

    def setTable(self, table):
        self.table = table

    def getName(self):
        return self.name

    def getBroker(self):
        return self.broker

    def setBroker(self, broker):
        self.broker = broker

    def isFuture(self):
        return self.brokerAccount.brokerType == self.logicConfig.brokerAccount.BrokerType.FUTURE

    def isSpot(self):
        return self.brokerAccount.brokerType == self.logicConfig.brokerAccount.BrokerType.SPOT

    def isOption(self):
        return self.brokerAccount.brokerType == self.logicConfig.brokerAccount.BrokerType.OPTION

    def isMargin(self):
        return self.brokerAccount.brokerType == self.logicConfig.brokerAccount.BrokerType.MARGIN

    def isBacktrader(self):
        return self.brokerAccount.mode == self.logicConfig.brokerAccount.BrokerMode.BACKTRADER

    def isPapertrader(self):
        return self.brokerAccount.mode == self.logicConfig.brokerAccount.BrokerMode.PAPER

    def isLivetrader(self):
        return self.brokerAccount.mode == self.logicConfig.brokerAccount.BrokerMode.LIVE

    def savePortfolio(self):
        self.saveInfo("account", "portfolio", self._portfolio.currentMoney.summary)
        return True

    def getPortfolio(self) -> PortfolioModel:
        return self._portfolio

    def getPortfolioQuoteMoney(self):
        return self._portfolio.currentMoney.summary