import pymongo

class db_service():
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client.techstax
        
    def saveToHistory(self, dataObj):
        try:
            self.db.github_history.insert_one(dataObj)
            return True
        except:
            return False

