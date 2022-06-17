# -*- coding: UTF-8 -*-

from os import listdir, pardir, path, mkdir, remove
from shutil import rmtree, move

from flask import app, redirect, url_for, flash

from cv2 import cv2 as cv

from face_recognition import (
	load_image_file,
	face_encodings,
	face_landmarks,
	face_locations,
	face_distance,
	compare_faces
)

class FaceCam():
	"""Class for easy face recognition"""

	def __init__(self):
		self.__count = 0
		self.__config = {
			'UPLOAD_FOLDER': '',
			'CAM_TYPE': 'test',
			'CAM_METHOD': 'https',
			'CAM_HOST': 'localhost',
			'CAM_PORT': '80',
			'CAM_USER': 'admin',
			'CAM_PASS': 'admin',
			'CAM_PATH': 'stream'
		}
		self.__capture = cv.VideoCapture()

	def init_app(self, config):
		"""Method for getting application config"""
		for key in self.__config.keys():
			if key in config.keys():
				self.__config[key] = config.get(key)
			else:
				raise ValueError(f'The key "{key}" was not found in the "config".')

	def __connect(self):
		"""Method for setup connection to camera"""
		#self.__capture.get(cv.CAP_PROP_FRAME_WIDTH)
		#self.__capture.get(cv.CAP_PROP_FRAME_HEIGHT)
		#self.__capture.get(cv.CAP_PROP_FPS)
		#self.__capture.get(cv.CAP_PROP_FRAME_COUNT)
		if self.__config['CAM_TYPE'] == 'remote':
			self.__capture.open('{method}://{user}:{password}@{host}:{port}/{path}'.format(
				method = self.__config['CAM_METHOD'],
				host = self.__config['CAM_HOST'],
				port = self.__config['CAM_PORT'],
				user = self.__config['CAM_USER'],
				password = self.__config['CAM_PASS'],
				path = self.__config['CAM_PATH']
			))
		elif self.__config['CAM_TYPE'] == 'direct':
			self.__capture.open(0, cv.CAP_DSHOW)
		elif self.__config['CAM_TYPE'] == 'test':
			self.__capture.open('http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4')

	def datasets(self, uuid, photo):
		""""""
		path_file = path.join(self.__config['UPLOAD_FOLDER'], uuid)
		if not path.exists(path_file):
			mkdir(path_file)
		photo.save(path.join(path_file, photo.filename))
		frame = cv.imread(path.join(path_file, photo.filename))
		rmtree(path_file)
		path_file = path.join(self.__config['UPLOAD_FOLDER'], pardir, 'datasets', uuid)
		if not path.exists(path_file):
			mkdir(path_file)
		locations, frame = self.locations(frame=frame)
		for location in locations:
			top, right, bottom, left = location
			frame = frame[top:bottom, left:right]
			cv.imwrite(path.join(path_file, f'face_{self.__count}.jpg'), frame)
			self.__count += 1

	def match(self, photo):
		""""""
		path_dataset = path.join(self.__config['UPLOAD_FOLDER'], pardir, 'datasets')
		path_file = path.join(self.__config['UPLOAD_FOLDER'], photo.filename)
		photo.save(path_file)
		face1 = load_image_file(path_file)
		remove(path_file)
		encodings1, face1 = self.encodings(face1)
		datasets = listdir(path_dataset)
		for dataset in datasets:
			photos = listdir(path.join(path_dataset, dataset))
			for p in photos:
				face2 = load_image_file(path.join(path_dataset, dataset, p))
				encodings2, face2 = self.encodings(face2)
				result = compare_faces([encodings2], encodings1)
				if (result != []) and (result != [False]):
					return result, dataset

	def encodings(self, frame):
		""""""
		encodings = face_encodings(frame)[0]
		return encodings, frame

	def locations(self, frame):
		""""""
		locations = face_locations(frame)
		return locations, frame

	def stream(self, play, width, height):
		""""""
		path_dataset = path.join(self.__config['UPLOAD_FOLDER'], pardir, 'datasets')
		while True:
			if not play:
				self.__capture.release()
				break
			if not self.__capture.isOpened():
				self.__capture.release()
				self.__connect()
				continue
			success, frame = self.__capture.read()
			if success:
				frame = cv.resize(frame, (width, height))
				#frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
				locations, frame = self.locations(frame=frame)
				for location in locations:
					top, right, bottom, left = location
					cv.rectangle(frame, (right, top), (left, bottom), (0, 0, 0), 2)
				if len(locations) >= 1:
					encode1 = face_encodings(frame)
					datasets = listdir(path_dataset)
					for dataset in datasets:
						photos = listdir(path.join(path_dataset, dataset))
						for p in photos:
							face2 = cv.imread(path.join(path_dataset, dataset, p))
							encode2 = face_encodings(face2)
							if encode1 != [] and encode2 != []:
								result = compare_faces([encode2[0]], encode1[0])
								if (result != []) and (result != [False]):
									with app.app_context():
										return redirect(url_for('base.get_index', uuid=dataset))
				success, jpeg = cv.imencode('.jpg', frame)
				if success:
					yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

# Export objects
__ALL__ = ['FaceCam']
