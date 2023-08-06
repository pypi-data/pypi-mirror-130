from typing import Dict, Any

from superorm.engine import QueryResult, CountResult, ExecResult, TemplateEngine
from superorm.logger import Logger
from superorm.mapper import Mapper


# noinspection SpellCheckingInspection
class Manager:

    # SQL Execution Engine
    _engine = None

    # XML profile properties
    mapper = None

    # logger
    _logger = None

    def __init__(self, engine: TemplateEngine, mapper: Mapper, logger: Logger):
        """
        Initialize Manager
        :param engine: SQL Execution Engine
        :param mapper: XML profile information
        """
        self._engine = engine
        self.mapper = mapper
        self._logger = logger

    def query(self, conn: Any, key: str, parameter: Dict) -> QueryResult:
        """
        Query result set
        :param conn: database conn
        :param key: SQL alias
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        # Get SQL
        sql_template = self.mapper["sqls"][key]
        return self._query(conn, sql_template, parameter)

    def count(self, conn: Any, key: str, parameter: Dict) -> CountResult:
        """
        Query quantity
        :param conn: database conn
        :param key: SQL alias
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        # Get SQL
        sql_template = self.mapper["sqls"][key]
        return self._count(conn, sql_template, parameter)

    def exec(self, conn: Any, key: str, parameter: Dict) -> ExecResult:
        """
        Implementation of SQL
        :param conn: database conn
        :param key: SQL alias
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        # Get SQL
        sql_template = self.mapper["sqls"][key]
        return self._exec(conn, sql_template, parameter)

    def _query(self, conn: Any, sql_template: str, parameter: Dict) -> QueryResult:
        """
        Query result set
        :param conn: database conn
        :param sql_template: SQL template
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        try:
            # Implementation of SQL
            query_list = self._engine.query(conn, self._logger, sql_template, parameter)
            # Translation alias
            data = []
            for query_item in query_list:
                item = {}
                for t in query_item.items():
                    if t[0] in self.mapper["mappers"]:
                        item[self.mapper["mappers"][t[0]]] = t[1]
                        continue
                    item[t[0]] = t[1]
                data.append(item)
        except Exception as e:
            self._logger.print_error(e)
            raise e

        return data

    def _count(self, conn: Any, sql_template: str, parameter: Dict) -> CountResult:
        """
        Query quantity
        :param conn: database conn
        :param sql_template: SQL template
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        try:
            # Implementation of SQL
            count = self._engine.count(conn, self._logger, sql_template, parameter)
        except Exception as e:
            self._logger.print_error(e)
            raise e

        return count

    def _exec(self, conn: Any, sql_template: str, parameter: Dict) -> ExecResult:
        """
        Implementation of SQL
        :param conn: database conn
        :param sql_template: SQL template
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        try:
            # Implementation of SQL
            lastrowid, rowcount = self._engine.exec(conn, self._logger, sql_template, parameter)
        except Exception as e:
            self._logger.print_error(e)
            raise e

        return lastrowid, rowcount
