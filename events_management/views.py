from datetime import datetime


class EventsView:
    @staticmethod
    def display_event_menu():
        print("\nGestion des evenements")
        print("1. Nouvel evenement")
        print("2. Menu des evenement filtrés")
        print("3. Mise à jour de l'evenement")
        print("4. Suppression evenement")
        print("a. Menu principal")
        print("q. Quitter")

        choice = input("Entrez votre choix : ")
        return choice

    @staticmethod
    def display_event_filter_menu():
        print("\nVues filtrées des evenements")
        print("1. Contrats non soldés")
        print("2. Contrats non signés")
        print("a. Menu principal")
        print("q. Quitter")

        choice = input("Entrez votre choix : ")
        return choice

    @staticmethod
    def prompt_for_new_event():
        print("Créer un nouvel événement")
        contrat_id = input("ID du contrat associé: ")
        contact_support_id = input("ID du contact support: ")
        date_debut = input("Date de début (YYYY-MM-DD HH:MM): ")
        date_fin = input("Date de fin (YYYY-MM-DD HH:MM): ")
        lieu = input("Lieu: ")
        nombre_participants = input("Nombre de participants: ")
        notes = input("Notes (facultatif): ")

        # Conversion des dates
        date_debut = datetime.strptime(date_debut, "%Y-%m-%d %H:%M")
        date_fin = datetime.strptime(date_fin, "%Y-%m-%d %H:%M")

        return {
            "contrat_id": int(contrat_id),
            "contact_support_id": int(contact_support_id),
            "date_debut": date_debut,
            "date_fin": date_fin,
            "lieu": lieu,
            "nombre_participants": int(nombre_participants),
            "notes": notes
        }

    @staticmethod
    def list_events(events):
        for event in events:
            # Afficher les informations de chaque client
            print(f"ID: {event.id}",
                  f"Contact support: {event.contact_support_id}",
                  f"Date de début: {event.date_debut}",
                  f"Date de fin: {event.date_fin}",
                  f"Lieu: {event.lieu}",
                  f"Nombre de participant: {event.nombre_participants}",
                  f"Notes: {event.notes}"),

    @staticmethod
    def prompt_for_event_id():
        print("\nEntrer l'ID de l'evenement :")
        event_id = input("ID: ")
        return event_id

    @staticmethod
    def prompt_for_updates():
        updates = {}
        print("Laisser vide si pas de changement.")

        date_debut = input("Nouvelle date de début: ")
        if date_debut:
            updates['date_debut'] = date_debut

        date_fin = input("Nouvelle date de fin: ")
        if date_fin:
            updates['date_fin'] = date_fin

        lieu = input("Nouveau lieu: ")
        if lieu:
            updates['lieu'] = lieu

        nombre_participants = input("Nouveau nombre de participant: ")
        if nombre_participants:
            updates['nombre_participants'] = nombre_participants

        notes = input("Nouvelles notes: ")
        if notes:
            updates['notes'] = notes

        return updates

    @staticmethod
    def prompt_for_support_updates():
        update = {}
        print("Laisser vide si pas de changement.")

        contact_support_id = input("Nouveau contact support: ")
        if contact_support_id:
            update['contact_support_id'] = contact_support_id
        return update

    @staticmethod
    def confirm_delete(event, event_id):
        confirm = input(
            f"Êtes-vous sûr de vouloir supprimer l'evenement' {event} (ID: {event_id}) ? (oui/non): ")
        return confirm.lower() == 'oui'
