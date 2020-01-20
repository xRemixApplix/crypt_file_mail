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
    CONFIG['pass_mail_exp'],
    587
)

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
    Mailbox = poplib.POP3_SSL('pop.googlemail.com', '995')
    Mailbox.user(CONFIG['mail_exp'])
    Mailbox.pass_(CONFIG['pass_mail_exp'])

    resp, items, octets = Mailbox.list()

    if len(items) > 0:
        print("Detection Reception Email(s)")
        for k in items:
            presp, text, octets = Mailbox.retr(int(k.decode("utf-8").split()[0]))
            text = [i.decode("utf-8") for i in text]
            text = [i for i in text if ':' in i]
            text = "\n".join(text)

            message = email.parser.Parser().parsestr(text)

            print(message['Code'])

    Mailbox.quit()

    if int(courant.hour) == 14 and not send:
        # Creation du fichier .csv consommation et envoi par mail
        LISTE_CONSO_EXCEL = FICHIER_EXCEL.lecture()
        LISTE_CONSO_CSV = FICHIER_CONSO.creation(LISTE_CONSO_EXCEL)
        FICHIER_CONSO.ecriture(LISTE_CONSO_CSV)
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

    if int(courant.hour) != 14:
        send = False
