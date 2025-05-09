from flask import Blueprint, jsonify, request
from .models import Book
from .schemas import book_schema, books_schema
from . import db

libro_bp = Blueprint('libro', __name__)

@libro_bp.route('/') # Endpoint base para verificar que la API funciona.
def index():
    return "API Biblioteca funcionando"

@libro_bp.route('/libros', methods=['GET']) # Lista todos los libros en la base de datos.
def get_books():
    libros = Book.query.all()
    result = books_schema.dump(libros)
    return jsonify(result) # Devuelve un JSON con una lista de libros.

@libro_bp.route('/libros/<int:id>', methods=['GET']) # Obtiene los datos de un libro específico por su ID.
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'message': 'Libro no encontrado'}), 404
    return book_schema.jsonify(book) # Devuelve un JSON con los datos del libro o error 404 si no se encuentra.

@libro_bp.route('/libros', methods=['POST']) # Crea un nuevo libro con los datos enviados en formato JSON.
def create_book():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        book = book_schema.load(json_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    db.session.add(book)
    db.session.commit()
    return book_schema.jsonify(book), 201 # Devuelve el libro creado y código 201, o error 400 si falta algún campo.

@libro_bp.route('/libros/<int:id>', methods=['PUT']) # Actualiza los datos de un libro existente.
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'message': 'Libro no encontrado'}), 404

    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        updated_book = book_schema.load(json_data, instance=book, partial=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    db.session.commit()
    return book_schema.jsonify(updated_book) # Devuelve el libro actualizado o error si no se encuentra o hay datos inválidos.

@libro_bp.route('/libros/<int:id>', methods=['DELETE']) # Elimina un libro por su ID.
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'message': 'Libro no encontrado'}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': f'Libro con ID {id} eliminado'}) # Devuelve un mensaje de confirmación.

@libro_bp.route('/libros/buscar', methods=['GET']) # Busca libros por título, autor o categoría.
def search_books():
    titulo = request.args.get('titulo', '', type=str)
    autor = request.args.get('autor', '', type=str)
    categoria = request.args.get('categoria', '', type=str)

    query = Book.query

    if titulo:
        query = query.filter(Book.title.ilike(f'%{titulo}%'))
    if autor:
        query = query.filter(Book.author.ilike(f'%{autor}%'))
    if categoria:
        query = query.filter(Book.genre.ilike(f'%{categoria}%'))

    libros_filtrados = query.all()
    return books_schema.jsonify(libros_filtrados) # Devuelve un JSON con los libros que coincidan con los filtros.

@libro_bp.route('/libros/buscar-titulo', methods=['GET']) # Busca libros por título parcial o completo.
def buscar_libros():
    titulo = request.args.get('titulo')
    if not titulo:
        return jsonify({'error': 'Debe proporcionar un parámetro de búsqueda: titulo'}), 400

    libros = Book.query.filter(Book.title.ilike(f"%{titulo}%")).all()
    return jsonify(books_schema.dump(libros)) # Devuelve una lista de libros que coinciden con el título

@libro_bp.route('/libros/buscar-categoria', methods=['GET']) # Busca libros por categoria parcial o completo.
def buscar_por_categoria():
    categoria = request.args.get('categoria', '', type=str)

    if not categoria:
        return jsonify({'error': 'Debe proporcionar el parámetro "categoria"'}), 400

    libros = Book.query.filter(Book.genre.ilike(f'%{categoria}%')).all()
    return books_schema.jsonify(libros) # Devuelve una lista de libros que coinciden con la categoria