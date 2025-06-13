import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from 'recharts'

export default function ResultChart({ data }) {
  if (!data || data.length === 0) return null
  const first = data[0]

  if (first.final_values) {
    const monthlyData = data.map((d) => ({ ticker: d.ticker, value: d.final_values.monthly }))
    const lumpData = data.map((d) => ({ ticker: d.ticker, value: d.final_values.lump_sum }))
    return (
      <>
        <h3 style={{ textAlign: 'center' }}>Monthly Investment</h3>
        <BarChart width={1000} height={300} data={monthlyData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="ticker" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#8884d8" name="Monthly" barSize={20} />
        </BarChart>
        <h3 style={{ textAlign: 'center', marginTop: '20px' }}>Lump Sum Investment</h3>
        <BarChart width={1000} height={300} data={lumpData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="ticker" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#82ca9d" name="Lump Sum" barSize={20} />
        </BarChart>
      </>
    )
  }

  return (
    <BarChart width={1000} height={600} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="ticker" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Bar dataKey="final_value" fill="#FFFFFF" barSize={20} />
    </BarChart>
  )
}
