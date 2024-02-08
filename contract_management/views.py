class ContractView:
    @staticmethod
    def display_contract_menu():
        print("\nGestion des contrats")
        print("1. Nouveau contrat")
        print("2. Menu des contrats filtrés")
        print("3. Mise à jour du contrat")
        print("4. Suppression contrat")
        print("q. Quitter")

        choice = input("Entrez votre choix : ")
        return choice

    @staticmethod
    def display_contract_filter_menu():
        print("\nVues filtrées des contrats")
        print("1. Contrats non soldés")
        print("2. Contrats non signés")
        print("q. Quitter")

        choice = input("Entrez votre choix : ")
        return choice

    @staticmethod
    def prompt_for_new_contract():
        print("\nCréer un nouveau contrat")

        # Demander l'ID du client pour lequel le contrat est créé
        client_id = input("ID du client: ")

        # Demander l'ID du collaborateur commercial associé au contrat
        contact_commercial_id = input("ID du collaborateur commercial associé: ")

        # Demander les informations spécifiques au contrat
        montant_total = input("Montant total du contrat: ")
        montant_restant = input("Montant restant à payer: ")
        statut = input("Statut du contrat (par exemple, 'signé', 'non signé'): ")

        return {
            "client_id": int(client_id),  # Convertir en entier
            "contact_commercial_id": int(contact_commercial_id),  # Convertir en entier
            "montant_total": float(montant_total),  # Convertir en flottant pour le montant
            "montant_restant": float(montant_restant),  # Idem pour la conversion en flottant
            "statut": statut
        }

    @staticmethod
    def list_contracts(contracts):
        for contract in contracts:
            # Afficher les informations de chaque client
            print(f"ID: {contract.id}",
                  f"Client: {contract.client_id}",
                  f"Contact commercial: {contract.contact_commercial_id}",
                  f"Total: {contract.montant_total}",
                  f"Reste à payer: {contract.montant_restant}",
                  f"Statut: {contract.statut}"),

    @staticmethod
    def prompt_for_contract_id():
        print("\nEntrer l'ID du contrat :")
        contract_id = input("ID: ")
        return contract_id

    @staticmethod
    def prompt_for_updates():
        updates = {}
        print("Laisser vide si pas de changement.")

        montant_total = input("Nouveau Total: ")
        if montant_total:
            updates['montant_total'] = montant_total

        montant_restant = input("Nouveau reste à payer: ")
        if montant_restant:
            updates['montant_restant'] = montant_restant

        statut = input("Nouveau statut: ")
        if statut:
            updates['statut'] = statut

        return updates

    @staticmethod
    def confirm_delete(contrat, contrat_id):
        confirm = input(
            f"Êtes-vous sûr de vouloir supprimer le contrat {contrat} (ID: {contrat_id}) ? (oui/non): ")
        return confirm.lower() == 'oui'
