#!/usr/bin/env python3
"""
=============================================================================
ERDEVEN WEEKLY CSV GENERATOR & EMAIL SENDER
=============================================================================
Exécution: Chaque SAMEDI 12:00 (heure France)
Fonction: Générer CSV 50-100 prospects + Envoyer par email
Destinataires: 
  - Nessnet@gmail.com
  - hugobaele31@gmail.com (CC)
=============================================================================
"""

import os
import csv
import json
import smtplib
import sqlite3
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from pathlib import Path
import logging

# ============================================================================
# CONFIGURATION
# ============================================================================

# Emails destinataires
EMAIL_TO = "Nessnet@gmail.com"
EMAIL_CC = "hugobaele31@gmail.com"

# Gmail sender (à configurer avec App Password)
EMAIL_SENDER = os.environ.get('EMAIL_SENDER', 'erdeven.pipeline@gmail.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')  # App Password Google

# Répertoires
OUTPUT_DIR = "/tmp/csv_hebdo"
LOG_FILE = "/tmp/erdeven_weekly.log"

# ============================================================================
# LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# FONCTION: RÉCUPÉRER NOUVEAUX PROSPECTS DE LA BD
# ============================================================================

def get_new_prospects_from_db(days=7):
    """
    Récupère les prospects ajoutés dans les N derniers jours
    depuis la BD SQLite
    """
    
    logger.info(f"Récupération prospects des {days} derniers jours...")
    
    try:
        conn = sqlite3.connect('/tmp/prospection_erdeven.db')
        c = conn.cursor()
        
        # Récupérer prospects depuis N jours
        date_limite = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        c.execute(f"""
            SELECT 
                nom, email, phone, localite, distance_km, type_bien,
                profil, score_vendeur, score_acheteur, source,
                date_ajout
            FROM particuliers
            WHERE date_ajout >= '{date_limite}'
            ORDER BY score_vendeur DESC, date_ajout DESC
            LIMIT 100
        """)
        
        prospects = c.fetchall()
        conn.close()
        
        logger.info(f"✅ {len(prospects)} prospects trouvés")
        return prospects
    
    except Exception as e:
        logger.error(f"❌ Erreur lecture BD: {e}")
        return []

# ============================================================================
# FONCTION: GÉNÉRER CSV
# ============================================================================

def generate_csv(prospects):
    """
    Génère un fichier CSV avec les prospects
    Nom: PROSPECTS_YYYY-MM-DD.csv (date du samedi)
    """
    
    logger.info("Génération du CSV...")
    
    # Créer répertoire s'il n'existe pas
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    # Nom du fichier (date du samedi)
    today = datetime.now()
    csv_filename = f"PROSPECTS_{today.strftime('%Y-%m-%d')}.csv"
    csv_path = os.path.join(OUTPUT_DIR, csv_filename)
    
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Nom', 'Email', 'Téléphone', 'Localité', 'Distance km',
                'Type Bien', 'Profil', 'Score', 'Source Primaire',
                'Sources Alternatives', 'Prix', 'Surface',
                'Date Découverte', 'Status', 'Notes', 'Contacté',
                'Résultat Contact', 'Prochaine Action'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for prospect in prospects:
                writer.writerow({
                    'Nom': prospect[0],
                    'Email': prospect[1] or '',
                    'Téléphone': prospect[2] or '',
                    'Localité': prospect[3],
                    'Distance km': prospect[4],
                    'Type Bien': prospect[5],
                    'Profil': prospect[6],
                    'Score': prospect[7] if prospect[6] == 'vendeur' else prospect[8],
                    'Source Primaire': prospect[9],
                    'Sources Alternatives': '',
                    'Prix': '',
                    'Surface': '',
                    'Date Découverte': prospect[10].strftime('%Y-%m-%d') if prospect[10] else datetime.now().strftime('%Y-%m-%d'),
                    'Status': 'Nouveau',
                    'Notes': '',
                    'Contacté': 'Non',
                    'Résultat Contact': '',
                    'Prochaine Action': 'À contacter'
                })
        
        logger.info(f"✅ CSV créé: {csv_path}")
        return csv_path
    
    except Exception as e:
        logger.error(f"❌ Erreur génération CSV: {e}")
        return None

# ============================================================================
# FONCTION: GÉNÉRER RÉSUMÉ EMAIL
# ============================================================================

def generate_email_body(prospects, csv_filename):
    """
    Génère le corps de l'email avec résumé statistiques
    """
    
    if not prospects:
        return """
Bonjour,

Aucun nouveau prospect cette semaine.

À bientôt,
Pipeline Erdeven Bot
"""
    
    # Statistiques
    total = len(prospects)
    vendeurs = sum(1 for p in prospects if p[6] == 'vendeur')
    acheteurs = total - vendeurs
    score_moyen = sum(p[7] if p[6] == 'vendeur' else p[8] for p in prospects) / total if total > 0 else 0
    meilleur = prospects[0]
    meilleur_score = meilleur[7] if meilleur[6] == 'vendeur' else meilleur[8]
    
    # Sources
    sources = {}
    for p in prospects:
        source = p[9]
        sources[source] = sources.get(source, 0) + 1
    
    sources_str = '\n'.join([f"• {source}: {count}" for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True)])
    
    # Localités
    localites = {}
    for p in prospects:
        loc = p[3]
        localites[loc] = localites.get(loc, 0) + 1
    
    localites_str = ', '.join([f"{loc} ({count})" for loc, count in sorted(localites.items(), key=lambda x: x[1], reverse=True)[:5]])
    
    # Email body
    body = f"""Bonjour,

Veuillez trouver en pièce jointe votre fichier de prospects de cette semaine.

═════════════════════════════════════════════════════════════════════

📊 RÉSUMÉ SEMAINE - {datetime.now().strftime('%d/%m/%Y')}

📈 STATISTIQUES:
- Nouveaux prospects: {total}
- Vendeurs: {vendeurs}
- Acheteurs: {acheteurs}
- Score moyen: {score_moyen:.0f}/100
- Meilleur score: {meilleur_score}/100 ({meilleur[0]} - {meilleur[5]})

📍 RÉPARTITION SOURCES:
{sources_str}

🏙️ LOCALITÉS PRINCIPALES:
{localites_str}

🏆 TOP 5 MEILLEURS PROSPECTS:
"""
    
    # Top 5
    for i, p in enumerate(prospects[:5], 1):
        score = p[7] if p[6] == 'vendeur' else p[8]
        body += f"{i}. {p[0]} - {p[5]} {p[3]} - {score}/100 - {p[6].title()}\n"
    
    body += f"""
═════════════════════════════════════════════════════════════════════

📁 FICHIER: {csv_filename}

💡 PROCHAIN ENVOI: Samedi prochain 12:00 (heure France)

À bientôt,
Pipeline Erdeven Bot
"""
    
    return body

# ============================================================================
# FONCTION: ENVOYER EMAIL
# ============================================================================

def send_email(csv_path, email_to, email_cc, prospects):
    """
    Envoie le CSV par email via Gmail
    """
    
    logger.info(f"Envoi email à {email_to} (CC: {email_cc})...")
    
    if not EMAIL_PASSWORD:
        logger.error("❌ EMAIL_PASSWORD non configurée!")
        return False
    
    try:
        # Créer message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = email_to
        msg['Cc'] = email_cc
        
        csv_filename = os.path.basename(csv_path)
        week_start = (datetime.now() - timedelta(days=7)).strftime('%d-%m-%Y')
        week_end = datetime.now().strftime('%d-%m-%Y')
        
        msg['Subject'] = f"📊 PROSPECTS ERDEVEN - Semaine du {week_start} au {week_end}"
        
        # Corps email
        email_body = generate_email_body(prospects, csv_filename)
        msg.attach(MIMEText(email_body, 'plain', 'utf-8'))
        
        # Pièce jointe CSV
        logger.info(f"Ajout pièce jointe: {csv_filename}")
        with open(csv_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {csv_filename}'
            )
            msg.attach(part)
        
        # Envoyer via Gmail SMTP
        logger.info("Connexion Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        
        # Envoyer à TO + CC
        recipients = [email_to, email_cc]
        text = msg.as_string()
        server.sendmail(EMAIL_SENDER, recipients, text)
        server.quit()
        
        logger.info(f"✅ Email envoyé à {email_to} et {email_cc}")
        return True
    
    except Exception as e:
        logger.error(f"❌ Erreur envoi email: {e}")
        return False

# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """
    Pipeline hebdomadaire complet:
    1. Récupérer prospects semaine
    2. Générer CSV
    3. Envoyer par email
    """
    
    logger.info("="*80)
    logger.info("🚀 PIPELINE HEBDOMADAIRE ERDEVEN - ENVOI CSV")
    logger.info(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*80)
    
    # Étape 1: Récupérer prospects
    prospects = get_new_prospects_from_db(days=7)
    
    if not prospects:
        logger.warning("⚠️ Aucun prospect trouvé pour cette semaine")
        logger.info("Création CSV vide...")
        prospects = []  # Créer CSV vide quand même
    
    # Étape 2: Générer CSV
    csv_path = generate_csv(prospects)
    
    if not csv_path:
        logger.error("❌ Impossible de générer le CSV")
        return False
    
    # Étape 3: Envoyer email
    success = send_email(csv_path, EMAIL_TO, EMAIL_CC, prospects)
    
    logger.info("="*80)
    if success:
        logger.info("✅ PIPELINE TERMINÉ AVEC SUCCÈS")
    else:
        logger.error("❌ ERREUR LORS DE L'ENVOI EMAIL")
    logger.info("="*80)
    
    return success

# ============================================================================
# EXÉCUTION
# ============================================================================

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
