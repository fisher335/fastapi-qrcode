# coding:utf-8

from fastapi import APIRouter, Body

from model.ResData import responseData
from service.DevService import get_dev_list
from service.FileService import getMinIOFileList, downloadFile

dev_app = APIRouter()


@dev_app.post("/list", tags=["设备清单"])
async def read_item(page: int = 1, pageSize: int = 10):
    fileList = sorted(get_dev_list(), key=lambda file: file.get("id"))
    print(get_dev_list())
    start = (page - 1) * pageSize
    end = page * pageSize
    filesPage = fileList[start:end]
    data = {"list": filesPage, "currentPage": page, "total": len(fileList), "pageSize": pageSize}
    return responseData.ok(data)


@dev_app.post("/add", tags=["MinIO文件"])
async def read_item(name: str = Body(..., embed=True)):
    downloadURL = downloadFile(name)
    return responseData.ok(downloadURL)
