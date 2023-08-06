"""Module containing opdatasource custom exceptions"""


class TimeChimpAPIError(Exception):
    """The API returned an error"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TimeChimpDateRangeError(Exception):
    """The date range requested is invalid"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TimeChimpJSONDecodeError(Exception):
    """The API JSON response could not be decoded"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)