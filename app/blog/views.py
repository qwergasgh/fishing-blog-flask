from app.blog import blueprint_blog
from flask import render_template, redirect, url_for, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Post, ImagePost
from .forms import PostForm
from app import db, app
import os


@login_required
@blueprint_blog.route('/<username>/new', methods=['GET', 'POST'])
def new_post(username):
    form = PostForm()
    if form.validate_on_submit():
        user_id = User.query.filter_by(user_name=username).first().id
        if len(form.images.data) > 1:
            images = True
        else:
            images = False
        post = Post(title=form.title.data, 
                    body=form.body.data, 
                    user_id=user_id,
                    images=images)
        db.session.add(post)
        db.session.commit()
        item = 0
        if images:
            for _image in form.images.data:
                file_type = _image.filename.split('.')[-1]
                file_name = f'{post.id}_{item}.{file_type}'
                file_path = os.path.join(app.config['UPLOAD_DIR_PATH'], file_name)
                _image.save(file_path)
                file_db_path = os.path.join(app.config['UPLOAD_DIR'], file_name)
                image = ImagePost(user_id=user_id, post_id=post.id, path=file_db_path)
                db.session.add(image)
                item += 1
            db.session.commit()
        return redirect(url_for('blueprint_blog.posts_user', username=username))
    return render_template('blog/new_post.html', title='New Post', form=form, files=None)


@login_required
@blueprint_blog.route('/<username>', methods=['GET', 'POST'])
def posts_user(username):
    id_user = User.query.filter_by(user_name=username).first().id
    posts = Post.query.filter_by(user_id=id_user).all()
    return render_template('blog/posts.html', title=f'Posts by {username}', posts=posts)


# @login_required
# @blueprint_blog.route('/upload_image/<filename>')
# def upload_image(filename):
#     return send_from_directory(os.path.join(
#         app.config['UPLOAD_PATH'], current_user.get_id()), filename)


@login_required
@blueprint_blog.route('/get_images', methods=['POST'])
def get_images():
    try:
        if request.method == 'POST':
            id_post = int(request.json['id_post'])
            path_images = [img.path for img in ImagePost.query.filter_by(post_id=id_post).all()]
            return jsonify({'valid': 'True', 'path_images': path_images}), 200
    except:
        return jsonify({'valid': 'False'}), 400
