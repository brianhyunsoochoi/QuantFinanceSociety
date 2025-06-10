from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import yfinance as yf


class SimulateRequest(BaseModel):
    tickers: list[str]
    amounts: list[float]
    strategy: str  # "monthly", "lump_sum", "both", or "ma_crossover"


class VolatilityRequest(BaseModel):
    tickers: list[str]


class BaseBackend(ABC):
    """Interface for backend implementations."""

    @abstractmethod
    def simulate(self, data: SimulateRequest) -> dict:
        raise NotImplementedError

    @abstractmethod
    def volatility(self, data: VolatilityRequest) -> dict:
        raise NotImplementedError


class YFinanceBackend(BaseBackend):
    """Backend using yfinance for historical price data."""

    @staticmethod
    def moving_average_crossover(prices: pd.Series, cash: float,
                                 short: int = 3, long: int = 12) -> float:
        short_ma = prices.rolling(window=short).mean()
        long_ma = prices.rolling(window=long).mean()
        position = 0
        shares = 0.0
        for date in prices.index:
            s = short_ma.loc[date]
            l = long_ma.loc[date]
            if pd.isna(s) or pd.isna(l):
                continue
            price = prices.loc[date]
            if s > l and position == 0:
                shares = cash / price
                cash = 0.0
                position = 1
            elif s < l and position == 1:
                cash = shares * price
                shares = 0.0
                position = 0
        final_price = prices.iloc[-1]
        return cash + shares * final_price

    def simulate(self, data: SimulateRequest) -> dict:
        results = []
        end_date = datetime.today()
        start_date = end_date - timedelta(days=5 * 365)

        for ticker, amount in zip(data.tickers, data.amounts):
            try:
                df = yf.download(ticker, start=start_date, end=end_date, progress=False)
                if df.empty or "Close" not in df.columns:
                    raise ValueError("No data received")

                df.index = pd.to_datetime(df.index)

                if isinstance(df.columns, pd.MultiIndex):
                    close_series = df["Close", ticker]
                else:
                    close_series = df["Close"]

                monthly = close_series.resample("MS").first()
                if monthly.empty:
                    raise ValueError("Monthly resampled data is empty")

                if data.strategy == "monthly":
                    monthly_investment = amount / len(monthly)
                    shares = (monthly_investment / monthly).sum()
                    final_value = float(shares * monthly.iloc[-1])
                elif data.strategy == "lump_sum":
                    shares = amount / monthly.iloc[0]
                    final_value = float(shares * monthly.iloc[-1])
                elif data.strategy == "both":
                    monthly_investment = amount / len(monthly)
                    shares_monthly = (monthly_investment / monthly).sum()
                    shares_lump = amount / monthly.iloc[0]
                    final_monthly = float(shares_monthly * monthly.iloc[-1])
                    final_lump = float(shares_lump * monthly.iloc[-1])
                elif data.strategy == "ma_crossover":
                    final_value = float(self.moving_average_crossover(monthly, amount))
                else:
                    raise ValueError("Invalid strategy")

                price_data = [
                    {"date": d.strftime("%Y-%m") if hasattr(d, "strftime") else str(d),
                     "price": float(p)}
                    for d, p in monthly.items()
                ]

                if data.strategy == "both":
                    results.append({
                        "ticker": ticker,
                        "final_values": {
                            "monthly": round(final_monthly, 2),
                            "lump_sum": round(final_lump, 2),
                        },
                        "prices": price_data,
                    })
                else:
                    results.append({
                        "ticker": ticker,
                        "final_value": round(final_value, 2),
                        "prices": price_data,
                    })
            except Exception as e:
                results.append({
                    "ticker": ticker,
                    "final_value": None,
                    "prices": [],
                    "error": str(e),
                })
        return {"results": results}

    def volatility(self, data: VolatilityRequest) -> dict:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=5 * 365)
        results = []
        for ticker in data.tickers:
            try:
                df = yf.download(ticker, start=start_date, end=end_date, progress=False)
                if df.empty or "Close" not in df.columns:
                    raise ValueError("No data received")
                df["returns"] = df["Close"].pct_change().dropna()
                returns = df["returns"].dropna()
                summary = {
                    "min": float(returns.min()),
                    "q1": float(returns.quantile(0.25)),
                    "median": float(returns.median()),
                    "q3": float(returns.quantile(0.75)),
                    "max": float(returns.max()),
                    "std": float(returns.std()),
                }
                results.append({"ticker": ticker, **summary})
            except Exception as e:
                results.append({"ticker": ticker, "error": str(e)})
        return {"results": results}


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

backend_service: BaseBackend = YFinanceBackend()

def get_backend() -> BaseBackend:
    return backend_service


@app.post("/simulate")
def simulate_endpoint(
    data: SimulateRequest, backend: BaseBackend = Depends(get_backend)
):
    return backend.simulate(data)


@app.post("/volatility")
def volatility_endpoint(
    data: VolatilityRequest, backend: BaseBackend = Depends(get_backend)
):
    return backend.volatility(data)
