import sys
import os
import shutil
from subprocess import Popen, PIPE

file_path = os.path.abspath(os.path.dirname(__file__))

if os.path.exists("{}/conf.py".format(file_path)):

    from serverD.conf import *
else:
    from serverD.conf_demo import *

    shutil.copy("{}/conf_demo.py".format(file_path), "{}/conf.py".format(file_path))

server_base_data = {

    "serverPut": "{user} {host} {pwd} {port} {locPath} {serPath}",
    "serverGet": "{user} {host} {pwd} {port} {locPath} {serPath}",
    "serverLogin": "{user} {host} {pwd} {port}",
    "serverTbj": "{user} {host} {pwd} {port} {pem}",

}


class ServerD:

    @staticmethod
    def serverB(s_type, s_data):
        cmd = '{}/serverE/{} {}'.format(file_path, s_type, s_data)
        print(cmd)
        os.system(cmd)

    def login(self, server_name):
        s_type = "serverLogin"
        if not isinstance(server_name, str):
            server_name = "{}".format(server_name)
        login_dict = server_dict.get(server_name)
        if not login_dict:
            print("{} 不存在".format(server_name))
            exit(1)
        s_data = server_base_data.get(s_type).format(**login_dict)
        self.serverB(s_type, s_data)

    def get(self, server_name, locPath, serPath, root=False):
        s_type = "serverGet"
        if not isinstance(server_name, str):
            server_name = "{}".format(server_name)
        get_dict = server_dict.get(server_name)
        if not get_dict:
            print("{} 不存在".format(server_name))
            exit(1)
        if root:
            get_dict.update({"locPath": locPath, "serPath": serPath, "user": 'root', "pwd": root_pwd})
        else:
            get_dict.update({"locPath": locPath, "serPath": serPath})
        s_data = server_base_data.get(s_type).format(**get_dict)
        self.serverB(s_type, s_data)

    def put(self, server_name, locPath, serPath, root=False):
        s_type = "serverPut"
        if not isinstance(server_name, str):
            server_name = "{}".format(server_name)
        get_dict = server_dict.get(server_name)
        if not get_dict:
            print("{} 不存在".format(server_name))
            exit(1)
        if root:
            get_dict.update({"locPath": locPath, "serPath": serPath, "user": 'root', "pwd": root_pwd})
        else:
            get_dict.update({"locPath": locPath, "serPath": serPath})
        s_data = server_base_data.get(s_type).format(**get_dict)
        self.serverB(s_type, s_data)

    def loginRoot(self, server_name):
        s_type = "serverLogin"
        if not isinstance(server_name, str):
            server_name = "{}".format(server_name)
        login_dict = server_dict.get(server_name)
        if not login_dict:
            print("{} 不存在".format(server_name))
            exit(1)
        login_dict["user"] = "root"
        login_dict["pwd"] = root_pwd
        s_data = server_base_data.get(s_type).format(**login_dict)
        self.serverB(s_type, s_data)

    def loginTbj(self, pwd):
        """
        :param server_name:
        :return:
        """
        s_type = "serverTbj"
        login_dict = server_dict.get("tbj")
        login_dict["pwd"] = pwd
        s_data = server_base_data.get(s_type).format(**login_dict)
        self.serverB(s_type, s_data)

    def main(self, server):
        try:
            if server:
                if server == "tbj":
                    try:
                        self.loginTbj(sys.argv[2])
                    except IndexError:
                        print("请输入正确格式: go tbj password")
                elif server == "root":
                    try:
                        self.loginRoot(sys.argv[2])
                    except IndexError:
                        print("请输入正确格式 go root server: 如: go root 429")

                elif server == "get":
                    try:
                        if sys.argv[1] == "root":
                            server_name = sys.argv[2]
                            serPath = sys.argv[3]
                            locPath = sys.argv[4]
                            self.get(server_name, locPath, serPath, root=True)
                        else:
                            server_name = sys.argv[1]
                            serPath = sys.argv[2]
                            locPath = sys.argv[3]
                            self.get(server_name, locPath, serPath)
                    except IndexError:
                        print("输入参数错误!!!\n正确示例 >>> get [root] <服务器名称> <服务器文件路径> <本地文件路径>")

                elif server == "put":
                    try:
                        if sys.argv[1] == "root":
                            server_name = sys.argv[2]
                            serPath = sys.argv[3]
                            locPath = sys.argv[4]
                            self.put(server_name, locPath, serPath, root=True)
                        else:
                            server_name = sys.argv[1]
                            serPath = sys.argv[2]
                            locPath = sys.argv[3]
                            self.put(server_name, locPath, serPath)
                    except IndexError:
                        print("输入参数错误!!!\n正确示例 >>> put [root] <服务器名称> <服务器文件路径> <本地文件路径>")

                else:
                    server_name = "{}".format(server)
                    print("正在登录{}...".format(server_name))
                    self.login(server_name)
            else:
                print("请输入服务器编号")
        except IndexError:
            print("输入参数错误!!!\n正确示例 >>>  go [登录类型] <服务器名称> ")


def main():
    try:
        base_server = sys.argv[1]
        sd = ServerD()
        sd.main(base_server)
    except IndexError:
        print("参数异常: 正确格式如下:{}{}".format("go <服务器名称>\n",
                                         "go root <服务器名称>\n",
                                         "go tbj <密码>\n",
                                         "put <服务器名称> <服务器文件路径> <本地文件路径>\n",
                                         "get <服务器名称> <服务器文件路径> <本地文件路径>\n",
                                         ))


def get():
    try:
        base_server = "get"
        sd = ServerD()
        sd.main(base_server)
    except IndexError:
        print("参数异常: 正确格式如下:{}{}".format(
            "go <服务器名称>\n",
            "go root <服务器名称>\n",
            "go tbj <密码>\n",
            "put <服务器名称> <服务器文件路径> <本地文件路径>\n",
            "get <服务器名称> <服务器文件路径> <本地文件路径>\n",
        ))


def put():
    try:
        base_server = "put"
        sd = ServerD()
        sd.main(base_server)
    except IndexError:
        print("参数异常: 正确格式如下:{}{}".format(
            "go <服务器名称>\n",
            "go root <服务器名称>\n",
            "go tbj <密码>\n",
            "put <服务器名称> <服务器文件路径> <本地文件路径>\n",
            "get <服务器名称> <服务器文件路径> <本地文件路径>\n",
        ))


def update_conf():
    try:
        new_conf_path = sys.argv[1]
        if os.path.exists(new_conf_path):
            shutil.copy(new_conf_path, "{}/conf.py".format(file_path))
        else:
            print("该文件不存在: {}".format(new_conf_path))
    except IndexError:
        print("updates <当前配置文件路径>\n 查看 可执行 vi {}/conf.py ".format(file_path))


def open_conf():
    """打开配置文件"""
    p = Popen("cat {}/conf.py".format(file_path), stdout=PIPE, shell=True)

    for i in p.stdout.readlines():
        ps_str = str(i, encoding="utf-8")
        print(ps_str, end='')
    print()


def alter_conf():
    """修改配置文件"""
    try:

        if not any([user, port, pwd, root_pwd, tbj_pem]):
            print("请录入默认配置")
            user1 = "{}".format(input("用户名:"))  # 用户名
            port1 = "{}".format(input("端口号:"))  # 端口号
            pwd1 = "{}".format(input("密码:"))  # 普通密码
            root_pwd1 = "{}".format(input("root密码:"))  # root 密码
            tbj_pem1 = "{}".format(input("跳板机序列号:"))
        else:
            user1 = user  # 用户名
            port1 = port  # 端口号
            pwd1 = pwd  # 普通密码
            root_pwd1 = root_pwd  # root 密码
            tbj_pem1 = tbj_pem

        if len(sys.argv) == 2:
            conf_sname = sys.argv[1]
            conf_param = ''
            conf_data = ''
        else:
            conf_sname = sys.argv[1]
            conf_param = sys.argv[2]
            conf_data = sys.argv[3]
        if conf_param == "sname":
            server_dict[conf_data] = server_dict[conf_sname]
            del server_dict[conf_sname]
        elif conf_sname in server_dict and len(sys.argv) > 2:
            server_dict[conf_sname][conf_param] = conf_data
        else:

            host = input("请录入服务器信息\n host:")
            new_user = input("user:(若默认{}请回车键跳过)".format(user1))
            new_port = input("port:(若默认{}请回车键跳过)".format(port1))
            new_pwd = input("pwd:(若默认{}请回车键跳过)".format(pwd1))
            new_tbj_pem = input("tbj_pem:(若默认{}请回车键跳过)".format(tbj_pem1))
            server_dict[conf_sname] = {"host": host, "user": new_user, "port": new_port, "pwd": new_pwd,
                                       "pem": new_tbj_pem}
        new_server_conf_str = '''
        user = "{}"  # 用户名
        port = "{}"  # 端口号
        pwd = "{}"  # 普通密码
        root_pwd = "{}"  # root 密码
        tbj_pem = "{}"  # 跳板机序号\n\nserver_dict = {}'''.format(user1, port1, pwd1, root_pwd1, tbj_pem1,
                                                              str(server_dict)).replace(" " * 8, "").replace("},",
                                                                                                             "},\n")
        with open("{}/conf.py".format(file_path), 'w') as f:
            f.write(new_server_conf_str)

    except IndexError:
        print("执行命令为: alters 服务器名称 (sname|host|user|port|pwd) 具体的值  alters 服务器名称")


if __name__ == '__main__':
    main()
