import nsepython
from portfoliotools.screener.stock_detail import StockDetail
import pandas as pd
import numpy as np
from datetime import datetime
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import scipy.stats as st

class OptionHelper:
    
    def fnoList(self):
        return nsepython.fnolist()
    
    def smape_kun(self, y_true, y_pred):
        return np.mean((np.abs(y_pred - y_true) * 200/ (np.abs(y_pred) +       np.abs(y_true))))
    
    def stockPrice(self, ticker, focus_period = 1000, lookback_period = 30, return_period = 1):
        stockObj = StockDetail(ticker, period = focus_period)
        prices = stockObj.calculate_return(return_period) # return_period Returns
        prices['Risk'] = prices['Return'].rolling( window = lookback_period).std()*np.sqrt(360/return_period) # return_period Risk
        prices['Return'] = prices['Return']*(360/return_period)
        return prices
    
    def getFutures(self, ticker):
        try:
            data = nsepython.nse_fno(ticker)
            data = [info.get('metadata', {}) for info in data['stocks'] if info.get('metadata',{}).get('instrumentType','') == 'Stock Futures']
            data = pd.DataFrame(data)
            data['expiryDate'] = data['expiryDate'].apply(lambda x: datetime.strptime(x, '%d-%b-%Y').strftime('%Y-%m-%d'))
            data['futurePrice'] = data['closePrice']
        except:
            data = pd.DataFrame(columns=['expiryDate', 'futurePrice'])
        return data

    def predict(self, df):
        result = {
                'MSE'         : np.nan,
                'SMAPE KUN'    : np.nan,
                'Pred Value'   : np.nan,
                'SD' : np.nan,
                'Pred Low 50%'  : np.nan,
                'Pred High 50%' :np.nan,
                'Model':None
            }
        train_data, test_data = df[0:int(len(df)*0.8)], df[int(len(df)*0.8):]

        train, test = train_data['data'].values, test_data['data'].values
        history = [x for x in train]
        predictions = list()
        p = 5
        d = 0
        q = 1
        for t in range(len(test)):
            model = ARIMA(history, order=(p,q,d))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            obs = test[t]
            history.append(obs)
        error = mean_squared_error(test, predictions)
        result['MSE'] = np.round(error, 3)
        error2 = self.smape_kun(test, predictions)
        result['SMAPE KUN'] = np.round(error2, 3)

        model = ARIMA(history, order=(p,q,d))
        model_fit = model.fit(disp=0)
        result['Model'] = model_fit
        output = model_fit.forecast(alpha =0.5)
        result['Pred Value']  = np.round(output[0][0],2)
        result['SD']  = np.round(output[1][0],2)
        result['Pred Low 50%'] = np.round(output[2][0][0],2)
        result['Pred High 50%']= np.round(output[2][0][1],2)
        return result
    
    def optionChain(self, ticker, predict = True):
        option_chain = nsepython.option_chain(ticker)
        result = []
        for data in option_chain['records']['data']:
            pe = data.get('PE', None)
            ce = data.get('CE', None)
            if pe is not None:
                result.append({
                    'strikePrice': data.get('strikePrice',0),
                    'expiryDate': data.get('expiryDate', ''),
                    'optionType': 'Put',
                    'closePrice': pe.get('lastPrice', 0),
                    'totalBuyQuantity': pe.get('totalBuyQuantity', 0),
                    'totalSellQuantity' : pe.get('totalSellQuantity', 0),
                    'openInterest' : pe.get('openInterest', 0),
                    'pchangeinOpenInterest' : pe.get('pchangeinOpenInterest', 0),
                    'identifier' : pe.get('identifier', ''),
                    'numberOfContractsTraded' : pe.get('totalTradedVolume', 0),
                    'impliedVolatility' : pe.get('impliedVolatility', 0),
                    'pChange' : pe.get('pChange', 0),
                    'underlyingValue' : pe.get('underlyingValue', 0),
                })
            if ce is not None:
                result.append({
                    'strikePrice': data.get('strikePrice',0),
                    'expiryDate': data.get('expiryDate', ''),
                    'optionType': 'Call',
                    'closePrice': ce.get('lastPrice', 0),
                    'totalBuyQuantity': ce.get('totalBuyQuantity', 0),
                    'totalSellQuantity' : ce.get('totalSellQuantity', 0),
                    'openInterest' : ce.get('openInterest', 0),
                    'pchangeinOpenInterest' : ce.get('pchangeinOpenInterest', 0),
                    'identifier' : ce.get('identifier', ''),
                    'numberOfContractsTraded' : ce.get('totalTradedVolume', 0),
                    'impliedVolatility' : ce.get('impliedVolatility', 0),
                    'pChange' : ce.get('pChange', 0),
                    'underlyingValue' : ce.get('underlyingValue', 0),
                })
        option_chain = pd.DataFrame(result)
        option_chain['expiryDate'] = option_chain['expiryDate'].apply(lambda x: datetime.strptime(x, '%d-%b-%Y').strftime('%Y-%m-%d'))
        expiryDates = option_chain['expiryDate'].unique()
        
        # Predict Price Range
        prices = self.stockPrice(ticker, focus_period = 365)
        data = prices[['Adj Close']]
        data.rename(columns={'Adj Close' : 'Close'}, inplace=True)
        # Expiry Dates
        daysToExpiry = [(datetime.strptime(d, '%Y-%m-%d') - datetime.now()).days for d in expiryDates]
        daysToExpiry = [z - round(z/7)*2 for z in daysToExpiry]
        forecast = {}
        i=0
        for days in daysToExpiry:
            data['Low_'+ str(days)] = data['Close'].rolling( window = days).min()
            data['Low_'+ str(days)] = data['Low_'+ str(days)].shift(-1*(days-1))
            data['High_'+ str(days)] = data['Close'].rolling( window = days).max()
            data['High_'+ str(days)] = data['High_'+ str(days)].shift(-1*(days-1))
            #data['Return_'+ str(days)] = (data['Close']/data['Close'].shift(days)-1)*100
            data['High_'+ str(days)] = ((data['High_'+ str(days)]/data['Close'])-1)*100
            data['Low_'+ str(days)] = ((data['Low_'+ str(days)]/data['Close'])-1)*100
            df_High = pd.DataFrame(data = data['High_'+ str(days)].values, columns = ['data'])
            df_Low = pd.DataFrame(data = data['Low_'+ str(days)].values, columns = ['data'])
            df_High.dropna(inplace=True)
            df_Low.dropna(inplace=True)
            temp = {}
            if predict:
                temp['High'] = self.predict(df_High)
                temp['Low'] = self.predict(df_Low)
            temp['DaysToExpiry'] = days
            forecast[expiryDates[i]] = temp
            i+=1
        # Append price ranges
        if predict:
            option_chain['predHighMean'] = option_chain['expiryDate'].apply(lambda x: forecast[x]['High']['Pred Value'])
            option_chain['predLowMean'] = option_chain['expiryDate'].apply(lambda x: forecast[x]['Low']['Pred Value'])
            option_chain['predHighSD'] = option_chain['expiryDate'].apply(lambda x: forecast[x]['High']['SD'])
            option_chain['predLowSD'] = option_chain['expiryDate'].apply(lambda x: forecast[x]['Low']['SD'])
        option_chain['daysToExpiry'] = option_chain['expiryDate'].apply(lambda x: forecast[x]['DaysToExpiry'])
        option_chain['ticker'] = ticker
        option_chain['Historical_IV'] = prices.tail(1)['Risk'].values[0]
        futures = self.getFutures(ticker)
        option_chain = option_chain.merge(futures[['expiryDate', 'futurePrice']], how = 'left', right_on='expiryDate', left_on='expiryDate')
        option_chain['futurePrice'].fillna(0, inplace=True)
        return option_chain
    
    def formatedOptionChain(self, ticker, predict = True):
        
        option_chain = self.optionChain(ticker, predict)
        if predict:
            df = option_chain.groupby(['ticker', 'expiryDate', 'strikePrice']).agg({'numberOfContractsTraded' : sum, 
                                                                               'underlyingValue': max,
                                                                              'predHighMean': max,
                                                                              'predLowMean':max,
                                                                              'predHighSD':max,
                                                                              'predLowSD':max,
                                                                              'daysToExpiry':max,
                                                                              'Historical_IV': max,
                                                                              'futurePrice': max})
        else:
            df = option_chain.groupby(['ticker', 'expiryDate', 'strikePrice']).agg({'numberOfContractsTraded' : sum, 
                                                                                   'underlyingValue': max,
                                                                                   'daysToExpiry':max,
                                                                                   'Historical_IV': max,
                                                                                   'futurePrice': max})
            
        df['call_price'] = option_chain.groupby(['ticker', 'expiryDate', 'strikePrice']).apply(self.callPrice)
        df['put_price'] = option_chain.groupby(['ticker', 'expiryDate', 'strikePrice']).apply(self.putPrice)
        df['iv_pe'] = option_chain.groupby(['ticker', 'expiryDate', 'strikePrice']).apply(self.groupImpliedVolatility,'Put')
        df['iv_ce'] = option_chain.groupby(['ticker', 'expiryDate', 'strikePrice']).apply(self.groupImpliedVolatility,'Call')
        df = df.reset_index()
        df['call_cost_per'] = df['call_price'] *100/df['underlyingValue']
        df['put_cost_per'] = df['put_price'] *100/df['underlyingValue']
        #df = df[df['iv_ce'] > 0]
        #df = df[df['iv_pe'] > 0]
        
        return df

    def straddleCost(self, data):
        try:
            callPrice = list(data[data['optionType'] == 'Call']['closePrice'].values)[0]
            putPrice = list(data[data['optionType'] == 'Put']['closePrice'].values)[0]
            return callPrice + putPrice
        except:
            return 0

    def callPrice(self, data):
        try:
            callPrice = list(data[data['optionType'] == 'Call']['closePrice'].values)[0]
            return callPrice
        except:
            return 0

    def putPrice(self, data):
        try:
            putPrice = list(data[data['optionType'] == 'Put']['closePrice'].values)[0]
            return putPrice
        except:
            return 0

    def straddleBreakEven(self, data, direction = 'up', displayPercent = False):
        try:
            cost = self.straddleCost(data)
            strike = list(data['strikePrice'].values)[0]
            spot = list(data['underlyingValue'].values)[0]
            if direction == 'up':
                price = strike + cost
            else:
                price = strike - cost
            if displayPercent:
                if spot != 0:
                    return ((price - spot)*100 / spot)
                else:
                    np.nan
            else:
                return price
        except:
            return 0

    def groupImpliedVolatility(self, data, optionType = 'Call'):
        try:
            return list(data[data['optionType'] == optionType]['impliedVolatility'].values)[0]
        except:
            return 0

    def calStdProbITM(self, breakEven, current, iv, expiry, optionType = 'CALL'):
        delta = round(100-100*st.norm.cdf(np.log(breakEven/current)/(iv*.01 * np.sqrt(expiry/250))),2)
        if optionType == 'CALL':
            return delta
        else:
            return 100-delta
        
    def getStraddleStrategy(self, ticker):
        option_chain = self.optionChain(ticker, True)
        straddleDetails = option_chain.groupby(['ticker', 'expiryDate', 'strikePrice']).agg({'numberOfContractsTraded' : sum, 
                                                                           'underlyingValue': max,
                                                                          'predHighMean': max,
                                                                          'predLowMean':max,
                                                                          'predHighSD':max,
                                                                          'predLowSD':max,
                                                                          'daysToExpiry':max,
                                                                            'Historical_IV': max,
                                                                            'futurePrice': max})
        straddleDetails['call_price'] = option_chain.groupby(['ticker', 'expiryDate', 'strikePrice']).apply(self.callPrice)
        straddleDetails['put_price'] = option_chain.groupby(['ticker', 'expiryDate', 'strikePrice']).apply(self.putPrice)
        straddleDetails['cost'] = option_chain.groupby(['ticker', 'expiryDate', 'strikePrice']).apply(self.straddleCost)
        straddleDetails['breakeven_up'] = option_chain.groupby(['ticker', 'expiryDate', 'strikePrice']).apply(self.straddleBreakEven,'up')
        straddleDetails['breakeven_down'] = option_chain.groupby(['ticker', 'expiryDate', 'strikePrice']).apply(self.straddleBreakEven,'down')
        straddleDetails['breakeven_up_per'] = option_chain.groupby(['ticker', 'expiryDate', 'strikePrice']).apply(self.straddleBreakEven,'up', True)
        straddleDetails['breakeven_down_per'] = option_chain.groupby(['ticker', 'expiryDate', 'strikePrice']).apply(self.straddleBreakEven,'down', True)
        straddleDetails['iv_pe'] = option_chain.groupby(['ticker', 'expiryDate', 'strikePrice']).apply(self.groupImpliedVolatility,'Put')
        straddleDetails['iv_ce'] = option_chain.groupby(['ticker', 'expiryDate', 'strikePrice']).apply(self.groupImpliedVolatility,'Call')
        straddleDetails = straddleDetails[straddleDetails['numberOfContractsTraded'] > 0]
        straddleDetails = straddleDetails[straddleDetails['iv_ce'] > 0]
        straddleDetails = straddleDetails[straddleDetails['iv_pe'] > 0]

        straddleDetails = straddleDetails.reset_index()
        straddleDetails['call_per'] = straddleDetails['call_price'] *100/straddleDetails['underlyingValue']
        straddleDetails['put_per'] = straddleDetails['put_price'] *100/straddleDetails['underlyingValue']
        straddleDetails['cost_per'] = straddleDetails['cost'] *100/straddleDetails['underlyingValue']
        straddleDetails['probITMCall'] = straddleDetails[['strikePrice', 'call_price', 'underlyingValue', 'iv_ce', 'daysToExpiry']].apply(lambda x: self.calStdProbITM(x['strikePrice'] + x['call_price'],x['underlyingValue'],x['iv_ce'], x['daysToExpiry'], 'CALL'), axis=1)
        straddleDetails['probUpStd'] = straddleDetails[['breakeven_up', 'underlyingValue', 'iv_ce', 'daysToExpiry']].apply(lambda x: self.calStdProbITM(x['breakeven_up'],x['underlyingValue'],x['iv_ce'], x['daysToExpiry'], 'CALL'), axis=1)
        straddleDetails['probUpPredict'] = straddleDetails[['predHighMean', 'predHighSD','breakeven_up_per','cost_per','iv_ce', 'daysToExpiry']].apply(lambda x: round(100-st.norm.cdf((x['breakeven_up_per'] + x['cost_per']*.1 - x['predHighMean'])/max(x['predHighSD'],x['iv_ce'] * np.sqrt(x['daysToExpiry']/250)))*100,2), axis=1)
        straddleDetails['probITMPut'] = straddleDetails[['strikePrice', 'put_price', 'underlyingValue', 'iv_pe', 'daysToExpiry']].apply(lambda x: self.calStdProbITM(x['strikePrice'] - x['put_price'],x['underlyingValue'],x['iv_pe'], x['daysToExpiry'], 'PUT'), axis=1)
        straddleDetails['probDownStd'] = straddleDetails[['breakeven_down', 'underlyingValue', 'iv_pe', 'daysToExpiry']].apply(lambda x: self.calStdProbITM(x['breakeven_down'],x['underlyingValue'],x['iv_pe'], x['daysToExpiry'], 'PUT'), axis=1)
        straddleDetails['probDownPredict'] = straddleDetails[['predLowMean', 'predLowSD','breakeven_down_per','cost_per','iv_pe','daysToExpiry']].apply(lambda x: round(st.norm.cdf((x['breakeven_down_per']-x['cost_per']*.1 - x['predLowMean'])/max(x['predLowSD'],x['iv_pe'] * np.sqrt(x['daysToExpiry']/250)))*100,2), axis=1)
        straddleDetails['probITMLongStraddle'] = (straddleDetails['probUpPredict'] + straddleDetails['probDownPredict'])
        straddleDetails['probITMLongStraddleStd'] = straddleDetails['probUpStd'] + straddleDetails['probDownStd']
        #straddleDetails = straddleDetails[straddleDetails.columns.drop(['probUpStd', 'probUpPredict', 'probDownStd', 'probDownPredict', 'predHighMean', 'predHighSD','predLowMean', 'predLowSD'])]
        return straddleDetails