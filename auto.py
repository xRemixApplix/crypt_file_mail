"""
    Fichier général de l'application en automatique
"""

# IMPORT
import datetime
import time
import json
import signal
import sys
import poplib
import email.parser
import os

from module.code_file import CodeFile
from module.conso_file import ConsoFile
from module.mail import Mail
from module.excel import Excel


# DETECTION FERMETURE PROGRAMME
def fermer_programme(signal_close, frame_close):
    """
        Detection de la fermeture du programme
    """
    print("##### FERMETURE DU PROGRAMME #####")
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
# Recuperation transformation intutilé mesure
with open('options/transfo_nom.json', encoding="utf-8") as json_transfo_nom:
    TRANSFO_NOM = json.load(json_transfo_nom)

# Declarations Instances de classe + CONSTANTES
FICHIER_CODE = CodeFile(STRUCT_FOLD['dest_csv_conso'] + 'ef_codes_StChristolDAlbion.csv')

# FONCTIONS
print("##### LANCEMENT DU PROGRAMME #####")
print("Initialisation : OK")
print("En Attente...")
send = False
while True:
    FICHIER_EXCEL_00 = Excel(STRUCT_FOLD['excel'] + '70001-Index Cpt ESID - Rapport Jour 00H-81-' + str(datetime.date.today().strftime("%y%m%d")) + '-0010.xlsx', "DATA")
    FICHIER_EXCEL_12 = Excel(STRUCT_FOLD['excel'] + '70001-Index Cpt ESID - Rapport Jour 12H-71-' + str(datetime.date.today().strftime("%y%m%d")) + '-1210.xlsx', "DATA")

    MAIL = Mail(
        CONFIG['mail_exp'],
        ARBO_DEST['destinataires'],
        ARBO_DEST['destinataires_cc'],
        'smtp.def.gouv.fr',
        'pop.def.gouv.fr',
        CONFIG['pass_mail_exp'],
        587,
        995
    )

    def ecriture_fichier_conso(heure):
        """
            Fonction reunissant tout les appels necessaires à la creation du
            fichier .csv de consommation.
        """
        LISTE_CONSO_EXCEL = FICHIER_EXCEL_00.lecture() if heure==1 else FICHIER_EXCEL_12.lecture()
        LISTE_CONSO_CSV = FICHIER_CONSO.creation(LISTE_CONSO_EXCEL, TRANSFO_NOM)
        FICHIER_CONSO.ecriture(LISTE_CONSO_CSV)

    def recup_nom_dernier_fichier(folder):
        """
            Recuperation du nom du dernier fichier de consommation
            créé.
        """
        print("Recuperation dernier fichier consommation envoye")
        # Recuperation du dernier fichier envoye dans le dossier où il se trouve
        liste = os.listdir(folder)
        id_last = 0
        for i in range(len(liste)):
            fichier_a_tester = float(os.path.getctime(STRUCT_FOLD['dest_csv_conso'] + "/" +\
                liste[i]))
            dernier_fichier = float(os.path.getctime(STRUCT_FOLD['dest_csv_conso'] + "/" +\
                liste[id_last]))
            if fichier_a_tester >= dernier_fichier:
                id_last = i
        print("Recuperation OK.")
        return liste[id_last]

    def verif_nom_fichier(nom_fichier):
        """
            Vérification du nom du dernier fichier de consommation
            créé.
        """
        verif_fichier = 'ef_consommations_StChristolDAlbion_' + str(datetime.date.today()) + "_" \
            + CONFIG['last_id'] + ".csv"
        if nom_fichier != verif_fichier:
            print("Nom du fichier incorrect.")
            print(">>>>>>>>>>>>>>>", nom_fichier)
            print("<<<<<<<<<<<<<<<", verif_fichier)
            print("Renommage du fichier.")
            os.rename(
                STRUCT_FOLD['dest_csv_conso'] + "/" + nom_fichier,
                STRUCT_FOLD['dest_csv_conso'] + "/" + verif_fichier
            )
        else:
            print("Le nom du fichier semble correct.")
            print("Merci d'effectuer une verification manuelle.")

        return verif_fichier

    # Si il n'y a aucun destinataire principal de declare
    while len(ARBO_DEST["destinataires"]) == 0:
        print("Creation de destinataires.")
        ARBO_DEST['destinataires'], ARBO_DEST['destinataires_cc'] = MAIL.create_dest()

        with open('options/dest_mail.json', "w") as json_data:
            json.dump(ARBO_DEST, json_data)

    # Datetime
    courant = datetime.datetime.now()

    # Detection Reception Mail
    """
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

            if message['From'].replace('<', '').replace('>', '') in ARBO_DEST['destinataires']:
                print("Expediteur reconnu :", message['From'])
                if message['Code'] == 'SI-01':
                    print("Erreur SI-01")
                    # Recuperation du dernier fichier envoye dans le dossier ou il se trouve
                    nom_last = recup_nom_dernier_fichier(STRUCT_FOLD['dest_csv_conso'])
                    print("Renvoi du mail")
                    # Envoi du fichier
                    MAIL.envoi(
                        STRUCT_FOLD['dest_csv_conso'] + "/" + nom_last,
                        "Rapport EXPL de St Christol d'Albion",
                        "Rapport de consommations presentes sur le site de St Christol d'Albion"
                    )
                elif message['Code'] == 'SI-02':
                    print("Erreur SI-02")
                    # Recuperation du dernier nom de fichier cree
                    nom_last = recup_nom_dernier_fichier(STRUCT_FOLD['dest_csv_conso'])
                    # Verification de la structure du nom
                    nom_verif = verif_nom_fichier(nom_last)
                    if nom_verif != nom_last:
                        # Renvoi du fichier par mail
                        MAIL.envoi(
                            STRUCT_FOLD['dest_csv_conso'] + "/" + nom_verif,
                            "Rapport EXPL de St Christol d'Albion",
                            "Rapport de consommations presentes sur le site de St Christol d'Albion"
                        )
                elif message['Code'] == 'SI-03':
                    print("Erreur SI-03")
                    # Recuperation du dernier nom de fichier cree
                    nom_last = recup_nom_dernier_fichier(STRUCT_FOLD['dest_csv_conso'])
                    # Recreation d'un fichier avec le meme nom 'corrige'
                    nom_verif = verif_nom_fichier(nom_last)
                    # Envoi du fichier par mail
                    if nom_verif != nom_last:
                        # Renvoi du fichier par mail
                        MAIL.envoi(
                            STRUCT_FOLD['dest_csv_conso'] + "/" + nom_verif,
                            "Rapport EXPL de St Christol d'Albion",
                            "Rapport de consommations presentes sur le site de St Christol d'Albion"
                        )
                elif message['Code'] == 'SI-04':
                    print("Erreur SI-04")
                    # Recuperation du dernier nom de fichier créé
                    nom_last = recup_nom_dernier_fichier(STRUCT_FOLD['dest_csv_conso'])
                    # Recreation d'un fichier avec le meme nom 'corrige'
                    # Envoi du fichier par mail
                else:
                    pass
                    # A voir quelles actions faire....
            else:
                print("Expediteur inconnu :", message['From'])

    Mailbox.quit()
    """
    if int(courant.hour) in CONFIG['heure_envoi_conso'] and not send:
        # Creation du fichier .csv consommation et envoi par mail
        FICHIER_CONSO = ConsoFile(STRUCT_FOLD['dest_csv_conso'] + 'ef_consommations_StChristolDAlbion_'
                          + str(datetime.date.today()) + "_" + FICHIER_CODE.lecture()[0] + ".csv")
        print("Creation Fichier : {}".format(FICHIER_CONSO.file_name))
        CONFIG['last_id'] = FICHIER_CODE.lecture()[0]
        ecriture_fichier_conso(int(courant.hour))
        
        with open('options/config.json', 'w') as json_config:
            json_config.write(json.dumps(CONFIG))
            
        FICHIER_CODE.mise_a_jour(FICHIER_CODE.lecture()[1:-1])

        MAIL.envoi(
            FICHIER_CONSO.file_name,
            "Rapport EXPL de St Christol d'Albion",
            "Rapport de consommations presentes sur le site de St Christol d'Albion"
        )

        # Si le fichier de codes est vide
        if len(FICHIER_CODE.lecture()) == 1:
            FICHIER_CODE.ecriture(FICHIER_CODE.creation(), STRUCT_FOLD)
            
            MAIL.envoi(
                FICHIER_CODE.file_name,
                "Fichier de Codes",
                "Fichier de Codes d'identification pour le site de St Christol d'Albion"
            )
            

        send = True

    if int(courant.hour) not in CONFIG['heure_envoi_conso']:
        send = False

    time.sleep(60)
