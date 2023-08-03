from datetime import datetime
import random
from flask import redirect, render_template, request, url_for
from flask_login import current_user
import requests
from cfg import google_api_key
from models.book import Book
from models.review import Review
from models.user_book import UserBook
from models.shelf import Shelf
from utils.util_funcs import UtilFuncs


class ShelfController():
    def add_to_shelf(user_book_id):
        shelf_id = request.form.get('shelf_id')
        Shelf.add_to_shelf(user_book_id, shelf_id)

    def edit_shelf(shelf_id):
        new_name = request.form.get('new_name')
        Shelf.edit_shelf(shelf_id, new_name)
