class DATABASE:
    DB = "cryptocurrency.db"

class TABLES:
    COIN = "coin"

# Not secret since all local  
class Mongo:
    DB         = "crypto"
    COIN_COLLECTION = "coins"
    QUOTES     = "quotes"
    USERNAME   = "root"
    PASSWORD   = "password"
    CLIENT     = "mongodb://localhost:27017"
    SLEEP      = 1
    LOG        = "scriptLog"
    LOG_DIR    = "logs"

class MySQL:
    USER = "root"
    PASSWORD = "password"
    HOST = '127.0.0.1'
    DB   = 'db'
    PORT = 3306
    
    
