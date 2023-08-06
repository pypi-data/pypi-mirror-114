class VirtualSetException(Exception):
    pass


class MustReturnBool(VirtualSetException):
    pass


class InvalidArgument(VirtualSetException):
    pass


class InvalidFunction(InvalidArgument):
    pass

"""
class ExpectationError(VirtualSetException, AssertionError):
    pass
"""