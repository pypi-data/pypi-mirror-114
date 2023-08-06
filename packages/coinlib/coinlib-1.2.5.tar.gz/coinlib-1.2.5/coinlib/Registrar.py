import os
from coinlib import log
from coinlib.ChartsFactory import ChartsFactory
from coinlib.brokerWorker.BrokerFactory import BrokerFactory
from coinlib.feature.FeatureFactory import FeatureFactory
from coinlib.logics.LogicLoader import LogicFactory
from coinlib.notification import NotificationFactory
from coinlib.statistics.StatisticsMethodFactory import StatisticsMethodFactory
from coinlib.statistics.StatisticsRuleFactory import StatisticsRuleFactory
from coinlib.symbols import SymbolFactory


class Registrar(object):
    _instance = None
    functionsCallbacks = {}
    statisticsCallbacks = {}
    logicCallbacks = {}
    featureCallbacks = {}
    symbolBrokerCallbacks = {}
    brokerCallbacks = {}
    notificationCallbacks = {}
    symbolFactory: SymbolFactory = None
    brokerFactory: BrokerFactory = None
    currentPluginLoading = None
    notificationFactory: NotificationFactory = None
    chartsFactory: ChartsFactory = None
    featureFactory: FeatureFactory = None
    workerEndpoint = None
    workerEndpointPort = None
    statsRuleFactory: StatisticsRuleFactory = None
    logicFactory: LogicFactory = None
    workspaceId = None
    environment = None
    statsMethodFactory: StatisticsMethodFactory = None
    worker_modules = []
    connected = False
    isRegistered = False
    iframe_host = None
    worker_id = None
    coinlib_backend = None
    chipmunkdb = "localhost"

    notifications = None
    simulator = None
    statistics = None
    logic = None
    brokers = None
    data = None
    functions = None
    features = None
    featureSaverServer = None
    fixed_modules = None


    def __new__(cls):
        if cls._instance is None:
            log.info('Creating the object')
            cls._instance = super(Registrar, cls).__new__(cls)
            # Put any initialization here.

        return cls._instance

    def hasEnvironment(self):
        return self.environment is not None

    def setEnvironment(self, env):
        if self.environment is None:
            self.environment = env
        else:
            log.error("You are trying to change the environment - thats probably an error?")

    def isLiveEnvironment(self):
        return self.environment == "live"
    
    def setBackendPath(self, path):
        self.iframe_host = path + ":3000"
        self.coinlib_backend = path + ":" + self.get_port()
       # self.chipmunkdb = path

    def get_port(self):
        return self.workerEndpointPort

    def set_coinlib_backend(self, endpoint):
        self.workerEndpoint = endpoint
        self.coinlib_backend = endpoint
        self.iframe_host = endpoint + ":3000"

    # IP address
    def get_coinlib_backend(self):
        return self.workerEndpoint

    def get_coinlib_backend_chipmunk(self):
        return self.get_coinlib_backend()

    def get_coinlib_backend_grpc(self):
        return self.get_coinlib_backend() + ":" + self.get_port()
