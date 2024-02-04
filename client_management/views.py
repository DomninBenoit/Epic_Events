class ClientView:
    @staticmethod
    def display_client_menu():
        print("\nGestion des clients")
        print("1. Nouveau client")
        print("2. Mise à jour du client")
        print("3. Suppression client")
        print("q. Quitter")

        choice = input("Entrez votre choix : ")
        return choice

    @staticmethod
    def prompt_for_new_client():
        print("Créer un nouveau client")
        nom_complet = input("Nom complet: ")
        email = input("Email: ")
        telephone = input("Téléphone: ")
        nom_entreprise = input("Nom de l'entreprise: ")

        return {
            "nom_complet": nom_complet,
            "email": email,
            "telephone": telephone,
            "nom_entreprise": nom_entreprise
        }

    @staticmethod
    def list_clients(clients):
        for client in clients:
            # Afficher les informations de chaque client
            print(f"ID: {client.id}",
                  f"Nom: {client.nom_complet}",
                  f"Email: {client.email}",
                  f"Telephone: {client.telephone}",
                  f"Nom d'entreprise: {client.nom_entreprise}"),

    @staticmethod
    def prompt_for_client_id():
        print("\nEntrer l'ID du collaborateur :")
        client_id = input("ID: ")
        return client_id

    @staticmethod
    def prompt_for_updates():
        updates = {}
        print("Laisser vide si pas de changement.")

        nom_complet = input("Nouveau nom: ")
        if nom_complet:
            updates['nom_complet'] = nom_complet

        email = input("Nouvel email: ")
        if email:
            updates['email'] = email

        telephone = input("Nouveau téléphone: ")
        if telephone:
            updates['telephone'] = telephone

        nom_entreprise = input("nouveau nom d'entreprise: ")
        if nom_entreprise:
            updates['nom_entreprise'] = nom_entreprise

        return updates

    @staticmethod
    def confirm_delete(nom_complet, client_id):
        confirm = input(
            f"Êtes-vous sûr de vouloir supprimer le client {nom_complet} (ID: {client_id}) ? (oui/non): ")
        return confirm.lower() == 'oui'
