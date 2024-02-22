from unittest.mock import patch, call, MagicMock

from client_management.views import ClientView


def test_display_client_menu():
    with patch('builtins.input', return_value='1') as mock_input, \
            patch('builtins.print') as mock_print:
        choice = ClientView.display_client_menu()

        assert choice == '1'
        mock_input.assert_called_once_with("Entrez votre choix : ")
        expected_print_calls = [
            call("\nGestion des clients"),
            call("1. Nouveau client"),
            call("2. Mise à jour du client"),
            call("3. Suppression client"),
            call("a. Menu principal"),
            call("q. Quitter"),
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)


def test_prompt_for_new_client():
    user_inputs = ['Alice Dupont', 'alice@example.com', '0123456789', 'Alice Corp']
    with patch('builtins.input', side_effect=user_inputs):
        client_info = ClientView.prompt_for_new_client()

        assert client_info == {
            "nom_complet": 'Alice Dupont',
            "email": 'alice@example.com',
            "telephone": '0123456789',
            "nom_entreprise": 'Alice Corp'
        }


def test_list_clients():
    clients = [
        MagicMock(id=1, nom_complet="Alice Dupont", email="alice@example.com", telephone="0123456789", nom_entreprise="Alice Corp"),
        MagicMock(id=2, nom_complet="Bob Martin", email="bob@example.com", telephone="9876543210", nom_entreprise="Bob Inc")
    ]

    with patch('builtins.print') as mock_print:
        ClientView.list_clients(clients)

        expected_calls = [
            call(f"ID: {clients[0].id}", f"Nom: {clients[0].nom_complet}", f"Email: {clients[0].email}", f"Telephone: {clients[0].telephone}", f"Nom d'entreprise: {clients[0].nom_entreprise}"),
            call(f"ID: {clients[1].id}", f"Nom: {clients[1].nom_complet}", f"Email: {clients[1].email}", f"Telephone: {clients[1].telephone}", f"Nom d'entreprise: {clients[1].nom_entreprise}"),
        ]
        mock_print.assert_has_calls(expected_calls, any_order=True)


def test_prompt_for_client_id():
    with patch('builtins.input', return_value='123'):
        client_id = ClientView.prompt_for_client_id()

        assert client_id == '123'


def test_prompt_for_updates():
    user_inputs = ['Alice Dupont', 'alice.new@example.com', '0987654321', 'New Alice Corp']
    with patch('builtins.input', side_effect=user_inputs):
        updates = ClientView.prompt_for_updates()

        assert updates == {
            'nom_complet': 'Alice Dupont',
            'email': 'alice.new@example.com',
            'telephone': '0987654321',
            'nom_entreprise': 'New Alice Corp'
        }


def test_confirm_delete():
    with patch('builtins.input', return_value='oui'):
        confirm = ClientView.confirm_delete("Alice Dupont", 1)

        assert confirm == True
