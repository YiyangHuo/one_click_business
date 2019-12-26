import pymongo

class DBMongo:
    DB_NAME = None
    DB_PATH = None
    _client = None
    _db_inst = None

    def __init__(self, db_name, db_path):
        self.DB_NAME = db_name
        self.DB_PATH = db_path
        self._client = pymongo.MongoClient(self.DB_PATH)
        self._db_inst = self._client[self.DB_NAME]

    def GetTable(self, table):
        return self._db_inst[table]

db = DBMongo('testdb', 'mongodb://localhost:27017/')
