from app.user import blueprint_user
from flask import render_template, redirect, url_for, request, current_app, abort
from flask_login import login_required, login_user, logout_user, current_user
from app import db, app
from app.models import User, Role
from app.utils import send_password_reset_email, get_avatar
from .forms import RegisterForm, LoginForm, EditProfileForm, ResetPasswordForm, ResetPasswordForm_token
from werkzeug.utils import secure_filename
import os


@blueprint_user.route('/<username>')
def user(username):
    user = User.query.filter_by(user_name=username).first()
    if user is None:
        abort(404)
    avatar = get_avatar(current_user.avatar)
    return render_template('user/user.html', 
                           user=user, 
                           avatar_path=avatar, 
                           title='User page')


@blueprint_user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        if email in current_app.config['ADMINS']:
            role_id = Role.query.filter_by(privilege=True).first()
        user = User(email=form.email.data,
                    user_name=form.user_name.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    phonenumber=form.phonenumber.data,
                    password=form.password.data,
                    role_id=role_id)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('blueprint_user.login'))
    return render_template('user/register.html', title='Register', form=form)


@blueprint_user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('blueprint_app.home'))
    return render_template('user/login.html', title='Login', form=form)


@blueprint_user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blueprint_app.home'))


@blueprint_user.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    name = current_user.user_name
    form = EditProfileForm()
    if form.validate_on_submit():
        file = form.avatar.data
        file_type = file.filename.split('.')[-1]
        file_name = f'{name}.{file_type}'
        file_path = os.path.join(app.config['AVATAR_DIR'], file_name)
        file.save(file_path)
        current_user.avatar = file_path
        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phonenumber = form.phonenumber.data
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('blueprint_user.edit_profile'))
    avatar = get_avatar(current_user.avatar)
    form.user_name.data = current_user.user_name
    form.email.data = current_user.email
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.phonenumber.data = current_user.phonenumber
    return render_template('user/edit_profile.html',
                           title=f"Edit profile {name}",
                           form=form,
                           name=name,
                           avatar_path=avatar)


@blueprint_user.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            send_password_reset_email(user)
        return redirect(url_for('blueprint_user.login'))
    return render_template('user/reset_password.html',
                           title='Reset Password',
                           form=form)


@blueprint_user.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('blueprint_app.index'))
    form = ResetPasswordForm_token()
    if form.validate_on_submit():
        user.password(form.password.data)
        db.session.commit()
        return redirect(url_for('blueprint_user.login'))
    return render_template('user/reset_password_token.html', form=form)
