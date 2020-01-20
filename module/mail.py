"""
    Fichier de la classe Mail
    Auteur : Remi Invernizzi
    Version : 1.0
    Date : Janvier 2020
"""


# IMPORT MODULES
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# CLASSE
class Mail:
    """
        Classe Mail : classe servant a la gestion de tout ce qui a un rapport
        avec les mails (authentification, definition des destinataires, etc...)
    """

    EMAIL_REGEX = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'
        r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE
    )

    def __init__(self, exp, dest_princ, dest_cop, smtp_serv, pop_serv, psswd, smtp_port, pop_port):
        """
            Constructeur de la classe 'Mail' :
                - exp           : adresse de l'expediteur (serveur).
                - dest_princ    : destinataire(s) principal(ux) du mail.
                - dest_cop      : destinataire(s) en copie du mail.
                - smtp_serv     : adresse du serveur SMTP.
                - psswd         : mot de passe d'acces au serveur mail.
        """
        self.message = MIMEMultipart()
        self.message['From'] = exp
        self.message['To'] = ','.join(dest_princ)
        self.message['CC'] = ','.join(dest_cop)

        self.smtp_serv = smtp_serv
        self.pop_serv = pop_serv
        self.psswd = psswd
        self.smtp_port = smtp_port
        self.pop_port = pop_port

    def envoi(self, fichier_a_envoyer, sujet_mail, texte_mail):
        """
            Envoi d'un mail :
                - fichier_a_envoyer : adresse du fichier a envoyer en piece jointe.
                - sujet_mail        : titre du mail a envoyer.
                - texte_mail        : texte du mail a envoyer.
        """
        self.message['Subject'] = sujet_mail
        # Corps
        self.message.attach(MIMEText(texte_mail.encode('utf-8'), 'plain', 'utf-8'))
        # Piece jointe
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((open(fichier_a_envoyer, 'rb')).read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            'piece; filename= %s' % fichier_a_envoyer.split('/')[-1]
        )
        self.message.attach(part)

        serveur = smtplib.SMTP(self.smtp_serv, self.smtp_port)
        serveur.starttls()
        serveur.login(self.message['From'], self.psswd)
        print("###   Authentification Reussie   ###")
        serveur.sendmail(
            self.message['From'],
            self.message['To'] + self.message['CC'],
            self.message.as_string().encode('utf-8')
        )
        print("###          Mail envoye         ###")
        serveur.quit()
        print("###  Deconnexion du serveur SMTP ###")

    def create_dest(self):
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
                    if re.match(self.EMAIL_REGEX, adress) is None:
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
