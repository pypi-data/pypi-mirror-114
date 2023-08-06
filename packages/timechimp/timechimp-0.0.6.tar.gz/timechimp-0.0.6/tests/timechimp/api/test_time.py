from datetime import datetime
import logging

import timechimp

logger = logging.getLogger(__name__)


class TestGetByTimeRange:
    times = timechimp.api.time.get_by_date_range(
            date_from=datetime.now().strftime("%Y-%m-%d"),
            date_to=datetime.now().strftime("%Y-%m-%d"),
            to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetByTimeRange.times, list))


class TestGetAll:
    times = timechimp.api.time.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.times, list))


class TestGetById:
    time = timechimp.api.time.get_by_id(
        time_id=TestGetAll.times[0]["id"],
        to_json=True) if TestGetAll.times else {}

    def test_is_dict(self):
        assert(isinstance(TestGetById.time, dict))
