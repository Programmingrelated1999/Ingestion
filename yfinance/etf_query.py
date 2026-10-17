import json, yfinance as yf
from pathlib import Path
import pandas as pd

# Return 10 Years Data, Weekly Interval
def get_stock_data_by_batch(tickers, period, interval):
    all_tickers_df = yf.download(tickers, period = period, interval = interval, actions=True)
    tickers_data = {}
    # Extract Each Ticker Data From All Data And Clean Data
    for ticker in tickers: 
        ticker_df = all_tickers_df.xs(ticker, axis =1, level='Ticker').dropna(how='all')
        for col in ['Capital Gains', 'Close', 'Dividends', 'High', 'Low', 'Open', 'Stock Splits', 'Volume']:
            if col not in ticker_df.columns:
                ticker_df[col] = 0
        tickers_data[ticker] = ticker_df
    return tickers_data

def main():
    # Read Json File Containing ETF Tickers
    script_wd = Path(__file__).resolve().parent
    with open(f'{script_wd}/tickers.json', 'r') as file: 
        data = json.load(file)
    tickers = [x['ticker'] for x in data]
    
    # Get Stock Data And Save It In CSV
    get_stock_data_by_batch(tickers, period='10y', interval='1wk')

if __name__ == '__main__':
    main()