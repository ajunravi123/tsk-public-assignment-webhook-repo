import pymongo
import yaml
dbConfig = yaml.load(open("app/services/config/db.yaml"))

class DBservices:
    def __init__(self):
        self.client = pymongo.MongoClient(dbConfig["HOST"], dbConfig["PORT"])
        self.db = self.client[dbConfig["DATABASE"]]
        
    def saveToHistory(self, dataObj):
        try:
            self.db["github_history"].insert_one(dataObj)
            return True
        except:
            return False

    def isExist(self, ref_id):
        try:
            xdata = self.db["github_history"].find({'request_id': ref_id })
            return True if xdata.count() > 0 else False
        except Exception as e:
            return e

