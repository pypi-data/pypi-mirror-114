import logging

import timechimp

logger = logging.getLogger(__name__)


class TestGetAll:
    user_contracts = timechimp.api.user_contracts.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.user_contracts, list))


class TestGetById:
    user_contract = timechimp.api.user_contracts.get_by_id(
        user_contract_id=TestGetAll.user_contracts[0]["id"],
        to_json=True) if TestGetAll.user_contracts else {}

    def test_is_dict(self):
        assert(isinstance(TestGetById.user_contract, dict))
