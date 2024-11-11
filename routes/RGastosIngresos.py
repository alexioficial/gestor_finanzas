from flask import Blueprint, render_template, request, session
from routes.RAuth import login_requerido
import model.MGastosIngresos as mgastosingresos
bp = Blueprint('GastosIngresos', __name__)

@bp.route('/GastosIngresos')
@login_requerido
def GastosIngresos():
    return render_template('GastosIngresos.html')

@bp.post('/RegGasto')
@login_requerido
def RegGasto():
    try:
        data = request.get_json()
        idusuario = session['idusuario']
        idcategoria = data.get('idcategoria')
        monto = float(data.get('monto').replace(',', ''))
        mgastosingresos.RGastosIngresos(idusuario, idcategoria, monto, 'gasto')
        return {'status': 0}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}

@bp.post('/RegIngreso')
@login_requerido
def RegIngreso():
    try:
        data = request.get_json()
        idusuario = session['idusuario']
        idcategoria = data.get('idcategoria')
        monto = float(data.get('monto').replace(',', ''))
        mgastosingresos.RGastosIngresos(idusuario, idcategoria, monto, 'ingreso')
        return {'status': 0}
    except Exception as e:
        return {'status': 1, 'msj': str(e)} 