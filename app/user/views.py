from app.user import blueprint_user
from flask import render_template

@blueprint_user.route('/<username>')
def user(username):
    return render_template('user/user.html', user=user, title='User page')