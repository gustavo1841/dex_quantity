import logging
import random
import requests
import time

class ParadoxClient:
    def __init__(self, config):
        self.JWT = None
        self.base_url = config['url']
        self.config = config
        self.getJWT()

    def build_auth_message(chainId: int, now: int, expiry: int):
        message = {
            "message": {
                "method": "POST",
                "path": "/v1/auth",
                "body": "",
                "timestamp": now,
                "expiration": expiry,
            },
            "domain": {"name": "Paradex", "chainId": hex(chainId), "version": "1"},
            "primaryType": "Request",
            "types": {
                "StarkNetDomain": [
                    {"name": "name", "type": "felt"},
                    {"name": "chainId", "type": "felt"},
                    {"name": "version", "type": "felt"},
                ],
                "Request": [
                    {"name": "method", "type": "felt"},
                    {"name": "path", "type": "felt"},
                    {"name": "body", "type": "felt"},
                    {"name": "timestamp", "type": "felt"},
                    {"name": "expiration", "type": "felt"},
                ],
            },
        }
        return message
    def get_account(self):
        print()
    def sign_message(self):
        print()
    def getJWT(self):
        # chain_id = ''
        # now = int(time.time())
        # expiry = now + 24 * 60 * 60
        # message = self.build_auth_message(chain_id, now, expiry)
        # sig = self.sign_message(message)
        # headers = {
        #     "PARADEX-STARKNET-ACCOUNT": self.account_address,
        #     "PARADEX-STARKNET-SIGNATURE": f'["{sig[0]}","{sig[1]}"]',
        #     "PARADEX-TIMESTAMP": str(now),
        #     "PARADEX-SIGNATURE-EXPIRATION": str(expiry),
        # }
        # url = f"{self.base_url}/auth"
        # logging.info(f"POST {url}")
        # logging.debug(f"Headers: {headers}")
        # response = requests.post(url,headers=headers)
        # status_code = response.status
        # response_data = await response.json()
        # if status_code == 200:
        #     logging.info(f"Success: {response_data}")
        # else:
        #     logging.error(f"Status Code: {status_code}, Response: {response_data}")
        # self.JWT = response_data.get("jwt_token", "")
        # self.headers = {"Authorization": f"Bearer {self.jwt}", "Content-Type": "application/json"}
        pass

    def get_market_price(self,symbol):
        # 获取最新市价价格
        # url = f"{self.base_url}/v1/orders"
        # headers = {
        #     "Accept": "application/json",
        #     "Authorization": f"Bearer {self.JWT}"
        # }
        # response = requests.get(url, headers=headers)
        # return response
        price = 50000 + random.uniform(-50, 50)# 模拟市场
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
        # 模拟当前订单浮盈百分比
        price = random.uniform(-1, 1)
        logging.warning(f"当前订单浮盈百分比{price}")
        return price

    def close_order(self):
        # 限价平仓
        logging.info(f"平仓成功")

    def account_price(self):
        # 账户余额
        return 2000
