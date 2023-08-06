import pandas as pd
import numpy as np

class DataTable():
    def __init__(self, df=None):
        self._df = None
        self._np = None
        self.columns = []
        self.col = {}
        self.index = []
        if df is not None:
            self.convertDataFrame(df)
        return None

    def to_df(self):
        return pd.DataFrame(self._rows)

    def getDf(self):
        return self._df

    def from_df(self, df: pd.DataFrame):
        self._df = df
        self.convertDataFrame(df)

    def convertDataFrame(self, df):
        self._df = df
        self._np = df.to_numpy().transpose()
        self.columns = self._df.columns.to_list()
        index = 0
        for c in self.columns:
            self.col[c] = index
            index = index + 1
        self.index = self._df.index.tolist()

    def rows(self):
        return self._np.transpose()

    def subTable(self, index=0, length=None, columns=None):
        sub = DataTable()
        sub._df = self._df
        sub.columns = self.columns
        sub.col = self.col
        if length is None:
            length = len(self.index)
        sub.index = self.index[index:index + length]

        if columns is not None:
            sub.columns = columns
            list = []
            index = 0
            cols = {}
            for c in columns:
                list.append(self._np[self.col[c], index:index + length])
                cols[c] = index
                index = index + 1
            sub._np = np.array(list)
            sub.col = cols
        else:
            sub._np = self._np[:, index:index + length]

        return sub

    def setColumn(self, name, data, index=None, pad=True, type=np.float):
        ## padding needed maybe


        if name not in self.col:
            columnIndex = len(self.col.keys())
            self.col[name] = columnIndex-1
            length = len(self.index)
            a = np.zeros(length)
            a[:] = np.nan
            newlist = []
            for i in range(len(self.col)-1):
                newlist.append(self._np[i])
            newlist.append(a)
            self._np = np.array(newlist)

        length = len(self.index)
        if isinstance(data, (int, float)):
            narr = np.zeros(self.length())
            narr[:] = np.array(data)
            data = narr
        if len(data) < length:
            data = np.pad(np.array(data, dtype=type), (length-len(data),0), 'constant', constant_values=np.nan)

        self._np[self.col[name]] = data

    def length(self):
        return len(self.index)


    def getColumns(self, names):
        return self._np[[self.col[name] for name in names]]

    def getLast(self, name):
        row = self.getColumn(name)
        if row is not None:
            for i, e in enumerate(reversed(row)):
                if e is not None:
                    if "Timestamp" in str(type(e)):
                        return e.to_pydatetime()
                    if not np.isnan(e):
                        return e
            return None
        return None

    def getColumn(self, name, index=None):
        if index is not None:
            return self._np[self.col[name]][index]
        return self._np[self.col[name]]

    def getColumnNames(self):
        return self.col.keys()

    def column(self, name, index=None):
        return self.getColumn(name, index)

    def lastElement(self, column):
        return self.row(-1)[self.col[column]]

    def lastRow(self, column=None):
        if column is not None:
            return self.lastElement(column)
        r = self.row(-1)
        d = {}
        i = 0
        for s in self.columns:
            d[s] = r[i]
            i = i +1
        return d

    def row(self, row):
        return self._np[:, row]
