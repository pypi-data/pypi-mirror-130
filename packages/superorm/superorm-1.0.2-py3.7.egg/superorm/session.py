import threading
from superorm.pool import ConnPool


class SessionManager:

    # Database conn pool
    _conn_pool = None

    # conn Session cache
    _cache = None

    def __init__(self, conn_pool: ConnPool):
        """
        Init the Thread cache for conn session
        """
        self._conn_pool = conn_pool
        self._cache = {}

    def get_session(self):
        """
        Get the cache session
        """
        _ident = threading.currentThread().ident
        if _ident in self._cache:
            return self._cache[_ident]
        _session = Session(self._conn_pool, self._conn_pool.obtain(), self)
        self._cache[_ident] = _session
        return self._cache[_ident]

    def destroy_session(self):
        """
        Destroy the cache
        """
        _ident = threading.currentThread().ident
        if _ident in self._cache:
            del self._cache[_ident]


class Session:

    # session pool
    _conn_pool = None

    # use index
    _conn_index = -1

    # session manager
    _session_manager = None

    # auto commit
    auto_commit = None

    def __init__(self, conn_pool: ConnPool, conn_index: int, session_manager: SessionManager):
        """
        Init SQLSession
        :param conn_pool: conn pool
        :param conn_index: The database connection index being used
        :param session_manager: session manager
        """
        self._conn_pool = conn_pool
        self._conn_index = conn_index
        self._session_manager = session_manager
        self.auto_commit = self.commit

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def conn(self):
        """
        Get this session conn
        :return: conn
        """
        return self._conn_pool.get(self._conn_index)

    def begin(self):
        """
        Begin transaction
        """
        def auto_commit():
            pass
        self.auto_commit = auto_commit

    def commit(self):
        """
        Commit this session
        """
        self._conn_pool.commit(self._conn_index)
        self._destroy()

    def rollback(self):
        """
        Rollback this session
        """
        self._conn_pool.rollback(self._conn_index)
        self._destroy()

    def _destroy(self):
        """
        Destroy this session
        """
        self._session_manager.destroy_session()
        self._conn_pool.give_back(self._conn_index)
        self._conn_pool = None
        self._conn_index = -1
        self._session_manager = None
        self.auto_commit = None
