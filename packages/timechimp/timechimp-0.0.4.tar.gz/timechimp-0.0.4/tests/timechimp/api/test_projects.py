import logging

import timechimp

logger = logging.getLogger(__name__)


class TestGetAll:
    projects = timechimp.api.projects.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.projects, list))


class TestGetById:
    tag = timechimp.api.projects.get_by_id(project_id=TestGetAll.projects[0]["id"],
                                           to_json=True) if TestGetAll.projects else {}

    def test_is_dict(self):
        assert(isinstance(TestGetById.tag, dict))
