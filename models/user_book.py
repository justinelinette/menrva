from datetime import datetime
from flask import flash, request
from flask_login import current_user
from models.book import Book
from models.base import BaseModel
from utils.exts import db


class UserBook(BaseModel, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    type = db.Column(db.String())
    book = db.relationship('Book', back_populates='user_books')

    def place_book(google_book_id, type):
        user = current_user
        book = Book.fetch_or_create(google_book_id)
        if not user or not book:
            return flash('Book not found or you do not have permission to place it.', 'error')
        user_book = UserBook.query.filter_by(
            user_id=current_user.id, book_id=google_book_id).first()
        if user_book:
            if user_book.type == 'tbr':
                return flash(
                    'You have already placed this book in your To Be Read bookcase.', 'error')
            elif user_book.type == 'read':
                return flash(
                    'You have already placed this book in your Read bookcase.', 'error')
        kwargs = {
            'user': user,
            'book': book,
            'type': type
        }
        user_book = UserBook.create(**kwargs)
        flash('Book logged successfully!', 'success')

    def change_book_type(user_book_id):
        book = UserBook.query.get(user_book_id)
        if book:
            if book.type == 'read':
                book.update(type='tbr', created=datetime.utcnow())
                flash('Book moved to "To Be Read" successfully!', 'success')
            elif book.type == 'tbr':
                book.update(type='read', created=datetime.utcnow())
                flash('Book moved to "Read" successfully!', 'success')
        else:
            flash('Book not found or you do not have permission to move it.', 'error')

    def delete_book(user_book_id):
        book = UserBook.query.get(user_book_id)
        if book:
            book.delete()
            flash('Book deleted successfully!', 'success')
        else:
            flash('Book not found or you do not have permission to delete it.', 'error')
