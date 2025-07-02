"""Read/write operations and data"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
ORDERS_FILE = DATA_DIR / "orders.csv"
SECURITIES_FILE = DATA_DIR / "securities.csv"
PRICES_FILE = DATA_DIR / "prices.csv"

for file in [ORDERS_FILE, SECURITIES_FILE, PRICES_FILE]:
    if not file.exists():
        file.write_text("")


def save_order(ticker, isin, quantity, price, date, operation):
    df = load_orders()
    new_row = pd.DataFrame(
        [
            {
                "Ticker": ticker,
                "ISIN": isin,
                "Quantità": quantity,
                "Prezzo": price,
                "Data": pd.to_datetime(date),
                "Operazione": operation,
            }
        ]
    )
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(ORDERS_FILE, index=False)


def load_orders():
    if ORDERS_FILE.stat().st_size == 0:
        return pd.DataFrame(
            columns=["Ticker", "ISIN", "Quantità", "Prezzo", "Data", "Operazione"]
        )
    return pd.read_csv(ORDERS_FILE, parse_dates=["Data"])


def save_security(ticker, isin, fullname, category):
    df = load_securities()
    new_row = pd.DataFrame(
        [{"Ticker": ticker, "ISIN": isin, "Nome": fullname, "Categoria": category}]
    )
    df = pd.concat([df, new_row], ignore_index=True)
    df.drop_duplicates(subset=["ISIN"], keep="last", inplace=True)
    df.to_csv(SECURITIES_FILE, index=False)


def load_securities():
    if SECURITIES_FILE.stat().st_size == 0:
        return pd.DataFrame(columns=["Ticker", "ISIN", "Nome", "Categoria"])
    return pd.read_csv(SECURITIES_FILE)


def save_price(ticker, isin, value, date):
    df = load_prices()
    new_row = pd.DataFrame(
        [
            {
                "Ticker": ticker,
                "ISIN": isin,
                "Valore": value,
                "Data": pd.to_datetime(date),
            }
        ]
    )
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(PRICES_FILE, index=False)


def load_prices():
    if PRICES_FILE.stat().st_size == 0:
        return pd.DataFrame(columns=["Ticker", "ISIN", "Valore", "Data"])
    return pd.read_csv(PRICES_FILE, parse_dates=["Data"])
