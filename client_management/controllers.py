import datetime
from common.base import Session
from client_management.model import Client
from client_management.views import ClientView


class ClientController:
    @classmethod
    def display_client_menu(cls, session, input=None):
        db_session = Session()
        clients = db_session.query(Client).all()
        ClientView.list_clients(clients)

        choice = ClientView.display_client_menu()

        if choice == '1' and session['user'].role_id == 2:
            # creation de client
            return "create_client", None
        elif choice in ['2', '3'] and session['user'].role_id == 2:
            client_id = ClientView.prompt_for_client_id()
            if choice == '2':
                # Mise à jour de client
                return "update_client", client_id
            elif choice == '3':
                # Suppression de client
                return "delete_client", client_id
        elif choice.lower() == 'a':
            return "main_menu", None
        elif choice.lower() == 'q':
            # Quitter l'application
            return "quit", None
        else:
            if choice != 'q' or choice != 'a':
                print("Accès non autorisé.")
            else:
                print("Choix invalide, veuillez réessayer.")
            return "client_management", None

    @classmethod
    def create_client(cls, session, input=None):

        client_data = ClientView.prompt_for_new_client()

        db_session = Session()
        contact_commercial = session.get("user")

        # Création d'une nouvelle instance de Client
        new_client = Client(
            contact_commercial_id=contact_commercial.id,
            nom_complet=client_data["nom_complet"],
            email=client_data["email"],
            telephone=client_data["telephone"],
            nom_entreprise=client_data["nom_entreprise"],
            # Assurez-vous de gérer correctement les champs date_creation et derniere_update
            date_creation=datetime.date.today(),  # Utilisez datetime.date.today() pour la date de création
            derniere_update=datetime.datetime.now()
            # Utilisez datetime.datetime.now() pour la date de dernière mise à jour
        )

        db_session.add(new_client)
        db_session.commit()
        print("Client créé avec succès.")

        db_session.close()
        return "client_management", None

    @classmethod
    def update_client(cls, session, client_id):
        db_session = Session()

        # Rechercher le client par son ID
        client = db_session.query(Client).filter_by(id=client_id).first()
        if not client:
            print(f"Aucun client trouvé avec l'ID {client_id}")
            return "client_management", None

        if client.contact_commercial_id == session['user'].id:
            # Demander à l'utilisateur les champs à mettre à jour
            updates = ClientView.prompt_for_updates()

            # Mise à jour des champs spécifiés
            if 'nom_complet' in updates:
                client.nom_complet = updates['nom_complet']
            if 'email' in updates:
                client.email = updates['email']
            if 'telephone' in updates:
                client.telephone = updates['telephone']
            if 'nom_entreprise' in updates:
                client.nom_entreprise = updates['nom_entreprise']

            # Enregistrer les modifications
            db_session.commit()
            print("Client mis à jour avec succès.")
        else:
            print('Impossible de modifier un client qui ne vous est pas associé !')

        return "client_management", None

    @classmethod
    def delete_client(cls, session, client_id):
        db_session = Session()

        # Rechercher le client par son ID
        client = db_session.query(Client).filter_by(id=client_id).first()
        if not client:
            print(f"Aucun client trouvé avec l'ID {client_id}")
            return "client_management", None
        if client.contact_commercial_id == session['user'].id:
            if ClientView.confirm_delete(client.nom_complet, client_id):
                # Supprimer le client
                db_session.delete(client)
                # Valider les modifications
                db_session.commit()
                print("Client supprimé avec succès.")
            else:
                print("Suppression annulée.")
        else:
            print('Impossible de supprimer un client qui ne vous est pas associé !')

        db_session.close()
        return "client_management", None
