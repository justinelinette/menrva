from datetime import datetime
from flask import flash, request
from flask_login import current_user
from models.book import Book
from models.base import BaseModel
from utils.exts import db


class Rating(BaseModel, db.Model):
    rating = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship('Book', back_populates='ratings')

    def rate_book(book_id):
        rating = request.form.get('rating')
        book = Book.query.get(book_id)
        if book:
            existing_rating = Rating.query.filter_by(
                user_id=current_user.id, book_id=book.id).first()
            if existing_rating:
                existing_rating.update(rating=rating)
            else:
                kwargs = {
                    'rating': rating,
                    'user_id': current_user.id,
                    'book_id': book.id
                }
                rating = Rating.create(**kwargs)
                if rating:
                    flash('Rating updated successfully!', 'success')
                else:
                    flash(
                        'Book not found or you do not have permission to rate it.', 'error')

    def delete_rating(rating_id):
        rating = Rating.query.get(rating_id)
        if not rating:
            flash('Rating not found or you do not have permission to delete it.', 'error')
        else:
            rating.delete()
            flash('Rating deleted successfully.', 'success')
