# coding:utf-8

from fastapi import APIRouter, Body

from model.ResData import responseData
from service.FileService import getMinIOFileList, downloadFile

file_app = APIRouter()


@file_app.get("/list", tags=["MinIO文件"])
async def read_item(page: int = 1, pageSize: int = 10):
    fileList = sorted(getMinIOFileList(), key=lambda file: file.date)
    start = (page - 1) * pageSize
    end = page * pageSize
    filesPage = fileList[start:end]
    data = {"list": filesPage, "currentPage": page, "total": len(fileList), "pageSize": pageSize}
    return responseData.ok(data)


@file_app.post("/download", tags=["MinIO文件"])
async def read_item(name: str = Body(..., embed=True)):
    downloadURL = downloadFile(name)
    return responseData.ok(downloadURL)
