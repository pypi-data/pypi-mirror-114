from databasedrivers.Interfaces.SQLInterface import SQLInterface
from typing import Union, Tuple, List, Dict
from databasedrivers.Configs.Classes.SQLConfigClass import SQLConfigClass
from databasedrivers.Configs.Dictonaries.SQLConfigDictionary import (
    sql_config_dictionary,
)

import mysql.connector
from os import getenv


class MySQLConnector(SQLInterface):
    _connection = None
    _cursor = None
    _data: Union[List[Dict], Dict] = None
    _query: str = None

    def __init__(
        self,
        configuration: SQLConfigClass = None,
        dictionary_configuration: sql_config_dictionary = None,
        file: str = None,
        hostname: str = None,
        port: int = None,
        username: str = None,
        password: str = None,
        database: str = None,
    ) -> SQLInterface:
        if configuration is not None:
            hostname = hostname or configuration.hostname
            port = port or configuration.port
            username = username or configuration.username
            password = password or configuration.password
            database = database or configuration.database
        elif dictionary_configuration is not None:
            hostname = hostname or dictionary_configuration.get("hostname", None)
            port = port or dictionary_configuration.get("port", None)
            username = username or dictionary_configuration.get("username", None)
            password = password or dictionary_configuration.get("password", None)
            database = database or dictionary_configuration.get("database", None)

        hostname = hostname or getenv("MYSQL_HOSTNAME")
        port = port or getenv("MYSQL_PORT")
        username = username or getenv("MYSQL_USERNAME")
        password = password or getenv("MYSQL_PASSWORD")
        database = database or getenv("MYSQL_DATABASE")

        self._connection = mysql.connector.MySQLConnection(
            user=username,
            password=password,
            host=hostname,
            port=port,
            database=database,
        )

        self._set_cursor()

    def __del__(self):
        self.close()

    def close(self) -> None:
        self._cursor.close()
        self._connection.close()

    def _set_cursor(self) -> None:
        self._cursor = self._connection.cursor(dictionary=True, buffered=True)

    def query(
        self, query: str, parameters: Union[Tuple, List] = None, commit: bool = True
    ) -> None:
        if parameters is None:
            self._cursor.execute(query)
        else:
            self._cursor.execute(query, parameters)

        if commit == True:
            self.commit()

        self._query = self._cursor.statement
        try:
            self._data = self._cursor.fetchall()
        except Exception as e:
            print(e)
            self._data = [{}]

    def get_array(self) -> List[Dict]:
        return self._data

    def get_row(self) -> Dict:
        try:
            result = self._data[0]
        except IndexError:
            result = {}
        return result

    def query_to_array(
        self, query: str, parameters: Union[Tuple, List] = None, commit: bool = True
    ) -> List[Dict]:
        self.query(query, parameters, commit)
        return self.get_array()

    def query_to_row(
        self, query: str, parameters: Union[Tuple, List] = None, commit: bool = True
    ) -> Dict:
        self.query(query, parameters, commit)
        return self.get_row()

    def commit(self) -> None:
        self._connection.commit()
