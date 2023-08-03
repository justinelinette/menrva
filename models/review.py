from datetime import datetime
from flask import flash, request
from flask_login import current_user
from models.book import Book
from models.base import BaseModel
from utils.exts import db


class Review(BaseModel, db.Model):
    title = db.Column(db.String(75))
    body = db.Column(db.String(2000), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship('Book', back_populates='reviews')

    def review_book(book_id):
        body = request.form.get('review')
        title = request.form.get('title')
        if not title:
            title = f"{current_user.username}'s Review"
        book = Book.query.get(book_id)
        print(title)
        if book:
            existing_review = Review.query.filter_by(
                user_id=current_user.id, book_id=book.id).first()
            if existing_review:
                existing_review.update(body=body, title=title)
            else:
                kwargs = {
                    'body': body,
                    'title': title,
                    'user_id': current_user.id,
                    'book_id': book.id
                }
                review = Review.create(**kwargs)
                if review:
                    flash('Review updated successfully!', 'success')
                else:
                    flash(
                        'Book not found or you do not have permission to review it.', 'error')

    def delete_review(review_id):
        review = Review.query.get(review_id)
        if not review:
            flash('Review not found or you do not have permission to delete it.', 'error')
        else:
            review.delete()
            flash('Review deleted successfully.', 'success')
