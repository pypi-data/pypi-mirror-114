#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import traceback
from .utils import timeit
from .utils import log
from .conf import MYSQL_SSLKEY_PATH
from .dbhelper import DBHelper
from contextlib import contextmanager


def with_mysql_reconnect(func):
    def close_mysql_conn(self):
        try:
            self.conn.close()
        except:
            log.warning(traceback.format_exc())
            self.conn = None

    def _(self, *args, **argitems):
        if self.type == 'mysql':
            import MySQLdb as m
        elif self.type == 'pymysql':
            import pymysql as m
        trycount = 3
        while True:
            try:
                x = func(self, *args, **argitems)
            except m.OperationalError as e:
                if e[0] >= 2000 and self.trans == 0:  # 客户端错误
                    log.info(traceback.format_exc())
                    close_mysql_conn(self)
                    self.connect()
                    trycount -= 1
                    if trycount > 0:
                        continue

                log.warning(traceback.format_exc())
                raise
            except (m.InterfaceError, m.InternalError):
                log.warning(traceback.format_exc())
                if self.trans == 0:
                    close_mysql_conn(self)
                    self.connect()
                    trycount -= 1
                    if trycount > 0:
                        continue
                raise
            else:
                return x
    return _


class DBConnection(DBHelper):
    def __init__(self, param, lasttime, status):
        self.name = param.get('name')
        self.param = param
        self.conn = None
        self.status = status
        self.lasttime = lasttime
        self.server_id = None
        self.conn_id = 0
        self.trans = 0  # is start transaction
        self.role = param.get('role', 'm')  # master/slave

    def __str__(self):
        return '<%s %s:%d %s@%s>' % (self.type,
                                     self.param.get(
                                         'host', ''), self.param.get('port', 0),
                                     self.param.get(
                                         'user', ''), self.param.get('db', 0)
                                     )

    def is_available(self):
        return self.status == 0

    def useit(self):
        self.status = 1
        self.lasttime = time.time()

    def releaseit(self):
        self.status = 0

    def connect(self):
        pass

    def close(self):
        pass

    def alive(self):
        pass

    def cursor(self):
        return self.conn.cursor()

    def last_insert_id(self):
        pass

    def start(self):  # start transaction
        self.trans = 1
        pass

    def commit(self):
        self.trans = 0
        self.conn.commit()

    def rollback(self):
        self.trans = 0
        self.conn.rollback()

    def escape(self, s):
        return s

    @contextmanager
    def connect_cur(self):
        cur = None
        try:
            cur = self.cursor()
            yield cur
            self.commit()
        except:
            self.rollback()
        finally:
            if cur is not None:
                cur.close()

class MySQLConnection(DBConnection):
    type = "mysql"

    def __init__(self, param, lasttime, status):
        DBConnection.__init__(self, param, lasttime, status)
        self.connect()

    def useit(self):
        self.status = 1
        self.lasttime = time.time()

    def releaseit(self):
        self.status = 0

    def connect(self):
        pass

    def close(self):
        log.info('server=%s|func=close|id=%d', self.type, self.conn_id % 10000)
        self.conn.close()
        self.conn = None

    @with_mysql_reconnect
    def alive(self):
        if self.is_available():
            cur = self.conn.cursor()
            cur.execute("show tables;")
            cur.close()
            self.conn.ping()

    @with_mysql_reconnect
    def execute(self, sql, param=None):
        return DBConnection.execute(self, sql, param)

    @with_mysql_reconnect
    def executemany(self, sql, param):
        return DBConnection.executemany(self, sql, param)

    @with_mysql_reconnect
    def query(self, sql, param=None, isdict=True, head=False):
        return DBConnection.query(self, sql, param, isdict, head)

    @with_mysql_reconnect
    def get(self, sql, param=None, isdict=True):
        return DBConnection.get(self, sql, param, isdict)

    def escape(self, s, enc='utf-8'):
        if str(type(s)) == "<class 'unicode'>":
            s = s.encode(enc)
        ns = self.conn.escape_string(s)
        if isinstance(ns, str):
            return ns
        return str(ns, enc)

    def last_insert_id(self):
        ret = self.query('select last_insert_id()', isdict=False)
        return ret[0][0]

    def start(self):
        self.trans = 1
        sql = "start transaction"
        return self.execute(sql)

    def commit(self):
        self.trans = 0
        sql = 'commit'
        return self.execute(sql)

    def rollback(self):
        self.trans = 0
        sql = 'rollback'
        return self.execute(sql)


class PyMySQLConnection(MySQLConnection):
    type = "pymysql"

    def __init__(self, param, lasttime, status):
        MySQLConnection.__init__(self, param, lasttime, status)

    def connect(self):
        engine = self.param['engine']
        if engine == 'pymysql':
            import pymysql

            ssl = None
            key_path = os.path.join(MYSQL_SSLKEY_PATH, '{host}_{port}'.format(**{
                'host': self.param['host'], 'port': self.param['port']}))
            if os.path.exists(key_path):
                log.debug('IP:%s|PORT:%s|SSL=True|ssl_path:%s',
                          self.param['host'], self.param['port'], key_path)
                ssl = {
                    'ssl': {
                        'ca': os.path.join(key_path, 'ssl-ca'),
                        'key': os.path.join(key_path, 'ssl-key'),
                        'cert': os.path.join(key_path, 'ssl-cert'),
                    }
                }
            self.conn = pymysql.connect(host=self.param['host'],
                                        port=self.param['port'],
                                        user=self.param['user'],
                                        passwd=self.param['passwd'],
                                        db=self.param['db'],
                                        charset=self.param['charset'],
                                        connect_timeout=self.param.get(
                                            'timeout', 10),
                                        ssl=ssl,
                                        )
            self.conn.autocommit(1)
            self.trans = 0

            cur = self.conn.cursor()
            cur.execute("show variables like 'server_id'")
            row = cur.fetchone()
            self.server_id = int(row[1])
            cur.close()

            cur = self.conn.cursor()
            cur.execute("select connection_id()")
            row = cur.fetchone()
            self.conn_id = row[0]
            cur.close()

        else:
            raise ValueError('engine error:' + engine)
        log.info('server=%s|func=connect|id=%d|name=%s|user=%s|role=%s|addr=%s:%d|db=%s',
                 self.type, self.conn_id % 10000,
                 self.name, self.param.get('user', ''), self.role,
                 self.param.get('host', ''), self.param.get('port', 0),
                 self.param.get('db', ''))


class SQLiteConnection(DBConnection):
    type = "sqlite"

    def __init__(self, param, lasttime, status):
        DBConnection.__init__(self, param, lasttime, status)

    def connect(self):
        engine = self.param['engine']
        self.trans = 0
        if engine == 'sqlite':
            import sqlite3
            self.conn = sqlite3.connect(
                self.param['db'], detect_types=sqlite3.PARSE_DECLTYPES, isolation_level=None)
        else:
            raise ValueError('engine error:' + engine)

    def useit(self):
        DBConnection.useit(self)
        if not self.conn:
            self.connect()

    def releaseit(self):
        DBConnection.releaseit(self)
        self.conn.close()
        self.conn = None

    def escape(self, s, enc='utf-8'):
        s = s.replace("'", "\'")
        s = s.replace('"', '\"')
        return s

    def last_insert_id(self):
        ret = self.query('select last_insert_rowid()', isdict=False)
        return ret[0][0]

    def start(self):
        self.trans = 1
        sql = "BEGIN"
        return self.conn.execute(sql)
