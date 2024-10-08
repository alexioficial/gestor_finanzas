from model.MMain import usuario

def Registrar(username, password):
    return usuario.insert({'username': username, 'password': password})

def Login(username, password):
    result = usuario.select({'username': username, 'password': password})
    if not result:
        return None
    return result