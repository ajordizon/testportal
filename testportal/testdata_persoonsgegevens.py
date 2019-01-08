from server import db
from werkzeug.security import generate_password_hash
from models import Persoongegevens, User, Pensioengegevens, Pensioenen

db.drop_all()
db.create_all()

usernames = ["Petertje01", "Mariekdepiek", "Barrydebaas95", "Charlottekapot"]
voornaam = ['Peter', 'Marieke', 'Barrie', 'Charlotte']
tussenvoegsel = 'von'
achternaam = 'Petermans'
telefoonnr = '123123123'
geboortedatum = ['12-12-1212', '13-12-1212', '14-12-1212', '15-12-1212']
adres = 'Peterstraat'
postcode = '1212QW'
provincie = 'Peteria'
land = 'Peterland'
emailadres = ['Peter.Petermans@hotmail.com', 'Marieke.Petermans@hotmail.com', 'Barrie.Petermans@hotmail.com', 'Charlotte.Petermans@hotmail.com']
bsn = '123123'
bruto = 500
partner = "No"
pensioen_leeftijd_jaar = [68, 68, 68, 70]
pensioen_leeftijd_maand = [0, 1, 6, 11]
verwacht_inkomen = [300, 12000, 6000, 1200]
verwacht_uitgaven = [800, 5000, 6000, 800]

pensioen_ref = [1,1,1,2,2,3,4]
pensioen_uitvoerder = ["Je moeder haar spaarpot", "Nationale Nederlanden", "De Staat", "Nationale Nederlanden", "De Staat", "Je vader zijn geheime bankrekening", "De Staat"]
bruto_per_jaar = [30000, 4000, 200, 15000, 200, 5000000, 60000]
investment_percentage = [10, 15, 15, 30, 45, 30, 45]
polisnummer = ["JM12345", "NN12346", "A12347", "NN12348", "A12349", "GB13245", "A12350"]
begindatum = ["10-01-1993","12-06-1993","15-03-1995","11-11-2010","11-11-1987","16-08-1999","12-12-1212"]
einddatum = ["20-01-2087","19-06-2084","20-01-2087","03-02-2056","03-02-2056","17-08-2099","12-12-2424"]


i = 0

for username in usernames:
    password = generate_password_hash("12345")

    newaccount = User(usernames[i], password)

    db.session.add(newaccount)
    db.session.commit()

    id = db.session.query(User)
    id = id.filter(User.username == usernames[i])
    id = id.one()
    id = id.id
    persoon_id = id

    newuser = Persoongegevens(voornaam[i], tussenvoegsel, achternaam, persoon_id, telefoonnr, geboortedatum[i], adres, postcode, provincie, land, emailadres[i], bsn, bruto, partner)

    db.session.add(newuser)
    db.session.commit()

    pensioen_id = id

    newpension = Pensioengegevens(pensioen_leeftijd_jaar[i], pensioen_leeftijd_maand[i], verwacht_inkomen[i], verwacht_uitgaven[i], pensioen_id)

    db.session.add(newpension)
    db.session.commit()

    i = i + 1

i = 0

for id in pensioen_ref:
    newpension = Pensioenen(id, pensioen_uitvoerder[i], bruto_per_jaar[i], investment_percentage[i], polisnummer[i], begindatum[i], einddatum[i])
    db.session.add(newpension)
    db.session.commit()
    i = i + 1


