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
from utils.sqlConnection import MySQLConnection
from createDBScript import CoinsTableConstants, getColumns, CoinTable

class CoinDB(MySQLConnection):
    def __init__(self) -> None:
        # self.connection = sql.connect("crypto.db")
        # self.cursor = self.connection.cursor()
        # self.client   = pymongo.MongoClient(Mongo.CLIENT, username=Mongo.USERNAME, password=Mongo.PASSWORD)
        # self.db       = self.client[Mongo.DB]
        # self.coinCol  = self.db[Mongo.COIN_COLLECTION]
        # self.mysqlConn   = self.getMySqlConnection()
        MySQLConnection.__init__(self)
        self.createDatabase()
        self.coins    = []
        self.quotes   = []
        self.symbols = []
        self.currIndex = 0
        self.currQuoteIndex = 0
        self.doneReadingCoins = False
        self.doneReadingQuotes = False
        self.coinValueStrings = []
        self.quoteValueStrings = []
    
    def insertCoinsToTable(self):
        coinString = sqlEntry.insertManyString("coins", self.coins)
        quoteString = sqlEntry.insertManyString("quotes", self.quotes)
        coin = self.coins[0]
        cols = getColumns(CoinsTableConstants)
        self.connect()
        # self.execute_query(sqlEntry.insertOneString("coins", coin))
        # self.execute_query(sqlEntry.insertOneValueString("coins", coin.valueString))
        # self.execute_insert_query("INSERT INTO `coins`%s VALUES %s;", CoinTable.getColumnsString(), coin.valueString)
        self.execute_insert_query(coin)
        self.disconnect()
    
    def createDatabase(self) -> mysqlc.connection:
        self.connect()
        self.execute_query("USE {}".format(DB_CREATION.DB_NAME))
        cursor = self.get_cursor()
        DB_CREATION.createTables(cursor)
        self.commit_query()
        self.disconnect()
                
    # Add coin and quote to internal list
    def addCoins(self, coins) -> None:
        for coin in coins:
            self.quotes.append(coin.getQuote())
            self._addCoin(coin)
    
    def getCoins(self) -> dict:
        return self.coinDict
    
    def _addCoin(self, coin) -> None:
        if coin.getSymbol() not in self.symbols:
            self.coins.append(coin)
            self.symbols.append(coin.getSymbol())
            self.coinValueStrings.append(coin.getValueString())
    

