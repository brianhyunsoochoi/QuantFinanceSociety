import React, { useState } from "react";
import axios from "axios";

function App() {
  const [numTickers, setNumTickers] = useState(2);
  const [tickers, setTickers] = useState(["", ""]);
  const [strategy, setStrategy] = useState("monthly");
  const [amount, setAmount] = useState(10000);
  const [results, setResults] = useState([]);

  const handleTickerChange = (index, value) => {
    const updated = [...tickers];
    updated[index] = value.toUpperCase();
    setTickers(updated);
  };

  const simulate = async () => {
    const response = await axios.post("http://localhost:8000/simulate", {
      tickers: tickers.filter((t) => t),
      strategy,
      amount,
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
        }}
      />

      <br />
      {[...Array(numTickers)].map((_, i) => (
        <input
          key={i}
          placeholder={`Ticker ${i + 1}`}
          value={tickers[i] || ""}
          onChange={(e) => handleTickerChange(i, e.target.value)}
        />
      ))}

      <br />
      <label>Strategy:</label>
      <select onChange={(e) => setStrategy(e.target.value)}>
        <option value="monthly">Invest Monthly</option>
        <option value="lump_sum">Lump Sum</option>
      </select>

      <br />
      <label>Investment Amount (USD):</label>
      <input type="number" value={amount} onChange={(e) => setAmount(parseFloat(e.target.value))} />

      <br />
      <button onClick={simulate}>Simulate</button>

      <hr />
      {results.length > 0 && (
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
      )}
    </div>
  );
}

export default App;