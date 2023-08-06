import logging

import timechimp

logger = logging.getLogger(__name__)


class TestGetAll:
    invoices = timechimp.api.invoices.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.invoices, list))


class TestGetById:
    tag = timechimp.api.invoices.get_by_id(invoice_id=TestGetAll.invoices[0]["id"],
                                           to_json=True) if TestGetAll.invoices else {}

    def test_is_dict(self):
        assert(isinstance(TestGetById.tag, dict))
