# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-28 09:54:51
@LastEditTime: 2021-07-30 09:40:26
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

    def _get_app_info_dependency_key(self, app_id):
        """
        :description: 获取应用信息缓存key
        :param app_id: 应用标识
        :return: 
        :last_editors: HuangJianYi
        """
        return f"app_info:appid_{app_id}"

    def get_app_info_dict(self,app_id,is_cache=True):
        """
        :description: 获取应用信息
        :param app_id: 应用标识
        :param is_cache: 是否缓存
        :return: 返回应用信息
        :last_editors: HuangJianYi
        """
        app_info_model = AppInfoModel(context=self)
        if is_cache:
            dependency_key = self._get_app_info_dependency_key(app_id)
            return app_info_model.get_cache_dict(dependency_key=dependency_key,where="app_id=%s", params=[app_id])
        else:
            return app_info_model.get_dict(where="app_id=%s", params=[app_id])