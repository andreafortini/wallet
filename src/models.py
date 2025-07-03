"""Data models"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Operation(Enum):
    BUY = "BUY"
    SELL = "SELL"


class Category(Enum):
    STOCK = "STOCK"
    BOND = "BOND"


class Orders(BaseModel):
    ticker: str
    isin: str
    quantity: int
    price: float
    data: datetime
    operation: Operation


class Prices(BaseModel):
    ticker: str
    isin: str
    value: float
    date: datetime


class Securities:
    ticker: str
    isin: str
    name: str
    category: Category
