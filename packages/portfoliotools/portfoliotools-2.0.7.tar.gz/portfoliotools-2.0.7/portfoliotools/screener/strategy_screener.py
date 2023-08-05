from portfoliotools.screener.utility.util import get_ticker_list, backTestStrategy
from portfoliotools.screener.stock_detail import StockDetail
from datetime import datetime, timedelta
import random
import json
import os
import pandas as pd
from abc import ABC, abstractmethod
import numpy as np
import requests
from bs4 import BeautifulSoup

nifty_next_50 = ["ABBOTINDIA", "ACC", "ADANIENT", "ADANIGREEN", "ADANITRANS", "ALKEM", "AMBUJACEM", "APOLLOHOSP", "AUROPHARMA", "DMART", "BAJAJHLDNG", "BANDHANBNK", "BERGEPAINT", "BIOCON", "BOSCHLTD", "CADILAHC", "COLPAL", "DABUR", "DLF", "GAIL", "GODREJCP", "HAVELLS", "HDFCAMC", "HINDPETRO", "ICICIGI", "ICICIPRULI", "IGL", "NAUKRI", "INDIGO", "JUBLFOOD", "LTI", "LUPIN", "MARICO", "MOTHERSUMI", "MRF", "MUTHOOTFIN", "NMDC", "PETRONET", "PIDILITIND", "PEL", "PGHH", "PNB", "SBICARD", "SIEMENS", "TORNTPHARM", "UBL", "MCDOWELL-N", "VEDL", "YESBANK"]

class Strategy:
    
    file_path = '{0}_Strategy.json'.format(datetime.today().strftime("%Y%m%d"))
    saved_data = {}
    
    def __init__( self, period = 700, target = .3, stop_loss = .15, tsl_period = 10, useSD = False, save = True, ticker_list = None):
        self.period = period
        self.target = target
        self.stop_loss = stop_loss
        self.tsl_period = tsl_period
        self.useSD = useSD
        self.save = save
        self.ticker_list = ticker_list
        
        self.saved_data = self.loadFromFile()
    
    def saveToFile(self, data):
        if self.save:
            with open(self.file_path, 'w') as outfile:
                json.dump(data, outfile)
    
    def loadFromFile(self):
        try:
            if os.path.exists(self.file_path) and self.save:
                with open(self.file_path) as f:
                    data = json.load(f)
                return data
            else:
                return {}
        except:
            return {}
        
    def getTickerList(self, pending = False, processed = False):
        if self.ticker_list is None:
            ticker_list = [ticker['Ticker'] for ticker in get_ticker_list()]
            ticker_list = ticker_list + nifty_next_50
        else:
            ticker_list = self.ticker_list
        processed_tickers = self.saved_data.get('processed_tickers', [])
        pending_tickers = list(set(ticker_list) - set(processed_tickers))
        if pending:
            return pending_tickers
        if processed:
            return processed_tickers
        return ticker_list
            
    def getCurrentAction(self, series):
        score = -1 # Hold:0, NA:-1
        if series[-1] == 'Buy':
            score = 1
        elif series[-1] == 'Sell':
            score = 2
        else:
            for x in series:
                if x == 'Buy':
                    score = 0
                if x == 'Sell' and score == 0:
                    score = -1
        if score == 1:
            return 'Buy'
        elif score == 2:
            return 'Sell'
        elif score == 0:
            return 'Hold'
        else: return -1
        
    @abstractmethod
    def processStrategy(self, stock_name, period = None):
        pass
    
    @abstractmethod
    def screener(self, formatMessage = True):
        pass
    
    def backTest(self, period = 6000, detailed = True, tickerList = None):
        result = []
        for ticker in tickerList or self.getTickerList():
            df = self.processStrategy(ticker, period = period, screener = False)
            columns = ['Signal', 'Trigger Price', 'Date', 'Sell Action']
            data = df[columns]

            trades = []
            temp = None
            for i in range(len(data)) :
                signal = data.loc[i, 'Signal']
                price = data.loc[i, 'Trigger Price']
                date = data.loc[i, 'Date']
                action = data.loc[i, 'Sell Action']
                if signal == 'Buy' and temp is None:
                    temp = {
                        'Stock':ticker
                    }
                    temp['Buy Price'] = price
                    temp['Buy Date'] = date
                if signal == 'Sell' and temp is not None:
                    temp['Sell Price'] = price
                    temp['Sell Date'] = date
                    temp['Trigger'] = action
                    temp['Days Invested'] = (date - temp['Buy Date']).days
                    temp['Return'] = price/temp['Buy Price']
                    trades.append(temp)
                    temp = None
            if detailed:
                result = result + trades
            else:
                z = pd.DataFrame(trades)
                loss = z[z['Return'] < 1]
                win = z[z['Return'] >= 1]
                win_return = round(100*(win['Return'].product() - 1),2)
                loss_return = round(100*(loss['Return'].product() - 1),2)
                accuracy = round(100*len(win) / (len(loss) + len(win)),2)
                
                summary = {
                    'Stock' : ticker,
                    'Trade Count': len(z),
                    'Return' : (accuracy*win_return/100) + ((100-accuracy)*loss_return/100),
                    'Accuracy' : accuracy,
                    'Average Days' : round(z['Days Invested'].mean(),0),
                    'Win Return': win_return,
                    'Loss Return': loss_return,
                }
                result = result + [summary]
        return pd.DataFrame(result)
    
class Strategy52WHigh(Strategy):
    
    file_path = '{0}_52WStrategy.json'.format(datetime.today().strftime("%Y%m%d"))
    
    def processStrategy(self, stock_name, period = None, screener = True):
        if period is None:
            period = self.period
            
        end_date = datetime.today()
        start_date = end_date + timedelta( days = -1* period )
        obj = StockDetail(stock_name, period = period)
        data = obj.historical_prices
        data['Index'] = list(range(len(data)))

        agg_dict = {'Open': 'first',
                  'High': 'max',
                  'Low': 'min',
                  'Adj Close': 'last',
                   'Index': 'last'}
        data = data[list(agg_dict.keys())]
        df = data.resample("W").agg(agg_dict)
        df.dropna(inplace = True)
        df['52W High'] = df['High'].rolling(window = 52).max()
        df['Breakout'] = df['High'] > df.shift(1)['52W High']
        df['Signal'] = (df['Breakout']) & (df.shift(1)['Breakout'] == False)
        df['Signal'] = df['Signal'].apply(lambda x: 'Buy' if x else '-')

        if self.useSD:
            df['Stop Loss'] = df['Adj Close'] - df['Adj Close'].rolling(window = self.tsl_period).std()*self.stop_loss
            df['Target'] = df['Adj Close'] + df['Adj Close'].rolling(window = self.tsl_period).std()*self.target
        else:
            df['Stop Loss'] = df['Adj Close']*(1-self.stop_loss)
            df['Target'] = df['Adj Close']*(1+self.target)

        df['Target'] = df[['Target', 'Signal']].apply(lambda x: x['Target'] if x['Signal'] == 'Buy' else np.NaN, axis = 1)
        df['Target'].fillna(method = 'ffill', inplace = True)
        df['Stop Loss'] = df[['Stop Loss', 'Signal']].apply(lambda x: x['Stop Loss'] if x['Signal'] == 'Buy' else np.NaN, axis = 1)
        df['Stop Loss'].fillna(method = 'ffill', inplace = True)

        df.reset_index(inplace = True)
        data.reset_index(inplace = True)

        df = data.merge(df[['Signal', 'Stop Loss', 'Target', 'Index']], how = 'left', left_on='Index', right_on='Index' )

        if self.useSD:
            df['TSL'] = df['Adj Close'] - df['Adj Close'].rolling(window = self.tsl_period*5).std()*self.stop_loss
        else:
            df['TSL'] = df['Adj Close']*(1-self.stop_loss)
            
        df['TSL'] = df[['Stop Loss', 'TSL']].apply(lambda x: max(x['Stop Loss'], x['TSL']), axis = 1)

        df['Signal'].fillna('-', inplace = True)
        df['Stop Loss'].fillna(method='ffill', inplace = True)
        df['Target'].fillna(method='ffill', inplace = True)
        df['TSL'].fillna(method='ffill', inplace = True)

        # Calculate Signals
        if screener:
            df = df.loc[df['Signal'].where(df['Signal'] == 'Buy').last_valid_index():]
            df.reset_index(inplace = True, drop = True)
        last_signal = None
        signal_target = None
        df['Sell Action'] = ''
        df['Trigger Price'] = ''
        for i in range(len(df)):
            signal = df.loc[i, 'Signal']
            target = df.loc[i, 'Target']
            tsl = df.loc[i, 'TSL']
            low = df.loc[i, 'Low']
            high = df.loc[i, 'High']
            close = df.loc[i, 'Adj Close']

            if last_signal is None:
                if signal == 'Buy':
                    last_signal = 'Buy'
                    signal_target = target
                    df.loc[i, 'Trigger Price'] = close
                else:
                    df.loc[i, 'Signal'] = ''
            else:
                if tsl > low or high > signal_target:
                    df.loc[i, 'Signal'] = 'Sell'
                    df.loc[i, 'Sell Action'] = 'TSL' if tsl > low else 'Target'
                    df.loc[i, 'Trigger Price'] = tsl if tsl > low else signal_target
                    last_signal = None
                    signal_target = None
                else:
                    df.loc[i, 'Target'] = signal_target
                    df.loc[i, 'Signal'] = ''
        return df
    
    def screener(self, formatMessage = True):
        result = []
        ticker_list = self.getTickerList()
        pending_tickers = self.getTickerList(pending = True)
        processed_tickers = self.getTickerList(processed = True)
        if len(pending_tickers) != 0:
            if self.save:
                sample_tickers = random.sample(pending_tickers, min(50, len(pending_tickers)))
            else:
                sample_tickers = pending_tickers
            for ticker in sample_tickers:
                try:
                    df = self.processStrategy(ticker)
                    action = self.getCurrentAction(list(df['Signal'].values))
                    if action in ['Buy', 'Sell', 'Hold']:
                        result.append({
                            'Stock': ticker,
                            'High': df.tail(1)['High'].values[0],
                            'Close': df.tail(1)['Adj Close'].values[0],
                            'Target': df.tail(1)['Target'].values[0],
                            'Stop Loss':df.tail(1)['Stop Loss'].values[0],
                            'Signal':action,
                            'TSL':df.tail(1)['TSL'].values[0],
                        })
                except:
                    pass

            # Save to file
            result = self.saved_data.get('result', []) + result
            processed_tickers = processed_tickers + sample_tickers
            data = {
                'processed_tickers': processed_tickers + sample_tickers,
                'result' : result
            }
            self.saveToFile(data)
            if len(processed_tickers) < len(ticker_list):
                return None
        else:
            result = self.saved_data.get('result', [])
        
        if formatMessage:
            message = '<b>52w High breached </b>\n\n'
            for stock in [x for x in result if x['Signal'] == 'Buy' ]:
                message += '🟢 <b>' + stock['Stock'] + '</b>\n'
                message += 'Signal: ' + str(stock['Signal']) + '\n'
                message += 'LTP ' + str(round(stock['Close'], 2)) + '\n'
                message += 'Target: ' + str(round(stock['Target'], 2)) + '\n'
                message += 'SL: ' + str(round(stock['TSL'], 2)) + '\n\n'
            for stock in [x for x in result if x['Signal'] == 'Sell' ]:
                message += '🔴 <b>' + stock['Stock'] + '</b>\n'
                message += 'Signal: ' + str(stock['Signal']) + '\n'
                message += 'LTP ' + str(round(stock['Close'], 2)) + '\n'
                message += 'Target: ' + str(round(stock['Target'], 2)) + '\n'
                message += 'SL: ' + str(round(stock['TSL'], 2)) + '\n\n'
            for stock in [x for x in result if x['Signal'] == 'Hold' ]:
                message += '🟠 <b>' + stock['Stock'] + '</b>\n'
                message += 'Signal: ' + str(stock['Signal']) + '\n'
                message += 'LTP ' + str(round(stock['Close'], 2)) + '\n'
                message += 'Target: ' + str(round(stock['Target'], 2)) + '\n'
                message += 'SL: ' + str(round(stock['TSL'], 2)) + '\n\n'

            return message
        else:
            return result
        
class ScreenerData:
    
    def __init__(self, url = None):
        self.url = url
        
    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, url):
        if url is not None:
            self._url = url
        
    def get(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        result = [x.find("tbody") for x in soup.find_all("table")]
        
        data = []
        # Headers
        headers = result[0].find("tr").find_all("th")
        headers = [y.find('a').children for y in headers]
        headers = [next(z).strip() for z in headers]

        # Data
        comps = result[0].find_all("tr")[1:]
        for comp in comps:
            details = comp.find_all("td")
            i = 0
            temp = {}
            for detail in details:
                if detail.find('a') is not None:
                    value = next(detail.find('a').children).strip()
                else:
                    value = next(detail.children).strip()
                try:
                    value = float(value)
                except:
                    pass
                temp[headers[i]] = value
                i += 1
            data.append(temp)

        data = pd.DataFrame(data)
        return data
        
class MagicFormulaStrategy:
    
    def screener(self, formatMessage = True):
        url = 'https://www.screener.in/screens/450341/Magic-Formula/'
        obj = ScreenerData(url)
        data = obj.get()
        data = data.sort_values(by = ['Earnings Yield', 'ROCE'], ascending = False)
        data.reset_index( inplace = True, drop = True)

        # Strategy
        amount_per_stock = 10000
        data['Quantity'] = round(amount_per_stock/data['CMP'],0)
        
        if formatMessage:
            message = '<b>Magic Formula Portfolio</b>\nInvest: 10K per ticker\n\n'
            for stock in data.to_dict(orient = 'record'):
                message += '<b>' + stock['Name'] + '</b>\n'
                message += 'LTP: ' + str(round(stock['CMP'], 2)) + '\n'
                message += 'Quantity: ' + str(round(stock['Quantity'], 2)) + '\n\n'
            return message
        return data