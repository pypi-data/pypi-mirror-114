# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2021-07-15 14:09:43
@LastEditTime: 2021-07-22 18:40:09
@LastEditors: HuangJianYi
:description: 通用Handler
"""
from seven_framework.config import *
from seven_framework.redis import *
from seven_framework.web_tornado.base_handler.base_api_handler import *

from seven_cloudapp_frame.handlers.frame_base import *


class IndexHandler(FrameBaseHandler):
    """
    :description: 默认页
    """
    def get_async(self):
        """
        :description: 默认页
        :param 
        :return 字符串
        :last_editors: HuangJingCan
        """
        self.write(UUIDHelper.get_uuid() + "_" + config.get_value("run_port") + "_api")

class MonitorHandler(BaseApiHandler):
    
    def get_async(self):
        """
        :description: 通用监控处理
        :last_editors: ChenXiaolei
        """
        config_monitor = app_config
        # 遍历配置,监控状态
        for key, value in config_monitor.items():
            if type(value) != dict:
                continue
            # Check MYSQL
            if key.find("db") > -1:
                try:
                    MySQLHelper(value).connection()
                except:
                    self.write(f"Mysql监控异常:{traceback.format_exc()}")
                    return
            # Check Redis
            elif key.find("redis") > -1:
                now_time = str(time.time)
                try:
                    monitor_key = f"framework_monitor_{config_monitor['run_port']}"

                    redis_client = RedisHelper.redis_init(config_dict=value)

                    redis_client.set(monitor_key, now_time)

                    if redis_client.get(monitor_key).decode() != now_time:
                        self.write("Reids监控异常,数据存在存取延迟")
                        return
                except:
                    self.write(f"Redis监控异常:{traceback.format_exc()}")
                    return
        self.write("ok")