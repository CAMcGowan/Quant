import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt



class StockChecker():

	def __init__(self, ticker, start_date = dt.datetime.now().date() - dt.timedelta(days=3*365), end_date = dt.datetime.now().date()):
		# Initalise the data to be used
		self.start_date = start_date
		self.end_date = end_date
		self.ticker = ticker
		self.data = yf.download(ticker,start=self.start_date,end=self.end_date)

	def movingaverage(self, ma_1=10, ma_2=100, figsize=(10,4), closing=True, averages= True, markers=True, legend=True, labels=True, limit=True, grid=True, title=True, x_label='Dates', y_label='Value (USD)', markers_on_avg=True, markersize=8):
		# Calculate moving averages based on any number of days desired. Also plot te results according to the specifications.
		# The moving averages
		self.data['ma_1']=self.data['Adj Close'].rolling(window=ma_1,min_periods=1,center=False).mean()
		self.data['ma_2']=self.data['Adj Close'].rolling(window=ma_2,min_periods=1,center=False).mean()

		# Define long/short signals
		x=np.where(self.data['ma_1'][ma_1:]>=self.data['ma_2'][ma_1:],1,0)

		if x[0] == 1:
			first_vals = np.ones(ma_1)
		else:
			first_vals = np.zeros(ma_1)
		x = np.append(first_vals, x)

		self.data['signals'] = x
		self.data['signals'] = self.data['signals'].diff()

		# The graph plotting
		plt.figure(figsize=figsize)

		# determining what to plot
		if closing == True:
			plt.plot(self.data['Adj Close'], label='Adjusted Close')
		if averages == True:
			plt.plot(self.data['ma_1'], label=str(ma_1)+ ' Day Moving Average')
			plt.plot(self.data['ma_2'], label=str(ma_2)+ ' Day Moving Average')
		if markers == True:
			if markers_on_avg == True:
				plt.plot(self.data.loc[self.data['signals']==1].index, self.data['ma_1'][self.data['signals']==1], label='LONG', lw=0, marker='^', c='g', markersize=markersize)
				plt.plot(self.data.loc[self.data['signals']==-1].index, self.data['ma_1'][self.data['signals']==-1], label='SHORT', lw=0, marker='v', c='r', markersize=markersize)
			else:
				plt.plot(self.data.loc[self.data['signals']==1].index, self.data['Adj Close'][self.data['signals']==1], label='LONG', lw=0, marker='^', c='g', markersize=markersize)
				plt.plot(self.data.loc[self.data['signals']==-1].index, self.data['Adj Close'][self.data['signals']==-1], label='SHORT', lw=0, marker='v', c='r', markersize=markersize)

		# Additional features
		if labels == True:
			plt.xlabel(x_label)
			plt.ylabel(y_label)
		if legend == True:
			plt.legend(loc='best')
		if limit == True:
			plt.xlim(self.data.index[0], self.data.index[-1])
		if grid == True:
			plt.grid()
		if title == True:
			plt.title('Moving averages for '+self.ticker)

		plt.show()

	def maoscillator(self, ma_1=10, ma_2=100, figsize=(10,4)):
		# Moving average oscillator plot.
		# The moving averages
		self.data['ma_1']=self.data['Adj Close'].rolling(window=ma_1,min_periods=1,center=False).mean()
		self.data['ma_2']=self.data['Adj Close'].rolling(window=ma_2,min_periods=1,center=False).mean()

		# Oscillations calc
		bar_vals = (self.data['ma_1']-self.data['ma_2']).values
		bar_vals = np.append(bar_vals, 0)
		n_len = self.data.shape[0]
		x = np.linspace(0, n_len, n_len+1)

		# plot
		plt.figure(figsize=figsize)
		plt.fill(x, bar_vals, edgecolor='#3487bf', facecolor='#6bb9ed', linewidth=2)#7dcbff')

		plt.legend(loc='best')
		plt.grid(True)
		plt.xlim(0,n_len)

	    # if labels == True:
		# 	plt.xlabel(x_label)
		# 	plt.ylabel(y_label)
		# if legend == True:
		# 	plt.legend(loc='best')
		# if limit == True:
		# 	plt.xlim(self.data.index[0], self.data.index[-1])
		# if grid == True:
		# 	plt.grid()
		# if title == True:
		# 	plt.title('Moving averages for '+self.ticker)

		plt.show()


test = StockChecker('SPY' )

# test.movingaverage(25, 250, markers_on_avg=False)

# test.movingaverage(25, 250, markers_on_avg=False)

test.maoscillator()
