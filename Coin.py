from utils.typeProtection import castFloat, castInt, noneProtect, \
    strToBool, replaceChar, Db_Protect
from utils.Quote import Quote
from dateutil import parser
import sqlite3
from utils.sqlEntry import sqlEntry
from utils.globalConstants import SQL
from datetime import datetime, date
from utils.EntryDates import Date

class Coin(sqlEntry):
    def __init__(self, unparsedCoin):
        sqlEntry.__init__(self)
        self.id = None
        self.name = None
        self.symbol = None
        self.altSymbol = None # Store symbol is invalid in database
        self.slug = None
        self.num_market_pairs = None
        self.date_added = None
        self.tags = None
        self.max_supply = None
        self.circulating_supply = None
        self.total_supply = None
        self.infinite_supply = None
        self.platform = None
        self.cmc_rank = None
        self.self_reported_circulating_supply = None
        self.self_reported_market_cap = None
        self.tvl_ratio = None
        self.last_updated = None
        self.quote = None

        self.createCoin(unparsedCoin)

    def createCoin(self, data):
        self.id = int(data["id"])
        self.name = data["name"]
        self.symbol = data["symbol"]
        self.slug = data["slug"]
        self.num_market_pairs = int(data["num_market_pairs"])
        self.date_added = Date(data["date_added"])
        self.tags = data["tags"] # FIXME loaded in DB with weird formatting
        self.max_supply = castFloat(data["max_supply"])
        self.circulating_supply = castFloat(data["circulating_supply"])
        self.total_supply = castFloat(data["total_supply"])
        self.infinite_supply = strToBool(data["infinite_supply"])
        self.platform = noneProtect(data["platform"])
        self.cmc_rank = int(data["cmc_rank"])
        self.self_reported_circulating_supply = castFloat(data["self_reported_circulating_supply"])
        self.self_reported_market_cap = castFloat(data["self_reported_market_cap"])
        self.tvl_ratio = castFloat(data["tvl_ratio"])
        self.last_updated = Date(data["last_updated"])
        self.currency = self.getCurrency(data["quote"])
        self.quote = self.createQuote(data["quote"])
        self.valueString = self.toMysqlValuesString()

    def createQuote(self, quoteData):
        quote = Quote(quoteData, self.currency, self.symbol)
        return quote
        
    def createQuoteEntry(self):
        quoteObj = self.quote
        quoteEntry    = quoteObj.toEntry()
        return quoteEntry       
        
    def getCurrency(self, dictkeys):
        for key in dictkeys:
            return key
        
    def getValueString(self):
        return self.valueString
        
    def toEntry(self):     # Removed Tags
        self.fixPossibleNones()   
        entryDict = {"id": self.id, "name": f"{self.name}", "symbol": f"{self.symbol}", "slug": f"{self.slug}", "num_market_pairs": self.num_market_pairs, 
            "date_added": self.date_added, "tags": "Empty", "max_supply": self.max_supply, "circulating_supply": self.circulating_supply, 
            "total_supply": self.total_supply, "infinite_supply": f"{self.infinite_supply}", "platform": f"{self.platform}", "cmc_rank": self.cmc_rank, 
            "self_reported_circulating_supply": self.self_reported_circulating_supply, "self_reported_market_cap": self.self_reported_market_cap, 
            "tvl_ratio": self.tvl_ratio, "last_updated": self.last_updated, "currency": f"{self.currency}"}
        
        return entryDict
    
    
    
    def fixPossibleNones(self):
        if self.circulating_supply is None or self.circulating_supply == "None":
            self.circulating_supply = 0
        if self.self_reported_market_cap is None or self.self_reported_market_cap == "None":
            self.self_reported_market_cap = 0
        if self.self_reported_circulating_supply is None or self.self_reported_market_cap == "None":
            self.self_reported_circulating_supply = 0
        if self.tvl_ratio is None or self.tvl_ratio == "None":
            self.tvl_ratio = 0
        if self.max_supply is None or self.max_supply == "None":
            self.max_supply = 0
    
    def getQuote(self):
        return self.quote
        
    def getSymbol(self):      
        return self.symbol
    
    def getName(self):
        return self.name
    
    def __repr__(self):
        return f'<Coin Object: "{self.name}">'
    
    def __str__(self):
        return self.name
    
    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return f"{self.id};{self.name};{self.symbol};{self.slug};" \
            + f"{self.num_market_pairs};{self.date_added};{self.tags};" \
            + f"{self.max_supply};{self.circulating_supply};" \
            + f"{self.total_supply};{self.infinite_supply};" \
            + f"{self.platform};{self.cmc_rank};" \
            + f"{self.self_reported_circulating_supply};" \
            + f"{self.self_reported_market_cap};{self.tvl_ratio};" \
            + f"{self.last_updated};{self.quote}"
            