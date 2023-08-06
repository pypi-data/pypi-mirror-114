"""Module interacting with TimeChimp Users API"""

from typing import Union, List

import requests

from timechimp._request import make_request
from timechimp._endpoint import USERS_ENDPOINT, DEFAULT_VERSION


def get_all(version: str = DEFAULT_VERSION,
            to_json: bool = False) -> Union[requests.models.Response,
                                            List[dict]]:
    """Get all the users

    Args:
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp users requests response object
    """
    return make_request(
        url=USERS_ENDPOINT.format(version=version),
        request_method=requests.get,
        to_json=to_json)


def get_by_id(user_id: int,
              version: str = DEFAULT_VERSION,
              to_json: bool = False) -> Union[requests.models.Response,
                                              dict]:
    """Get a user by id

    Args:
        user_id: the unique id of the user
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp users requests response object
    """
    return make_request(
        url="/".join([USERS_ENDPOINT.format(version=version),
                      str(user_id)]),
        request_method=requests.get,
        to_json=to_json)


def update(user: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Update a user

    Args:
        user: the dict containing the new users properties values
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp users requests response object
    """
    return make_request(
        url=USERS_ENDPOINT.format(version=version),
        request_method=requests.put,
        to_json=to_json,
        json=user)
