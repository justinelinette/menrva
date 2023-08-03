from flask import Blueprint, request, redirect
from flask_login import login_required
from models.user_book import UserBook
from controllers.book_controllers import BookController


user_book_views = Blueprint('user_book_views', __name__)


@user_book_views.route('/place_book/<google_book_id>', methods=['POST'])
@login_required
def place_book(google_book_id):
    BookController.place_book(google_book_id)
    return redirect(request.referrer)


@user_book_views.route('/change_book_type/<user_book_id>', methods=['POST'])
@login_required
def change_book_type(user_book_id):
    UserBook.change_book_type(user_book_id)
    return redirect(request.referrer)


@user_book_views.route('/rate_book/<user_book_id>', methods=['POST'])
@login_required
def rate_book(user_book_id):
    UserBook.rate_book(user_book_id)
    return redirect(request.referrer)


@user_book_views.route('/delete_book/<user_book_id>', methods=['POST', 'DELETE'])
@login_required
def delete_book(user_book_id):
    UserBook.delete_book(user_book_id)
    return redirect(request.referrer)
