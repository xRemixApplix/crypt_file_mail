"""
    Fichier de la classe Code_file
    Auteur : Remi Invernizzi
    Version : 1.0
    Date : Janvier 2020
"""


# IMPORT MODULES
import random

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
