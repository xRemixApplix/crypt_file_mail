"""
    Fichier regroupant les fonctions gérant le fichier .csv de code aléatoire d'identification.
"""

# IMPORT
import random
import module.csv as csv


# CONSTANTES
NBRE_LIGNES = 1000
LISTE_CARAC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


#FONCTIONS
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

    csv.ecriture("module/ef_codes_NomSite", list_codes)

# AUTO-LANCEMENT
if __name__ == '__main__':
    import csv
    creation()
