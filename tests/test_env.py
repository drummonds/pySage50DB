import os
import unittest

from dotenv import load_dotenv, find_dotenv

from pysage50db import PySageError

class TestEnv(unittest.TestCase):

    def test_env(self):
        # Check that a local .env has been not set or that there is a production variable.
        # Note that this test will fail in a raw environment.  It is really a run time test.
        env = find_dotenv()
        if env:
            # Have a real intallation and some of the test should work.
            print(env)
            load_dotenv(env)
            try:
                # Python 2
                connection_string = os.environ['PYSAGE_CNXN'].decode('utf8')
            except AttributeError:
                # Python 3
                connection_string = os.environ['PYSAGE_CNXN']
            print(connection_string)
            assert (len(connection_string + ' ') > 1)

        else:
            print('Searched {}\n or {}\nupwards to root and not found file'.format( globals()['__file__'], os.getcwd()))
            self.assertTrue(True, 'No .env file as should be in blank default installation.')
