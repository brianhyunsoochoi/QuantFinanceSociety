import React, { useState } from "react";
import axios from "axios";
import ResultChart from "./Chart.jsx";
import PriceChart from "./PriceChart.jsx";

function App() {
  const [numTickers, setNumTickers] = useState(1);
  const [tickers, setTickers] = useState([""]);
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
    <div style={{ padding: 30 }}>
      <h1>📊 Investment Strategy Simulator</h1>

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
      />

      <br />
      {[...Array(numTickers)].map((_, i) => (
        <div key={i} style={{ marginBottom: 4 }}>
          <input
            placeholder={`Ticker ${i + 1}`}
            value={tickers[i] || ""}
            onChange={(e) => handleTickerChange(i, e.target.value)}
          />
          <input
            type="number"
            style={{ marginLeft: 4 }}
            value={amounts[i]}
            onChange={(e) => handleAmountChange(i, e.target.value)}
          />
        </div>
      ))}

      <br />
      <label>Strategy:</label>
      <select onChange={(e) => setStrategy(e.target.value)}>
        <option value="monthly">Invest Monthly</option>
        <option value="lump_sum">Lump Sum</option>
      </select>

      <br />
      <button onClick={simulate}>Simulate</button>

      <hr />
      {results.length > 0 && (
        <>
          <table>
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
          <ResultChart data={results} />
          <PriceChart data={priceData} tickers={results.map((r) => r.ticker)} />
        </>
      )}
    </div>
  );
}

export default App;
