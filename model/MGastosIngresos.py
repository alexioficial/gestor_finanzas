from components.conexion import gastosingreso, GenerarUUID

def RGastosIngresos(idusuario, idcategoria, monto, tipo):
    return gastosingreso.insert_one({
        'idgastosingreso': GenerarUUID(),
        'idusuario': idusuario,
        'idcategoria': idcategoria,
        'monto': monto,
        'tipo': tipo
    })