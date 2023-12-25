# import sqlite3 as sql
from mysql.connector import errorcode
import mysql.connector as mysqlc
from utils.globalConstants import FileConstants
from databaseUtils.Constants import MySQL
from createDBScript import DB_CREATION
from Coin import Coin
import time
import os

class CoinDB:
    def __init__(self) -> None:
        # self.connection = sql.connect("crypto.db")
        # self.cursor = self.connection.cursor()
        # self.client   = pymongo.MongoClient(Mongo.CLIENT, username=Mongo.USERNAME, password=Mongo.PASSWORD)
        # self.db       = self.client[Mongo.DB]
        # self.coinCol  = self.db[Mongo.COIN_COLLECTION]
        # self.mysqlConn   = self.getMySqlConnection()
        self.createDatabase()
        self.quoteCols = []
        self.coins    = []
        self.quotes   = []
        self.currIndex = 0
        self.currQuoteIndex = 0
        self.doneReadingCoins = False
        self.doneReadingQuotes = False
        
    def createDatabase(self) -> mysqlc.connection:
        try:
            con = mysqlc.connect(user = MySQL.USER, password = MySQL.PASSWORD,
                                host = MySQL.HOST, port = MySQL.PORT,
                                database = MySQL.DB)
        except mysqlc.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(e)
           
        print("getting cursor...")
        cursor = con.cursor()
    
        try:
            cursor.execute("USE {}".format(DB_CREATION.DB_NAME))
            DB_CREATION.createTables(cursor)
        except mysqlc.Error as err:
            print("Database {} does not exists.".format(DB_CREATION.DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                DB_CREATION.create_database(cursor)
                DB_CREATION.createTables(cursor)
                print("Database {} created successfully.".format(DB_CREATION.DB_NAME))
                con.database = DB_CREATION.DB_NAME
            else:
                print(err)
                exit(1)
        
    def getMySqlConnection(self):
        try:
            con = mysqlc.connect(user = MySQL.USER, password = MySQL.PASSWORD,
                                host = MySQL.HOST, port = MySQL.PORT,
                                database = MySQL.DB)
        except mysqlc.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(e)
        else:
            con.close()
        
        return con
                
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
           
    def resetParams(self) -> None:
        self.currQuoteIndex = 0
        self.currIndex = 0
        self.doneReadingCoins = False
        self.doneReadingQuotes = False
            
    def getCurrentIndex(self, masterIdx) -> int:
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
    
    def coinExists(self, symbol = None, name = None) -> bool:
        pass
    
    def getCoin(self, symbol = None, name = None) -> Coin:
        pass
    
    def getCoins(self) -> dict:
        return self.coinDict
    

