## 
def is_integer( d ):
    if type( d ).__name__ == 'int':
        return True
    return False
    
def is_boolean( d ):
    if type( d ).__name__ == 'bool':
        return True
    return False
    
def is_string( d ):
    if type( d ).__name__ == 'str':
        return True
    return False
    
def is_list( d ):
    if type( d ).__name__ == 'list':
        return True
    return False
    
def is_dict( d ):
    if type( d ).__name__ == 'dict':
        return True
    return False
