# -*- coding: UTF-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError

# Create instance of database
db = SQLAlchemy()
migrate = Migrate()

# Create base model
class Base(db.Model):
	__abstract__  = True

	# Create columns
	id = db.Column(db.Integer, primary_key=True)
	date_created  = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# Export objects
__ALL__ = ['SQLAlchemyError', 'db', 'migrate', 'Base']
