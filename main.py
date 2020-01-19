"""
    Script general permettant de lancer la version utilisateur de l'application.
"""

# IMPORT
import json

import module.code_file as code
import module.conso_file as conso
import module.mail as mail
import module.excel as excel
import module.csv as csv


# SCRIPT
# Recuperation destinataires des mails
with open('options/dest_mail.json') as json_dest_mail:
    ARBO_DEST = json.load(json_dest_mail)
# Recuperation structures dossier application
with open('options/struct_folder.json') as json_struct_folder:
    STRUCT_FOLD = json.load(json_struct_folder)
