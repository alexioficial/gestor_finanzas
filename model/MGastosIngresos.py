from components.conexion import gastosingresos, GenerarUUID
from model.MAuth import usuario
from datetime import datetime

def RGastosIngresos(idusuario, idcategoria, monto, tipo):
    if tipo == 'G':
        usuario.update_one({'idusuario': idusuario}, {'$inc': {'balance': -monto}})
    else:
        usuario.update_one({'idusuario': idusuario}, {'$inc': {'balance': monto}})
    return gastosingresos.insert_one({
        'idgastosingreso': GenerarUUID(),
        'idusuario': idusuario,
        'idcategoria': idcategoria,
        'monto': monto,
        'tipo': tipo,
        'created_at': datetime.now()
    })

def SGastosIngresosPorIdUsuario(idusuario):
    result = gastosingresos.aggregate([
        { '$match': {'idusuario': idusuario} },
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