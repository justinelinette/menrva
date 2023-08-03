from flask import request, redirect, url_for, flash
from flask_login import current_user, login_user
from utils.exts import db
from models.user import User


class UserController():

    def register():
        email = request.form.get('email')
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return flash('Passwords do not match.', 'error')
        else:
            user_by_username = User.query.filter_by(username=username).first()
            user_by_email = User.query.filter_by(email=email).first()

        if user_by_username:
            return flash(
                'Username already exists. Please choose a different username.', 'error')
        elif user_by_email:
            return flash(
                'Email already exists. Please choose a different email address.', 'error')
        else:
            kwargs = {
                'email': email,
                'username': username,
                'first_name': first_name,
                'last_name': last_name
            }
            new_user = User(**kwargs)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(username=username).first()
            if user:
                login_user(new_user)
                flash(
                    'Account created successfully! You are now logged in.', 'success')
                return redirect(url_for('book_views.home'))
            else:
                return flash('Failed to create an account. Please try again.', 'error')

    def login():
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('book_views.home'))
        else:
            return flash('Invalid username or password. Please try again.', 'error')

    def user_settings():
        form_type = request.form.get('form_type')
        user = current_user

        if form_type == 'change_username':
            new_username = request.form.get('new_username')
            user.update(username=new_username)

        elif form_type == 'change_email':
            new_email = request.form.get('new_email')
            user.update(email=new_email)

        elif form_type == 'change_password':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_new_password = request.form.get('confirm_new_password')
            User.change_password(
                current_password, new_password, confirm_new_password)

        elif form_type == 'set_yearly_goal':
            yearly_goal = request.form.get('yearly_goal')
            goal_type = request.form.get('goal_type')
            user.update(yearly_goal=yearly_goal, goal_type=goal_type)

        elif form_type == 'upload_profile_image':
            profile_image = request.files.get('profile_image')
            User.upload_profile_image(profile_image)
