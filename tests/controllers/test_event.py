from datetime import datetime

import pytest
from unittest.mock import patch, MagicMock
from events_management.controllers import EventsController  # Assurez-vous que le chemin d'importation est correct
from events_management.model import Evenement


@pytest.mark.parametrize("choice,user_id,expected", [
    ('1', 2, ("create_event", None)),  # Supposons que seul l'utilisateur avec role_id 2 peut créer un événement
    ('2', 2, ("display_filtered_events", None)),  # Tout utilisateur peut afficher des événements filtrés
    ('3', 3, ("update_event", "some_id")),  # Seul l'utilisateur avec role_id 3 peut mettre à jour un événement
    ('3', 1, ("update_support_event", "some_id")),  # Option spéciale pour role_id 1 pour la mise à jour d'un événement de support
    ('4', 1, ("delete_event", "some_id")),  # Seul l'utilisateur avec role_id 1 peut supprimer un événement
    ('a', 1, ("main_menu", None)),  # Tous les utilisateurs peuvent retourner au menu principal
    ('q', 1, ("quit", None)),  # Tous les utilisateurs peuvent quitter
    ('invalid', 1, ("event_management", None)),  # Test pour un choix invalide
    ('1', 1, ("event_management", None)),  # Test d'accès non autorisé pour création d'événement par un rôle non autorisé
])
def test_display_event_menu(choice, user_id, expected):
    with patch('events_management.controllers.Session', MagicMock()), \
         patch('events_management.controllers.EventsView.display_event_menu', return_value=choice), \
         patch('events_management.controllers.EventsView.prompt_for_event_id', return_value="some_id"), \
         patch('events_management.controllers.EventsView.list_events'):
        user_session = {'user': MagicMock(role_id=user_id)}
        result = EventsController.display_event_menu(user_session)
        assert result == expected


@pytest.mark.parametrize("user_role_id, user_id, expected", [
    (3, 1, ("event_management", None)),  # Utilisateur avec role_id 3 (support), filtrant par son ID
    (1, 2, ("event_management", None)),
    # Utilisateur avec role_id 1 (admin), filtrant les événements sans contact support
])
def test_display_filtered_events(user_role_id, user_id, expected):
    with patch('events_management.controllers.Session', MagicMock()) as mock_session, \
            patch('events_management.controllers.EventsView.list_events') as mock_list_events, \
            patch('builtins.input', return_value=""):
        # Créer une session utilisateur simulée
        user_session = {'user': MagicMock(id=user_id, role_id=user_role_id)}

        # Simuler les événements retournés par la requête
        mock_events = [MagicMock(), MagicMock()]
        mock_session.return_value.query.return_value.filter.return_value.all.return_value = mock_events

        # Exécuter la méthode testée
        result = EventsController.display_filtered_events(user_session)

        # Vérification que le résultat attendu est retourné
        assert result == expected, "Le résultat attendu n'est pas retourné par display_filtered_events"

        # Vérifier que list_events est appelé avec les événements retournés par la requête
        mock_list_events.assert_called_once_with(mock_events)


@pytest.mark.parametrize("contrat_exists, is_contrat_associated, support_exists, expected_return1, expected_return2", [
    (True, True, True, "event_management", None),  # Cas où tout est valide
    (False, True, True, "event_management", None),  # Cas où le contrat n'existe pas
    (True, False, True, "event_management", None),  # Cas où le contrat n'est pas associé au collaborateur connecté
    (True, True, False, "event_management", None),  # Cas où le collaborateur support n'existe pas
])
def test_create_event(contrat_exists, is_contrat_associated, support_exists, expected_return1, expected_return2):
    with patch('common.base.Session', MagicMock()) as mock_session, \
            patch('events_management.controllers.EventsView.prompt_for_new_event', return_value={
                "contrat_id": "1",
                "contact_support_id": "1",
                "date_debut": "2022-01-01",
                "date_fin": "2022-01-02",
                "lieu": "Paris",
                "nombre_participants": 100,
                "notes": "Notes de l'événement"
            }):
        mock_session_instance = mock_session.return_value
        mock_session_instance.add = MagicMock()  # S'assurer que add est un mock

        mock_contrat = MagicMock(contact_commercial_id=1 if is_contrat_associated else 2)
        mock_support = MagicMock() if support_exists else None
        mock_session_instance.query.return_value.filter_by.side_effect = [mock_contrat, mock_support]

        user_session = {'user': MagicMock(id=1)}

        result = EventsController.create_event(user_session)

        assert result == (expected_return1, expected_return2), "Le résultat attendu n'est pas retourné par create_event"


@pytest.mark.parametrize("event_exists, updates, expected_return", [
    (True, {"date_debut": "2023-01-01 10:00", "date_fin": "2023-01-02 18:00", "lieu": "Nouveau lieu",
            "nombre_participants": 150, "notes": "Mise à jour des notes"}, ("event_management", None)),
])
def test_update_event(event_exists, updates, expected_return):
    event_id = "some_id"
    user_id = 1

    with patch('events_management.controllers.Session', MagicMock()) as mock_session, \
            patch('events_management.controllers.EventsView.prompt_for_updates', return_value=updates):
        mock_event = MagicMock(contact_support_id=user_id) if event_exists else None
        mock_session.return_value.query.return_value.filter_by.return_value.first.return_value = mock_event

        user_session = {'user': MagicMock(id=user_id)}

        result = EventsController.update_event(user_session, event_id)

        assert result == expected_return

        if event_exists:
            mock_session.return_value.commit.assert_called_once()

