from components.conexion import usuario, GenerarUUID
from datetime import datetime

def Registrar(username, password):
    return usuario.insert_one({
        'idusuario': GenerarUUID(),
        'username': username,
        'password': password,
        'balance': 0.0,
        'status': 'A',
        'created_at': datetime.now()
    })

def Login(username, password):
    return usuario.find_one({'username': username, 'password': password})

def SUsuarioPorId(idusuario):
    return usuario.find_one({'idusuario': idusuario})