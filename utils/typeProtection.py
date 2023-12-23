def castFloat(num):
    num = noneProtect(num)
    if num is None or type(num) == bool:
        return num
    try:
        flt = float(num)
        return flt
    except ValueError as ve:
        print(ve)
        return num
        
def castInt(num):
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

def strToBool(boolStr):
    if boolStr is None:
        return None
    if boolStr == "False" or boolStr == "false":
        return False
    elif boolStr == "True" or boolStr == "true":
        return True
    else:
        return boolStr