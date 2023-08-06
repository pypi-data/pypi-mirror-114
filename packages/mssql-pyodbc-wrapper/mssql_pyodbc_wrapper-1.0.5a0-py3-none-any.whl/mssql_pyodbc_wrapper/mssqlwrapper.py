# Francisco A. B. Sampaio, INEGI, 2021
# This package is a wrapper of the pyodbc module that acts as a simplified implementation for use cases where a local
# SQL Server database is to be accessed.
# It seeks to simplify use of the pyodbc module and, instead of offering the complete functionality of it, offer
# straightforward methods for interacting with the database.
# ==== IMPORT STATEMENTS ====
import pyodbc
import pandas as pd


# ==== EXCEPTION HANDLING ====
class QueryTypeError(Exception):
    pass


# ==== STATIC FUNCTIONS ====
# The interface object also provides a static function for building query strings from parameters.
# This is useful when implementing SQL injection safe programs.
# It does not allow for complex queries, only very basic SELECT, INSERT and UPDATE.
def build_simple_query_string(query_type, table_name, columns):
    _sql_query = ''

    if query_type == 'SELECT':
        _sql_query = 'SELECT '
        if columns == '*':
            _sql_query += '* '
        else:
            for _column_name in columns:
                _sql_query += f'{_column_name}, '
            _sql_query = _sql_query[:-2]
        _sql_query += f' FROM {table_name};'
    elif query_type == 'INSERT':
        _sql_query = f'INSERT INTO {table_name} ' \
                     f'('
        _parameters = ''
        for _column_name in columns:
            _sql_query += f'{_column_name}, '
            _parameters += '?, '

        _sql_query = _sql_query[:-2] + f') VALUES ({_parameters[:-2]});'
    else:
        raise QueryTypeError("Invalid query type argument.")

    return _sql_query


# ==== CLASS ====
class MSSQLWrapper:
    # The wrapper receives only the server name and the database name as its arguments in the constructor.
    def __init__(self, connection, **kwargs):
        self.connection = connection
        allowed_attributes = {'server', 'database', 'dsn', 'uid', 'pwd'}
        self.__dict__.update((keys, values) for keys, values in kwargs.items() if keys in allowed_attributes)

    @classmethod
    def from_localdb(cls, server, database):
        return MSSQLWrapper(pyodbc.connect(f'DRIVER=SQL SERVER;'
                                           f'SERVER={server};'
                                           f'DATABASE={database};'), server=server, database=database)

    @classmethod
    def from_dsn(cls, dsn='dsn', uid='sa', pwd=''):
        return MSSQLWrapper(pyodbc.connect(f'DSN={dsn};'
                                           f'UID={uid};'
                                           f'PWD={pwd}'), dsn=dsn, uid=dsn, pwd=pwd)

    def safe_select(self, table_name, columns):
        _sql_query = build_simple_query_string("SELECT", table_name, columns)
        return pd.read_sql_query(_sql_query, self.connection)

    def unsafe_select(self, sql_query):
        return pd.read_sql_query(sql_query, self.connection)
