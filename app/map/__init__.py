from flask import Blueprint, render_template, abort, current_app
from jinja2 import TemplateNotFound
import os
from flask_login import login_required
from app.map.forms import csv_upload
from werkzeug.utils import secure_filename
map = Blueprint('map', __name__,
                        template_folder='templates')

@map.route('/locations/upload', methods=['POST', 'GET'])
@login_required
def upload():
    form = csv_upload()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
    try:
        return render_template('upload_map.html', form=form)
    except TemplateNotFound:
        abort(404)