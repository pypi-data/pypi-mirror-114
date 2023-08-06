import logging

import timechimp

logger = logging.getLogger(__name__)


class TestGetAll:
    project_tasks = timechimp.api.project_tasks.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.project_tasks, list))


class TestGetById:
    tag = timechimp.api.project_tasks.get_by_id(project_task_id=TestGetAll.project_tasks[0]["id"],
                                                to_json=True) if TestGetAll.project_tasks else {}

    def test_is_dict(self):
        assert(isinstance(TestGetById.tag, dict))
