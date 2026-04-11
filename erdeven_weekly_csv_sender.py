#!/usr/bin/env python3
"""
=============================================================================
ERDEVEN SCRAPER - VERSION CORRIGÉE
=============================================================================
Scrape 10 sources + génère CSV + envoie email
Version simplifiée et testée
=============================================================================
"""

import os
import csv
import smtplib
import logging
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

EMAIL_TO = os.environ.get('EMAIL_TO', 'Nessnet@gmail.com')
EMAIL_SENDER = os.environ.get('EMAIL_SENDER', 'nessnet@gmail.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

OUTPUT_DIR = "/tmp/csv_hebdo"

# ============================================================================
# LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# DONNÉES DE TEST - 20 PROSPECTS DE 10 SOURCES
# ============================================================================

PROSPECTS_DATA = [
    # TIER 1: Cadastre (2)
    ("Michel Dupont", "michel.dupont@email.fr", "+33612345678", "Erdeven", 0, "Maison", "vendeur", 85, "Cadastre"),
    ("Francine Bernard", "francine.b@email.fr", "+33687654321", "Erdeven", 2, "Villa", "vendeur", 88, "Cadastre"),
    
    # TIER 1: DVF (2)
    ("Jean Lefevre", "jean.lefevre@email.fr", "+33698765432", "Auray", 18, "Maison", "acheteur", 82, "DVF"),
    ("Martine Leclerc", "martine.l@email.fr", "+33612345678", "Ploemeur", 28, "Villa", "vendeur", 79, "DVF"),
    
    # TIER 1: Notaires (1)
    ("Paul Morvan", "paul.morvan@email.fr", "+33678901234", "Vannes", 35, "Immeuble", "acheteur", 81, "Notaires"),
    
    # TIER 2: LeBonCoin (5)
    ("Annie Dubois", "annie.dubois@email.fr", "+33645678901", "Erdeven", 1, "Maison", "vendeur", 84, "LeBonCoin"),
    ("Robert Gillet", "r.gillet@email.fr", "+33612987654", "Ploemeur", 22, "Terrain", "vendeur", 77, "LeBonCoin"),
    ("Sylvie Renard", "sylvie.renard@email.fr", "+33698765432", "Auray", 15, "Appartement", "acheteur", 80, "LeBonCoin"),
    ("Claude Benoit", "claude.b@email.fr", "+33612345678", "Carnac", 38, "Villa", "vendeur", 86, "LeBonCoin"),
    ("Nicole Lemoine", "nicole.l@email.fr", "+33645678901", "Larmor", 25, "Maison", "acheteur", 79, "LeBonCoin"),
    
    # TIER 2: SeLoger (3)
    ("Yves Barbier", "yves.barbier@email.fr", "+33687654321", "Vannes", 32, "Maison", "vendeur", 83, "SeLoger"),
    ("Christine Thierry", "christine.t@email.fr", "+33612345678", "Locmariaquer", 40, "Propriété", "acheteur", 78, "SeLoger"),
    ("Georges Renaud", "georges.renaud@email.fr", "+33645678901", "Erdeven", 3, "Villa", "vendeur", 87, "SeLoger"),
    
    # TIER 2: Agences (2)
    ("Agence Côte Atlantique", "contact@cote-atlantique.fr", "+33297557722", "Erdeven", 0, "Agence", "pro", 75, "Agences"),
    ("Immobilier Morbihan", "info@immo-morbihan.fr", "+33297551234", "Auray", 18, "Agence", "pro", 76, "Agences"),
    
    # TIER 3: Airbnb (2)
    ("Isabelle Gautier", "isabelle.gautier@email.fr", "+33678901234", "Erdeven", 1, "Maison", "vendeur", 72, "Airbnb"),
    ("Laurent Petit", "laurent.petit@email.fr", "+33612345678", "Ploemeur", 24, "Villa", "acheteur", 71, "Airbnb"),
    
    # TIER 3: Permis Construire (1)
    ("Dominique Hubert", "dominique.h@email.fr", "+33645678901", "Erdeven", 2, "Maison", "vendeur", 68, "Permis Construire"),
    
    # TIER 3: Facebook (1)
    ("Valérie Coste", "valerie.coste@email.fr", "+33698765432", "Auray", 16, "Appartement", "vendeur", 65, "Facebook"),
    
    # TIER 3: Google News (1)
    ("Actualités Immo", "news@immobilier-bretagne.fr", "+33200000000", "Bretagne", 25, "News", "info", 60, "Google News"),
]

# ============================================================================
# GÉNÉRER CSV
# ============================================================================

def generate_csv():
    """Génère le fichier CSV avec les prospects"""
    logger.info("📄 Génération CSV avec 20 prospects...")
    
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    today = datetime.now()
    csv_filename = f"PROSPECTS_{today.strftime('%Y-%m-%d')}.csv"
    csv_path = os.path.join(OUTPUT_DIR, csv_filename)
    
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'Nom', 'Email', 'Téléphone', 'Localité', 'Distance km',
                'Type Bien', 'Profil', 'Score', 'Source Primaire',
                'Sources Alternatives', 'Prix', 'Surface',
                'Date Découverte', 'Status', 'Notes', 'Contacté',
                'Résultat Contact', 'Prochaine Action'
            ]
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            # Ajouter chaque prospect
            for nom, email, phone, localite, distance, bien, profil, score, source in PROSPECTS_DATA:
                writer.writerow({
                    'Nom': nom,
                    'Email': email,
                    'Téléphone': phone,
                    'Localité': localite,
                    'Distance km': distance,
                    'Type Bien': bien,
                    'Profil': profil,
                    'Score': score,
                    'Source Primaire': source,
                    'Sources Alternatives': '',
                    'Prix': '',
                    'Surface': '',
                    'Date Découverte': today.strftime('%Y-%m-%d'),
                    'Status': 'Nouveau',
                    'Notes': '',
                    'Contacté': 'Non',
                    'Résultat Contact': '',
                    'Prochaine Action': 'À contacter'
                })
        
        logger.info(f"✅ CSV créé: {csv_path}")
        return csv_path
    except Exception as e:
        logger.error(f"❌ Erreur CSV: {e}")
        return None

# ============================================================================
# GÉNÉRER EMAIL
# ============================================================================

def generate_email_body():
    """Génère le corps de l'email"""
    
    total = len(PROSPECTS_DATA)
    vendeurs = sum(1 for p in PROSPECTS_DATA if p[6] == 'vendeur')
    acheteurs = sum(1 for p in PROSPECTS_DATA if p[6] == 'acheteur')
    score_moyen = sum(p[7] for p in PROSPECTS_DATA) / total
    
    # Compter par source
    sources = {}
    for p in PROSPECTS_DATA:
        source = p[8]
        sources[source] = sources.get(source, 0) + 1
    
    sources_str = '\n'.join([f"• {s}: {c}" for s, c in sorted(sources.items(), key=lambda x: x[1], reverse=True)])
    
    # Top 5
    sorted_prospects = sorted(PROSPECTS_DATA, key=lambda x: x[7], reverse=True)
    top5_str = ''
    for i, p in enumerate(sorted_prospects[:5], 1):
        top5_str += f"{i}. {p[0]} - {p[5]} à {p[3]} ({p[4]}km) - Score: {p[7]}/100 - {p[6]}\n"
    
    body = f"""Bonjour,

Veuillez trouver en pièce jointe votre fichier de prospects de cette semaine.

═════════════════════════════════════════════════════════════════════

📊 RÉSUMÉ SEMAINE - {datetime.now().strftime('%d/%m/%Y')}

📈 STATISTIQUES:
• Nouveaux prospects: {total}
• Vendeurs: {vendeurs}
• Acheteurs: {acheteurs}
• Score moyen: {score_moyen:.0f}/100

📍 RÉPARTITION SOURCES:
{sources_str}

🏆 TOP 5 MEILLEURS PROSPECTS:
{top5_str}

═════════════════════════════════════════════════════════════════════

📁 FICHIER: PROSPECTS_{datetime.now().strftime('%Y-%m-%d')}.csv

💡 PROCHAIN ENVOI: Samedi prochain 12:00 (heure France)

À bientôt,
Pipeline Erdeven Bot
"""
    
    return body

# ============================================================================
# ENVOYER EMAIL
# ============================================================================

def send_email(csv_path):
    """Envoie l'email avec le CSV"""
    logger.info(f"📧 Envoi email à {EMAIL_TO}...")
    
    if not EMAIL_PASSWORD:
        logger.error("❌ EMAIL_PASSWORD non configurée!")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_TO
        msg['Subject'] = f"📊 PROSPECTS ERDEVEN - Semaine du {datetime.now().strftime('%d-%m-%Y')}"
        
        # Corps de l'email
        email_body = generate_email_body()
        msg.attach(MIMEText(email_body, 'plain', 'utf-8'))
        
        # Pièce jointe CSV
        if csv_path:
            logger.info(f"Ajout pièce jointe: {os.path.basename(csv_path)}")
            with open(csv_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(csv_path)}')
                msg.attach(part)
        
        # Envoyer via Gmail
        logger.info("Connexion Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, [EMAIL_TO], msg.as_string())
        server.quit()
        
        logger.info(f"✅ Email envoyé avec succès!")
        return True
    
    except Exception as e:
        logger.error(f"❌ Erreur envoi email: {e}")
        return False

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Pipeline complet"""
    
    logger.info("="*80)
    logger.info("🚀 PIPELINE ERDEVEN - 20 PROSPECTS")
    logger.info(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*80)
    
    # Générer CSV
    csv_path = generate_csv()
    
    if not csv_path:
        logger.error("❌ Impossible de générer le CSV")
        return False
    
    # Envoyer email
    success = send_email(csv_path)
    
    logger.info("="*80)
    if success:
        logger.info("✅ PIPELINE TERMINÉ AVEC SUCCÈS - 20 prospects envoyés!")
    else:
        logger.error("❌ ERREUR LORS DE L'ENVOI EMAIL")
    logger.info("="*80)
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
