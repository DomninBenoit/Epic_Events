from unittest import TestCase

import bcrypt
import pytest
from unittest.mock import patch, MagicMock
from authentication.controllers import AuthenticationController, CollaborateurController, MainMenuController
from authentication.model import Collaborateur, Role
from common.base import Session
from authentication.views import LoginView, MainMenuView


@pytest.fixture
def mock_session(mocker):
    mock = mocker.patch.object(Session, '__call__', return_value=mocker.MagicMock())
    return mock.return_value

def test_login_success(mock_session, mocker):
    hashed_password = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())
    expected_user = MagicMock()
    expected_user.email = "test@example.com"
    expected_user.mot_de_passe = hashed_password
    mock_session.query.return_value.filter_by.return_value.first.return_value = expected_user
    mocker.patch("authentication.views.LoginView.prompt_for_credentials", return_value={"email": "domnin@test.fr", "password": "password123"})
    mocker.patch("bcrypt.checkpw", return_value=True)

    session = {}


def test_logout():
    session = {'user': 'existing_user'}
    response = AuthenticationController.logout(session, {})
    assert 'user' not in session
    assert response == ("login", None)


@patch('common.base.Session')
@patch('authentication.controllers.CollaborateurView')
def test_display_collaborateur_menu(MockCollaborateurView, MockSession):
    # Configuration du mock pour la base de données
    mock_session = MockSession.return_value
    mock_session.query.return_value.all.return_value = [MagicMock(spec=Collaborateur)]

    # Configuration des mocks pour les interactions utilisateur
    MockCollaborateurView.list_collaborateurs.return_value = None
    MockCollaborateurView.display_collaborateur_menu.return_value = 'a'  # Simule le choix de retourner au menu principal

    result = CollaborateurController.display_collaborateur_menu(None)
    assert result == ("main_menu", None)

    # Testez d'autres scénarios en changeant la valeur retournée par display_collaborateur_menu


@patch('common.base.Session')
@patch('authentication.controllers.CollaborateurView')
def test_create_collaborateur(MockCollaborateurView, MockSession):
    mock_session = MockSession.return_value

    MockCollaborateurView.prompt_for_new_collaborateur.return_value = {
        "nom_utilisateur": "testuser",
        "email": "test@example.com",
        "role": "support",
        "mot_de_passe": "securepassword"
    }

    result = CollaborateurController.create_collaborateur(None)
    assert result == ("collaborateur_management", None)


@patch('common.base.Session')
@patch('authentication.views.CollaborateurView.prompt_for_updates')
def test_update_collaborateur(mock_prompt_for_updates, mock_session):
    # Préparer les données pour le test
    mock_collab = MagicMock(spec=Collaborateur)
    mock_collab.nom_utilisateur = "ancien_nom"
    mock_collab.email = "ancien_email@example.com"

    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_collab
    mock_prompt_for_updates.return_value = {
        'nom_utilisateur': 'nouveau_nom',
        'email': 'nouvel_email@example.com',
        'mot_de_passe': 'nouveau_mot_de_passe'
    }

    result = CollaborateurController.update_collaborateur(None, 1)

    assert result == ("collaborateur_management", None)


@patch('common.base.Session')
@patch('authentication.views.CollaborateurView.confirm_delete', return_value=True)
def test_delete_collaborateur_with_confirmation(mock_confirm_delete, mock_session):
    # Préparer les données pour le test
    mock_collab = MagicMock(spec=Collaborateur)
    mock_collab.nom_utilisateur = "nom_utilisateur"

    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_collab

    result = CollaborateurController.delete_collaborateur(None, 5)

    assert result == ("collaborateur_management", None)


@pytest.mark.parametrize("input_value, expected_output", [
    ('1', ("client_management", None)),
    ('2', ("contract_management", None)),
    ('3', ("event_management", None)),
    ('4', ("collaborateur_management", None)),  # Assumons que l'utilisateur a le role_id requis pour cet exemple
    ('q', ("quit", None)),
    ('invalid_choice', ("main_menu", None))  # Cas d'un choix invalide
])
def test_display_menu(input_value, expected_output):
    session_mock = {'user': MagicMock(role_id=1)}  # Assurez-vous que cette mock session correspond aux attentes de votre méthode
    with patch('builtins.input', return_value=input_value):
        result = MainMenuController.display_menu(session_mock)
        assert result == expected_output
