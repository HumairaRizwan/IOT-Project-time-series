# -*- coding: utf-8 -*-
"""Time_series_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WP45hwJg2wetsregKTdEj6es0Y3Fdb5l

# Time Series Analysis

## 1) Importing necessary libraries for time series analysis
"""

import pandas as pd
import matplotlib.pylab as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_pacf,plot_acf
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARMA', FutureWarning)
warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARIMA',FutureWarning)
from datetime import date

"""## 2) Importing dataset for analysis using pandas library as a dataframe"""

df = pd.read_csv('D:\sliit\iot\proj\iotbda-assignment-2023-2023_004_team\dataset\colombo_rh_2012-2018.csv', delimiter=',')
df.head(10)

df.head(10)

"""## 3) Getting a basic description of the data"""

df.describe()

df.info()

"""## 4) Converting date column to datetime format by combining year, month, and day columns
this replaces the unparsable invalid dates values with NaT
"""

df['date'] = pd.to_datetime(df[['year', 'month', 'day']],errors='coerce')

df.dropna(subset=['date'], inplace=True)

"""## 5) Dropping unnecessary data columns from the dataset

#### station_id - not required to be considred as it is unique
#### station_name - Since all the data is for the city of Colombo
"""

df = df.drop(['station_id','station_name','year', 'month', 'day'], axis=1)

"""## 6) Checking null values"""

df.isnull().sum()

"""## 7) Checking duplicates for date"""

df.date.duplicated().sum()

df.count()

df[df['date'] == '6/20/2018']

"""For each date there are min and max values for some records. Therefore we get the Max value only from those duplicates while non-duplicates remains the same"""

aggregated_df = df.groupby('date').max('obs_val')

aggregated_df.head()

aggregated_df[aggregated_df.index == '6/20/2018']

aggregated_df.index.duplicated().sum() # check for duplicates

aggregated_df.count()

plt.plot(aggregated_df.obs_val)
plt.title('Relative Humidity Over Time')
plt.xlabel('Year')
plt.ylabel('Humidity')
plt.show()

"""## 8) Cheking if the data is stationary"""

def stationarity_check(ts):
    
    # Determing rolling statistics
    roll_mean = pd.Series(ts).rolling(window=12).mean()
    # Plot rolling statistics:
    plt.plot(ts, color='green',label='Original')
    plt.plot(roll_mean, color='blue', label='Rolling Mean')
    plt.legend(loc='best')
    plt.title('Rolling Mean')
    plt.show(block=False)
    
    # Perform Augmented Dickey-Fuller test:
    print('Augmented Dickey-Fuller test:')
    df_test = adfuller(ts)
    print("type of df_test: ",type(df_test))
    print("df_test: ",df_test)
    df_output = pd.Series(df_test[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    print("df_output: \n",df_output)
    for key,value in df_test[4].items():
        df_output['Critical Value (%s)'%key] = value
    print(df_output)

"""### Augmented Dickey-Fuller(ADF) test at 5% significance level

#### H0 = Data is no stationary  H1 = Data is stationary

#### alpha = 0.05  p-value =  3.268165e-12

#### Since p-value is less than alpha value we reject H0 at 5% significance level. Hence at 5% significance level the data are stationary
"""

stationarity_check(aggregated_df.obs_val)

import statsmodels.api as sm

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(aggregated_df.obs_val, lags=100, ax=ax1) # 
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(aggregated_df.obs_val, lags=100, ax=ax2)#

"""## 9) Using AIC value to get p and q values

#### d value is 0 since the data is stationary and does not require any differencing
"""

import itertools
p = q = r = range(0, 4)
pqr = itertools.product(p, q , r)
for param in pqr:
    try:
        mod = ARIMA(aggregated_df.obs_val,order=param)
        results = mod.fit()
        print('ARMA{} - AIC:{}'.format(param, results.aic))
    except:
        continue

"""### Since ARMA(3,0,3) has the least AIC value (AIC:14808.337527493812) this is the best fit

## 10) Fitting the model
"""

model = ARIMA(aggregated_df.obs_val,order=(3,0,3)) 
results_MA = model.fit( ) 
plt.plot(aggregated_df.obs_val)
plt.plot(results_MA.fittedvalues, color='red')
plt.title('Fitting data _ MSE: %.2f'% (((results_MA.fittedvalues-aggregated_df.obs_val)**2).mean()))
plt.show()

train_data = aggregated_df.iloc[:-365]
test_data = aggregated_df.iloc[-365:]

forecast = results_MA .predict(start='01/01/2018',end='12/31/2018').rename('test Predictions')
test_data.plot( legend=True)
forecast.plot(legend=True)
plt.title('Temperature Time Series with ARIMA predictions')

"""## 11) Exporting the model as a pickle file for predictions"""

import pickle
 #Writing different model files to file
path = 'D:/sliit/iot/proj/iotbda-assignment-2023-2023_004_team/'
with open( path + 'modelForRH.sav', 'wb') as f:
    pickle.dump(results_MA,f)