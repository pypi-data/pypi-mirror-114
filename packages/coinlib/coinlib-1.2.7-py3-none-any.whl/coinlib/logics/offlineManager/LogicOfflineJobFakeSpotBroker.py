import pandas as pd

from coinlib.logics.offlineManager.LogicOfflineJobFakeBroker import LogicOfflineJobFakeBroker


class LogicOfflineJobFakeSpotBroker(LogicOfflineJobFakeBroker):

    def __init__(self, manager):
        super(LogicOfflineJobFakeSpotBroker, self).__init__(manager)
        pass
