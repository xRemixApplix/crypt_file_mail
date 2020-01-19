"""
    Fichier de la classe Csv
    Auteur : Remi Invernizzi
    Version : 1.0
    Date : Janvier 2020
"""


# IMPORT MODULES
###


# CLASSE
class Csv:
    """
        Classe Csv : classe servant a la gestion de tout ce qui a un rapport
        avec les differents fiichiers .csv.
    """

    def __init__(self, file_name):
        """
            Constructeur de la classe 'Csv' :
                - file_name     : nom du fichier.
        """
        self.file_name = file_name

    def ecriture(self, list_info):
        """
            Ecriture d'une liste dans un fichier .csv
        """
        with open(self.file_name, 'w') as file_csv:
            for code in list_info:
                file_csv.write(str(code))
                file_csv.write('\n')

    def lecture(self):
        """
            Lecture d'un fichier .csv retournant une liste
        """
        with open(self.file_name + ".csv", 'r') as file_csv:
            return file_csv.read().split('\n')
