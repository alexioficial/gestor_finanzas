from flask import Blueprint, render_template, redirect

bp = Blueprint('Inicio', __name__)

@bp.route('/')
def Inicio():
    return render_template('Inicio.html')