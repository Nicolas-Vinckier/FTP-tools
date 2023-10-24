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


def recherche_recursive(ftp, path):
    def lister_contenu(path):
        contenu = ftp.nlst(path)
        list_dir = []
        list_file = []
        for element in contenu:
            if ftp.nlst(element) == []:
                list_file.append(element)
            else:
                list_dir.append(element)
        return list_dir, list_file

    def parcourir_dossiers(path):
        list_dir, list_file = lister_contenu(path)
        for dossier in list_dir:
            parcourir_dossiers(dossier)

    list_dir, list_file = lister_contenu(path)

    total_dossiers = len(list_dir)
    total_fichiers = len(list_file)

    return total_dossiers, total_fichiers


def menu_connexion(ftp):
    while True:
        print("Menu de Connexion:")
        print("1. Nombre de dossier/fichier")
        print("2. Revenir au menu principal")

        choix = input("Votre choix : ")

        if choix == "1":
            try:
                print("Recherche en cours...")
                total_dossiers, total_fichiers = recherche_recursive(ftp, ".")
                print(f"Nombre de dossiers : {total_dossiers}")
                print(f"Nombre de fichiers : {total_fichiers}")
            except:
                print("Erreur lors de la récupération du nombre de fichiers.")
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
    menu_connexion
