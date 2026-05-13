import ReactECharts from 'echarts-for-react'

import { ChartFrame } from './ChartFrame.jsx'

const indicators = [
  { name: 'Negative', max: 1 },
  { name: 'Bot Impact', max: 1 },
  { name: 'Speed', max: 1 },
  { name: 'Controversy', max: 1 },
  { name: 'Trend Shift', max: 1 },
]

export function RiskRadarChart({ data }) {
  const values = data
    ? [
        data.negative_sentiment,
        data.bot_impact,
        data.propagation_speed,
        data.controversy,
        data.trend_shift,
      ]
    : []

  const option = {
    color: ['#42f5d7'],
    radar: {
      indicator: indicators,
      radius: '66%',
      axisName: { color: '#c9d4ea' },
      splitLine: { lineStyle: { color: 'rgba(154, 166, 191, 0.18)' } },
      splitArea: { areaStyle: { color: ['rgba(66, 245, 215, 0.04)', 'rgba(66, 245, 215, 0.01)'] } },
      axisLine: { lineStyle: { color: 'rgba(154, 166, 191, 0.2)' } },
    },
    series: [
      {
        type: 'radar',
        data: [{ value: values, name: 'Risk Factors' }],
        areaStyle: { color: 'rgba(66, 245, 215, 0.22)' },
        lineStyle: { width: 2 },
        symbolSize: 5,
      },
    ],
    tooltip: {},
  }

  return (
    <ChartFrame title="Risk Radar" description="Composite signal strength" empty={!data}>
      <ReactECharts option={option} className="chart-surface" notMerge />
    </ChartFrame>
  )
}

