import numpy as np
import pandas as pd
import data.etf_query as etf_query


def fake_download_df():
    # Mimics yf.download output: MultiIndex columns (Price, Ticker)
    dates = pd.date_range("2024-01-01", periods=3)
    columns = pd.MultiIndex.from_product(
        [["Close", "Open", "Volume"], ["AAA", "BBB"]], names=["Price", "Ticker"]
    )
    df = pd.DataFrame(np.arange(18, dtype=float).reshape(3, 6), index=dates, columns=columns)
    df.iloc[0, df.columns.get_level_values("Ticker") == "BBB"] = np.nan  # BBB has no data on day 1
    return df


def test_get_stock_data_by_batch_splits_and_cleans(monkeypatch):
    # Replace the real network call with fake data
    monkeypatch.setattr(etf_query.yf, "download", lambda *a, **k: fake_download_df())

    result = etf_query.get_stock_data_by_batch(["AAA", "BBB"], period="1y", interval="1d")

    assert set(result) == {"AAA", "BBB"}
    expected_cols = ['Capital Gains', 'Close', 'Dividends', 'High', 'Low', 'Open', 'Stock Splits', 'Volume']
    for df in result.values():
        assert list(df.columns) == expected_cols
    # Missing columns filled with 0
    assert (result["AAA"]["Dividends"] == 0).all()
    # All-NaN rows dropped
    assert len(result["AAA"]) == 3
    assert len(result["BBB"]) == 2


def test_main_downloads_and_saves(monkeypatch):
    calls = {}

    def fake_get_data(tickers, period, interval):
        calls["tickers"] = tickers
        return {"X": "df"}

    def fake_save(data):
        calls["saved"] = data

    monkeypatch.setattr(etf_query, "get_stock_data_by_batch", fake_get_data)
    monkeypatch.setattr(etf_query, "save_tickers", fake_save)

    etf_query.main()

    assert len(calls["tickers"]) > 0  # read from data/tickers.json
    assert calls["saved"] == {"X": "df"}
