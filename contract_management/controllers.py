import datetime
from decimal import Decimal

from authentication.model import Collaborateur
from common.base import Session
from contract_management.model import Contrat
from contract_management.views import ContractView
from client_management.model import Client


class ContractController:
    @classmethod
    def display_contract_menu(cls, session, input=None):
        db_session = Session()
        contracts = db_session.query(Contrat).all()
        ContractView.list_contracts(contracts)

        choice = ContractView.display_contract_menu()

        if choice == '1':
            # creation de contrat
            return "create_contract", None
        elif choice == '2':
            # sous menu des vues filtrées des contrats
            return "display_contract_filter_menu", None
        elif choice in ['3', '4']:
            contract_id = ContractView.prompt_for_contract_id()
            if choice == '3':
                # Mise à jour du contrat
                return "update_contract", contract_id
            elif choice == '4':
                # Suppression du contrat
                return "delete_contract", contract_id
        elif choice.lower() == 'q':
            # Quitter l'application
            return "quit", None
        else:
            print("Choix invalide, veuillez réessayer.")
            return "contract_management", None

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
    def create_contract(cls, session, input=None):
        contract_data = ContractView.prompt_for_new_contract()

        db_session = Session()
        # Vérifiez que le client existe
        client = db_session.query(Client).filter_by(id=contract_data["client_id"]).first()
        if not client:
            print(f"Aucun client trouvé avec l'ID {contract_data['client_id']}")
            db_session.close()
            return "contract_management", None

        # Vérifiez que le collaborateur commercial existe
        contact_commercial = db_session.query(Collaborateur).filter_by(id=contract_data["contact_commercial_id"]).first()
        if not contact_commercial:
            print(f"Aucun collaborateur commercial trouvé avec l'ID {contract_data['contact_commercial_id']}")
            db_session.close()
            return "contract_management", None

        # Création d'une nouvelle instance de Contrat
        new_contract = Contrat(
            client_id=contract_data["client_id"],
            contact_commercial_id=contact_commercial.id,  # Utiliser l'ID du collaborateur connecté
            montant_total=Decimal(contract_data["montant_total"]),
            montant_restant=Decimal(contract_data["montant_restant"]),
            date_creation=datetime.date.today(),
            statut=contract_data["statut"]
        )

        db_session.add(new_contract)
        db_session.commit()
        print("Contrat créé avec succès.")

        db_session.close()
        return "contract_management", None

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
