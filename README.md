# Investment Strategy Simulator

This project provides a simple web application to compare dollar-cost averaging (DCA) and lump-sum investment strategies over the last five years.

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

