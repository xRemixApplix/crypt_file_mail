"""
    Interface graphique pour un acces utilisateur au programme
"""

# IMPORT
import tkinter

# SCRIPT
def aide():
    """
        Fenetre "about" du programme
    """
    help_frame = tkinter.Tk()

    help_frame.geometry("350x300+250+250")
    help_frame.title("About")


def list_file():
    """
        Acces à la liste des fichiers excel existant
    """
    print("Liste Fichiers")


def create():
    """
        Creation de la fenetre principale
    """
    main_frame = tkinter.Tk()

    main_frame.geometry("800x600+200+200")
    main_frame.title("Interface Utilisateur")
    main_frame['bg'] = '#D7D7D7'

    # Menu
    menu = tkinter.Menu(main_frame)

    sousmenu = tkinter.Menu(menu, tearoff=0)
    menu.add_cascade(label="Menu", menu=sousmenu)   # "Menu"
    sousmenu.add_command(label="Liste Fichier", command=list_file)
    menu.add_command(label="?", command=aide)       # "?"

    main_frame.config(menu=menu)
    main_frame.mainloop()
