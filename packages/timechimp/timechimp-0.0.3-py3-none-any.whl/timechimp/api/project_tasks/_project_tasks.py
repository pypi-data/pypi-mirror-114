"""Module interacting with TimeChimp API project tasks endpoint"""

from typing import Union, List

import requests

from timechimp._request import make_request
from timechimp._endpoint import PROJECT_TASKS_ENDPOINT, DEFAULT_VERSION


def get_all(version: str = DEFAULT_VERSION,
            params: dict = None,
            to_json: bool = False) -> Union[requests.models.Response,
                                            List[dict]]:
    """Get all project tasks

    Args:
        version: the version of the endpoint to use
        params: the query parameters
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project tasks requests response object
    """
    return make_request(
        url=PROJECT_TASKS_ENDPOINT.format(version=version),
        request_method=requests.get,
        params=params,
        to_json=to_json)


def get_by_id(project_task_id: int,
              version: str = DEFAULT_VERSION,
              to_json: bool = False) -> Union[requests.models.Response,
                                              dict]:
    """Get a project task by id

    Args:
        version: the version of the endpoint to use
        project_task_id: the unique id of the project task
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project tasks requests response object
    """
    return make_request(
        url="/".join([PROJECT_TASKS_ENDPOINT.format(version=version),
                      str(project_task_id)]),
        request_method=requests.get,
        to_json=to_json)


def get_by_project(
        project_id: int,
        version: str = DEFAULT_VERSION,
        to_json: bool = False) -> Union[requests.models.Response,
                                        List[dict]]:
    """Get the project tasks by project

    Args:
        version: the version of the endpoint to use
        project_id: the unique id of the project
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project tasks requests response object
    """
    return make_request(
        url="/".join([PROJECT_TASKS_ENDPOINT.format(version=version),
                      "project",
                      str(project_id)]),
        request_method=requests.get,
        to_json=to_json)


def get_by_task(
        task_id: int,
        version: str = DEFAULT_VERSION,
        to_json: bool = False) -> Union[requests.models.Response,
                                        List[dict]]:
    """Get the project tasks by task

    Args:
        version: the version of the endpoint to use
        task_id: the unique id of the task
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project tasks requests response object
    """
    return make_request(
        url="/".join([PROJECT_TASKS_ENDPOINT.format(version=version),
                      "task",
                      str(task_id)]),
        request_method=requests.get,
        to_json=to_json)


def update(project_task: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Import project tasks from TimeChimp

    Args:
        version: the version of the endpoint to use
        project_task: the dict containing the new project tasks properties values
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project tasks requests response object
    """
    return make_request(
        url=PROJECT_TASKS_ENDPOINT.format(version=version),
        request_method=requests.put,
        to_json=to_json,
        json=project_task)


def create(project_task: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Create a new project task entry

    Args:
        project_task: the JSON representation of the project task entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project task requests response object
    """
    return make_request(
        url=PROJECT_TASKS_ENDPOINT.format(version=version),
        request_method=requests.post,
        json=project_task,
        to_json=to_json)


def delete(project_task_id: int,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Delete a project task entry by id

    Args:
        project_task_id: the JSON representation of the project task entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp project task requests response object
    """
    return make_request(
        url=PROJECT_TASKS_ENDPOINT.format(version=version),
        request_method=requests.delete,
        params={"id": project_task_id},
        to_json=to_json)
