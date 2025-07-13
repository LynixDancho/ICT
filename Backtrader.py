import backtrader as bt
import yfinance as yf
import matplotlib as mp

data = yf.download('TSLA')
data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
data.info()
 
data_daily= bt.feeds.PandasData(dataname=data,
                                     open=3,
                                     close=0,
                                     high=1,
                                     low=2,
                                     volume=4,
                                     openinterest=None,
                                     datetime=None)
data_hourly= bt.feeds.PandasData(dataname=data,
                                     open=3,
                                     close=0,
                                     high=1,
                                     low=2,
                                     volume=4,
                                     openinterest=None,
                                     datetime=None,
                                     timeframe=bt.TimeFrame.Minutes)                                
cerebero =bt.Cerebro()
cerebero.adddata(data_daily)
cerebero.run()

cerebero.plot()