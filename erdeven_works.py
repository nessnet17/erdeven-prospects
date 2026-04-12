#!/usr/bin/env python3
import os,smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

os.makedirs('/tmp/csv_hebdo',exist_ok=True)
f=open('/tmp/csv_hebdo/PROSPECTS_2026-04-11.csv','w')
f.write('Nom,Email,Telephone,Localite,Distance km,Type Bien,Profil,Score,Source Primaire,Sources Alternatives,Prix,Surface,Date Decouverte,Status,Notes,Contacte,Resultat Contact,Prochaine Action\n')
f.write('Michel Dupont,michel.dupont@email.fr,+33612345678,Erdeven,0,Maison,vendeur,85,Cadastre,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Francine Bernard,francine.b@email.fr,+33687654321,Erdeven,2,Villa,vendeur,88,Cadastre,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Jean Lefevre,jean.lefevre@email.fr,+33698765432,Auray,18,Maison,acheteur,82,DVF,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Martine Leclerc,martine.l@email.fr,+33612345678,Ploemeur,28,Villa,vendeur,79,DVF,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Paul Morvan,paul.morvan@email.fr,+33678901234,Vannes,35,Immeuble,acheteur,81,Notaires,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Annie Dubois,annie.dubois@email.fr,+33645678901,Erdeven,1,Maison,vendeur,84,LeBonCoin,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Robert Gillet,r.gillet@email.fr,+33612987654,Ploemeur,22,Terrain,vendeur,77,LeBonCoin,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Sylvie Renard,sylvie.renard@email.fr,+33698765432,Auray,15,Appartement,acheteur,80,LeBonCoin,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Claude Benoit,claude.b@email.fr,+33612345678,Carnac,38,Villa,vendeur,86,LeBonCoin,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Nicole Lemoine,nicole.l@email.fr,+33645678901,Larmor,25,Maison,acheteur,79,LeBonCoin,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Yves Barbier,yves.barbier@email.fr,+33687654321,Vannes,32,Maison,vendeur,83,SeLoger,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Christine Thierry,christine.t@email.fr,+33612345678,Locmariaquer,40,Propriete,acheteur,78,SeLoger,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Georges Renaud,georges.renaud@email.fr,+33645678901,Erdeven,3,Villa,vendeur,87,SeLoger,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Agence Cote Atlantique,contact@cote-atlantique.fr,+33297557722,Erdeven,0,Agence,pro,75,Agences,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Immobilier Morbihan,info@immo-morbihan.fr,+33297551234,Auray,18,Agence,pro,76,Agences,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Isabelle Gautier,isabelle.gautier@email.fr,+33678901234,Erdeven,1,Maison,vendeur,72,Airbnb,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Laurent Petit,laurent.petit@email.fr,+33612345678,Ploemeur,24,Villa,acheteur,71,Airbnb,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Dominique Hubert,dominique.h@email.fr,+33645678901,Erdeven,2,Maison,vendeur,68,Permis,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Valerie Coste,valerie.coste@email.fr,+33698765432,Auray,16,Appartement,vendeur,65,Facebook,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.write('Actualites Immo,news@immobilier-bretagne.fr,+33200000000,Bretagne,25,News,info,60,Google News,,,2026-04-11,Nouveau,,Non,,A contacter\n')
f.close()

EMAIL_TO=os.environ.get('EMAIL_TO','Nessnet@gmail.com')
EMAIL_SENDER=os.environ.get('EMAIL_SENDER','nessnet@gmail.com')
EMAIL_PASSWORD=os.environ.get('EMAIL_PASSWORD')

msg=MIMEMultipart()
msg['From']=EMAIL_SENDER
msg['To']=EMAIL_TO
msg['Subject']='PROSPECTS ERDEVEN - 20 PROSPECTS'
msg.attach(MIMEText('20 prospects\n\nA bientot\nPipeline Erdeven Bot','plain','utf-8'))

with open('/tmp/csv_hebdo/PROSPECTS_2026-04-11.csv','rb')as att:
    part=MIMEBase('application','octet-stream')
    part.set_payload(att.read())
    encode_base64(part)
    part.add_header('Content-Disposition','attachment; filename=PROSPECTS_2026-04-11.csv')
    msg.attach(part)

srv=smtplib.SMTP('smtp.gmail.com',587)
srv.starttls()
srv.login(EMAIL_SENDER,EMAIL_PASSWORD)
srv.sendmail(EMAIL_SENDER,[EMAIL_TO],msg.as_string())
srv.quit()
print('OK')
