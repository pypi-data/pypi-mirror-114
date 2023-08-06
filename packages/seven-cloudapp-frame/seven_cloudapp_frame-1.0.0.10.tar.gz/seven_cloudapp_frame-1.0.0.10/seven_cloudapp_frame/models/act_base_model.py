# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-28 09:54:51
@LastEditTime: 2021-07-28 15:08:52
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

    def _get_act_info_cache_key(self, act_id):
        """
        :description: 获取用户信息缓存key
        :param act_id: 活动标识
        :return: 
        :last_editors: HuangJianYi
        """
        return f"act_info:actid_{act_id}"

    def get_act_info_dict(self,act_id):
        """
        :description: 获取活动信息
        :param act_id: 活动标识
        :return: 返回应用信息
        :last_editors: HuangJianYi
        """
        act_info_dict = ActInfoModel(context=self.context).get_dict_by_id(act_id)
        if not act_info_dict or act_info_dict["is_release"] == 0 or act_info_dict["is_del"] == 1:
            return None
        return act_info_dict

    def get_act_info_dict_cache(self,act_id):
        """
        :description: 获取活动信息
        :param act_id: 活动标识
        :return: 返回应用信息
        :last_editors: HuangJianYi
        """
        redis_key = self._get_act_info_cache_key(act_id)
        redis_init = SevenHelper.redis_init()
        act_info_dict = redis_init.get(redis_key)
        if act_info_dict:
            act_info_dict = json.loads(act_info_dict)
        else:
            act_info_dict = self.get_act_info_dict(act_id)
            if act_info_dict:
                redis_init.set(redis_key, SevenHelper.json_dumps(act_info_dict), ex=config.get_value("cache_expire", 60 * 1))
        return act_info_dict
    