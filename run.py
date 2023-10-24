import json
import os
import ftplib


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


# Fonction de connexion au serveur FTP
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


# Fonction d'ajout d'un nouveau serveur FTP
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


# Fonction de sélection du serveur FTP
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


if __name__ == "__main__":
    main()
