#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/16 13:31
# @Author  : CoderCharm
# @File    : auth.py
# @Software: PyCharm
# @Github  : github/CoderCharm
# @Email   : wg_python@163.com
# @Desc    :
"""
纯增删改查操作，写在model里面
"""
from utils.sqlite_db import SqliteDB


class User():
    """
    用户表
    """
    id = ''
    name = ''
    email = ''
    phone = ''
    password = ''
    type = ''

    @classmethod
    def single_by_id(cls, uid: str):
        db = SqliteDB()
        user = db.getOne(table="users", where=f"id = '{uid}'")
        return user

    @classmethod
    def single_by_phone(cls, phone: int = 0):
        db = SqliteDB()
        user = db.getOne(table="users", where="name = 'admin'")
        if user is None:
            user = {}
        return user

    @classmethod
    def fetch_all(cls, page: int = 1, page_size: int = 10):
        db = SqliteDB()
        user = db.getOne(table="users", where="name = 'admin'")
        if user is None:
            user = {}
        return user
