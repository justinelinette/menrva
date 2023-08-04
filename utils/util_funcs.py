from collections import Counter
from datetime import datetime
from flask_login import current_user
from sqlalchemy import desc
from models.book import Book
from models.rating import Rating
from models.review import Review
from models.user_book import UserBook


class UtilFuncs():

    def get_booklist(type, sort):
        user = current_user
        sort_options = {
            'title': Book.title,
            'author': Book.authors,
            'created': UserBook.created,
            'rating': Rating.rating,
            'pages': Book.pages
        }
        sort_attr = sort_options.get(sort, UserBook.created)

        query = user.user_books.filter_by(type=type)
        if sort in ('title', 'author', 'pages'):
            query = query.join(UserBook.book).order_by(sort_attr)
        elif sort == 'rating':
            query = query.join(UserBook.book).join(
                Book.ratings).order_by(desc(Rating.rating))
        elif sort == 'created':
            query = query.order_by(desc(UserBook.created))
        user_books = query.all()
        return user_books

    def log_check(google_book_id):
        user_book = UserBook.query.filter_by(
            user_id=current_user.id, book_id=google_book_id).first()
        if user_book:
            logged = True
        else:
            logged = False
        return logged

    def avg_rating(ratings):
        total_ratings = 0
        num_ratings = 0
        for rating in ratings:
            if rating.rating != None:
                total_ratings += rating.rating
                num_ratings += 1
        if num_ratings == 0:
            avg_rating = 0
        else:
            raw_avg = (total_ratings / num_ratings)
            avg_rating = round(raw_avg)
        return avg_rating

    def days_left():
        current_date = datetime.now()
        end_of_year = datetime(current_date.year, 12, 31)
        time_left = end_of_year - current_date
        days_left = time_left.days
        return days_left

    def get_books_this_year(books, current_year):
        start_of_year = datetime(current_year, 1, 1)
        end_of_year = datetime(current_year, 12, 31)
        return [book for book in books if start_of_year <= book.created <= end_of_year]

    def get_total_pages(books):
        return sum(book.book.pages for book in books)

    def get_shelves_by_type(user_shelves, shelf_type):
        return [shelf for shelf in user_shelves if shelf.type == shelf_type]

    def calculate_progress(completed):
        current_year = datetime.now().year
        start_of_year = datetime(current_year, 1, 1).date()
        days_passed = (datetime.now().date() - start_of_year).days

        total_goal = current_user.goal.amount
        daily_rate = total_goal / 365
        benchmark = daily_rate * days_passed
        difference = completed - benchmark
        if completed > benchmark:
            status = 'ahead of'
        elif completed < benchmark:
            status = 'behind'
        else:
            status = 'on track'
        if completed >= total_goal:
            status = 'achieved'
        ahead_behind = round(difference)
        if status == 'behind':
            ahead_behind = ahead_behind * -1
        return f'{ahead_behind:,}', status

    def calculate_avg_length():
        user = current_user
        short = 0
        medium = 0
        long = 0
        extra_long = 0

        for user_book in user.user_books:
            page_count = user_book.book.pages

            if page_count <= 250:
                short += 1
            elif 251 <= page_count <= 499:
                medium += 1
            elif 500 <= page_count <= 999:
                long += 1
            else:
                extra_long += 1

        max_count = max(short, medium, long, extra_long)
        if max_count == short:
            avg_length = 'short'
        elif max_count == medium:
            avg_length = 'medium'
        elif max_count == long:
            avg_length = 'long'
        else:
            avg_length = 'extra-long'
        return avg_length

    def get_top_genres(user_books):
        all_genres = []
        for user_book in user_books:
            genres = user_book.book.genres
            all_genres.extend(genres)

        genre_counts = Counter(all_genres)
        most_common_genres = genre_counts.most_common(3)
        top_genres = [genre for genre, count in most_common_genres]

        return top_genres
