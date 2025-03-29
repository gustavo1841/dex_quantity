import logging
import random


class EdgexClient:
    def __init__(self, config):
        self.JWT = None
        self.base_url = config['url']
        self.config = config


    def getJWT(self):
        # 获取授权JWT
        self.JWT = "Bearer {JWT}"

    def get_market_price(self, symbol):
        # 获取最新市价价格
        # url = f"{self.base_url}/v1/orders"
        # headers = {
        #     "Accept": "application/json",
        #     "Authorization": f"Bearer {self.JWT}"
        # }
        # response = requests.get(url, headers=headers)
        # return response
        price = 50000 + random.uniform(-50, 50)  # 模拟市场
        logging.warning(f"获取当前{symbol}最新行情价格：{price}")
        return price

    def limit_order(self, pair, side, order_price):
        # 限价开单
        logging.info(
            f"代币种类:{pair['paradex_symbol']}，杠杆倍数：{pair['paradex_leverage']}，交易金额(USD){pair['base_amount']}，差价：{pair['max_price_deviation']} {side} 限价单执行: {order_price}，账户余额: {self.account_price()}")
        return order_price

    def count_unorder(self):
        # 获取当前未平仓订单数量
        return random.uniform(-50, 50)

    def order_detail(self):
        # 模拟当前订单浮盈
        price = random.uniform(-50, 50)
        logging.warning(f"当前订单浮盈百分比{price}")
        return price

    def close_order(self):
        # 限价平仓
        logging.info(f"平仓成功")

    def account_price(self):
        # 账户余额
        return 2000

