from wtforms import SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from flask_wtf import FlaskForm

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=64)])
    body = TextAreaField("Body", validators=[DataRequired(), Length(min=3, max=1024)])
    submit = SubmitField('Submit')