from flask import Blueprint, render_template, request, session
from routes.RAuth import login_requerido
from json import dumps
import model.MBilletera as mbilletera

bp = Blueprint('Billetera', __name__)

@bp.route('/Billetera')
@login_requerido
def Billetera():
    return render_template('Billetera.html')

@bp.post('/RegBilletera')
def RegBilletera():
    try:
        data = request.get_json()
        idusuario = session.get('idusuario')
        idbilletera = data.get('idbilletera')
        txt_nombre = data.get('txt_nombre')
        chk_status = data.get('chk_status')
        if idbilletera == '':
            mbilletera.RegBilletera(idusuario, txt_nombre, chk_status)
        else:
            mbilletera.UBilletera(idusuario, idbilletera, txt_nombre, chk_status)
        return {'status': 0}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}

@bp.post('/BuscarBilleteras')
def BuscarBilleteras():
    try:
        html = ''
        idusuario = session['idusuario']
        billeteras = mbilletera.SBilleteras(idusuario)
        for billetera in billeteras:
            billetera['_id'] = str(billetera['_id'])
            es_activa = billetera['status']
            activo = 'danger' if not es_activa else 'success'
            status_text = 'ACTIVA' if es_activa else 'INACTIVA'
            html += f'''
                <li class="list-group-item" onclick='LlenarCampos({dumps(billetera)})'>
                    {billetera['nombre']}
                    <span>
                        <span class="badge bg-{activo}">{status_text}</span>
                    </span>
                </li>
            '''
        return {'status': 0, 'html': html}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}

@bp.post('/EliminarBilletera')
def EliminarBilletera():
    try:
        data = request.get_json()
        idusuario = session['idusuario']
        idbilletera = data.get('idbilletera')
        mbilletera.DBilletera(idusuario, idbilletera)
        return {'status': 0}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}

@bp.post('/LlenarDdlBilleteras')
def LlenarDdlBilleteras():
    try:
        idusuario = session['idusuario']
        billeteras = mbilletera.SBilleteras(idusuario)
        html = ''
        for billetera in billeteras:
            html += f'<option value="{billetera["idbilletera"]}">{billetera["nombre"]}</option>'
        return {'status': 0, 'html': html}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}