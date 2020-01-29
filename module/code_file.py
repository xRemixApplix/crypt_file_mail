"""
    Fichier de la classe Code_file
    Auteur : Remi Invernizzi
    Version : 1.0
    Date : Janvier 2020
"""


# IMPORT MODULES
import random
import shutil
import datetime

from module.csv import Csv


# CLASSE
class CodeFile(Csv):
    """
        Classe CodeFile : classe servant a la gestion de tout ce qui a un rapport
        avec le fichier de code
    """

    NBRE_LIGNES = 1000
    LISTE_CARAC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    def __init__(self, file_name):
        """
            Constructeur de la classe 'CodeFile' :
                - file_name     : nom du fichier de code.
        """
        Csv.__init__(self, file_name)

    def creation(self):
        """
            Creation du fichier .csv contenant les milles identifiants permettant de reconnaitre
            les fichiers transmis par mail.
        """
        list_codes = []
        while len(list_codes) < self.NBRE_LIGNES:
            temp = ""
            while len(temp) < 4:
                temp += self.LISTE_CARAC[random.randint(0, len(self.LISTE_CARAC)-1)]

            if temp not in list_codes:
                list_codes.append(temp)

        return list_codes

    def ecriture(self, list_info, STRUCT_FOLD):
        """
            Ecriture d'une liste dans un fichier .csv
        """
        Csv.ecriture(self, list_info)
        # Copie du fichier pour archivage
        shutil.copy(
            self.file_name,
            STRUCT_FOLD['dest_csv_code_archiv'] + 'ef_codes_StChristolDAlbion_' +\
                 str(datetime.date.today()) + ".csv"
        )

    def mise_a_jour(self, list_info):
        """
           Mise a jour des informations contenu dans un fichier .csv
        """
        Csv.ecriture(self, list_info)
