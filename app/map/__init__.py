from flask import Blueprint, url_for, render_template, abort, current_app, jsonify
from jinja2 import TemplateNotFound
import logging
import os
from app.db.models import Location
import csv
from app.db import db
from flask_login import login_required, current_user
from app.map.forms import csv_upload
from werkzeug.utils import secure_filename, redirect
map = Blueprint('map', __name__,
                        template_folder='templates')


@map.route('/locations', methods=['GET'], defaults={"page": 1})
@map.route('/locations/<int:page>', methods=['GET'])
def browse_locations(page):
    page = page
    per_page = 20
    pagination = Location.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    try:
        return render_template('browse_locations.html',data=data,pagination=pagination)
    except TemplateNotFound:
        abort(404)

@map.route('/api/locations/', methods=['GET'])
def api_locations():
    data = Location.query.all()
    try:
        return jsonify(data=[location.serialize() for location in data])
    except TemplateNotFound:
        abort(404)


@map.route('/locations/map', methods=['GET'])
def map_locations():
    google_api_key = current_app.config.get('GOOGLE_API_KEY')
    #log = logging.getLogger("myApp")
    #log.info(google_api_key)
    try:
        return render_template('map_locations.html',google_api_key=google_api_key)
    except TemplateNotFound:
        abort(404)

@map.route('/locations/upload', methods=['POST', 'GET'])
@login_required
def upload():
    form = csv_upload()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        list_of_locations = []
        with open(filepath) as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                list_of_locations.append(
                    Location(row['location'], row['longitude'], row['latitude'], row['population']))

        current_user.locations = list_of_locations
        db.session.commit()
        return redirect(url_for('map.browse_locations'))
    try:
        return render_template('upload_map.html', form=form)
    except TemplateNotFound:
        abort(404)