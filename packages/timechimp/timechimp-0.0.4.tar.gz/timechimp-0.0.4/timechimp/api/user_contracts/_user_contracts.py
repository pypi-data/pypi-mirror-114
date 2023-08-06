"""Module interacting with user contract endpoint"""

from typing import Union, List

import requests

from timechimp._request import make_request
from timechimp._endpoint import USER_CONTRACTS_ENDPOINT, DEFAULT_VERSION


def get_all(version: str = DEFAULT_VERSION,
            params: dict = None,
            to_json: bool = False) -> Union[requests.models.Response,
                                            List[dict]]:
    """Get all the user contracts

    Args:
        version: the version of the endpoint to use
        params: the query string parameters
        to_json: convert the request response to a json object

    Returns:
        TimeChimp user contracts requests response object
    """
    return make_request(
        url=USER_CONTRACTS_ENDPOINT.format(version=version),
        request_method=requests.get,
        params=params,
        to_json=to_json)


def get_by_id(user_contract_id: int,
              version: str = DEFAULT_VERSION,
              to_json: bool = False) -> Union[requests.models.Response,
                                              dict]:
    """Get a user contract by id

    Args:
        user_contract_id: the unique id of the user contract
        version: the version of the endpoint to use
        to_json: convert the request response to a json object
        **kwargs: extra parameters for requests.get

    Returns:
        TimeChimp user contracts requests response object
    """
    return make_request(
        url="/".join([USER_CONTRACTS_ENDPOINT.format(version=version),
                      str(user_contract_id)]),
        request_method=requests.get,
        to_json=to_json)


def get_by_user(user_id: int,
                version: str = DEFAULT_VERSION,
                to_json: bool = False) -> Union[requests.models.Response,
                                                   List[dict]]:
    """Get user contracts by user

    Args:
        user_id: the unique id of the user
        version: the version of the endpoint to use
        to_json: convert the request response to a json object
        **kwargs: extra parameters for requests.get

    Returns:
        TimeChimp user contracts requests response object
    """
    return make_request(
        url="/".join([USER_CONTRACTS_ENDPOINT.format(version=version),
                      "user",
                      str(user_id)]),
        request_method=requests.get,
        to_json=to_json)


def create(user_contract: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Create a user contract

    Args:
        user_contracts: the json representation of the user contract
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp user contracts requests response object
    """
    return make_request(
        url=USER_CONTRACTS_ENDPOINT.format(version=version),
        request_method=requests.post,
        json=user_contract,
        to_json=to_json)


def update(user_contract: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Update a user contract

    Args:
        user_contracts: the json representation of the user contract
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp user contracts requests response object
    """
    return make_request(
        url=USER_CONTRACTS_ENDPOINT.format(version=version),
        request_method=requests.put,
        json=user_contract,
        to_json=to_json)


def delete(user_contract_id: int,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response, dict]:
    """Delete a user contract

    Args:
        user_contract_id: the unique id of the user
        version: the version of the endpoint to use
        to_json: convert the request response to a json object
        **kwargs: extra parameters for requests.get

    Returns:
        TimeChimp user contracts requests response object
    """
    return make_request(
        url=USER_CONTRACTS_ENDPOINT.format(version=version),
        request_method=requests.delete,
        params={"id": user_contract_id},
        to_json=to_json)
