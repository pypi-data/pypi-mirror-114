"""Internal request dispatcher allowing to log request data"""

import copy
import logging
import os
from typing import Union

import requests

from timechimp import _response
from timechimp._env_variable import _ENV_ACCESS_TOKEN_VAR


logger = logging.getLogger(__name__)


def kwargs_to_string(**kwargs) -> str:
    """Beautify string representation of **kwargs
    Hide the TimeChimp access token

    Args:
        **kwargs: extra args for the request method

    Returns:
        A string representation of **kwargs
    """
    kwargs_copy = copy.deepcopy(kwargs)
    kwargs_copy["headers"]["Authorization"] = "HIDDEN_TOKEN"
    kwargs_str = ""

    for kwarg, val in kwargs_copy.items():
        kwargs_str += "\n" if kwargs_str else ""
        kwargs_str += " = ".join([kwarg, f"{val!r}"])
    
    return kwargs_str


def make_request(
        url: str,
        to_json: bool,
        request_method: Union[requests.get,
                              requests.delete,
                              requests.put,
                              requests.post,
                              requests.patch],
        **kwargs) -> Union[requests.models.Response,
                           list, dict]:
    """ Dispatch a request for the given url, method and arguments

    Args:
        url: the request url
        to_json: whether to return the response as json
        request_method: the request method
        **kwargs: extra args for the request method

    Returns:
        The request response
    """
    kwargs["headers"] = {"Authorization": f"Bearer {os.environ[_ENV_ACCESS_TOKEN_VAR]}"}

    logger.info(f"{request_method.__name__.upper()} {url}")  # GET https://www.api.timechimp.com
    logger.info(kwargs_to_string(**kwargs))

    response = request_method(
            url=url,
            **kwargs)

    _response.check_status(response)

    if to_json:
        return _response.to_json(response)

    return response
