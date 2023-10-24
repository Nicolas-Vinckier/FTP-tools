import os
import json
import ftplib


def connexion_ftp(fichier_config):
    # Chargement du fichier de configuration
    data = json.load(open(fichier_config, "r"))

    # Création d'une instance de la classe FTP
    ftp = ftplib.FTP()

    # Connexion au serveur FTP
    ftp.connect(data["ip"], int(data["port"]))
    ftp.login(data["username"], data["password"])

    # Affichage d'un message indiquant que la connexion a réussi
    print("Connexion réussie !")

    # Retour de l'instance de la classe FTP
    return ftp


def select_server():
    # Liste des fichiers de configuration
    fichiers = os.listdir("serveursFTP")

    # Affichage de la liste des fichiers de configuration
    for i, fichier in enumerate(fichiers):
        print(f"{i + 1}. {fichier}")

    # Saisie du numéro du serveur FTP à sélectionner
    choix = int(input("Sélectionnez un serveur FTP : "))

    # Retour du fichier de configuration du serveur FTP sélectionné
    return os.path.join("serveursFTP", fichiers[choix - 1])


def lister_fichiers_dossiers(ftp, chemin="."):
    contenu = []

    try:
        # Tente de se déplacer vers le répertoire spécifié
        ftp.cwd(chemin)
    except ftplib.error_perm as e:  # Si une erreur de permission se produit
        print(f"Permission refusée pour {chemin}: {str(e)}")
        return (
            contenu  # retourne la liste vide, car vous ne pouvez pas explorer ce chemin
        )

    # Récupérer la liste des fichiers et dossiers dans le répertoire courant du serveur FTP
    elements = ftp.nlst()

    for element in elements:
        # Si c'est un dossier, ajouter le dossier à la liste et parcourir récursivement son contenu
        if "." not in element:
            contenu.append(element)
            contenu.extend(lister_fichiers_dossiers(ftp, element))
        else:
            # Si c'est un fichier, ajouter le fichier à la liste
            contenu.append(element)

    # Retourner au répertoire précédent pour d'autres appels récursifs
    ftp.cwd("..")

    return contenu


def menu_connexion(ftp):
    while True:
        print("Menu de Connexion:")
        print("1. Liste des fichiers et dossiers")
        print("2. Revenir au menu principal")

        choix = input("Votre choix : ")

        if choix == "1":
            try:
                print("Recherche en cours...")
                contenu = lister_fichiers_dossiers(ftp)
                print("Liste des fichiers et dossiers :")
                for element in contenu:
                    print(element)
            except Exception as e:
                print(
                    "Erreur lors de la récupération de la liste des fichiers et dossiers :",
                    str(e),
                )
            print(contenu)
        elif choix == "2":
            break
        else:
            print("Choix invalide, veuillez réessayer.")


def main():
    # Sélection du serveur FTP
    fichier_config = select_server()

    # Connexion au serveur FTP
    ftp = connexion_ftp(fichier_config)

    # Affichage du menu de connexion
    menu_connexion(ftp)
