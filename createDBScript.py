from __future__ import print_function
from mysql.connector import errorcode
import mysql.connector

class DB_CREATION:
    DB_NAME = "crypto"
    TABLES = {}

    TABLES["coins"] = (
        "CREATE TABLE IF NOT EXISTS `coins` ("
        "   `id` int(10) NOT NULL,"
        "   `name` varchar(80) NOT NULL,"
        "   `symbol` varchar(16) NOT NULL,"
        "   `slug` TEXT, "
        "   `num_market_pairs` int(16) DEFAULT 0,"
        "   `date_added` date NOT NULL,"
        "   `tags` BLOB, "
        "   `max_supply` REAL DEFAULT 0,"
        "   `circulating_supply` REAL DEFAULT 0,"
        "   `total_supply` REAL DEFAULT 0,"
        "   `infinite_supply` TEXT,"
        "   `platform` TEXT,"
        "   `cmc_rank` int(10) NOT NULL,"
        "   `self_reported_circulating_supply` REAL DEFAULT 0,"
        "   `self_reported_market_cap` REAL DEFAULT 0,"
        "   `tvl_ratio` REAL DEFAULT 0,"
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
