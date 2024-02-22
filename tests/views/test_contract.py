from unittest.mock import patch, call, MagicMock

from contract_management.views import ContractView


def test_display_contract_menu():
    with patch('builtins.input', return_value='1') as mock_input, \
            patch('builtins.print') as mock_print:
        choice = ContractView.display_contract_menu()

        assert choice == '1'
        mock_input.assert_called_once_with("Entrez votre choix : ")
        expected_calls = [
            call("\nGestion des contrats"),
            call("1. Nouveau contrat"),
            call("2. Menu des contrats filtrés"),
            call("3. Mise à jour du contrat"),
            call("4. Suppression contrat"),
            call("a. Menu principal"),
            call("q. Quitter"),
        ]
        mock_print.assert_has_calls(expected_calls, any_order=False)


def test_display_contract_filter_menu():
    with patch('builtins.input', return_value='1') as mock_input, \
            patch('builtins.print') as mock_print:
        choice = ContractView.display_contract_filter_menu()

        assert choice == '1'
        mock_input.assert_called_once_with("Entrez votre choix : ")
        expected_calls = [
            call("\nVues filtrées des contrats"),
            call("1. Contrats non soldés"),
            call("2. Contrats non signés"),
            call("a. Menu principal"),
            call("q. Quitter"),
        ]
        mock_print.assert_has_calls(expected_calls, any_order=False)


def test_prompt_for_new_contract():
    user_inputs = ['1', '2', '10000', '5000', 'signé']
    with patch('builtins.input', side_effect=user_inputs):
        contract_info = ContractView.prompt_for_new_contract()

        assert contract_info == {
            "client_id": 1,
            "contact_commercial_id": 2,
            "montant_total": 10000.0,
            "montant_restant": 5000.0,
            "statut": 'signé'
        }


def test_list_contracts():
    contracts = [
        MagicMock(id=1, client_id=1, contact_commercial_id=2, montant_total=10000, montant_restant=5000, statut='signé'),
        MagicMock(id=2, client_id=2, contact_commercial_id=3, montant_total=15000, montant_restant=7500, statut='non signé')
    ]

    with patch('builtins.print') as mock_print:
        ContractView.list_contracts(contracts)

        expected_calls = [
            call(f"ID: {contracts[0].id}", f"Client: {contracts[0].client_id}", f"Contact commercial: {contracts[0].contact_commercial_id}", f"Total: {contracts[0].montant_total}", f"Reste à payer: {contracts[0].montant_restant}", f"Statut: {contracts[0].statut}"),
            call(f"ID: {contracts[1].id}", f"Client: {contracts[1].client_id}", f"Contact commercial: {contracts[1].contact_commercial_id}", f"Total: {contracts[1].montant_total}", f"Reste à payer: {contracts[1].montant_restant}", f"Statut: {contracts[1].statut}")
        ]
        mock_print.assert_has_calls(expected_calls, any_order=True)


def test_prompt_for_contract_id():
    with patch('builtins.input', return_value='123'):
        contract_id = ContractView.prompt_for_contract_id()

        assert contract_id == '123'


def test_prompt_for_updates():
    user_inputs = ['20000', '10000', 'signé']
    with patch('builtins.input', side_effect=user_inputs):
        updates = ContractView.prompt_for_updates()

        assert updates == {
            'montant_total': '20000',
            'montant_restant': '10000',
            'statut': 'signé'
        }


def test_confirm_delete():
    with patch('builtins.input', return_value='oui'):
        confirm = ContractView.confirm_delete("Contrat 1", 1)

        assert confirm == True
