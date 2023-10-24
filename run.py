import os
import json
import ftplib
from outils.create_ftp import new_ftp_server
from outils.connexion import connexion_ftp, select_server


# Fonction d'initialisation
def initialisation():
    # Création du dossier "serveursFTP" si il n'existe pas
    if not os.path.exists("serveursFTP"):
        os.mkdir("serveursFTP")

    # Vérification de l'existence des fichiers de configuration
    for fichier in os.listdir("serveursFTP"):
        # Si le fichier n'existe pas, on le crée
        if not os.path.isfile(os.path.join("serveursFTP", fichier)):
            with open(os.path.join("serveursFTP", fichier), "w") as f:
                f.write("{}")


# Fonction principale
def main():
    # Initialisation du programme
    initialisation()

    # Boucle principale
    while True:
        # Affichage du menu utilisateur
        choix = menu_utilisateur()

        # Traitement du choix de l'utilisateur
        if choix == 1:
            # Connexion au serveur FTP
            ftp = connexion_ftp(select_server())

            # Affichage du répertoire courant
            print(ftp.pwd())

            # Fermeture de la connexion au serveur FTP
            ftp.close()
        elif choix == 2:
            # Ajout d'un nouveau serveur FTP
            new_ftp_server()
        elif choix == 3:
            # Quitter le programme
            break


# Fonction d'affichage du menu utilisateur
def menu_utilisateur():
    # Affichage du menu utilisateur
    print("1. Connexion au serveur FTP")
    print("2. Ajout d'un nouveau serveur FTP")
    print("3. Quitter")

    # Saisie du choix de l'utilisateur
    choix = int(input("Votre choix : "))

    # Retour du choix de l'utilisateur
    return choix


if __name__ == "__main__":
    main()
