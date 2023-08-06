import logging

import timechimp

logger = logging.getLogger(__name__)


class TestGetAll:
    tags = timechimp.api.tags.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.tags, list))


class TestGetById:
    tag = timechimp.api.tags.get_by_id(tag_id=TestGetAll.tags[0]["id"],
                                       to_json=True) if TestGetAll.tags else {}

    def test_is_dict(self):
        assert(isinstance(TestGetById.tag, dict))
