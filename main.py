"""
    Fichier général de l'application pour utilisateur
"""

# IMPORT
import json

import module.mail as mail
import module.gui as gui


# SCRIPT
# Recuperation destinataires des mails
with open('options/dest_mail.json') as json_dest_mail:
    ARBO_DEST = json.load(json_dest_mail)
# Recuperation structures dossier application
with open('options/struct_folder.json') as json_struct_folder:
    STRUCT_FOLD = json.load(json_struct_folder)


# Si il n'y a aucun destinataire principal de declare
while len(ARBO_DEST["destinataires"]) == 0:
    ARBO_DEST['destinataires'], ARBO_DEST['destinataires_cc'] = mail.create_dest()

    with open('options/dest_mail.json', "w") as json_data:
        json.dump(ARBO_DEST, json_data)


# Demarrage de l'interface utilisateur
#####################################################
gui.create()
#####################################################
