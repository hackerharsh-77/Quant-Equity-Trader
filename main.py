# region imports
from AlgorithmImports import *
# endregion

class EnergeticApricotArmadillo(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2021, 1, 1)
        self.SetCash(100000)

        spy = self.AddEquity("SPY", Resolution.Daily)
        spy.SetDataNormalizationMode(DataNormalizationMode.Raw)

        self.spy = spy.Symbol
        self.SetBenchmark("SPY")
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)

        self.entryPrice = 0
        self.period = timedelta(31)
        self.nextEntryTime= self.Time 

    def OnData(self, data: Slice):
        if not self.spy in data:
            return
       # price = data.Bars[self.spy].Close
        price = data[self.spy].Close
       # price = self.Securities[self.spy].Close
        if not self.Portfolio.Invested:
            if self.nextEntryTime <= self.Time:
               # self.MarketOrder(self.spy, self.Portfolio.Cash /price) calculates manually
               self.SetHoldings(self.spy,1)
               self.Log("BUY SPY @" + str(price))
               self.entryPrice = price
        elif self.entryPrice * 1.1 < price or self.entryPrice * 0.9 > price:
            self.Liquidate()
            self.Log("SELL SPY @" + str(price))
            self.nextEntryTime = self.Time + self.period
