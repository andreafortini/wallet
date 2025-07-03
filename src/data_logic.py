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


# TODO: review the function
def get_current_portfolio_composition():
    orders = data_loader.load_orders()
    if orders.empty:
        return pd.DataFrame()

    orders["Quantità"] = orders.apply(
        lambda row: row["Quantità"] if row["Operazione"] == "Buy" else -row["Quantità"],
        axis=1,
    )
    agg = orders.groupby("Ticker")["Quantità"].sum().reset_index()
    return agg[agg["Quantità"] > 0]


# TODO: review the function
def get_portfolio_evolution():
    orders = data_loader.load_orders()
    prices = data_loader.load_prices()

    if orders.empty or prices.empty:
        return pd.DataFrame()

    orders["Quantità"] = orders.apply(
        lambda row: row["Quantità"] if row["Operazione"] == "Buy" else -row["Quantità"],
        axis=1,
    )
    orders["Spesa"] = orders["Quantità"] * orders["Prezzo"]
    orders = orders.sort_values("Data")
    prices = prices.sort_values("Data")

    spend_data = orders.groupby("Data")["Spesa"].sum().cumsum().reset_index()
    spend_data.columns = ["Data", "Soldi Spesi"]

    merged = pd.merge(
        prices, orders[["Ticker", "ISIN", "Quantità"]], on=["Ticker", "ISIN"]
    )
    merged["Valore"] = merged["Valore"] * merged["Quantità"]
    value_data = merged.groupby("Data")["Valore"].sum().reset_index()
    value_data.columns = ["Data", "Valore Portafoglio"]

    df = pd.merge(spend_data, value_data, on="Data", how="outer").sort_values("Data")
    df.fillna(method="ffill", inplace=True)
    return df


# TODO: review the function
def get_summary_metrics():
    orders = data_loader.load_orders()
    prices = data_loader.load_prices()

    if orders.empty or prices.empty:
        return {}

    orders["Quantità"] = orders.apply(
        lambda row: row["Quantità"] if row["Operazione"] == "Buy" else -row["Quantità"],
        axis=1,
    )
    net_qty = orders.groupby(["Ticker", "ISIN"])["Quantità"].sum().reset_index()
    net_qty = net_qty[net_qty["Quantità"] > 0]

    latest_prices = (
        prices.sort_values("Data").groupby(["Ticker", "ISIN"]).last().reset_index()
    )
    merged = pd.merge(net_qty, latest_prices, on=["Ticker", "ISIN"])
    merged["Valore Attuale"] = merged["Quantità"] * merged["Valore"]
    total_value = merged["Valore Attuale"].sum()

    orders["Spesa"] = orders["Prezzo"] * orders["Quantità"]
    total_spent = orders[orders["Operazione"] == "Buy"]["Spesa"].sum()
    total_gained = orders[orders["Operazione"] == "Sell"]["Spesa"].sum()
    net_spent = total_spent - total_gained

    profit = total_value - net_spent
    perc = (profit / net_spent) * 100 if net_spent else 0

    return {
        "total_value": round(total_value, 2),
        "net_spent": round(net_spent, 2),
        "profit": round(profit, 2),
        "percent": round(perc, 2),
    }
