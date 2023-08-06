
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class PrizeRosterModel(BaseModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None):
        super(PrizeRosterModel, self).__init__(PrizeRoster, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class PrizeRoster:

    def __init__(self):
        super(PrizeRoster, self).__init__()
        self.id = 0  # id(act_id+user_id+guid)md5int生成
        self.app_id = ""  # 应用标识
        self.act_id = 0  # 活动标识
        self.user_id = 0  # 用户标识
        self.open_id = ""  # open_id
        self.user_nick = ""  # 用户昵称
        self.order_no = ""  # 订单号
        self.module_id = 0  # 活动模块标识
        self.module_name = ""  # 活动模块名称
        self.goods_type = 0  # 物品类型（1虚拟2实物）
        self.prize_type = 0  # 奖品类型(1现货2优惠券3红包4参与奖5预售)
        self.prize_id = 0  # 奖品标识
        self.prize_name = ""  # 奖品名称
        self.prize_pic = ""  # 奖品图
        self.prize_detail_json = ""  # 奖品详情图（json）
        self.prize_price = 0  # 奖品价格
        self.tag_name = ""  # 标签名称(奖项名称)
        self.tag_id = 0  # 标签ID(奖项标识)
        self.prize_status = 0  # 奖品状态（0未发货1已发货2不予发货3已退款10处理中）
        self.pay_status = 0  # 支付状态(0未支付1已支付)
        self.goods_id = 0  # 商品ID
        self.goods_code = ""  # 商品编码
        self.is_sku = 0  # 是否有SKU
        self.sku_id = ""  # sku_id
        self.sku_name = ""  # sku_name
        self.sku_detail_json = ""  # sku详情json
        self.main_pay_order_no = ""  # 支付主订单号
        self.sub_pay_order_no = ""  # 支付子订单号
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.i1 = 0  # i1
        self.i2 = 0  # i2
        self.i3 = 0  # i3
        self.i4 = 0  # i4
        self.i5 = 0  # i5
        self.s1 = ""  # s1
        self.s2 = ""  # s2
        self.s3 = ""  # s3
        self.s4 = ""  # s4
        self.s5 = ""  # s5
        self.d1 = "1900-01-01 00:00:00"  # d1
        self.d2 = "1900-01-01 00:00:00"  # d2

    @classmethod
    def get_field_list(self):
        return ['id', 'app_id', 'act_id', 'user_id', 'open_id', 'user_nick', 'order_no', 'module_id', 'module_name', 'goods_type', 'prize_type', 'prize_id', 'prize_name', 'prize_pic', 'prize_detail_json', 'prize_price', 'tag_name', 'tag_id', 'prize_status', 'pay_status', 'goods_id', 'goods_code', 'is_sku', 'sku_id', 'sku_name', 'sku_detail_json', 'main_pay_order_no', 'sub_pay_order_no', 'create_date', 'i1', 'i2', 'i3', 'i4', 'i5', 's1', 's2', 's3', 's4', 's5', 'd1', 'd2']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "prize_roster_tb"
    