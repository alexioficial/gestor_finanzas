from flask import Blueprint, render_template, url_for, session
from routes.RAuth import login_requerido

bp = Blueprint('Categoria', __name__)

@bp.route('/Categoria')
@login_requerido
def Categoria():
    return render_template('Categoria.html')
