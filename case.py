"""
Implements TestCase and TestCasePlugin.

Nose discriminates between subclasses of unittest.TestCase and everything else.
Subclasses of unittest.TestCase cannot use advanced features (such as test
generators) to nose can work with legacy tests. [1] However, since nose doesn't
run classes that are not subclasses of unittest.TestCase identically, along
with advanced features, we access those advanced features without any change in
behavior by reimplementing TestCase.

.. [1]
    Jason Pellerin (author Nose). Sep 16 2012. Conflicts between unittest and
    nose frameworks.
    http://stackoverflow.com/a/12447407/577199
"""
import re
import unittest

from nose.plugins.base import Plugin
import nose.tools


_CAPS = re.compile('([A-Z])')


class TestCase(object):
    def __init__(self):
        self._cleanups = []

    def fail(self, msg=None):
        raise AssertionError(msg)

    def addCleanup(self, f, *args, **kwargs):
        self._cleanups.append((f, args, kwargs))

    def doCleanups(self):
        while self._cleanups:
            function, args, kwargs = self._cleanups.pop()
            function(*args, **kwargs)


# Dynamically add 'assert*' methods to TestCase. This could also be implemented
# using __getattr__, but then no 'assert*' method could be overridden.
for attr in dir(unittest.TestCase):
    if attr.startswith('assert') and '_' not in attr:
        pep8_name = _CAPS.sub(lambda m: '_' + m.groups()[0].lower(), attr)
        setattr(TestCase, attr, getattr(nose.tools, pep8_name))
del attr

TestCase.fail.__func__.__doc__ = unittest.TestCase.fail.__doc__
TestCase.addCleanup.__func__.__doc__ = unittest.TestCase.addCleanup.__doc__
TestCase.doCleanups.__func__.__doc__ = unittest.TestCase.doCleanups.__doc__


class TestCasePlugin(Plugin):
    """
    Plugin for Nose that calls ``doCleanups()`` on TestCase objects which are
    not subclasses of unittest.Testcase after each test is run.
    """
    name = 'testcase'

    def options(self, parser, env):
        """Sets additional command line options."""
        super(TestCasePlugin, self).options(parser, env)

    def configure(self, options, config):
        """Configures the test timer plugin."""
        super(TestCasePlugin, self).configure(options, config)

    def afterTest(self, test):
        try:
            test_case = test.test.inst
        except AttributeError:
            pass
        else:
            test_case.doCleanups()
