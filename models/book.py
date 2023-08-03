import requests
from cfg import google_api_key
from models.author import Author
from models.genre import Genre
from models.base import BaseModel
from utils.exts import db


class Book(BaseModel, db.Model):
    google_book_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    pages = db.Column(db.Integer, nullable=True)
    cover = db.Column(db.String(200), nullable=True)
    publisher = db.Column(db.String(200), nullable=True)
    date_published = db.Column(db.String(200), nullable=True)
    summary = db.Column(db.String(), nullable=True)
    authors = db.relationship(
        'Author', secondary='book_authors', back_populates='books')
    genres = db.relationship(
        'Genre', secondary='book_genres', back_populates='books')
    user_books = db.relationship(
        'UserBook', back_populates='book', lazy='dynamic')
    reviews = db.relationship('Review', back_populates='book', lazy='dynamic')
    ratings = db.relationship('Rating', back_populates='book', lazy='dynamic')

    def fetch_or_create(google_book_id):
        book = Book.query.filter_by(google_book_id=google_book_id).first()
        if not book:
            api_key = google_api_key
            url = f'https://www.googleapis.com/books/v1/volumes/{google_book_id}?key={api_key}'
            response = requests.get(url)
            if response.status_code == 200:
                book_data = response.json()
                if 'volumeInfo' in book_data:
                    book_info = {
                        'google_book_id': book_data.get('id'),
                        'title': book_data['volumeInfo'].get('title', 'Unknown Title'),
                        'pages': book_data['volumeInfo'].get('pageCount', ['Unknown Pagecount']),
                        'summary': book_data['volumeInfo'].get('description', ['No summary available']),
                        'publisher': book_data['volumeInfo'].get('publisher', 'Unknown Publisher'),
                        'date_published': book_data['volumeInfo'].get('publishedDate', 'Unknown Published Date'),
                        'cover': book_data['volumeInfo'].get('imageLinks', {}).get('thumbnail', '').replace('&edge=curl', '').replace('&z=0', '&z=1'),
                    }

                    authors_data = book_data['volumeInfo'].get(
                        'authors', ['Unknown Author'])
                    authors = []
                    for author_name in authors_data:
                        author = Author.query.filter_by(
                            name=author_name).first()
                        if not author:
                            author = Author(name=author_name)
                            db.session.add(author)
                        authors.append(author)
                    genres_data = book_data['volumeInfo'].get('categories', [])
                    genres = []
                    for genre_string in genres_data:
                        genre_list = [genre.strip()
                                      for genre in genre_string.split('/')]
                        for genre_name in genre_list:
                            genre = Genre.query.filter_by(
                                name=genre_name).first()
                            if not genre:
                                genre = Genre(name=genre_name)
                                db.session.add(genre)
                            if genre not in genres:
                                genres.append(genre)

                    book = Book(**book_info)
                    book.authors = authors
                    book.genres = genres
                    db.session.add(book)
                    db.session.commit()
                    print(book.authors)
                else:
                    raise ValueError(
                        'Book details not found in Google Books API.')
            else:
                raise ValueError('Error fetching data from Google Books API.')

        return book
