import time
import logging
from .conf import LOG_CONF
from . import logger
logger.install('stdout')

log = logging.getLogger()

class DBFunc(object):
    def __init__(self, data):
        self.value = data

def timeit(func):
    def _(*args, **kwargs):
        starttm = time.time()
        ret = 0
        num = 0
        err = ''
        try:
            retval = func(*args, **kwargs)
            if isinstance(retval, list):
                num = len(retval)
            elif isinstance(retval, dict):
                num = 1
            elif isinstance(retval, int):
                ret = retval
            return retval
        except Exception as e:
            err = str(e)
            ret = -1
            raise e
        finally:
            endtm = time.time()
            conn = args[0]
            # dbcf = conn.pool.dbcf
            dbcf = conn.param
            sql = repr(args[1])
            if not LOG_CONF.get('log_allow_print_sql', True):
                sql = '***'

            log.info(
                'server=%s|id=%d|name=%s|user=%s|addr=%s:%d|db=%s|idle=%d|busy=%d|max=%d|trans=%d|time=%d|ret=%s|num=%d|sql=%s|err=%s',
                conn.type, conn.conn_id % 10000,
                conn.name, dbcf.get('user', ''),
                dbcf.get('host', ''), dbcf.get('port', 0),
                dbcf.get('db', ''),
                len(conn.pool.dbconn_idle),
                len(conn.pool.dbconn_using),
                conn.pool.max_conn, conn.trans,
                int((endtm - starttm) * 1000000),
                str(ret), num,
                sql, err)
    return _

def timesql(func):
    def _(*args, **kwargs):
        starttm = time.time()
        ret = 0
        num = 0
        err = ''
        try:
            retval = func(*args, **kwargs)
            if isinstance(retval, list):
                num = len(retval)
            elif isinstance(retval, dict):
                num = 1
            elif isinstance(retval, int):
                ret = retval
            return retval
        except Exception as e:
            err = str(e)
            ret = -1
            raise e
        finally:
            endtm = time.time()
            conn = args[0]
            # dbcf = conn.pool.dbcf
            dbcf = conn._kwargs
            sql = repr(args[1])
            if not LOG_CONF.get('log_allow_print_sql', True):
                sql = '***'

            log.info(
                'server=%s|conn=%d|user=%s|addr=%s:%d|db=%s|time=%d|ret=%s|num=%d|sql=%s|err=%s' % (
                getattr(conn, '_server_id', '0'), getattr(conn, '_conn_id', 0) % 10000,
                dbcf.get('user', ''), dbcf.get('host', ''), 
                dbcf.get('port', 0), dbcf.get('database', ''),
                int((endtm - starttm) * 1000000),
                str(ret), num,
                sql, err))
    return _
