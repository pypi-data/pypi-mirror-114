"""Module interacting with TimeChimp API project users endpoint"""

from typing import Union, List

import requests

from timechimp._request import make_request
from timechimp._endpoint import PROJECT_USERS_ENDPOINT, DEFAULT_VERSION


def get_all(version: str = DEFAULT_VERSION,
            params: dict = None,
            to_json: bool = False) -> Union[requests.models.Response,
                                            List[dict]]:
    """Get all project users

    Args:
        version: the version of the endpoint to use
        params: the query parameters
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project users requests response object
    """
    return make_request(
        url=PROJECT_USERS_ENDPOINT.format(version=version),
        request_method=requests.get,
        params=params,
        to_json=to_json)


def get_by_id(project_user_id: int,
              version: str = DEFAULT_VERSION,
              to_json: bool = False) -> Union[requests.models.Response,
                                              dict]:
    """Get a project user by id

    Args:
        version: the version of the endpoint to use
        project_user_id: the unique id of the project user
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project users requests response object
    """
    return make_request(
        url="/".join([PROJECT_USERS_ENDPOINT.format(version=version),
                      str(project_user_id)]),
        request_method=requests.get,
        to_json=to_json)


def get_by_project(
        project_id: int,
        version: str = DEFAULT_VERSION,
        to_json: bool = False) -> Union[requests.models.Response,
                                        List[dict]]:
    """Get the project users by project

    Args:
        version: the version of the endpoint to use
        project_id: the unique id of the project
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project users requests response object
    """
    return make_request(
        url="/".join([PROJECT_USERS_ENDPOINT.format(version=version),
                      "project",
                      str(project_id)]),
        request_method=requests.get,
        to_json=to_json)


def get_by_user(
        user_id: int,
        version: str = DEFAULT_VERSION,
        to_json: bool = False) -> Union[requests.models.Response,
                                        List[dict]]:
    """Get the project users by user

    Args:
        version: the version of the endpoint to use
        user_id: the unique id of the user
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project users requests response object
    """
    return make_request(
        url="/".join([PROJECT_USERS_ENDPOINT.format(version=version),
                      "user",
                      str(user_id)]),
        request_method=requests.get,
        to_json=to_json)


def update(project_user: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Import project users from TimeChimp

    Args:
        version: the version of the endpoint to use
        project_user: the dict containing the new project users properties values
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project users requests response object
    """
    return make_request(
        url=PROJECT_USERS_ENDPOINT.format(version=version),
        request_method=requests.put,
        to_json=to_json,
        json=project_user)


def create(project_user: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Create a new project user entry

    Args:
        project_user: the JSON representation of the project user entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project user requests response object
    """
    return make_request(
        url=PROJECT_USERS_ENDPOINT.format(version=version),
        request_method=requests.post,
        json=project_user,
        to_json=to_json)


def delete(project_user_id: int,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Delete a project user entry by id

    Args:
        project_user_id: the JSON representation of the project user entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project user requests response object
    """
    return make_request(
        url=PROJECT_USERS_ENDPOINT.format(version=version),
        request_method=requests.delete,
        params={"id": project_user_id},
        to_json=to_json)
