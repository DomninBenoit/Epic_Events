import datetime
from decimal import Decimal

from authentication.model import Collaborateur
from common.base import Session
from contract_management.model import Contrat
from events_management.model import Evenement
from events_management.views import EventsView
from client_management.model import Client


class EventsController:
    @classmethod
    def display_event_menu(cls, session, input=None):
        db_session = Session()
        events = db_session.query(Evenement).all()
        EventsView.list_events(events)

        choice = EventsView.display_event_menu()

        if choice == '1':
            # creation d'un evenement
            return "create_event", None
        elif choice == '2':
            # sous menu des vues filtrées des evenements
            return "display_event_filter_menu", None
        elif choice in ['3', '4']:
            event_id = EventsView.prompt_for_event_id()
            if choice == '3':
                # Mise à jour de l'evenement
                return "update_event", event_id
            elif choice == '4':
                # Suppression de l'evenement
                return "delete_event", event_id
        elif choice.lower() == 'q':
            # Quitter l'application
            return "quit", None
        else:
            print("Choix invalide, veuillez réessayer.")
            return "event_management", None

    @classmethod
    def display_contract_filter_menu(cls, session, input=None):
        choice = ContractView.display_contract_filter_menu()

        if choice == '1':
            # Vue filtrée des contrats avec reste à payer
            response = cls.display_filtered_contracts(session, "open_contract")
            print("reste a payer")
            return response[0], response[1]
        elif choice == '2':
            # Vue filtrée des contrats non signés
            response = cls.display_filtered_contracts(session, "pending_contract")
            print("non signé")
            return response[0], response[1]
        elif choice.lower() == 'q':
            # Quitter l'application
            return "quit", None
        else:
            print("Choix invalide, veuillez réessayer.")
            return "contract_management", None

    @classmethod
    def display_filtered_contracts(cls, session, filter_type=None):
        db_session = Session()

        if filter_type == "open_contract":
            contracts = db_session.query(Contrat).filter(Contrat.montant_restant > 0).all()
        elif filter_type == "pending_contract":
            contracts = db_session.query(Contrat).filter(Contrat.statut == "non signé").all()
        else:
            contracts = db_session.query(Contrat).all()

        ContractView.list_contracts(contracts)
        db_session.close()
        return "display_contract_filter_menu", None

    @classmethod
    def create_event(cls, session, input=None):
        event_data = EventsView.prompt_for_new_event()

        db_session = Session()

        # Vérifiez que le contrat existe
        contrat = db_session.query(Contrat).filter_by(id=event_data["contrat_id"]).first()
        if not contrat:
            print(f"Aucun contrat trouvé avec l'ID {event_data['contrat_id']}")
            db_session.close()
            return "event_management", None

        # Vérifiez que le collaborateur support existe
        contact_support = db_session.query(Collaborateur).filter_by(id=event_data["contact_support_id"]).first()
        if not contact_support:
            print(f"Aucun collaborateur support trouvé avec l'ID {event_data['contact_support_id']}")
            db_session.close()
            return "event_management", None

        # Création d'une nouvelle instance d'Evenement
        new_event = Evenement(
            contrat_id=event_data["contrat_id"],
            contact_support_id=event_data["contact_support_id"],
            date_debut=event_data["date_debut"],
            date_fin=event_data["date_fin"],
            lieu=event_data["lieu"],
            nombre_participants=event_data["nombre_participants"],
            notes=event_data["notes"]
        )

        db_session.add(new_event)
        db_session.commit()
        print("Événement créé avec succès.")

        db_session.close()
        return "event_management", None

    @classmethod
    def update_contract(cls, session, contrat_id):
        db_session = Session()

        # Rechercher le contrat par son ID
        contrat = db_session.query(Contrat).filter_by(id=contrat_id).first()
        if not contrat:
            print(f"Aucun client trouvé avec l'ID {contrat_id}")
            return "contract_management", None

        # Demander à l'utilisateur les champs à mettre à jour
        updates = ContractView.prompt_for_updates()

        # Mise à jour des champs spécifiés
        if 'montant_total' in updates:
            contrat.montant_total = updates['montant_total']
        if 'montant_restant' in updates:
            contrat.montant_restant = updates['montant_restant']
        if 'statut' in updates:
            contrat.statut = updates['statut']

        # Enregistrer les modifications
        db_session.commit()
        print("Contrat mis à jour avec succès.")

        return "contract_management", None

    @classmethod
    def delete_contract(cls, session, contrat_id):
        db_session = Session()

        # Rechercher le client par son ID
        contrat = db_session.query(Contrat).filter_by(id=contrat_id).first()
        if not contrat:
            print(f"Aucun contrat trouvé avec l'ID {contrat_id}")
            return "client_management", None
        if ContractView.confirm_delete(contrat, contrat_id):
            # Supprimer le client
            db_session.delete(contrat)
            # Valider les modifications
            db_session.commit()
            print("Contrat supprimé avec succès.")
        else:
            print("Suppression annulée.")

        db_session.close()
        return "contract_management", None
