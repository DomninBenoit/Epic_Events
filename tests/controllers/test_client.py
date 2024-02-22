import pytest
from unittest.mock import patch, MagicMock
from client_management.controllers import ClientController


# Exemple de test pour display_client_menu
@pytest.mark.parametrize("choice,role_id,expected", [
    ('1', 2, ("create_client", None)),
    ('2', 2, ("update_client", "some_id")),
    ('3', 2, ("delete_client", "some_id")),
    ('a', 2, ("main_menu", None)),
    ('q', 2, ("quit", None)),
    ('invalid', 2, ("client_management", None)),
])
def test_display_client_menu(choice, role_id, expected):
    with patch('client_management.controllers.Session', MagicMock()), \
         patch('client_management.controllers.ClientView.display_client_menu', return_value=choice), \
         patch('client_management.controllers.ClientView.prompt_for_client_id', return_value="some_id"), \
         patch('client_management.controllers.ClientView.list_clients'):
        user_session = {'user': MagicMock(role_id=role_id)}
        result = ClientController.display_client_menu(user_session)
        assert result == expected


def test_create_client():
    client_data = {"nom_complet": "John Doe", "email": "john@example.com", "telephone": "1234567890",
                   "nom_entreprise": "Example Corp"}
    with patch('client_management.controllers.Session') as mock_session, \
            patch('client_management.controllers.ClientView.prompt_for_new_client', return_value=client_data):
        # Simuler un utilisateur connecté
        user_session = {'user': MagicMock(id=1)}

        # Créer une instance mock pour la session
        mock_session_instance = mock_session.return_value

        result = ClientController.create_client(user_session)

        assert result == ("client_management", None)
        mock_session_instance.add.assert_called()
        mock_session_instance.commit.assert_called()


def test_update_client_successful():
    # Simuler un client existant
    mock_client = MagicMock()
    mock_client.contact_commercial_id = 1
    updates = {"nom_complet": "Jane Doe", "email": "jane@example.com", "telephone": "0987654321",
               "nom_entreprise": "Doe Inc."}

    with patch('client_management.controllers.Session') as mock_session, \
            patch('client_management.controllers.ClientView.prompt_for_updates', return_value=updates):
        # Créer une instance mock pour la session
        mock_session_instance = mock_session.return_value
        mock_session_instance.query.return_value.filter_by.return_value.first.return_value = mock_client

        # Simuler un utilisateur connecté avec l'ID correspondant
        user_session = {'user': MagicMock(id=1)}

        result = ClientController.update_client(user_session, client_id="some_id")

        assert result == ("client_management", None)
        assert mock_client.nom_complet == "Jane Doe"
        mock_session_instance.commit.assert_called_once()


def test_update_client_unauthorized():
    # Simuler un client existant avec un contact commercial différent
    mock_client = MagicMock()
    mock_client.contact_commercial_id = 2

    with patch('client_management.controllers.Session') as mock_session:
        # Créer une instance mock pour la session
        mock_session_instance = mock_session.return_value
        mock_session_instance.query.return_value.filter_by.return_value.first.return_value = mock_client

        # Simuler un utilisateur connecté sans correspondance
        user_session = {'user': MagicMock(id=1)}

        result = ClientController.update_client(user_session, client_id="some_id")

        assert result == ("client_management", None)
        mock_session_instance.commit.assert_not_called()


def test_delete_client_successful():
    mock_client = MagicMock()
    mock_client.contact_commercial_id = 1

    with patch('client_management.controllers.Session') as mock_session, \
            patch('client_management.controllers.ClientView.confirm_delete', return_value=True):
        # Créer une instance mock pour la session
        mock_session_instance = mock_session.return_value
        mock_session_instance.query.return_value.filter_by.return_value.first.return_value = mock_client

        # Simuler un utilisateur connecté autorisé
        user_session = {'user': MagicMock(id=1)}

        result = ClientController.delete_client(user_session, client_id="some_id")

        assert result == ("client_management", None)
        mock_session_instance.delete.assert_called_once_with(mock_client)
        mock_session_instance.commit.assert_called_once()


def test_delete_client_cancelled():
    mock_client = MagicMock()
    mock_client.contact_commercial_id = 1

    with patch('client_management.controllers.Session') as mock_session, \
            patch('client_management.controllers.ClientView.confirm_delete', return_value=False):
        mock_session_instance = mock_session.return_value
        mock_session_instance.query.return_value.filter_by.return_value.first.return_value = mock_client

        user_session = {'user': MagicMock(id=1)}

        result = ClientController.delete_client(user_session, client_id="some_id")

        assert result == ("client_management", None)
        mock_session_instance.delete.assert_not_called()
        mock_session_instance.commit.assert_not_called()
