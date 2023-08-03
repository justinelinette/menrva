from flask import Blueprint, request, redirect
from flask_login import login_required
from models.rating import Rating


rating_views = Blueprint('rating_views', __name__)


@rating_views.route('/rate_book/<book_id>', methods=['POST'])
@login_required
def rate_book(book_id):
    Rating.rate_book(book_id)
    return redirect(request.referrer)


@rating_views.route('/delete_rating/<rating_id>', methods=['POST', 'DELETE'])
@login_required
def delete_rating(rating_id):
    Rating.delete_rating(rating_id)
    return redirect(request.referrer)
