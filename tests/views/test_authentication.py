from unittest.mock import patch, call, MagicMock

from authentication.model import Departement
from authentication.views import LoginView, MainMenuView, CollaborateurView


def test_prompt_for_credentials():
    with patch('builtins.input', side_effect=['user@example.com', 'password123']), \
         patch('builtins.print') as mock_print:
        credentials = LoginView.prompt_for_credentials()

        assert credentials == {"email": "user@example.com", "password": "password123"}
        mock_print.assert_called_with("Veuillez vous connecter.")


def test_display_bad_credentials_message():
    with patch('builtins.print') as mock_print:
        LoginView.display_bad_credentials_message()

        mock_print.assert_called_with("Les identifiants sont incorrects. Veuillez réessayer.")


def test_main_menu_view_display():
    with patch('builtins.input', return_value='1') as mock_input, \
            patch('builtins.print') as mock_print:
        choice = MainMenuView.display()

        # Vérifie que le bon choix est retourné basé sur l'entrée simulée
        assert choice == '1'

        # Vérifie que la fonction input a été appelée correctement
        mock_input.assert_called_once_with("Entrez votre choix : ")

        # Prépare une liste des appels attendus à `print`
        expected_print_calls = [
            call("\nMenu Principal"),
            call("1. Gestion des clients"),
            call("2. Gestion des contrats"),
            call("3. Gestion des événements"),
            call("4. Gestion des collaborateurs"),
            call("q. Quitter"),
        ]

        # Vérifier que chaque ligne attendue du menu a été imprimée
        mock_print.assert_has_calls(expected_print_calls, any_order=True)


def test_display_collaborateur_menu():
    expected_user_input = '2'
    with patch('builtins.input', return_value=expected_user_input) as mock_input, \
            patch('builtins.print') as mock_print:
        choice = CollaborateurView.display_collaborateur_menu()

        # Vérifie que le choix retourné est basé sur l'entrée utilisateur simulée
        assert choice == expected_user_input, "Le choix retourné ne correspond pas à l'entrée utilisateur simulée"

        # Vérifie que la fonction input a été appelée correctement
        mock_input.assert_called_once_with("Entrez votre choix : ")

        # Prépare une liste des appels attendus à `print`
        expected_print_calls = [
            call("\nGestion des collaborateurs"),
            call("1. Nouveau collaborateur"),
            call("2. Mise à jour du collaborateur"),
            call("3. Suppression collaborateur"),
            call("a. Menu principal"),
            call("q. Quitter"),
        ]

        # Vérifie que chaque ligne attendue du menu a été imprimée
        mock_print.assert_has_calls(expected_print_calls, any_order=False)


def test_prompt_for_new_collaborateur():
    # Simuler les entrées de l'utilisateur pour les différentes invites
    user_inputs = ['jdoe', 'jdoe@example.com', 'securepassword', '1']
    with patch('builtins.input', side_effect=user_inputs) as mock_input, \
            patch('builtins.print') as mock_print:
        collaborateur_info = CollaborateurView.prompt_for_new_collaborateur()

        # Vérifier que les informations retournées correspondent aux entrées simulées
        assert collaborateur_info == {
            "nom_utilisateur": 'jdoe',
            "email": 'jdoe@example.com',
            "mot_de_passe": 'securepassword',
            "role": '1'
        }, "Les informations du collaborateur retournées ne correspondent pas aux entrées simulées"

        # Vérifier que les invites correctes ont été affichées à l'utilisateur
        expected_print_calls = [
            call("Créer un nouveau collaborateur"),
            call("Rôles disponibles: "),
        ]

        for departement in Departement:
            expected_print_calls.append(call(f"{departement.value}"))

        mock_print.assert_has_calls(expected_print_calls, any_order=False)

        # Vérifier que les bonnes questions ont été posées dans le bon ordre
        expected_input_calls = [
            call("Nom d'utilisateur: "),
            call("Email: "),
            call("Mot de passe: "),
            call("Choisissez un rôle parmi les options ci-dessus: ")
        ]

        mock_input.assert_has_calls(expected_input_calls)


def test_list_collaborateurs():
    collaborateurs = [
        MagicMock(id=1, nom_utilisateur="Alice", email="alice@example.com"),
        MagicMock(id=2, nom_utilisateur="Bob", email="bob@example.com")
    ]

    with patch('builtins.print') as mock_print:
        CollaborateurView.list_collaborateurs(collaborateurs)

        expected_calls = [
            call(f"ID: {collaborateurs[0].id}, Nom: {collaborateurs[0].nom_utilisateur}, Email: {collaborateurs[0].email}"),
            call(f"ID: {collaborateurs[1].id}, Nom: {collaborateurs[1].nom_utilisateur}, Email: {collaborateurs[1].email}")
        ]
        mock_print.assert_has_calls(expected_calls, any_order=True)


def test_prompt_for_collaborateur_id():
    with patch('builtins.input', return_value='123'), patch('builtins.print') as mock_print:
        collab_id = CollaborateurView.prompt_for_collaborateur_id()

        assert collab_id == '123'
        mock_print.assert_called_once_with("\nEntrer l'ID du collaborateur :")


def test_prompt_for_updates():
    user_inputs = ['newuser', 'newemail@example.com', 'newpassword']
    with patch('builtins.input', side_effect=user_inputs):
        updates = CollaborateurView.prompt_for_updates()

        expected_updates = {
            'nom_utilisateur': 'newuser',
            'email': 'newemail@example.com',
            'mot_de_passe': 'newpassword'
        }
        assert updates == expected_updates


def test_confirm_delete():
    with patch('builtins.input', return_value='oui'):
        confirm = CollaborateurView.confirm_delete("Alice", 1)

        assert confirm == True
