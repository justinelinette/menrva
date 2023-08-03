from datetime import datetime
from flask import request, flash
from flask_login import current_user
from models.user_book import UserBook
from models.base import BaseModel
from utils.exts import db

book_shelf = db.Table('book_shelf',
                      db.Column('shelf_id', db.Integer,
                                db.ForeignKey('shelf.id')),
                      db.Column('user_book_id', db.Integer,
                                db.ForeignKey('user_book.id'))
                      )


class Shelf(BaseModel, db.Model):
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    books = db.relationship('UserBook', secondary=book_shelf,
                            backref='shelves', lazy='dynamic')

    def create_shelf(type):
        name = request.form.get('name')
        shelf_info = {
            'user_id': current_user.id,
            'name': name,
            'type': type
        }
        shelf = Shelf.create(**shelf_info)
        if not shelf:
            return flash("Error creating shelf.", "error")
        else:
            return flash(f"{shelf.name} shelf successfully created!", "success")

    def edit_shelf(shelf_id, new_name):
        shelf = Shelf.query.filter_by(id=shelf_id).first()
        if not shelf:
            return flash("You do not have permission to edit this shelf.", "error")
        if not shelf.user_id == current_user.id:
            return flash("You don't have permission to delete this shelf.", "error")
        shelf.update(name=new_name)
        return flash(
            f"Shelf name successfully changed to: {shelf.name}!", "success")

    def delete_shelf(shelf_id):
        shelf = Shelf.query.filter_by(id=shelf_id).first()
        if not shelf:
            return flash("Shelf not found.", "error")
        if not shelf.user_id == current_user.id:
            return flash("You don't have permission to delete this shelf.", "error")
        shelf.delete()
        flash("Shelf successfully deleted!", "success")

    def add_to_shelf(user_book_id, shelf_id):
        user_book = UserBook.query.get(user_book_id)
        shelf = Shelf.query.get(shelf_id)
        if user_book in shelf.books:
            return flash("Book is already on this shelf.", "error")
        if not shelf:
            return flash("Shelf not found or you don't have permission to add a book to it.", "error")
        if not user_book:
            return flash("Book not found.", "error")
        if user_book.user != current_user:
            return flash("You don't have permission to add a book to this shelf.", "error")
        shelf.books.append(user_book)
        db.session.commit()
        flash("Book successfully added to the shelf.", "success")

    def remove_from_shelf(user_book_id, shelf_id):
        user_book = UserBook.query.get(user_book_id)
        shelf = Shelf.query.get(shelf_id)

        if not shelf:
            return flash("You don't have permission to remove a book from this shelf.", "error")
        if not user_book:
            return flash("Book not found.", "error")
        if user_book.user != current_user:
            return flash("You don't have permission to remove a book from this shelf.", "error")
        if user_book in shelf.books:
            shelf.books.remove(user_book)
            db.session.commit()
            flash("Book successfully removed from the shelf.", "success")
        else:
            flash("The book is not in the shelf.", "error")
