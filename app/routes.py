from flask import Blueprint, jsonify, request
from .models import Book
from .schemas import book_schema, books_schema
from . import db

libro_bp = Blueprint('libro', __name__)

@libro_bp.route('/')
def index():
    return "API Biblioteca funcionando"

@libro_bp.route('/libros', methods=['GET'])
def get_books():
    libros = Book.query.all()
    result = books_schema.dump(libros)
    return jsonify(result)

@libro_bp.route('/libros/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'message': 'Libro no encontrado'}), 404
    return book_schema.jsonify(book)

@libro_bp.route('/libros', methods=['POST'])
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
    return book_schema.jsonify(book), 201

@libro_bp.route('/libros/<int:id>', methods=['PUT'])
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
    return book_schema.jsonify(updated_book)

@libro_bp.route('/libros/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'message': 'Libro no encontrado'}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Libro eliminado correctamente'})

@libro_bp.route('/libros/buscar', methods=['GET'])
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
    return books_schema.jsonify(libros_filtrados)