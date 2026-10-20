import json, yfinance as yf
from pathlib import Path
import pandas as pd
from app.database import connect_db, save_tickers

# Return 10 Years Data, Weekly Interval
def get_stock_data_by_batch(tickers, period, interval):
    all_tickers_df = yf.download(tickers, period = period, interval = interval, actions=True)
    tickers_data = {}
    # Extract Each Ticker Data From All Data And Clean Data
    expected_cols = ['Capital Gains', 'Close', 'Dividends', 'High', 'Low', 'Open', 'Stock Splits', 'Volume']
    for ticker in tickers: 
        ticker_df = all_tickers_df.xs(ticker, axis=1, level='Ticker').dropna(how='all')
        ticker_df = ticker_df.reindex(columns=expected_cols,fill_value=0)
        tickers_data[ticker] = ticker_df
    return tickers_data

def main():
    # Read Json File Containing ETF Tickers
    script_wd = Path(__file__).resolve().parent
    with open(f'{script_wd}/tickers.json', 'r') as file: 
        data = json.load(file)
    tickers = [x['ticker'] for x in data]
    
    # Get Stock Data 
    tickets_data = get_stock_data_by_batch(tickers, period='10y', interval='1d')
    db = connect_db; save_tickers(db, tickets_data)    

if __name__ == '__main__':
    main()