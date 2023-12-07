'''Custom api exception '''
class BadArgException(Exception):
    '''
    This exception is raised if user try to send
    a non-valid field for fetch or update any model
    '''
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
