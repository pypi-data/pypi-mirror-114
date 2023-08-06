"""Module interacting with TimeChimp API tags endpoint"""

from typing import Union, List

import requests

from timechimp._request import make_request
from timechimp._endpoint import TAGS_ENDPOINT, DEFAULT_VERSION


def get_all(version: str = DEFAULT_VERSION,
            to_json: bool = False) -> Union[requests.models.Response,
                                            List[dict]]:
    """Get all tags

    Args:
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp tags requests response object
    """
    return make_request(
        url=TAGS_ENDPOINT.format(version=version),
        request_method=requests.get,
        to_json=to_json)


def get_by_id(tag_id: int,
              version: str = DEFAULT_VERSION,
              to_json: bool = False) -> Union[requests.models.Response,
                                              dict]:
    """Get a tag by id

    Args:
        version: the version of the endpoint to use
        tag_id: the unique id of the tag
        to_json: convert the request response to a json object

    Returns:
        TimeChimp tags requests response object
    """
    return make_request(
        url="/".join([TAGS_ENDPOINT.format(version=version),
                      str(tag_id)]),
        request_method=requests.get,
        to_json=to_json)


def update(tag: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Update a tag

    Args:
        version: the version of the endpoint to use
        tag: the dict containing the new tags properties values
        to_json: convert the request response to a json object

    Returns:
        TimeChimp tags requests response object
    """
    return make_request(
        url=TAGS_ENDPOINT.format(version=version),
        request_method=requests.put,
        to_json=to_json,
        json=tag)


def create(tag: dict,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Create a new tag entry

    Args:
        tag: the JSON representation of the tag entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp tag requests response object
    """
    return make_request(
        url=TAGS_ENDPOINT.format(version=version),
        request_method=requests.post,
        json=tag,
        to_json=to_json)


def delete(tag_id: int,
           version: str = DEFAULT_VERSION,
           to_json: bool = False) -> Union[requests.models.Response,
                                           dict]:
    """Delete a tag entry by id

    Args:
        tag_id: the JSON representation of the tag entry to create
        version: the version of the endpoint to use
        to_json: convert the request response to a json object

    Returns:
        TimeChimp tag requests response object
    """
    return make_request(
        url=TAGS_ENDPOINT.format(version=version),
        request_method=requests.delete,
        params={"id": tag_id},
        to_json=to_json)
