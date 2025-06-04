import React from 'react';

export default function BoxPlotChart({ data, width = 600, height = 400 }) {
  if (!data || data.length === 0) return null;
  const values = data.flatMap(d => [d.min, d.max]);
  const yMin = Math.min(...values);
  const yMax = Math.max(...values);
  const padding = 40;
  const plotWidth = width - padding * 2;
  const plotHeight = height - padding * 2;
  const scaleY = v => padding + plotHeight - ((v - yMin) / (yMax - yMin)) * plotHeight;
  const boxWidth = plotWidth / data.length / 2;

  return (
    <svg width={width} height={height} style={{ background: 'white' }}>
      {data.map((d, i) => {
        const x = padding + (i + 0.5) * (plotWidth / data.length);
        return (
          <g key={d.ticker}>
            <line x1={x} x2={x} y1={scaleY(d.min)} y2={scaleY(d.max)} stroke="black" />
            <rect x={x - boxWidth / 2} y={scaleY(d.q3)} width={boxWidth} height={scaleY(d.q1) - scaleY(d.q3)} fill="#69b3a2" stroke="black" />
            <line x1={x - boxWidth / 2} x2={x + boxWidth / 2} y1={scaleY(d.median)} y2={scaleY(d.median)} stroke="black" />
            <text x={x} y={height - padding / 2} textAnchor="middle" fontSize="12">{d.ticker}</text>
          </g>
        );
      })}
    </svg>
  );
}
