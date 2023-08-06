"""Module interacting with TimeChimp API invoice endpoint"""

from typing import Union, List

import requests

from timechimp._request import make_request
from timechimp._endpoint import INVOICES_ENDPOINT, DEFAULT_VERSION


def get_by_project(project_id: int,
                   version: str = DEFAULT_VERSION,
                   to_json: bool = False, ) -> Union[requests.models.Response,
                                                     List[dict]]:
    """Get a invoice entry by project

    Args:
        project_id: the unique id of the project
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp invoice requests response object
    """
    return make_request(
        url="/".join([INVOICES_ENDPOINT.format(version=version),
                      "project",
                      str(project_id)]),
        request_method=requests.get,
        to_json=to_json)


def get_by_id(invoice_id: int,
              version: str = DEFAULT_VERSION,
              to_json: bool = False, ) -> Union[requests.models.Response,
                                                dict]:
    """Get a invoice entry by id

    Args:
        invoice_id: the unique id of the invoice entry
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp invoice requests response object
    """
    return make_request(
        url="/".join([INVOICES_ENDPOINT.format(version=version),
                      str(invoice_id)]),
        request_method=requests.get,
        to_json=to_json)


def get_all(version: str = DEFAULT_VERSION,
            params: dict = None,
            to_json: bool = False) -> Union[requests.models.Response,
                                            List[dict]]:
    """Get all the invoice entries

    Args:
        version: the version of the endpoint to use
        params: the query string parameters
        to_json: convert the request response to a json object

    Returns:
        TimeChimp invoice requests response object
    """
    return make_request(
        url=INVOICES_ENDPOINT.format(version=version),
        request_method=requests.get,
        params=params,
        to_json=to_json)
