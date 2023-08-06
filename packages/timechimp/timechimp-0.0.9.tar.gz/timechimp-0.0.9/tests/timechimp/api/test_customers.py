import logging

import timechimp

logger = logging.getLogger(__name__)


class TestGetAll:
    customers = timechimp.api.customers.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.customers, list))


class TestGetById:
    tag = timechimp.api.customers.get_by_id(customer_id=TestGetAll.customers[0]["id"],
                                            to_json=True) if TestGetAll.customers else {}

    def test_is_dict(self):
        assert(isinstance(TestGetById.tag, dict))
