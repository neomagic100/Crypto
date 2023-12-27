class sqlEntry():
    def __init__(self):
        pass
    
    def toEntry(self):
        pass
    
    def toMysqlValuesString(self):
        valueDict = self.toEntry()
        s = '('
        for val in valueDict.values():
            if type(val) == int or type(val) == float:
                s += f'{val}, '
            else:
                s += f'"{val}", '
        # Remove last comma and space
        s = s[0:-2]
        s += ')'
        
        return s
    
    def containedIn(self, iterable):
        for item in iterable:
            if self.symbol == item.symbol:
                return True
        return False
    
    @staticmethod
    def insertManyString(tableName, iterable):
        insert = "INSERT INTO `{}` VALUES ".format(tableName)
        for item in iterable:
            insert += item.toMysqlValuesString() + ", "
        insert = insert[0:-2] + ";"
        return insert
    
    def insertOneString(tableName, item):
        insert = "INSERT INTO `{}` VALUES ".format(tableName)
        insert += item.toMysqlValuesString() + ";"
        return insert
    
    def getSqlDate(self, date):
        pass
     