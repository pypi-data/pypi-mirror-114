# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2020-04-16 14:38:22
@LastEditTime: 2021-07-28 11:15:56
@LastEditors: HuangJianYi
:Description: 基础路由
"""
# 框架引用
from seven_framework.web_tornado.monitor import MonitorHandler
from seven_cloudapp_frame.handlers.core import *
from seven_cloudapp_frame.handlers.server import *
from seven_cloudapp_frame.handlers.client import *

def seven_cloudapp_frame_route():
    return [
        (r"/monitor", MonitorHandler),
        (r"/", IndexHandler),
        #客户端
        (r"/client/address", address.AddressInfoListHandler),
        (r"/client/login", user.LoginHandler),
        (r"/client/authorize", user.AuthorizeHandler),
        (r"/client/apply_black_unbind", user.ApplyBlackUnbindHandler),
        (r"/client/user_asset_list", user.UserAssetListHandler),
        (r"/client/asset_log_list", user.AssetLogListHandler),
        (r"/client/theme_info", theme.ThemeInfoHandler),
        (r"/client/save_theme", theme.SaveThemeHandler),
        (r"/client/save_skin", theme.SaveSkinHandler),
        (r"/client/theme_info_list", theme.ThemeInfoListHandler),
        (r"/client/skin_info_list", theme.SkinInfoListHandler),

        #千牛端
        (r"/server/saas_custom", base_s.SaasCustomHandler),
        (r"/server/login", user_s.LoginHandler),
        (r"/server/send_sms", base_s.SendSmsHandler),
        (r"/server/stat_report_list", report_s.StatReportListHandler),
        (r"/server/trend_report_list", report_s.TrendReportListHandler),
        (r"/server/update_user_status", user_s.UpdateUserStatusHandler),
        (r"/server/update_user_status_by_black", user_s.UpdateUserStatusByBlackHandler),
        (r"/server/audit_user_black", user_s.AuditUserBlackHandler),
        (r"/server/user_black_list", user_s.UserBlackListHandler),
        (r"/server/update_user_asset", user_s.UpdateUserAssetHandler),
        (r"/server/asset_log_list", user_s.AssetLogListHandler),
    ]