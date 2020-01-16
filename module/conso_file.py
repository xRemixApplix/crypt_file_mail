"""
    Fichier regroupant les fonctions gérant le fichier .csv
    contenant les informations de consommation.
"""

# IMPORT
import datetime

import csv



# CONSTANTES
ENTETE = "id_cp; bd; p; val; eq_kwh; eq_eu"


# FONCTIONS
def creation(file_name):
    """
        Creation du fichier .csv contenant les informations des mesures
        à envoyer par mail.
    """
    list_conso = [ENTETE]
    date = name = mesure = ""

    for data in excel.lecture(file_name, 'DATA'):
        if name != data[2]:
            date = excel.convert_date(data[0])
            mesure = data[1]
            name = data[2]
        else:
            ligne = str(data[2]) + ";"
            ligne += excel.convert_date(data[0]).strftime("%d/%m/%Y %H:%M") + ";"
            ligne += format_ecart(excel.convert_date(data[0]), date) + ";"
            ligne += str(round(data[1]-mesure, 3))
            ligne += ";;"

            date = excel.convert_date(data[0])
            mesure = data[1]

            list_conso.append(ligne)

    liste_codes = csv.lecture("module/ef_codes_StChristolDAlbion")
    csv.ecriture("module/ef_consommations_StChristolDAlbion_" + str(datetime.date.today()) + "_"
                 + liste_codes[0], list_conso)
    csv.ecriture("module/ef_codes_StChristolDAlbion", liste_codes[1:-1])


def format_ecart(date_d, date_d_1):
    """
        Formate l'ecart de temps entre les deux informations.
    """
    ecart = date_d-date_d_1

    ecart = str(ecart).split(':')

    ecart = str(int(ecart[0])) + " heure(s)" if int(ecart[0]) > 0 else '' \
        + str(int(ecart[1])) + " minute(s)" if int(ecart[1]) > 0 else '' \
        + str(int(ecart[2])) + " seconde(s)" if int(ecart[2]) > 0 else ''

    return ecart


# AUTO-LANCEMENT
if __name__ == '__main__':
    creation('test.xlsx')
