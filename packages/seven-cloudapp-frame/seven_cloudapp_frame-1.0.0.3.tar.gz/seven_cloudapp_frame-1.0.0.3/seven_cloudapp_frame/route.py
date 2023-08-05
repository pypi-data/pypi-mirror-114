# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2020-04-16 14:38:22
@LastEditTime: 2021-07-23 09:25:28
@LastEditors: HuangJianYi
:Description: 基础路由
"""
# 框架引用
from seven_cloudapp_frame.handlers.core import *
from seven_cloudapp_frame.handlers.server import *
from seven_cloudapp_frame.handlers.client import *

def seven_cloudapp_frame_route():
    return [
        (r"/monitor", MonitorHandler),
        (r"/", IndexHandler),
        (r"/client/address", address.GetAddressInfoListHandler),
    ]