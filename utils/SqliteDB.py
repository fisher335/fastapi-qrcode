# -*- coding: utf-8 -*-
import sqlite3

from dbutils.persistent_db import PersistentDB


class Pool(object):  # 数据库连接池
    __pool = None  # 记录第一个被创建的对象引用
    config = {
        'database': '../sms.db'  # 数据库文件路径
    }

    def __new__(cls, *args, **kwargs):
        """创建连接池对象  单例设计模式(每个线程中只创建一个连接池对象)  PersistentDB为每个线程提供专用的连接池"""
        if cls.__pool is None:  # 如果__pool为空，说明创建的是第一个连接池对象
            cls.__pool = PersistentDB(sqlite3, maxusage=None, closeable=False, **cls.config)
        return cls.__pool


def dict_factory(cursor, row):
    # 将游标获取的数据处理成字典返回
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SqliteDB:

    def __init__(self, database="./sms.db", dict_out=True):
        try:
            self.conn = sqlite3.connect(database)
            # 字典形式放回
            if dict_out:
                self.conn.row_factory = dict_factory
            # 创建一个cursor：
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)

    def __enter__(self):
        """自动从连接池中取出一个连接"""
        db_pool = Pool()
        self.conn = db_pool.connection()
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """自动释放当前连接资源 归还给连接池"""
        self.cur.close()
        self.conn.close()

    # 返回执行execute()方法后影响的行数
    def execute(self, sql):
        self.cursor.execute(sql)
        rowcount = self.cursor.rowcount
        return rowcount

    # 删除并返回影响行数
    def delete(self, **kwargs):
        table = kwargs['table']
        where = kwargs['where']
        whereStr = ""
        if where is not None:
            whereStr = where
        sql = f"delete from {table} where {whereStr};"
        try:
            # print(sql)
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
        except:
            # 发生错误时回滚
            self.conn.rollback()
        return self.cursor.rowcount

    # 新增并返回新增ID
    def insert(self, **kwargs):
        table = kwargs['table']
        del kwargs['table']
        sql = 'insert into %s(' % table
        fields = ""
        values = ""
        for k, v in kwargs.items():
            fields += "%s," % k
            values += "'%s'," % v
        fields = fields.rstrip(',')
        values = values.rstrip(',')
        sql = sql + fields + ")values(" + values + ")"
        print(sql)
        res = []
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            # 获取自增id
            res = self.cursor.lastrowid
        except:
            # 发生错误时回滚
            self.conn.rollback()
        return res

    # 修改数据并返回影响的行数

    def update(self, **kwargs):
        table = kwargs['table']
        # del kwargs['table']
        kwargs.pop('table')
        where = kwargs['where']
        kwargs.pop('where')
        sql = 'update %s set ' % table
        for k, v in kwargs.items():
            sql += "%s='%s'," % (k, v)
        sql = sql.rstrip(',')
        sql += ' where %s' % where
        print(sql)
        rowcount = 0
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            # 影响的行数
            rowcount = self.cursor.rowcount
        except:
            # 发生错误时回滚
            self.conn.rollback()
        return rowcount

    # 查-一条条数据
    def getOne(self, **kwargs):
        table = kwargs['table']
        field = 'field' in kwargs and kwargs['field'] or '*'
        where = 'where' in kwargs and 'where ' + kwargs['where'] or ''
        order = 'order' in kwargs and 'order by ' + kwargs['order'] or ''
        sql = 'select %s from %s %s %s limit 1' % (field, table, where, order)
        print(sql)
        data = []
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            data = self.cursor.fetchall()[0]
        except:
            # 发生错误时回滚
            self.conn.rollback()
        return data

    # 查所有数据
    def getAll(self, **kwargs):
        table = kwargs['table']
        field = 'field' in kwargs and kwargs['field'] or '*'
        where = 'where' in kwargs and 'where ' + kwargs['where'] or ''
        order = 'order' in kwargs and 'order by ' + kwargs['order'] or ''
        sql = 'select %s from %s %s %s ' % (field, table, where, order)
        print(sql)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            data = self.cursor.fetchall()
            return list(data)
        except:
            # 发生错误时回滚
            self.conn.rollback()
            return []

    def createtb(self, sql=None, table=None, drop=None):

        if table is None:
            print("table参数不能为空")
            return False

        # 强制清空
        if drop is not None:
            self.droptb(table)

        # 查看表格是否已经存在
        self.cursor.execute(f"SELECT COUNT(*) FROM sqlite_master where type='table' and name='{table}'")
        values = self.cursor.fetchall()
        existtb = values[0][0]

        if existtb == 0:
            # 执行一条SQL语句：创建user表 'CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name VARCHAR)'
            self.cursor.execute(sql)

        return self.cursor.rowcount

    def droptb(self, table=None):
        if table is None:
            print("表格不能为空")
            return False
        self.cursor.execute(f"drop table if exists {table};")
        return self.cursor.rowcount

    def __del__(self):
        self.conn.close()  # 关闭连接


if __name__ == '__main__':
    db = SqliteDB()
    # sql = "CREATE TABLE asin (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, asin VARCHAR, status VARCHAR, title VARCHAR, cover VARCHAR, stars double, lreviewdate VARCHAR, description VARCHAR, url VARCHAR, atime timestamp NULL DEFAULT NULL, mtime timestamp NULL DEFAULT NULL, price double, flag INTEGER DEFAULT 0, reviewcount INTEGER DEFAULT 0)"
    # sql = "CREATE TABLE keyword (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, keyword VARCHAR, flag INTEGER DEFAULT 0, isrelate INTEGER DEFAULT 0, locked INTEGER DEFAULT 0, );"
    # sql = "CREATE TABLE pre_asin (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, asin VARCHAR, status VARCHAR, title VARCHAR, cover VARCHAR, stars double, lreviewdate VARCHAR, description VARCHAR, url VARCHAR, atime timestamp NULL DEFAULT NULL, mtime timestamp NULL DEFAULT NULL, price double, flag INTEGER DEFAULT 0, reviewcount INTEGER DEFAULT 0)"
    # res = db.createtb(sql=sql,table='asin')
    # print(res)

    # asin = ''
    # for i in range(5):
    #     asin += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    #
    # # insert测试
    # cs = db.insert(table="asin", asin=asin, title="标题"+str(random.randint(100,999)), stars=4.3)
    # print(cs)

    # delete 测试
    # cs = db.delete(table="asin", where="id=6")
    # print(cs)

    # update 测试
    # cs = db.update(table="asin", title="8888", stars=4.9, where="id=2")
    # print(cs)

    # select 测试
    cs = db.getOne(table="users", where='''id = "admin" ''')
    print(cs)
