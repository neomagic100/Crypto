from dateutil import parser
from utils.globalConstants import SQL

class Date():
    def __init__(self, date):
        self.date = parser.parse(date)
        self.entry = self.getSqlDate(self.date)
        
    def getSqlDate(self, date):
        fDate = date.strftime(SQL.DATE_FORMAT)
        return f'DATE("{fDate}")'
    
    def __repr__(self):
        return self.entry