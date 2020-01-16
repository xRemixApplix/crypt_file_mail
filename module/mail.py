"""
    Fichier regroupant les fonctions gérant les mails
"""

# IMPORT
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# CONSTANTES
EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)

# FONCTIONS
def envoi(fichier_a_envoyer, liste_destinataires, liste_destinataires_cc):
    """
        Envoi d'un mail
    """
    # Destinataires
    from_add = "remi.invernizzi@gmail.com"
    to_add = liste_destinataires
    cc_add = liste_destinataires_cc

    message = MIMEMultipart()

    # Entete
    message['From'] = from_add
    message['To'] = ','.join(to_add)
    message['CC'] = ','.join(cc_add)
    message['Subject'] = "Rapport EXPL de XXXXXX"
    # Corps
    msg = "Report de consommation presentes sur le site de XXXXXX"
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
    to_adds = to_add + cc_add

    serveur.sendmail(from_add, to_adds, texte)
    serveur.quit()


def create_dest():
    """
        Declaration des destinataires principaux et en copie pour remplissage
        du fichier JSON les listants
    """
    list_dest = []
    list_dest_cc = []

    # Definitions des destinataires
    print("########################################")
    print("# Creation des destinataires de mails. #")
    print("########################################")

    while True:
        try:
            adress, param = input("Adresse Destinaire : ").split(' ')
        except ValueError:
            # Texte en rouge
            print('\x1b[6;31;40m'
                  + "Erreur de syntaxe"
                  + '\x1b[0m')
        else:
            if adress.upper() != "Q":
                if re.match(EMAIL_REGEX, adress) is None:
                    # Texte en orange
                    print('\x1b[6;33;40m'
                          + "Format de l'adresse incorrecte"
                          + '\x1b[0m')
                else:
                    if param.upper() == "D":
                        list_dest.append(adress.lower())
                    elif param.upper() == "C":
                        list_dest_cc.append(adress.lower())
                    else:
                        # Texte en orange
                        print('\x1b[6;33;40m'
                              + "Etat Destinataire non reconnu (D: Principal, C: Copie)"
                              + '\x1b[0m')
            else:
                break

    return list_dest, list_dest_cc


# AUTO-LANCEMENT
if __name__ == '__main__':
    envoi("test_conso.csv", ["r.invernizzi@jp-indus.fr"], [""])
