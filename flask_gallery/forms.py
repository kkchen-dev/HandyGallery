from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    key_phrases = StringField("Key Phrases", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Search Title")


class BookDeletion(FlaskForm):
    confirm = BooleanField("Confirm Deletion")
    submit = SubmitField("Delete the Book")