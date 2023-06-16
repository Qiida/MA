def raiseInputOutputException(message=None):
    try:
        raise LcmIOException(message)
    except LcmIOException as exception:
        print(exception)


def raiseMissingDataException(lcm, message):
    try:
        raise LcmMissingDataException(lcm=lcm, message=message)
    except LcmException as exception:
        print(exception)


class LcmException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class LcmIOException(LcmException):
    def __init__(self, message="lcm.IOException: Either file or path."):
        super().__init__(message)


class LcmMissingDataException(LcmException):
    def __init__(self, lcm, message="lcm.MissingDataException"):
        super().__init__(message)
