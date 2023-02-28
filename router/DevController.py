# coding:utf-8

from fastapi import APIRouter, Body

from common.response_data import responseData
from service.DevService import get_dev_list


dev_app = APIRouter()


@dev_app.post("/list")
async def get_list(page: int = 1, pageSize: int = 10):
    fileList = sorted(get_dev_list(), key=lambda file: file.get("id"))
    print(get_dev_list())
    start = (page - 1) * pageSize
    end = page * pageSize
    filesPage = fileList[start:end]
    data = {"list": filesPage, "currentPage": page, "total": len(fileList), "pageSize": pageSize}
    return responseData.ok(data)

