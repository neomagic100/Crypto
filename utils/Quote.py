from utils.typeProtection import castFloat
from utils.sqlEntry import sqlEntry
from dateutil import parser
import sqlite3
from utils.globalConstants import SQL

class Quote(sqlEntry):
    def __init__(self, rawQuote, currency, symbol):
        sqlEntry.__init__(self)
        quote = rawQuote[currency]
        self.price = castFloat(quote["price"])
        self.volume_24h = castFloat(quote["volume_24h"])
        self.volume_change_24h = castFloat(quote["volume_change_24h"])
        self.percent_change_1h = castFloat(quote["percent_change_1h"])
        self.percent_change_24h = castFloat(quote["percent_change_24h"])
        self.percent_change_7d = castFloat(quote["percent_change_7d"])
        self.percent_change_30d = castFloat(quote["percent_change_30d"])
        self.percent_change_60d = castFloat(quote["percent_change_60d"])
        self.percent_change_90d = castFloat(quote["percent_change_90d"])
        self.market_cap = castFloat(quote["market_cap"])
        self.market_cap_dominance = castFloat(quote["market_cap_dominance"])
        self.fully_diluted_market_cap = castFloat(quote["fully_diluted_market_cap"])
        self.tvl = quote["tvl"]
        self.last_updated = parser.parse(quote["last_updated"])
        self.symbol = symbol

    def toEntry(self):
        # entryString = f'"price": "{self.price}", "volume_24h": "{self.volume_24h}", "volume_change_24h": "{self.volume_change_24h}", ' \
        #     + f'"percent_change_1h": "{self.percent_change_1h}", "percent_change_24h": "{self.percent_change_24h}", "percent_change_7d": "{self.percent_change_7d}", ' \
        #     + f'"percent_change_30d": "{self.percent_change_30d}", "percent_change_60d": "{self.percent_change_60d}", ' \
        #     + f'"percent_change_90d": "{self.percent_change_90d}", "market_cap": "{self.market_cap}", "market_cap_dominance": "{self.market_cap_dominance}", ' \
        #     + f'"fully_diluted_market_cap": "{self.fully_diluted_market_cap}", "tvl": "{self.tvl}", "last_updated": "{self.last_updated}"'
        # return entryString
        entryDict = {"price": f"{self.price}", "volume_24h": f"{self.volume_24h}", "volume_change_24h": f"{self.volume_change_24h}",
            "percent_change_1h": f"{self.percent_change_1h}", "percent_change_24h": f"{self.percent_change_24h}", "percent_change_7d": f"{self.percent_change_7d}",
            "percent_change_30d": f"{self.percent_change_30d}", "percent_change_60d": f"{self.percent_change_60d}",
            "percent_change_90d": f"{self.percent_change_90d}", "market_cap": f"{self.market_cap}", "market_cap_dominance": f"{self.market_cap_dominance}",
            "fully_diluted_market_cap": f"{self.fully_diluted_market_cap}", "tvl": f"{self.tvl}", "last_updated": f"{self.last_updated}"}
        return entryDict
    
    def getSqlDate(self, date):
        fDate = date.strftime(SQL.DATE_FORMAT)
        return str(fDate)
    # def toSingleEntry(self):
    #     entryString = self.toEntry()
    #     return ("{%s}" % entryString)
        
    def __repr__(self):
        return f'<Quote Object: "Price"={self.price}>'
    
    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return f'{self.price};{self.volume_24h};{self.volume_change_24h};' \
            + f'{self.percent_change_1h};{self.percent_change_24h};{self.percent_change_7d};' \
            + f'{self.percent_change_30d};{self.percent_change_60d};{self.percent_change_90d};' \
            + f'{self.market_cap};{self.market_cap_dominance};{self.fully_diluted_market_cap};' \
            + f'{self.tvl};{self.last_updated};'