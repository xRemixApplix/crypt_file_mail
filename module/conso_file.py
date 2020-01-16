"""
    Fichier regroupant les fonctions gérant le fichier .csv
    contenant les informations de consommation.
"""

# IMPORT
import csv
import excel


# CONSTANTES
ENTETE = "id_cp; bd; p; val; eq_kwh; eq_eu"


# FONCTIONS
def creation(file_name):
    """
        Creation du fichier .csv contenant les informations des mesures
        à envoyer par mail.
    """
    list_conso = [ENTETE]
    date = name = ""

    for data in excel.lecture(file_name, 'DATA'):
        if name != data[2]:
            date = excel.convert_date(data[0])
            name = data[2]
        else:
            ligne = str(data[2]) + ";"
            ligne += str(excel.convert_date(data[0]))+ ";"
            ligne += format_ecart(excel.convert_date(data[0]), date) + ";"
            ligne += str(round(data[1], 2))
            ligne += ";;"

            date = excel.convert_date(data[0])

            list_conso.append(ligne)

    csv.ecriture("module/test_conso", list_conso)


def format_ecart(date_d, date_d_1):
    """
        Formate l'ecart de temps entre les deux informations.
    """
    ecart = date_d-date_d_1

    ecart = str(ecart)

    if ecart == "0:01:00":
        ecart = "1 minute"
    elif ecart == "0:10:00":
        ecart = "10 minutes"
    elif ecart == "1:00:00":
        ecart = "1 heure"

    return ecart


# AUTO-LANCEMENT
if __name__ == '__main__':
    creation('test.xlsx')
