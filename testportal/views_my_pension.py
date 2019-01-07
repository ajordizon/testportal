from flask import *
from flask_login import current_user, login_required, LoginManager, login_user, logout_user
from models import User, Comment, Persoongegevens, Pensioengegevens, Pensioenen
from server import app, db


@app.route("/mijnpensioenen")
def mijnpensioenen():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    id = db.session.query(User).filter_by(username = current_user.username).first().id
    #Pension_uitvoerder, polisnummer, bruto, begin, eind

    pensioenen = db.session.query(Pensioenen) #.filter_by(pensioen_id = current_user.id).first()
    pensioen_gebruiker = ""

    for pensioen in pensioenen:
        if pensioen.pensioen_id == id:
            pensioen_gebruiker += "<tr>" + \
                             "<td>" + str(pensioen.pensioen_uitvoerder) + "</td>" + \
                             "<td>" + str(pensioen.polisnummer) + "</td>" + \
                             "<td>" + str(pensioen.bruto_per_jaar) + "</td>" + \
                             "<td>" + str(pensioen.begintijd) + "</td>" + \
                             "<td>" + str(pensioen.eindtijd) + "</td>" + \
                             "</tr>"

    return render_template("mijnpensioenen.html", pensioenen_gebruiker = pensioen_gebruiker)


@app.route("/mijnpensioenentest")
def mijnpensioenentest():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    id = db.session.query(User).filter_by(username = current_user.username).first().id
    #Pension_uitvoerder, polisnummer, bruto, begin, eind

    pensioenen = db.session.query(Pensioenen) #.filter_by(pensioen_id = current_user.id).first()
    pensioen_gebruiker = ""

    for pensioen in pensioenen:
        if pensioen.pensioen_id == id:
            pensioen_gebruiker += "<tr>" + \
                             "<td>" + str(pensioen.pensioen_uitvoerder) + "</td>" + \
                             "<td>" + str(pensioen.polisnummer) + "</td>" + \
                             "<td>" + str(pensioen.bruto_per_jaar) + "</td>" + \
                             "<td>" + str(pensioen.begintijd) + "</td>" + \
                             "<td>" + str(pensioen.eindtijd) + "</td>" + \
                             "</tr>"

    return render_template("mijnpensioenentest.html", pensioenen_gebruiker = pensioen_gebruiker)

#voor profielpagina:
    # id = db.session.query(User).filter_by(username = current_user.username).first().id
    # pensioenen = db.session.query(Pensioenen)

    # pensioen_overzicht = ""

    # for pensioen in pensioenen:
    #     if pensioen.pensioen_id == id:
    #         uitvoerder = str(pensioen.pensioen_uitvoerder)
    #         if len(uitvoerder) > 40:
    #             uitvoerder = uitvoerder[0:37]
    #         pensioen_overzicht += "<tr>" + \
    #                          "<td>" + uitvoerder + "</td>" + \
    #                          "<td>" + str(pensioen.bruto_per_jaar) + "</td>" + \
    #                          "</tr>"