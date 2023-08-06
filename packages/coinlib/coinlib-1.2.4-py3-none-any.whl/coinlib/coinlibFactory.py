import sys

from coinlib.brokerWorker.BrokerFactory import BrokerFactory
from coinlib.feature.FeatureFactory import FeatureFactory
from coinlib.helper import pip_install_or_ignore
from coinlib.notification.NotificationFactory import NotificationFactory
from coinlib.symbols import SymbolFactory

pip_install_or_ignore("ipynb_path", "ipynb_path")
pip_install_or_ignore("websocket", "websocket-client")
pip_install_or_ignore("plotly", "plotly")
pip_install_or_ignore("simplejson", "simplejson")
pip_install_or_ignore("asyncio", "asyncio")
pip_install_or_ignore("grpc", "grpcio-tools")
pip_install_or_ignore("matplotlib", "matplotlib")
pip_install_or_ignore("pandas", "pandas")
pip_install_or_ignore("timeit", "timeit")
pip_install_or_ignore("dateutil", "python-dateutil")
pip_install_or_ignore("chipmunkdb", "chipmunkdb-python-client")

from coinlib.logics import LogicLoader
from coinlib.statistics import StatisticsRuleFactory, StatisticsMethodFactory
from coinlib import ChartsFactory
from coinlib.DataWorker import WorkerJobListener
from coinlib.Registrar import Registrar
import asyncio
from coinlib.helper import log

registrar = Registrar()

def run_main_function(worker_modules = []):
    registrar.setEnvironment("live")
    registrar.worker_modules = worker_modules if worker_modules is not None else []
    registrar.statsRuleFactory = StatisticsRuleFactory.StatisticsRuleFactory()
    registrar.statsMethodFactory = StatisticsMethodFactory.StatisticsMethodFactory()
    registrar.chartsFactory = ChartsFactory.ChartsFactory()
    registrar.symbolFactory = SymbolFactory.SymbolFactory()
    registrar.notificationFactory = NotificationFactory()
    registrar.logicFactory = LogicLoader.LogicFactory()
    registrar.brokerFactory = BrokerFactory()
    registrar.featureFactory = FeatureFactory()


    workerJobs = WorkerJobListener()
    workerJobs.start()

    log.info("Starting Coinlib Factory")

    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    finally:
        loop.close()

if __name__ == '__main__':
    worker_modules = []
    if len(sys.argv) > 1:
        worker_modules = sys.argv[1].split(",")
    run_main_function(worker_modules)