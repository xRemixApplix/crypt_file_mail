"""
    Fichier de la classe Code_file
    Auteur : Remi Invernizzi
    Version : 1.0
    Date : Janvier 2020
"""

# IMPORT
import datetime

from csv import Csv


# CLASSE
class ConsoFile(Csv):
    """
        Classe ConsoFile : classe servant a la gestion de tout ce qui a un rapport
        avec le fichier de csv de consommation
    """

    ENTETE = "id_cp; bd; p; val; eq_kwh; eq_eu"

    def __init__(self, file_name):
        """
            Constructeur de la classe 'CodeFile' :
                - file_name     : nom du fichier de consommation.
        """
        Csv.__init__(self, file_name)

    def creation(self, struct_fold, excel_file):
        """
            Creation du fichier .csv contenant les informations des mesures
            à envoyer par mail.
        """
        list_conso = [self.ENTETE]
        date = name = mesure = ""

        for data in excel_file.lecture(self.file_name, 'DATA'):
            if name != data[2]:
                date = excel_file.convert_date(data[0])
                mesure = data[1]
                name = data[2]
            else:
                ligne = str(data[2]) + ";"
                ligne += excel_file.convert_date(data[0]).strftime("%d/%m/%Y %H:%M") + ";"
                ligne += self.format_ecart(excel_file.convert_date(data[0]), date) + ";"
                ligne += str(round(data[1]-mesure, 3))
                ligne += ";;"

                date = excel_file.convert_date(data[0])
                mesure = data[1]

                list_conso.append(ligne)

        liste_codes = Csv.lecture(struct_fold['dest_csv_conso'] + 'ef_codes_StChristolDAlbion')
        file_conso = struct_fold['dest_csv_conso'] + 'ef_consommations_StChristolDAlbion_' \
            + str(datetime.date.today()) + "_" + liste_codes[0]
        Csv.ecriture(self.file_name, list_conso)
        Csv.ecriture(struct_fold['dest_csv_conso'] + 'ef_codes_StChristolDAlbion', liste_codes[1:-1])

        return file_conso


    def format_ecart(self, date_d, date_d_1):
        """
            Formate l'ecart de temps entre les deux informations de consommation.
        """
        ecart = date_d-date_d_1

        ecart = str(ecart).split(':')

        ecart = str(int(ecart[0])) + " heure(s)" if int(ecart[0]) > 0 else '' \
            + str(int(ecart[1])) + " minute(s)" if int(ecart[1]) > 0 else '' \
            + str(int(ecart[2])) + " seconde(s)" if int(ecart[2]) > 0 else ''

        return ecart
