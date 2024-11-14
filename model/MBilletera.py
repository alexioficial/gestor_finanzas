from components.conexion import billetera, GenerarUUID

def RegBilletera(idusuario, nombre, status):
    return billetera.insert_one({'idbilletera': GenerarUUID(), 'nombre': nombre, 'status': status, 'idusuario': idusuario})

def UBilletera(idusuario, idbilletera, nombre, status):
    return billetera.update_one({'idusuario': idusuario, 'idbilletera': idbilletera}, {'$set': {'nombre': nombre, 'status': status}})

def SBilleteras(idusuario):
    return list(billetera.find({'idusuario': idusuario}))

def SBilleterasActivas(idusuario):
    return list(billetera.find({'idusuario': idusuario, 'status': 'A'}))

def SBilleterasNombre(idusuario, nombre):
    return billetera.find_one({'idusuario': idusuario, 'nombre': nombre})

def DBilletera(idusuario, idbilletera):
    return billetera.delete_one({'idusuario': idusuario, 'idbilletera': idbilletera})