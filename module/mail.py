"""
    Fichier regroupant les fonctions gérant les mails
"""

# IMPORT
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# CONSTANTES

# FONCTIONS
def envoi(fichier_a_envoyer):
    """
        Envoi d'un mail
    """
    # Destinataires
    from_add = "remi.invernizzi@gmail.com"
    to_add = "r.invernizzi@jp-indus.fr"
    cc_add = ""
    
    message = MIMEMultipart()
    
    # Entete
    message['From'] = from_add
    message['To'] = to_add
    message['CC'] = cc_add
    message['Subject'] = "Test Envoi Mail en Python"
    # Corps
    msg = "Test Mail à l'aide d'un script codé en python"
    message.attach(MIMEText(msg.encode('utf-8'), 'plain', 'utf-8'))
    # Piece jointe    
    nom_piece_jointe = fichier_a_envoyer.split('/')[-1]
    piece = open(fichier_a_envoyer, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((piece).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'piece; filename= %s' % nom_piece_jointe)
    message.attach(part)
    # Connexion au serveur sortant de l'expéditeur
    serveur = smtplib.SMTP('smtp.gmail.com', 587)
    # Specification de la securisation
    serveur.starttls()
    # Authentification Expediteur
    serveur.login(from_add, "22bp86g5mf937ztk")
    texte = message.as_string().encode('utf-8')
    to_adds = [to_add] + [cc_add]

    serveur.sendmail(from_add, to_adds, texte)
    serveur.quit()


# AUTO-LANCEMENT
if __name__ == '__main__':
    envoi("test_conso.csv")
