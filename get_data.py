#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 15:26:44 2019

@author: user
"""

import tushare as ts
import os
import bs4 as bs
import pickle
pro=ts.pro_api(token='5b20c657940d3b0e2b3c78273695774418793e6030a48a3b385c2b3f')
def find_and_save_CSI_300():
    CSI_300_df=ts.get_hs300s()
    print(CSI_300_df)
    tickers=CSI_300_df['code'].values
    tickers_mod=[]
    for ticker in tickers:
        if ticker[0] == '6':
            ticker=ticker+'.SH'
            tickers_mod.append(ticker)
        else:
            ticker=ticker+'.SZ'
            tickers_mod.append(ticker)
    print(tickers_mod)
    
    with open("CSI_tickers.pickle","wb") as f:
        pickle.dump(tickers_mod,f)
    print(tickers_mod)
    return tickers_mod
find_and_save_CSI_300()
    
    
    
def get_data_from_tushare(reload_CSI_300=False):
    if reload_CSI_300:
        tickers_mod=find_and_save_CSI_300()
    else:
        with open("CSI_tickers.pickle","rb") as f:
            tickers_mod=pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    for ticker_mod in tickers_mod:
        print(ticker_mod)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker_mod)):
            df=pro.daily(ts_code=str(ticker_mod),
                         start_date='20170101',end_date='20191201')
            df.reset_index(inplace=True)
            df.set_index('trade_date',inplace=True)
            df.to_csv('stock_dfs/{}.csv'.format(ticker_mod))
        else:
            print('Hey~~~We already have {}'.format(ticker_mod))
            
get_data_from_tushare()