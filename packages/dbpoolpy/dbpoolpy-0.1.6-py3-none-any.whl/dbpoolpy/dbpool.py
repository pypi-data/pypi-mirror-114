# coding: utf-8
import time
import random
import threading
import traceback
from contextlib import contextmanager
from .utils import log
from .dbconnect import SQLiteConnection
from .dbconnect import PyMySQLConnection
from .pooled_db import PooledDB

dbpool = None


class DBPoolBase(object):
    def acquire(self, name):
        pass

    def release(self, name, conn):
        pass

class DBPool(DBPoolBase):
    def __init__(self, dbcf):
        # one item: [conn, last_get_time, stauts]
        self.dbconn_idle = []
        self.dbconn_using = []

        self.dbcf = dbcf
        self.max_conn = 20
        self.min_conn = 1

        if self.dbcf.get('conn') is not None:
            self.max_conn = self.dbcf['conn']

        self.connection_class = {
            SQLiteConnection.type:SQLiteConnection,
            PyMySQLConnection.type:PyMySQLConnection
        }
        # x = globals()
        # for v in x.values():
        #     if str(type(v)) == "<class 'type'>" and v != DBConnection and issubclass(v, DBConnection):
        #         self.connection_class[v.type] = v
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)
        self.open(self.min_conn)

    def synchronize(func):
        def _(self, *args, **argitems):
            self.lock.acquire()
            x = None
            try:
                x = func(self, *args, **argitems)
            finally:
                self.lock.release()
            return x
        return _

    def open(self, n=1):
        param = self.dbcf
        newconns = []
        for i in range(0, n):
            myconn = self.connection_class[param['engine']](param, time.time(), 0)
            myconn.pool = self
            newconns.append(myconn)
        self.dbconn_idle += newconns

    def clear_timeout(self):
        # log.info('try clear timeout conn ...')
        now = time.time()
        dels = []
        allconn = len(self.dbconn_idle) + len(self.dbconn_using)
        for c in self.dbconn_idle:
            if allconn == 1:
                break
            if now - c.lasttime > self.dbcf.get('idle_timeout', 10):
                dels.append(c)
                allconn -= 1

        if dels:
            log.debug('close timeout db conn:%d', len(dels))
        for c in dels:
            if c.conn:
                c.close()
            self.dbconn_idle.remove(c)

    @synchronize
    def acquire(self, timeout=10):
        start = time.time()
        while len(self.dbconn_idle) == 0:
            if len(self.dbconn_idle) + len(self.dbconn_using) < self.max_conn:
                self.open()
                continue
            self.cond.wait(timeout)
            if int(time.time() - start) > timeout:
                log.error('func=acquire|error=no idle connections')
                raise RuntimeError('no idle connections')

        conn = self.dbconn_idle.pop(0)
        conn.useit()
        self.dbconn_using.append(conn)

        if random.randint(0, 100) > 80:
            try:
                self.clear_timeout()
            except:
                log.error(traceback.format_exc())

        return conn

    @synchronize
    def release(self, conn):
        if conn:
            if conn.trans:
                log.debug('realse close conn use transaction')
                conn.close()
                # conn.connect()

            self.dbconn_using.remove(conn)
            conn.releaseit()
            if conn.conn:
                self.dbconn_idle.insert(0, conn)
        self.cond.notify()

    @synchronize
    def alive(self):
        for conn in self.dbconn_idle:
            conn.alive()

    def size(self):
        return len(self.dbconn_idle), len(self.dbconn_using)

def checkalive(name=None):
    global dbpool
    while True:
        if name is None:
            checknames = dbpool.keys()
        else:
            checknames = [name]
        for k in checknames:
            pool = dbpool[k]
            pool.alive()
        time.sleep(300)


def init_pool(db_conf, is_old=False):
    global dbpool
    if dbpool:
        log.warn("too many install db")
        return dbpool
    dbpool = {}
    for name, item in db_conf.items():
        if is_old:
            item['name'] = name
            dbp = DBPool(item)
        else:
            dbp = PooledDB(**item)
        dbpool[name] = dbp
    return dbpool


def acquire(name, is_old=False, timeout=10):
    global dbpool
    # log.info("acquire:", name)
    pool = dbpool[name]
    if is_old:
        con = pool.acquire(timeout)
        con.name = name
    else:
        con = pool.connection()
        log.info('name=%s|max_con=%s|con=%s|idle_cache=%s' % (
            name,
            con._pool._maxconnections, 
            con._pool._connections, 
            len(con._pool._idle_cache))
            )
    return con


def release(conn, is_old=False):
    if not conn:
        return
    if is_old:
        global dbpool
        pool = dbpool[conn.name]
        return pool.release(conn)
    else:
        return conn.close()

@contextmanager
def connect_without_exception(token):
    conn = None
    try:
        conn = acquire(token)
        yield conn
    except:
        log.error("error=%s", traceback.format_exc())
    finally:
        if conn:
            release(conn)

@contextmanager
def connect_db(token, is_old=False):
    '''出现异常捕获后，关闭连接并抛出异常'''
    conn = None
    try:
        conn = acquire(token, is_old)
        yield conn
    except:
        log.error("error=%s", traceback.format_exc())
        raise
    finally:
        if conn:
            release(conn, is_old)


def with_connect_db(name, errfunc=None, errstr=''):
    '''数据库连接装饰器,可以用在静态方法和类方法里
    name: 要连接的数据库：可以用tuple和list连接多个数据库
    静态方法：self必传值为None
    '''
    def f(func):
        def _(self, *args, **kwargs):
            multi_db = isinstance(name, (tuple, list))
            is_class_methed = str(type(self)).startswith("<class '__main__")
            if not is_class_methed and self is not None:
                raise Exception(
                    "with_connect_db在装饰静态方法时，方法调用传值首个必须为None, 而不是%s" 
                    % str(self))
            if multi_db:           # 连接多个数据库
                dbs = {}
                for dbname in name:
                    dbs[dbname] = acquire(dbname)
                if is_class_methed:
                    self.db = dbs
                else:
                    self = dbs
            else:
                if is_class_methed:
                    self.db = acquire(name)
                else:
                    self = acquire(name)

            res = None
            try:
                res = func(self, *args, **kwargs)
            except:
                if errfunc:
                    return getattr(self, errfunc)(error=errstr)
                else:
                    raise Exception(traceback.format_exc())
            finally:
                if multi_db:
                    dbs = self.db if is_class_methed else self
                    dbnames = list(dbs.keys())
                    for dbname in dbnames:
                        release(dbs.pop(dbname))
                else:
                    release(self.db if is_class_methed else self)
                if is_class_methed:
                    self.db = None
                else:
                    self = None
            return res
        return _
    return f
