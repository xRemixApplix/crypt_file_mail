"""
    Fichier général de l'application en automatique
"""

# IMPORT
import datetime
import json

import module.code_file as code
import module.conso_file as conso
import module.mail as mail
import module.csv as csv


# SCRIPT
# Recuperation destinataires des mails
with open('options/dest_mail.json') as json_dest_mail:
    ARBO_DEST = json.load(json_dest_mail)
# Recuperation structures dossier application
with open('options/struct_folder.json') as json_struct_folder:
    STRUCT_FOLD = json.load(json_struct_folder)


# Creation du fichier .csv consommation et envoi par mail
FILE_CONSO = conso.creation(STRUCT_FOLD['excel'] + 'test_' + str(datetime.date.today())
                            + '.xlsx', STRUCT_FOLD)
mail.envoi(FILE_CONSO + '.csv', ARBO_DEST['destinataires'],
           ARBO_DEST['destinataires_cc'], "Rapport EXPL de St Christol d'Albion",
           "Rapport de consommations presentes sur le site de St Christol d'Albion")


# Si le fichier de codes est vide
if len(csv.lecture(STRUCT_FOLD['dest_csv_conso'] + 'ef_codes_StChristolDAlbion')) == 1:
    code.creation(STRUCT_FOLD['dest_csv_conso']
                  + 'ef_codes_StChristolDAlbion')
    mail.envoi(STRUCT_FOLD['dest_csv_conso'] + 'ef_codes_StChristolDAlbion.csv',
               ARBO_DEST['destinataires'],
               ARBO_DEST['destinataires_cc'], "Fichier de codes", "Fichier de codes.")
