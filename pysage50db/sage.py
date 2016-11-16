"""Interface to Sage accounting ODBC DB connector

This provides an interface to extract data from the accounting system and save as JSON file.

It works by extracting the data into a Pandas dataframe and then doing queries from that.

"""
import json
import numpy as np
import pandas as pd
import pyodbc
import os

from luca import p


class PySageError(Exception):
    pass

def get_default_connection_string():
    # Make sure environment variables loaded.
    try:
        try:
            # Python 2
            connection_string = os.environ['PYSAGE_CNXN'].decode('utf8')
        except AttributeError:
            # Python 3
            connection_string = os.environ['PYSAGE_CNXN']
    except KeyError:
        raise PySageError('Environment missing PYSAGE_CNXN setting. '
            + 'Check for .env file looked here ??')
    return connection_string


def get_max_transaction_in_sage(cnxn):
    sql = """
SELECT
    max(TRAN_NUMBER)
FROM
    AUDIT_JOURNAL
    """
    df = pd.read_sql(sql, cnxn)
    return int(df.iloc[0,0])

def get_dataframe_sage_odbc_query(sql, name):
    """This executes a SQL query if it needs to or pulls in a json file from disk.
    The results of the SQL query are returned as a dataframe.  To decide which to do
    the maximum transaction is compared to the json file."""
    connection_string = get_default_connection_string()
    cnxn = pyodbc.connect(connection_string)
    # Get the maximum transaction number
    json_check_file_name = name + '_check.json'
    json_file_name = name + '.json'
    # Read it from file
    try:
        with open(json_check_file_name) as f:
            data = json.load(f)
        max_transaction_stored = data['max_transaction_stored']
    except (FileNotFoundError, ValueError):  # Triggered as open nonexistent file is ok but no data
        max_transaction_stored = 0
    max_transaction_in_sage = get_max_transaction_in_sage(cnxn)
    if max_transaction_stored == 0 or max_transaction_stored != max_transaction_in_sage:
        # If no data stored or it is out of date then
        df = pd.read_sql(sage_all_data, cnxn)
        # Read fresh data from sage
        # Update files
        df.to_json(json_file_name)
        data = {'max_transaction_stored': max_transaction_in_sage}
        with open(json_check_file_name, 'w') as f:
            json.dump(data, f)


sage_all_data = """
SELECT
    aj.TRAN_NUMBER, aj.TYPE, aj.DATE, nl.ACCOUNT_REF, aj.ACCOUNT_REF as ALT_REF, aj.INV_REF, aj.DETAILS, AJ.TAX_CODE,
    aj.AMOUNT, aj.FOREIGN_AMOUNT, aj.BANK_FLAG, ah.DATE_BANK_RECONCILED, aj.EXTRA_REF
FROM
NOMINAL_LEDGER nl, AUDIT_HEADER ah
LEFT OUTER JOIN AUDIT_JOURNAL aj ON nl.ACCOUNT_REF = aj.NOMINAL_CODE
WHERE
aj.HEADER_NUMBER = ah.HEADER_NUMBER AND
aj.DATE > '2000-01-01' AND aj.DELETED_FLAG = 0
"""


class SageDB:
    """Interface to SAGE line 50 account system.
    """
    def  __init__(self, connection_string=''):
        if connection_string == '':
            connection_string = get_default_connection_string()
        self.sqldata = get_dataframe_sage_odbc_query(sage_all_data, 'SageODBC')
        if self.sqldata['DATE'].dtype == np.object:
            self.sqldata['DATE'] = self.sqldata['DATE'].astype('datetime64')

