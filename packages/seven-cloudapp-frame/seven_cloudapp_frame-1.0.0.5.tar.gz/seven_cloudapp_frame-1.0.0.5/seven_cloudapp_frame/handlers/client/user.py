# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-26 18:31:06
@LastEditTime: 2021-07-27 09:15:57
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.user_base_model import *
from seven_cloudapp_frame.models.stat_base_model import *

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

        app_info = self.get_app_info(app_id)
        if not app_info:
            return self.reponse_json_error("error","小程序不存在")

        if self.check_request_user(app_id, app_info["current_limit_count"]):
            return self.reponse_json_error("current_limit", "登录失败")

        invoke_result_data = InvokeResultData()
        user_base_model = UserBaseModel(context=self)
        user_base_model.get_or_add_user_by_openid(app_id, act_id, open_id, user_nick, avatar)
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
    @filter_check_params("act_id")
    def get_async(self):
        """
        :description: 更新用户信息
        :param avatar：头像
        :param act_id：活动id
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id
        user_nick = self.get_taobao_param().user_nick
        act_id = int(self.get_param("act_id", 0))
        avatar = self.get_param("avatar")

        invoke_result_data = InvokeResultData()
        user_base_model = UserBaseModel(context=self)
        invoke_result_data = user_base_model.update_user_by_openid(app_id, act_id, open_id, user_nick, avatar)
        if invoke_result_data.success == False:
            return self.reponse_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        else:
            return self.reponse_json_success("更新成功")
