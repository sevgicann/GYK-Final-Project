from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import uuid
from utils.logger import log_database_operation, log_function_call, get_logger

# User class will be defined in app.py after db is initialized