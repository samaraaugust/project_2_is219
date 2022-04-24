from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class csv_upload(FlaskForm):
    file = FileField()
    submit = SubmitField()

class edit_location(FlaskForm):
    title = TextAreaField('Title', [validators.length(min=1, max=300)])
    #title = TextAreaField('Title', [validators.length(min=1, max=300)])
    submit = SubmitField()