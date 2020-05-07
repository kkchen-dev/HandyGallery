from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Length


class ToggleRead(FlaskForm):
    submit = SubmitField("Toggle Read")


class SearchForm(FlaskForm):
    key_phrases = StringField("Key Phrases", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Search Title")