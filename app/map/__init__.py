from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

map = Blueprint('map', __name__,
                        template_folder='templates')

@map.route('/upload')
def upload():
    try:
        return render_template('upload_map.html')
    except TemplateNotFound:
        abort(404)