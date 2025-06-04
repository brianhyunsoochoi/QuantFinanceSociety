import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from 'recharts'

export default function PriceChart({ data, tickers }) {
  return (
    <LineChart width={1000} height={600} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Legend />
      {tickers.map((t, idx) => (
        <Line key={t} type="monotone" dataKey={t} stroke={['#8884d8', '#82ca9d', '#ff7300', '#387908', '#d0ed57'][idx % 5]} />
      ))}
    </LineChart>
  )
}

