from flask import Blueprint, render_template, redirect, url_for, request, session
from functools import wraps
import model.MAuth as mauth

bp = Blueprint('Auth', __name__)

def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if 'idusuario' not in session:
            return redirect(url_for('Auth.Login'))
        return f(*args, **kwargs)
    return decorador

@bp.route('/Login', methods = ['GET', 'POST'])
def Login():
    if request.method == 'POST':
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            user = mauth.Login(username, password)
            if user is None:
                return {'status': 1, 'msj': 'El usuario no existe'}
            session['idusuario'] = user['idusuario']
            session['username'] = user['username']
            session['password'] = user['password']
            return {'status': 0, 'redireccion': '/'}
        except Exception as e:
            return {'status': 1, 'msj': str(e)}
    return render_template('auth/Login.html')