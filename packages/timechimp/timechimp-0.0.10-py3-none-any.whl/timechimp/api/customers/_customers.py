"""Module interacting with TimeChimp API customer endpoint"""

from typing import Union, List

import requests

from timechimp._request import make_request
from timechimp._endpoint import CUSTOMERS_ENDPOINT, DEFAULT_VERSION


def get_by_id(customer_id: int,
              version: str = DEFAULT_VERSION,
              to_json: bool = False) -> Union[requests.models.Response,
                                              dict]:
    """Get a customer entry by id

    Args:
        customer_id: the unique id of the customer entry
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp customer requests response object
    """
    return make_request(
        url="/".join([CUSTOMERS_ENDPOINT.format(version=version),
                      str(customer_id)]),
        request_method=requests.get,
        to_json=to_json)


def get_by_name(
        customer_name: str,
        version: str = DEFAULT_VERSION,
        to_json: bool = False) -> Union[requests.models.Response,
                                        dict]:
    """Get a customer entry by id

    Args:
        customer_name: the unique name of the customer entry
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp customer requests response object
    """
    return make_request(
        url="/".join([CUSTOMERS_ENDPOINT.format(version=version),
                      "name",
                      customer_name]),
        request_method=requests.get,
        to_json=to_json)


def get_by_relation(
        relation_id: int,
        version: str = DEFAULT_VERSION,
        to_json: bool = False) -> Union[requests.models.Response,
                                        List[dict]]:
    """Get a customer entry by id

    Args:
        relation_id: the unique id of the relation entry
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp customer requests response object
    """
    return make_request(
        url="/".join([CUSTOMERS_ENDPOINT.format(version=version),
                      "relationid",
                      str(relation_id)]),
        request_method=requests.get,
        to_json=to_json)


def get_all(version: str = DEFAULT_VERSION,
            params: dict = None,
            to_json: bool = False) -> Union[requests.models.Response,
                                            List[dict]]:
    """Get all the customer entries

    Args:
        version: the version of the endpoint to use
        params: the query string parameters
        to_json: convert the request response to a json object

    Returns:
        TimeChimp customer requests response object
    """
    return make_request(
        url=CUSTOMERS_ENDPOINT.format(version=version),
        request_method=requests.get,
        params=params,
        to_json=to_json)


def update(customer: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Update a customer entry

    Args:
        customer: the JSON representation of the customer entry to update
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp customer requests response object
    """
    return make_request(
        url=CUSTOMERS_ENDPOINT.format(version=version),
        request_method=requests.put,
        json=customer,
        to_json=to_json)


def create(customer: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Create a new customer entry

    Args:
        customer: the JSON representation of the customer entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp customer requests response object
    """
    return make_request(
        url=CUSTOMERS_ENDPOINT.format(version=version),
        request_method=requests.post,
        json=customer,
        to_json=to_json)


def delete(customer_id: int,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Delete a customer entry by id

    Args:
        customer_id: the JSON representation of the customer entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp customer requests response object
    """
    return make_request(
        url=CUSTOMERS_ENDPOINT.format(version=version),
        request_method=requests.delete,
        params={"id": customer_id},
        to_json=to_json)
