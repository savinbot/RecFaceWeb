# -*- coding: UTF-8 -*-

from public.models.base import SQLAlchemyError, db, Base

# Table for storing user data
class Users(Base):
	__tablename__ = 'users'

	# Columns for user data
	unique_id = db.Column(db.String(64), nullable=False, unique=True)
	first_name = db.Column(db.String(128), nullable=False)
	second_name = db.Column(db.String(128), nullable=False)
	last_name = db.Column(db.String(128), nullable=False)

	# Method for initialize the table
	def __init__(self, uid, fname, sname, lname):
		self.unique_id = uid
		self.first_name = fname
		self.second_name = sname
		self.last_name = lname

	# ---
	def __str__(self):
		return f'<User ID: {self.user_id}>'
	# ---
	def __repr__(self):
		return 'User ID: {}\nFirst name: {}\nSecond name: {}\nLast name: {}'.format(
			self.unique_id,
			self.first_name,
			self.second_name,
			self.last_name
		)

# Export objects
__ALL__ = ['SQLAlchemyError', 'db', 'Users']
