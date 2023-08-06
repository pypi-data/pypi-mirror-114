# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-28 09:54:51
@LastEditTime: 2021-07-28 15:46:29
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.db_models.app.app_info_model import *
from seven_cloudapp_frame.models.seven_model import *

class AppBaseModel():
    """
    :description: 应用信息基类
    """
    def __init__(self, context):
        self.context = context

    def _get_app_info_cache_key(self, app_id):
        """
        :description: 获取应用信息缓存key
        :param app_id: 应用标识
        :return: 
        :last_editors: HuangJianYi
        """
        return f"app_info:appid_{app_id}"

    def get_app_info_dict(self,app_id):
        """
        :description: 获取应用信息
        :param app_id: 应用标识
        :return: 返回应用信息
        :last_editors: HuangJianYi
        """
        return AppInfoModel(context=self).get_dict("app_id=%s", params=[app_id])
    
    def get_app_info_dict_cache(self,app_id):
        """
        :description: 获取应用信息
        :param app_id: 应用标识
        :return: 返回应用信息
        :last_editors: HuangJianYi
        """
        redis_key = self._get_app_info_cache_key(app_id)
        redis_init = SevenHelper.redis_init()
        app_info_dict = redis_init.get(redis_key)
        if app_info_dict:
            app_info_dict = json.loads(app_info_dict)
        else:
            app_info_dict = self.get_app_info_dict(app_id)
            if app_info_dict:
                redis_init.set(redis_key, SevenHelper.json_dumps(app_info_dict), ex=config.get_value("cache_expire", 60 * 1))
        return app_info_dict