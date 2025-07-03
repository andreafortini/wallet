"""Business logic to manipulate data"""

import pandas as pd

from src import data_loader


def get_isin():
    df = data_loader.load_securities()
    return df["ISIN"].unique().tolist()


def get_ticker():
    df = data_loader.load_securities()
    return df["Ticker"].unique().tolist()


def get_ticker_from_isin(isin: str):
    df = data_loader.load_securities()
    detail = df[df["ISIN"] == isin].iloc[0]
    return detail["Ticker"]


def get_isin_from_ticker(ticker: str):
    df = data_loader.load_securities()
    detail = df[df["Ticker"] == ticker].iloc[0]
    return detail["ISIN"]
