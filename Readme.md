# 易盛行情、交易API的Python高级封装

-----


## 易盛金融衍生品系统

易盛推出的金融衍生品系统，目前市场上在用的有`3.0`、`8.0`、`9.0`三个平台，各个平台有自己对应的行情与交易API。

- `3.0`：国际金融衍生品交易分析系统, 用于外盘交易。
- `8.0`：内盘期货交易管理系统，用于内盘交易。
- `9.0`（内盘）：启明星期货期权交易平台，内盘的行情和交易。
- `9.0`（外盘）：北斗星期货期权交易平台，外盘的行情和交易。


对于**内盘**开发者，
- 可先联系期货公司获取目前正在使用的易盛系统版本号：
 - 使用9.0平台对应的9.0API。
 - 使用8.0平台对应8.0API。

对于**外盘**开发者：
- 目前交易可以用3.0API和9.0API
- 行情可以用3.0也可以用9.0（以期货公司部署的行情后台系统为准，如果都可以的话，建议9.0）。
- 交易也可以使用3.0和9.0（以期货公司部署的交易后台系统为准，目前使用3.0交易后台的公司较多）。
## 使用方式
### 快速体验方法一
双击`快速体验方式一.bat`

### 快速体验方法二
双击`快速体验方式二.exe`

### 行情
|ExampleQuote.py|只需要修改此文件即可

1.在Config中配置账号、密码、需要订阅的合约
```bash
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
    '''
```
2.定义回调函数:
```bash
class MarketEvent(MarketEventBase):
    # 回调函数，负责处理易盛的所有逻辑
    def OnTick(self, tick):
        # 接受行情的逻辑
        msg = [tick.ExchangeID,
               tick.ProductID, tick.InstrumentID, tick.TradingTime, tick.PreClosePrice, tick.PreSettlementPrice,
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
```
3.登录
```bash
    market = Market(Config, MarketEvent)  # 导入配置文件、回调函数
    market.login()  # 登录
    input() # 阻塞进程
```

### 交易
|ExampleTrade.py|只需要修改此文件即可
```bash
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
```

### 9.0 API(内盘)
|系统|行情|交易|
|--|--|--|
|Windows|TapQuoteAPI.dll|TapTradeAPI.dll|
|Linux|TapQuoteAPI.so|TapTradeAPI.so|

### 9.0 API(外盘)
|系统|行情|交易|
|--|--|--|
|Windows|TapQuoteAPI.dll|iTapTradeAPI.dll|
|Linux|TapQuoteAPI.so|libiTapTradeAPI.so|


------

## 疑问
### 

1.邮箱 976308589@qq.com

2.QQ`976308589`

### 

1.python3.6.8+64位

