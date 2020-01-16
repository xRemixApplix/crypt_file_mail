"""
    Fichier regroupant les fonctions CRUDs des fichiers CSV
"""

#FONCTIONS
def ecriture(file_name, list_codes):
    """
        Ecriture d'une liste dans un fichier .csv
    """
    with open(file_name + ".csv", 'w') as file_csv:
        for code in list_codes:
            file_csv.write(str(code))
            file_csv.write('\n')


def lecture(file_name):
    """
        Lecture d'un fichier .csv retournant une liste
    """
    with open(file_name + ".csv", 'r') as file_csv:
        return file_csv.read().split('\n')
