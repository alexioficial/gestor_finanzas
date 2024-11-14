from flask import Blueprint, render_template, url_for, session, request
from routes.RAuth import login_requerido
import model.MAuth as mauth
import model.MGastosIngresos as mgastosingresos
import model.MBilletera as mbilletera

bp = Blueprint('Inicio', __name__)

@bp.route('/')
@login_requerido
def Inicio():
    return render_template('Inicio.html')

@bp.post('/Logout')
def Logout():
    try:
        session.clear()
        return {'status': 0, 'redireccion': url_for('Auth.Login')}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}

@bp.post('/ObtenerDatosInicio')
def ObtenerDatosInicio():
    try:
        data = request.get_json()
        idbilletera = data.get('idbilletera')
        dtusuario = mauth.SUsuarioPorId(session['idusuario'])
        dtusuario['_id'] = str(dtusuario['_id'])
        dtusuario['created_at'] = dtusuario['created_at'].strftime('%d/%m/%Y')
        dtusuario['balance'] = f'${dtusuario["balance"]:,.2f}'
        transacciones = mgastosingresos.SGastosIngresosPorIdUsuario(session['idusuario'], idbilletera)
        if idbilletera != '0':
            dtbilletera = mbilletera.billetera.find_one({'idusuario': session['idusuario'], 'idbilletera': idbilletera})
            dtbilletera['balance'] = f'${dtbilletera["balance"]:,.2f}'
            dtbilletera['_id'] = str(dtbilletera['_id'])
        else:
            dtbilletera = {'balance': dtusuario['balance']}
        for transaccion in transacciones:
            transaccion['_id'] = str(transaccion['_id'])
            transaccion['created_at'] = transaccion['created_at'].strftime('%d/%m/%Y')
            transaccion['categoria']['_id'] = str(transaccion['categoria']['_id'])
            transaccion['monto'] = f'${transaccion["monto"]:,.2f}'
        return {'status': 0, 'dtusuario': dtusuario, 'transacciones': transacciones, 'dtbilletera': dtbilletera}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}

@bp.post('/RegGasto')
def RegGasto():
    try:
        data = request.get_json()
        idusuario = session['idusuario']
        idcategoria = data.get('idcategoria')
        monto = data.get('monto')
        idbilletera = data.get('idbilletera')
        try:
            monto = float(monto.replace(',', ''))
        except:
            monto = 0.0
        if monto > 0:
            mgastosingresos.RGastosIngresos(idusuario, idcategoria, monto, 'G', idbilletera)
        return {'status': 0}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}

@bp.post('/RegIngreso')
def RegIngreso():
    try:
        data = request.get_json()
        idusuario = session['idusuario']
        idcategoria = data.get('idcategoria')
        monto = data.get('monto')
        idbilletera = data.get('idbilletera')
        try:
            monto = float(monto.replace(',', ''))
        except:
            monto = 0.0
        if monto > 0:
            mgastosingresos.RGastosIngresos(idusuario, idcategoria, monto, 'I', idbilletera)
        return {'status': 0}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}