import React, { useState } from 'react';
import axios from 'axios';
import BoxPlotChart from './components/BoxPlotChart.jsx';

export default function VolatilityComparison({ onBack }) {
  const [tickers, setTickers] = useState(['AAPL', 'TSLA']);
  const [results, setResults] = useState([]);

  const analyze = async () => {
    const response = await axios.post('http://localhost:8000/volatility', { tickers });
    setResults(response.data.results);
  };

  return (
    <div style={{ padding: '20px', color: 'white' }}>
      <button onClick={onBack} style={{ marginBottom: '20px' }}>Back</button>
      <h1>Stock Volatility Comparison</h1>
      <textarea rows={3} style={{ width: '100%' }} value={tickers.join(',')}
        onChange={e => setTickers(e.target.value.split(',').map(t => t.trim().toUpperCase()).filter(Boolean))}/>
      <button onClick={analyze} style={{ marginTop: '10px' }}>Analyze</button>
      {results.length > 0 && (
        <div style={{marginTop:'20px'}}>
          <BoxPlotChart data={results} width={600} height={400} />
        </div>
      )}
    </div>
  );
}
