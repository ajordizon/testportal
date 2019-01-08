from flask import *
from flask_login import current_user, login_required, LoginManager, login_user, logout_user
from flask import request
from models import User, Comment, Persoongegevens, Pensioengegevens, Pensioenen, Scenarios
from server import app, db
import views_my_pension

login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

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
    session['logged_in'] = True
    return redirect(url_for('index'))

@app.route("/", methods=["GET", "POST"])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == "GET":
        id = db.session.query(User).filter_by(username = current_user.username).first().id

        persoonnaam = db.session.query(Persoongegevens).filter_by(persoon_id = id).first().voornaam
        persoontsvs = db.session.query(Persoongegevens).filter_by(persoon_id = id).first().tussenvoegsel
        persoonachter = db.session.query(Persoongegevens).filter_by(persoon_id = id).first().achternaam

        dob = db.session.query(Persoongegevens).filter_by(persoon_id = id).first().geboortedatum
        salaris = db.session.query(Persoongegevens).filter_by(persoon_id = id).first().brutosalaris
        partner = db.session.query(Persoongegevens).filter_by(persoon_id = id).first().partner

        leeftijd_pensioen_jaar = db.session.query(Pensioengegevens).filter_by(pensioen_id = id).first().pensioen_leeftijd_jaar
        leeftijd_pensioen_maand = db.session.query(Pensioengegevens).filter_by(pensioen_id = id).first().pensioen_leeftijd_maand
        inkomen = db.session.query(Pensioengegevens).filter_by(pensioen_id = id).first().verwacht_inkomen
        uitgaven = db.session.query(Pensioengegevens).filter_by(pensioen_id = id).first().verwacht_uitgaven
        polis_nummer = db.session.query(Pensioenen).filter_by(pensioen_id = id).first().polisnummer
        investment = db.session.query(Pensioenen).filter_by(pensioen_id = id).first().investment_percentage


        som = inkomen - uitgaven
        shortsur = "earnings"
        if som < 0:
            shortsur = "shortage"
        if leeftijd_pensioen_maand == 0:
            leeftijd_pensioen = "" + str(leeftijd_pensioen_jaar) + " years"
        elif leeftijd_pensioen_maand == 1:
            leeftijd_pensioen = "" + str(leeftijd_pensioen_jaar) + " years and 1 month"
        else:
            leeftijd_pensioen = "" + str(leeftijd_pensioen_jaar) + " years and " + str(leeftijd_pensioen_maand) + " months"


        session['naam'] = str(persoonnaam) + " " + str(persoontsvs) + " " + str(persoonachter)
        session['som'] = som
        session['dob'] = str(dob)
        session['partner'] = str(partner)
        session['salaris'] = str(salaris)
        session['leeftijd_pensioen'] = str(leeftijd_pensioen)
        session['leeftijd_pensioen_jaar'] = str(leeftijd_pensioen_jaar)
        session['leeftijd_pensioen_maand'] = str(leeftijd_pensioen_maand)
        session['inkomen'] = str(inkomen)
        session['uitgaven'] = str(uitgaven)
        session['shortsur'] = shortsur
        session['polisnummer'] = str(polis_nummer)
        session['investment_percentage'] = str(investment)

        return render_template("index.html", session = session)
    return redirect(url_for('index'))

@app.route("/anderepensioenen")
def anderepensioenen():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    return render_template("anderepensioenen.html")

@app.route("/anderinkomen")
def anderinkomen():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    return render_template("anderinkomen.html")

@app.route("/mijnprofiel")
def mijnprofiel():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    id = db.session.query(User).filter_by(username = current_user.username).first().id
    pensioenen = db.session.query(Pensioenen)

    pensioen_overzicht = ""

    for pensioen in pensioenen:
        if pensioen.pensioen_id == id:
            uitvoerder = str(pensioen.pensioen_uitvoerder)
            if len(uitvoerder) > 40:
                uitvoerder = uitvoerder[0:37]
            pensioen_overzicht += "<tr>" + \
                             "<td>" + uitvoerder + "</td>" + \
                             "<td>" + str(pensioen.bruto_per_jaar) + "</td>" + \
                             "</tr>"
    return render_template("mijnprofiel.html", session = session, pensioen_overzicht = pensioen_overzicht)

@app.route("/editdetails")
def editdetails():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template("editdetails.html", session = session)

@app.route("/changepartner", methods=["GET", "POST"])
def changepartner():
    if request.method == "POST":
        option = request.form['partner']
        if option == "yes":
            id = db.session.query(User).filter_by(username = current_user.username).first().id
            pers = db.session.query(Persoongegevens).filter_by(persoon_id = id).first()
            pers.partner = "Yes"
            db.session.commit()
            nieuwpartner = db.session.query(Persoongegevens).filter_by(persoon_id = id).first().partner
            session['partner'] = str(nieuwpartner)
            return render_template("mijnprofiel.html")
        elif option == "no":
            id = db.session.query(User).filter_by(username = current_user.username).first().id
            pers = db.session.query(Persoongegevens).filter_by(persoon_id = id).first()
            pers.partner = "No"
            db.session.commit()
            nieuwpartner = db.session.query(Persoongegevens).filter_by(persoon_id = id).first().partner
            session['partner'] = str(nieuwpartner)
            return render_template("mijnprofiel.html")

@app.route("/profilebuildup")
def profilebuildup():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template("profilebuildup.html")

@app.route("/scenarios")
def scenarios():
#    id = db.session.query(User).filter_by(username = current_user.username).first().id
#    scenarios = db.session.query(Scenarios)
#    jaar = db.session.query(Scenarios).filter_by(scenario_id = id).first().pensioen_jaar
#    maand = db.session.query(Scenarios).filter_by(scenario_id = id).first().pensioen_maand

#    if maand != None:
#            session['scenarios_jaar'] = str(jaar)
#            session['scenarios_maand'] = str(maand)

#    scenarios_overzicht = ""
#    for i in scenarios:
       #     scenarios_overzicht += "<tr>" + \'

    return render_template("scenarios.html") #, scenarios_overzicht = scenarios_overzicht)

@app.route("/scenariostest", methods=["GET","POST"])
def scenariostest():
    if request.method == "POST":
        pensioen_jaar= request.form['pension_year']
        pensioen_maand = request.form['pension_months']
        scenario_id = db.session.query(User).filter_by(username = current_user.username).first().id
        scenario = Scenarios(scenario_id,pensioen_jaar, pensioen_maand)
        db.session.add(scenario)
        db.session.commit()
    return render_template("scenarios.html")

@app.route("/investment")
def investment():
    if not current_user.is_authenticated:
       return redirect(url_for('login'))
    return render_template("investments.html")

@app.route("/createall")
def createall():
    db.create_all()
    return render_template("index.html")

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    session['logged_in'] = False
    session.pop('som', None)
    session.pop('dob', None)
    session.pop('partner', None)
    session.pop('salaris', None)
    session.pop('leeftijd_pensioen', None)
    session.pop('leeftijd_pensioen_jaar', None)
    session.pop('leeftijd_pensioen_maand', None)
    session.pop('inkomen', None)
    session.pop('uitgaven', None)
    session.pop('shortsur', None)
    session.pop('polisnummer', None)
    session.pop('investment_percentage', None)
    session.pop('scenarios_jaar', None)
    session.pop('scenarios_maand', None)
    return redirect(url_for('index'))