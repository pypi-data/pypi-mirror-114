# -*- coding: utf-8 -*-

import os
import sys
import random

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

import grpc
from jiexi_client.grpc_docx import docx_grpc_pb2, docx_grpc_pb2_grpc


def lazyproperty(f):
    """
    @lazyprop decorator. Decorated method will be called only on first access
    to calculate a cached property value. After that, the cached value is
    returned.
    """
    cache_attr_name = "_%s" % f.__name__  # like '_foobar' for prop 'foobar'
    docstring = f.__doc__

    def get_prop_value(obj):
        try:
            return getattr(obj, cache_attr_name)
        except AttributeError:
            value = f(obj)
            setattr(obj, cache_attr_name, value)
            return value

    return property(get_prop_value, doc=docstring)


class Client(object):
    _instance = None

    def __new__(cls, invoker_config, debug=True):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, invoker_config, debug=True):
        self.client_ip = random.choice(invoker_config.get("host"))
        self.port = invoker_config.get("port")
        self.err = None
        self.volume_id = None
        self.cms_id = None
        self.channel = None  # client channel thread safe

    @lazyproperty
    def init_channel(self):
        address = self.client_ip + ":" + str(self.port)
        channel = grpc.insecure_channel(address)
        self.channel = channel

        stub = docx_grpc_pb2_grpc.DocxServiceStub(channel)
        return stub

    def init_content(self, path, subject):
        # 检查参数以及初始化数据
        self.path = path
        self.check_arg(path)
        try:
            res = open(path, mode="rb")
        except Exception as e:
            self.err = e
            return path, None
        return res.read(), subject

    def send(self, path, subject):
        stub = self.init_channel
        content, subject = self.init_content(path, subject)
        response = stub.GetMsg(docx_grpc_pb2.MsgRequest(name=content, subject=subject))
        return response

    def check_arg(self, path):
        # 后续实现
        pass

    def main(self, path, subject):
        res = self.send(path, subject)
        return res.msg

    def close(self):
        if self.channel is not None:
            self.channel.close()

