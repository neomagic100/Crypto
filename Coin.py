from utils.typeProtection import castFloat, castInt, noneProtect, \
    strToBool
from utils.Quote import Quote
from dateutil import parser
import sqlite3

class Coin():
    def __init__(self, unparsedCoin):
        self.id = None
        self.name = None
        self.symbol = None
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
        self.symbol = data["symbol"]
        self.slug = data["slug"]
        self.num_market_pairs = castInt(data["num_market_pairs"])
        self.date_added = parser.parse(data["date_added"])
        self.tags = data["tags"]
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
        
    def getCurrency(self, dictkeys):
        for key in dictkeys:
            return key
        
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