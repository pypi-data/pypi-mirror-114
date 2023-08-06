"""Module testing the TimeChimp users endpoint"""

import logging

import timechimp

logger = logging.getLogger(__name__)


class TestGetAll:
    users = timechimp.api.users.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.users, list))


class TestGetById:
    user = timechimp.api.users.get_by_id(user_id=TestGetAll.users[0]["id"],
                                         to_json=True) if TestGetAll.users else {}

    def test_is_dict(self):
        assert(isinstance(TestGetById.user, dict))
