import selenium.common.exceptions as selenium_exceptions


class ElementStillThereError(Exception):

    """Raised when an element that shouldn't be present, is
    """
    pass


class WaitFailedError(Exception):

    """Raised when a ByClauses wait method fails in a way we *don't* want @retry to catch
    """

    def __init__(self, message, cause):
        super(WaitFailedError, self).__init__("{}, caused by {}".format(message, repr(cause)))
        self.cause = cause


class DontRetryError(Exception):

    """Raised when a retryable error happens, but we don't want to retry
    """

    def __init__(self, message, cause):
        super(DontRetryError, self).__init__("{}, caused by {}".format(message, repr(cause)))
        self.cause = cause


class NavigationError(Exception):

    """Happens for things like 404's, 500's, expected element doesn't show up, etc.
    """
    pass


class FrontEndError(Exception):

    """Raised when an error or warning message pops up
    """
    pass



element_exceptions = (
    selenium_exceptions.InvalidElementStateException,
    selenium_exceptions.NoSuchElementException,
    selenium_exceptions.ElementNotVisibleException,
    ElementStillThereError,
    ValueError,
)

cant_see_exceptions = (
    selenium_exceptions.NoSuchElementException,
    selenium_exceptions.ElementNotVisibleException,
    selenium_exceptions.NoSuchElementException,
    ValueError,
)
