import logging

import timechimp

logger = logging.getLogger(__name__)


class TestGetAll:
    tasks = timechimp.api.tasks.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.tasks, list))


class TestGetById:
    task = timechimp.api.tasks.get_by_id(task_id=TestGetAll.tasks[0]["id"],
                                         to_json=True) if TestGetAll.tasks else {}

    def test_is_dict(self):
        assert(isinstance(TestGetById.task, dict))
