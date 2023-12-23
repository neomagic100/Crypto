from utils.typeProtection import castFloat
from dateutil import parser
import sqlite3

class Quote():
    def __init__(self, rawQuote, currency):
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

    def __repr__(self):
        return f'<Quote Object: "Price"={self.price}>'
    
    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return f'{self.price};{self.volume_24h};{self.volume_change_24h};' \
            + f'{self.percent_change_1h};{self.percent_change_24h};{self.percent_change_7d};' \
            + f'{self.percent_change_30d};{self.percent_change_60d};{self.percent_change_90d};' \
            + f'{self.market_cap};{self.market_cap_dominance};{self.fully_diluted_market_cap};' \
            + f'{self.tvl};{self.last_updated};'