from flask import Blueprint, request, redirect
from flask_login import login_required
from models.shelf import Shelf
from controllers.shelf_controllers import ShelfController


shelf_views = Blueprint('shelf_views', __name__)


@shelf_views.route('/create_shelf/<type>', methods=['POST'])
@login_required
def create_shelf(type):
    Shelf.create_shelf(type)
    return redirect(request.referrer)


@shelf_views.route('/edit_shelf/<shelf_id>', methods=['POST'])
@login_required
def edit_shelf(shelf_id):
    ShelfController.edit_shelf(shelf_id)
    return redirect(request.referrer)


@shelf_views.route('/delete_shelf/<shelf_id>', methods=['POST', 'DELETE'])
@login_required
def delete_shelf(shelf_id):
    Shelf.delete_shelf(shelf_id)
    return redirect(request.referrer)


@shelf_views.route('/add_to_shelf/<user_book_id>', methods=['POST'])
def add_to_shelf(user_book_id):
    ShelfController.add_to_shelf(user_book_id)
    return redirect(request.referrer)


@shelf_views.route('/remove_from_shelf/<user_book_id>/<shelf_id>', methods=['POST'])
@login_required
def remove_from_shelf(user_book_id, shelf_id):
    Shelf.remove_from_shelf(user_book_id, shelf_id)
    return redirect(request.referrer)
