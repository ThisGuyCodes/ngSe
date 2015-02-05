from selenium.webdriver import Remote
import selenium.common.exceptions as selenium_exceptions
from selenium.webdriver.common.by import By as selenium_by

from .browser import retry, cant_see_exceptions, ElementStillThereError
from .contract import must_be


class ByDict(dict):

    """Our own selenium By implementation, allows us to use the text from steps to get By values
    """
    # This is the prefix used to auto-generate NegativeByClause's
    negative_prefix = "NOT_"

    # These two allow us to use attributes and dict keys the same
    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def __getitem__(self, item):
        # Performs generation of NegativeByClause's
        if isinstance(item, basestring):
            if item.startswith(self.negative_prefix):
                return NegativeByClause(self[item[len(self.negative_prefix):]])
        return super(ByDict, self).__getitem__(item)

    def __setitem__(self, key, value):
        # Prevent inaccessible keys from getting in
        if isinstance(key, basestring):
            if key.startswith(self.negative_prefix):
                raise ValueError("Keys in this dict cannot start with '{}'".format(self.negative_prefix))
        super(ByDict, self).__setitem__(key, value)

# Implement the class, add existing values
By = ByDict()
# Is this the best way to do this? Allow retrieving key: None = value: None (for simplifying step parsing)
By[None] = None
for key, value in selenium_by.__dict__.iteritems():
    if not key.startswith('__') and isinstance(value, basestring):
        By[key] = value


class ByClause(object):

    """Implements a custom by-type, and provides conversion to underlying by-types.
    Instances pass the underlying by-type, and a function that accepts a search value and returns it modified
    appropriately.
    """

    def __init__(self, by, f):
        # Contract
        must_be(by, "by", basestring)
        if not hasattr(f, "__call__"):
            raise ValueError("f must be a callable")
        #
        self.convert = f
        self.by = by

    def __repr__(self):
        # TODO[TJ]: This seems not-good, how can we do a better of this?
        return "<{}: internal by: {}>".format(type(self), self.by)

    def convert(self, *args, **kwargs):
        raise NotImplementedError

    @retry(timeout=5)
    def wait(self, what, browser):
        """Waits for (or tries to) the desired effect, by default this is for the element to be available.
        This is put here to be override-able, so you can, say, wait for the element to 'leave'
        """
        # Contract
        must_be(what, "what", basestring)
        must_be(browser, "browser", Remote)
        #
        return self.find(what, browser)

    def find(self, what, browser):
        """Finds the desired element (what) in the provided browser
        """
        # Contract
        must_be(what, "what", basestring)
        must_be(browser, "browser", Remote)
        #
        what = self.convert(what)
        try:
            return browser.find_element(value=what, by=self.by)
        except selenium_exceptions.NoSuchElementException as e:
            e.msg += "\n  (Element: [{}], By: [{}])".format(what, self.by)
            raise e


class NegativeByClause(ByClause):

    """Takes a ByClause, and returns a subclass who's wait method waits for the element to 'leave'
    """

    def __init__(self, base_by_clause):
        # Contract
        must_be(base_by_clause, "base_by_clause", ByClause)
        #
        ByClause.__init__(self, base_by_clause.by, base_by_clause.convert)

    @retry(timeout=5)
    def wait(self, what, browser):
        """Waits for the desired element to 'leave'. Or tries to.
        """
        # Contract
        must_be(what, "what", basestring)
        must_be(browser, "browser", Remote)
        #
        try:
            self.find(what, browser)
        except cant_see_exceptions:
            return
        else:
            raise ElementStillThereError


def _inner_text_convert(value):
    # Contract
    must_be(value, "value", basestring)
    #
    parts = value.split('\\')
    text = parts.pop()
    others = " and ".join(parts)
    if len(others) > 0:
        others = " and {}".format(others)
    return '//*[contains(text(), "{}"){}]'.format(text, others)


# Implement the class, add existing values
By = ByDict()
# Is this the best way to do this? Allow retrieving key: None = value: None (for simplifying step parsing)
By[None] = None
for key, value in selenium_by.__dict__.iteritems():
    if not key.startswith('__') and isinstance(value, basestring):
        By[key] = ByClause(value, lambda v: v)

By.INNER_TEXT = ByClause(selenium_by.XPATH, _inner_text_convert)
By.NG_CLICK = ByClause(selenium_by.CSS_SELECTOR, lambda v: '[ng-click="{}"]'.format(v))
By.VISIBLE_CLICK = ByClause(selenium_by.CSS_SELECTOR, lambda v: '[ng-click="{}"]:not(.ng-hide)'.format(v))
By.NG_MODEL = ByClause(selenium_by.CSS_SELECTOR, lambda v: '[ng-model="{}"]'.format(v))
By.VISIBLE_MODEL = ByClause(selenium_by.CSS_SELECTOR, lambda v: '[ng-model="{}"]:not(.ng-hide)'.format(v))
By.VISIBLE_SELECTOR = ByClause(selenium_by.CSS_SELECTOR, lambda v: '{}:not(.ng-hide)'.format(v))