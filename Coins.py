# import sqlite3 as sql

from utils.globalConstants import FileConstants
import time
import os

class CoinDB:
    def __init__(self) -> None:
        # self.connection = sql.connect("crypto.db")
        # self.cursor = self.connection.cursor()
        self.client   = pymongo.MongoClient(Mongo.CLIENT, username=Mongo.USERNAME, password=Mongo.PASSWORD)
        self.db       = self.client[Mongo.DB]
        self.coinCol  = self.db[Mongo.COIN_COLLECTION]
        self.quoteCols = []
        self.coins    = []
        self.quotes   = []
        self.currIndex = 0
        self.currQuoteIndex = 0
        self.doneReadingCoins = False
        self.doneReadingQuotes = False
        
    # Add coin and quote to internal list
    def addCoin(self, coin) -> None:
        quoteCol = self.db[coin.getSymbol()]
        self.quoteCols.append(quoteCol)
        self.quotes.append(coin.createQuoteEntry())
        # insertedQuote = quoteCol.insert_one(coin.createQuoteEntry())
        # print(f"{insertedQuote} {coin.getSymbol()}")
        
        if not self.coinExists(symbol = coin.getSymbol()):
            # inserted = self.coinCol.insert_one(coin.toEntry())
            self.coins.append(coin.toEntry())
            # print(f"{inserted} {coin.name}") 
    
    # Add internal coins and quotes to DB   
    def insertIntoDB(self):
        if not self.doneReadingCoins:
            self.currIndex = self.getCurrentIndex(self.currIndex)
            coinArray = self.coins[self.currIndex : -1]
            
            try:
                for coin in coinArray:
                    self.coinCol.insert_one(coin)
                    self.currIndex += 1
                # self.coinCol.insert_many(self.coins)
            except OSError as err:
                try:
                    with open(FileConstants.ERROR_FILE, "w") as f:
                        f.write(str(self.currIndex))
                    
                    time.sleep(Mongo.SLEEP)
                    self.reinitializeConnection()
                    time.sleep(Mongo.SLEEP)
                    
                    self.insertIntoDB()
                    
                except Exception as e:
                    print("Fatal Error")
                    e.with_traceback()
                    err.with_traceback()
                    
            except Exception as err:
                try:
                    with open(FileConstants.ERROR_FILE, "w") as f:
                        f.write(str(self.currIndex))
                    
                    time.sleep(Mongo.SLEEP)
                    self.reinitializeConnection()
                    time.sleep(Mongo.SLEEP)
                    
                    self.insertIntoDB()
                    
                except Exception as e:
                    print("Fatal Error")
                    e.with_traceback()
                    err.with_traceback()
        
        self.doneReadingCoins = True    
        self.currIndex = 0
        
        if not self.doneReadingQuotes:
        
            if self.quoteCols == []:
                raise Exception("There are no Quote collections specified")
            
            if len(self.quoteCols) != len(self.quotes):
                raise Exception("Number of Quote collections is not equal ot number of quotes")
            
            self.currQuoteIndex = self.getCurrentIndex(self.currQuoteIndex)
            quoteArray = self.quotes[self.currQuoteIndex : -1] 
            colArray = self.quoteCols[self.currQuoteIndex : -1]
            
            try:
                for i in range(len(quoteArray)):
                    colArray[i].insert_one(quoteArray[i])
                    
            except OSError as err:
                try:
                    with open(FileConstants.ERROR_FILE, "w") as f:
                        f.write(str(self.currQuoteIndex))
                    
                    time.sleep(Mongo.SLEEP)
                    self.reinitializeConnection()
                    time.sleep(Mongo.SLEEP)
                    
                    self.insertIntoDB()
                    
                except Exception as e:
                    print("Fatal Error")
                    e.with_traceback()
                    err.with_traceback()
                    
            except Exception as err:
                try:
                    with open(FileConstants.ERROR_FILE, "w") as f:
                        f.write(str(self.currQuoteIndex))
                    
                    time.sleep(Mongo.SLEEP)
                    self.reinitializeConnection()
                    time.sleep(Mongo.SLEEP)
                    
                    self.insertIntoDB()
                    
                except Exception as e:
                    print("Fatal Error")
                    e.with_traceback()
                    err.with_traceback()
        
        self.currQuoteIndex = 0
        self.doneReadingQuotes = True
        
    def resetParams(self):
        self.currQuoteIndex = 0
        self.currIndex = 0
        self.doneReadingCoins = False
        self.doneReadingQuotes = False
            
    def getCurrentIndex(self, masterIdx):
        cwd = os.getcwd()
        path = os.path.join(cwd, FileConstants.ERROR_FILE)
        
        if not os.path.exists(path):
            return masterIdx
        else:
            currIndex = 0
            
            try:
                with open(FileConstants.ERROR_FILE, "r") as f:
                    currIndex = f.read(FileConstants.MAX_BUFFER)
                os.remove(path)
                
                return int(currIndex)   
            except ValueError as ve:
                if currIndex == "":
                    return masterIdx
                else:
                    return currIndex
                
                
                             
            
    def reinitializeConnection(self):
        self.client   = pymongo.MongoClient(Mongo.CLIENT, username=Mongo.USERNAME, password=Mongo.PASSWORD)
        self.db       = self.client[Mongo.DB]
    
    def coinExists(self, symbol = None, name = None) -> bool:
        doc = self.getCoin(symbol, name)
        if doc is not None and type(doc) == dict:
            return True
        
        # if self.coins == []:
        #     return False
        
        # for coin in self.coins:
        #     if symbol is not None:
        #         if symbol == coin["_id"]:
        #             return True
        #     elif name is not None:
        #         if name == coin["name"]:
        #             return True
                
        return False
    
    def getCoin(self, symbol = None, name = None):
        query = None
        
        if name is not None:
            query = {"name": f"{name}"}
        elif symbol is not None:
            query = {"_id": f"{symbol}"}
        
        if query is None:
            raise Exception("Must query a name or symbol in getCoin()")
        
        doc = self.coinCol.find_one(query)
            
        return doc

    def getCoins(self) -> dict:
        return self.coinDict
    

