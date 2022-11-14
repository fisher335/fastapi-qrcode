from dbutils.persistent_db import PersistentDB
import sqlite3


class Pool(object):  # 数据库连接池
    __pool = None  # 记录第一个被创建的对象引用
    config = {
        'database': './sms.db'  # 数据库文件路径
    }

    def __new__(cls, *args, **kwargs):
        """创建连接池对象  单例设计模式(每个线程中只创建一个连接池对象)  PersistentDB为每个线程提供专用的连接池"""
        if cls.__pool is None:  # 如果__pool为空，说明创建的是第一个连接池对象
            cls.__pool = PersistentDB(sqlite3, maxusage=None, closeable=False, **cls.config)
        return cls.__pool


class Connect:
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


# # 查询一条数据
# def find_one(table, data):
#     sql = 'select * from ' + table + ' where ip=?'
#     with Connect() as db:  # 从连接池中取出一个连接
#         db.cur.execute(sql, (data,))  # sqlite用元组接受字符串
#         result = db.cur.fetchone()
#     return result[0]
#
#
# # 插入一条数据
# def insert_one(table, data):
#     sql = 'insert or ignore into ' + table + '(ip) values(?)'  # 不重复插入
#     with Connect() as db:
#         db.cur.execute(sql, (data,))
#         db.conn.commit()
#
#
# # 删除一条数据
# def delete_one(table, data):
#     sql = 'delete from ' + table + ' where ip=?'
#     with Connect() as db:
#         db.cur.execute(sql, (data,))
#         db.conn.commit()


"""
SQLite 由于线程安全机制 不支持 PooledDB 线程共享连接模式   故使用PersistentDB 线程专用连接模式 为每个线程单独开连接池
SQLite 只支持读并发 即:写独占，读共享，所以要在修改操作时使用互斥锁。 为了体现精简性，这里就不演示了
PooledDB()中的参数解释自行查找
"""


