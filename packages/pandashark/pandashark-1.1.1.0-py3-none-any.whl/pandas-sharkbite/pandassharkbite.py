from . import AuthInfo, Range, Configuration, ZookeeperInstance, AccumuloConnector, Authorizations, Key, AccumuloBase, AccumuloIterator

class AccumuloIterator(AccumuloBase):

    _scanner = None
    _iter = None
    _resultset = None
    _chunkSize = 0
    _chunkCounter = 0

    def __init__(self, scanner):
        self._scanner = scanner
        self._resultset = scanner.getResultSet()
    
    def __init__(self, scanner, chunkSize):
        self._scanner = scanner
        self._resultset = scanner.getResultSet()
        self._chunkSize = chunkSize

    def __iter__(self):
        self._iter = self._resultset.__iter__()
        return self

    def nextBatch(self):
        self._chunkCounter = 0

    def __next__(self):
        tk = self._iter.__next__()
        if tk is None or (self._chunkSize > 0 and self._chunkCounter >= self._chunkSize ):
            raise StopIteration
        else:
            self._chunkCounter += 1
            return tk
        

class DataFrameIterator(AccumuloIterator):

    _columns = set()
    _iterator  = None
    def __init__(self, iterator: AccumuloIterator):
        self.__iterator = iterator
    
    def __iter__(self):
        self.__iterator.__iter__(self)
        return self

    def get_columns(self):
        return self._columns

    def __next__(self):
        tk = None
        datums = []
        
        while True:
            try:
                tk = self.__iterator.__next__()
            except StopIteration:
                self.__iterator.nextBatch()
                return datums
            tk_obj = dict()
            column = tk.getKey().getColumnFamily() + "." + tk.getKey().getColumnQualifier()
            self._columns.add(column)
            tk_obj[column] = tk.getValue().get()
            tk_obj['value'] = tk.getValue().get()
            tk_obj['column'] = column
            tk_obj['row'] = tk.getKey().getRow()
            tk_obj['visibility'] = tk.getKey().getColumnVisibility()
            datums.append(tk_obj)