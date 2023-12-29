from pymongo import MongoClient, InsertOne
from datetime import datetime
from databaseUtils.Constants import Mongo
from Coin import Coin
from Quote import Quote
import os
from pathlib import Path

class CoinDB():
    def __init__(self, data) -> None:
        self.coins = []
        self.quotes = []
        
        for entry in data:
            coin = Coin(entry)
            self.coins.append(coin)
            self.quotes.append(Quote(entry["quote"], 'USD', coin.getSymbol()))
        
        self.insert_coins_and_quotes(self.coins, self.quotes)       
    
    def convert_to_datetime(self, date_string):
        if date_string:
            return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return None
     
    # Function to insert many coins and many quotes with minimal queries
    def insert_coins_and_quotes(self, coins, quotes):
        logFile = self.openLogFile()
        try:
            client = MongoClient(Mongo.CLIENT, username=Mongo.USERNAME, password=Mongo.PASSWORD, authSource="admin")
            write(logFile, f"Established connection to {Mongo.CLIENT}")
            db = client[Mongo.DB]  # Replace 'your_database' with your database name
            write(logFile, f"Acquired database {Mongo.DB}")
            coin_collection = db[Mongo.COIN_COLLECTION]  # Collection for coins
            write(logFile, f"Found collection {Mongo.COIN_COLLECTION}")
            quote_collection = db[Mongo.QUOTES]  # Collection for quotes
            write(logFile, f"Found collection {Mongo.QUOTES}")

            # Create a unique index on 'symbol' field if it doesn't exist already
            coin_collection.create_index([('symbol', 1)], unique=True)
            write(logFile, f"Created Index in {Mongo.COIN_COLLECTION}")
            write(logFile, f"Beginning Inserting into {Mongo.COIN_COLLECTION}")
            for coin in coins:
                try:
                    coinExists = coin_collection.find({'symbol': coin.symbol}).limit(1)
                    if coinExists.retrieved == 0:
                        result = coin_collection.insert_one(vars(coin))
                        write(logFile, f"Inserted {coin.getName()} into {Mongo.COIN_COLLECTION}")
                except:
                    write(logFile, f"Coin {coin.name} already exists")
                    
            write(logFile, f"Finished Inserting into {Mongo.COIN_COLLECTION}")
            # Prepare bulk write operations for coins insertion
            
            # bulk_operations = [InsertOne(vars(coin)) for coin in coins]

            # Attempt bulk insertion of coins while handling duplicates
            # try:
            #     result = coin_collection.bulk_write(bulk_operations, ordered=False)
            #     print(f"Inserted {result.inserted_count} coins.")
            # except:
            #     print("Some coins were not inserted due to duplicate symbols.")

            # Prepare list of quote data
            write(logFile, f"Beginning Inserting into {Mongo.QUOTES}")
            quotes_data = [vars(quote) for quote in quotes]
            # Insert many quotes with actual last_updated field
            quote_collection.insert_many(quotes_data)
            write(logFile, f"Finished Inserting into {Mongo.QUOTES}")

            # Update last_updated field in Coin entry with the latest Quote entry's last_updated field for each symbol
            write(logFile, f"Updating entries in {Mongo.COIN_COLLECTION} to reflect dates in {Mongo.QUOTES}")
            
            for symbol in set(coin.getSymbol() for coin in coins):
                latest_quote = quote_collection.find({'symbol': symbol}).sort('last_updated', -1).limit(1)
                latest_quote_date = latest_quote[0]['last_updated']
                coin_collection.update_many({'symbol': symbol}, {'$set': {'last_updated': latest_quote_date}})
                
            write(logFile, f"Finished updating entries in {Mongo.COIN_COLLECTION} to reflect dates in {Mongo.QUOTES}")
        except Exception as e:
            write(logFile, e)
            print(e)
        finally:
            client.close()
            write(logFile, "Closed Database Connection")
            logFile.close()
    
    def openLogFile(self):
        timeNow = str(datetime.now())
        logFileName = Mongo.LOG + "_" + timeNow[:timeNow.index(".")].replace(" ", "_").replace(":", "") + ".log"
        directory = os.getcwd()
        if "C:" in directory:
            file = Path().cwd() / Mongo.LOG_DIR / logFileName 
        else:
            file = f"./{Mongo.LOG_DIR/logFileName}"
        logFile = open(file, "w")
        return logFile

def write(logfile, stringOut):
    timeNow = str(datetime.now())
    try:
        logfile.write(f"{timeNow} > {stringOut}\n")
    except:
        logfile.write(f"{timeNow} > Warning: Log has character not recognizable to UTF-8\n")