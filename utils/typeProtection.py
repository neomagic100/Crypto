def castFloat(num) -> float:
    num = noneProtect(num)
    if num is None or type(num) == bool:
        return num
    try:
        flt = float(num)
        return flt
    except ValueError as ve:
        print(ve)
        return num
        
def castInt(num) -> int:
    num = noneProtect(num)
    if num is None or type(num) == bool:
        return num
    try:
        integer = int(num)
        return integer
    except ValueError as ve:
        print(ve)
        return num  
    
def noneProtect(var):
    if var is None or var == "None" or var == "none":
        return None
    return var

def strToBool(boolStr) -> str:
    if boolStr is None:
        return None
    if boolStr == "False" or boolStr == "false":
        return False
    elif boolStr == "True" or boolStr == "true":
        return True
    else:
        return boolStr
    
def replaceChar(string, newChar, index) -> str:
    length = len(string)
    
    if index < 0:
        index = length - index * -1
    
    if index == 0:
        stringBegin = ""
    else:
        stringBegin = string[0 : index]
    
    if index == length - 1: # end of string
        stringEnd = ""
    else:
        stringEnd = string[index + 1 : length]
    
    return stringBegin + newChar + stringEnd
    
    
class Db_Protect:
    DOLLAR_REPLACEMENT = "!!!"
    PERIOD_REPLACEMENT = "@@"