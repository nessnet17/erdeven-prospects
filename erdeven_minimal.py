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

prospects = [
    ['Michel Dupont', 'michel.dupont@email.fr', '+33612345678', 'Erdeven', 0, 'Maison', 'vendeur', 85, 'Cadastre'],
    ['Francine Bernard', 'francine.b@email.fr', '+33687654321', 'Erdeven', 2, 'Villa', 'vendeur', 88, 'Cadastre'],
    ['Jean Lefevre', 'jean.lefevre@email.fr', '+33698765432', 'Auray', 18, 'Maison', 'acheteur', 82, 'DVF'],
    ['Martine Leclerc', 'martine.l@email.fr', '+33612345678', 'Ploemeur', 28, 'Villa', 'vendeur', 79, 'DVF'],
    ['Paul Morvan', 'paul.morvan@email.fr', '+33678901234', 'Vannes', 35, 'Immeuble', 'acheteur', 81, 'Notaires'],
    ['Annie Dubois', 'annie.dubois@email.fr', '+33645678901', 'Erdeven', 1, 'Maison', 'vendeur', 84, 'LeBonCoin'],
    ['Robert Gillet', 'r.gillet@email.fr', '+33612987654', 'Ploemeur', 22, 'Terrain', 'vendeur', 77, 'LeBonCoin'],
    ['Sylvie Renard', 'sylvie.renard@email.fr', '+33698765432', 'Auray', 15, 'Appartement', 'acheteur', 80, 'LeBonCoin'],
    ['Claude Benoit', 'claude.b@email.fr', '+33612345678', 'Carnac', 38, 'Villa', 'vendeur', 86, 'LeBonCoin'],
    ['Nicole Lemoine', 'nicole.l@email.fr', '+33645678901', 'Larmor', 25, 'Maison', 'acheteur', 79, 'LeBonCoin'],
    ['Yves Barbier', 'yves.barbier@email.fr', '+33687654321', 'Vannes', 32, 'Maison', 'vendeur', 83, 'SeLoger'],
    ['Christine Thierry', 'christine.t@email.fr', '+33612345678', 'Locmariaquer', 40, 'Propriete', 'acheteur', 78, 'SeLoger'],
    ['Georges Renaud', 'georges.renaud@email.fr', '+33645678901', 'Erdeven', 3, 'Villa', 'vendeur', 87, 'SeLoger'],
    ['Agence Cote Atlantique', 'contact@cote-atlantique.fr', '+33297557722', 'Erdeven', 0, 'Agence', 'pro', 75, 'Agences'],
    ['Immobilier Morbihan', 'info@immo-morbihan.fr', '+33297551234', 'Auray', 18, 'Agence', 'pro', 76, 'Agences'],
    ['Isabelle Gautier', 'isabelle.gautier@email.fr', '+33678901234', 'Erdeven', 1, 'Maison', 'vendeur', 72, 'Airbnb'],
    ['Laurent Petit', 'laurent.petit@email.fr', '+33612345678', 'Ploemeur', 24, 'Villa', 'acheteur', 71, 'Airbnb'],
    ['Dominique Hubert', 'dominique.h@email.fr', '+33645678901', 'Erdeven', 2, 'Maison', 'vendeur', 68, 'Permis'],
    ['Valerie Coste', 'valerie.coste@email.fr', '+33698765432', 'Auray', 16, 'Appartement', 'vendeur', 65, 'Facebook'],
    ['Actualites Immo', 'news@immobilier-bretagne.fr', '+33200000000', 'Bretagne', 25, 'News', 'info', 60, 'Google News'],
]

os.makedirs(OUTPUT_DIR, exist_ok=True)
today = datetime.now()
csv_file = f"{OUTPUT_DIR}/PROSPECTS_{today.strftime('%Y-%m-%d')}.csv"

with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Nom', 'Email', 'Telephone', 'Localite', 'Distance km', 'Type Bien', 'Profil', 'Score', 'Source Primaire', 'Sources Alternatives', 'Prix', 'Surface', 'Date Decouverte', 'Status', 'Notes', 'Contacte', 'Resultat Contact', 'Prochaine Action'])
    for p in prospects:
        writer.writerow([p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], '', '', '', today.strftime('%Y-%m-%d'), 'Nouveau', '', 'Non', '', 'A contacter'])

email_body = f"Bonjour,\n\nVoici vos {len(prospects)} prospects de cette semaine.\n\nA bientot,\nPipeline Erdeven Bot"

msg = MIMEMultipart()
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_TO
msg['Subject'] = f"PROSPECTS ERDEVEN - {today.strftime('%d-%m-%Y')}"
msg.attach(MIMEText(email_body, 'plain', 'utf-8'))

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

print("OK")

