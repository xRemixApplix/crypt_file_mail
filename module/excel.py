"""
    Fichier de la classe Excel
    Auteur : Remi Invernizzi
    Version : 1.0
    Date : Janvier 2020
"""


# IMPORT MODULES
import datetime
import xlrd


# CLASSE
class Excel:
    """
        Classe Excel : classe servant a la gestion de tout ce qui a un rapport
        avec le fichier excel a lire avant envoi par mail.
    """

    def __init__(self, file_name, sheet):
        """
            Constructeur de la classe 'Excel' :
                - file_name     : nom du fichier a lire.
                - sheet         : feuille du fichier excel concerne.
        """
        self.file_name = file_name
        self.sheet = sheet

    def lecture(self):
        """
            Lecture des données d'une feuille specifique dans un fichier excel
        """
        workbook_classeur = xlrd.open_workbook(self.file_name + '.xlsx')
        liste_data = []

        sheet_page = workbook_classeur.sheet_by_name(self.sheet)
        for rownum in range(sheet_page.nrows):
            liste_data.append(sheet_page.row_values(rownum))

        return liste_data[1:]

    def convert_date(self, info):
        """
            Conversion d'un float vers le format datetime :
                - info : flottant qui sera transforme en datetime
        """
        return datetime.datetime(*xlrd.xldate_as_tuple(info, 0))
