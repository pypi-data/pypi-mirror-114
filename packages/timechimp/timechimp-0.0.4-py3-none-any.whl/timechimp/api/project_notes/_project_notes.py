"""Module interacting with TimeChimp API project notes endpoint"""

from typing import Union, List

import requests

from timechimp._request import make_request
from timechimp._endpoint import PROJECT_NOTES_ENDPOINT, DEFAULT_VERSION


def get_all(version: str = DEFAULT_VERSION,
            params: dict = None,
            to_json: bool = False) -> Union[requests.models.Response,
                                            List[dict]]:
    """Get all project notes

    Args:
        version: the version of the endpoint to use
        params: the query parameters
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project notes requests response object
    """
    return make_request(
        url=PROJECT_NOTES_ENDPOINT.format(version=version),
        request_method=requests.get,
        params=params,
        to_json=to_json)


def get_by_id(project_note_id: int,
              version: str = DEFAULT_VERSION,
              to_json: bool = False) -> Union[requests.models.Response,
                                              dict]:
    """Get a project note by id

    Args:
        version: the version of the endpoint to use
        project_note_id: the unique id of the project note
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project notes requests response object
    """
    return make_request(
        url="/".join([PROJECT_NOTES_ENDPOINT.format(version=version),
                      str(project_note_id)]),
        request_method=requests.get,
        to_json=to_json)


def get_by_project(
        project_id: int,
        version: str = DEFAULT_VERSION,
        to_json: bool = False) -> Union[requests.models.Response,
                                        List[dict]]:
    """Get the project notes by project

    Args:
        version: the version of the endpoint to use
        project_id: the unique id of the project
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project notes requests response object
    """
    return make_request(
        url="/".join([PROJECT_NOTES_ENDPOINT.format(version=version),
                      "project",
                      str(project_id)]),
        request_method=requests.get,
        to_json=to_json)


def update(project_note: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Import project notes from TimeChimp

    Args:
        version: the version of the endpoint to use
        project_note: the dict containing the new project notes properties values
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project notes requests response object
    """
    return make_request(
        url=PROJECT_NOTES_ENDPOINT.format(version=version),
        request_method=requests.put,
        to_json=to_json,
        json=project_note)


def create(project_note: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Create a new project note entry

    Args:
        project_note: the JSON representation of the project note entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project note requests response object
    """
    return make_request(
        url=PROJECT_NOTES_ENDPOINT.format(version=version),
        request_method=requests.post,
        json=project_note,
        to_json=to_json)


def delete(project_note_id: int,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Delete a project note entry by id

    Args:
        project_note_id: the JSON representation of the project note entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project note requests response object
    """
    return make_request(
        url=PROJECT_NOTES_ENDPOINT.format(version=version),
        request_method=requests.delete,
        params={"id": project_note_id},
        to_json=to_json)
