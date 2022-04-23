from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from app.map.forms import csv_upload
map = Blueprint('map', __name__,
                        template_folder='templates')

@map.route('/locations/upload')
def upload():
    form = csv_upload()
    try:
        return render_template('upload_map.html', form=form)
    except TemplateNotFound:
        abort(404)