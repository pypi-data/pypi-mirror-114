from coinlib.logics.LogicJob import LogicJob


class LogicOfflineJob(LogicJob):
    #, name, group, inputs, df, indicator, worker
    def __init__(self, table, logicComponentInfo, logicElement, inputs, fakeManager, worker):
        super(LogicOfflineJob, self).__init__(table, logicComponentInfo, logicElement, inputs, fakeManager, worker)
        self.worker = worker
        self.result_col = None

        pass

