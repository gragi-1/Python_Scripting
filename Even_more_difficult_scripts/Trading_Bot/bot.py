import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Download historical data
data = yf.download('AAPL', start='2020-01-01', end='2022-12-31')

# Calculate short and long moving averages
data['short_ma'] = data['Close'].rolling(window=14).mean()
data['long_ma'] = data['Close'].rolling(window=28).mean()

# Create signals
data['signal'] = 0.0
data['signal'][14:] = np.where(data['short_ma'][14:] > data['long_ma'][14:], 1.0, 0.0)

# Generate trading orders
data['positions'] = data['signal'].diff()

# Plot the data
plt.figure(figsize=(10,5))
plt.plot(data['Close'], label='Close Price', color='blue', alpha=0.35)
plt.plot(data['short_ma'], label='14-day SMA', color='red', alpha=0.35)
plt.plot(data['long_ma'], label='28-day SMA', color='green', alpha=0.35)
plt.plot(data.loc[data.positions == 1.0].index, data.short_ma[data.positions == 1.0], '^', markersize=10, color='m')
plt.plot(data.loc[data.positions == -1.0].index, data.short_ma[data.positions == -1.0], 'v', markersize=10, color='k')
plt.ylabel('Price in $')
plt.xlabel('Trade Date')
plt.legend(loc='best')
plt.grid()
plt.show()

# Backtest the strategy
initial_capital = float(100000.0)
positions = pd.DataFrame(index=data.index).fillna(0.0)
positions['AAPL'] = 100*data['signal']
portfolio = positions.multiply(data['Adj Close'], axis=0)
pos_diff = positions.diff()
portfolio['holdings'] = (positions.multiply(data['Adj Close'], axis=0)).sum(axis=1)
portfolio['cash'] = initial_capital - (pos_diff.multiply(data['Adj Close'], axis=0)).sum(axis=1).cumsum()
portfolio['total'] = portfolio['cash'] + portfolio['holdings']
portfolio['returns'] = portfolio['total'].pct_change()

print(portfolio.head())