from coinmarketcap import DataRequest
from Coins import CoinDB
from time import sleep
class CoinCap:
    def __init__(self, begin = True, start = None, limit = None, convert = None):
        self.data = self.capture(begin, start, limit, convert)
        self.coinDB = CoinDB(self.data)

    def capture(self, begin, start, limit, convert):
        dataReq = DataRequest(begin, start, limit, convert)
        data = dataReq.getData()
        return data.data
    
    def getDB(self):
        return self.coinDB
    
if __name__ == "__main__":
    while True:
        coinCapture = CoinCap()
        coinCapture = None
        sleep(300.0)
    