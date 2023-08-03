
from flask_login import LoginManager, current_user
from flask import Flask, redirect, render_template
from flask_migrate import Migrate
from models.user import User
from views.user_views import user_views
from views.book_views import book_views
from views.user_book_views import user_book_views
from views.shelf_views import shelf_views
from views.review_views import review_views
from views.rating_views import rating_views
from utils.exts import db
from cfg import secret_key


def create_app():
    app = Flask(__name__)
    app.secret_key = secret_key

    # Configure the SQLite databases for users and books
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menrva.db'
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register the blueprints
    app.register_blueprint(user_views, url_prefix='/user')
    app.register_blueprint(book_views, url_prefix='/books')
    app.register_blueprint(user_book_views, url_prefix='/books')
    app.register_blueprint(shelf_views, url_prefix='/books/shelves')
    app.register_blueprint(review_views, url_prefix='/books/review')
    app.register_blueprint(rating_views, url_prefix='/books/rating')
    app.config['UPLOAD_FOLDER'] = 'static/images/pfps'
    login_manager = LoginManager(app)
    login_manager.login_view = 'user_views.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect('/books/home')
        return render_template('index.html.j2')
    return app


app = create_app()
