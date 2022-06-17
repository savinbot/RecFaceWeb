# -*- coding: UTF-8 -*-

from uuid import uuid4

from public.routes.base import (
	app, current_app, jsonify,
	session, g, Response, make_response, request,
	redirect, abort, url_for,
	Blueprint, flash, render_template, send_from_directory,
	TemplateNotFound,
	generate_password_hash, check_password_hash,
	SQLAlchemyError, db, Users,
	base, face
)

# Create blueprint for base url
auth = Blueprint(name='auth', import_name=__name__)

# Method for validating input field
def check_field(field):
	flag = True
	chars = ' 1234567890_?"!№@#$%^&*)(}{][><,./\|`~+-:;'
	for char in field:
		if char in chars:
			flag = False
			break
	return flag


def allowed_file(filename):
	ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for authentication page
@auth.get('/auth')
def get_auth():
	try:
		return render_template('auth.html', locale='en', title='RecFace', subtitle='Authentication')
	except TemplateNotFound:
		current_app.logger.warn('The "signup.html" template not found!')
		return abort(501)

# Route for registration page with GET requests
@auth.get('/auth/signup')
def get_signup():
	try:
		return render_template('signup.html', locale='en', title='RecFace', subtitle='Registration')
	except TemplateNotFound:
		current_app.logger.warn('The "signup.html" template not found!')
		return abort(501)

# Route for registration page with POST requests
@auth.post('/auth/signup')
def post_signup():
	try:
		uuid = uuid4().hex[:10].lower()
		fname = request.form.get('f_name')
		f_name = check_field(request.form.get('f_name', ' '))
		s_name = check_field(request.form.get('s_name', ' '))
		l_name = check_field(request.form.get('l_name', ' '))
		if f_name and s_name and l_name:
			f_name = request.form.get('f_name')
			s_name = request.form.get('s_name')
			l_name = request.form.get('l_name')
			user = Users(uid=uuid, fname=f_name, sname=s_name, lname=l_name)
			files = request.files.getlist('photo')
			for file in files:
				if file and allowed_file(file.filename):
					face.datasets(uuid, file)
			db.session.add(user)
			db.session.commit()
			flash('User successfully created, you can now log in.', 'info')
			return redirect(url_for('base.auth.get_auth'))
		else:
			flash('Incorrect data was entered in the form.', 'error')
		return redirect(url_for('base.auth.get_signup'))
	except SQLAlchemyError as error:
		current_app.logger.error(error)
		return abort(500)
	except Exception as error:
		current_app.logger.error(error)
		return abort(500)

# Route for authorization page with GET requests
@auth.get('/auth/signin')
def get_signin():
	try:
		atype = request.args.get('type', 'photo')
		return render_template('signin.html', locale='en', title='RecFace', subtitle='Authorization', type=atype)
	except TemplateNotFound:
		current_app.logger.warn('The "signin.html" template not found!')
		return abort(501)

# Route for authorization page with POST requests
@auth.post('/auth/signin')
def post_signin():
	try:
		files = request.files.getlist('photo')
		for file in files:
			if file and allowed_file(file.filename):
				succcess, uuid = face.match(photo=file)
				if succcess:
					return redirect(url_for('base.get_index', uuid=uuid))
				else:
					flash('Incorrect data was entered in the form.', 'error')
		return redirect(url_for('base.auth.get_signin'))
	except SQLAlchemyError as error:
		current_app.logger.error(error)
		return abort(500)
	except Exception as error:
		current_app.logger.error(error)
		return abort(500)

# Export objects
__ALL__ = ['auth']
