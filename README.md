# pySage50DB
Python database interface Sage Line 50 Accountancy

This is a Windows only tool, 32bit python interface to the ODBC.  It can run as single CLI for use in other programs.
Its sole purpose is to get a copy of the latest database as a JSON file.  This then allows all the other code to run on
 any version of python with or without access to the data.

# Creating the .EXE file


### Installing a module locally
An aide memoire for me You need a command line like this:
'pip install git+file://C:/it/majorprojects/pySage50DB'

# Local Setup
You need to do a couple of things to get this to work:
- Install a 32bit version of Python to work with the 32bit version of Sage ODBC
- Setup the SAGE ODBC connection as a System DSN - see below.
- Create a .env file or put in the environment your settings for the ODBC string - see .env_template which is a
template.

### Setting up Sage ODBC

Create a System DSN 'CompanyX2015' which points to the file location eg  \\\\SERVER\Company.001\ACCDATA

`Control Panel\Aministrative Tools\ODBC Data Sources(32bit)`

The driver should be installed SageLine50V2

###### Check

Run Sage and open CompanyX current.

# Roadmap

The testing of this code is really dependent on having access to a live Sage ODBC connection.



