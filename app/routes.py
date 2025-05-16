from flask import Blueprint, jsonify, request
from .models import Book
from .schemas import book_schema, books_schema
from . import db

libro_bp = Blueprint('libro', __name__)

@libro_bp.route('/')  # Endpoint base para verificar que la API funciona.
def index():
    return "API Biblioteca funcionando"

@libro_bp.route('/libros', methods=['GET'])  # Lista todos los libros en la base de datos.
def obtener_libros():
    libros = Book.query.all()
    resultado = books_schema.dump(libros)
    return jsonify(resultado)  # Devuelve un JSON con una lista de libros.

@libro_bp.route('/libros/<int:id>', methods=['GET'])  # Obtiene los datos de un libro específico por su ID.
def obtener_libro(id):
    libro = Book.query.get(id)
    if not libro:
        return jsonify({'mensaje': 'Libro no encontrado'}), 404
    return book_schema.jsonify(libro)  # Devuelve un JSON con los datos del libro o error 404 si no se encuentra.

@libro_bp.route('/libros', methods=['POST'])  # Crea un nuevo libro con los datos enviados en formato JSON.
def crear_libro():
    datos_json = request.get_json()
    if not datos_json:
        return jsonify({'mensaje': 'No se proporcionaron datos de entrada'}), 400

    try:
        libro = book_schema.load(datos_json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    db.session.add(libro)
    db.session.commit()
    return book_schema.jsonify(libro), 201  # Devuelve el libro creado y código 201, o error 400 si falta algún campo.

@libro_bp.route('/libros/<int:id>', methods=['PUT'])  # Actualiza los datos de un libro existente.
def actualizar_libro(id):
    libro = Book.query.get(id)
    if not libro:
        return jsonify({'mensaje': 'Libro no encontrado'}), 404

    datos_json = request.get_json()
    if not datos_json:
        return jsonify({'mensaje': 'No se proporcionaron datos de entrada'}), 400

    # Actualizar solo los campos que vienen en el JSON
    for campo in ['title', 'author', 'genre', 'published_date', 'isbn', 'status']:
        if campo in datos_json:
            setattr(libro, campo, datos_json[campo])

    db.session.commit()
    return book_schema.jsonify(libro)  # Devuelve el libro actualizado o error si no se encuentra o hay datos inválidos.

@libro_bp.route('/libros/<int:id>', methods=['DELETE'])  # Elimina un libro por su ID.
def eliminar_libro(id):
    libro = Book.query.get(id)
    if not libro:
        return jsonify({'mensaje': 'Libro no encontrado'}), 404

    db.session.delete(libro)
    db.session.commit()
    return jsonify({'mensaje': f'Libro con ID {id} eliminado'})  # Devuelve un mensaje de confirmación.

@libro_bp.route('/libros/buscar', methods=['GET'])  # Busca libros por título, autor o categoría.
def buscar_libros():
    titulo = request.args.get('titulo', '', type=str)
    autor = request.args.get('autor', '', type=str)
    categoria = request.args.get('categoria', '', type=str)

    consulta = Book.query

    if titulo:
        consulta = consulta.filter(Book.title.ilike(f'%{titulo}%'))
    if autor:
        consulta = consulta.filter(Book.author.ilike(f'%{autor}%'))
    if categoria:
        consulta = consulta.filter(Book.genre.ilike(f'%{categoria}%'))

    libros_filtrados = consulta.all()
    return books_schema.jsonify(libros_filtrados)  # Devuelve un JSON con los libros que coincidan con los filtros.

@libro_bp.route('/libros/buscar-titulo', methods=['GET'])  # Busca libros por título parcial o completo.
def buscar_libros_por_titulo():
    titulo = request.args.get('titulo')
    if not titulo:
        return jsonify({'error': 'Debe proporcionar un parámetro de búsqueda: titulo'}), 400

    libros = Book.query.filter(Book.title.ilike(f"%{titulo}%")).all()
    return jsonify(books_schema.dump(libros))  # Devuelve una lista de libros que coinciden con el título.

@libro_bp.route('/libros/buscar-categoria', methods=['GET'])  # Busca libros por categoría parcial o completa.
def buscar_libros_por_categoria():
    categoria = request.args.get('categoria', '', type=str)

    if not categoria:
        return jsonify({'error': 'Debe proporcionar el parámetro "categoria"'}), 400

    libros = Book.query.filter(Book.genre.ilike(f'%{categoria}%')).all()
    return books_schema.jsonify(libros)  # Devuelve una lista de libros que coinciden con la categoría.

@libro_bp.route('/libros/ordenar', methods=['GET'])  # Ordena los libros por un campo (por defecto: título) de forma ascendente.
def ordenar_libros():
    ordenar_por = request.args.get('por', 'title')
    
    if ordenar_por not in ['title', 'author', 'published_date']:
        return jsonify({'error': 'Criterio de ordenamiento no válido'}), 400
    
    libros = Book.query.order_by(getattr(Book, ordenar_por).asc()).all()
    return books_schema.jsonify(libros)  # Devuelve los libros ordenados en formato JSON.

@libro_bp.route('/libros/paginados', methods=['GET'])  # Obtiene libros paginados.
def obtener_libros_paginados():
    pagina = request.args.get('page', 1, type=int)  
    por_pagina = request.args.get('per_page', 10, type=int)  

    libros_paginados = Book.query.paginate(pagina, por_pagina, False)

    libros = books_schema.dump(libros_paginados.items)

    respuesta = {
        'libros': libros,
        'total': libros_paginados.total,
        'paginas': libros_paginados.pages,
        'pagina': libros_paginados.page,
        'por_pagina': libros_paginados.per_page
    }

    return jsonify(respuesta)  # Devuelve un JSON con los datos de los libros y la paginación.