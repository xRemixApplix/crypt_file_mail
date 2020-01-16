"""
    Fichier général de l'application
"""

# IMPORT
import module.code_file as code
import module.conso_file as conso
import module.mail as mail
import module.excel as excel

import json

# SCRIPT
with open('options/dest_mail.json') as json_data:
    arbo_dest = json.load(json_data)
    
while len(arbo_dest["destinataires"])==0:
    arbo_dest['destinataires'], arbo_dest['destinataires_cc'] = mail.create_dest()
    
    with open('options/dest_mail.json', "w") as json_data:
        json.dump(arbo_dest, json_data)
