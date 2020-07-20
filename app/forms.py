from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired


class ItemForm(FlaskForm):
    media = SelectField(
        'Media', choices=[('Book', 'Book'), ('Audio CD', 'Audio CD'), ('DVD', 'DVD')]) # noqa
    author = StringField('Author')
    title = StringField('Book title', validators=[DataRequired()])
    opinion = TextAreaField('Opinion')
    rented = BooleanField('Hired')


class AuthorForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    desc = StringField('desc', validators=[])
