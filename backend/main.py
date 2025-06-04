from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yfinance as yf
from datetime import datetime, timedelta

app = FastAPI()

# CORS 설정 (React와 연결 위해)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포에선 도메인 제한 필요
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
            df = yf.download(ticker, start=start_date, end=end_date)
            monthly = df["Close"].resample("ME").first()

            if monthly.empty:
                raise ValueError("no data")

            if data.strategy == "monthly":
                monthly_investment = amount / len(monthly)
                shares = monthly_investment / monthly
                total_shares = shares.sum()
            else:
                first_price = monthly.iloc[0]
                total_shares = amount / first_price

            final_price = monthly.iloc[-1]
            final_value = float(total_shares * final_price)

            price_data = [
                {"date": d.strftime("%Y-%m"), "price": float(p)}
                for d, p in monthly.items()
            ]

            results.append(
                {
                    "ticker": ticker,
                    "final_value": round(final_value, 2),
                    "prices": price_data,
                }
            )

        except Exception:
            results.append({"ticker": ticker, "final_value": None, "prices": []})

    return {"results": results}
