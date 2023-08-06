# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-28 09:54:51
@LastEditTime: 2021-07-30 09:36:47
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.db_models.act.act_info_model import *
from seven_cloudapp_frame.models.seven_model import *

class ActBaseModel():
    """
    :description: 活动信息基类
    """
    def __init__(self, context):
        self.context = context

    def _get_act_info_dependency_key(self, act_id):
        """
        :description: 获取用户信息缓存key
        :param act_id: 活动标识
        :return: 
        :last_editors: HuangJianYi
        """
        return f"act_info:actid_{act_id}"

    def get_act_info_dict(self,act_id,is_cache=True):
        """
        :description: 获取活动信息
        :param act_id: 活动标识
        :param is_cache: 是否缓存
        :return: 返回活动信息
        :last_editors: HuangJianYi
        """
        act_info_model = ActInfoModel(context=self.context)
        if is_cache:
            dependency_key = self._get_act_info_dependency_key(act_id)
            act_info_dict = act_info_model.get_cache_dict_by_id(act_id,dependency_key=dependency_key)
        else:
            act_info_dict = act_info_model.get_dict_by_id(act_id)
        if not act_info_dict or act_info_dict["is_release"] == 0 or act_info_dict["is_del"] == 1:
            return None
        return act_info_dict
    