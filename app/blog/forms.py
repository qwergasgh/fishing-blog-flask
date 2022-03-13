from wtforms import SubmitField, StringField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, InputRequired
from flask_wtf.file import FileRequired, FileAllowed
from flask_wtf import FlaskForm


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=64)])
    body = TextAreaField("Body", validators=[DataRequired(), Length(min=3, max=1024)])
    images = MultipleFileField('Upload images',
                               validators=[FileRequired(),
                                           FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField('Save', validators=[InputRequired()])

    def validate(self):
        if self.title is None:
            return False
        if self.body is None:
            return False
        return True

