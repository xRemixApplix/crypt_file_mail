"""
    Fichier regroupant les fonctions gérant le fichier .csv de code aléatoire d'identification.
"""

# IMPORT
import random

# CONSTANTES
NBRE_LIGNES = 1000
LISTE_CARAC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def creation():
    """
        Creation du fichier .csv contenant les milles identifiant permettant de reconnaitre
        les fichiers transmis par mail.
    """
    list_codes = []
    while len(list_codes) < NBRE_LIGNES:
        temp = ""
        while len(temp) < 4:
            temp += LISTE_CARAC[random.randint(0, len(LISTE_CARAC)-1)]

        if temp not in list_codes:
            list_codes.append(temp)

    ecriture(list_codes)


def ecriture(list_codes):
    """
        Ecriture de la liste de code dans le fichier .csv
    """
    with open("ef_codes_NomSite.csv", 'w') as file_csv:
        for code in list_codes:
            file_csv.write(code)
            file_csv.write('\n')


# Auto-lancement
if __name__ == '__main__':
    creation()
