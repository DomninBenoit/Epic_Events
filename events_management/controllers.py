from datetime import datetime
from authentication.model import Collaborateur
from common.base import Session
from contract_management.model import Contrat
from events_management.model import Evenement
from events_management.views import EventsView


class EventsController:
    @classmethod
    def display_event_menu(cls, session, input=None):
        db_session = Session()
        events = db_session.query(Evenement).all()
        EventsView.list_events(events)

        choice = EventsView.display_event_menu()

        if choice == '1' and session['user'].role_id == 2:
            # creation d'un evenement
            return "create_event", None
        elif choice == '2':
            # sous menu des vues filtrées des evenements
            return "display_filtered_events", None
        elif choice in ['3', '4'] and session['user'].role_id in [1, 3]:
            event_id = EventsView.prompt_for_event_id()
            if choice == '3':
                if session['user'].role_id == 3:
                    # Mise à jour de l'evenement
                    return "update_event", event_id
                elif session['user'].role_id == 1:
                    return "update_support_event", event_id
            elif choice == '4':
                # Suppression de l'evenement
                return "delete_event", event_id
        elif choice.lower() == 'a':
            return "main_menu", None
        elif choice.lower() == 'q':
            # Quitter l'application
            return "quit", None
        else:
            if choice in ['1', '3', '4']:
                print("Accès non autorisé.")
            else:
                print("Choix invalide, veuillez réessayer.")
            return "event_management", None

    @classmethod
    def display_filtered_events(cls, session, inputs=None):
        db_session = Session()
        user_id = session['user'].id
        user_role_id = session['user'].role_id

        if user_role_id == 3:
            events = db_session.query(Evenement).filter(Evenement.contact_support_id == user_id).all()
        elif user_role_id == 1:
            events = db_session.query(Evenement).filter(Evenement.contact_support_id == "").all()

        EventsView.list_events(events)
        input("Appuyez sur Entrée pour continuer...")

        return "event_management", None

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

        # Vérifiez que le contrat est associé au collaborateur connecté
        if contrat.contact_commercial_id != session['user'].id:
            print("Ce contrat n'est pas associé à votre compte.")
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
        event = db_session.query(Evenement).filter_by(id=event_id, contact_support_id=session['user'].id).first()
        if not event:
            print(f"Aucun evenement trouvé avec l'ID {event_id} associé à votre compte.")
            return "event_management", None

        # Demander à l'utilisateur les champs à mettre à jour
        updates = EventsView.prompt_for_updates()

        # Mise à jour des champs spécifiés
        if 'date_debut' in updates:
            event.date_debut = datetime.strptime(updates['date_debut'], '%Y-%m-%d %H:%M')
        if 'date_fin' in updates:
            event.date_fin = datetime.strptime(updates['date_fin'], '%Y-%m-%d %H:%M')
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
    def update_support_event(cls, session, event_id):
        db_session = Session()

        # Rechercher l'evenement par son ID
        event = db_session.query(Evenement).filter_by(id=event_id).first()
        if not event:
            print(f"Aucun evenement trouvé avec l'ID {event_id}.")
            return "contract_management", None

        update = EventsView.prompt_for_support_updates()

        if 'contact_support_id' in update:
            event.contact_support_id = update['contact_support_id']

        # Enregistrer les modifications
        db_session.commit()
        print("Contact Support mis à jour avec succès.")

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
