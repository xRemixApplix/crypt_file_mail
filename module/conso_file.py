"""
    Fichier de la classe Code_file
    Auteur : Remi Invernizzi
    Version : 1.1
    Date : Novembre 2020
"""

# IMPORT
from module.csv import Csv
from module.excel import convert_date


# FONCTION
def format_ecart(date_d, date_d_1):
    """
        Formate l'ecart de temps entre les deux informations de consommation.
    """
    ecart = date_d-date_d_1

    ecart = str(ecart).split(':')

    ecart = str(int(ecart[0])) + " heure" if int(ecart[0]) > 0 else '' \
        + str(int(ecart[1])) + " minutes" if int(ecart[1]) > 0 else '' \
        + str(int(ecart[2])) + " secondes" if int(ecart[2]) > 0 else ''

    return ecart


# CLASSE
class ConsoFile(Csv):
    """
        Classe ConsoFile : classe servant a la gestion de tout ce qui
        a un rapport avec le fichier de csv de consommation
    """

    ENTETE = "id_cp; bd; p; val; eq_kwh; eq_eu"

    def __init__(self, file_name):
        """
            Constructeur de la classe 'CodeFile' :
                - file_name     : nom du fichier de consommation.
        """
        Csv.__init__(self, file_name)

    def creation(self, liste_conso_excel, transfo_nom):
        """
            Creation du fichier .csv contenant les informations des mesures
            à envoyer par mail.
        """
        list_conso = [self.ENTETE]
        date = name = mesure = ""

        for data in liste_conso_excel:
            date_convertie = convert_date(data[0])
            if name != data[2]:
                date = date_convertie
                mesure = data[1]
                name = data[2]
            else:
                ligne = transfo_nom[str(data[2])] + ";"
                ligne += date_convertie.strftime("%d/%m/%Y %H:%M") + ";"
                ligne += format_ecart(date_convertie, date) + ";"
                ligne += str(round(data[1]-mesure, 3))
                ligne += ";;"

                date = date_convertie
                mesure = data[1]

                list_conso.append(ligne)

        return list_conso
