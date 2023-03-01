# coding:utf-8
from datetime import timedelta
from typing import Dict, Any

from faker import Faker
from fastapi import APIRouter, Body, Depends
from fastapi.params import Form

import config.main
from common.jwt import create_access_token
from common.jwt import get_current_user
from common.response_data import responseData
from service.UserService import *

# 用户的分路由


user_app = APIRouter()


@user_app.post("/login")
async def login(username: str = Form(...),
                password: str = Form(...)):
    user = checkPWD(username, password)
    if user:
        access_token_expires = timedelta(minutes=config.main.ACCESS_TOKEN_EXPIRE_MINUTES)
        # 登录token 存储了user.id
        token = create_access_token(username, expires_delta=access_token_expires),
        menus = getMenus(user.get('type', '普通用户'))
        data = {'token': token, 'meuns': menus, 'routers': "/home_/users_/user/info_/test"}
        return responseData.ok(data)
    else:

        return responseData.fail('密码验证错误')


@user_app.post("/list", response_model=responseData)
def get_list(paras: Dict[str, Any], page: int = Body(..., embed=True), pageSize: int = Body(..., embed=True)):
    print(page, pageSize, paras)
    faker = Faker()
    user_list = get_users(paras)
    start = (page - 1) * pageSize
    end = page * pageSize
    data = {"list": user_list[start:end], "currentPage": page, "total": len(user_list), "pageSize": pageSize}
    return responseData.ok(data)


@user_app.get("/who")
def get_current_user(user=Depends(get_current_user)):
    payload = user
    # du = model_to_dict(user)
    # print(du)
    return responseData.ok(payload)
