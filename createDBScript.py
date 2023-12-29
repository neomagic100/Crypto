from __future__ import print_function
import mysql.connector

class CoinsTableConstants:
    ID = 'id'
    NAME = 'name'
    SYMBOL = 'symbol'
    SLUG = 'slug'
    NUM_MARKET_PAIRS = 'num_market_pairs'
    DATE_ADDED = 'date_added'
    TAGS = 'tags'
    MAX_SUPPLY = 'max_supply'
    CIRCULATING_SUPPLY = 'circulating_supply'
    TOTAL_SUPPLY = 'total_supply'
    INFINITE_SUPPLY = 'infinite_supply'
    PLATFORM = 'platform'
    CMC_RANK = 'cmc_rank'
    SELF_REPORTED_CIRCULATING_SUPPLY = 'self_reported_circulating_supply'
    SELF_REPORTED_MARKET_CAP = 'self_reported_market_cap'
    TVL_RATIO = 'tvl_ratio'
    LAST_UPDATED = 'last_updated'
    CURRENCY = 'currency'

    @classmethod
    def __iter__(cls):
        values = []
        
        for key, value in cls.__dict__.items():
            if not key.startswith("__"):
                values.append(value)
        return iter(values)
    
def getColumns(tableConstants):
    const = tableConstants()
    cols = [col for col in const]
    return cols

class CoinTable:
    def getColumnsString():
        cols = getColumns(CoinsTableConstants)
        s = ""
        for col in cols:
            s += "`{}`, ".format(col)
        s = s[0 : -2]
        return "(" + s + ")"
    
class DB_CREATION:
    DB_NAME = "crypto"
    TABLES = {}

    TABLES["coins"] = (
        "CREATE TABLE IF NOT EXISTS `coins` ("
        "   `id` int(10) NOT NULL,"
        "   `name` varchar(80) NOT NULL,"
        "   `symbol` varchar(16) NOT NULL,"
        "   `slug` TEXT, "
        "   `num_market_pairs` int(16),"
        "   `date_added` date NOT NULL,"
        "   `tags` BLOB, "
        "   `max_supply` REAL,"
        "   `circulating_supply` REAL,"
        "   `total_supply` REAL,"
        "   `infinite_supply` TEXT,"
        "   `platform` TEXT,"
        "   `cmc_rank` int(10) NOT NULL,"
        "   `self_reported_circulating_supply` REAL,"
        "   `self_reported_market_cap` REAL,"
        "   `tvl_ratio` REAL,"
        "   `last_updated` date," 
        "   `currency` varchar(5) DEFAULT 'USD',"
        "   PRIMARY KEY(`symbol`)"
        ")  ENGINE=InnoDB"
    )

    TABLES["quotes"] = (
        "CREATE TABLE IF NOT EXISTS `quotes` ("
        "   `symbol` varchar(16) NOT NULL,"
        "   `price` REAL NOT NULL,"
        "   `volume_24h` REAL NOT NULL,"
        "   `volume_change_24h` REAL NOT NULL,"
        "   `percent_change_1h` REAL NOT NULL,"
        "   `percent_change_24h` REAL NOT NULL,"
        "   `percent_change_7d` REAL NOT NULL,"
        "   `percent_change_30d` REAL NOT NULL,"
        "   `percent_change_60d` REAL NOT NULL,"
        "   `percent_change_90d` REAL NOT NULL,"
        "   `market_cap` REAL NOT NULL,"
        "   `market_cap_dominance` REAL NOT NULL,"
        "   `fully_diluted_market_cap` REAL NOT NULL,"
        "   `tvl` REAL NOT NULL,"
        "   `last_updated` date NOT NULL,"
        "   PRIMARY KEY(`last_updated`, `symbol`), KEY `symbol` (`symbol`),"
        "   CONSTRAINT `quote_from_coin_fk_1` FOREIGN KEY (`symbol`) "
        "       REFERENCES `coins` (`symbol`) "
        "           ON DELETE CASCADE "
        "           ON UPDATE CASCADE "
        ")  ENGINE=InnoDB"
    )

    TABLES["hasQuote"] = (
        "CREATE TABLE IF NOT EXISTS `hasQuote` ("
        "   `symbol` varchar(16) NOT NULL,"
        "   `quoteDate` date NOT NULL,"
        "   PRIMARY KEY(`symbol`, `quoteDate`), KEY `symbol` (`symbol`), "
        "   KEY `quoteDate` (`quoteDate`),"
        "   CONSTRAINT `coin_has_quote_fk_1` FOREIGN KEY (`symbol`) "
        "       REFERENCES `coins` (`symbol`) "
        "           ON DELETE CASCADE "
        "           ON UPDATE CASCADE,"
        "   CONSTRAINT `coin_has_quote_fk_2` FOREIGN KEY (`quoteDate`) "
        "       REFERENCES `quotes` (`last_updated`) "
        "           ON DELETE CASCADE "
        "           ON UPDATE CASCADE "
        ")  ENGINE=InnoDB"
    )
    
    def create_database(cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_CREATION.DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
            
    def createTables(cursor):
        try:
            for tableName, table in DB_CREATION.TABLES.items():
                cursor.execute(table)
                print(f"Created Table {tableName}")
        except mysql.connector.Error as err:
            print("Failed creating table: {}".format(err))
            exit(1)
