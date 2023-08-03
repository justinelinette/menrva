from flask import Blueprint, request, redirect
from flask_login import login_required
from models.review import Review


review_views = Blueprint('review_views', __name__)


@review_views.route('/review_book/<book_id>', methods=['POST'])
@login_required
def review_book(book_id):
    Review.review_book(book_id)
    return redirect(request.referrer)


@review_views.route('/delete_review/<review_id>', methods=['POST', 'DELETE'])
@login_required
def delete_review(review_id):
    Review.delete_review(review_id)
    return redirect(request.referrer)
