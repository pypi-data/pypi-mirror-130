import pandas as pd
# from rltrade import config
# from rltrade.data import IBKRDownloader,FeatureEngineer

# demo = True
# train_period = ('2021-11-22','2021-11-25') #for training the model
# test_period = ('2021-11-25','2021-11-30') 
# path = 'models/daytrades/ESNQ'
# ticker_list = ['ESZ1','NQZ1']
# sec_types = ['FUT','FUT']
# exchanges = ['GLOBEX','GLOBEX']
# tech_indicators = config.STOCK_INDICATORS_LIST # indicators from stockstats
# additional_indicators = config.ADDITIONAL_DAYTRADE_INDICATORS

# env_kwargs = {
#     "initial_amount": 50_000, #this does not matter as we are making decision for contract and not money.
#     "ticker_col_name":"tic",
#     "mode":'min',
#     "filter_threshold":1, #between 0.1 to 1, select percentage of top stocks 0.3 means 30% of top stocks
#     "target_metrics":['asset','cagr','sortino'], #asset, cagr, sortino, calamar, skew and kurtosis are available options.
#     "transaction_cost":1.5, #transaction cost per order
#     "tech_indicator_list":tech_indicators + additional_indicators, 
#     "reward_scaling": 1}

# PPO_PARAMS = {'ent_coef':0.0005,
#             'learning_rate':0.0001,
#             'batch_size':151}

# print('Downloading Data')
# df = IBKRDownloader(start_date = train_period[0], # first date
#                     end_date = test_period[1], #last date
#                     ticker_list = ticker_list,
#                     sec_types=sec_types,
#                     exchanges=exchanges,
#                     demo=demo,
#                     ).fetch_min_data()
# df.to_csv('testdata/df.csv',index=False)

# fe = FeatureEngineer(additional_indicators=additional_indicators,
#                     stock_indicator_list=tech_indicators,
#                     cov_matrix=True,
#                     mode='min')

# df = fe.add_half_hour_time(df)

# df.to_csv("testdata/temp.csv",index=False)

# print(df)

path = 'models/daytrades/ESNQ'
df = pd.read_csv(path+'/test_df.csv')
print(df['return'].sum())