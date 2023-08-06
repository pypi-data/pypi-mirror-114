import pandas as pd
import numpy as np
import json

from coinlib import Registrar, CoinlibDataInterface
from coinlib.BasicJob import BasicJob
from coinlib.dataWorker_pb2 import ParameterTable
from coinlib.logics.manager.LogicJobBroker import LogicJobBroker


class LogicJob(BasicJob):
    #, name, group, inputs, df, indicator, worker
    def __init__(self, table, logicComponentInfo, logicElement, inputs, manager, worker):
        super(LogicJob, self).__init__(table, inputs, manager)

        self.registrar = Registrar()
        self.trader: LogicJobBroker = None
        self.broker: LogicJobBroker = None
        self.component = logicComponentInfo
        self.setUniqueName(logicElement.identifier)
        self.logicElement = logicElement
        self.worker = worker
        self.name = logicElement.identifier
        self.manager = manager

        self.params = {}
        self.data = CoinlibDataInterface()
        self.data.connect()

        self.trader = manager.getBroker()
        # both names can work
        self.broker = manager.getBroker()
        self.alerts = self
        self.screener = self

    def traderName(self):
        return "ASDASD"

    def setParameterTable(self, parameterTable: ParameterTable):
        params = {}
        for p in parameterTable.parameters:
            val = json.loads(p.value)
            params[p.name] = val
        self.params = params

    def hasParam(self, paramName: str):
        if paramName in self.params:
            return True
        return False

    def param(self, paramName: str):
        if paramName in self.params:
            return self.params[paramName]
        return None

    def getTrader(self) -> LogicJobBroker:
        return self.trader

    def getName(self):
        return self.name

    def isLivetrader(self):
        return self.manager.isLivetrader()

    def isPapertrader(self):
        return self.manager.isPapertrader()

    def isBacktrader(self):
        return self.manager.isBacktrader()

    #### Symbol Blocks



    ##### Trader Blocks

    ## reachable through .broker / .trader

    #### Alert blocks

    def notification(self, text, notificationModule, images=[], parameters={}, auth={}):

        self.manager.saveInfo("notification", "notification", {"text": text, "module": notificationModule, "parameters": parameters})

        return True

    def notificationInteractive(self, callback, text,  buttons, notificationModule, images=[], parameters={}, auth={}):

        self.manager.saveInfo("notification", "notificationInteractive", {"text": text, "buttons": buttons, "module": notificationModule, "parameters": parameters})

        return True


    ####