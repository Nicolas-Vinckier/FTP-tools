import os
import json
import ftplib
import time


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


def speedtest(ftp):
    # Création d'un fichier de 1 Mo
    with open("10Mo.txt", "wb") as f:
        f.write(b"0" * 10000000)

    # Envoi du fichier sur le serveur FTP
    ftp.storbinary("STOR 10Mo.txt", open("10Mo.txt", "rb"))

    # Suppression du fichier sur le serveur FTP
    ftp.delete("10Mo.txt")

    # Suppression du fichier en local
    os.remove("10Mo.txt")


def menu_connexion(ftp):
    while True:
        print("Menu de Connexion:")
        print("0. Revenir au menu principal")
        print("1. SpeedTest")

        choix = input("Votre choix : ")
        contenu = []

        if choix == "0":
            break
        elif choix == "1":
            start = time.time()
            speedtest(ftp)
            end = time.time()

            # Affichage du temps d'exécution
            print("SpeedTest terminé en", end - start, "secondes.")

            # Calcul du débit
            debit = 10 / (end - start)

            # Affichage du débit
            print("Débit : {:.2f} Mo/s".format(debit))

        else:
            print("Choix invalide, veuillez réessayer.")


def main():
    # Affichage du menu de connexion
    menu_connexion(None)
