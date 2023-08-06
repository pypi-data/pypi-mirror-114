import logging

import timechimp

logger = logging.getLogger(__name__)


class TestGetAll:
    expenses = timechimp.api.expenses.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.expenses, list))


class TestGetById:
    tag = timechimp.api.expenses.get_by_id(expense_id=TestGetAll.expenses[0]["id"],
                                           to_json=True) if TestGetAll.expenses else {}

    def test_is_dict(self):
        assert(isinstance(TestGetById.tag, dict))
