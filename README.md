# Quant Finance Society

This project provides a collection of small tools to explore quantitative finance concepts.
The main page allows choosing between the following mini projects:

1. **Investment Strategy Simulator** – evaluate dollar-cost averaging (DCA), lump-sum investment, a direct comparison of the two and a simple moving average crossover strategy over the last five years.
2. **Stock Volatility Comparison** – visualise daily return distributions with simple boxplots.

## Structure

- **backend/** – FastAPI service that fetches historical prices via `yfinance` and performs the simulation.
- **frontend/** – React application built with Vite. It displays input forms and charts using Recharts.

## Running locally

1. Install Python dependencies:
   ```bash
   pip install fastapi uvicorn yfinance
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

