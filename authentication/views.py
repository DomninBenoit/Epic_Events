from authentication.model import Departement


class LoginView:

    @staticmethod
    def prompt_for_credentials():
        # Afficher une invite pour que l'utilisateur saisisse ses identifiants
        print("Veuillez vous connecter.")
        email = input("Email: ")
        password = input("Mot de passe: ")
        return {
            "email": email,
            "password": password
        }

    @staticmethod
    def display_bad_credentials_message():
        # Afficher un message d'erreur si les identifiants sont incorrects
        print("Les identifiants sont incorrects. Veuillez réessayer.")

class MainMenuView:

    @staticmethod
    def display_start_menu():
        print("\n Epic Event")
        print("1. Creation collaborateur")
        print("2. Identification")
        print("q. Quitter")

        choice = input("Entrez votre choix : ")
        return choice

    @staticmethod
    def display():
        print("\nMenu Principal")
        print("1. Gestion des clients")
        print("2. Gestion des événements")
        print("3. Gestion des collaborateurs")
        print("q. Quitter")

        choice = input("Entrez votre choix : ")
        return choice

class CollaborateurView:
    @staticmethod
    def display_collaborateur_menu():
        print("\nGestion des collaborateurs")
        print("1. Voir profil")
        print("q. Quitter")

        choice = input("Entrez votre choix : ")
        return choice

    @staticmethod
    def prompt_for_new_collaborateur():
        print("Créer un nouveau collaborateur")
        nom_utilisateur = input("Nom d'utilisateur: ")
        email = input("Email: ")
        mot_de_passe = input("Mot de passe: ")

        print("Rôles disponibles: ")
        for departement in Departement:
            print(f"{departement.value}")

        role = input("Choisissez un rôle parmi les options ci-dessus: ")

        return {
            "nom_utilisateur": nom_utilisateur,
            "email": email,
            "mot_de_passe": mot_de_passe,
            "role": role
        }

    @staticmethod
    def view_profile(collaborateur):
        if collaborateur:
            # Afficher les informations du collaborateur
            print(f"ID: {collaborateur.id}, Nom: {collaborateur.nom_utilisateur}, Email: {collaborateur.email}")
        else:
            print("Profil non trouvé.")
