from flask import Blueprint, render_template, url_for, session
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
        html = ''
        return {'status': 0, 'html': html}
    except Exception as e:
        return {'status': 1, 'msj': str(e)}

@bp.post('/BuscarCategorias')
def BuscarCategorias():
    try:
        html = ''
        categorias = mcategoria.SCategorias()
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