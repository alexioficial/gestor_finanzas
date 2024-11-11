from flask import Blueprint, render_template, request, session
from routes.RAuth import login_requerido
from json import dumps
import model.MCategoria as mcategoria

bp = Blueprint('Categoria', __name__)

@bp.route('/Categoria')
@login_requerido
def Categoria():
    return render_template('Categoria.html')

@bp.post('/RegCategoria')
def RegCategoria():
    try:
        data = request.get_json()
        idusuario = session.get('idusuario')
        idcategoria = data.get('idcategoria')
        txt_nombre = data.get('txt_nombre')
        chk_status = data.get('chk_status')
        if idcategoria == '':
            mcategoria.RegCategoria(idusuario, txt_nombre, chk_status)
        else:
            mcategoria.UCategoria(idusuario, idcategoria, txt_nombre, chk_status)
        return {'status': 0}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}

@bp.post('/BuscarCategorias')
def BuscarCategorias():
    try:
        html = ''
        idusuario = session['idusuario']
        categorias = mcategoria.SCategorias(idusuario)
        for categoria in categorias:
            categoria['_id'] = str(categoria['_id'])
            es_activa = categoria['status']
            activo = 'danger' if not es_activa else 'success'
            status_text = 'ACTIVA' if es_activa else 'INACTIVA'
            html += f'''
                <li class="list-group-item" onclick='LlenarCampos({dumps(categoria)})'>
                    {categoria['nombre']}
                    <span>
                        <span class="badge bg-{activo}">{status_text}</span>
                    </span>
                </li>
            '''
        return {'status': 0, 'html': html}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}

@bp.post('/EliminarCategoria')
def EliminarCategoria():
    try:
        data = request.get_json()
        idusuario = session['idusuario']
        idcategoria = data.get('idcategoria')
        mcategoria.DCategoria(idusuario, idcategoria)
        return {'status': 0}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}

@bp.post('/LlenarDdlCategorias')
def LlenarDdlCategorias():
    try:
        idusuario = session['idusuario']
        categorias = mcategoria.SCategorias(idusuario)
        html = ''
        for categoria in categorias:
            html += f'<option value="{categoria["idcategoria"]}">{categoria["nombre"]}</option>'
        return {'status': 0, 'html': html}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}