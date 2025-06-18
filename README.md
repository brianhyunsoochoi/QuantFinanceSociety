# Quant Finance Society

This project provides a collection of small tools to explore quantitative finance concepts.
The main page allows choosing between the following mini projects:

1. **Investment Strategy Simulator** – evaluate dollar-cost averaging (DCA), lump-sum investment, a direct comparison of the two and a configurable moving average crossover strategy over the last five years. When comparing monthly vs lump sum the final values are shown in two separate charts.
2. **Stock Volatility Comparison** – visualise daily return distributions with simple boxplots.

## Structure

- **backend/** – FastAPI service that fetches historical prices via `yfinance` and performs the simulation. The `BaseBackend` interface allows swapping the implementation (e.g. `YFinanceBackend`).
- **frontend/** – React application built with Vite. It displays input forms and charts using Recharts.

## Running locally

1. Install Python dependencies:
   ```bash
   pip install fastapi uvicorn yfinance pandas matplotlib
   ```
2. Start the backend:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```
3. Install frontend dependencies and start the dev server:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

The frontend expects the backend at `http://localhost:8000`.
Once both servers are running, open the frontend in your browser and choose a project from the main menu.


## Moving Average ROI Script

A small command-line utility `golden_cross_roi.py` calculates the return on investment when buying at golden crosses and selling at dead crosses. It downloads two years of daily prices with `yfinance` and supports three moving average combinations:

- **10 & 50**
- **20 & 60** (default)
- **50 & 200**

This script targets **Python 3.9** and requires `pandas`, `matplotlib` and
`yfinance`.
Run it with a ticker symbol and an optional `--option` argument:

```bash
python golden_cross_roi.py AAPL --option 10_50
```

The script prints each trade's ROI, the average ROI and shows a chart with the moving averages and crossover points.
