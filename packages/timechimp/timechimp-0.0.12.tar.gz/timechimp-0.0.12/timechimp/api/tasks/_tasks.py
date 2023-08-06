"""Module interacting with TimeChimp API tasks endpoint"""

from typing import Union, List

import requests

from timechimp._request import make_request
from timechimp._endpoint import TASKS_ENDPOINT, DEFAULT_VERSION


def get_all(version: str = DEFAULT_VERSION,
            to_json: bool = False) -> Union[requests.models.Response,
                                            List[dict]]:
    """Get all tasks

    Args:
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp tasks requests response object
    """
    return make_request(
        url=TASKS_ENDPOINT.format(version=version),
        request_method=requests.get,
        to_json=to_json)


def get_by_id(task_id: int,
              version: str = DEFAULT_VERSION,
              to_json: bool = False) -> Union[requests.models.Response,
                                              dict]:
    """Get a task by id

    Args:
        version: the version of the endpoint to use
        task_id: the unique id of the task
        to_json: convert the request response to a json object

    Returns:
        TimeChimp tasks requests response object
    """
    return make_request(
        url="/".join([TASKS_ENDPOINT.format(version=version),
                      str(task_id)]),
        request_method=requests.get,
        to_json=to_json)


def update(task: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Update a task

    Args:
        version: the version of the endpoint to use
        task: the dict containing the new tasks properties values
        to_json: convert the request response to a json object

    Returns:
        TimeChimp tasks requests response object
    """
    return make_request(
        url=TASKS_ENDPOINT.format(version=version),
        request_method=requests.put,
        to_json=to_json,
        json=task)


def create(task: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Create a new task entry

    Args:
        task: the JSON representation of the task entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp task requests response object
    """
    return make_request(
        url=TASKS_ENDPOINT.format(version=version),
        request_method=requests.post,
        json=task,
        to_json=to_json)


def delete(task_id: int,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Delete a task entry by id

    Args:
        task_id: the JSON representation of the task entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp task requests response object
    """
    return make_request(
        url=TASKS_ENDPOINT.format(version=version),
        request_method=requests.delete,
        params={"id": task_id},
        to_json=to_json)
