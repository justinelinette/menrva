from utils.exts import db
from models.base import BaseModel


class Author(BaseModel, db.Model):
    name = db.Column(db.String(200), nullable=False, unique=True)
    books = db.relationship(
        'Book', secondary='book_authors', back_populates='authors')


book_authors = db.Table('book_authors',
                        db.Column('book_id', db.Integer, db.ForeignKey(
                            'book.id'), primary_key=True),
                        db.Column('author_id', db.Integer, db.ForeignKey(
                            'author.id'), primary_key=True)
                        )
