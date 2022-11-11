# coding:utf-8
from starlette.requests import Request

from common.jwt import check_jwt_token
from config.Config import WHITE_URL, ALLOW_LIST, USER_LIST
from utils.SqliteDB import SqliteDB


def user_check(user: str, pwd: str) -> bool:
    flag = False
    for i in USER_LIST:
        pw = i.get(user)
        if pw == pwd:
            flag = True
    return flag


#  检查用户名和密码
def checkPWD(name: str, pwd: str):
    db = SqliteDB()
    password = db.getOne(table="users", where=f"id ={name} ")
    if password.strip() == pwd.strip():
        return True
    else:
        return False


def checkToken(request: Request):
    # 拦截访问token
    hs = request.headers
    token = hs.get("Authorization")
    # print(request.url.path)
    flag = False
    # // 先判断是否在白名单中
    if request.url.path in WHITE_URL:
        flag = True
    try:
        user = check_jwt_token(token)
        if user.get('sub', None) in ALLOW_LIST:
            flag = True
    except:
        pass
    return flag


def getMenus():
    home = [{
        'icon': 'el-icon-setting',
        'index': '/home',
        'title': '首页',
        'subs': None
    }, {
        'icon': 'el-icon-menu',
        'index': '2',
        'title': '用户管理',
        'subs': [
            {
                'icon': None,
                'index': '/users',
                'title': '用户列表',
                'subs': None
            },
            {
                'icon': None,
                'index': '/user/info',
                'title': '用户信息',
                'subs': None
            }
        ]
    }, {
        "icon": 'el-icon-setting',
        "index": '/scaner',
        "title": '扫描设备'
    },
        {
            "icon": 'el-icon-setting',
            "index": '/shell',
            "title": 'webShell'
        }
        , {
            "icon": 'el-icon-setting',
            "index": '/vis',
            "title": '拓扑结构'
        }, {
            "icon": 'el-icon-setting',
            "index": '/tongdao',
            "title": '构建通道'
        }, {
            "icon": 'el-icon-setting',
            "index": '/luyou',
            "title": '设备管理'
        }, {
            "icon": 'el-icon-setting',
            "index": '/test',
            "title": '测试管理'
        }, {
            "icon": 'el-icon-setting',
            "index": '/ddc',
            "title": '文件管理'
        }]

    return home
