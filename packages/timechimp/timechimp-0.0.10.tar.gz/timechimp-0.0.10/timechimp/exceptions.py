"""Module containing opdatasource custom exceptions"""


class TimeChimpAPIError(Exception):
    """The API returned an error"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
