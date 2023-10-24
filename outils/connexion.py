import os
import json
import ftplib

def connexion_ftp(fichier_config):
    # Ouverture du fichier de configuration
    with open(fichier_config, "r") as f:
        data = json.load(f)

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
