import logging

import timechimp

logger = logging.getLogger(__name__)


class TestGetAll:
    mileages = timechimp.api.mileage.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.mileages, list))


class TestGetById:
    tag = timechimp.api.mileage.get_by_id(mileage_id=TestGetAll.mileages[0]["id"],
                                          to_json=True) if TestGetAll.mileages else {}

    def test_is_dict(self):
        assert(isinstance(TestGetById.tag, dict))
