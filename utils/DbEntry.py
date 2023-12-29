from datetime import datetime

class DB_Entry:
    def __init__(self):
        pass
    
    def convert_to_datetime(self, date_string):
        if date_string:
            return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return None
            
    def getSymbol(self):      
        return self.symbol