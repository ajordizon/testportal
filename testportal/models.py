from server import app, db
from socket import gethostname
from flask import *
import hashlib
import os
import sys
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import current_user, login_required, login_user, LoginManager, logout_user, UserMixin
from werkzeug.security import check_password_hash
from server import app, db
import server



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
    geboortedatum = db.Column(db.String(25))
    adres = db.Column(db.String(40))
    postcode = db.Column(db.String(6))
    provincie = db.Column(db.String(40))
    land = db.Column(db.String(40))
    emailadres = db.Column(db.String(40))
    bsn = db.Column(db.String(40))
    brutosalaris = db.Column(db.Numeric(50))
    partner = db.Column(db.String(5))

    persoon = db.relationship('User', foreign_keys=persoon_id)

    def __init__(self, Voornaam, Tussenvoegsel, Achternaam, Persoon_id, Telefoonnr, Geboortedatum, Adres, Postcode, Provincie, Land, Emailadres, Bsn, Brutosalaris, Partner):
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
        self.partner = Partner



class Pensioengegevens(db.Model):

    __tablename__= "pensioengegevens"

    id = db.Column(db.Integer, primary_key=True)
    pensioen_leeftijd_jaar = db.Column(db.Numeric(4))
    pensioen_leeftijd_maand = db.Column(db.Numeric(2))
    verwacht_inkomen = db.Column(db.Numeric(50))
    verwacht_uitgaven = db.Column(db.Numeric(50))
    pensioen_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pensioen = db.relationship('User', foreign_keys=pensioen_id)


    def __init__(self, Pensioen_leeftijd_jaar, Pensioen_leeftijd_maand, Verwacht_inkomen, Verwacht_uitgaven, Pensioen_id):
        self.pensioen_leeftijd_jaar = Pensioen_leeftijd_jaar
        self.pensioen_leeftijd_maand = Pensioen_leeftijd_maand
        self.verwacht_inkomen = Verwacht_inkomen
        self.verwacht_uitgaven = Verwacht_uitgaven
        self.pensioen_id = Pensioen_id

class Pensioenen(db.Model):

    __tablename__= "pensioenen"

    id = db.Column(db.Integer, primary_key=True)
    pensioen_id = db.Column(db.Integer, db.ForeignKey('pensioengegevens.pensioen_id'), nullable=False)
    pensioen = db.relationship('Pensioengegevens', foreign_keys=pensioen_id)
    pensioen_uitvoerder = db.Column(db.String(80))
    bruto_per_jaar = db.Column(db.Numeric(50))
    investment_percentage = db.Column(db.String(25))
    polisnummer = db.Column(db.String(40))
    begintijd = db.Column(db.String(40))
    eindtijd = db.Column(db.String(40))

    def __init__(self, Pensioen_id, Pensioen_uitvoerder, Bruto_per_jaar, Investment_percentage, Polisnummer, Begintijd, Eindtijd):
        self.pensioen_id = Pensioen_id
        self.pensioen_uitvoerder = Pensioen_uitvoerder
        self.bruto_per_jaar = Bruto_per_jaar
        self.investment_percentage = Investment_percentage
        self.polisnummer = Polisnummer
        self.begintijd = Begintijd
        self.eindtijd = Eindtijd

class Scenarios(db.Model):

    __tablename__= "scenarios"
    id = db.Column(db.Integer, primary_key=True)
    pensioen_jaar = db.Column(db.String(80))
    bruto_per_maand = db.Column(db.Numeric(50))

    def __init__(self, Pensioen_jaar, Pensioen_maand):
        self.pensioen_jaar = Pensioen_jaar
        self.pensioen_maand = Pensioen_maand


