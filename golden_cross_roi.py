import argparse
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

MA_OPTIONS = {
    "10_50": (10, 50),
    "20_60": (20, 60),
    "50_200": (50, 200),
}

def download_data(ticker: str) -> pd.DataFrame:
    """Download historical price data."""
    return yf.download(ticker, start="2022-01-01", end="2024-01-01", progress=False)

def compute_ma(df: pd.DataFrame, short: int, long: int) -> None:
    """Add moving average columns."""
    df["MA_short"] = df["Close"].rolling(window=short).mean()
    df["MA_long"] = df["Close"].rolling(window=long).mean()

def compute_signals(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return golden and dead cross points."""
    df["Signal"] = 0
    df.loc[df["MA_short"] > df["MA_long"], "Signal"] = 1
    df["Crossover"] = df["Signal"].diff()
    golden = df[df["Crossover"] == 1]
    dead = df[df["Crossover"] == -1]
    return golden, dead

def pair_trades(golden: pd.DataFrame, dead: pd.DataFrame) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
    """Pair buy and sell dates for ROI calculation."""
    buy_dates = golden.index
    sell_dates = dead.index
    if len(buy_dates) == 0:
        return []
    sell_dates = sell_dates[sell_dates > buy_dates[0]]
    pairs = []
    for buy_date in buy_dates:
        valid = sell_dates[sell_dates > buy_date]
        if len(valid) == 0:
            break
        sell_date = valid[0]
        pairs.append((buy_date, sell_date))
        sell_dates = sell_dates[sell_dates > sell_date]
    return pairs

def compute_rois(df: pd.DataFrame, pairs: list[tuple[pd.Timestamp, pd.Timestamp]]) -> list[tuple[pd.Timestamp, pd.Timestamp, float]]:
    """Compute ROI for each trade pair."""
    rois = []
    for buy_date, sell_date in pairs:
        buy_price = df.loc[buy_date, "Close"]
        sell_price = df.loc[sell_date, "Close"]
        roi = (sell_price - buy_price) / buy_price * 100
        rois.append((buy_date, sell_date, roi))
    return rois

def plot(df: pd.DataFrame, golden: pd.DataFrame, dead: pd.DataFrame, short: int, long: int, ticker: str) -> None:
    """Visualise price, moving averages and crossovers."""
    plt.figure(figsize=(14, 6))
    plt.plot(df["Close"], label="Close Price", alpha=0.5)
    plt.plot(df["MA_short"], label=f"MA{short}", linestyle="--")
    plt.plot(df["MA_long"], label=f"MA{long}", linestyle="--")
    plt.scatter(golden.index, golden["Close"], marker="^", color="green", label="Golden Cross", s=100)
    plt.scatter(dead.index, dead["Close"], marker="v", color="red", label="Dead Cross", s=100)
    plt.title(f"Moving Average Crossover Strategy - {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate ROI based on moving average crossovers")
    parser.add_argument("ticker", help="Ticker symbol")
    parser.add_argument(
        "--option",
        choices=list(MA_OPTIONS.keys()),
        default="20_60",
        help="Moving average combination to use",
    )
    args = parser.parse_args()
    short, long = MA_OPTIONS[args.option]
    df = download_data(args.ticker)
    if df.empty:
        print("Failed to download data")
        return
    compute_ma(df, short, long)
    golden, dead = compute_signals(df)
    pairs = pair_trades(golden, dead)
    rois = compute_rois(df, pairs)
    for buy_date, sell_date, roi in rois:
        print("======= ROI =======")
        print("Buy date:", buy_date.date())
        print("Sell date:", sell_date.date())
        print("ROI (%):", round(roi, 2))
    if rois:
        avg_roi = sum(r[2] for r in rois) / len(rois)
        print("======= AVG ROI =======")
        print(round(avg_roi, 2))
    else:
        print("\nNo valid ROI calculation interval")
    plot(df, golden, dead, short, long, args.ticker)

if __name__ == "__main__":
    main()
