from authentication.model import Collaborateur, Role
from common.base import Session
import bcrypt
from authentication.views import LoginView, MainMenuView, CollaborateurView


class AuthenticationController:
    @classmethod
    def login(cls, session, route_params):
        # Afficher la vue de connexion et attendre les entrées de l'utilisateur
        credentials = LoginView.prompt_for_credentials()

        # Créer une session SQLAlchemy pour interroger la base de données
        db_session = Session()

        # Rechercher l'utilisateur par son email (ou nom d'utilisateur)
        user = db_session.query(Collaborateur).filter_by(email=credentials["email"]).first()

        # Si l'utilisateur existe et que le mot de passe correspond
        if user and bcrypt.checkpw(credentials["password"].encode('utf-8'), user.mot_de_passe.encode('utf-8')):
            session["user"] = user
            return "main_menu", None
        else:
            # Si les identifiants sont incorrects, afficher un message d'erreur
            LoginView.display_bad_credentials_message()
            return "login", None

    @classmethod
    def logout(cls, session, route_params):
        # Ici, vous pouvez gérer la déconnexion de l'utilisateur
        session.pop("user", None)
        return "login", None


class MainMenuController:

    @classmethod
    def start_menu(cls, session, input=None):
        choice = MainMenuView.display_start_menu()

        if choice == "1":
            return "create_collaborateur", None
        elif choice == "2":
            return "login", None
        elif choice.lower() == "q":
            return "quit", None
        else:
            print("Choix invalide, veuillez réessayer.")
            return "start_menu", None

    @classmethod
    def display_menu(cls, session, input=None):
        choice = MainMenuView.display()

        if choice == '1':
            # Logique pour la gestion des clients
            return "clients_management", None
        elif choice == '2':
            # Logique pour la gestion des événements
            return "events_management", None
        elif choice == '3':
            # Logique pour afficher les rapports
            return "collaborateur_management", None
        elif choice.lower() == 'q':
            # Quitter l'application
            return "quit", None
        else:
            print("Choix invalide, veuillez réessayer.")
            return "main_menu", None


class CollaborateurController:

    @classmethod
    def create_collaborateur(cls, session, input=None):
        collaborateur_data = CollaborateurView.prompt_for_new_collaborateur()

        db_session = Session()

        role = db_session.query(Role).filter_by(nom=collaborateur_data["role"]).first()
        print(role)
        if role is None:
            print(f"Rôle '{collaborateur_data['role']}' non trouvé.")
            db_session.close()
            return "start_menu", None

        new_collaborateur = Collaborateur(
            nom_utilisateur=collaborateur_data["nom_utilisateur"],
            email=collaborateur_data["email"],
            role_id=role.id
        )

        new_collaborateur.set_mot_de_passe(collaborateur_data["mot_de_passe"])

        db_session.add(new_collaborateur)
        db_session.commit()

        return "main_menu", None