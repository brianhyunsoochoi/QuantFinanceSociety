from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def moving_average_crossover(prices: pd.Series, cash: float,
                              short: int = 3, long: int = 12) -> float:
    """Simple moving average crossover strategy."""
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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulateRequest(BaseModel):
    tickers: list[str]
    amounts: list[float]
    strategy: str  # "monthly", "lump_sum", "both", or "ma_crossover"

@app.post("/simulate")
def simulate(data: SimulateRequest):
    results = []
    end_date = datetime.today()
    start_date = end_date - timedelta(days=5 * 365)

    for ticker, amount in zip(data.tickers, data.amounts):
        try:
            print(f"\n▶ Processing: {ticker}, Amount: {amount}")
            print(f"▶ Date range: {start_date.date()} ~ {end_date.date()}")

            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
            print(f"✅ Raw data head:\n{df.head()}")

            if df.empty or "Close" not in df.columns:
                raise ValueError("No data received")

            df.index = pd.to_datetime(df.index)

            if isinstance(df.columns, pd.MultiIndex):
                close_series = df["Close", ticker]
            else:
                close_series = df["Close"]

            monthly = close_series.resample("MS").first()

            print(f"✅ Monthly resampled data:\n{monthly.head()}")
            print("index type:", type(monthly.index[0]))

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
                final_value = float(moving_average_crossover(monthly, amount))
            else:
                raise ValueError("Invalid strategy")

            price_data = [
                {"date": d.strftime("%Y-%m") if hasattr(d, "strftime") else str(d), "price": float(p)}
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
            print(f"❌ Error while processing {ticker}: {e}")
            results.append({
                "ticker": ticker,
                "final_value": None,
                "prices": [],
                "error": str(e),
            })

    return {"results": results}
class VolatilityRequest(BaseModel):
    tickers: list[str]

@app.post("/volatility")
def volatility(data: VolatilityRequest):
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
