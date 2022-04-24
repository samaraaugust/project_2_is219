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

@map.route('/locations_datatables/', methods=['GET'])
def browse_locations_datatables():
    data = Location.query.all()
    retrieve_url = ('map.retrieve_location', [('location_id', ':id')])
    add_url = url_for('map.add_location')
    delete_url = ('map.delete_location', [('location_id', ':id')])
    try:
        return render_template('browse_datatables.html', delete_url=delete_url, add_url=add_url,retrieve_url=retrieve_url, Location=Location, data=data)
    except TemplateNotFound:
        abort(404)

@map.route('/locations/map/<int:location_id>')
def retrieve_location(location_id):
    location = Location.query.get(location_id)
    return render_template('location_view.html', location=location)

@map.route('/locations', methods=['GET'], defaults={"page": 1})
@map.route('/locations/<int:page>', methods=['GET'])
def browse_locations(page):
    page = page
    per_page = 20
    pagination = Location.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    add_url = url_for('map.add_location')
    retrieve_url = ('map.retrieve_location', [('location_id', ':id')])
    try:
        return render_template('browse_locations.html',add_url=add_url, retrieve_url=retrieve_url, Location=Location, data=data,pagination=pagination)
    except TemplateNotFound:
        abort(404)

@map.route('/locations/new', methods=['POST', 'GET'])
def add_location():
    form = new_location()
    if form.validate_on_submit():
        location = Location(title=form.title.data, longitude=form.longitude.data, latitude=form.latitude.data, population=form.population.data)
        db.session.add(location)
        db.session.commit()
        flash('Congratulations, you just add a new location')
        return redirect(url_for('map.browse_locations_datatables'))

    return render_template('new_location.html', form=form)

@map.route('/locations/<int:location_id>/delete', methods=['POST'])
def delete_location(location_id):
    location = Location.query.get(location_id)
    db.session.delete(location)
    db.session.commit()
    flash('Location Deleted', 'success')
    return redirect(url_for('map.browse_locations_datatables'), 302)

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