import sys
import os
import unittest

from IPython.testing import globalipapp


class Settings(object):
    INSTALLED_APPS = [
        'django.contrib.auth',
        'django_tabcomplete',
    ]

    SECRET_KEY = '123'


class TestFilterCompletion(unittest.TestCase):
    def setUp(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'mydjangosettings'
        sys.modules['mydjangosettings'] = Settings()
        import django
        django.setup()
        self.ipshell = globalipapp.get_ipython()
        import django_tabcomplete

    def assert_completion(self, buf, expected=[], unexpected=[]):
        if not isinstance(expected, (set, list, tuple)):
            expected = [expected]
        if not isinstance(unexpected, (set, list, tuple)):
            expected = [unexpected]
        _, actual = self.ipshell.complete(buf)
        not_found = set(expected) - set(actual)
        if not_found:
            raise AssertionError('Completions of %r do not include %r. '
                                 'Got %r' % (buf, sorted(not_found), actual))
        found = set(unexpected) & set(actual)
        if found:
            raise AssertionError('Completions of %r do include unwanted %r. '
                                 '' % (buf, sorted(found)))

    def test_single_field(self):
        self.assert_completion('User.objects.filter(us', 'username')
        self.assert_completion('User.objects.filter(', 'username')
        self.assert_completion('User.objects.filter(username', 'username')
        self.assert_completion('User.objects.filter(usa',
                               unexpected='username')
