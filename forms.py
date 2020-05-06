from flask_wtf import FlaskForm
from wtforms import SubmitField


class ToggleRead(FlaskForm):
    submit = SubmitField("Toggle Read")