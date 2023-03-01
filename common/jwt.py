#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/16 11:51
# @Author  : CoderCharm
# @File    : jwt.py
# @Software: PyCharm
# @Github  : github/CoderCharm
# @Email   : wg_python@163.com
# @Desc    :
"""

一些通用的依赖功能

"""

from datetime import timedelta, datetime
from typing import Any, Union, Optional

from fastapi import Header
#
from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from model.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    生成token
    :param subject:需要存储到token的数据(注意token里面的数据，属于公开的)
    :param expires_delta:
    :return:
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    :param plain_password: 原密码
    :param hashed_password: hash后的密码
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    获取 hash 后的密码
    :param password:
    :return:
    """
    return pwd_context.hash(password)


def check_jwt_token(
        token: Optional[str]
) -> Union[str, Any]:
    """
    解析验证token  默认验证headers里面为token字段的数据
    可以给 headers 里面token替换别名, 以下示例为 X-Token
    token: Optional[str] = Header(None, alias="X-Token")
    :param token:
    :return:
    """

    try:
        payload = jwt.decode(
            token,
            Config.SECRET_KEY, algorithms=[Config.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise custom_exc.TokenExpired()
    except (jwt.JWTError, ValidationError, AttributeError):
        raise custom_exc.TokenAuthError()


def get_current_user(Authorization=Header()) -> User:
    """
    根据header中token 获取当前用户
    :param Authorization: 头部header中的token
    :return:
    """

    playload = check_jwt_token(Authorization)
    # 从数据库查找用户信息
    # user = User.single_by_id(uid=playload.get("sub"))
    user = User()
    user.name = playload.get("sub")
    if not user:
        raise custom_exc.TokenAuthError(err_desc="User not found")
    return user
