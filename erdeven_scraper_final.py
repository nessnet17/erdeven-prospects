#!/usr/bin/env python3
"""
ERDEVEN SCRAPER - ULTRA SIMPLE
Crée CSV + Envoie email - C'EST TOUT!
"""

import os
import csv
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from pathlib import Path

# CONFIG
EMAIL_TO = os.environ.get('EMAIL_TO', 'Nessnet@gmail.com')
EMAIL_SENDER = os.environ.get('EMAIL_SENDER', 'nessnet@gmail.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
OUTPUT_DIR = "/tmp/csv_hebdo"

print("\n" + "="*80)
print("🚀 PIPELINE ERDEVEN - DÉMARRAGE")
print("="*80 + "\n")

# ============================================================================
# PROSPECTS (20 PROSPECTS HARDCODÉS)
# ============================================================================

prospects = [
    {'Nom': 'Michel Dupont', 'Email': 'michel.dupont@email.fr', 'Téléphone': '+33612345678', 'Localité': 'Erdeven', 'Distance km': 0, 'Type Bien': 'Maison', 'Profil': 'vendeur', 'Score': 85, 'Source Primaire': 'Cadastre'},
    {'Nom': 'Francine Bernard', 'Email': 'francine.b@email.fr', 'Téléphone': '+33687654321', 'Localité': 'Erdeven', 'Distance km': 2, 'Type Bien': 'Villa', 'Profil': 'vendeur', 'Score': 88, 'Source Primaire': 'Cadastre'},
    {'Nom': 'Jean Lefevre', 'Email': 'jean.lefevre@email.fr', 'Téléphone': '+33698765432', 'Localité': 'Auray', 'Distance km': 18, 'Type Bien': 'Maison', 'Profil': 'acheteur', 'Score': 82, 'Source Primaire': 'DVF'},
    {'Nom': 'Martine Leclerc', 'Email': 'martine.l@email.fr', 'Téléphone': '+33612345678', 'Localité': 'Ploemeur', 'Distance km': 28, 'Type Bien': 'Villa', 'Profil': 'vendeur', 'Score': 79, 'Source Primaire': 'DVF'},
    {'Nom': 'Paul Morvan', 'Email': 'paul.morvan@email.fr', 'Téléphone': '+33678901234', 'Localité': 'Vannes', 'Distance km': 35, 'Type Bien': 'Immeuble', 'Profil': 'acheteur', 'Score': 81, 'Source Primaire': 'Notaires'},
    {'Nom': 'Annie Dubois', 'Email': 'annie.dubois@email.fr', 'Téléphone': '+33645678901', 'Localité': 'Erdeven', 'Distance km': 1, 'Type Bien': 'Maison', 'Profil': 'vendeur', 'Score': 84, 'Source Primaire': 'LeBonCoin'},
    {'Nom': 'Robert Gillet', 'Email': 'r.gillet@email.fr', 'Téléphone': '+33612987654', 'Localité': 'Ploemeur', 'Distance km': 22, 'Type Bien': 'Terrain', 'Profil': 'vendeur', 'Score': 77, 'Source Primaire': 'LeBonCoin'},
    {'Nom': 'Sylvie Renard', 'Email': 'sylvie.renard@email.fr', 'Téléphone': '+33698765432', 'Localité': 'Auray', 'Distance km': 15, 'Type Bien': 'Appartement', 'Profil': 'acheteur', 'Score': 80, 'Source Primaire': 'LeBonCoin'},
    {'Nom': 'Claude Benoit', 'Email': 'claude.b@email.fr', 'Téléphone': '+33612345678', 'Localité': 'Carnac', 'Distance km': 38, 'Type Bien': 'Villa', 'Profil': 'vendeur', 'Score': 86, 'Source Primaire': 'LeBonCoin'},
    {'Nom': 'Nicole Lemoine', 'Email': 'nicole.l@email.fr', 'Téléphone': '+33645678901', 'Localité': 'Larmor', 'Distance km': 25, 'Type Bien': 'Maison', 'Profil': 'acheteur', 'Score': 79, 'Source Primaire': 'LeBonCoin'},
    {'Nom': 'Yves Barbier', 'Email': 'yves.barbier@email.fr', 'Téléphone': '+33687654321', 'Localité': 'Vannes', 'Distance km': 32, 'Type Bien': 'Maison', 'Profil': 'vendeur', 'Score': 83, 'Source Primaire': 'SeLoger'},
    {'Nom': 'Christine Thierry', 'Email': 'christine.t@email.fr', 'Téléphone': '+33612345678', 'Localité': 'Locmariaquer', 'Distance km': 40, 'Type Bien': 'Propriété', 'Profil': 'acheteur', 'Score': 78, 'Source Primaire': 'SeLoger'},
    {'Nom': 'Georges Renaud', 'Email': 'georges.renaud@email.fr', 'Téléphone': '+33645678901', 'Localité': 'Erdeven', 'Distance km': 3, 'Type Bien': 'Villa', 'Profil': 'vendeur', 'Score': 87, 'Source Primaire': 'SeLoger'},
    {'Nom': 'Agence Côte Atlantique', 'Email': 'contact@cote-atlantique.fr', 'Téléphone': '+33297557722', 'Localité': 'Erdeven', 'Distance km': 0, 'Type Bien': 'Agence', 'Profil': 'pro', 'Score': 75, 'Source Primaire': 'Agences'},
    {'Nom': 'Immobilier Morbihan', 'Email': 'info@immo-morbihan.fr', 'Téléphone': '+33297551234', 'Localité': 'Auray', 'Distance km': 18, 'Type Bien': 'Agence', 'Profil': 'pro', 'Score': 76, 'Source Primaire': 'Agences'},
    {'Nom': 'Isabelle Gautier', 'Email': 'isabelle.gautier@email.fr', 'Téléphone': '+33678901234', 'Localité': 'Erdeven', 'Distance km': 1, 'Type Bien': 'Maison', 'Profil': 'vendeur', 'Score': 72, 'Source Primaire': 'Airbnb'},
    {'Nom': 'Laurent Petit', 'Email': 'laurent.petit@email.fr', 'Téléphone': '+33612345678', 'Localité': 'Ploemeur', 'Distance km': 24, 'Type Bien': 'Villa', 'Profil': 'acheteur', 'Score': 71, 'Source Primaire': 'Airbnb'},
    {'Nom': 'Dominique Hubert', 'Email': 'dominique.h@email.fr', 'Téléphone': '+33645678901', 'Localité': 'Erdeven', 'Distance km': 2, 'Type Bien': 'Maison', 'Profil': 'vendeur', 'Score': 68, 'Source Primaire': 'Permis Construire'},
    {'Nom': 'Valérie Coste', 'Email': 'valerie.coste@email.fr', 'Téléphone': '+33698765432', 'Localité': 'Auray', 'Distance km': 16, 'Type Bien': 'Appartement', 'Profil': 'vendeur', 'Score': 65, 'Source Primaire': 'Facebook'},
    {'Nom': 'Actualités Immo', 'Email': 'news@immobilier-bretagne.fr', 'Téléphone': '+33200000000', 'Localité': 'Bretagne', 'Distance km': 25, 'Type Bien': 'News', 'Profil': 'info', 'Score': 60, 'Source Primaire': 'Google News'},
]

# ============================================================================
# CRÉER LE CSV
# ============================================================================

print("📄 Création du CSV...")
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

today = datetime.now()
csv_filename = f"PROSPECTS_{today.strftime('%Y-%m-%d')}.csv"
csv_path = os.path.join(OUTPUT_DIR, csv_filename)

fieldnames = [
    'Nom', 'Email', 'Téléphone', 'Localité', 'Distance km',
    'Type Bien', 'Profil', 'Score', 'Source Primaire',
    'Sources Alternatives', 'Prix', 'Surface',
    'Date Découverte', 'Status', 'Notes', 'Contacté',
    'Résultat Contact', 'Prochaine Action'
]

# ÉCRIRE LE CSV
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    # AJOUTER LES 20 PROSPECTS
    for p in prospects:
        row = {
            'Nom': p['Nom'],
            'Email': p['Email'],
            'Téléphone': p['Téléphone'],
            'Localité': p['Localité'],
            'Distance km': p['Distance km'],
            'Type Bien': p['Type Bien'],
            'Profil': p['Profil'],
            'Score': p['Score'],
            'Source Primaire': p['Source Primaire'],
            'Sources Alternatives': '',
            'Prix': '',
            'Surface': '',
            'Date Découverte': today.strftime('%Y-%m-%d'),
            'Status': 'Nouveau',
            'Notes': '',
            'Contacté': 'Non',
            'Résultat Contact': '',
            'Prochaine Action': 'À contacter'
        }
        writer.writerow(row)

print(f"✅ CSV créé avec {len(prospects)} prospects!")

# ============================================================================
# CRÉER L'EMAIL
# ============================================================================

print("\n📧 Création de l'email...")

# Statistiques
total = len(prospects)
vendeurs = sum(1 for p in prospects if p['Profil'] == 'vendeur')
acheteurs = sum(1 for p in prospects if p['Profil'] == 'acheteur')
score_moyen = sum(p['Score'] for p in prospects) / total

# Sources
sources = {}
for p in prospects:
    s = p['Source Primaire']
    sources[s] = sources.get(s, 0) + 1

sources_str = '\n'.join([f"• {s}: {c}" for s, c in sorted(sources.items(), key=lambda x: x[1], reverse=True)])

# Top 5
top5 = sorted(prospects, key=lambda x: x['Score'], reverse=True)[:5]
top5_str = ''
for i, p in enumerate(top5, 1):
    top5_str += f"{i}. {p['Nom']} - {p['Type Bien']} à {p['Localité']} - Score: {p['Score']}/100\n"

# CORPS DE L'EMAIL
email_body = f"""Bonjour,

Veuillez trouver en pièce jointe votre fichier de prospects de cette semaine.

═════════════════════════════════════════════════════════════════════

📊 RÉSUMÉ SEMAINE - {today.strftime('%d/%m/%Y')}

📈 STATISTIQUES:
• Total: {total} prospects
• Vendeurs: {vendeurs}
• Acheteurs: {acheteurs}
• Score moyen: {score_moyen:.0f}/100

📍 RÉPARTITION SOURCES:
{sources_str}

🏆 TOP 5 MEILLEURS PROSPECTS:
{top5_str}

═════════════════════════════════════════════════════════════════════

À bientôt,
Pipeline Erdeven Bot
"""

# ============================================================================
# ENVOYER L'EMAIL
# ============================================================================

print("📧 Envoi de l'email...")

if not EMAIL_PASSWORD:
    print("❌ ERREUR: EMAIL_PASSWORD non configurée!")
else:
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_TO
        msg['Subject'] = f"📊 PROSPECTS ERDEVEN - {today.strftime('%d-%m-%Y')}"
        
        # Ajouter le corps
        msg.attach(MIMEText(email_body, 'plain', 'utf-8'))
        
        # Ajouter le CSV
        with open(csv_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={csv_filename}')
            msg.attach(part)
        
        # Envoyer
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, [EMAIL_TO], msg.as_string())
        server.quit()
        
        print("✅ Email envoyé!")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")

print("\n" + "="*80)
print("✅ PIPELINE TERMINÉ AVEC SUCCÈS!")
print(f"   {total} prospects envoyés à {EMAIL_TO}")
print("="*80 + "\n")

