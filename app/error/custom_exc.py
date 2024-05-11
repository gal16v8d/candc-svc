"""Custom api exception """


class BadArgException(Exception):
    """
    This exception is raised if user try to send
    a non-valid field for fetch or update any model
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class BadBodyException(Exception):
    """
    This exception is raised if user does not
    send the expected payload type in a request.
    """

    def __init__(self, name: str) -> None:
        super().__init__(f"{name} data should be json")


class BadModelException(Exception):
    """This exception is raised if user try to fetch a non-valid model"""


class NotFoundException(Exception):
    """This exception is raised if no data is found in db"""

    def __init__(self, name: str) -> None:
        super().__init__(f"{name} not found")


class UnpatchableFieldException(Exception):
    """
    This exception is raised if you attempt to
    update a field that is marked as ignorable/unpatchable.
    """

    def __init__(self, field_name: str) -> None:
        super().__init__(f"{field_name} can not be updated")
