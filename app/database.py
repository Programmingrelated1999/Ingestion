import arcticdb as adb
from dotenv import load_dotenv
import os, yfinance as yf

# Load Environment Variables
load_dotenv()
arcticdb_local_uri = os.getenv('ARCTICDB_LOCAL_URI')

# Connect To Arctic Database
def connect_db():
    db = adb.Arctic(arcticdb_local_uri)
    return db

def save_tickers(tickers):
    db = connect_db()
    lib = db.get_library('daily_price', create_if_missing=True) 
    for ticker, df in tickers.items():
        lib.write(ticker, df, metadata={"source": "yfinance", "auto_adjust": False})
    
# Delete Library
def delete_library(db, name):
    if name in db.list_libraries():
        db.delete_library(name)
        print(f"Library '{name}' deleted successfully.")
    else: 
        print(f"Library '{name}' does not exists.")

def main():
    db = connect_db()
    lib = db["daily_price"] 
    print(lib.list_symbols())
    item = lib.read("VUSA.L")
    df = item.data
    print(df.tail())

if __name__ == "__main__":
    main()