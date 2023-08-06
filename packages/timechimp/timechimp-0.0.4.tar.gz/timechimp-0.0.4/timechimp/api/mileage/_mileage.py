"""Module interacting with TimeChimp API mileage endpoint"""

from datetime import datetime
from typing import Union, List

import requests

from timechimp.enum import ApprovalStatus
from timechimp._request import make_request
from timechimp._endpoint import MILEAGE_ENDPOINT, DEFAULT_VERSION


def get_by_date_range(
    date_from: str,
    date_to: str,
    version: str = DEFAULT_VERSION,
    to_json: bool = False) -> Union[requests.models.Response,
                                    List[dict]]:
    """Get mileage entries by date range

    Args:
        date_from: inclusive date as YYYY-MM-DD
        date_to: inclusive date as YYYY-MM-DD
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp mileage requests response object

    Raises:
        ValueError, date_from cannot occur later than date_to
    """
    if datetime.strptime(date_from, "%Y-%m-%d") > datetime.strptime(date_to, "%Y-%m-%d"):
        raise ValueError(f"date_from={date_from} cannot occur later than date_to={date_to}")

    return make_request(
        url="/".join([MILEAGE_ENDPOINT.format(version=version),
                      "daterange",
                      date_from,
                      date_to]),
        request_method=requests.get,
        to_json=to_json)


def get_by_project(project_id: int,
                   version: str = DEFAULT_VERSION,
                   to_json: bool = False, ) -> Union[requests.models.Response,
                                                     List[dict]]:
    """Get a mileage entry by project

    Args:
        project_id: the unique id of the project
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp mileage requests response object
    """
    return make_request(
        url="/".join([MILEAGE_ENDPOINT.format(version=version),
                      "project",
                      str(project_id)]),
        request_method=requests.get,
        to_json=to_json)


def get_by_id(mileage_id: int,
              version: str = DEFAULT_VERSION,
              to_json: bool = False, ) -> Union[requests.models.Response,
                                                dict]:
    """Get a mileage entry by id

    Args:
        mileage_id: the unique id of the mileage entry
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp mileage requests response object
    """
    return make_request(
        url="/".join([MILEAGE_ENDPOINT.format(version=version),
                      str(mileage_id)]),
        request_method=requests.get,
        to_json=to_json)


def get_all(version: str = DEFAULT_VERSION,
            params: dict = None,
            to_json: bool = False) -> Union[requests.models.Response,
                                            List[dict]]:
    """Get all the mileage entries

    Args:
        version: the version of the endpoint to use
        params: the query string parameters
        to_json: convert the request response to a json object

    Returns:
        TimeChimp mileage requests response object
    """
    return make_request(
        url=MILEAGE_ENDPOINT.format(version=version),
        request_method=requests.get,
        params=params,
        to_json=to_json)


def update(mileage: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Update a mileage entry

    Args:
        mileage: the JSON representation of the mileage entry to update
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp mileage requests response object
    """
    return make_request(
        url=MILEAGE_ENDPOINT.format(version=version),
        request_method=requests.put,
        json=mileage,
        to_json=to_json)


def create(mileage: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Create a new mileage entry

    Args:
        mileage: the JSON representation of the mileage entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp mileage requests response object
    """
    return make_request(
        url=MILEAGE_ENDPOINT.format(version=version),
        request_method=requests.post,
        json=mileage,
        to_json=to_json)


def delete(mileage_id: int,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Delete a mileage entry by id

    Args:
        mileage_id: the JSON representation of the mileage entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp mileage requests response object
    """
    return make_request(
        url=MILEAGE_ENDPOINT.format(version=version),
        request_method=requests.delete,
        params={"id": mileage_id},
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
        TimeChimp mileage requests response object
    """
    return make_request(
        url="/".join([MILEAGE_ENDPOINT.format(version=version),
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
        TimeChimp mileage requests response object
    """
    return make_request(
        url="/".join([MILEAGE_ENDPOINT.format(version=version),
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
        TimeChimp mileage requests response object
    """
    return make_request(
        url="/".join([MILEAGE_ENDPOINT.format(version=version),
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
        TimeChimp mileage requests response object
    """
    return make_request(
        url="/".join([MILEAGE_ENDPOINT.format(version=version),
                      "changestatusexternal"]),
        request_method=requests.post,
        json={
            "registrationIds": registration_ids,
            "status": approval_status.value,
            "message": message,
            "name": name
        },
        to_json=to_json)
