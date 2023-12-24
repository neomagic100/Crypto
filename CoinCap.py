from coinmarketcap import DataRequest
from Coin import Coin
from Coins import CoinDB

class CoinCap:
    def __init__(self, begin = True, start = None, limit = None, convert = None):
        self.data = self.capture(begin, start, limit, convert)
        self.getCoinArray()
        self.coinDB = CoinDB()

    def capture(self, begin, start, limit, convert):
        dataReq = DataRequest(begin, start, limit, convert)
        data = dataReq.getData()
        return data.data
    
    def getCoinArray(self):
        self.coins = []
        for entry in self.data:
            coin = Coin(entry)
            self.coins.append(coin)
            
    def initCoinData(self):
        for coin in self.coins:
            self.coinDB.addCoin(coin)
        print("Coins and Quotes fetched")
        self.coinDB.insertIntoDB()
    
    def getDB(self):
        return self.coinDB
    
if __name__ == "__main__":
    coinCapture = CoinCap()
    coinCapture.initCoinData()
    