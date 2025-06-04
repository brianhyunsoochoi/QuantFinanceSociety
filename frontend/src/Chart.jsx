import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts'

export default function ResultChart({ data }) {
  return (
    <BarChart width={1000} height={600} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="ticker" />
      <YAxis />
      <Tooltip />
      <Bar dataKey="final_value" fill="#FFFFFF" barSize={20}/>
    </BarChart>
  )
}
