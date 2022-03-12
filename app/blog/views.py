from app.blog import blueprint_blog
from flask import render_template, redirect, url_for, request, current_app
from flask_login import login_required, login_user, logout_user, current_user
from app import db
from app.models import User
from .forms import PostForm


@blueprint_blog.route('/<username>/new', methods=['GET', 'POST'])
def new_post(username):
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
        form.validate_on_submit():
        post = Post(body=form.body.data,
        author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form, posts=posts)
    return render_template('blog/new.html', title='New Post')