from utils.exts import db
from models.base import BaseModel


class Genre(BaseModel, db.Model):
    name = db.Column(db.String(200), nullable=False, unique=True)
    books = db.relationship(
        'Book', secondary='book_genres', back_populates='genres')


book_genres = db.Table('book_genres',
                       db.Column('book_id', db.Integer, db.ForeignKey(
                           'book.id'), primary_key=True),
                       db.Column('genre_id', db.Integer, db.ForeignKey(
                           'genre.id'), primary_key=True)
                       )
