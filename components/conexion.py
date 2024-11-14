from pymongo import MongoClient
from uuid import uuid4
import os

cluster = MongoClient(os.getenv('MONGO_URI'))
db = cluster['gestor_finanzas']

usuario = db['usuario']
gasto = db['gasto']
ingreso = db['ingreso']
categoria = db['categoria']
gastosingresos = db['gastosingresos']
billetera = db['billetera']

usuario.create_index([("username", 1)], unique = True)

def GenerarUUID():
    return uuid4().hex