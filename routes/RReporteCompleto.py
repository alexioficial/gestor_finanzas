from flask import Blueprint, render_template, request, session
from datetime import datetime
from routes.RAuth import login_requerido
from model.MReporteCompleto import SReporteCompleto

bp = Blueprint('ReporteCompleto', __name__)

@bp.route('/ReporteCompleto', methods = ['GET', 'POST'])
@login_requerido
def ReporteCompleto():
    return render_template('ReporteCompleto.html')

@bp.post('/ProcesarReporteCompleto')
def ProcesarReporteCompleto():
    try:
        data = request.get_json()
        idusuario = session['idusuario']
        idcategoria = data.get('idcategoria')
        idbilletera = data.get('idbilletera')
        tipo = data.get('tipo')
        fecha_inicial = datetime.strptime(data.get('fecha_inicial'), '%d/%m/%Y')
        fecha_final = datetime.strptime(data.get('fecha_final'), '%d/%m/%Y')
        organizar = data.get('organizar')
        
        resultado = SReporteCompleto(
            idusuario = idusuario,
            idcategoria = idcategoria,
            idbilletera = idbilletera,
            tipo = tipo,
            fecha_inicial = fecha_inicial,
            fecha_final = fecha_final,
            organizar = organizar
        )
        balance_total = 0.0
        totales_por_categoria = []
        totales_por_billetera = []
        for dt in resultado:
            dt['_id'] = str(dt['_id'])
            dt['usuario']['_id'] = str(dt['usuario']['_id'])
            dt['categoria']['_id'] = str(dt['categoria']['_id'])
            try:
                dt['billetera'][0]['_id'] = str(dt['billetera'][0]['_id'])
                billetera_0 = False
            except:
                billetera_0 = True
            
            # if dt['tipo'] == 'I':
            #     balance_total += dt['monto']
            # else:
            #     balance_total -= dt['monto']

            # total_por_categoria = {}
            # total_por_categoria['']
            # totales_por_categoria.append(total_por_categoria)

            # total_por_billetera = {}
            # totales_por_billetera.append(total_por_billetera)
        
        return {'status': 0, 'data': resultado}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}