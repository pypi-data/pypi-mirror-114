# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-19 13:37:16
@LastEditTime: 2021-07-26 17:44:56
@LastEditors: HuangJianYi
@Description: 
"""
import threading, multiprocessing
from seven_framework.console.base_console import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.db_models import stat

from seven_cloudapp_frame.models.db_models.asset.asset_inventory_model import *
from seven_cloudapp_frame.models.db_models.asset.asset_warn_config_model import *
from seven_cloudapp_frame.models.db_models.asset.asset_warn_notice_model import *
from seven_cloudapp_frame.models.db_models.user.user_asset_model import *
from seven_cloudapp_frame.models.db_models.stat.stat_queue_model import *
from seven_cloudapp_frame.models.db_models.stat.stat_orm_model import *
from seven_cloudapp_frame.models.db_models.stat.stat_report_model import *
from seven_cloudapp_frame.models.db_models.stat.stat_log_model import *


class FrameConsoleModel():
    """
    :description: 控制台基类
    """
    def console_asset_warn(self, mod_count=10, sub_table_count=0):
        """
        :description: 控制台资产预警
        :param mod_count: 单表队列数
        :param sub_table_count: 分表数
        :return: 
        :last_editors: HuangJianYi
        """
        if sub_table_count == 0:

            self._start_process_user_asset_warn(None, mod_count)
            self._start_process_asset_inventory_warn(None, mod_count)

        else:

            for i in range(sub_table_count):

                t = multiprocessing.Process(target=self._start_process_user_asset_warn, args=[str(i), mod_count])
                t.start()

                j = multiprocessing.Process(target=self._start_process_asset_inventory_warn, args=[str(i), mod_count])
                j.start()

    def console_stat_queue(self, mod_count=10, sub_table_count=0):
        """
        :description: 控制台统计上报
        :param mod_count: 单表队列数
        :param sub_table_count: 分表数
        :return: 
        :last_editors: HuangJianYi
        """
        if sub_table_count == 0:

            self._start_process_stat_queue(None, mod_count)

        else:

            for i in range(sub_table_count):

                t = multiprocessing.Process(target=self._start_process_stat_queue, args=[str(i), mod_count])
                t.start()

    def _start_process_user_asset_warn(self, sub_table, mod_count):

        for i in range(mod_count):

            t = threading.Thread(target=self._process_user_asset_warn, args=[sub_table, i, mod_count])
            t.start()

    def _start_process_asset_inventory_warn(self, sub_table, mod_count):

        for i in range(mod_count):

            j = threading.Thread(target=self._process_asset_inventory_warn, args=[sub_table, i, mod_count])
            j.start()

    def _process_user_asset_warn(self, sub_table, mod_value, mod_count):
        """
        :description: 处理用户资产负数预警
        :param sub_table: 分表名称
        :param mod_value: 当前队列值
        :param mod_count: 队列数
        :return: 
        :last_editors: HuangJianYi
        """
        user_asset_model = UserAssetModel(sub_table=sub_table)
        asset_warn_notice_model = AssetWarnNoticeModel()
        print(f"{TimeHelper.get_now_format_time()} 用户资产负数预警队列{mod_value}启动")
        while True:
            now_date = TimeHelper.get_now_format_time()
            now_day_int = SevenHelper.get_now_day_int()
            user_asset_list = user_asset_model.get_list(f"MOD(user_id,{mod_count})={mod_value} and asset_value<0 and {now_day_int}>warn_day ", order_by="create_date asc", limit="100")
            if len(user_asset_list) > 0:
                for user_asset in user_asset_list:
                    try:
                        user_asset.warn_date = now_date
                        user_asset.warn_day = now_day_int
                        user_asset_model.update_entity(user_asset, "warn_date,warn_day")

                        asset_warn_notice = AssetWarnNotice()
                        asset_warn_notice.app_id = user_asset.app_id
                        asset_warn_notice.act_id = user_asset.act_id
                        asset_warn_notice.user_id = user_asset.user_id
                        asset_warn_notice.open_id = user_asset.open_id
                        asset_warn_notice.user_nick = user_asset.user_nick
                        asset_warn_notice.asset_type = user_asset.asset_type
                        asset_warn_notice.asset_object_id = user_asset.asset_object_id
                        if user_asset.asset_type == 1:
                            asset_warn_notice.log_title = f"次数异常,值为负数:{user_asset.asset_value}"
                        elif user_asset.asset_type == 2:
                            asset_warn_notice.log_title = f"积分异常,值为负数:{user_asset.asset_value}"
                        else:
                            asset_warn_notice.log_title = f"档位异常,档位ID:{user_asset.asset_object_id},值为负数:{user_asset.asset_value}"

                        asset_warn_notice.info_json = SevenHelper.json_dumps(user_asset)
                        asset_warn_notice.create_date = now_date
                        asset_warn_notice.create_day = now_day_int
                        asset_warn_notice_model.add_entity(asset_warn_notice)

                    except Exception as ex:
                        logger_error.error(f"用户资产负数预警队列{mod_value}异常,json串:{SevenHelper.json_dumps(user_asset)},ex:{ex.decode()}")
                        continue
            else:
                time.sleep(1)

    def _process_asset_inventory_warn(self, sub_table, mod_value, mod_count):
        """
        :description: 处理资产每日进销存是否对等预警
        :param sub_table: 分表名称
        :param mod_value: 当前队列值
        :param mod_count: 队列数
        :return: 
        :last_editors: HuangJianYi
        """
        asset_inventory_model = AssetInventoryModel(sub_table=sub_table)
        asset_warn_notice_model = AssetWarnNoticeModel()
        print(f"{TimeHelper.get_now_format_time()} 资产每日进销存预警队列{mod_value}启动")
        while True:
            now_date = TimeHelper.get_now_format_time()
            now_day_int = SevenHelper.get_now_day_int()
            asset_inventory_list = asset_inventory_model.get_list(f"MOD(user_id,{mod_count})={mod_value} and create_day={now_day_int} and process_count=0", order_by="create_date asc", limit="100")
            if len(asset_inventory_list) > 0:
                for asset_inventory in asset_inventory_list:
                    try:
                        asset_inventory.process_count = 1
                        asset_inventory.process_date = now_date
                        asset_inventory_model.update_entity(asset_inventory, "process_count,process_date")

                        if (asset_inventory.history_value + asset_inventory.inc_value + asset_inventory.dec_value) != asset_inventory.now_value:

                            asset_warn_notice = AssetWarnNotice()
                            asset_warn_notice.app_id = asset_inventory.app_id
                            asset_warn_notice.act_id = asset_inventory.act_id
                            asset_warn_notice.user_id = asset_inventory.user_id
                            asset_warn_notice.open_id = asset_inventory.open_id
                            asset_warn_notice.user_nick = asset_inventory.user_nick
                            asset_warn_notice.asset_type = asset_inventory.asset_type
                            asset_warn_notice.asset_object_id = asset_inventory.asset_object_id
                            asset_warn_notice.log_title = f"历史值:{asset_inventory.history_value},增加：{asset_inventory.inc_value},减少：{asset_inventory.dec_value},当前值:{asset_inventory.now_value}"
                            if asset_inventory.asset_type == 1:
                                asset_warn_notice.log_title = "次数每日进销存异常," + asset_warn_notice.log_title
                            elif asset_inventory.asset_type == 2:
                                asset_warn_notice.log_title = "积分每日进销存异常," + asset_warn_notice.log_title
                            else:
                                asset_warn_notice.log_title = f"价格档位每日进销存异常,档位ID:{asset_inventory.asset_object_id}," + asset_warn_notice.log_title

                            asset_warn_notice.info_json = SevenHelper.json_dumps(asset_inventory)
                            asset_warn_notice.create_date = now_date
                            asset_warn_notice.create_day = now_day_int
                            asset_warn_notice_model.add_entity(asset_warn_notice)

                    except Exception as ex:
                        logger_error.error(f"资产每日进销存预警队列{mod_value}异常,json串:{SevenHelper.json_dumps(asset_inventory)},ex:{ex.decode()}")
                        continue
            else:
                time.sleep(60 * 60)

    def _start_process_stat_queue(self, sub_table, mod_count):

        for i in range(mod_count):

            t = threading.Thread(target=self._process_stat_queue, args=[sub_table, i, mod_count])
            t.start()

    def _process_stat_queue(self, sub_table, mod_value, mod_count):
        """
        :description: 处理统计队列
        :param sub_table: 分表名称
        :param mod_value: 当前队列值
        :param mod_count: 队列数
        :return: 
        :last_editors: HuangJianYi
        """
        db_transaction = DbTransaction(db_config_dict=config.get_value("db_cloudapp"))
        stat_queue_model = StatQueueModel(sub_table=sub_table, db_transaction=db_transaction)
        stat_log_model = StatLogModel(sub_table=sub_table, db_transaction=db_transaction)
        stat_report_model = StatReportModel(db_transaction=db_transaction)
        stat_orm_model = StatOrmModel()
        print(f"{TimeHelper.get_now_format_time()} 统计队列{mod_value}启动")
        while True:
            now_date = TimeHelper.get_now_format_time()
            now_day_int = SevenHelper.get_now_day_int()
            now_month_int = SevenHelper.get_now_month_int()
            stat_queue_list = stat_queue_model.get_list(f"MOD(user_id,{mod_count})={mod_value} and process_count<10 and '{now_date}'>process_date", order_by="process_date asc", limit="100")
            if len(stat_queue_list) > 0:
                redis_init = SevenHelper.redis_init()
                for stat_queue in stat_queue_list:
                    try:
                        redis_stat_orm_key = f"stat_orm_info:{stat_queue.act_id}_{stat_queue.module_id}_{stat_queue.key_name}"
                        stat_orm = redis_init.get(redis_stat_orm_key)
                        if not stat_orm:
                            stat_orm = stat_orm_model.get_entity("((act_id=%s and module_id=%s) or (act_id=0 and module_id=0)) and key_name=%s", params=[stat_queue.act_id, stat_queue.module_id, stat_queue.key_name])
                            if stat_orm:
                                redis_init.set(redis_stat_orm_key, SevenHelper.json_dumps(stat_orm), ex=config.get_value("cache_expire", 60 * 1))
                        if not stat_orm:
                            stat_queue.process_count += 1
                            stat_queue.process_result = "orm不存在"
                            minute = 1 if stat_queue.process_count <= 5 else 5
                            stat_queue.process_date = TimeHelper.add_minutes_by_format_time(minute=minute)
                            stat_queue_model.update_entity(stat_queue, "process_count,process_result,process_date")
                            continue
                        if isinstance(stat_orm, StatOrm) == False:
                            stat_orm = json.loads(stat_orm)
                        is_add = True
                        if stat_orm.is_repeat == 1:
                            if stat_orm.repeat_type == 2:
                                stat_log_total = stat_log_model.get_total("act_id=%s and module_id=%s and orm_id=%s and user_id=%s", params=[stat_orm.act_id, stat_orm.module_id, stat_orm.id, stat_orm.user_id])
                            else:
                                stat_log_total = stat_log_model.get_total("act_id=%s and module_id=%s and orm_id=%s and user_id=%s and create_day=%s", params=[stat_orm.act_id, stat_orm.module_id, stat_orm.id, stat_orm.user_id, now_day_int])
                            if stat_log_total > 0:
                                is_add = False

                        stat_log = StatLog()
                        stat_log.app_id = stat_queue.app_id
                        stat_log.act_id = stat_queue.act_id
                        stat_log.module_id = stat_queue.module_id
                        stat_log.orm_id = stat_queue.orm_id
                        stat_log.user_id = stat_queue.user_id
                        stat_log.open_id = stat_queue.open_id
                        stat_log.key_value = stat_queue.key_value
                        stat_log.create_day = now_day_int
                        stat_log.create_month = now_month_int
                        stat_log.create_date = now_date

                        stat_report_condition = "act_id=%s and module_id=%s and key_name=%s and create_day=%s"
                        stat_report_param = [stat_orm.act_id, stat_orm.module_id, stat_orm.key_name, now_day_int]
                        stat_report_total = stat_report_model.get_total(stat_report_condition, params=stat_report_param)

                        db_transaction.begin_transaction()
                        if is_add:
                            if stat_report_total == 0:
                                stat_report = StatReport()
                                stat_report.app_id = stat_queue.app_id
                                stat_report.act_id = stat_queue.act_id
                                stat_report.module_id = stat_queue.module_id
                                stat_report.key_name = stat_queue.key_name
                                stat_report.key_value = stat_queue.key_value
                                stat_report.create_date = now_date
                                stat_report.create_year = now_date.year
                                stat_report.create_month = now_month_int
                                stat_report.create_day = now_day_int
                                stat_report_model.add_entity(stat_report)
                            else:
                                stat_report_model.update_table(f"key_value=key_value+{stat_queue.key_value}", stat_report_condition, params=stat_report_param)
                        stat_log_model.add_entity(stat_log)
                        stat_queue_model.del_entity("id=%s", params=[stat_queue.id])
                        db_transaction.commit_transaction()

                    except Exception as ex:
                        logger_error.error(f"统计队列{mod_value}异常,json串:{SevenHelper.json_dumps(stat_queue)},ex:{ex.decode()}")
                        db_transaction.rollback_transaction()
                        stat_queue.process_count += 1
                        stat_queue.process_result = f"出现异常,json串:{SevenHelper.json_dumps(stat_queue)},ex:{ex.decode()}"
                        minute = 1 if stat_queue.process_count <= 5 else 5
                        stat_queue.process_date = TimeHelper.add_minutes_by_format_time(minute=minute)
                        stat_queue_model.update_entity(stat_queue, "process_count,process_result,process_date")
                        continue
            else:
                time.sleep(1)
