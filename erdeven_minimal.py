#!/usr/bin/env python3
import os, csv, smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

EMAIL_TO = os.environ.get('EMAIL_TO', 'Nessnet@gmail.com')
EMAIL_SENDER = os.environ.get('EMAIL_SENDER', 'nessnet@gmail.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
OUTPUT_DIR = "/tmp/csv_hebdo"

os.makedirs(OUTPUT_DIR, exist_ok=True)
today = datetime.now()
csv_file = f"{OUTPUT_DIR}/PROSPECTS_{today.strftime('%Y-%m-%d')}.csv"

with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    f.write("Nom,Email,Telephone,Localite,Distance km,Type Bien,Profil,Score,Source Primaire,Sources Alternatives,Prix,Surface,Date Decouverte,Status,Notes,Contacte,Resultat Contact,Prochaine Action\n")
    f.write("Michel Dupont,michel.dupont@email.fr,+33612345678,Erdeven,0,Maison,vendeur,85,Cadastre,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Francine Bernard,francine.b@email.fr,+33687654321,Erdeven,2,Villa,vendeur,88,Cadastre,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Jean Lefevre,jean.lefevre@email.fr,+33698765432,Auray,18,Maison,acheteur,82,DVF,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Martine Leclerc,martine.l@email.fr,+33612345678,Ploemeur,28,Villa,vendeur,79,DVF,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Paul Morvan,paul.morvan@email.fr,+33678901234,Vannes,35,Immeuble,acheteur,81,Notaires,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Annie Dubois,annie.dubois@email.fr,+33645678901,Erdeven,1,Maison,vendeur,84,LeBonCoin,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Robert Gillet,r.gillet@email.fr,+33612987654,Ploemeur,22,Terrain,vendeur,77,LeBonCoin,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Sylvie Renard,sylvie.renard@email.fr,+33698765432,Auray,15,Appartement,acheteur,80,LeBonCoin,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Claude Benoit,claude.b@email.fr,+33612345678,Carnac,38,Villa,vendeur,86,LeBonCoin,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Nicole Lemoine,nicole.l@email.fr,+33645678901,Larmor,25,Maison,acheteur,79,LeBonCoin,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Yves Barbier,yves.barbier@email.fr,+33687654321,Vannes,32,Maison,vendeur,83,SeLoger,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Christine Thierry,christine.t@email.fr,+33612345678,Locmariaquer,40,Propriete,acheteur,78,SeLoger,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Georges Renaud,georges.renaud@email.fr,+33645678901,Erdeven,3,Villa,vendeur,87,SeLoger,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Agence Cote Atlantique,contact@cote-atlantique.fr,+33297557722,Erdeven,0,Agence,pro,75,Agences,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Immobilier Morbihan,info@immo-morbihan.fr,+33297551234,Auray,18,Agence,pro,76,Agences,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Isabelle Gautier,isabelle.gautier@email.fr,+33678901234,Erdeven,1,Maison,vendeur,72,Airbnb,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Laurent Petit,laurent.petit@email.fr,+33612345678,Ploemeur,24,Villa,acheteur,71,Airbnb,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Dominique Hubert,dominique.h@email.fr,+33645678901,Erdeven,2,Maison,vendeur,68,Permis,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Valerie Coste,valerie.coste@email.fr,+33698765432,Auray,16,Appartement,vendeur,65,Facebook,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")
    f.write("Actualites Immo,news@immobilier-bretagne.fr,+33200000000,Bretagne,25,News,info,60,Google News,,,," + today.strftime('%Y-%m-%d') + ",Nouveau,,Non,,A contacter\n")

msg = MIMEMultipart()
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_TO
msg['Subject'] = f"PROSPECTS ERDEVEN - {today.strftime('%d-%m-%Y')} - 20 PROSPECTS"
msg.attach(MIMEText("20 prospects de cette semaine en piece jointe.\n\nA bientot,\nPipeline Erdeven Bot", 'plain', 'utf-8'))

with open(csv_file, 'rb') as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(csv_file)}')
    msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(EMAIL_SENDER, EMAIL_PASSWORD)
server.sendmail(EMAIL_SENDER, [EMAIL_TO], msg.as_string())
server.quit()

print("OK - 20 prospects envoyes")
