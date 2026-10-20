import arcticdb as adb
from dotenv import load_dotenv
import os, logging, yfinance as yf

# Load Environment Variables
load_dotenv()
arcticdb_local_uri = os.getenv('ARCTICDB_LOCAL_URI')

# Logging
logger = logging.getLogger(__name__)

# Connect To Arctic Database
def connect_db():
    db = adb.Arctic(arcticdb_local_uri)
    return db

# Save Tickers In Database 
def save_tickers(db, tickers):
    lib = db.get_library('daily_price', create_if_missing=True) 
    for ticker, df in tickers.items():
        logger.info("Saving %s to daily_price", ticker)
        lib.write(ticker, df, metadata={"source": "yfinance", "auto_adjust": False})
        logger.info("Saved %s to daily_price successfully", ticker)

# Delete Library
def delete_library(db, name):
    if name in db.list_libraries():
        db.delete_library(name)
        logger.info("Library %s deleted successfully.", name)
        print(f"Library '{name}' deleted successfully.") # To Be Replaced
    else: 
        logger.warning("Library %s does not exists.", name)
        print(f"Library '{name}' does not exists.")

# TESTING PURPOSE ONLY
def _tester():
    db = connect_db()
    lib = db["daily_price"] 
    print(lib.list_symbols())
    item = lib.read("VUSA.L")
    df = item.data
    print(df.head())

if __name__ == "__main__":
    _tester()