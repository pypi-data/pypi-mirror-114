import logging

import timechimp

logger = logging.getLogger(__name__)


class TestGetAll:
    project_users = timechimp.api.project_users.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.project_users, list))


class TestGetById:
    tag = timechimp.api.project_users.get_by_id(project_user_id=TestGetAll.project_users[0]["id"],
                                                to_json=True) if TestGetAll.project_users else {}

    def test_is_dict(self):
        assert(isinstance(TestGetById.tag, dict))
