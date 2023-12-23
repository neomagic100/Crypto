import sqlite3 as sql

class CoinDB:
    def __init__(self) -> None:
        self.connection = sql.connect("crypto.db")
        self.cursor = self.connection.cursor()

    def addCoin(self, coin) -> None:
        self.cursor.execute("")
        # self.coinDict[coin.name] = coin

    def getCoins(self) -> dict:
        return self.coinDict
    

