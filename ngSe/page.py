from types import NoneType

from .by import ByClause, By
from .contract import must_be


class AppPage(object):

    """Object to represent pages to navigate to in the app
    """

    def __init__(self, page, wait_for=None, wait_for_by=By.ID):
        # Contract
        if not isinstance(page, basestring) and not hasattr(page, "__call__"):
            raise ValueError("page must be a string or callable")
        must_be(wait_for, "wait_for", (NoneType, basestring))
        must_be(wait_for_by, "wait_for_by", (ByClause))
        #
        self._page = page
        self.wait_for = wait_for
        self.wait_for_by = wait_for_by

    @property
    def page(self):
        if not isinstance(self._page, basestring) and hasattr(self._page, "__call__"):
            return self._page()
        return self._page
