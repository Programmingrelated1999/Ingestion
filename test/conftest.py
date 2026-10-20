import pytest, os, pandas as pd
import app.database as database
from dotenv import load_dotenv

# Sample Test Dataframe
def get_sample_data():
    df = pd.DataFrame(columns = ['Capital Gains', 'Close', 'Dividends', 'High', 'Low', 'Open', 'Stock Splits', 'Volume'])
    df.index.name = 'Date'
    df.loc['2026-10-11'] = [0.0, 111.955002, 0.0, 113.093481, 110.710093, 110.725031, 0.0, 457820.0]
    df.loc['2026-10-12'] = [0.0, 112.014999, 0.0, 112.142502, 111.754997, 111.955002, 0.0, 220934.0]
    return {'TEST.L': df}

# Load Env Var 
load_dotenv()
arctic_test_uri = os.getenv('ARCTICDB_TEST_URI')

# Fixture: Use TestDB Instead Of Actual LocalDB For Testing.
@pytest.fixture
def use_test_db(monkeypatch):
    monkeypatch.setattr(database, "arcticdb_local_uri", arctic_test_uri)

# Fixture: Return Test Database Instance
@pytest.fixture
def db(use_test_db):
    return database.connect_db()

# Fixture: Return Sample Tickers
@pytest.fixture
def sample_tickers():
    return get_sample_data()