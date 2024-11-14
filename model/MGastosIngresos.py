from components.conexion import gastosingresos, GenerarUUID
from model.MAuth import usuario
from model.MBilletera import billetera
from datetime import datetime

def RGastosIngresos(idusuario, idcategoria, monto, tipo, idbilletera):
    if tipo == 'G':
        usuario.update_one({'idusuario': idusuario}, {'$inc': {'balance': -monto}})
        if idbilletera != '0':
            billetera.update_one({'idusuario': idusuario, 'idbilletera': idbilletera}, {'$inc': {'balance': -monto}})
    else:
        usuario.update_one({'idusuario': idusuario}, {'$inc': {'balance': monto}})
        if idbilletera != '0':
            billetera.update_one({'idusuario': idusuario, 'idbilletera': idbilletera}, {'$inc': {'balance': monto}})
    return gastosingresos.insert_one({
        'idgastosingreso': GenerarUUID(),
        'idusuario': idusuario,
        'idcategoria': idcategoria,
        'monto': monto,
        'tipo': tipo,
        'idbilletera': idbilletera,
        'created_at': datetime.now()
    })

def SGastosIngresosPorIdUsuario(idusuario, idbilletera):
    result = gastosingresos.aggregate([
        { '$match': {'idusuario': idusuario, 'idbilletera': idbilletera if idbilletera != '0' else {'$exists': True}} },
        { '$lookup': {
            'from': 'categoria',
            'localField': 'idcategoria',
            'foreignField': 'idcategoria',
            'as': 'categoria'
        } },
        { '$unwind': '$categoria' },
        { '$sort': {'created_at': -1} }
    ])
    return list(result)[:10]