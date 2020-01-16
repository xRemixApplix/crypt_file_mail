"""
    Fichier général de l'application
"""

# IMPORT
import json

import module.code_file as code
import module.conso_file as conso
import module.mail as mail
import module.excel as excel


# SCRIPT
with open('options/dest_mail.json') as json_data:
    ARBO_DEST = json.load(json_data)

while len(ARBO_DEST["destinataires"]) == 0:
    ARBO_DEST['destinataires'], ARBO_DEST['destinataires_cc'] = mail.create_dest()

    with open('options/dest_mail.json', "w") as json_data:
        json.dump(ARBO_DEST, json_data)
