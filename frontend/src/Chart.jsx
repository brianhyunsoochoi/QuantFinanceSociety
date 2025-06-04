import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts'

export default function ResultChart({ data }) {
  return (
    <BarChart width={500} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="ticker" />
      <YAxis />
      <Tooltip />
      <Bar dataKey="final_value" fill="#8884d8" />
    </BarChart>
  )
}
