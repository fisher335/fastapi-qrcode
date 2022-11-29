# coding=utf-8
import time

from nmap import nmap

from common.dplog.dplog import Logger as log
from utils.SSHUtil import MySSH


def normalScan():
    nm = nmap.PortScanner()
    re = nm.scan('172.16.120.55', '22,80,88', arguments="--traceroute")
    log.info(re)
    result = []
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    for host, status in hosts_list:
        log.info(host + ":" + status)
        _d = {'host': host, "status": status}
        result.append(_d)
    return result


def creatWays(li: list[dict]):
    result = ''
    for i in range(len(li)):
        if i == 0:
            with MySSH(ip=li[i].get("ip")) as client:
                print(li[i].get("ip") + '开始进行登录')
                r = client.exec_cmd('''cd /home/liuj/work/config_v2ray''')
                re = client.exec_cmd(
                    '''./config_v2ray.py  -node_type=first -next_ip={}  -next_uuid='{}'  '''.format(
                        li[i + 1].get("ip"), li[i + 1].get('id')))
                print('---------------'+re+'1111111111111111111111111111')
                if 'True' in re:
                    result += '{}设备设置成功'.format(li[i].get('ip')) + '\r\n'
        if 0 < i < (len(li) - 1):
            with MySSH(ip=li[i].get('ip')) as client:
                print(li[i].get('ip') + '开始进行登录')
                r = client.exec_cmd('''cd /home/liuj/work/config_v2ray ''')
                re = client.exec_cmd(
                    '''echo '123456' | sudo -S ./config_v2ray.py  -node_type=middle -next_ip='{}'  
                    -next_uuid='{}}' -cur_uuid='3918201f-af82-d659-2e69-b4408b6e417c' '''.format(
                        (li[i + 1].get("ip"), li[i + 1].get('id'))))
                # if 'True' in re:
                if True:
                    result += ('{}设备设置成功'.format(li[i].get('ip')) + '\r\n')

        if i == (len(li) - 1):
            print(li[i].get('ip') + '开始进行登录')
            with MySSH(ip=li[i].get('ip')) as client:
                r = client.exec_cmd('''cd ~/work/config_v2ray ''')
                re = client.exec_cmd(
                    '''echo '123456' | sudo -S ./config_v2ray.py  -node_type=last -cur_uuid='{}}'   '''.format(
                        li[i + 1].get('id')))
                print(re)
                result += '{}设备设置成功'.format(li[i].get('ip')) + '\r\n'
    return result


def checkWays():
    # with MySSH(ip='172.16.120.228', username='liuj', password='123456') as client:
    #     _a = client.exec_cmd('curl --socks4 127.0.0.1:1082  www.baidu.com')
    #     print(a)
    # if '百度' in _a:
    time.sleep(4)
    if True:
        return True


if __name__ == '__main__':
    li = ['172.16.120.228', '172.16.120.253', '172.16.120.246']
    a = creatWays(li)
    print(a)
