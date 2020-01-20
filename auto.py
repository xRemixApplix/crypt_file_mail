"""
    Fichier général de l'application en automatique
"""

# IMPORT
import datetime
import json
import signal
import sys
import poplib
import email.parser

from module.code_file import CodeFile
from module.conso_file import ConsoFile
from module.mail import Mail
from module.excel import Excel


# DETECTION FERMETURE PROGRAMME
def fermer_programme(signal, frame):
    """
        Detection de la fermeture du programme
    """
    print("FERMETURE")
    sys.exit()
signal.signal(signal.SIGINT, fermer_programme)

# SCRIPT
# Recuperation config application
with open('options/config.json') as json_config:
    CONFIG = json.load(json_config)
# Recuperation destinataires des mails
with open('options/dest_mail.json') as json_dest_mail:
    ARBO_DEST = json.load(json_dest_mail)
# Recuperation structures dossier application
with open('options/struct_folder.json') as json_struct_folder:
    STRUCT_FOLD = json.load(json_struct_folder)

# Declarations Instances de classe + CONSTANTES
FICHIER_EXCEL = Excel(STRUCT_FOLD['excel'] + 'test_' + str(datetime.date.today()) + '.xlsx', "DATA")
FICHIER_CODE = CodeFile(STRUCT_FOLD['dest_csv_conso'] + 'ef_codes_StChristolDAlbion')
FICHIER_CONSO = ConsoFile(STRUCT_FOLD['dest_csv_conso'] + 'ef_consommations_StChristolDAlbion_'
                          + str(datetime.date.today()) + "_" + FICHIER_CODE.lecture()[0] + ".csv")
MAIL = Mail(
    CONFIG['mail_exp'],
    ARBO_DEST['destinataires'],
    ARBO_DEST['destinataires_cc'],
    'smtp.gmail.com',
    'pop.googlemail.com',
    CONFIG['pass_mail_exp'],
    587,
    995
)

# FONCTIONS  
def ecriture_fichier_conso():
    LISTE_CONSO_EXCEL = FICHIER_EXCEL.lecture()
    LISTE_CONSO_CSV = FICHIER_CONSO.creation(LISTE_CONSO_EXCEL)
    FICHIER_CONSO.ecriture(LISTE_CONSO_CSV)

# Si il n'y a aucun destinataire principal de declare
while len(ARBO_DEST["destinataires"]) == 0:
    ARBO_DEST['destinataires'], ARBO_DEST['destinataires_cc'] = MAIL.create_dest()

    with open('options/dest_mail.json', "w") as json_data:
        json.dump(ARBO_DEST, json_data)

print("Initialisation : OK")
print("En Attente...")
send = False
while True:
    # Datetime
    courant = datetime.datetime.now()

    # Detection Reception Mail
    Mailbox = poplib.POP3_SSL(MAIL.pop_serv, MAIL.pop_port)
    Mailbox.user(MAIL.message['From'])
    Mailbox.pass_(MAIL.psswd)

    resp, items, octets = Mailbox.list()

    if len(items) > 0:
        print("Detection Reception Email(s)")
        for k in items:
            presp, text, octets = Mailbox.retr(int(k.decode("utf-8").split()[0]))
            text = [i.decode("utf-8") for i in text]
            text = [i for i in text if ':' in i]
            text = "\n".join(text)

            message = email.parser.Parser().parsestr(text)

            if message['Code'] == 'SI-01':
                print("Erreur SI-01")
                # Recuperation du dernier fichier envoye dans le dossier où il se trouve
                # Envoi du fichier
            elif message['Code'] == 'SI-02':
                print("Erreur SI-02")
                # Recuperation du dernier nom de fichier créé
                # Verification de la structure du nom
                # Renvoi du fichier par mail
            elif message['Code'] == 'SI-03':
                print("Erreur SI-03")
                # Recuperation du dernier nom de fichier créé
                # Recreation d'un fichier avec le meme nom 'corrige'
                # Envoi du fichier par mail
            elif message['Code'] == 'SI-04':
                print("Erreur SI-04")
                # Recuperation du dernier nom de fichier créé
                # Recreation d'un fichier avec le meme nom 'corrige'
                # Envoi du fichier par mail
            else:
                pass
                # A voir quelles actions faire....

    Mailbox.quit()

    if int(courant.hour) in CONFIG['heure_envoi_conso'] and not send:
        # Creation du fichier .csv consommation et envoi par mail
        ecriture_fichier_conso()
        MAIL.envoi(
            FICHIER_CONSO.file_name,
            "Rapport EXPL de St Christol d'Albion",
            "Rapport de consommations presentes sur le site de St Christol d'Albion"
        )

        # Si le fichier de codes est vide
        if len(FICHIER_CODE.lecture()) == 1:
            FICHIER_CODE.ecriture(FICHIER_CODE.creation())
            MAIL.envoi(
                FICHIER_CODE.file_name,
                "Fichier de Codes",
                "Fichier de Codes d'identification pour le site de St Christol d'Albion"
            )

        send = True

    if int(courant.hour) not in CONFIG['heure_envoi_conso']:
        send = False
