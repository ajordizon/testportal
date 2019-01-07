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

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def __init__(self, Username, Password_hash):
        self.username = Username
        self.password_hash = Password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()


class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)

class Persoongegevens(db.Model):

    __tablename__ = "persoongegevens"

    id = db.Column(db.Integer, primary_key=True)
    voornaam = db.Column(db.String(40))
    tussenvoegsel = db.Column(db.String(40))
    achternaam = db.Column(db.String(40))
    persoon_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    telefoonnr = db.Column(db.String(20))
    geboortedatum = db.Column(db.Date)
    adres = db.Column(db.String(40))
    postcode = db.Column(db.String(6))
    provincie = db.Column(db.String(40))
    land = db.Column(db.String(40))
    emailadres = db.Column(db.String(40))
    bsn = db.Column(db.String(40))
    brutosalaris = db.Column(db.Numeric(50))
    persoon = db.relationship('User', foreign_keys=persoon_id)

    def __init__(self, Voornaam, Tussenvoegsel, Achternaam, Persoon_id, Telefoonnr, Geboortedatum, Adres, Postcode, Provincie, Land, Emailadres, Bsn, Brutosalaris):
        self.voornaam = Voornaam
        self.tussenvoegsel = Tussenvoegsel
        self.achternaam = Achternaam
        self.persoon_id = Persoon_id
        self.telefoonnr = Telefoonnr
        self.geboortedatum = Geboortedatum
        self.adres = Adres
        self.postcode = Postcode
        self.provincie = Provincie
        self.land = Land
        self.emailadres = Emailadres
        self.bsn = Bsn
        self.brutosalaris = Brutosalaris



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", comments=Comment.query.all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    comment = Comment(content=request.form["contents"], commenter=current_user)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login.html", error="no user")

    if not user.check_password(request.form["password"]):
        return render_template("login.html", error="Wrong pass for %s" % user.username)

    login_user(user)
    return redirect(url_for('index'))

@app.route("/mijnprofiel")
def mijnprofiel():
    return render_template("mijnprofiel.html")

@app.route("/investment")
def investment():
    return render_template("investments.html")

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':

    if 'liveconsole' not in gethostname():
        app.run()