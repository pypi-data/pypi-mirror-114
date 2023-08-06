# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-26 15:44:04
@LastEditTime: 2021-07-28 15:34:21
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.db_models.theme.theme_info_model import *
from seven_cloudapp_frame.models.db_models.theme.theme_ver_model import *
from seven_cloudapp_frame.models.db_models.skin.skin_info_model import *



class ThemeBaseModel():
    """
    :description: 主题皮肤基类
    """
    def __init__(self, context):
        self.context = context

    def get_theme_info(self,theme_id, ver_no):
        """
        :description: 获取主题信息
        :param act_id：活动标识
        :param theme_id：主题标识
        :param ver_no：客户端版本号
        :return: 返回主题信息
        :last_editors: HuangJianYi
        """

        theme_info_model = ThemeInfoModel(context=self.context)
        theme_info_dict = theme_info_model.get_dict_by_id(theme_id)
        if not theme_info_dict:
            return theme_info_dict
        out_id = theme_info_dict["out_id"]
        if ver_no:
            theme_ver = ThemeVerModel(context=self).get_dict("out_id=%s and ver_no=%s", params=[out_id, ver_no])
            if theme_ver and theme_ver["client_json"] != "":
                theme_info_dict["client_json"] = theme_ver["client_json"]
        skin_info_list = SkinInfoModel(context=self).get_dict_list("theme_id=%s", params=theme_id)
        theme_info_dict["skin_list"] = skin_info_list
        return theme_info_dict
    
    def get_theme_info_cache(self,theme_id, ver_no):
        """
        :description: 获取主题信息
        :param act_id：活动标识
        :param theme_id：主题标识
        :param ver_no：客户端版本号
        :return: 返回主题信息
        :last_editors: HuangJianYi
        """
        redis_key = f"theme_info:themeid_{theme_id}_verno_{ver_no}"
        redis_init = SevenHelper.redis_init()
        theme_info_dict = redis_init.get(redis_key)
        if theme_info_dict:
            theme_info_dict = json.loads(theme_info_dict)
        else:
            theme_info_dict = self.get_theme_info(theme_id, ver_no)
            if theme_info_dict:
                redis_init.set(redis_key, SevenHelper.json_dumps(theme_info_dict), ex=config.get_value("cache_expire", 60 * 1))
        return theme_info_dict

    def get_theme_list(self,app_id):
        """
        :description: 获取主题列表
        :param app_id：应用标识
        :return: 获取主题列表
        :last_editors: HuangJianYi
        """
        dict_list = ThemeInfoModel(context=self).get_dict_list("(app_id=%s or app_id='') and is_release=1", params=[app_id])
        for dict_info in dict_list:
            dict_info["client_json"] = self.json_loads(dict_info["client_json"]) if dict_info["client_json"] else {}
            dict_info["server_json"] = self.json_loads(dict_info["server_json"]) if dict_info["server_json"] else {}
        return dict_list
    
    def get_theme_list_cache(self,app_id):
        """
        :description: 获取主题列表
        :param app_id：应用标识
        :return: 获取主题列表
        :last_editors: HuangJianYi
        """
        redis_key = f"theme_list:appid_{app_id}"
        redis_init = SevenHelper.redis_init()
        theme_list = redis_init.get(redis_key)
        if theme_list:
            theme_list = json.loads(theme_list)
        else:
            theme_list = self.get_theme_list(app_id)
            if theme_list:
                redis_init.set(redis_key, SevenHelper.json_dumps(theme_list), ex=config.get_value("cache_expire", 60 * 1))
        return theme_list

    def get_skin_list(self, theme_id=0, theme_out_id=""):
        """
        :description: 获取皮肤列表
        :param theme_id：主题标识
        :param theme_out_id：外部主题标识
        :return: 获取主题列表
        :last_editors: HuangJianYi
        """
        condition = ""
        params = []
        if not theme_id or not theme_out_id:
            return []

        if theme_id:
            condition = "theme_id=%s"
            params.append(theme_id)
        if theme_out_id:
            if condition:
                condition+=" and "
            condition += " theme_out_id=%s"
            params.append(theme_out_id)

        dict_list = SkinInfoModel(context=self).get_dict_list(condition, params=params)
        for dict_info in dict_list:
            dict_info["client_json"] = self.json_loads(dict_info["client_json"]) if dict_info["client_json"] else {}
            dict_info["server_json"] = self.json_loads(dict_info["server_json"]) if dict_info["server_json"] else {}
        return dict_list

    def get_skin_list_cache(self, theme_id=0, theme_out_id=""):
        """
        :description: 获取皮肤列表
        :param theme_id：主题标识
        :param theme_out_id：外部主题标识
        :return: 获取主题列表
        :last_editors: HuangJianYi
        """
        redis_key = f"skin_list:themeid_{theme_id}_themeoutid_{theme_out_id}"
        redis_init = SevenHelper.redis_init()
        theme_list = redis_init.get(redis_key)
        if theme_list:
            theme_list = json.loads(theme_list)
        else:
            theme_list = self.get_skin_list(theme_id,theme_out_id)
            if theme_list:
                redis_init.set(redis_key, SevenHelper.json_dumps(theme_list), ex=config.get_value("cache_expire", 60 * 1))
        return theme_list

    def save_theme(self, app_id, theme_name, client_json, server_json, out_id, ver_no):
        """
        :description: 添加或修改主题
        :param app_id：app_id
        :param theme_name：主题名称
        :param client_json：客户端内容json
        :param server_json：服务端内容json
        :param out_id：外部id
        :param ver_no：客户端版本号
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if not out_id:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数不能为空或等于0"
            return invoke_result_data

        theme_info_model = ThemeInfoModel(context=self)
        theme_ver_model = ThemeVerModel(context=self)
        theme_info = theme_info_model.get_entity("out_id=%s", params=[out_id])
        if theme_info:
            if client_json:
                if ver_no:
                    theme_ver = theme_ver_model.get_entity('out_id=%s and ver_no=%s', params=[out_id, ver_no])
                    if theme_ver:
                        theme_ver_model.update_table('client_json=%s', 'out_id=%s and ver_no=%s', params=[client_json, out_id, ver_no])
                    else:
                        theme_ver = ThemeVer()
                        theme_ver.app_id = theme_info.app_id
                        theme_ver.out_id = out_id
                        theme_ver.theme_id = theme_info.id
                        theme_ver.client_json = client_json
                        theme_ver.ver_no = ver_no
                        theme_ver.create_date = theme_info.create_date
                        theme_ver_model.add_entity(theme_ver)
                else:
                    theme_info_model.update_table('client_json=%s', 'out_id=%s', params=[client_json, out_id])
            if server_json:
                theme_info_model.update_table('server_json=%s', 'out_id=%s', params=[server_json, out_id])
        else:
            theme_total = theme_info_model.get_total()
            if not theme_name:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "主题名称不能为空"
                return invoke_result_data
            theme_info = ThemeInfo()
            theme_info.theme_name = theme_name
            theme_info.client_json = client_json
            theme_info.server_json = server_json
            theme_info.out_id = out_id
            if app_id != "":
                theme_info.app_id = app_id
                theme_info.is_private = 1
            theme_info.sort_index = int(theme_total) + 1
            theme_info.is_release = 1
            theme_info.create_date = self.get_now_datetime()
            theme_id = theme_info_model.add_entity(theme_info)
            if ver_no:
                theme_ver = ThemeVer()
                theme_ver.app_id = theme_info.app_id
                theme_ver.out_id = out_id
                theme_ver.theme_id = theme_id
                theme_ver.client_json = client_json
                theme_ver.ver_no = ver_no
                theme_ver.create_date = theme_info.create_date
                theme_ver_model.add_entity(theme_ver)

        return invoke_result_data

    def save_skin(self, app_id, skin_name, client_json, server_json, theme_out_id, skin_out_id):
        """
        :description: 保存皮肤
        :param app_id：应用标识
        :param skin_name：皮肤名称
        :param client_json：客户端内容json
        :param server_json：服务端内容json
        :param theme_out_id：样式外部id
        :param skin_out_id：皮肤外部id
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if not skin_out_id:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数不能为空或等于0"
            return invoke_result_data
        skin_info_model = SkinInfoModel(context=self)
        skin_info = skin_info_model.get_entity("out_id=%s", params=[skin_out_id])
        if skin_info:
            if client_json:
                skin_info_model.update_table('client_json=%s', 'out_id=%s', params=[client_json, skin_out_id])
            if server_json:
                skin_info_model.update_table('server_json=%s', 'out_id=%s', params=[server_json, skin_out_id])
        else:
            skin_info_total = skin_info_model.get_total('theme_out_id=%s', params=theme_out_id)
            if not skin_name:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "皮肤名称不能为空"
                return invoke_result_data
            theme_info_model = ThemeInfoModel(context=self)
            theme_info = theme_info_model.get_entity("out_id=%s", params=theme_out_id)
            if not theme_info:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "没有找到对应主题"
                return invoke_result_data
            skin_info = SkinInfo()
            skin_info.skin_name = skin_name
            skin_info.client_json = client_json
            skin_info.server_json = server_json
            if app_id != "":
                skin_info.app_id = app_id
            skin_info.sort_index = skin_info_total + 1
            skin_info.theme_id = theme_info.id
            skin_info.create_date = self.get_now_datetime()
            skin_info.modify_date = self.get_now_datetime()
            skin_info.out_id = skin_out_id
            skin_info.theme_out_id = theme_out_id
            skin_id = skin_info_model.add_entity(skin_info)
        invoke_result_data.data = skin_id
        return invoke_result_data