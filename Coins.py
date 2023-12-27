# import sqlite3 as sql
from mysql.connector import errorcode
import mysql.connector as mysqlc
from utils.globalConstants import FileConstants
from databaseUtils.Constants import MySQL
from createDBScript import DB_CREATION
from Coin import Coin
from utils.sqlEntry import sqlEntry
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
        self.coins    = []
        self.quotes   = []
        self.symbols = []
        self.currIndex = 0
        self.currQuoteIndex = 0
        self.doneReadingCoins = False
        self.doneReadingQuotes = False
    
    def insertCoinsToTable(self):
        coinString = sqlEntry.insertManyString("coins", self.coins)
        quoteString = sqlEntry.insertManyString("quotes", self.quotes)
        # coinEntryStrings = []
        # quoteEntryStrings = []
        
        # for coin in self.coins:
        #     coinEntry = sqlEntry.insertOneString("coins", coin)
        
        # for quote in self.quotes:
        #     quoteEntryStrings.append(sqlEntry)
        print("Starting insertion of coins")
        for coin in self.coins:
            print(coin)
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
            
            cursor = con.cursor()
    
            try:
                currString = None
                cursor.execute("USE {}".format(DB_CREATION.DB_NAME))
                currString = sqlEntry.insertOneString("coins", coin)
                cursor.execute(currString)
                # cursor.execute(coinString)
                # cursor.execute(quoteString)
                
                con.close
            except mysqlc.Error as err:
                print(err)
                print(currString)
                exit(1)
            else:
                exit(1)
        
    
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
            exit(1)
           
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
        
        con.close()
        
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
        self.quotes.append(coin.quote)
        if coin.symbol not in self.symbols:
            self.symbols.append(coin.symbol)
            self.coins.append(coin)
           
    def resetParams(self) -> None:
        self.currQuoteIndex = 0
        self.currIndex = 0
        self.doneReadingCoins = False
        self.doneReadingQuotes = False
    
    def coinExists(self, symbol = None, name = None) -> bool:
        pass
    
    def getCoin(self, symbol = None, name = None) -> Coin:
        pass
    
    def getCoins(self) -> dict:
        return self.coinDict
    

