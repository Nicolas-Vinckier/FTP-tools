import os
import json


def new_ftp_server():
    # Saisie des informations du serveur FTP
    ip = input("IP du serveur FTP : ")
    port = input("Port du serveur FTP : ")
    username = input("Nom d'utilisateur du serveur FTP : ")
    password = input("Mot de passe du serveur FTP : ")

    # Saisie du nom du fichier de configuration
    nom_fichier = input("Nom personalisé du serveur : ")

    # Création du fichier de configuration
    with open(os.path.join("serveursFTP", nom_fichier + ".json"), "w") as f:
        data = {
            "ip": ip,
            "port": port,
            "username": username,
            "password": password,
        }
        json.dump(data, f)
