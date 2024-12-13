# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

load_dotenv()

"""
Load sensitive data from .env file
"""
app_port = os.getenv('APP_PORT')
allowed_hosts = os.getenv('ALLOWED_HOSTS')

api_key = os.getenv('API_KEY')
secret = os.getenv('APP_SECRET')
algorithm = os.getenv('ALGORITHM')
token_expires_in = int(os.getenv('TOKEN_EXPIRES_IN_MINUTES'))

admin_password = os.getenv('ADMIN_PASSWORD')

db_manager = os.getenv('DB_MANAGER')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
