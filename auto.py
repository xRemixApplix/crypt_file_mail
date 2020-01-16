"""
    Fichier général de l'application en automatique
"""

# IMPORT
import json

import module.code_file as code
import module.conso_file as conso
import module.mail as mail
import module.excel as excel
import module.csv as csv


# SCRIPT
with open('options/dest_mail.json') as json_data:
    ARBO_DEST = json.load(json_data)
    
if len(csv.lecture("module/ef_codes_NomSite")) == 1: # Si le fichier de codes est vide
    code.creation()
    mail.envoi("module/ef_codes_NomSite.csv", ARBO_DEST['destinataires'],
               ARBO_DEST['destinataires_cc'], "Fichier de codes", "Fichier de codes.")
