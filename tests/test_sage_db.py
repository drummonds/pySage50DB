"""Unit tests for AIS

Aim to exercise both p and remittance docu
"""
from decimal import Decimal
from os import remove, path
from unittest import TestCase, main

from dotenv import load_dotenv, find_dotenv

from pysage50db import SageDB, PySageError


class SageTestCase(TestCase):

    def setUp(self):
        load_dotenv(find_dotenv())

    def clean_up(self):
        for fn2 in ['SageODBC_check.json', 'SageODBC.json']:
            for fn in [fn2, '../' + fn2]:
                try:
                    remove(fn)
                except FileNotFoundError:
                    pass

    def test_sage_number(self):
        # Not a very good test as specific to my installation and database of sage
        self.clean_up()  # Delete Json files
        sage = SageDB()  # Create JSON files
        # This should work with memoized files and so should the assertions
        sage2 = SageDB()  # Do nothin as  JSON files are up to date
