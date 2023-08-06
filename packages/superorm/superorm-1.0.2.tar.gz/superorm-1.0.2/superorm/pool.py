from threading import Lock

from superorm.engine import ConnHandle, ConnBuilder


class ConnPool:

    # _lock
    _lock = None

    # conn
    _conn_builder = None
    _conn_handle = None

    # Current number of connections
    _lazy_init = None
    _max_conn_number = 0

    # conns
    _conns = None

    # use flag
    _flags = None

    def __init__(self, conn_builder: ConnBuilder, conn_handle: ConnHandle,
                 lazy_init=True, max_conn_number=10):
        """
        Init conn pool
        :param conn_builder: ConnBuilder
        :param conn_handle: ConnHandle
        :param lazy_init: lazy_init
        :param max_conn_number: max_conn_number
        """
        # lock
        self._lock = Lock()
        # conn
        self._conn_builder = conn_builder
        self._conn_handle = conn_handle

        self._lazy_init = lazy_init
        self._max_conn_number = max_conn_number

        # db conn
        self._conns = []
        # used conn
        self._flags = []
        # lazy loading
        if not lazy_init:
            for i in range(max_conn_number):
                self._conns.append(self._conn_builder.connect())
                self._flags.append(i)

    def obtain(self) -> int:
        """
        Obtain SQL conn index from conn Pool
        :return: SQL conn index
        """
        self._lock.acquire()
        while True:
            flags_length = len(self._flags)
            conns_length = len(self._conns)
            # When connections are exhausted and 
            # the maximum number of connections is not exceeded
            if flags_length == 0 and conns_length < self._max_conn_number:
                # init new conn
                conn = self._conn_builder.connect()
                self._conns.append(conn)
                # return the conn
                self._lock.release()
                return conns_length
            if flags_length > 0:
                # set use flag
                index = self._flags[0]
                self._flags = self._flags[1:]
                # test the conn
                self._conn_handle.ping(self._conns[index])
                # end test conn
                self._lock.release()
                return index

    def commit(self, index: int):
        """
        Commit
        :param index: The index of the conn in the conn pool
        """
        self._conn_handle.commit(self._conns[index])

    def rollback(self, index: int):
        """
        Commit conn
        :param index: The index of the conn in the conn pool
        """
        self._conn_handle.rollback(self._conns[index])

    def get(self, index: int):
        """
        Get the conn from the conn pool
        :param index: The index of the conn in the conn pool
        """
        return self._conns[index]

    def give_back(self, index: int):
        """
        Return the conn to the conn pool
        :param index: The index of the conn in the conn pool
        """
        self._flags.append(index)
