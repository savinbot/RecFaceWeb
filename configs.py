# -*- coding: UTF-8 -*-

from os import path, urandom
from datetime import timedelta

# Defalut configuration of application
_root_dir = path.abspath(path.dirname(__file__))

_web_name = 'RecFace'
_web_secret = urandom(16).hex()
_web_host = '192.168.0.100'
_web_port = 80
_web_env = 'developmnet'
_web_debug = True

_session_driver = 'sqlalchemy'
_session_folder = 'sessions'
_session_name = f'{_web_name}_session'
_session_domain = ''
_session_http = True
_session_secure = False
_session_samesite = 'Lax'
_session_refresh = True
_session_lifetime = timedelta(hours=12)
_cookie_size = 4093

_db_driver = 'sqlite'
_db_host = _web_host
_db_port = 3306
_db_user = 'root'
_db_pass = 'root'
_db_name = 'RecFace'

_cam_type = 'direct' # Connection methods: test, direct or remote
_cam_method = 'http'
_cam_host = _web_host
_cam_port = 544
_cam_path = ''
_cam_user = 'admin'
_cam_pass = 'admin'

_send_x_file = False
_content_length = 16 * 1024 * 1024
_send_file_age = timedelta(hours=12)
_json_as_ascii = True
_json_sort_keys = True
