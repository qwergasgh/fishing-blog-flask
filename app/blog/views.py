from app.blog import blueprint_blog
from flask import render_template, redirect, url_for
from flask_login import login_required
from app.models import User, Post
from .forms import PostForm
from app import db

@login_required
@blueprint_blog.route('/<username>/new', methods=['GET', 'POST'])
def new_post(username):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, 
                    body=form.body.data, 
                    user_id=User.query.order_by(user_name=username).first())
        db.session.add(post)
        return redirect(url_for('blueprint_blog.posts', username=username))
    return render_template('blog/new.html', title='New Post', form=form)

@login_required
@blueprint_blog.route('/<username>')
def posts(username):
    posts = Post.query.order_by(user_id=User.query.order_by(user_name=username)).all()
    return render_template('blog/posts.html', title=f'{username} Posts', posts=posts)
