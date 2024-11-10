from components.conexion import usuario, GenerarUUID

def Registrar(username, password):
    return usuario.insert_one({'idusuario': GenerarUUID(), 'username': username, 'password': password})

def Login(username, password):
    return usuario.find_one({'username': username, 'password': password})