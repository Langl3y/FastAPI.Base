# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

load_dotenv()

"""
Load sensitive data from .env file
"""
app_port = os.getenv('APP_PORT')
allowed_hosts = os.getenv('ALLOWED_HOSTS')

db_manager = os.getenv('DB_MANAGER')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
