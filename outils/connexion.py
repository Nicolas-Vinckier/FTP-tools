import os
import json
import ftplib
import time
import subprocess


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
    print("===== Liste des serveurs FTP =====")
    for i, fichier in enumerate(fichiers):
        print(f"{i + 1}. {fichier}")

    # Saisie du numéro du serveur FTP à sélectionner
    choix = int(input("Sélectionnez un serveur FTP : "))

    # Retour du fichier de configuration du serveur FTP sélectionné
    return os.path.join("serveursFTP", fichiers[choix - 1])


def speedtest(ftp):
    # Création d'un fichier de 1 Mo
    with open("100Mo.txt", "wb") as f:
        f.write(b"0" * 100000000)

    # Envoi du fichier sur le serveur FTP
    start = time.time()
    ftp.storbinary("STOR 100Mo.txt", open("100Mo.txt", "rb"))
    end = time.time()

    # Suppression du fichier sur le serveur FTP
    ftp.delete("100Mo.txt")

    # Suppression du fichier en local
    os.remove("100Mo.txt")

    # Affichage du temps d'exécution
    print("SpeedTest terminé en", end - start, "secondes.")

    # Calcul du débit
    debit = 100 / (end - start)

    # Affichage du débit
    print("Débit : {:.2f} Mo/s".format(debit))


def ping_test(ftp):
    # Get the server's IP address from the FTP connection
    ip_address = ftp.sock.getpeername()[0]

    # Get the current time before the ping test
    start_time = time.time()

    # Ping the server
    try:
        output = subprocess.check_output(["ping", "-n", "1", "-w", "5000", ip_address])
        print("Ping successful!")
    except subprocess.CalledProcessError:
        print("Ping failed.")

    # Get the current time after the ping test
    end_time = time.time()

    # Calculate the time taken for the ping test
    ping_time = end_time - start_time

    # Round the time to 2 decimal places
    ping_time = round(ping_time, 2)

    print(f"Time taken for ping: {ping_time} seconds")


def menu_connexion(ftp):
    while True:
        print("===== Menu de Connexion: =====")
        print("0. Revenir au menu principal")
        print("1. SpeedTest")
        print("2. Ping Test")

        choix = input("Votre choix : ")
        contenu = []

        if choix == "0":
            break
        elif choix == "1":
            print("===== SpeedTest =====")
            speedtest(ftp)
        elif choix == "2":
            print("===== Ping Test =====")
            ping_test(ftp)

        else:
            print("Choix invalide, veuillez réessayer.")


def main():
    # Affichage du menu de connexion
    menu_connexion(None)
