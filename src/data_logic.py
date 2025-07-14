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


def get_current_portfolio_composition():
    orders = data_loader.load_orders()
    prices = data_loader.load_prices()
    
    if orders.empty or prices.empty:
        return pd.DataFrame()

    orders["Quantità"] = orders.apply(
        lambda row: row["Quantità"] if row["Operazione"] == "Buy" else -row["Quantità"],
        axis=1,
    )
    
    # Group by Ticker and sum quantities
    portfolio_qty = orders.groupby("Ticker")["Quantità"].sum().reset_index()
    portfolio_qty = portfolio_qty[portfolio_qty["Quantità"] > 0]
    
    # Get the latest prices for each ticker
    latest_prices = prices.groupby("Ticker")["Valore"].last().reset_index()
    latest_prices.columns = ["Ticker", "Prezzo_Attuale"]
    
    # Merge the portfolio quantities with the latest prices
    portfolio_composition = pd.merge(portfolio_qty, latest_prices, on="Ticker", how="left")
    
    # Calculate total value for each ticker
    portfolio_composition["Valore_Totale"] = portfolio_composition["Quantità"] * portfolio_composition["Prezzo_Attuale"]
    
    return portfolio_composition


def get_portfolio_evolution():
    orders = data_loader.load_orders()
    prices = data_loader.load_prices()

    if orders.empty or prices.empty:
        return pd.DataFrame()

    # Prepare orders data
    orders["Data"] = pd.to_datetime(orders["Data"])
    orders["Quantità"] = orders.apply(
        lambda row: row["Quantità"] if row["Operazione"] == "Buy" else -row["Quantità"], axis=1
    )
    orders["Spesa"] = orders["Quantità"] * orders["Prezzo"]
    
    # Prepare prices data
    prices["Data"] = pd.to_datetime(prices["Data"])
    
    # Create a complete date range from the minimum to the maximum date in both orders and prices
    start_date = min(prices["Data"].min(), orders["Data"].min())
    end_date = max(prices["Data"].max(), orders["Data"].max())
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 1. Calculate daily spend
    daily_spend = orders.groupby("Data")["Spesa"].sum()
    cumulative_spend = daily_spend.reindex(all_dates, fill_value=0).cumsum()
    
    # 2. Calculate daily quantities
    daily_qty = orders.groupby(["Data", "Ticker"])["Quantità"].sum().unstack(fill_value=0)
    cumulative_qty = daily_qty.reindex(all_dates, fill_value=0).cumsum().fillna(method='ffill').fillna(0)
    
    # 3. Prepare prices for each date
    daily_prices = prices.pivot(index="Data", columns="Ticker", values="Valore")
    daily_prices = daily_prices.reindex(all_dates).fillna(method='ffill').fillna(0)
    
    # 4. Calculate portfolio value for each date
    portfolio_values = []
    for date in all_dates:
        daily_value = 0
        for ticker in cumulative_qty.columns:
            if ticker in daily_prices.columns:
                qty = cumulative_qty.loc[date, ticker]
                price = daily_prices.loc[date, ticker]
                daily_value += qty * price
        portfolio_values.append(daily_value)
    
    # 5. Create result DataFrame
    result = pd.DataFrame({
        "Data": all_dates,
        "Soldi Spesi": cumulative_spend.values,
        "Valore Portafoglio": portfolio_values
    })
    
    return result


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
