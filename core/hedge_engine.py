from core.api_clients.paradex import ParadoxClient
from core.api_clients.edgex import EdgexClient
from core.position_manager import PositionManager
import logging
import random
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class HedgeEngine:
    def __init__(self, config):
        self.paradex_clients = ParadoxClient(config['paradex'])
        self.edgex_clients = EdgexClient(config['edgex'])
        self.position_manager = PositionManager()
        self.pairs = config['pairs']  # 自定义交易对
        self.rounds = config['execution']['total_rounds']  # 刷量次数
        self.trade_interval = config['execution']['intra_round_delay']  # 刷量时间随机间隔
        self.round_interval = config['execution']['inter_round_delay']  # 轮次间隔时间随机

    def check_token(self, pair):
        # 检查交易所是否存在该代币品种
        market_para_price = self.paradex_clients.get_market_price(pair['paradex_symbol'])
        market_edge_price = self.edgex_clients.get_market_price(pair['edgex_symbol'])
        if market_para_price < 0:
            logging.error(f"para交易所找不到该代币品种：{pair['paradex_symbol']}")
            return False
        if market_para_price < 0:
            logging.error(f"edge交易所找不到该代币品种：{pair['edgex_symbol']}")
            return False
        return market_para_price > 0 and market_edge_price > 0

    def log_balances(self):
        logging.info(
            f"Para 账户余额: {self.paradex_clients.account_price()}, Edge 账户余额: {self.edgex_clients.account_price()}")

    def paradex_unrealized_pnl(self, pair):
        # 拿到当前浮盈百分比情况
        paradex_order_price = self.paradex_clients.order_detail()
        edgex_order_price = self.edgex_clients.order_detail()
        if paradex_order_price + edgex_order_price >= pair['max_price_deviation']:
            logging.info(f"检测到未实现盈亏满足条件{pair['max_price_deviation']}%，直接限价平仓")
            self.paradex_clients.close_order()
            self.edgex_clients.close_order()
            return False
        return True

    def check_close(self):
        paradex = self.paradex_clients.count_unorder()
        edgex = self.edgex_clients.count_unorder()
        isFlag = False
        if paradex > 0:
            logging.info("paradex未平仓，等待平仓中.....")
            self.paradex_clients.close_order()
            isFlag = True
        if edgex > 0:
            logging.info("edgex未平仓，等待平仓中.....")
            self.edgex_clients.close_order()
            isFlag = True
        return isFlag

    def run(self):
        for i in range(self.rounds):
            logging.info(f"开始第 {i + 1} 轮刷量")
            self.log_balances()
            # 检查是否还存在有未关闭的仓位
            while self.check_close():
                logging.info("仓位未完全关闭，等待处理")
                time.sleep(3)

            for pair in self.pairs:
                logging.info(
                    f"第 {i + 1} 轮刷量，本次的交易品种是{pair['paradex_symbol']}，开始检查交易所是否存在该交易品种....")
                if not self.check_token(pair):
                    break
                market_para_price = self.paradex_clients.get_market_price(pair['paradex_symbol'])
                market_edge_price = self.edgex_clients.get_market_price(pair['paradex_symbol'])
                # 检测两个交易所的差价，少的一方做多，多的一方做空，默认为para做多，
                if abs(market_edge_price - market_para_price) > 0:
                    # 限价买入
                    logging.info(
                        f"交易所价格偏差过大 ({abs(market_para_price - market_edge_price)})，调整对冲策略[para:SELL，edgex:BUY]")
                    self.paradex_clients.limit_order(pair, 'SELL', market_para_price)
                    self.edgex_clients.limit_order(pair, 'BUY', market_edge_price)
                    while self.paradex_unrealized_pnl(pair):
                        logging.warning("实时监测中......")
                        time.sleep(2)
                else:
                    # 限价买入
                    logging.info(
                        f"交易所价格 ({abs(market_para_price - market_edge_price)})，调整对冲策略[para:BUY，edgex:SELL]")
                    self.paradex_clients.limit_order(pair, 'BUY')
                    self.edgex_clients.limit_order(pair, 'SELL')
                    while self.paradex_unrealized_pnl(pair):
                        logging.warning("实时监测中......")
                        time.sleep(2)

                time.sleep(random.randint(*self.trade_interval))
            self.log_balances()
            logging.info(f"结束第 {i + 1} 轮刷量")
            time.sleep(random.randint(*self.round_interval))
        logging.info("刷量结束")
