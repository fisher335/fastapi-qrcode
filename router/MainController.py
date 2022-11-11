# conding:utf-8
import os
import urllib
from typing import Optional

from fastapi import APIRouter, Request, Body, Response, UploadFile, File, Depends

from starlette.responses import FileResponse, RedirectResponse
from service.FileService import get_localfile_list

# main的分路由


main_app = APIRouter()


@main_app.get('/test')  # 解码成功后返回用户id
async def test():
    return {'result': 'ok'}


@main_app.get("/favicon.ico")
async def read_item():
    a = RedirectResponse('/static/favicon.ico')
    return a


@main_app.get('/home/loadData')
def getLoadData():
    return 'hello java'
