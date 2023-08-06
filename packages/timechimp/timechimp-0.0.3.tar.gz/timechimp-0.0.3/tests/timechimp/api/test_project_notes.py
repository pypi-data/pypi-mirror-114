import logging

import timechimp

logger = logging.getLogger(__name__)


class TestGetAll:
    project_notes = timechimp.api.project_notes.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.project_notes, list))


class TestGetById:
    tag = timechimp.api.project_notes.get_by_id(project_note_id=TestGetAll.project_notes[0]["id"],
                                                to_json=True) if TestGetAll.project_notes else {}

    def test_is_dict(self):
        assert(isinstance(TestGetById.tag, dict))
