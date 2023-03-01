# conding:utf-8
import base64
import os
import tempfile
from random import randint

import openai
import qrcode
import requests
from fastapi import APIRouter, Depends, Form, UploadFile
from fastapi import Request
from starlette import status
from starlette.responses import RedirectResponse, FileResponse
from starlette.templating import Jinja2Templates

import config.main
from common.main import get_template
from utils.ocr_util import OcrClient

# main的分路由
templates = Jinja2Templates(directory="router/templates")
main_app = APIRouter()


@main_app.get('/')
@main_app.get('/index')
@main_app.get('/qrcode/')
async def test(result: dict = Depends(get_template)):
    result['data'] = 'hello'
    return templates.TemplateResponse("index.html", result)


@main_app.get("/favicon.ico")
async def read_item():
    return RedirectResponse('/static/favicon.ico')


@main_app.get('/list/')
async def list_header(request: Request, result: dict = Depends(get_template)):
    result['session'] = request.headers
    return templates.TemplateResponse('list.html', result)


@main_app.get('/wiki/')
async def wiki(dic: dict = Depends(get_template)):
    return templates.TemplateResponse("wiki.html", dic)


@main_app.post('/wiki/')
async def wiki(url: str = Form(), dic: dict = Depends(get_template)):
    key  = config.main.AI_KEY
    r_key = base64.b64decode(key).decode("utf-8")
    openai.api_key = r_key
    response = openai.Image.create(prompt=url, n=1, size="1024x1024")
    image_url = response["data"][0]["url"]
    dic["path"] = image_url
    return templates.TemplateResponse("aipic.html", dic)


@main_app.post('/qrcode/')
async def qrcodelike(url: str = Form(), result: dict = Depends(get_template)):
    img_name = randint(1, 1000000)
    imge = qrcode.make(url)
    pa = 'static' + os.sep + 'qrcode' + os.sep + str(img_name) + ".png"
    print(pa)
    imge.save(pa)
    result['img'] = img_name
    return templates.TemplateResponse('qrcode.html', result)


@main_app.get('/upload/')
async def upload_get(dic: dict = Depends(get_template)):
    return templates.TemplateResponse('upload.html', dic)


@main_app.post('/upload/')
async def upload_post(file: UploadFile):
    file_name = file.filename
    print(file_name)
    file_path = 'static' + os.sep + 'videos' + os.sep + file_name
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return RedirectResponse(url='/file/', status_code=status.HTTP_302_FOUND)


@main_app.get('/file/')
async def file_list(dic=Depends(get_template)):
    li_file = []
    video_path = 'static' + os.sep + 'videos'
    for path, dir, file in os.walk(video_path):
        for i in file:
            li_file.append(i)
    dic['files'] = li_file
    return templates.TemplateResponse('file.html', dic)


@main_app.get('/download/{filename}/')
def download_file(filename):
    video_path = 'static' + os.sep + 'qrcode' + os.sep + filename
    print(filename)
    respons = FileResponse(video_path, filename=filename)
    return respons


@main_app.get('/downloadfile/{filename}/')
def download_file(filename):
    video_path = 'static' + os.sep + 'videos' + os.sep + filename
    print(filename)
    respons = FileResponse(video_path, filename=filename)
    return respons


@main_app.get('/zhuang/')
def dazhuang(dic: dict = Depends(get_template)):
    return templates.TemplateResponse('zhuang.html', dic)


@main_app.route('/ip/')
def get_ip():
    my_ip = requests.get('http://jsonip.com').json()['ip']
    return my_ip


@main_app.get('/ocr/')
def ocr_get(dic: dict = Depends(get_template)):
    return templates.TemplateResponse('ocr.html', dic)


@main_app.post('/ocr/')
def ocr_post(file: UploadFile,dic = Depends(get_template)):
    file_name = file.filename
    tempfile_path = tempfile.gettempdir()
    file_tmp_path = os.path.join(tempfile_path, file_name)
    with open(file_tmp_path, 'wb') as f:
        f.write(file.file.read())
    oc = OcrClient()
    dic['content'] = str(oc.simple_ocr(file_tmp_path))
    return templates.TemplateResponse("ocr.html",dic)


@main_app.get('/invoice/')
def invoice_get(dic: dict = Depends(get_template)):
    return templates.TemplateResponse('invoice.html', dic)


@main_app.post('/invoice/')
def invoice_post(file: UploadFile):
    file_name = file.filename
    tempfile_path = tempfile.gettempdir()
    file_tmp_path = os.path.join(tempfile_path, file_name)
    with open(file_tmp_path, 'wb') as f:
        f.write(file.file.read())
    oc = OcrClient()
    return str(oc.fapiao(file_tmp_path))
