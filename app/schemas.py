from app import ma
from .models import Book

class BookSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Book
        load_instance = True

    id = ma.auto_field()
    title = ma.auto_field()
    author = ma.auto_field()
    genre = ma.auto_field()
    published_date = ma.auto_field()

book_schema = BookSchema()
books_schema = BookSchema(many=True)