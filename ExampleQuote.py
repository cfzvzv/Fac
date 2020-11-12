from Code.Quote import MarketEventBase, Market


class Config:
    # 地址
    MarketAddress = "61.163.243.173:7171"  # 行情地址

    # # 账户
    MarketUserName = "ES"  # 账号
    MarketPassword = "123456"  # 密码

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
               tick.ProductID, tick.InstrumentID, tick.TradingTime , tick.PreClosePrice,
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


if __name__ == '__main__':
    market = Market(Config, MarketEvent)  # 导入配置文件、回调函数
    market.login()  # 登录
    input()  # 阻塞进程
