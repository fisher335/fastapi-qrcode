import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from common.register import register_tortoise
from config.main import SERVER_CONFIG, TORTOISE_ORM
from router.DevController import dev_app
from router.MainController import main_app
from router.UserController import user_app

app = FastAPI(title='快速调用接口', description='验证项目', version='1.0.0', docs_url='/docs', redoc_url='/redocs', )

# 拦截器的例子
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # 拦截访问token
    # flag = checkToken(request)
    # 对校验进行判断
    # if not flag:
    #     response = Response("not allowed user")
    #     response.status_code = status.HTTP_401_UNAUTHORIZED
    #     return response
    response = await call_next(request)
    return response


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://192.168.0.18:8000",

]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_app, prefix="", tags=["其他接口"])
app.include_router(user_app, prefix="/user", tags=["用户相关"])
app.include_router(dev_app, prefix="/dev", tags=["设备相关"])
app.mount("/static", StaticFiles(directory="static"), name="static")
# register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)
if __name__ == '__main__':
    # nacos_app.start()
    uvicorn.run(app='run:app', host="0.0.0.0", port=8088, workers=2,loop="asyncio",reload = True,log_level = "warning")
    # uvicorn.run(app='run:app', host="127.0.0.1", port=SERVER_CONFIG['port'],  debug=True, log_level="debug")
