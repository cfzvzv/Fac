import time

from Code.Quote import MarketEventBase, Market
from Code.Trade import TradeBase


# 配置信息
class Config:
    # 地址
    # 注册易盛外盘9.0仿真交易账号，http://www.esunny.com.cn/index.php?m=content&c=index&a=lists&catid=50
    # 地址
    MarketAddress = "123.161.206.213:7171"
    TradeAddress = "123.161.206.213:8383"

    # 账户
    MarketUserName = "ES"
    MarketPassword = "123456"
    TradeUserName = "Q1203070045"  # 公用测试账户。为了测试准确，请注册使用您自己的账户。
    TradePassword = "a123456"

    # 合约
    ExchangeID = "COMEX"
    ProductID = "GC"
    InstrumentID = "2012"

    # 行情
    AskPrice1 = -1
    BidPrice1 = -1

    # 合约
    cons = '''
    CME F ES 2010
    CME F ES 2012
    CME F ES 2103
    CME F NQ 2012
    CME F NQ 2103
    COMEX F GC 2012
    COMEX F GC 2102
    COMEX F HG 2012
    COMEX F HG 2103
    COMEX F SI 2012
    COMEX F SI 2103
    EUREX F DAX 2012
    HKEX F HSI 2010
    HKEX F HSI 2011
    HKEX F MHI 2010
    HKEX F MHI 2011
    NYMEX F CL 2010
    NYMEX F CL 2012
    NYMEX F CL 2101
    NYMEX F QM 2011
    NYMEX F QM 2012
    SGX F CN 2010
    SGX F CN 2011
    '''


class MarketEvent(MarketEventBase):
    # 回调函数，负责处理易盛的所有逻辑
    def OnTick(self, tick):
        # 接受行情的逻辑
        msg = [tick.ExchangeID,
               tick.ProductID, tick.InstrumentID, tick.TradingTime, tick.PreClosePrice,
               tick.PreSettlementPrice,
               tick.PreOpenInterest, tick.OpenPrice, tick.LastPrice, tick.HighestPrice, tick.LowestPrice, 0, 0,
               tick.UpperLimitPrice, tick.LowerLimitPrice, tick.TotalVolume, tick.TotalTurnover, tick.OpenInterest,
               tick.AveragePrice, tick.ClosePrice, tick.SettlementPrice, tick.LastVolume, tick.ImpliedBidPrice,
               tick.ImpliedBidVolume, tick.ImpliedAskPrice, tick.ImpliedAskVolume, tick.PreDelta, tick.CurrDelta,
               tick.InsideVolume, tick.OutsideVolume, tick.TurnoverRate, 0, 0, 0, 0, tick.OpenInterest,
               tick.ChangeSpeed, tick.ChangeRate, tick.ChangeValue, tick.Swing, tick.TotalBidVolume,
               tick.TotalAskVolume]
        for i in range(20):
            msg += [tick.GetBidPrice(i),
                    tick.GetBidVolume(i),
                    tick.GetAskPrice(i),
                    tick.GetAskVolume(i)]
        msg = [str(i) for i in msg]
        print(msg)
        print(tick.UpdateMillisec)


class Trade(TradeBase):
    def alg(self):
        while self.trade.IsOpened() != 1:
            time.sleep(1)

        es_trade_api = self.get_es_api()
        qryParam = self.get_params()
        # 查询委托单 有些接口查询有间隔限制，如：CTP查询间隔为1秒
        time.sleep(1)
        print("Press any key to QueryOrder.")
        input()
        self.trade.QueryOrder(qryParam)

        # 查询成交单
        time.sleep(3)
        print("Press any key to QueryTradeOrder.")
        input()
        self.trade.QueryTradeOrder(qryParam)

        # 查询合约
        qryParam.ExchangeID = self.cfg.ExchangeID
        qryParam.ProductID = self.cfg.ProductID
        time.sleep(3)
        print("Press any key to QueryInstrument.")
        input()
        self.trade.QueryInstrument(qryParam)
        # 查询持仓
        time.sleep(3)
        print("Press any key to QueryPosition.")
        input()
        self.trade.QueryPosition(qryParam)

        # 查询账户
        time.sleep(3)
        print("Press any key to QueryAccount.")
        input()
        self.trade.QueryAccount(qryParam)

        # 委托下单
        time.sleep(1)
        print("Press any key to OrderAction.")
        input()
        order = es_trade_api.Order()
        order.InvestorID = self.cfg.TradeUserName

        order.ExchangeID = self.cfg.ExchangeID
        order.ProductID = self.cfg.ProductID
        order.InstrumentID = self.cfg.InstrumentID
        order.Price = self.cfg.AskPrice1
        order.Volume = 1
        order.Direction = es_trade_api.DirectionKind_Buy
        order.OpenCloseType = es_trade_api.OpenCloseKind_Open
        # 下单高级选项，可选择性设置
        order.ActionType = es_trade_api.OrderActionKind_Insert  # 下单
        order.OrderType = es_trade_api.OrderKind_Order  # 标准单
        order.PriceCond = es_trade_api.PriceConditionKind_LimitPrice  # 限价
        order.VolumeCond = es_trade_api.VolumeConditionKind_AnyVolume  # 任意数量
        order.TimeCond = es_trade_api.TimeConditionKind_GFD  # 当日有效
        order.ContingentCond = es_trade_api.ContingentCondKind_Immediately  # 立即
        order.HedgeType = es_trade_api.HedgeKind_Speculation  # 投机
        self.trade.OrderAction(order)


if __name__ == '__main__':
    market = Market(Config, MarketEvent)  # 导入配置文件、回调函数
    market.login()  # 登录
    trade = Trade(Config)  # 导入配置文件
    trade.login()  # 登录
    trade.alg()  # 运行策略

    input()  # 阻塞进程
