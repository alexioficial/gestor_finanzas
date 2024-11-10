from flask import Blueprint, render_template, request, session
from routes.RAuth import login_requerido
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
        txt_nombre = data.get('txt_nombre')
        chk_status = data.get('chk_status')
        mcategoria.RegCategoria(idusuario, txt_nombre, chk_status)
        return {'status': 0}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}

@bp.post('/BuscarCategorias')
def BuscarCategorias():
    try:
        html = ''
        idusuario = session.get('idusuario')
        categorias = mcategoria.SCategorias(idusuario)
        for categoria in categorias:
            activo = 'danger' if not categoria.get('status') else 'success'
            status_text = 'ACTIVO' if categoria.get('status') else 'INACTIVO'
            html += f'''
                <li class="list-group-item">
                    {categoria.get('nombre')}
                    <span>
                        <i class="fas fa-minus text-{activo} me-2"></i>
                        <span class="badge bg-{activo}">{status_text}</span>
                    </span>
                </li>
            '''
        return {'status': 0, 'html': html}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}
    
@bp.post('/BuscarCategoriaPorNombre')
def BuscarCategoriaPorNombre():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        idusuario = session.get('idusuario')
        categoria = mcategoria.SCategoriasNombre(idusuario, nombre)
        if categoria:
            return {
                'status': 0,
                'nombre': categoria.get('nombre'),
                'status': categoria.get('status')
            }
        else:
            return {'status': 1, 'msj': 'Categoría no encontrada'}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}
