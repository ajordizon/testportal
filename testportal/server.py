from socket import gethostname
from flask import *
import hashlib
import os
import sys
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import current_user, login_required, login_user, LoginManager, logout_user, UserMixin
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.config["DEBUG"] = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="lepel",
    password="kaas15geel",
    hostname="lepel.mysql.pythonanywhere-services.com",
    databasename="lepel$deelnemers",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.secret_key = "siekritkiej"