from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def login():
    """Página de login"""
    return render_template('login.html')

@views_bp.route('/dashboard')
def dashboard():
    """Dashboard principal"""
    return render_template('dashboard.html')
