import os
import time
import abc
import datetime
import traceback
from .utils import DBFunc
from .utils import timesql
from . import pager
from contextlib import contextmanager


class DBHelper:
    def __init__(self):
        self._con = None

    @abc.abstractmethod
    @contextmanager
    def connect_cur(self):
        cur = None
        try:
            yield cur
        except:
            pass
        finally:
            pass

    #执行命令
    @timesql
    def execute(self, sql, param=None):
        '''执行单个sql命令'''
        with self.connect_cur() as cur:
            if param:
                if not isinstance(param, (dict, tuple)):
                    param = tuple([param])
                ret = cur.execute(sql, param)
            else:
                ret = cur.execute(sql)
            return ret

    @timesql
    def executemany(self, sql, param):
        '''调用executemany执行多条命令'''
        with self.connect_cur() as cur:
            if param:
                if not isinstance(param, (dict, tuple)):
                    param = tuple([param])
                ret = cur.executemany(sql, param)
            else:
                ret = cur.executemany(sql)
            return ret

    @timesql
    def query(self, sql, param=None, isdict=True, hashead=False):
        '''sql查询，返回查询结果
        sql: 要执行的sql语句
        param: 要传入的参数
        isdict: 返回值格式是否为dict, 默认True
        hashead: 如果isdict为Fasle, 返回的列表中是否包含列标题
        '''
        with self.connect_cur() as cur:
            if not param:
                cur.execute(sql)
            else:
                if not isinstance(param, (dict, tuple)):
                    param = tuple([param])
                cur.execute(sql, param)
            res = cur.fetchall()
            res = [self.format_timestamp(r, cur) for r in res]
            if res and isdict:
                ret = []
                xkeys = [i[0] for i in cur.description]
                for item in res:
                    ret.append(dict(zip(xkeys, item)))
            else:
                ret = res
                if hashead:
                    xkeys = [i[0] for i in cur.description]
                    ret.insert(0, xkeys)
            return ret

    @timesql
    def get(self, sql, param=None, isdict=True):
        '''sql查询，只返回一条
        sql: sql语句
        param: 传参
        isdict: 返回值是否是dict
        '''
        with self.connect_cur() as cur:
            if param:
                if not isinstance(param, (dict, tuple)):
                    param = tuple([param])
                cur.execute(sql, param)
            else:
                cur.execute(sql)
            res = cur.fetchone()
            res = self.format_timestamp(res, cur)
            if res and isdict:
                xkeys = [i[0] for i in cur.description]
                return dict(zip(xkeys, res))
            else:
                return res

    def format_timestamp(self, ret, cur):
        '''将字段以_time结尾的格式化成datetime'''
        if not ret:
            return ret
        index = []
        for d in cur.description:
            if d[0].endswith('_time'):
                index.append(cur.description.index(d))

        res = []
        for i, t in enumerate(ret):
            if i in index and isinstance(t, int):
                res.append(datetime.datetime.fromtimestamp(t))
            else:
                res.append(t)
        return res

    def escape(self, s):
        return s

    def value2sql(self, v):
        if isinstance(v, str):
            if v.startswith(('now()', 'md5(')):
                return v
            return "'%s'" % self.escape(v)
        elif isinstance(v, datetime.datetime) or isinstance(v, datetime.date):
            return "'%s'" % str(v)
        elif isinstance(v, DBFunc):
            return v.value
        else:
            if v is None:
                return 'NULL'
            return str(v)

    def exp2sql(self, key, op, value):
        item = '(`%s` %s ' % (key.strip('`').replace('.', '`.`'), op)
        if op == 'in':
            item += '(%s))' % ','.join([self.value2sql(x) for x in value])
        elif op == 'not in':
            item += '(%s))' % ','.join([self.value2sql(x) for x in value])
        elif op == 'between':
            item += ' %s and %s)' % (self.value2sql(
                value[0]), self.value2sql(value[1]))
        else:
            item += self.value2sql(value) + ')'
        return item

    def dict2sql(self, d, sp=','):
        '''字典可以是 {name:value} 形式，也可以是 {name:(operator, value)}'''
        x = []
        for k, v in d.items():
            if isinstance(v, tuple):
                x.append('%s' % self.exp2sql(k, v[0], v[1]))
            else:
                x.append('`%s`=%s' %
                         (k.strip(' `').replace('.', '`.`'), self.value2sql(v)))
        return sp.join(x)

    def dict2on(self, d, sp=' and '):
        x = []
        for k, v in d.items():
            x.append('`%s`=`%s`' % (k.strip(' `').replace(
                '.', '`.`'), v.strip(' `').replace('.', '`.`')))
        return sp.join(x)

    def dict2insert(self, d):
        keys = list(d.keys())
        keys.sort()
        vals = ['%s' % self.value2sql(d[k]) for k in keys]
        new_keys = ['`' + k.strip('`') + '`' for k in keys]
        return ','.join(new_keys), ','.join(vals)

    def fields2where(self, fields, where=None):
        if not where:
            where = {}
        for f in fields:
            if f.value == None or (f.value == '' and f.isnull == False):
                continue
            where[f.name] = (f.op, f.value)
        return where

    def format_table(self, table):
        '''调整table 支持加上 `` 并支持as'''
        # 如果有as
        table = table.strip(' `').replace(',', '`,`')
        index = table.find(' ')
        if ' ' in table:
            return '`%s`%s' % (table[:index], table[index:])
        else:
            return '`%s`' % table

    def insert(self, table, values, other=None):
        '''插入'''
        keys, vals = self.dict2insert(values)
        sql = "insert into %s(%s) values (%s)" % (
            self.format_table(table), keys, vals)
        if other:
            sql += ' ' + other
        return self.execute(sql)

    def insert_list(self, table, values_list, other=None):
        '''批量插入'''
        sql = 'insert into %s ' % self.format_table(table)
        sql_key = ''
        sql_value = []
        for values in values_list:
            keys, vals = self.dict2insert(values)
            sql_key = keys  # 正常key肯定是一样的
            sql_value.append('(%s)' % vals)
        sql += ' (' + sql_key + ') ' + 'values' + ','.join(sql_value)
        if other:
            sql += ' ' + other
        return self.execute(sql)

    def update(self, table, values, where=None, other=None):
        '''更新'''
        sql = "update %s set %s" % (
            self.format_table(table), self.dict2sql(values))
        if where:
            sql += " where %s" % self.dict2sql(where, ' and ')
        if other:
            sql += ' ' + other
        return self.execute(sql)

    def delete(self, table, where, other=None):
        '''删除'''
        sql = "delete from %s" % self.format_table(table)
        if where:
            sql += " where %s" % self.dict2sql(where, ' and ')
        if other:
            sql += ' ' + other
        return self.execute(sql)

    def select(self, table, where=None, fields='*', other=None, isdict=True):
        '''查询出一个列表'''
        sql = self.select_sql(table, where, fields, other)
        return self.query(sql, None, isdict=isdict)

    def select_one(self, table, where=None, fields='*', other=None, isdict=True):
        '''查询出一个'''
        if not other:
            other = ' limit 1'
        if 'limit' not in other:
            other += ' limit 1'
        sql = self.select_sql(table, where, fields, other)
        return self.get(sql, None, isdict=isdict)

    def get_one(self, table, where=None, fields='*', other=None, isdict=True):
        '''查询出一个, 不存在则报错, 如果fields只有一个字段, 则返回单个value'''
        res = self.select_one(table, where, fields, other, isdict)
        if not res:
            raise Exception(
                'no data get_one from the table(%s), where(%s), fields(%s), other(%s)' % 
                (table, where, fields, other))
        if (isinstance(fields, str) and fields not in ['*', ''] and fields.find(',') == -1
            ) or ( isinstance(fields, (list, tuple)) and len(fields)==1):
            if isdict:
                res = list(res.values())[0]
            else:
                res = res[0]
        return res

    def select_join(self, table1, table2, join_type='inner', on=None, where=None, fields='*', other=None, isdict=True):
        sql = self.select_join_sql(
            table1, table2, join_type, on, where, fields, other)
        return self.query(sql, None, isdict=isdict)

    def select_one_join(self, table1, table2, join_type='inner', on=None, where=None, fields='*', other=None,
                        isdict=True):
        if not other:
            other = ' limit 1'
        if 'limit' not in other:
            other += ' limit 1'

        sql = self.select_join_sql(
            table1, table2, join_type, on, where, fields, other)
        return self.get(sql, None, isdict=isdict)

    def get_one_join(self, table1, table2, join_type='inner', on=None, where=None, fields='*', other=None,
                        isdict=True):
        '''查询出一个, 不存在则报错, 如果fields只有一个字段, 则返回单个value'''
        res = self.select_one_join(table1, table2, join_type, on, where, fields, other, isdict)
        if not res:
            raise Exception(
                'no data get_one_join from the table1(%s), table2(%s), join_type(%s), on(%s), where(%s), fields(%s), other(%s)' % 
                (table1, table2, join_type, on, where, fields, other))
        if (isinstance(fields, str) and fields not in ['*', ''] and fields.find(',') == -1
            ) or ( isinstance(fields, (list, tuple)) and len(fields)==1):
            if isdict:
                res = list(res.values())[0]
            else:
                res = res[0]
        return res

    def select_sql(self, table, where=None, fields='*', other=None):
        if isinstance(fields, list) or isinstance(fields, tuple):
            fields = ','.join(fields)
        sql = "select %s from %s" % (fields, self.format_table(table))
        if where:
            sql += " where %s" % self.dict2sql(where, ' and ')
        if other:
            sql += ' ' + other
        return sql

    def select_join_sql(self, table1, table2, join_type='inner', on=None, where=None, fields='*', other=None):
        if isinstance(fields, list) or isinstance(fields, tuple):
            fields = ','.join(fields)
        sql = "select %s from %s %s join %s" % (
            fields, self.format_table(table1), join_type, self.format_table(table2))
        if on:
            sql += " on %s" % self.dict2on(on, ' and ')
        if where:
            sql += " where %s" % self.dict2sql(where, ' and ')
        if other:
            sql += ' ' + other
        return sql

    def select_page(self, sql, pagecur=1, pagesize=20, count_sql=None, maxid=-1, isdict=True):
        page = pager.db_pager(self, sql, pagecur, pagesize, count_sql, maxid)
        if isdict:
            page.todict()
        else:
            page.tolist()
        return page


class SimpleDBConnection(DBHelper):
    def __init__(self, creator, *args, **kwargs):
        self._con = None
        self._args, self._kwargs = args, kwargs
        try:
            self._creator = creator.connect
        except Exception as e:
            raise Exception('数据库连接器不可用')
        self._con = self._creator(*self._args, **self._kwargs)
        # 记录连接的数据库信息
        self._server_id = None
        self._conn_id = 0
        self.conn_info()

    def __enter__(self):
        """Enter the runtime context for the connection object."""
        return self

    def __exit__(self, *exc):
        """Exit the runtime context for the connection object.
        This does not close the connection, but it ends a transaction.
        """
        if exc[0] is None and exc[1] is None and exc[2] is None:
            self.commit()
        else:
            self.rollback()

    def conn_info(self):
        """获取数据库连接信息，便于问题追踪"""
        cur = self._con.cursor()
        cur.execute("show variables like 'server_id'")
        row = cur.fetchone()
        self._server_id = int(row[1])
        cur.close()

        cur = self._con.cursor()
        cur.execute("select connection_id()")
        row = cur.fetchone()
        self._conn_id = row[0]
        cur.close()


    def cursor(self, *args, **kwargs):
        return self._con.cursor(*args, **kwargs)

    def close(self):
        self._con.close()

    def begin(self, *args, **kwargs):
        begin = self._con.begin
        begin(*args, **kwargs)

    def commit(self):
        self._con.commit()

    def rollback(self):
        self._con.rollback()

    def cancel(self):
        cancel = self._con.cancel
        cancel()

    def ping(self, *args, **kwargs):
        return self._con.ping(*args, **kwargs)
    
    def escape(self, s):
        return self._con.escape_string(s)

    @contextmanager
    def connect_cur(self):
        cur = None
        try:
            cur = self.cursor()
            yield cur
            self.commit()
        except Exception as e:
            self.rollback()
            raise e
        finally:
            if cur is not None:
                cur.close()
