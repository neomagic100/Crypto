from utils.typeProtection import castFloat, castInt, noneProtect, \
    strToBool, replaceChar, Db_Protect
from utils.Quote import Quote
from dateutil import parser
import sqlite3

class Coin():
    def __init__(self, unparsedCoin):
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
        self.id = castInt(data["id"])
        self.name = data["name"]
        self.symbol = self.verifySymbol(data["symbol"])
        self.slug = data["slug"]
        self.num_market_pairs = castInt(data["num_market_pairs"])
        self.date_added = parser.parse(data["date_added"])
        self.tags = data["tags"] # FIXME loaded in DB with weird formatting
        self.max_supply = castFloat(data["max_supply"])
        self.circulating_supply = castFloat(data["circulating_supply"])
        self.total_supply = castFloat(data["total_supply"])
        self.infinite_supply = strToBool(data["infinite_supply"])
        self.platform = noneProtect(data["platform"])
        self.cmc_rank = castInt(data["cmc_rank"])
        self.self_reported_circulating_supply = castFloat(data["self_reported_circulating_supply"])
        self.self_reported_market_cap = castFloat(data["self_reported_market_cap"])
        self.tvl_ratio = castFloat(data["tvl_ratio"])
        self.last_updated = parser.parse(data["last_updated"])
        self.currency = self.getCurrency(data["quote"])
        self.quote = self.createQuote(data["quote"]) 

    def createQuote(self, quoteData):
        quote = Quote(quoteData, self.currency)
        return quote
    
    def verifySymbol(self, symbol):
        tempSymbol = symbol
        
        if symbol == "":
            self.altSymbol = symbol
            tempSymbol = self.getName()
        
        if "$" in tempSymbol:
            self.altSymbol = symbol
            tempSymbol = tempSymbol.replace("$", Db_Protect.DOLLAR_REPLACEMENT)
        
        if tempSymbol.startswith("."):
            tempSymbol = replaceChar(tempSymbol, Db_Protect.PERIOD_REPLACEMENT, 0)
        
        if tempSymbol.endswith("."):
            tempSymbol = replaceChar(tempSymbol, Db_Protect.PERIOD_REPLACEMENT, -1)
            
        return tempSymbol
        
    def createQuoteEntry(self):
        quoteObj = self.quote
        quoteEntry    = quoteObj.toEntry()
        return quoteEntry       
        
    def getCurrency(self, dictkeys):
        for key in dictkeys:
            return key
        
    def toEntry(self):
        # entryString = f'"_id": "{self.symbol}", "id": "{self.id}", "name": "{self.name}", "symbol": "{self.symbol}", "slug": "{self.slug}", "num_market_pairs": "{self.num_market_pairs}", ' \
        #     + f'"date_added": "{self.date_added}", "tags": "{self.tags}", "max_supply": "{self.max_supply}", "circulating_supply": "{self.circulating_supply}", ' \
        #     + f'"total_supply": "{self.total_supply}", "infinite_supply": "{self.infinite_supply}", "platform": "{self.platform}", "cmc_rank": "{self.cmc_rank}", ' \
        #     + f'"self_reported_circulating_supply": "{self.self_reported_circulating_supply}", "self_reported_market_cap": "{self.self_reported_market_cap}", ' \
        #     + f'"tvl_ratio": "{self.tvl_ratio}", "last_updated": "{self.last_updated}", "currency": "{self.currency}", "quote": {self.quote.toSingleEntry()}'
        # return entryString
        
        entryDict = {"_id": f"{self.symbol}", "id": f"{self.id}", "name": f"{self.name}", "symbol": f"{self.symbol}", "slug": f"{self.slug}", "num_market_pairs": f"{self.num_market_pairs}", 
            "date_added": f"{self.date_added}", "tags": f"{self.tags}", "max_supply": f"{self.max_supply}", "circulating_supply": f"{self.circulating_supply}", 
            "total_supply": f"{self.total_supply}", "infinite_supply": f"{self.infinite_supply}", "platform": f"{self.platform}", "cmc_rank": f"{self.cmc_rank}", 
            "self_reported_circulating_supply": f"{self.self_reported_circulating_supply}", "self_reported_market_cap": f"{self.self_reported_market_cap}", 
            "tvl_ratio": f"{self.tvl_ratio}", "last_updated": f"{self.last_updated}", "currency": f"{self.currency}"}
        
        return entryDict
    
    # def toSingleEntry(self):
    #     entryString = self.toEntry()
    #     return ("{%s}" % entryString)
         
        
    def getQuote(self):
        return self.quote
        
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
            
    def getSymbol(self):      
        return self.symbol
    
    def getName(self):
        return self.name