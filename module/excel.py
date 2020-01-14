"""
    Fichier regroupant les fonctions CRUDs des fichiers excel
"""

# IMPORT
import xlrd

# FONCTIONS
def lecture(file_name, sheet):
    """
        Lecture des données d'un fichier .xlsx
    """
    workbook_classeur = xlrd.open_workbook(file_name)
    liste_data = []

    sheet_page = workbook_classeur.sheet_by_name(sheet)
    for rownum in range(sheet_page.nrows):
        liste_data.append(sheet_page.row_values(rownum))

    return liste_data[1:]
