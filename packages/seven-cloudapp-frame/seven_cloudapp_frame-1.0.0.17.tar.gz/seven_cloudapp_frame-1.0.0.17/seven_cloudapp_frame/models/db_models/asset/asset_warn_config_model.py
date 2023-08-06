# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-19 11:06:25
@LastEditTime: 2021-07-29 18:29:27
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *


class AssetWarnConfigModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None):
        super(AssetWarnConfigModel, self).__init__(AssetWarnConfig, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类

class AssetWarnConfig:

    def __init__(self):
        super(AssetWarnConfig, self).__init__()
        self.id = 0  # id
        self.app_id = ""  # 应用标识
        self.act_id = 0  # 活动标识
        self.notice_object_ids = ""  # 通知人对象(多个逗号分隔)
        self.notice_phones = ""  # 通知人手机号(多个逗号分隔)
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 更新时间

    @classmethod
    def get_field_list(self):
        return ['id', 'app_id', 'act_id', 'notice_object_ids', 'notice_phones', 'create_date', 'modify_date']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "asset_warn_config_tb"
