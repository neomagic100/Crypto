class DATABASE:
    DB = "cryptocurrency.db"

class TABLES:
    COIN = "coin"

# Not secret since all local  
class Mongo:
    CLIENT     = "mongodb://localhost:27017/"
    DB         = "coins"
    COIN_COLLECTION = "_coinEntries"
    USERNAME   = "root"
    PASSWORD   = "password"
    SLEEP      = 1

class MySQL:
    USER = "root"
    PASSWORD = "password"
    HOST = '127.0.0.1'
    DB   = 'db'
    PORT = 3306
    
    
