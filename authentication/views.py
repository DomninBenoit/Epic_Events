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
        print("1. Nouveau collaborateur")
        print("2. Mise à jour du collaborateur")
        print("3. Suppression collaborateur")
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
    def list_collaborateurs(collaborateurs):
        for collaborateur in collaborateurs:
            # Afficher les informations du collaborateur
            print(f"ID: {collaborateur.id}, Nom: {collaborateur.nom_utilisateur}, Email: {collaborateur.email}")

    @staticmethod
    def prompt_for_collaborateur_id():
        print("\nEntrer l'ID du collaborateur :")
        collab_id = input("ID: ")
        return collab_id

    @staticmethod
    def prompt_for_updates():
        updates = {}
        print("Laisser vide si pas de changement.")

        nom_utilisateur = input("Nouveau nom d'utilisateur: ")
        if nom_utilisateur:
            updates['nom_utilisateur'] = nom_utilisateur

        email = input("Nouvel email: ")
        if email:
            updates['email'] = email

        mot_de_passe = input("Nouveau mot de passe: ")
        if mot_de_passe:
            updates['mot_de_passe'] = mot_de_passe

        return updates

    @staticmethod
    def confirm_delete(nom_utilisateur, collab_id):
        confirm = input(
            f"Êtes-vous sûr de vouloir supprimer le collaborateur {nom_utilisateur} (ID: {collab_id}) ? (oui/non): ")
        return confirm.lower() == 'oui'
