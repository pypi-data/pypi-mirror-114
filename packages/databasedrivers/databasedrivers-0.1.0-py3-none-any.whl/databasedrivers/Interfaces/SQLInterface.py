from typing import Union, Tuple, List, Dict
from databasedrivers.Configs.Classes.SQLConfigClass import SQLConfigClass
from databasedrivers.Configs.Dictonaries.SQLConfigDictionary import (
    sql_config_dictionary,
)


class SQLInterface:
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
    ) -> "SQLInterface":
        pass

    def __del__(self) -> None:
        pass

    def close(self) -> None:
        pass

    def _set_cursor(self) -> None:
        pass

    def query(
        self, query: str, parameters: Union[Tuple, List] = None, commit: bool = 1
    ) -> None:
        pass

    def get_array(self) -> List[Dict]:
        pass

    def get_row(self) -> Dict:
        pass

    def query_to_array(
        self, query: str, parameters: Union[Tuple, List] = None, commit: bool = 1
    ) -> List[Dict]:
        pass

    def query_to_row(
        self, query: str, parameters: Union[Tuple, List] = None, commit: bool = 1
    ) -> Dict:
        pass

    def commit(self) -> None:
        pass
