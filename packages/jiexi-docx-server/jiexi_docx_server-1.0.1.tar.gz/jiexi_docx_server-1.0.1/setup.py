# coding=utf-8
from setuptools import find_packages, setup

requires = [
    "requests~=2.25.1",
    "six~=1.16.0",
]

client_dir = "jiexi_client"

setup(
    name="jiexi_docx_server",
    version="1.0.1",
    author="sirun.wang",
    author_email="870355373@qq.com",
    description="解析菁优网docx试卷",
    keywords="17content_render",
    packages=[f"{client_dir}.{c}" for c in find_packages(where=client_dir)]
    + [client_dir],
    include_package_data=True,
    install_requires=requires,
)
