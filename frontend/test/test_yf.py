# test_yfinance.py
import yfinance as yf
from datetime import datetime, timedelta

ticker = "AAPL"  # 또는 "MSFT", "GOOGL" 등 실제 티커
start_date = datetime.today() - timedelta(days=5 * 365)
end_date = datetime.today()

df = yf.download(ticker, start=start_date, end=end_date)

print(f"✅ Downloaded {ticker} data")
print(df.head())

if df.empty:
    print("❌ 데이터가 비어 있습니다.")
else:
    print("✅ 데이터가 정상적으로 로드되었습니다.")
