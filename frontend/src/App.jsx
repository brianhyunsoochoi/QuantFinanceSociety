import React, { useState } from 'react';
import StrategySimulator from './StrategySimulator.jsx';
import VolatilityComparison from './VolatilityComparison.jsx';

export default function App() {
  const [page, setPage] = useState('home');

  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    backgroundColor: '#1e1e1e',
    color: 'white',
    gap: '16px',
    padding: '40px 20px',
  };

  if (page === 'simulator') {
    return <StrategySimulator onBack={() => setPage('home')} />;
  }
  if (page === 'volatility') {
    return <VolatilityComparison onBack={() => setPage('home')} />;
  }

  return (
    <div style={containerStyle}>
      <h1>Quant Finance Projects</h1>
      <button onClick={() => setPage('simulator')} style={{padding:'12px', width:'260px'}}>Investment Strategy Simulator</button>
      <button onClick={() => setPage('volatility')} style={{padding:'12px', width:'260px'}}>Stock Volatility Comparison</button>
    </div>
  );
}
