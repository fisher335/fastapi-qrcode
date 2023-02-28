from utils.sqlite_db import SqliteDB


def get_dev_list(params=None):

    with SqliteDB() as db:  # 从连接池中取出一个连接
        result = db.getAll(table='sm_dev')
    return result

if __name__ == "__main__":
    print(get_dev_list())
