"""
    Fichier général de l'application en automatique
"""

# IMPORT
import json

import module.code_file as code
import module.conso_file as conso
import module.mail as mail
import module.csv as csv


# SCRIPT
with open('options/dest_mail.json') as json_data:
    ARBO_DEST = json.load(json_data)


# Creation du fichier .csv consommation et envoi par mail
FILE_CONSO = conso.creation('test.xlsx')
mail.envoi(FILE_CONSO + ".csv", ARBO_DEST['destinataires'],
           ARBO_DEST['destinataires_cc'], "Rapport EXPL de St Christol d'Albion",
           "Rapport de consommations presentes sur le site de St Christol d'Albion")


# Si le fichier de codes est vide
if len(csv.lecture("file_conso/ef_codes_StChristolDAlbion")) == 1:
    code.creation("file_conso/ef_codes_StChristolDAlbion")
    mail.envoi("file_conso/ef_codes_StChristolDAlbion.csv", ARBO_DEST['destinataires'],
               ARBO_DEST['destinataires_cc'], "Fichier de codes", "Fichier de codes.")
