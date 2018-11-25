import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DATA_DIR = os.path.join(BASE_DIR,"data")

def symbol_to_path(symbol, base_dir=BASE_DATA_DIR):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def get_data(symbols, dates):
    """Read stock data (close price) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)  #Empty Dataframe
    if 'NIFTY' not in symbols:  # add NIFTY for reference, if absent
        symbols.insert(0, 'NIFTY')

    for symbol in symbols:
         #Read and join data for each symbol
        csv_path = symbol_to_path(symbol)
        df_temp = pd.read_csv(csv_path, index_col='Date', parse_dates=True, usecols=['Date','Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns = {'Close':symbol})
        df = df.join(df_temp)
        if symbol == 'NIFTY':
            df = df.dropna(subset=["NIFTY"])  # drop dates when NIFTY did not trade
    return df

def plot_data(df, title='Stock Prices', xlabel='Date', ylabel='Price'):
    ax = df.plot(title=title, fontsize=12, figsize=(12,8))
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

def normalize_data(df):
    return df/df.iloc[0,:]

def get_rolling_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    return values.rolling(window=window).mean()


def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    return values.rolling(window=window).std()


def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    upper_band = rm + 2*rstd
    lower_band = rm - 2*rstd

    return upper_band, lower_band

def compute_cumulative_returns(df):
    """Compute and return the daily return values."""
    cumulative_returns = df.copy()

    #daily_returns[1:] = (df[1:]/df[:-1].values)-1
    cumulative_returns = (df/df.iloc[0])-1

    return cumulative_returns

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    daily_returns = df.copy()

    #daily_returns[1:] = (df[1:]/df[:-1].values)-1
    daily_returns = (df/df.shift(1))-1
    daily_returns.iloc[0,:] = 0

    return daily_returns

def test_run3():
    # Read data
    dates = pd.date_range('2017-07-01', '2018-11-24')  # one month only
    symbols = ['NIFTY','RELIANCE']
    df = get_data(symbols, dates)
    plot_data(df)

    # Compute daily returns
    cumulative_returns = compute_cumulative_returns(df)
    plot_data(cumulative_returns, title="Cumulative returns", ylabel="Cumulative returns")

def test_run2():
    # Read data
    dates = pd.date_range('2015-07-01', '2018-11-24')  # one month only
    symbols = ['NIFTY','RELIANCE','TCS']
    df = get_data(symbols, dates)
    #plot_data(df)

    # Compute daily returns
    daily_returns = compute_daily_returns(df)
    #plot_data(daily_returns, title="Daily returns", ylabel="Daily returns")

    #daily_returns['RELIANCE'].hist(bins=20, label='RELIANCE', figsize=(12,8))
    #daily_returns['TCS'].hist(bins=20, label='TCS')
    daily_returns['NIFTY'].hist(bins=50, label='NIFTY', figsize=(12,8))

    mean = daily_returns['NIFTY'].mean()
    std = daily_returns['NIFTY'].std()
    print(daily_returns['NIFTY'].kurtosis())
    plt.axvline(mean, color='w', linestyle='dashed', linewidth=3)
    plt.axvline(std, color='r', linestyle='dashed', linewidth=3)
    plt.axvline(-std, color='r', linestyle='dashed', linewidth=3)
    plt.legend(loc='upper right')

    beta_RELIANCE,alpha_RELIANCE = np.polyfit(daily_returns['NIFTY'], daily_returns['RELIANCE'],1)
    daily_returns.plot(kind='scatter',x='NIFTY',y='RELIANCE')
    plt.plot(daily_returns['NIFTY'], beta_RELIANCE*daily_returns['NIFTY']+alpha_RELIANCE, '-', color='r')

    print(daily_returns.corr(method='pearson'))
    plt.show()


def test_run1():
    # Read data
    dates = pd.date_range('2017-01-01', '2018-11-24')
    symbols = ['NIFTY']
    df = get_data(symbols, dates)

    # Compute Bollinger Bands
    # 1. Compute rolling mean
    rm_NIFTY = get_rolling_mean(df['NIFTY'], window=20)

    # 2. Compute rolling standard deviation
    rstd_NIFTY = get_rolling_std(df['NIFTY'], window=20)

    # 3. Compute upper and lower bands
    upper_band, lower_band = get_bollinger_bands(rm_NIFTY, rstd_NIFTY)

    # Plot raw SPY values, rolling mean and Bollinger Bands
    ax = df['NIFTY'].plot(title="Bollinger Bands", label='NIFTY', fontsize=12, figsize=(12,8))
    rm_NIFTY.plot(label='Rolling mean', ax=ax)
    upper_band.plot(label='upper band', ax=ax)
    lower_band.plot(label='lower band', ax=ax)

    # Add axis labels and legend
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.show()


def test_run():
     # Define a date range
    dates = pd.date_range("2016-1-1","2018-11-24")

    # Choose stock symbols to read
    symbols = ['SBIN','RELIANCE','HDFCBANK','TCS','TATAMOTORS']

    # Get stock data
    df = get_data(symbols, dates)

    ax = df['NIFTY'].plot(title='NIFTY rolling mean', label='NIFTY', fontsize=12, figsize=(12,8))

    rm_NIFTY = pd.rolling_mean(df['NIFTY'], window=20)

    rm_NIFTY.plot(label='Rolling mean', ax=ax)

    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend(loc='upper left')
    plt.show()


    #nd = np.array(df)
    plot_data(df)
    #print(df.loc['2018-11-10':'2018-11-18', ['SBIN','TCS','NIFTY']])

    nd1 = np.array([(2,3,4),(1,2,3)])
    nd2 = np.ones((5,5), dtype=np.int_)

    np.random.seed(567)
    nd3 = np.random.rand(5,5)
    nd4 = np.random.normal(50,10,size=(5,5))
    nd5 = np.random.randint(0,10,size=(5,3))
    #print(len(nd5.shape))

def setPlt():
    numPts = 50
    x = [random.random() for n in range(numPts)]
    y = [random.random() for n in range(numPts)]
    sz = 2 ** (10*np.random.rand(numPts))
    plt.scatter(x, y, s=sz, alpha=0.5)

def pltToSvg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s

def get_svg(df):
    #setPlt() # create the plot
    plot_data(df);
    svg = pltToSvg() # convert plot to SVG
    plt.cla() # clean up plt so it can be re-used
    #response = HttpResponse(svg, content_type='image/svg+xml')
    return svg
