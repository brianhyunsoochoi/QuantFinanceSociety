import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from 'recharts'

export default function ResultChart({ data }) {
  if (!data || data.length === 0) return null
  const first = data[0]
  return (
    <BarChart width={1000} height={600} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="ticker" />
      <YAxis />
      <Tooltip />
      <Legend />
      {first.final_values ? (
        <>
          <Bar dataKey="final_values.monthly" fill="#8884d8" name="Monthly" barSize={20}/>
          <Bar dataKey="final_values.lump_sum" fill="#82ca9d" name="Lump Sum" barSize={20}/>
        </>
      ) : (
        <Bar dataKey="final_value" fill="#FFFFFF" barSize={20}/>
      )}
    </BarChart>
  )
}
