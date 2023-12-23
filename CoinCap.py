from coinmarketcap import DataRequest
from Coin import Coin

class CoinCap:
    def __init__(self, begin = True, start = None, limit = None, convert = None):
        self.data = self.capture(begin, start, limit, convert)
        self.getCoinArray()

    def capture(self, begin, start, limit, convert):
        dataReq = DataRequest(begin, start, limit, convert)
        data = dataReq.getData()
        return data.data
    
    def getCoinArray(self):
        self.coins = []
        for entry in self.data:
            coin = Coin(entry)
            self.coins.append(coin)
    
