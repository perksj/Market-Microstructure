import time
import requests
import pandas as pd
from typing import Dict, List

BASE_URL = "https://api.binance.com"

class BinanceDataLoader:
    def __init__(self, symbol: str, depth_levels: int = 10):
        self.symbol = symbol.upper()
        self.depth_levels = depth_levels

    def _get(self, endpoint: str, params: Dict):
        response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def get_order_book(self) -> pd.DataFrame:
        """
        Returns top N levels of the limit order book as a DataFrame.
        """
        data = self._get(
            "/api/v3/depth",
            params={
                "symbol": self.symbol,
                "limit": self.depth_levels
            }
        )

        bids = [
            {"price": float(p), "volume": float(v), "side": "bid"}
            for p, v in data["bids"]
        ]
        asks = [
            {"price": float(p), "volume": float(v), "side": "ask"}
            for p, v in data["asks"]
        ]

        df = pd.DataFrame(bids + asks)
        df["timestamp"] = pd.Timestamp.utcnow()

        return df

    def get_recent_trades(self, limit: int = 500) -> pd.DataFrame:
        """
        Returns recent trades.
        """
        data = self._get(
            "/api/v3/trades",
            params={
                "symbol": self.symbol,
                "limit": limit
            }
        )

        df = pd.DataFrame(data)
        df = df.rename(columns={
            "price": "price",
            "qty": "quantity",
            "time": "timestamp"
        })

        df["price"] = df["price"].astype(float)
        df["quantity"] = df["quantity"].astype(float)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["is_buyer_maker"] = df["isBuyerMaker"]

        return df[["price", "quantity", "timestamp", "is_buyer_maker"]]
