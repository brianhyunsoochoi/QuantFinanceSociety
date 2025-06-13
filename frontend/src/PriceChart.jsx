import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from 'recharts'

export default function PriceChart({ data, tickers }) {
  const colors = ['#8884d8', '#82ca9d', '#ff7300', '#387908', '#d0ed57']
  return (
    <LineChart width={1000} height={600} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Legend />
      {tickers.map((t, idx) => (
        <Line
          key={t}
          type="monotone"
          dataKey={t}
          stroke={colors[idx % colors.length]}
        />
      ))}
      {tickers.map((t) => (
        <>
          {data.length > 0 && data[0][`${t}_short`] !== undefined && (
            <Line
              key={`${t}_short`}
              type="monotone"
              dataKey={`${t}_short`}
              stroke="#cccccc"
              strokeDasharray="5 5"
            />
          )}
          {data.length > 0 && data[0][`${t}_long`] !== undefined && (
            <Line
              key={`${t}_long`}
              type="monotone"
              dataKey={`${t}_long`}
              stroke="#ff0000"
              strokeDasharray="3 3"
            />
          )}
        </>
      ))}
    </LineChart>
  )
}

