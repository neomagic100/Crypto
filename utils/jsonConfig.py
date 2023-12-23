from utils.Status import Status

class JsonConfig():
    def __init__(self, json):
        self.json = json
        self.status = None
        self.data = None
        self.coinNameDict = {}
        self.symbolDict = {}
        self.splitIntoDicts()

    def splitIntoDicts(self):
        if not self.json:
            raise Exception("No json found")
        self.status = Status(self.json['status'])
        self.data = self.json['data']

        for coin in self.data:
            self.coinNameDict[coin['name']] = coin
            self.symbolDict[coin['symbol']] = coin

    def getCoinNames(self):
        return self.coinNameDict
    
    def getSymbolDict(self):
        return self.symbolDict
    
    def getJson(self):
        return self.json
    
    def getStatus(self):
        return self.status
    
    