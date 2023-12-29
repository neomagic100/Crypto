from utils.DbEntry import DB_Entry

class Quote(DB_Entry):
    def __init__(self, raw_quote, currency, symbol):
        DB_Entry.__init__(self)
        quote = raw_quote.get(currency, {})
        self.price = float(quote.get('price')) if quote.get('price') is not None else None
        self.volume_24h = float(quote.get('volume_24h')) if quote.get('volume_24h') is not None else None
        self.volume_change_24h = float(quote.get('volume_change_24h')) if quote.get('volume_change_24h') is not None else None
        self.percent_change_1h = float(quote.get('percent_change_1h')) if quote.get('percent_change_1h') is not None else None
        self.percent_change_24h = float(quote.get('percent_change_24h')) if quote.get('percent_change_24h') is not None else None
        self.percent_change_7d = float(quote.get('percent_change_7d')) if quote.get('percent_change_7d') is not None else None
        self.percent_change_30d = float(quote.get('percent_change_30d')) if quote.get('percent_change_30d') is not None else None
        self.percent_change_60d = float(quote.get('percent_change_60d')) if quote.get('percent_change_60d') is not None else None
        self.percent_change_90d = float(quote.get('percent_change_90d')) if quote.get('percent_change_90d') is not None else None
        self.market_cap = float(quote.get('market_cap')) if quote.get('market_cap') is not None else None
        self.market_cap_dominance = float(quote.get('market_cap_dominance')) if quote.get('market_cap_dominance') is not None else None
        self.fully_diluted_market_cap = float(quote.get('fully_diluted_market_cap')) if quote.get('fully_diluted_market_cap') is not None else None
        self.tvl = float(quote.get('tvl')) if quote.get('tvl') is not None else None
        self.last_updated = self.convert_to_datetime(quote.get('last_updated'))
        self.symbol = symbol

    def __repr__(self):
        return f'<Quote Object for {self.symbol}: "{self.last_updated}, {self.price}">'
    
    def getSymbol(self):
        return self.getSymbol()