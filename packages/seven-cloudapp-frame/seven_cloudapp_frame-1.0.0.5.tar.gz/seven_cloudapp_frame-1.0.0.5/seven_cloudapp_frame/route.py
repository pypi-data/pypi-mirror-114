# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2020-04-16 14:38:22
@LastEditTime: 2021-07-26 20:13:14
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
        #客户端
        (r"/client/address", address.GetAddressInfoListHandler),
        (r"/client/login", user.LoginHandler),
        (r"/client/authorize", user.AuthorizeHandler),

        #千牛端
        (r"/server/saas_custom", base_s.SaasCustomHandler),
        (r"/server/send_sms", base_s.SendSmsHandler),
        (r"/server/get_stat_report_list", report_s.GetStatReportListHandler),
        (r"/server/get_trend_report_list", report_s.GetTrendReportListHandler),
    ]