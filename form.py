from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
from flask_ckeditor import CKEditor


class LoginForm(FlaskForm):
    email=StringField('enter your email',validators=[DataRequired()])
    password=PasswordField('enter your password',validators=[DataRequired()])
    submit=SubmitField("Register")

class FieldForm(FlaskForm):
    name=StringField('enter your name',validators=[DataRequired()])
    email=StringField('enter your email',validators=[DataRequired()])
    password=StringField('enter your password',validators=[DataRequired()])
    submit=SubmitField("Register")

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")
