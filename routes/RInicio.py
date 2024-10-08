from flask import Blueprint, render_template, url_for, session
from routes.RAuth import login_requerido

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