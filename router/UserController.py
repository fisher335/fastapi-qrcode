# coding:utf-8
from datetime import timedelta

from faker import Faker
from fastapi import APIRouter, Body, Depends
from fastapi.params import Form

from common.jwt import get_current_user
from config import Config
from model.ResData import responseData

from service.UserService import user_check, getMenus
from common.jwt import create_access_token

# 用户的分路由


user_app = APIRouter()


@user_app.post("/login")
async def login(username: str = Form(...),
                password: str = Form(...)):
    if user_check(username, password):
        access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
        # 登录token 存储了user.id
        token = create_access_token(username, expires_delta=access_token_expires),
        menus = getMenus()
        data = {'token': token, 'meuns': menus, 'routers': "/home_/users_/user/info_/test"}
        return responseData.ok(data)
    else:

        return responseData.fail('密码验证错误')


@user_app.post("/list", response_model=responseData)
def read_item(page: str = Body(..., embed=True), pageSize: str = Body(..., embed=True),
              name: str = Body(..., embed=True), address: str = Body(..., embed=True)):
    print(page, pageSize, name, address)
    faker = Faker()
    user_list = []
    for i in range(10):
        u = {'id': 112 + i, 'name': "测试姓名" + str(i), 'address': faker.address(),
             'date': faker.time(pattern="%H:%M:%S", end_datetime=None)}
        user_list.append(u)
    data = {"list": user_list, "currentPage": 1, "total": 19, "pageSize": 1}

    return responseData.ok(data)


@user_app.get("/who")
def get_current_user(user=Depends(get_current_user)):
    payload = user
    # du = model_to_dict(user)
    # print(du)
    return responseData.ok(payload)
