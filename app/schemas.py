from app import ma
from .models import Book
from marshmallow import fields, validate

class BookSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Book
        load_instance = True

    id = ma.auto_field()
    title = fields.String(required=True, validate=validate.Length(min=1, max=100))
    author = fields.String(required=True, validate=validate.Length(min=1, max=100))
    isbn = fields.String(required=True, validate=validate.Length(equal=13))
    genre = fields.String(required=True, validate=validate.Length(min=1, max=50))
    status = fields.String(required=True, validate=validate.Length(min=1, max=50))
    published_date = fields.Date(required=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)