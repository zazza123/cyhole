class PycryptException(Exception):
    """
        General exception of pycrypt library
    """
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description
    
class RequestTypeNotSupported(PycryptException):
    pass

class AuthorizationAPIKeyError(PycryptException):
    pass

class MissingAPIKeyError(PycryptException):
    pass