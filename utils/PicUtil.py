#coding:utf-8
from utils.DBUtil import db

@db
def get_art(cur):
    cur.execute("select * from blog_article")
    rows = cur.fetchall()
    print(rows)



if __name__ == '__main__':
    get_art()