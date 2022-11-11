# coding=utf-8
from utils.SSHUtil import SSHClient

a = SSHClient(host='172.16.120.228', port=22, username='liuj', password='123456')
a.connect()
# a.write('cd ~/work/config_v2ray')
c = a.read(
    "sudo -S ./config_v2ray.py  -node_type=first -next_ip={} -next_port=6688 -next_uuid='3918201f-af82-d659-2e69-b4408b6e417c' ")
print(c)