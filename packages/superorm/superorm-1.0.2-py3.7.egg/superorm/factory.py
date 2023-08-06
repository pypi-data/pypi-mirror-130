from typing import Callable, Any, Dict

from superorm.dao import DAO
from superorm.engine import TemplateEngine, ConnBuilder, ConnHandle, ExecuteEngine, QueryResult, CountResult, ExecResult
from superorm.logger import DefaultLogger, Logger
from superorm.manager import Manager
from superorm.mapper import Mapper
from superorm.pool import ConnPool
from superorm.session import SessionManager
from superorm.wraps import sqlsession


class SQLSessionFactory:

    # Session Manager
    _session_manager = None

    # SQL template execution engine
    _engine = None

    # logger
    _logger = None

    # DAO
    _dao = None

    def __init__(self, conn_builder: ConnBuilder, conn_handle: ConnHandle, execute_engine: ExecuteEngine,
                 lazy_init: bool, max_conn_number: int, logger: Logger):
        """
        Init session pool
        :param conn_builder: ConnBuilder
        :param conn_handle: ConnHandle
        :param execute_engine: ExecuteEngine
        :param lazy_init: lazy_init
        :param max_conn_number: max_conn_number
        :param logger: Logger
        """
        _conn_pool = ConnPool(conn_builder, conn_handle, lazy_init, max_conn_number)
        self._session_manager = SessionManager(_conn_pool)
        self._engine = TemplateEngine(execute_engine)
        self._logger = logger
        self._dao = {}
        self.transaction_wraps = sqlsession(self)

    def load_dao(self, name: str, mapper: Mapper):
        """
        Load DAO from string
        """
        _manager = Manager(self._engine, mapper, self._logger)
        _dao = DAO(self._session_manager, _manager)
        self._dao[name] = _dao
        return self

    def get_dao(self, dao_name: str) -> DAO:
        """
        Get dao
        :param dao_name: dao name
        :return: DAO
        """
        return self._dao[dao_name]

    def query(self, sql_template: str, parameter: Dict) -> QueryResult:
        """
        Query list information
        :param sql_template: SQL template to be executed
        :param parameter: parameter
        :return: Query results
        """
        _session = self._session_manager.get_session()
        _conn = _session.conn()
        _query_result = self._engine.query(_conn, self._logger, sql_template, parameter)
        _session.auto_commit()
        return _query_result

    def count(self, sql_template: str, parameter: Dict) -> CountResult:
        """
        Query quantity
        :param sql_template: SQL template to be executed
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        _session = self._session_manager.get_session()
        _conn = _session.conn()
        _count_result = self._engine.count(_conn, self._logger, sql_template, parameter)
        _session.auto_commit()
        return _count_result

    def exec(self, sql_template: str, parameter: Dict) -> ExecResult:
        """
        Implementation of SQL
        :param sql_template: SQL template to be executed
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        _session = self._session_manager.get_session()
        _conn = _session.conn()
        _exec_result = self._engine.exec(_conn, self._logger, sql_template, parameter)
        _session.auto_commit()
        return _exec_result

    def transaction(self, handle: Callable[[], None]) -> Any:
        """
        Open a session
        :param handle: session operation
        :return: SQL Session
        """
        with self._session_manager.get_session() as session:
            try:
                handle()
                session.commit()
                return None
            except Exception as e:
                session.rollback()
                return e


class SQLSessionFactoryBuild:

    _conn_builder = None
    _conn_handle = None
    _execute_engine = None

    _lazy_init = True
    _max_conn_number = 10

    _logger = None

    def __init__(self, conn_builder: ConnBuilder, conn_handle: ConnHandle, execute_engine: ExecuteEngine):
        """
        Init session pool
        :param conn_builder: ConnBuilder
        :param conn_handle: ConnHandle
        :param execute_engine: ExecuteEngine
        """
        self._conn_builder = conn_builder
        self._conn_handle = conn_handle
        self._execute_engine = execute_engine

        self._logger = DefaultLogger()

    def set_logger(self, logger: Logger):
        """
        Set Logger
        :param logger: log printing
        :return self
        """
        self._logger = logger
        return self

    def set_lazy_loading(self, lazy: bool):
        """
        Set thread pool lazy loading
        :param lazy: bool
        :return: SQLSessionFactoryBuild
        """
        self._lazy_init = lazy
        return self

    def set_max_conn_number(self, number):
        """
        Sets the maximum number of connections to the thread pool
        :param number: max number
        :return: SQLSessionFactoryBuild
        """
        self._max_conn_number = number
        return self

    def build(self) -> SQLSessionFactory:
        return SQLSessionFactory(
            self._conn_builder,
            self._conn_handle,
            self._execute_engine,
            self._lazy_init,
            self._max_conn_number,
            self._logger
        )
