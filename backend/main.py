from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

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
    strategy: str  # "monthly" or "lump_sum"

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
                shares = monthly_investment / monthly
                total_shares = shares.sum()
            else:
                first_price = monthly.iloc[0]
                total_shares = amount / first_price

            final_price = monthly.iloc[-1]

            product = total_shares * final_price
            if hasattr(product, "item"):
                final_value = product.item()
            elif hasattr(product, "iloc"):
                final_value = product.iloc[0]
            else:
                final_value = float(product)

            price_data = [
                {"date": d.strftime("%Y-%m") if hasattr(d, "strftime") else str(d), "price": float(p)}
                for d, p in monthly.items()
            ]

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
