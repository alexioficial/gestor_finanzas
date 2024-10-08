from flask import Blueprint, render_template, redirect, request, session

bp = Blueprint('Auth', __name__)

@bp.route('/Login', methods = ['GET', 'POST'])
def Login():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print(data)
            return {'status': 0}
        except Exception as e:
            return {'status': 1, 'msj': str(e)}
    return render_template('auth/Login.html')