import pandas as pd, arcticdb as adb
from app.database import connect_db, save_tickers, delete_library

# Test ConnectDb Function - Must Return Arctic DB Instance
def test_connect_db(use_test_db):
    db = connect_db()
    assert isinstance(db, adb.Arctic)

# Test Saving Tickers Function - Must Have Daily Price Library And TEST.L Symbol From Sample Test Data
def test_tickers_save(db, sample_tickers):
    save_tickers(db, sample_tickers)
    assert 'daily_price' in db.list_libraries()
    lib = db['daily_price']
    assert 'TEST.L' in lib.list_symbols()

# Test Valid Library Deletion - Print Successful Library Deletion Statement
def test_existing_library(db, capsys):
    db.create_library("testing")
    delete_library(db, "testing")
    captured = capsys.readouterr()
    assert captured.out == f"Library 'testing' deleted successfully.\n"

# Test Invalid Library Deletion - Must Print Error Statement
def test_non_existing_library(db, capsys):
    delete_library(db, "helloworld")
    captured = capsys.readouterr()
    assert captured.out == f"Library 'helloworld' does not exists.\n"