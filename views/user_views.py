from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, logout_user
from controllers.user_controllers import UserController

user_views = Blueprint('user_views', __name__)


@user_views.route('/register', methods=['GET'])
def register():
    return render_template('register.html.j2')


@user_views.route('/register', methods=['POST'])
def register_post():
    UserController.register()
    return redirect(url_for('book_views.home'))


@user_views.route('/login', methods=['GET'])
def login():
    return render_template('login.html.j2')


@user_views.route('/login', methods=['POST'])
def login_post():
    UserController.login()
    return redirect(url_for('book_views.home'))


@user_views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_views.login'))


@user_views.route('/user_settings', methods=['GET'])
@login_required
def user_settings():
    return render_template('user_settings.html.j2')


@user_views.route('/user_settings', methods=['POST'])
@login_required
def user_settings_post():
    UserController.user_settings()
    return render_template('user_settings.html.j2')
