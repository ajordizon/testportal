from socket import gethostname
from flask import *
import hashlib
import os
import sys
import views
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import current_user, login_required, login_user, LoginManager, logout_user, UserMixin
from werkzeug.security import check_password_hash
from server import app, db
from models import User, Comment, Persoongegevens
import server




if __name__ == '__main__':

    if 'liveconsole' not in gethostname():
        app.run()