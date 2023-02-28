import time

import paramiko


class MySSH(object):
    def __init__(self, ip="172.16.120.228", username="root", password="123456", port=22):
        self.__transport = None
        self.conn = None
        if ip:
            self.ip = ip.strip()
        else:
            raise ValueError("需要设备连接地址（ip 或 别名）")
        self.port = int(port)
        self.username = username
        self.password = password

    def __enter__(self):
        """初始化 SSH 连接，调起一个模拟终端，会话结束前可以一直执行命令。
        Raises:
            e: 抛出 paramiko 连接失败的任何异常
        """
        ssh_connect_params = {
            "hostname": self.ip,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "look_for_keys": False,
            "allow_agent": False,
            "timeout": 5,  # TCP 连接超时时间
        }
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            conn.connect(**ssh_connect_params)
        except Exception as e:
            raise e
        self.conn = conn.invoke_shell(term="vt100", width=500, height=1000)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('{}设备上的命令运行结束'.format(self.ip))
        self.conn.close()
        return True

    def exec_cmd(self, cmd, recv_time=3):
        """登录设备，执行命令

        Args:
            cmd ([type]): 命令字符串
            recv_time (int, optional): 读取回显信息的超时时间. Defaults to 3.

        Raises:
            EOFError: 没有任何信息输出，说明连接失败。

        Returns:
            output: 
        """
        cmd = cmd.strip() + "\n"
        self.conn.sendall(cmd)
        time.sleep(int(recv_time))
        output = self.conn.recv(1024 * 1024)
        if len(output) == 0:
            raise EOFError("连接可能被关闭，没有任何信息输出")
        return output.decode('utf-8')

    def upload_file(self, localpath, remotepath):

        self.__transport = paramiko.Transport((self.ip, self.port))
        self.__transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(self.__transport)

        # 实例化一个 sftp对象,指定连接的通道
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 发送文件
        sftp.put(localpath=localpath, remotepath=remotepath)
        # 下载文件
        # sftp.get(remotepath, localpath)
        self.__transport.close()

    def download(self, local_path, remote_path):
        self.__transport = paramiko.Transport((self.ip, self.port))
        self.__transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(self.__transport)

        # 实例化一个 sftp对象,指定连接的通道
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path, local_path)


if __name__ == '__main__':
    with MySSH() as client:
        r = client.exec_cmd('''cd ~/work/config_v2ray ''')
        re = client.exec_cmd(
            '''echo '123456' | sudo -S ./config_v2ray.py  -node_type=first -next_ip='172.16.120.253' -next_port=6688 -next_uuid='3918201f-af82-d659-2e69-b4408b6e417c'  ''')
        if 'True' in re:
            print()
