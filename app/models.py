from . import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID único para cada libro
    title = db.Column(db.String(100), nullable=False)  # Título del libro
    author = db.Column(db.String(100), nullable=False)  # Autor del libro
    genre = db.Column(db.String(50), nullable=False)  # Género del libro
    published_date = db.Column(db.Date, nullable=False)  # Fecha de publicación

    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"