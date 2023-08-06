from portfoliotools.screener.utility.util import get_ticker_list, backTestStrategy
from portfoliotools.screener.stock_detail import StockDetail
from portfoliotools.screener.option_screener import OptionHelper
from datetime import datetime, timedelta
import random
import json
import os
import pandas as pd
from abc import ABC, abstractmethod
import numpy as np
import requests
from bs4 import BeautifulSoup
import nsetools

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
        
# Option Strategies
class OptionIVDiffStrategy(Strategy):
    
    file_path = '{0}_OptionIVDiffStrategy.json'.format(datetime.today().strftime("%Y%m%d"))
    helper = OptionHelper()
    lot_sizes = nsetools.Nse().get_fno_lot_sizes()
    
    def getTickerList(self, pending = False, processed = False):

        if self.ticker_list is None:
            ticker_list = self.helper.fnoList()
        else:
            ticker_list = self.ticker_list
        processed_tickers = list(set(self.saved_data.get('processed_tickers', [])))
        pending_tickers = list(set(ticker_list) - set(processed_tickers))
        if pending:
            return pending_tickers
        if processed:
            return processed_tickers
        return ticker_list
    
    def processStrategy(self, ticker, nextExpiryCount = 1, threshold = 0.01):
        
        df = self.helper.formatedOptionChain(ticker, False)
        nearestExpiry = list(set(df.expiryDate.values))
        nearestExpiry.sort()
        nearestExpiry = nearestExpiry[nextExpiryCount-1]
        df = df[df['expiryDate'].isin([nearestExpiry])]

        callStrikes = list(set((df[df['iv_ce'] > 0].strikePrice.values)))
        putStrikes = list(set((df[df['iv_pe'] > 0].strikePrice.values)))
        strikes = list(set((df.strikePrice.values)))
        strikes.sort(reverse = False)
        up = df.underlyingValue.values[0]

        iv_ce = round(np.mean(df[df['strikePrice'].isin(self._getClosestStrikes(callStrikes, up))].iv_ce),2)
        iv_pe = round(np.mean(df[df['strikePrice'].isin(self._getClosestStrikes(putStrikes, up))].iv_pe),2)
        iv = round((iv_ce + iv_pe)/2,2)
        days_to_expiry = (datetime.strptime(nearestExpiry, '%Y-%m-%d') - datetime.today()).days
        low = round(up*(1 - iv*np.sqrt(days_to_expiry/365)/100),2)
        high = round(up*(1 + iv*np.sqrt(days_to_expiry/365)/100),2)
        strike_low = self._getClosestStrikes(putStrikes, low,1)[0]
        strike_low_nxt = strikes[strikes.index(strike_low) - 1]
        strike_high = self._getClosestStrikes(callStrikes, high,1)[0]
        strike_high_nxt = strikes[strikes.index(strike_high) + 1]
        strike_low_put_price = df[df['strikePrice'].isin([strike_low])].put_price.values[0]
        strike_low_put_nxt_price = df[df['strikePrice'].isin([strike_low_nxt])].put_price.values[0]
        strike_high_call_price = df[df['strikePrice'].isin([strike_high])].call_price.values[0]
        strike_high_call_nxt_price = df[df['strikePrice'].isin([strike_high_nxt])].call_price.values[0]
        lot_size = self.lot_sizes.get(ticker, 1)
        strike_low_max_profit = round((strike_low_put_price - strike_low_put_nxt_price)*lot_size,2)
        strike_low_max_loss = round((strike_low_nxt - strike_low)*lot_size + strike_low_max_profit,2)
        strike_high_max_profit = round((strike_high_call_price - strike_high_call_nxt_price)*lot_size,2)
        strike_high_max_loss = round((strike_high - strike_high_nxt)*lot_size + strike_high_max_profit,2)
        
        data = {
            'ticker' : ticker,
            'iv_ce' : iv_ce,
            'iv_pe' : iv_pe,
            'underlying' : float(up),
            'lot_size' : float(lot_size),
            'days_to_expiry' : days_to_expiry,
            'iv' : iv,
            'low' : low,
            'high' : high,
            'iv_diff' : round(iv_pe - iv_ce,2),
            'strike_low' : float(strike_low),
            'strike_high' : float(strike_high),
            'strike_low_pe_price' : strike_low_put_price,
            'strike_high_ce_price' : strike_high_call_price,
            'strike_low_nxt' : float(strike_low_nxt),
            'strike_high_nxt' : float(strike_high_nxt),
            'strike_low_pe_nxt_price' : strike_low_put_nxt_price,
            'strike_high_ce_nxt_price' : strike_high_call_nxt_price,
            'strike_low_max_profit' : strike_low_max_profit,
            'strike_low_max_loss' : strike_low_max_loss,
            'strike_high_max_profit' : strike_high_max_profit,
            'strike_high_max_loss' : strike_high_max_loss
            }
        data['strategy_action'], data['strategy_max_profit'], data['strategy_max_loss'] = self._getAction(data, threshold)
        data['strategy_summary'] = self._strategySummary(data)
        return data
    
    def screener(self,nextExpiryCount = 1, threshold = 0.01):
        
        result = []
        ticker_list = self.getTickerList()
        pending_tickers = self.getTickerList(pending = True)
        processed_tickers = self.getTickerList(processed = True)
        
        if len(pending_tickers) != 0:
            if self.save:
                sample_tickers = random.sample(pending_tickers, min(10, len(pending_tickers)))
            else:
                sample_tickers = pending_tickers
            for ticker in sample_tickers:
                try:
                    data = self.processStrategy(ticker, nextExpiryCount, threshold)
                    result.append(data)
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
            
        data = pd.DataFrame(result)
        return data
    
    
    def _sortStrikes(self, up, x):
        return abs(up-x)

    def _getClosestStrikes(self, strikes, value, count = 3):
        strikes.sort(key = lambda x: self._sortStrikes(value, x))
        filtered_strikes = strikes[:count]
        return filtered_strikes
    
    def _getAction(self, x, threshold = 0.01):
        
        action = ('', 0, 0) # (action, max_profit, max_loss)
        if abs(x['iv_diff']) > threshold:
            if x['iv_diff'] > 0:
                action = ('Sell PUT', x['strike_low_max_profit'], x['strike_low_max_loss'])
            else:
                action = ('Sell CALL', x['strike_high_max_profit'], x['strike_high_max_loss'])
        return action

    def _strategySummary(self, x):
        message = ''
        if x['strategy_action'] == 'Sell PUT':
            message += '<b>' + x['ticker'] + '</b>\n\n'
            message += '<b>Trades:</b>\n' + 'Sell PUT@' + str(x['strike_low']) + ' for ' + str(x['strike_low_pe_price']) +'\n'
            message += 'Buy PUT@' + str(x['strike_low_nxt']) + ' for ' + str(x['strike_low_pe_nxt_price']) +'\n'
            message += '<b>Max Profit:</b> ' + str(x['strategy_max_profit']) + '\n'
            message += '<b>Max Loss:</b> ' + str(x['strategy_max_loss']) + '\n'
        elif x['strategy_action'] == 'Sell CALL':
            message += '<b>' + x['ticker'] + '</b>\n\n'
            message += '<b>Trades:</b>\n' + 'Sell CALL@' + str(x['strike_high']) + ' for ' + str(x['strike_high_ce_price']) +'\n'
            message += 'Buy CALL@' + str(x['strike_high_nxt']) + ' for ' + str(x['strike_high_ce_nxt_price']) +'\n'
            message += '<b>Max Profit:</b> ' + str(x['strategy_max_profit']) + '\n'
            message += '<b>Max Loss:</b> ' + str(x['strategy_max_loss']) + '\n'
        else:
            pass
        
        return message
    
    
# Screener Strategies       
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