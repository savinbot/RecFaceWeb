# -*- coding: UTF-8 -*-

import configs
import logging

from flask import Flask
from flask_session import Session

from public.models.base import db, migrate
from public.routes.base import base, face
from public.routes.auth import auth

# Create flask application
app = Flask(
	import_name = __name__.split('.')[0],
	static_url_path = '/assets',
	static_folder = configs.path.join(configs._root_dir, 'public', 'assets'),
	template_folder = configs.path.join(configs._root_dir, 'public', 'views')
)

# Setup configuration of flask application
app.config['ENV'] = configs._web_env
app.config['DEBUG'] = configs._web_debug
app.config['NAME'] = configs._web_name
app.config['SECRET_KEY'] = configs._web_secret

# Configure database and migrations
match configs._db_driver:
	case 'mysql':
		app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{configs._db_user}:{configs._db_pass}@{configs._db_host}:{configs._db_port}/{configs._db_name}'
	case 'postgresql':
		app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{configs._db_user}:{configs._db_pass}@{configs._db_host}:{configs._db_port}/{configs._db_name}'
	case 'sqlite' | _:
		app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{configs.path.join(configs._root_dir, 'databases', f'{configs._db_name}.sqlite3')}"
# ------
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# ------
db.init_app(app)
migrate.init_app(app, db)

# Configure sessions and cookies
session = Session()
# ------
app.config['SESSION_TYPE'] = configs._session_driver
app.config['SESSION_KEY_PREFIX'] = f'{configs._session_name}:'
app.config['SESSION_COOKIE_NAME'] = configs._session_name
app.config['SESSION_COOKIE_DOMAIN'] = configs._session_domain
app.config['SESSION_COOKIE_HTTPONLY'] = configs._session_http
app.config['SESSION_COOKIE_SECURE'] = configs._session_secure
app.config['SESSION_COOKIE_SAMESITE'] = configs._session_samesite
app.config['SESSION_REFRESH_EACH_REQUEST'] = configs._session_refresh
app.config['PERMANENT_SESSION_LIFETIME'] = configs._session_lifetime
app.config['MAX_COOKIE_SIZE'] = configs._cookie_size
# ------
match configs._session_driver:
	case 'sqlalchemy':
		app.config['SESSION_PERMANENT'] = True
		app.config['SESSION_SQLALCHEMY'] = db
		app.config['SESSION_SQLALCHEMY_TABLE'] = configs._session_folder
	case 'filesystem' | _:
		app.config['SESSION_USE_SIGNER'] = False
		app.config['SESSION_PERMANENT'] = False
		app.config['SESSION_FILE_THRESHOLD'] = 500
		app.config['SESSION_FILE_DIR'] = configs._session_folder
# ------
session.init_app(app)

# Configure contents and uploads
app.config['UPLOAD_FOLDER'] = configs.path.join(configs._root_dir, 'uploads')
# ------
app.config['MAX_CONTENT_LENGTH'] = configs._content_length
app.config['USE_X_SENDFILE'] = configs._send_x_file
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = configs._send_file_age
# ------
app.config['JSON_AS_ASCII'] = configs._json_as_ascii
app.config['JSON_SORT_KEYS'] = configs._json_sort_keys

# Configure cameras
app.config['CAM_TYPE'] = configs._cam_type
app.config['CAM_METHOD'] = configs._cam_method
app.config['CAM_HOST'] = configs._cam_host
app.config['CAM_PORT'] = configs._cam_port
app.config['CAM_PATH'] = configs._cam_path
app.config['CAM_USER'] = configs._cam_user
app.config['CAM_PASS'] = configs._cam_pass
# ------
face.init_app(app.config)

# !!! Comment that string if using flask-migrate commands.
with app.app_context():
	db.create_all()

# CRITICAL FATAL ERROR WARN INFO DEBUG
#logging.basicConfig(filename=configs.path.join(configs._root_dir, 'logging', 'debug.log'), level=logging.DEBUG)

# Registration blueprints with routes of application
base.register_blueprint(auth)
app.register_blueprint(base)

if __name__ == '__main__':
	# Run the flask application
	app.run(
		host=configs._web_host,
		port=configs._web_port
	)
	my_string = input()
