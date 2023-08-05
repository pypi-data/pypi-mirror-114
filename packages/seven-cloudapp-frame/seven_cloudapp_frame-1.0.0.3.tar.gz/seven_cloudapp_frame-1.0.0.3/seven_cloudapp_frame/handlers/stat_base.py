# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-26 09:39:08
@LastEditTime: 2021-07-26 14:18:08
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.libs.customize.seven_helper import *

from seven_cloudapp_frame.models.db_models.stat.stat_queue_model import *


class StatBase():
    """
    :description: 统计上报基类
    """
    def __init__(self, context):
        self.context = context

    def add_stat(self, app_id, act_id, module_id, user_id, open_id, key_name, key_value, sub_table=None):
        """
        :description: 添加上报
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param user_id：用户标识
        :param open_id：open_id
        :param key_name：统计key
        :param key_value：统计value
        :param sub_table：分表名称（是否分表由业务方决定）
        :return:
        :last_editors: HuangJianYi
        """
        stat_queue_model = StatQueueModel(sub_table=sub_table, context=self.context)

        stat_queue = StatQueue()
        stat_queue.app_id = app_id
        stat_queue.act_id = act_id
        stat_queue.module_id = module_id
        stat_queue.user_id = user_id
        stat_queue.open_id = open_id
        stat_queue.key_name = key_name
        stat_queue.key_value = key_value
        stat_queue.create_date = SevenHelper.get_now_datetime()
        stat_queue.process_date = SevenHelper.get_now_datetime()
        return stat_queue_model.add_entity(stat_queue)

    def add_stat_list(self, app_id, act_id, module_id, user_id, open_id, key_list_dict, sub_table=None):
        """
        :description: 添加上报
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param user_id：用户标识
        :param open_id：open_id
        :param key_list_dict:键值对字典
        :param sub_table：分表名称（是否分表由业务方决定）
        :return:
        :last_editors: HuangJianYi
        """
        stat_queue_model = StatQueueModel(sub_table=sub_table, context=self.context)
        stat_queue_list = []
        for key,value in key_list_dict.items():
            stat_queue = StatQueue()
            stat_queue.app_id = app_id
            stat_queue.act_id = act_id
            stat_queue.module_id = module_id
            stat_queue.user_id = user_id
            stat_queue.open_id = open_id
            stat_queue.key_name = key
            stat_queue.key_value = value
            stat_queue.create_date = SevenHelper.get_now_datetime()
            stat_queue.process_date = SevenHelper.get_now_datetime()
            stat_queue_list.add(stat_queue)
        return stat_queue_model.add_list(stat_queue_list)
