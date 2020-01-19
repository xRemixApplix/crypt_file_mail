def create_dest():
    """
        Declaration des destinataires principaux et en copie pour remplissage
        du fichier JSON les listants
    """
    list_dest = []
    list_dest_cc = []

    # Definitions des destinataires
    print("########################################")
    print("# Creation des destinataires de mails. #")
    print("########################################")

    while True:
        try:
            adress, param = input("Adresse Destinaire : ").split(' ')
        except ValueError:
            # Texte en rouge
            print('\x1b[6;31;40m'
                  + "Erreur de syntaxe"
                  + '\x1b[0m')
        else:
            if adress.upper() != "Q":
                if re.match(EMAIL_REGEX, adress) is None:
                    # Texte en orange
                    print('\x1b[6;33;40m'
                          + "Format de l'adresse incorrecte"
                          + '\x1b[0m')
                else:
                    if param.upper() == "D":
                        list_dest.append(adress.lower())
                    elif param.upper() == "C":
                        list_dest_cc.append(adress.lower())
                    else:
                        # Texte en orange
                        print('\x1b[6;33;40m'
                              + "Etat Destinataire non reconnu (D: Principal, C: Copie)"
                              + '\x1b[0m')
            else:
                break

    return list_dest, list_dest_cc

