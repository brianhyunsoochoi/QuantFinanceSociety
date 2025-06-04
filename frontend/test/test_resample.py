import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 설정
ticker = "AAPL"
start_date = datetime.today() - timedelta(days=5 * 365)
end_date = datetime.today()

# 다운로드
df = yf.download(ticker, start=start_date, end=end_date)

print("✅ df.columns:")
print(df.columns)

# ✅ 확인 1: MultiIndex인지 체크
if isinstance(df.columns, pd.MultiIndex):
    print("❗️ df.columns is a MultiIndex → 문제 생길 수 있음")
else:
    print("✅ df.columns is normal (single-level)")

# ✅ 확인 2: 'Close' 컬럼 추출 후 .resample("M")
try:
    close_series = df["Close"]
    print("\n✅ Close series preview:")
    print(close_series.head())

    # 인덱스 강제 datetime
    df.index = pd.to_datetime(df.index)

    # resample
    monthly = close_series.resample("M").first()
    print("\n✅ Monthly resampled preview:")
    print(monthly.head())

    # 시도: 날짜 포맷
    for d, p in monthly.items():
        formatted = d.strftime("%Y-%m")  # 여기서 실패할 수 있음
        print(f"{formatted}: {p}")

    print("\n✅ strftime 통과 ✅ 문제 없음")

except Exception as e:
    print(f"\n❌ Error: {e}")