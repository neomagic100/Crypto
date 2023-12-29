import mysql.connector
from databaseUtils.Constants import MySQL
from createDBScript import CoinTable, getColumns, CoinsTableConstants

class MySQLConnection:
    def __init__(self):
        self.host = MySQL.HOST
        self.username = MySQL.USER
        self.password = MySQL.PASSWORD
        self.database = MySQL.DB
        self.port     = MySQL.PORT
        self.connection = None
        self.cursor = None
        self.verbose = False

    def connect(self, verbose=False):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database,
                port=MySQL.PORT
            )
            self.cursor = self.connection.cursor()
            if verbose:
                self.verbose = verbose
                print("Connected to MySQL Database!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def disconnect(self, verbose = False):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            if self.verbose or verbose:
                print("Disconnected from MySQL Database!")
                
    def execute_query(self, query, verbose = False):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            if self.verbose or verbose:
                print("Query executed successfully!")
        except mysql.connector.Error as err:
            self.connection.rollback()
            print(f"Error executing query: {err}")

    # def execute_insert_query(self, query, columns, values, verbose = False):
    #     try:
    #         self.cursor.execute(query, (columns, values))
    #         self.connection.commit()
    #         if self.verbose or verbose:
    #             print("Query executed successfully!")
    #     except mysql.connector.Error as err:
    #         self.connection.rollback()
    #         print(f"Error executing query: {err}")
    
    def execute_insert_query(self, coin, verbose = False):
        try:
            self.cursor = self.connection.cursor()
            sql = ("INSERT INTO coins "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            data = (coin.id, coin.name, coin.symbol, coin.slug, coin.num_market_pairs, 
                                       coin.date_added.entry, "Empty", coin.max_supply, coin.circulating_supply, coin.total_supply, 
                                       coin.infinite_supply, "None", coin.cmc_rank, coin.self_reported_circulating_supply, 
                                       coin.self_reported_market_cap, coin.tvl_ratio, coin.last_updated.entry, coin.currency)
            self.cursor.execute(sql, data)
            self.connection.commit()
            if self.verbose or verbose:
                print("Query executed successfully!")
        except mysql.connector.Error as err:
            self.connection.rollback()
            print(f"Error executing query: {err}")

    def fetch_data(self):
        return self.cursor.fetchall()
    
    def get_cursor(self):
        return self.cursor
    
    def commit_query(self):
        if self.cursor is not None and self.connection is not None:
            self.connection.commit()
        else:
            raise Exception("Either the connection or cursor was not established")
