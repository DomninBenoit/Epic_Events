from datetime import datetime
from unittest.mock import patch, call, MagicMock

from events_management.views import EventsView


def test_display_event_menu():
    with patch('builtins.input', return_value='1') as mock_input, \
            patch('builtins.print') as mock_print:
        choice = EventsView.display_event_menu()

        assert choice == '1'
        mock_input.assert_called_once_with("Entrez votre choix : ")
        expected_calls = [
            call("\nGestion des evenements"),
            call("1. Nouvel evenement"),
            call("2. Menu des evenement filtrés"),
            call("3. Mise à jour de l'evenement"),
            call("4. Suppression evenement"),
            call("a. Menu principal"),
            call("q. Quitter"),
        ]
        mock_print.assert_has_calls(expected_calls, any_order=False)


def test_display_event_filter_menu():
    with patch('builtins.input', return_value='1') as mock_input, \
            patch('builtins.print') as mock_print:
        choice = EventsView.display_event_filter_menu()

        assert choice == '1'
        mock_input.assert_called_once_with("Entrez votre choix : ")
        expected_calls = [
            call("\nVues filtrées des evenements"),
            call("1. Contrats non soldés"),
            call("2. Contrats non signés"),
            call("a. Menu principal"),
            call("q. Quitter"),
        ]
        mock_print.assert_has_calls(expected_calls, any_order=False)


def test_prompt_for_new_event():
    user_inputs = ['1', '2', '2023-01-01 09:00', '2023-01-01 17:00', 'Paris', '100', 'Notes de l’événement']
    with patch('builtins.input', side_effect=user_inputs):
        event_info = EventsView.prompt_for_new_event()

        assert event_info == {
            "contrat_id": 1,
            "contact_support_id": 2,
            "date_debut": datetime.strptime("2023-01-01 09:00", "%Y-%m-%d %H:%M"),
            "date_fin": datetime.strptime("2023-01-01 17:00", "%Y-%m-%d %H:%M"),
            "lieu": "Paris",
            "nombre_participants": 100,
            "notes": "Notes de l’événement"
        }


def test_list_events():
    events_mock = [
        MagicMock(id=1, contact_support_id=2, date_debut="2022-01-01 09:00", date_fin="2022-01-01 17:00", lieu="Paris", nombre_participants=100, notes="Notes 1"),
        MagicMock(id=2, contact_support_id=3, date_debut="2022-02-01 09:00", date_fin="2022-02-01 17:00", lieu="Lyon", nombre_participants=50, notes="Notes 2")
    ]

    with patch('builtins.print') as mock_print:
        EventsView.list_events(events_mock)

        # Vous pouvez ajouter des appels attendus en fonction de vos données mock
        expected_calls = [
            call(f"ID: 1", "Contact support: 2", "Date de début: 2022-01-01 09:00", "Date de fin: 2022-01-01 17:00", "Lieu: Paris", "Nombre de participant: 100", "Notes: Notes 1"),
            call(f"ID: 2", "Contact support: 3", "Date de début: 2022-02-01 09:00", "Date de fin: 2022-02-01 17:00", "Lieu: Lyon", "Nombre de participant: 50", "Notes: Notes 2")
        ]
        mock_print.assert_has_calls(expected_calls, any_order=True)


def test_prompt_for_event_id():
    with patch('builtins.input', return_value="123") as mock_input:
        event_id = EventsView.prompt_for_event_id()

        assert event_id == "123"
        mock_input.assert_called_once_with("ID: ")


def test_prompt_for_updates():
    user_inputs = ['2023-01-01 10:00', '2023-01-01 18:00', 'New York', '200', 'Updated notes']
    with patch('builtins.input', side_effect=user_inputs):
        updates = EventsView.prompt_for_updates()

        assert updates == {
            'date_debut': '2023-01-01 10:00',
            'date_fin': '2023-01-01 18:00',
            'lieu': 'New York',
            'nombre_participants': '200',
            'notes': 'Updated notes'
        }


def test_prompt_for_support_updates():
    with patch('builtins.input', return_value="2") as mock_input:
        update = EventsView.prompt_for_support_updates()

        assert update == {'contact_support_id': '2'}
        mock_input.assert_called_once_with("Nouveau contact support: ")


def test_confirm_delete():
    with patch('builtins.input', return_value="oui") as mock_input:
        confirmation = EventsView.confirm_delete("Event Test", "123")

        assert confirmation == True
        mock_input.assert_called_once_with("Êtes-vous sûr de vouloir supprimer l'evenement' Event Test (ID: 123) ? (oui/non): ")
