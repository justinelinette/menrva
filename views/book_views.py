from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from controllers.book_controllers import BookController


book_views = Blueprint('book_views', __name__)


@book_views.route('/home', methods=['GET'])
@login_required
def home():
    kwargs = BookController.home()
    return render_template('home.html.j2', **kwargs)


@book_views.route('/home', methods=['POST'])
@login_required
def home_post():
    return redirect(url_for('book_views.search_results', search_query=request.form['search_query']))


@book_views.route('/bookcase/read', methods=['GET'])
@login_required
def read():
    kwargs = BookController.bookcase('read')
    return render_template('read.html.j2', **kwargs)


@book_views.route('/bookcase/read', methods=['POST'])
@login_required
def read_post():
    kwargs = BookController.bookcase('read')
    return render_template('read.html.j2', **kwargs)


@book_views.route('/bookcase/to_be_read', methods=['GET'])
@login_required
def to_be_read_post():
    kwargs = BookController.bookcase('tbr')
    return render_template('to_be_read.html.j2', **kwargs)


@book_views.route('/bookcase/to_be_read', methods=['POST'])
@login_required
def to_be_read():
    kwargs = BookController.bookcase('tbr')
    return render_template('to_be_read.html.j2', **kwargs)


@book_views.route('/search_results')
@login_required
def search_results():
    kwargs = BookController.search_results()
    return render_template('search_results.html.j2', **kwargs)


@book_views.route('/bookcase/sort_books', methods=['POST'])
def sort_books():
    BookController.sort_books()
    return redirect(request.referrer)


@book_views.route('/book_details/<google_book_id>', methods=['GET'])
@login_required
def book_details(google_book_id):
    kwargs = BookController.book_details(google_book_id)
    return render_template('book_details.html.j2', **kwargs)


@book_views.route('/book_details/<google_book_id>', methods=['POST'])
@login_required
def book_details_post(google_book_id):
    BookController.book_details_post()
    kwargs = BookController.book_details(google_book_id)
    return render_template('book_details.html.j2', **kwargs)
