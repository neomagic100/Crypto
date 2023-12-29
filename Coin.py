from utils.DbEntry import DB_Entry

class Coin(DB_Entry):
    def __init__(self, data):
        DB_Entry.__init__(self)
        self.id = int(data.get('id')) if data.get('id') is not None else None
        self.name = data.get('name')
        self.symbol = data.get('symbol')
        self.slug = data.get('slug')
        self.num_market_pairs = int(data.get('num_market_pairs')) if data.get('num_market_pairs') is not None else None
        self.date_added = self.convert_to_datetime(data.get('date_added'))
        self.tags = data.get('tags') if data.get('tags') is not None else []
        self.max_supply = data.get('max_supply')
        self.circulating_supply = data.get('circulating_supply')
        self.total_supply = data.get('total_supply')
        self.infinite_supply = data.get('infinite_supply')
        self.platform = data.get('platform')
        self.cmc_rank = int(data.get('cmc_rank')) if data.get('cmc_rank') is not None else None
        self.self_reported_circulating_supply = data.get('self_reported_circulating_supply')
        self.self_reported_market_cap = data.get('self_reported_market_cap')
        self.tvl_ratio = data.get('tvl_ratio')
        self.last_updated = self.convert_to_datetime(data.get('last_updated'))
    
    def getName(self):
        return self.name
    
    def __repr__(self):
        return f'<Coin Object: "{self.name}">'
    
    def __str__(self):
        return self.name
            