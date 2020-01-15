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
def creation():
    """
        Creation du fichier .csv contenant les informations des mesures
        à envoyer par mail.
    """
    list_conso = [ENTETE]

    for data in excel.lecture('../test.xlsx', 'DATA'):
        ligne = str(data[2]) + ";" + str(excel.convert_date(data[0])) + ";" + str(data[0]) + ";" + str(data[1]) + ";;"
        list_conso.append(ligne)

    csv.ecriture("test_conso", list_conso)


# AUTO-LANCEMENT
if __name__ == '__main__':
    creation()
