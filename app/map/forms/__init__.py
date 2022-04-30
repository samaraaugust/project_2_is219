from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class csv_upload(FlaskForm):
    file = FileField()
    submit = SubmitField()

class edit_location(FlaskForm):
    title = TextAreaField('Title', [validators.length(min=1, max=300)])
    longitude = TextAreaField('Longitude', [validators.length(min=1, max=300)])
    latitude = TextAreaField('Latitude', [validators.length(min=1, max=300)])
    population = TextAreaField('Population', [validators.length(min=1, max=300)])
    submit = SubmitField()

class new_location(FlaskForm):
    title = TextAreaField('Title', [validators.length(min=1, max=300)])
    longitude = TextAreaField('Longitude', [validators.length(min=1, max=300)])
    latitude = TextAreaField('Latitude', [validators.length(min=1, max=300)])
    population = TextAreaField('Population', [validators.length(min=1, max=300)])
    submit = SubmitField()