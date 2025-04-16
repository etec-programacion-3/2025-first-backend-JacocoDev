from flask import Blueprint

libro_bp = Blueprint('libro', __name__)

@libro_bp.route('/')
def index():
    return "API Biblioteca funcionando"