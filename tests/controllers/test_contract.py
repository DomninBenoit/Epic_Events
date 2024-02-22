from decimal import Decimal

import pytest
from unittest.mock import patch, MagicMock
from contract_management.controllers import ContractController
from contract_management.model import Contrat


@pytest.mark.parametrize("choice,user_id,expected", [
    ('1', 1, ("create_contract", None)),
    ('2', 2, ("display_contract_filter_menu", None)),
    ('3', 1, ("update_contract", "some_id")),
    ('4', 2, ("delete_contract", "some_id")),
    ('a', 1, ("main_menu", None)),
    ('q', 1, ("quit", None)),
    ('invalid', 1, ("contract_management", None)),
])
def test_display_contract_menu(choice, user_id, expected):
    with patch('contract_management.controllers.Session', MagicMock()), \
         patch('contract_management.controllers.ContractView.display_contract_menu', return_value=choice), \
         patch('contract_management.controllers.ContractView.prompt_for_contract_id', return_value="some_id"), \
         patch('contract_management.controllers.ContractView.list_contracts'):
        user_session = {'user': MagicMock(id=user_id)}
        result = ContractController.display_contract_menu(user_session)
        assert result == expected


@pytest.mark.parametrize("choice, expected_call", [
    ('1', ("display_filtered_contracts", "open_contract")),
    ('2', ("display_filtered_contracts", "pending_contract")),
])
def test_display_contract_filter_menu(choice, expected_call):
    with patch('contract_management.controllers.ContractView.display_contract_filter_menu', return_value=choice), \
            patch(
                'contract_management.controllers.ContractController.display_filtered_contracts') as mock_display_filtered:
        # Configurez le mock pour retourner une valeur par défaut lorsqu'il est appelé.
        mock_display_filtered.return_value = (expected_call[1], None)

        result = ContractController.display_contract_filter_menu({})

        mock_display_filtered.assert_called_once_with({}, expected_call[1])
        assert result == (expected_call[1], None)


@pytest.mark.parametrize("filter_type, filter_call", [
    ("open_contract", MagicMock(montant_restant=100)),
    ("pending_contract", MagicMock(statut="non signé"))
])
def test_display_filtered_contracts(filter_type, filter_call):
    with patch('common.base.Session') as mock_session, \
         patch('contract_management.controllers.ContractView.list_contracts') as mock_list_contracts:
        mock_session_instance = mock_session.return_value
        mock_query = mock_session_instance.query.return_value
        # Configurez les mocks pour simuler les contrats retournés par le filtre
        if filter_type == "open_contract":
            mock_query.filter.return_value.all.return_value = [filter_call]
        elif filter_type == "pending_contract":
            mock_query.filter.return_value.all.return_value = [filter_call]

        ContractController.display_filtered_contracts({}, filter_type)

        # Vérifiez que list_contracts est appelée avec la liste de contrats filtrée
        mock_list_contracts.assert_called_once()

@patch('common.base.Session')
@patch('contract_management.controllers.ContractView.prompt_for_new_contract')
def test_create_contract(mock_prompt_for_new_contract, mock_session):
    mock_session_instance = mock_session.return_value
    mock_query_client = mock_session_instance.query.return_value.filter_by.return_value.first.side_effect = [MagicMock(), None]  # Simuler le client existant, puis l'absence de collaborateur

    contract_data = {
        "client_id": 1,
        "contact_commercial_id": 2,
        "montant_total": "1000",
        "montant_restant": "1000",
        "statut": "non signé"
    }
    mock_prompt_for_new_contract.return_value = contract_data

    # Test lorsque le client existe mais le collaborateur commercial n'existe pas
    result = ContractController.create_contract({})
    assert result == ("contract_management", None)
    mock_session_instance.commit.assert_not_called()


@pytest.mark.parametrize("is_contract_found, is_user_associated, updates, expected_return", [
    # Ajustez votre paramétrage si nécessaire
    (True, True, {"montant_total": Decimal("2000.00"), "montant_restant": Decimal("1500.00"), "statut": "en cours"}, ("contract_management", None)),
])
def test_update_contract(is_contract_found, is_user_associated, updates, expected_return):
    with patch('common.base.Session') as mock_session, \
         patch('contract_management.controllers.ContractView.prompt_for_updates', return_value=updates):
        mock_contrat = MagicMock(contact_commercial_id=1)
        mock_session.return_value.query.return_value.filter_by.return_value.first.return_value = mock_contrat
        user_session = {"user": MagicMock(id=1)}  # Assurez-vous que l'ID correspond

        result = ContractController.update_contract(user_session, contrat_id=123)

        assert result == expected_return
