import json
import uuid

import paramiko
from fastapi import APIRouter
from fastapi.params import Body
from starlette.websockets import WebSocket, WebSocketDisconnect

from model.ResData import responseData
from model.WebSocket import ConnectionManager
from service.ScanService import normalScan, creatWays, checkWays

scan_app = APIRouter()


@scan_app.post("/scan")
async def read_item(scan_type: str = Body(default="normal", embed=True, alias="type")):
    li = []
    if scan_type == "快速扫描":
        li = normalScan()
    data = {"list": li}
    return responseData.ok(data)


@scan_app.post("/creatWays")
async def read_item(router: list[dict] = Body(default='', embed=True)):
    router = [{'ip': '172.16.120.228'}, {'ip': '172.16.120.253'}, {'ip': '172.16.120.246'}]
    li = []
    for i in router:
        i['id'] = str(uuid.uuid4())
        li.append(i)
    print(li)
    r = creatWays(li)

    data = {"list": r}
    print(data)
    return responseData.ok(data)


@scan_app.post("/checkWays")
async def read_item(router1: str = Body(default='', embed=True),
                    router2: str = Body(default='', embed=True),
                    router3: str = Body(default='', embed=True)
                    ):
    li = [router1, router2, router3]
    data = {}
    if checkWays():
        data = {"list": '测试通过'}
    else:
        data = {"list": '测试-通过'}
    return responseData.ok(data)


@scan_app.websocket("/shell/{dev_id}")
async def websocket_endpoint(websocket: WebSocket, dev_id: str):
    manager = ConnectionManager()
    await manager.connect(websocket)
    await manager.send_personal_message([f"设备172.16.120.228连接成功！！!"], websocket)

    # await manager.broadcast(f"用户{dev_id}进入聊天室")

    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message([f"你输入了: {data}"], websocket)
            # 创建SSHClient 实例对象
            ssh = paramiko.SSHClient()
            # 调用方法，表示没有存储远程机器的公钥，允许访问
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接远程机器，地址，端口，用户名密码
            ssh.connect("172.16.120.228", 22, 'root', '123456', timeout=20)
            # 输入linux命令
            # ls = "cat /proc/cpuinfo"
            stdin, stdout, stderr = ssh.exec_command(data, get_pty=True, timeout=20)

            # 输出命令执行结果
            # 关闭连接
            while True:
                try:
                    nextline = stdout.readline().strip()  # 读取脚本输出内容
                    # 发送消息到客户端
                    await manager.send_personal_message(nextline, websocket)
                    print("已发送消息:%s" % nextline)
                    # 判断消息为空时,退出循环
                    if not nextline:
                        break
                except Exception as e:
                    print(e)
                    await manager.send_personal_message("运行服务器出错，请刷新", websocket)
            ssh.close()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"用户-{dev_id}-离开")
