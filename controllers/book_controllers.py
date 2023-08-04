from datetime import datetime
import random
from flask import request
from flask_login import current_user
import requests
from cfg import google_api_key
from models.book import Book
from models.rating import Rating
from models.review import Review
from models.user_book import UserBook
from models.shelf import Shelf
from utils.util_funcs import UtilFuncs


class BookController():
    def home():
        user = current_user
        current_year = datetime.now().year
        tbr_books = UtilFuncs.get_booklist('tbr', 'created')
        read_books = UtilFuncs.get_booklist('read', 'created')
        books_this_year = UtilFuncs.get_books_this_year(
            read_books, current_year)
        pages_this_year = UtilFuncs.get_total_pages(books_this_year)
        tbr_shelves = UtilFuncs.get_shelves_by_type(
            user.shelves, 'tbr')
        read_shelves = UtilFuncs.get_shelves_by_type(
            user.shelves, 'read')

        kwargs = {
            'username': user.username,
            'pfp': user.pfp,
            'user_shelves': user.shelves,
            'tbr_books': tbr_books,
            'read_books': read_books,
            'tbr_shelves': tbr_shelves,
            'read_shelves': read_shelves,
            'books_this_year': len(books_this_year),
            'pages_this_year': pages_this_year,
            'total_pages': UtilFuncs.get_total_pages(read_books),
            'days_left': UtilFuncs.days_left(),
            'avg_length': UtilFuncs.calculate_avg_length(),
            'top_genres': UtilFuncs.get_top_genres(read_books),
            'avg_user_rating': UtilFuncs.avg_rating(user.ratings)
        }
        if tbr_books:
            kwargs['up_next'] = random.choice(tbr_books)
        goal = user.goal
        if goal:
            kwargs['goal_amount'] = f'{goal.amount:,}'
            kwargs['goal_type'] = user.goal.type
            if user.goal.type == 'books':
                completed = len(books_this_year)
            elif user.goal.type == 'pages':
                completed = pages_this_year
            kwargs['goal_left'] = f'{(goal.amount - completed):,}'
            kwargs['goal_percentage'] = completed / goal.amount * 100
            kwargs['progress'], kwargs['status'] = UtilFuncs.calculate_progress(
                completed)
        return kwargs

    def bookcase(type):
        sort = request.form.get('sort', 'created')
        kwargs = {
            'user': current_user,
            'username': current_user.username,
            'user_books': UtilFuncs.get_booklist(type, sort),
            'shelves': [shelf for shelf in current_user.shelves if shelf.type == type]
        }
        return kwargs

    def book_details(google_book_id):
        book = Book.fetch_or_create(google_book_id)
        reviews = Review.query.filter_by(book_id=book.id).all()
        ratings = Rating.query.filter_by(book_id=book.id).all()
        avg_rating = UtilFuncs.avg_rating(ratings)
        user_book = UserBook.query.filter_by(
            book_id=book.id, user_id=current_user.id).first()
        kwargs = {
            'book': book,
            'user_book': user_book,
            'logged': UtilFuncs.log_check(google_book_id),
            'reviews': reviews,
            'avg_rating': avg_rating,
            'user_review': Review.query.filter_by(book_id=book.id, user_id=current_user.id).first(),
            'user_rating': Rating.query.filter_by(book_id=book.id, user_id=current_user.id).first()
        }
        if user_book:
            kwargs['shelves'] = user_book.shelves
            if current_user.shelves:
                type = user_book.type
                kwargs['user_shelves'] = [
                    shelf for shelf in current_user.shelves if shelf.type == type]
        else:
            kwargs['shelves'] = None
            kwargs['user_shelves'] = None
        return kwargs

    def search_results():
        search_query = request.args.get('search_query')
        url = f'https://www.googleapis.com/books/v1/volumes?q={search_query}&maxResults={40}&key={google_api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            search_results = response.json().get('items', [])
            kwargs = {
                'search_results': search_results,
                'search_query': search_query
            }
            return kwargs
        else:
            return "Error fetching books from Google Books API"

    def place_book(google_book_id):
        type = request.form.get('book_type')
        UserBook.place_book(google_book_id, type)
