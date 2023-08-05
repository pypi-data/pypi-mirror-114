# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
from typing import Any, List, Optional

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from jiexi_client.client.client import Client


class JiexiDocx(object):
    """
    菁优网docx文件解析试题入库服务,只针对oto题型的转换
    """

    def __init__(self, env="TEST", timeout=50, port=50053):
        if env == "TEST":
            debug = True
            host = ["10.7.18.151"]
        else:
            host = ["10.7.18.188"]
            debug = False
        invoker_config = self.adapt_invoker_config(host, timeout, port)
        self.invoker = Client(invoker_config, debug=debug)

    @staticmethod
    def adapt_invoker_config(host, timeout, port):
        host = filter(None, host)
        invoker_config = {"host": list(host), "port": port, "timeout": timeout}
        return invoker_config

    def jiexi_docx(self, path, subject):
        """
        @description: 解析试卷服务
        @param {path: docx文件的本地地址, subject: docx文件所属的学科}
        @return
        """
        arg_dict = locals()
        del arg_dict["self"]
        res = self.invoker.main(path, subject=subject)
        return res


if __name__ == "__main__":
    ceshi = JiexiDocx(env="TEST")
    res = ceshi.jiexi_docx(
        path="/Users/sirun.wang/Library/Containers/com.tencent.WeWorkMac/Data/Documents/Profiles/F58E330DA43BCD14B0C9BCF79C0A8225/Caches/Files/2021-04/a267bc45342c755ee182333fbb095ca7/RES_000203380919初中语文.docx",
        subject="chinese",
    )
    print(res)
