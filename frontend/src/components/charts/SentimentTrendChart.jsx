import ReactECharts from 'echarts-for-react'

import { formatHour } from '../../utils/formatters.js'
import { ChartFrame } from './ChartFrame.jsx'

export function SentimentTrendChart({ data = [], focusNegative = false }) {
  const option = {
    color: ['#54f5a8', '#f5c44b', '#ff5d8f'],
    tooltip: { trigger: 'axis' },
    legend: {
      top: 0,
      textStyle: { color: '#9aa6bf' },
    },
    grid: { left: 34, right: 18, bottom: 30, top: 46, containLabel: true },
    xAxis: {
      type: 'category',
      data: data.map((point) => formatHour(point.time)),
      axisLine: { lineStyle: { color: '#283043' } },
      axisLabel: { color: '#9aa6bf' },
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#9aa6bf' },
      splitLine: { lineStyle: { color: 'rgba(154, 166, 191, 0.12)' } },
    },
    series: [
      {
        name: 'Positive',
        type: 'line',
        smooth: true,
        data: data.map((point) => point.positive ?? 0),
        areaStyle: { opacity: focusNegative ? 0.02 : 0.08 },
        lineStyle: { opacity: focusNegative ? 0.45 : 1 },
      },
      {
        name: 'Neutral',
        type: 'line',
        smooth: true,
        data: data.map((point) => point.neutral ?? 0),
        lineStyle: { opacity: focusNegative ? 0.45 : 1 },
      },
      {
        name: 'Negative',
        type: 'line',
        smooth: true,
        data: data.map((point) => point.negative ?? 0),
        areaStyle: { opacity: focusNegative ? 0.24 : 0.12 },
        lineStyle: { width: focusNegative ? 4 : 2 },
        symbolSize: focusNegative ? 8 : 5,
      },
    ],
  }

  return (
    <ChartFrame title="Sentiment Trend" description="Hourly public opinion balance" empty={!data.length}>
      <ReactECharts option={option} className="chart-surface" notMerge />
    </ChartFrame>
  )
}
