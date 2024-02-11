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
    def display_event_filter_menu(cls, session, input=None):
        choice = EventsView.display_event_filter_menu()

        if choice == '1':
            # Vue filtrée des contrats avec reste à payer
            response = cls.display_filtered_events(session, "open_contract")
            print("reste a payer")
            return response[0], response[1]
        elif choice == '2':
            # Vue filtrée des contrats non signés
            response = cls.display_filtered_events(session, "pending_contract")
            print("non signé")
            return response[0], response[1]
        elif choice.lower() == 'q':
            # Quitter l'application
            return "quit", None
        else:
            print("Choix invalide, veuillez réessayer.")
            return "event_management", None

    @classmethod
    def display_filtered_events(cls, session, filter_type=None):
        db_session = Session()

        if filter_type == "open_contract":
            events = db_session.query(Evenement).filter(Contrat.montant_restant > 0).all()
        elif filter_type == "pending_contract":
            events = db_session.query(Evenement).filter(Contrat.statut == "non signé").all()
        else:
            events = db_session.query(Evenement).all()

        EventsView.list_events(events)
        db_session.close()
        return "display_event_filter_menu", None

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
    def update_event(cls, session, event_id):
        db_session = Session()

        # Rechercher l'evenement par son ID
        event = db_session.query(Evenement).filter_by(id=event_id).first()
        if not event:
            print(f"Aucun evenement trouvé avec l'ID {event_id}")
            return "contract_management", None

        # Demander à l'utilisateur les champs à mettre à jour
        updates = EventsView.prompt_for_updates()

        # Mise à jour des champs spécifiés
        if 'date_debut' in updates:
            event.date_debut = updates['date_debut']
        if 'date_fin' in updates:
            event.date_fin = updates['date_fin']
        if 'lieu' in updates:
            event.lieu = updates['lieu']
        if 'nombre_participants' in updates:
            event.nombre_participants = updates['nombre_participants']
        if 'notes' in updates:
            event.notes = updates['notes']

        # Enregistrer les modifications
        db_session.commit()
        print("Evenement mis à jour avec succès.")

        return "event_management", None

    @classmethod
    def delete_event(cls, session, event_id):
        db_session = Session()

        # Rechercher l'event par son ID
        event = db_session.query(Evenement).filter_by(id=event_id).first()
        if not event:
            print(f"Aucun contrat trouvé avec l'ID {event_id}")
            return "client_management", None
        if EventsView.confirm_delete(event, event_id):
            # Supprimer l'event
            db_session.delete(event)
            # Valider les modifications
            db_session.commit()
            print("Event supprimé avec succès.")
        else:
            print("Suppression annulée.")

        db_session.close()
        return "event_management", None
