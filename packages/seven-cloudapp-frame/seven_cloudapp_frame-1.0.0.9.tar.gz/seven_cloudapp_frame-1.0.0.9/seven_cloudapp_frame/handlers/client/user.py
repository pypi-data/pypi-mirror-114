# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-26 18:31:06
@LastEditTime: 2021-07-28 15:47:11
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.user_base_model import *
from seven_cloudapp_frame.models.stat_base_model import *
from seven_cloudapp_frame.models.app_base_model import *
from seven_cloudapp_frame.models.asset_base_model import *


class LoginHandler(TaoBaseHandler):
    """
    :description: 登录处理
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        :description: 登录处理
        :param act_id:活动id
        :return: dict
        :last_editors: HuangJianYi
        """
        act_id = int(self.get_param("act_id", 0))
        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id
        user_nick = self.get_taobao_param().user_nick
        avatar = self.get_param("avatar")

        app_base_model = AppBaseModel(context=self)
        app_info_dict = app_base_model.get_app_info_dict_cache(app_id)
        if not app_info_dict:
            return self.reponse_json_error("error","小程序不存在")

        if self.check_request_user(app_id, app_info_dict["current_limit_count"]):
            return self.reponse_json_error("current_limit", "登录失败")

        user_base_model = UserBaseModel(context=self)
        invoke_result_data = user_base_model.save_user_by_openid(app_id, act_id, open_id, user_nick, avatar)
        if invoke_result_data.success == False:
            return self.reponse_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        user_info_dict = invoke_result_data.data
        stat_base_model = StatBaseModel(context=self)
        key_list_dict = {}
        key_list_dict["VisitCountEveryDay"] = 1
        key_list_dict["VisitManCountEveryDay"] = 1
        key_list_dict["VisitManCountEveryDayIncrease"] = 1
        stat_base_model.add_stat_list(app_id, act_id, user_info_dict["user_id"], open_id, key_list_dict)
        return self.reponse_json_success(invoke_result_data.data)

class AuthorizeHandler(TaoBaseHandler):
    """
    :description: 授权更新用户信息
    """
    @filter_check_params("act_id,user_id")
    def get_async(self):
        """
        :description: 更新用户信息
        :param avatar：头像
        :param act_id：活动id
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_taobao_param().source_app_id
        user_id = int(self.get_param("user_id", 0))
        open_id = self.get_taobao_param().open_id
        user_nick = self.get_taobao_param().user_nick
        act_id = int(self.get_param("act_id", 0))
        avatar = self.get_param("avatar")

        invoke_result_data = InvokeResultData()
        user_base_model = UserBaseModel(context=self)
        invoke_result_data = user_base_model.update_user_info(app_id, act_id, user_id, open_id, user_nick, avatar)
        if invoke_result_data.success == False:
            return self.reponse_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        else:
            return self.reponse_json_success("更新成功")

class ApplyBlackUnbindHandler(TaoBaseHandler):
    """
    :description: 提交黑名单解封申请
    """
    @filter_check_params("act_id,user_id")
    def get_async(self):
        """
        :description: 提交黑名单解封申请
        :param {act_id:活动id}
        :param {reason:解封理由}
        :return {*}
        :last_editors: HuangJianYi
        """
        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id
        user_id = int(self.get_param("user_id", 0))
        act_id = int(self.get_param("act_id", 0))
        reason = self.get_param("reason", "误封号,申请解封")

        invoke_result_data = InvokeResultData()
        user_base_model = UserBaseModel(context=self)
        invoke_result_data = user_base_model.apply_black_unbind(app_id, act_id, user_id,open_id,reason)
        if invoke_result_data.success == False:
            return self.reponse_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        else:
            return self.reponse_json_success()

class UserAssetListHandler(TaoBaseHandler):
    """
    :description: 获取用户资产列表
    """
    @filter_check_params("act_id,user_id")
    def get_async(self):
        """
        :description: 获取用户资产列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param user_id：用户标识
        :return list
        :last_editors: HuangJianYi
        """
        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id
        act_id = int(self.get_param("act_id", 0))
        user_id = int(self.get_param("user_id", 0))

        asset_base_model = AssetBaseModel(context=self)
        return self.reponse_json_success(asset_base_model.get_user_asset_list(app_id, act_id, user_id, open_id))

class AssetLogListHandler(TaoBaseHandler):
    """
    :description: 资产流水记录
    """
    @filter_check_params("act_id,user_id,asset_type")
    def get_async(self):
        """
        :description: 资产流水记录
        :param app_id：应用标识
        :param act_id：活动标识
        :param user_id：用户标识
        :param open_id：open_id
        :param user_nick：昵称
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :param asset_object_id：资产对象标识
        :param page_size：条数
        :param page_index：页数
        :return list
        :last_editors: HuangJianYi
        """
        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id
        user_nick = self.get_taobao_param().user_nick
        act_id = int(self.get_param("act_id", 0))
        user_id = int(self.get_param("user_id", 0))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))
        asset_type = int(self.get_param("asset_type", 0))
        asset_object_id = self.get_param("asset_object_id")

        asset_base_model = AssetBaseModel(context=self)
        return self.reponse_json_success(asset_base_model.get_asset_log_list(app_id, act_id, asset_type, page_size, page_index, user_id, asset_object_id, "", "", user_nick, open_id, 0, ""))