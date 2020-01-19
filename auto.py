"""
    Fichier général de l'application en automatique
"""

# IMPORT
import datetime
import json

from module.code_file import CodeFile
from module.conso_file import ConsoFile
from module.mail import Mail
from module.csv import Csv
from module.excel import Excel


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

# Declarations Instances de classe
fichier_excel = Excel(STRUCT_FOLD['excel'] + 'test_' + str(datetime.date.today()) + '.xlsx', "DATA")
fichier_code = CodeFile(STRUCT_FOLD['dest_csv_conso'] + 'ef_codes_StChristolDAlbion')
fichier_conso = ConsoFile(STRUCT_FOLD['dest_csv_conso'] + 'ef_consommations_StChristolDAlbion_' + str(datetime.date.today()) + "_" + fichier_code.lecture()[0] + ".csv")
mail = Mail(CONFIG['mail_exp'], ARBO_DEST['destinataires'], ARBO_DEST['destinataires_cc'], 'smtp.gmail.com', CONFIG['pass_mail_exp'], 587)


# Si il n'y a aucun destinataire principal de declare
while len(ARBO_DEST["destinataires"]) == 0:
    ARBO_DEST['destinataires'], ARBO_DEST['destinataires_cc'] = mail.create_dest()

    with open('options/dest_mail.json', "w") as json_data:
        json.dump(ARBO_DEST, json_data)


# Creation du fichier .csv consommation et envoi par mail
liste_conso_excel = fichier_excel.lecture()
liste_conso_csv = fichier_conso.creation(liste_conso_excel, fichier_excel)
fichier_conso.ecriture(liste_conso_csv)
mail.envoi(fichier_conso.file_name, "Rapport EXPL de St Christol d'Albion", "Rapport de consommations presentes sur le site de St Christol d'Albion")


# Si le fichier de codes est vide
if len(fichier_code.lecture()) == 1:
    fichier_code.ecriture(fichier_code.creation())
    mail.envoi(fichier_code.file_name,"Fichier de Codes", "Fichier de Codes pour le site de St Christol d'Albion")