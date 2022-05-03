from flask import Blueprint, url_for, render_template, abort, current_app, jsonify, flash
from jinja2 import TemplateNotFound
import logging
import os
from app.db.models import Location
import csv
from app.db import db
from flask_login import login_required, current_user
from app.map.forms import csv_upload, edit_location, new_location
from werkzeug.utils import secure_filename, redirect
map = Blueprint('map', __name__,
                        template_folder='templates')

@map.route('/locations_datatables/', methods=['GET', 'POST'])
@login_required
def browse_locations_datatables():
    data = Location.query.all()
    log3 = logging.getLogger("request")
    log3.info("Request Method: browse_locations_datatables")
    retrieve_url = ('map.retrieve_location', [('location_id', ':id')])
    add_url = url_for('map.add_location')
    delete_url = ('map.delete_location', [('location_id', ':id')])
    edit_url = ('map.edit_locations', [('location_id', ':id')])
    try:
        return render_template('browse_datatables.html', delete_url=delete_url, add_url=add_url, edit_url=edit_url, retrieve_url=retrieve_url, Location=Location, data=data)
    except TemplateNotFound:
        abort(404)

@map.route('/locations/map/<int:location_id>')
@login_required
def retrieve_location(location_id):
    log3 = logging.getLogger("request")
    log3.info("Request Method: retrieve_locations")
    location = Location.query.get(location_id)
    return render_template('location_view.html', location=location)

@map.route('/locations/new', methods=['POST', 'GET'])
@login_required
def add_location():
    log3 = logging.getLogger("request")
    log3.info("Request Method: add_location")
    form = new_location()
    if form.validate_on_submit():
        location = Location(title=form.title.data, longitude=form.longitude.data, latitude=form.latitude.data, population=form.population.data)
        current_user.locations = current_user.locations + [location]
        db.session.commit()
        flash('Congratulations, you just add a new location', 'success')
        return redirect(url_for('map.browse_locations_datatables'))

    return render_template('new_location.html', form=form)

@map.route('/locations/<int:location_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_locations(location_id):
    log3 = logging.getLogger("request")
    log3.info("Request Method: edit_locations")
    location = Location.query.get(location_id)
    form = edit_location(obj=location)
    if form.validate_on_submit():
        location.title = form.title.data
        location.longitude = form.longitude.data
        location.latitude = form.latitude.data
        location.population = form.population.data
        db.session.add(location)
        db.session.commit()
        flash('Location Edited Successfully', 'success')
        return redirect(url_for('map.browse_locations_datatables'))
    return render_template('location_edit.html', form=form)

@map.route('/locations/<int:location_id>/delete', methods=['POST'])
@login_required
def delete_location(location_id):
    log3 = logging.getLogger("request")
    log3.info("Request Method: delete_location")
    location = Location.query.get(location_id)
    db.session.delete(location)
    db.session.commit()
    flash('Location Deleted', 'success')
    return redirect(url_for('map.browse_locations_datatables'), 302)

@map.route('/api/locations/', methods=['GET'])
@login_required
def api_locations():
    log3 = logging.getLogger("request")
    log3.info("Request Method: api_locations")
    data = Location.query.all()
    try:
        return jsonify(data=[location.serialize() for location in data])
    except TemplateNotFound:
        abort(404)


@map.route('/locations/map', methods=['GET'])
@login_required
def map_locations():
    log3 = logging.getLogger("request")
    log3.info("Request Method: map_locations")
    google_api_key = current_app.config.get('GOOGLE_API_KEY')
    try:
        return render_template('map_locations.html', google_api_key=google_api_key)
    except TemplateNotFound:
        abort(404)

@map.route('/locations/upload', methods=['POST', 'GET'])
@login_required
def upload():
    log3 = logging.getLogger("request")
    log3.info("Request Method: upload")
    form = csv_upload()
    if form.validate_on_submit():
        log = logging.getLogger("myApp")
        log2 = logging.getLogger("csv")
        filename = secure_filename(form.file.data.filename)
        log2.info("CSV Uploaded: " + filename)
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
        return redirect(url_for('map.browse_locations_datatables'))
    try:
        return render_template('upload_map.html', form=form)
    except TemplateNotFound:
        abort(404)