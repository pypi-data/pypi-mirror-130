from abc import abstractmethod
from typing import List, Dict, Tuple, Any

from superorm.logger import Logger
from superorm.handler import render


# the query method result
QueryResult = List[Dict]
CountResult = int
ExecResult = Tuple[int, int]


class ConnBuilder:

    @abstractmethod
    def connect(self) -> Any:
        """
        Gets the database connection method
        """


class ConnHandle:

    @abstractmethod
    def ping(self, conn: Any):
        """
        Test whether the connection is available, and reconnect
        :param conn: database conn
        """

    @abstractmethod
    def commit(self, conn: Any):
        """
        Commit the connection
        :param conn: database conn
        """

    @abstractmethod
    def rollback(self, conn: Any):
        """
        Rollback the connection
        :param conn: database conn
        """


class ExecuteEngine:
    """
    SQL Execution Engine
    """
    @abstractmethod
    def query(self, conn: Any, logger: Logger, sql: str, parameter: list) -> QueryResult:
        """
        Query list information
        :param conn database conn
        :param logger logger
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """

    @abstractmethod
    def count(self, conn: Any, logger: Logger, sql: str, parameter: list) -> CountResult:
        """
        Query quantity information
        :param conn database conn
        :param logger logger
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """

    @abstractmethod
    def exec(self, conn: Any, logger: Logger, sql: str, parameter: list) -> ExecResult:
        """
        Execute SQL statement
        :param conn database conn
        :param logger logger
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Last inserted ID, affecting number of rows
        """


# noinspection SpellCheckingInspection
class TemplateEngine:
    """
    SQL template execution engine
    Using the jinja2 template engine
    """
    # SQL Execution Engine
    _execute_engine = None

    def __init__(self, execute_engine: ExecuteEngine):
        """
        Init SQL Execution Engine
        :param execute_engine: SQL Execution Engine
        """
        self._execute_engine = execute_engine

    def query(self, conn: Any, logger: Logger, sql_template: str, parameter: Dict) -> QueryResult:
        """
        Query list information
        :param conn database conn
        :param logger logger
        :param sql_template: SQL template to be executed
        :param parameter: parameter
        :return: Query results
        """
        # render and execute
        sql, param = render(sql_template, parameter)
        return self._execute_engine.query(conn, logger, sql, param)

    def count(self, conn: Any, logger: Logger, sql_template: str, parameter: Dict) -> CountResult:
        """
        Query quantity information
        :param conn database conn
        :param logger logger
        :param sql_template: SQL template to be executed
        :param parameter: parameter
        :return: Query results
        """
        # render and execute
        sql, param = render(sql_template, parameter)
        return self._execute_engine.count(conn, logger, sql, param)

    def exec(self, conn: Any, logger: Logger, sql_template: str, parameter: Dict) -> ExecResult:
        """
        Execute SQL statement
        :param conn database conn
        :param logger logger
        :param sql_template: SQL template to be executed
        :param parameter: parameter
        :return: Last inserted ID, affecting number of rows
        """
        # render and execute
        sql, param = render(sql_template, parameter)
        return self._execute_engine.exec(conn, logger, sql, param)
