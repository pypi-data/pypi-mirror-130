from typing import Dict

from superorm.engine import QueryResult, CountResult, ExecResult
from superorm.logger import Logger
from superorm.manager import Manager

from superorm.session import SessionManager


# noinspection SpellCheckingInspection
class DAO:

    # Thread cache for conn session
    _session_manager = None

    # SQL Manager
    manager = None

    def __init__(self, session_manager: SessionManager, manager: Manager):
        """
        Initialize Manager
        :param session_manager: Thread cache for conn session
        :param manager: SQL Manager
        """
        self._session_manager = session_manager
        self.manager = manager

    def query(self, key: str, parameter: Dict) -> QueryResult:
        """
        Query result set
        :param key: SQL alias
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        session = self._session_manager.get_session()
        query_result = self.manager.query(session.conn(), key, parameter)
        session.auto_commit()
        return query_result

    def count(self, key: str, parameter: Dict) -> CountResult:
        """
        Query quantity
        :param key: SQL alias
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        session = self._session_manager.get_session()
        count_result = self.manager.count(session.conn(), key, parameter)
        session.auto_commit()
        return count_result

    def exec(self, key: str, parameter: Dict) -> ExecResult:
        """
        Implementation of SQL
        :param key: SQL alias
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        session = self._session_manager.get_session()
        exec_result = self.manager.exec(session.conn(), key, parameter)
        session.auto_commit()
        return exec_result
