"""Module interacting with TimeChimp API time endpoint"""

from datetime import datetime
from typing import Union, List

import requests

from timechimp.enum import ApprovalStatus
from timechimp._request import make_request
from timechimp._endpoint import TIME_ENDPOINT, DEFAULT_VERSION


def get_by_date_range(date_from: str,
                      date_to: str,
                      version: str = DEFAULT_VERSION,
                      to_json: bool = False) -> Union[requests.models.Response,
                                                      List[dict]]:
    """Get time entries by date range

    Args:
        date_from: inclusive date as YYYY-MM-DD
        date_to: inclusive date as YYYY-MM-DD
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp time requests response object

    Raises:
        ValueError, date_from cannot occur later than date_to
    """
    if datetime.strptime(date_from, "%Y-%m-%d") > datetime.strptime(date_to, "%Y-%m-%d"):
        raise ValueError(f"date_from={date_from} cannot occur later than date_to={date_to}")

    return make_request(
        url="/".join([TIME_ENDPOINT.format(version=version),
                      "daterange",
                      date_from,
                      date_to]),
        request_method=requests.get,
        to_json=to_json)


def get_by_project(project_id: int,
                   version: str = DEFAULT_VERSION,
                   to_json: bool = False, ) -> Union[requests.models.Response,
                                                     List[dict]]:
    """Get a time entry by project

    Args:
        project_id: the unique id of the project
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp time requests response object
    """
    return make_request(
        url="/".join([TIME_ENDPOINT.format(version=version),
                      "project",
                      str(project_id)]),
        request_method=requests.get,
        to_json=to_json)


def get_by_project_by_timerange(
        project_id: int,
        date_from: str,
        date_to: str,
        version: str = DEFAULT_VERSION,
        to_json: bool = False) -> Union[requests.models.Response,
                                        List[dict]]:
    """Get time entries by project and by time range

    Args:
        project_id: the unique id of the project
        date_from: inclusive date as YYYY-MM-DD
        date_to: inclusive date as YYYY-MM-DD
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp time requests response object

    Raises:
        ValueError, date_from cannot occur later than date_to
    """
    if datetime.strptime(date_from, "%Y-%m-%d") > datetime.strptime(date_to, "%Y-%m-%d"):
        raise ValueError(f"date_from={date_from} cannot occur later than date_to={date_to}")

    return make_request(
        url="/".join([TIME_ENDPOINT.format(version=version),
                      "project",
                      str(project_id),
                      date_from,
                      date_to]),
        request_method=requests.get,
        to_json=to_json)


def get_by_id(time_id: int,
              version: str = DEFAULT_VERSION,
              to_json: bool = False, ) -> Union[requests.models.Response,
                                                dict]:
    """Get a time entry by id

    Args:
        time_id: the unique id of the time entry
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp time requests response object
    """
    return make_request(
        url="/".join([TIME_ENDPOINT.format(version=version),
                      str(time_id)]),
        request_method=requests.get,
        to_json=to_json)


def get_all(version: str = DEFAULT_VERSION,
            to_json: bool = False) -> Union[requests.models.Response,
                                            List[dict]]:
    """Get all the time entries

    Args:
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp time requests response object
    """
    return make_request(
        url=TIME_ENDPOINT.format(version=version),
        request_method=requests.get,
        to_json=to_json)


def update(time: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Update a time entry

    Args:
        time: the JSON representation of the time entry to update
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp time requests response object
    """
    return make_request(
        url=TIME_ENDPOINT.format(version=version),
        request_method=requests.put,
        json=time,
        to_json=to_json)


def create(time: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Create a new time entry

    Args:
        time: the JSON representation of the time entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp time requests response object
    """
    return make_request(
        url=TIME_ENDPOINT.format(version=version),
        request_method=requests.post,
        json=time,
        to_json=to_json)


def delete(time_id: int,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Delete a time entry by id

    Args:
        time_id: the JSON representation of the time entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp time requests response object
    """
    return make_request(
        url=TIME_ENDPOINT.format(version=version),
        request_method=requests.delete,
        params={"id": time_id},
        to_json=to_json)


def submit_for_approval_internal(
    registration_ids: List[int],
    message: str,
    version: str = DEFAULT_VERSION,
    to_json: bool = False) -> Union[requests.models.Response,
                                    dict]:
    """Submit registration ids for internal approval

    Args:
        registration_ids: the list of registration ids
        message: the message the current submission
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp time requests response object
    """
    return make_request(
        url="/".join([TIME_ENDPOINT.format(version=version),
                      "submitinternal"]),
        request_method=requests.post,
        json={
            "registrationIds": registration_ids,
            "message": message
        },
        to_json=to_json)


def change_status_internal(
    registration_ids: List[int],
    approval_status: ApprovalStatus,
    message: str,
    version: str = DEFAULT_VERSION,
    to_json: bool = False) -> Union[requests.models.Response,
                                    dict]:
    """Change the internal submitted registration ids approval status

    Args:
        registration_ids: the list of registration ids
        approval_status: ApprovalStatus.APPROVED or ApprovalStatus.REJECTED
        message: the message the current submission
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp time requests response object
    """
    return make_request(
        url="/".join([TIME_ENDPOINT.format(version=version),
                      "changestatusinternal"]),
        request_method=requests.post,
        json={
            "registrationIds": registration_ids,
            "status": approval_status.value,
            "message": message,
        },
        to_json=to_json)


def submit_for_approval_external(
    registration_ids: List[int],
    contact_person_emails: List[str],
    message: str,
    version: str = DEFAULT_VERSION,
    to_json: bool = False) -> Union[requests.models.Response,
                                    dict]:
    """Submit registration ids for internal approval

    Args:
        registration_ids: the list of registration ids
        contact_person_emails: a list of contact emails
        message: the message the current submission
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp time requests response object
    """
    return make_request(
        url="/".join([TIME_ENDPOINT.format(version=version),
                      "submitexternal"]),
        request_method=requests.post,
        json={
            "registrationIds": registration_ids,
            "contactPersonEmails": contact_person_emails,
            "message": message
        },
        to_json=to_json)


def change_status_external(
    registration_ids: List[int],
    approval_status: ApprovalStatus,
    message: str,
    name: str,
    version: str = DEFAULT_VERSION,
    to_json: bool = False) -> Union[requests.models.Response,
                                    dict]:
    """Change the external submitted registration ids approval status

    Args:
        registration_ids: the list of registration ids
        approval_status: ApprovalStatus.APPROVED or ApprovalStatus.REJECTED
        message: the message the current submission
        name: the name of the reviewer
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp time requests response object
    """
    return make_request(
        url="/".join([TIME_ENDPOINT.format(version=version),
                      "changestatusexternal"]),
        request_method=requests.post,
        json={
            "registrationIds": registration_ids,
            "status": approval_status.value,
            "message": message,
            "name": name
        },
        to_json=to_json)


def start_timer(
    timer_id: int,
    version: str = DEFAULT_VERSION,
    to_json: bool = False) -> Union[requests.models.Response,
                                    str]:
    """Start a new timer

    Args:
        timer_id: the id of the started timer
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp time requests response object
    """
    return make_request(
        url="/".join([TIME_ENDPOINT.format(version=version),
                      "starttimer",
                      str(timer_id)]),
        request_method=requests.post,
        to_json=to_json)


def stop_timer(
    timer_id: int,
    version: str = DEFAULT_VERSION,
    to_json: bool = False) -> Union[requests.models.Response,
                                    int]:
    """Stop a timer to to get the number of elapsed hours

    Args:
        timer_id: the id of the timer to stop
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp time requests response object
    """
    return make_request(
        url="/".join([TIME_ENDPOINT.format(version=version),
                      "stoptimer",
                      str(timer_id)]),
        request_method=requests.post,
        to_json=to_json)


def get_status_history(
    time_id: int,
    version: str = DEFAULT_VERSION,
    to_json: bool = False,) -> Union[requests.models.Response,
                                     dict]:
    """Get a time entry's status history

    Args:
        time_id: the unique id of the time entry
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp time requests response object
    """
    return make_request(
        url="/".join([TIME_ENDPOINT.format(version=version),
                      str(time_id),
                      "statushistories"]),
        request_method=requests.get,
        to_json=to_json)
