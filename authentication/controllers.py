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
    def display_menu(cls, session, input=None):
        choice = MainMenuView.display()

        if choice == '1':
            # Logique pour la gestion des clients
            return "client_management", None
        elif choice == '2':
            # Logique pour la gestion des contrats
            return "contract_management", None
        elif choice == '3':
            # Logique pour la gestion des événements
            return "event_management", None
        elif choice == '4':
            # Logique pour afficher la gestion du collaborateur
            return "collaborateur_management", None
        elif choice.lower() == 'q':
            # Quitter l'application
            return "quit", None
        else:
            print("Choix invalide, veuillez réessayer.")
            return "main_menu", None


class CollaborateurController:
    @classmethod
    def display_collaborateur_menu(cls, session, input=None):
        db_session = Session()
        collaborateurs = db_session.query(Collaborateur).all()
        CollaborateurView.list_collaborateurs(collaborateurs)

        choice = CollaborateurView.display_collaborateur_menu()

        if choice == '1':
            # creation de collaborateur
            return "create_collaborateur", None
        elif choice in ['2', '3']:
            collab_id = CollaborateurView.prompt_for_collaborateur_id()
            if choice == '2':
                # Mise à jour de collaborateur
                return "update_collaborateur", collab_id
            elif choice == '3':
                # Suppression de collaborateur
                return "delete_collaborateur", collab_id
        elif choice.lower() == 'q':
            # Quitter l'application
            return "quit", None
        else:
            print("Choix invalide, veuillez réessayer.")
            return "collaborateur_management", None

    @classmethod
    def create_collaborateur(cls, session, input=None):
        collaborateur_data = CollaborateurView.prompt_for_new_collaborateur()

        db_session = Session()

        role = db_session.query(Role).filter_by(nom=collaborateur_data["role"]).first()

        if role is None:
            print(f"Rôle '{collaborateur_data['role']}' non trouvé.")
            db_session.close()
            return "collaborateur_management", None

        new_collaborateur = Collaborateur(
            nom_utilisateur=collaborateur_data["nom_utilisateur"],
            email=collaborateur_data["email"],
            role_id=role.id
        )

        new_collaborateur.set_mot_de_passe(collaborateur_data["mot_de_passe"])

        db_session.add(new_collaborateur)
        db_session.commit()

        return "collaborateur_management", None

    @classmethod
    def update_collaborateur(cls, session, collab_id):
        db_session = Session()

        # Rechercher le collaborateur par son ID
        collaborateur = db_session.query(Collaborateur).filter_by(id=collab_id).first()
        if not collaborateur:
            print(f"Aucun collaborateur trouvé avec l'ID {collab_id}")
            return "collaborateur_management", None

        # Demander à l'utilisateur les champs à mettre à jour
        updates = CollaborateurView.prompt_for_updates()

        # Mise à jour des champs spécifiés
        if 'nom_utilisateur' in updates:
            collaborateur.nom_utilisateur = updates['nom_utilisateur']
        if 'email' in updates:
            collaborateur.email = updates['email']
        if 'mot_de_passe' in updates:
            collaborateur.set_mot_de_passe(updates['mot_de_passe'])

        # Enregistrer les modifications
        db_session.commit()
        print("Collaborateur mis à jour avec succès.")

        return "collaborateur_management", None

    @classmethod
    def delete_collaborateur(cls, session, collab_id):
        db_session = Session()

        # Rechercher le collaborateur par son ID
        collaborateur = db_session.query(Collaborateur).filter_by(id=collab_id).first()
        if not collaborateur:
            print(f"Aucun collaborateur trouvé avec l'ID {collab_id}")
            return "collaborateur_management", None
        if CollaborateurView.confirm_delete(collaborateur.nom_utilisateur, collab_id):
            # Supprimer le collaborateur
            db_session.delete(collaborateur)
            # Valider les modifications
            db_session.commit()
            print("Collaborateur supprimé avec succès.")
        else:
            print("Suppression annulée.")

        db_session.close()
        return "collaborateur_management", None