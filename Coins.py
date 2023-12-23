# import sqlite3 as sql
import pymongo
from databaseUtils.Constants import Mongo

class CoinDB:
    def __init__(self) -> None:
        # self.connection = sql.connect("crypto.db")
        # self.cursor = self.connection.cursor()
        self.client   = pymongo.MongoClient(Mongo.CLIENT, username=Mongo.USERNAME, password=Mongo.PASSWORD)
        self.db       = self.client[Mongo.DB]
        self.col      = self.db[Mongo.COLLECTION]
    

    def addCoin(self, coin) -> None:
        if not self.coinExists(symbol = coin.symbol):
            inserted = self.col.insert_one(coin.toEntry())
            # self.col.insert_one({"_id": coin.symbol, },{"$set": {}})
            print(f"{inserted} {coin.name}")
        # else:
        #     updated = self.updateCoin(coin)
            
    def updateCoin(self, coin):
        doc = self.getCoin(symbol = coin.symbol)
        quote = doc["quote"]
        quote.append
                
    
    def coinExists(self, symbol = None, name = None) -> bool:
        doc = self.getCoin(symbol, name)
        if doc is not None and type(doc) == dict:
            return True
        
        return False
    
    def getCoin(self, symbol = None, name = None):
        query = None
        
        if name is not None:
            query = {"name": f"{name}"}
        elif symbol is not None:
            query = {"_id": f"{symbol}"}
        
        if query is None:
            raise Exception("Must query a name or symbol in getCoin()")
        
        doc = self.col.find_one(query)
            
        return doc

    def getCoins(self) -> dict:
        return self.coinDict
    

