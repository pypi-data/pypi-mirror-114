import os

from setuptools import setup, find_packages


def gen_data_files(*dirs):
    """打包不规则格式数据"""
    results = []

    for src_dir in dirs:
        for root,dirs,files in os.walk(src_dir):
            results.append((root, map(lambda f:root + "/" + f, files)))
    return results


setup(
    name="serverD",
    version="0.1.7",
    description="快速的服务器登录, 上传, 下载",
    long_description="快速的服务器登录, 上传, 下载",
    url="https://github.com/pansj66/serverD",
    author="shijiang Pan",
    author_email="1377161366@qq.com",
    license="MIT Licence",
    packages=find_packages(include=[
        "serverD", "serverD.*",  # 需要的依赖

    ]),
    #
    # packages=find_packages(include=[
    #     "serverD", "serverD.*",
    #     "serverE", "serverE.*",
    # ]),
    include_package_data=True,

    data_files=gen_data_files("serverD/serverE"),  # 打包不规则程序, 包含的文件夹
    platforms=["all"],

    entry_points={
        'console_scripts': [  # 添加的系统中的命令
            "go = serverD.main:main",  # 需要运行的脚本及方法
            "get = serverD.main:get",
            "put = serverD.main:put",
            "updates = serverD.main:update_conf",
            "alters = serverD.main:alter_conf",
            "opens = serverD.main:open_conf",
        ]
    },

)

# print(gen_data_files("serverD/serverE"))
