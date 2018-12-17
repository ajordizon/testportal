from flask_app import db, Persoonsgegevens


db.drop_all()
db.create_all()


id
voornaam
tusenvoegsel
achternaam
persoon_id
telefoonnr
geboortedatum
adres
postcode
provincie
land
emailadres
bsn
persoon


db.commit()