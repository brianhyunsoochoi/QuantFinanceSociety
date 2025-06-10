import React, { useState } from "react";
import axios from "axios";
import ResultChart from "./Chart.jsx";
import PriceChart from "./PriceChart.jsx";

function StrategySimulator({ onBack }) {
  const [numTickers, setNumTickers] = useState(1);
  const [tickers, setTickers] = useState(["AAPL"]);
  const [amounts, setAmounts] = useState([1000]);
  const [strategy, setStrategy] = useState("monthly");
  const [results, setResults] = useState([]);

  const priceData = React.useMemo(() => {
    if (results.length === 0) return [];
    const length = results[0].prices.length;
    const arr = [];
    for (let i = 0; i < length; i++) {
      const entry = { date: results[0].prices[i].date };
      results.forEach((r) => {
        entry[r.ticker] = r.prices[i]?.price;
      });
      arr.push(entry);
    }
    return arr;
  }, [results]);

  const handleTickerChange = (index, value) => {
    const updated = [...tickers];
    updated[index] = value.toUpperCase();
    setTickers(updated);
  };

  const handleAmountChange = (index, value) => {
    const updated = [...amounts];
    updated[index] = parseFloat(value) || 0;
    setAmounts(updated);
  };

  const simulate = async () => {
    const validTickers = tickers.filter((t) => t);
    const usedAmounts = amounts.slice(0, validTickers.length);
    const response = await axios.post("http://localhost:8000/simulate", {
      tickers: validTickers,
      amounts: usedAmounts,
      strategy,
    });
    setResults(response.data.results);
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "flex-start",
        minHeight: "100vh",
        padding: "40px 20px",
        backgroundColor: "#1e1e1e",
        color: "white",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "1000px",
          display: "flex",
          flexDirection: "column",
          gap: "16px",
        }}
      >
        <button onClick={onBack}>Back</button>
        <h1 style={{ textAlign: "center" }}>Investment Strategy Simulator</h1>

        <label>Ticker Count:</label>
        <input
          type="number"
          value={numTickers}
          min={1}
          max={5}
          onChange={(e) => {
            const count = parseInt(e.target.value);
            setNumTickers(count);
            setTickers((prev) => [...prev, ...Array(count - prev.length).fill("")]);
            setAmounts((prev) => [...prev, ...Array(count - prev.length).fill(1000)]);
          }}
          style={{ width: "98%", padding: "8px" }}
        />

        {[...Array(numTickers)].map((_, i) => (
          <div key={i} style={{ display: "flex", gap: "8px", marginBottom: "8px" }}>
            <input
              placeholder={`Ticker ${i + 1}`}
              value={tickers[i] || ""}
              onChange={(e) => handleTickerChange(i, e.target.value)}
              style={{ flex: 1, padding: "8px" }}
            />
            <input
              type="number"
              value={amounts[i]}
              onChange={(e) => handleAmountChange(i, e.target.value)}
              style={{ width: "120px", padding: "8px" }}
            />
          </div>
        ))}

        <label>Strategy:</label>
        <select
          onChange={(e) => setStrategy(e.target.value)}
          style={{ width: "100%", padding: "8px" }}
        >
          <option value="monthly">Invest Monthly</option>
          <option value="lump_sum">Lump Sum</option>
          <option value="both">Monthly vs Lump Sum</option>
          <option value="ma_crossover">Moving Average Crossover</option>
        </select>

        <button
          onClick={simulate}
          style={{
            width: "100%",
            padding: "12px",
            backgroundColor: "white",
            color: "black",
            border: "none",
            borderRadius: "6px",
            fontWeight: "bold",
            cursor: "pointer",
          }}
        >
          Simulate
        </button>

        {results.length > 0 && (
          <>
            {strategy === "both" ? (
              <table style={{ width: "100%", textAlign: "left", marginTop: "20px" }}>
                <thead>
                  <tr>
                    <th>Ticker</th>
                    <th>Monthly (USD)</th>
                    <th>Lump Sum (USD)</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((r) => (
                    <tr key={r.ticker}>
                      <td>{r.ticker}</td>
                      <td>{r.final_values ? `$${r.final_values.monthly}` : "Error"}</td>
                      <td>{r.final_values ? `$${r.final_values.lump_sum}` : "Error"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <table style={{ width: "100%", textAlign: "left", marginTop: "20px" }}>
                <thead>
                  <tr>
                    <th>Ticker</th>
                    <th>Final Value (USD)</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((r) => (
                    <tr key={r.ticker}>
                      <td>{r.ticker}</td>
                      <td>{r.final_value ? `$${r.final_value}` : "Error"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}

            <ResultChart data={results} />
            <PriceChart data={priceData} tickers={results.map((r) => r.ticker)} />
          </>
        )}
      </div>
    </div>
  );
}
export default StrategySimulator;
