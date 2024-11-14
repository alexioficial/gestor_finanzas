from components.conexion import gastosingresos
from datetime import datetime

def SReporteCompleto(**args):
    idusuario = args.get('idusuario')
    idcategoria = args.get('idcategoria')
    idbilletera = args.get('idbilletera')
    tipo = args.get('tipo') # G, I o T
    fecha_inicial = args.get('fecha_inicial')
    fecha_final = args.get('fecha_final')
    organizar = args.get('organizar') # fecha asc o desc
    result = gastosingresos.aggregate([
        { '$match': {
            'idusuario': idusuario,
            'idcategoria': idcategoria if idcategoria != '0' else { '$exists': True },
            'idbilletera': idbilletera if idbilletera != '0' else { '$exists': True },
            'tipo': tipo if tipo != 'T' else { '$exists': True },
            'created_at': { '$gte': fecha_inicial, '$lte': fecha_final }
        } },
        { '$lookup': {
            'from': 'usuario',
            'localField': 'idusuario',
            'foreignField': 'idusuario',
            'as': 'usuario'
         }},
        { '$lookup': {
            'from': 'categoria',
            'localField': 'idcategoria',
            'foreignField': 'idcategoria',
            'as': 'categoria'
        } },
        { '$lookup': {
            'from': 'billetera',
            'localField': 'idbilletera',
            'foreignField': 'idbilletera',
            'as': 'billetera'
        }},
        { '$unwind': '$usuario' },
        { '$unwind': '$categoria' },
        { '$sort': { 'created_at': 1 if organizar == 'asc' else -1 } }
    ])
    return list(result)