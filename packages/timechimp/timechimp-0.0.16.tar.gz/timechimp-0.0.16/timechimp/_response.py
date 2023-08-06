"""Helper functions to work with the requests.models.Response"""

import logging
import pprint
from typing import Union
from json.decoder import JSONDecodeError

import requests

from timechimp.exceptions import TimeChimpAPIError, TimeChimpJSONDecodeError

logger = logging.getLogger(__name__)


def check_status(response: requests.models.Response) -> None:
    """Check the response status

    Args:
        response: the request response

    Raises:
        TimeChimpAPIError: depending on the response status code

    Returns:
        None
    """
    if not response.ok:
        raise TimeChimpAPIError("\n".join([
            f"response status_code={response.status_code}",
            f"response text={response.text}"
        ]))


def to_json(response: requests.models.Response) -> Union[list, dict]:
    """ Convert a request response to json

    Log the response as text if cannot be decoded to json (useful for debugging)

    Args:
        response: the request response to decode

    Raises:
        TimeChimpJSONDecodeError: the response could not be decoded to json
        TimeChimpAPIError: the API returned an error message

    Returns:
        the response converted as a dict or list
    """
    try:
        response_json = response.json()
    except JSONDecodeError:
        raise TimeChimpJSONDecodeError(f"Error when trying to decode response={response.text}")

    if "message" in response_json:
        raise TimeChimpAPIError(pprint.pformat(response_json,
                                               indent=4,
                                               sort_dicts=True))

    return response_json
