from __future__ import print_function
from mysql.connector import errorcode
import mysql.connector

class DB_CREATION:
    DB_NAME = "crypto"
    TABLES = {}

    TABLES["coins"] = (
        "CREATE TABLE IF NOT EXISTS `coins` ("
        "   `symbol` varchar(16) NOT NULL,"
        "   `name` varchar(80) NOT NULL,"
        # "   `slug`: ?, "
        "   `num_market_pairs` int(16),"
        "   `date_added` date NOT NULL,"
        # "   `tags` ?, "
        "   `max_supply` REAL,"
        "   `circulating_supply` REAL,"
        "   `total_supply` REAL,"
        "   `infinite_supply` enum('True', 'False') DEFAULT 'False',"
        "   `platform` TEXT,"
        "   `cmc_rank` int(10),"
        "   `self_reported_circulating_supply` REAL,"
        "   `self_reported_market_cap` REAL,"
        "   `tvl_ratio` REAL,"
        "   `last_updated` date," 
        "   `currency` enum('USD') DEFAULT 'USD',"
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
