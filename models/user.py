
from datetime import datetime
import os
from flask import current_app, flash
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models.base import BaseModel
from utils.exts import db


class User(UserMixin, BaseModel, db.Model):
    email = db.Column(db.String(), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    first_name = db.Column(db.String(64), unique=True, nullable=False)
    last_name = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    yearly_goal = db.Column(db.Integer, nullable=True)
    goal_type = db.Column(db.String(10), nullable=True)
    pfp = db.Column(db.String())
    profile_type = db.Column(db.String(10), default='public')
    shelves = db.relationship('Shelf', backref='user', lazy=True)
    user_books = db.relationship('UserBook', backref='user', lazy='dynamic')
    reviews = db.relationship('Review', backref='user', lazy='dynamic')
    ratings = db.relationship('Rating', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def allowed_img(filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def is_username_available(new_username):
        user = User.query.filter_by(username=new_username).first()
        return user is None

    def change_username(new_username):
        user = current_user
        if new_username:
            if User.is_username_available(new_username):
                user.update(username=new_username)
                flash('Username changed successfully!', 'success')
            else:
                flash('Username already taken. Please choose another.', 'error')

    def is_email_available(new_email):
        user = User.query.filter_by(email=new_email).first()
        return user is None

    def change_email(new_email):
        user = current_user
        if new_email:
            if User.is_email_available(new_email):
                user.update(email=new_email)
                flash('Email changed successfully!', 'success')
            else:
                flash('Email already in use. Please use another.', 'error')

    def change_password(current_password, new_password, confirm_new_password):
        if current_password and new_password and confirm_new_password:
            if current_user.check_password(current_password):
                if new_password == confirm_new_password:
                    current_user.set_password(new_password)
                    db.session.commit()
                    flash('Password changed successfully!', 'success')
                else:
                    flash('New password and confirm password do not match.', 'error')
            else:
                flash('Current password is incorrect.', 'error')

    def set_yearly_goal(yearly_goal, goal_type):
        user = current_user
        if yearly_goal:
            try:
                yearly_goal = int(yearly_goal)
                user.update(yearly_goal=yearly_goal, goal_type=goal_type)
                flash('Yearly reading goal set successfully!', 'success')
            except ValueError:
                flash('Please enter a valid number for the yearly goal.', 'error')

    def upload_profile_image(profile_image):
        user = current_user
        if profile_image and User.allowed_img(profile_image.filename):
            filename = secure_filename(profile_image.filename)
            profile_image.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename))
            user.update(pfp=filename)
            flash('Profile image uploaded successfully!', 'success')
        else:
            flash('Invalid file format. Please upload an image.', 'error')
