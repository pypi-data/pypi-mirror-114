"""Module interacting with TimeChimp API projects endpoint"""

from typing import Union, List

import requests

from timechimp._request import make_request
from timechimp._endpoint import PROJECTS_ENDPOINT, DEFAULT_VERSION


def get_all(version: str = DEFAULT_VERSION,
            params: dict = None,
            to_json: bool = False) -> Union[requests.models.Response,
                                            List[dict]]:
    """Get all the projects

    Args:
        version: the version of the endpoint to use
                 "2", get also inactive projects
        params: the query parameters
        headers: the requests.get headers param to use

    Returns:
        TimeChimp projects requests response object
    """
    return make_request(
        url=PROJECTS_ENDPOINT.format(version=version),
        request_method=requests.get,
        params=params,
        to_json=to_json)


def get_by_id(project_id: int,
              version: str = DEFAULT_VERSION,
              to_json: bool = False) -> Union[requests.models.Response,
                                              dict]:
    """Get a project by id

    Args:
        project_id: the unique id of the project
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project s requests response object
    """
    return make_request(
        url="/".join([PROJECTS_ENDPOINT.format(version=version),
                      str(project_id)]),
        request_method=requests.get,
        to_json=to_json)


def get_by_customer(
        customer_id: int,
        version: str = DEFAULT_VERSION,
        to_json: bool = False) -> Union[requests.models.Response,
                                        List[dict]]:
    """Get the projects by customer

    Args:
        customer_id: the unique id of the the customer
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project s requests response object
    """
    return make_request(
        url="/".join([PROJECTS_ENDPOINT.format(version=version),
                      "customer",
                      str(customer_id)]),
        request_method=requests.get,
        to_json=to_json)


def get_by_insight(
        insight_id: int,
        version: str = DEFAULT_VERSION,
        to_json: bool = False) -> Union[requests.models.Response,
                                        List[dict]]:
    """Get the projects by insight

    Args:
        insight_id: the unique id of the
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project s requests response object
    """
    return make_request(
        url="/".join([PROJECTS_ENDPOINT.format(version=version),
                      "insights",
                      str(insight_id)]),
        request_method=requests.get,
        to_json=to_json)


def update(project: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Update a project

    Args:
        version: the version of the endpoint to use
        project: the dict containing the new project s properties values
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project s requests response object
    """
    return make_request(
        url=PROJECTS_ENDPOINT.format(version=version),
        request_method=requests.put,
        to_json=to_json,
        json=project)


def create(project: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Create a new project entry

    Args:
        project: the JSON representation of the project  entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project  requests response object
    """
    return make_request(
        url=PROJECTS_ENDPOINT.format(version=version),
        request_method=requests.post,
        json=project,
        to_json=to_json)


def delete(project_id: int,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Delete a project entry by id

    Args:
        project_id: the JSON representation of the project  entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project  requests response object
    """
    return make_request(
        url=PROJECTS_ENDPOINT.format(version=version),
        request_method=requests.delete,
        params={"id": project_id},
        to_json=to_json)
