# -*- coding: UTF-8 -*-

from uuid import uuid4

from flask import (
	app, current_app, jsonify,
	session, g, Response, make_response, request,
	redirect, abort, url_for, escape,
	Blueprint, flash, render_template, send_from_directory
)
from jinja2 import TemplateNotFound
from werkzeug.security import generate_password_hash, check_password_hash

from public.models.users import SQLAlchemyError, db, Users
from public.models.face import FaceCam

# Create blueprint for base url
base = Blueprint(name='base', import_name=__name__)

# Create instance of face recognition
face = FaceCam()

# List of IP addresses
WHITE_LIST = ['192.168.0.100', '192.168.0.101']

#
@base.before_request
def before():
	# Restricting access to the website by IP addresses
	ip = request.environ.get('REMOTE_ADDR')
	if not ip in WHITE_LIST:
		return abort(403, 'Иди ты на хуй заебал! Иди дрочись со своим говно-PHP дальше, может свое очко им хакнишь, еблан ты бл.') #'Access to this website is restricted by a whitelist of IP addresses.'

# Error hadler for 403 - Forbidden
@base.app_errorhandler(403)
def error_403(error):
	response = make_response(
		render_template('errors.html', locale='en', title='RecFace', subtitle='Forbidden', message=str(error)),
		403
	)
	return response

# Error hadler for 404 - Not Found
@base.app_errorhandler(404)
def error_404(error):
	response = make_response(
		render_template('errors.html', locale='en', title=f'RecFace', subtitle='Not found', message=str(error)),
		404
	)
	return response

# Error hadler for 429 - Too Many Requests
@base.app_errorhandler(429)
def error_429(error):
	response = make_response(
		render_template('errors.html', locale='en', title='RecFace', subtitle='Too many requests', message=str(error)),
		429
	)
	return response

# Error hadler for 501 - Internal Server Error
@base.app_errorhandler(500)
def error_500(error):
	db.session.rollback()
	db.session.close()
	current_app.logger.error(error)
	response = make_response(
		render_template('errors.html', locale='en', title='RecFace', subtitle='Internal server error', message=str(error)),
		500
	)
	return response

# Error hadler for 501 - Not Implemented
@base.app_errorhandler(501)
def error_501(error):
	current_app.logger.warning(error)
	response = make_response(
		render_template('errors.html', locale='en', title='RecFace', subtitle='Not implemented', message=str(error)),
		501
	)
	return response

# Error hadler for 503 Service Unavailable
@base.app_errorhandler(503)
def error_503(error):
	current_app.logger.warning(error)
	response = make_response(
		render_template('errors.html', locale='en', title='RecFace', subtitle='Service unavailable', message=str(error)),
		503
	)
	response.headers.add('Retry-After', 43200)
	return response

# Route for static files
@base.get('/assets/<path:filename>')
def assets(filename):
	return send_from_directory('assets', filename)

# Route for video stream
@base.get('/video')
def video():
	play = request.args.get('play', '0') == str(1)
	width = int(request.args.get('width', 720))
	height = int(request.args.get('height', 480))
	return Response(
		face.stream(play=play, width=width, height=height),
		mimetype='multipart/x-mixed-replace; boundary=frame'
	)

# Route for index page
@base.get('/')
@base.get('/welcome')
def get_index():
	try:
		uuid = request.args.get('uuid', None)
		if uuid is not None:
			user = Users.query.filter_by(unique_id=uuid).first()
			if user is not None:
				flash(f'User successefully matched!', 'info')
				flash(f'User ID: {user.unique_id}', 'info')
				flash(f'Fist name: {user.first_name}', 'info')
				flash(f'Second name: {user.second_name or "Not specified"}', 'info')
				flash(f'Last name: {user.last_name}', 'info')
			else:
				flash('The user with such data was not found.', 'error')
		return render_template('welcome.html', locale='en', title='RecFace', subtitle='Welcome')
	except TemplateNotFound:
		current_app.logger.warn('The "welcome.html" template not found!')
		return abort(501)

# Export objects
__ALL__ = [
	'app', 'current_app', 'jsonify',
	'session', 'g', 'Response', 'make_response', 'request',
	'redirect', 'abort', 'url_for',
	'Blueprint', 'flash', 'render_template', 'send_from_directory',
	'TemplateNotFound',
	'generate_password_hash', 'check_password_hash',
	'SQLAlchemyError', 'db', 'Users',
	'base', 'face'
]
