import ReactECharts from 'echarts-for-react'

import { ChartFrame } from './ChartFrame.jsx'

export function TopicClusterChart({ data = [] }) {
  const topics = [...data].sort((left, right) => (right.value || 0) - (left.value || 0))
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const item = params?.[0]?.data
        if (!item) return ''
        return `${item.name}<br/>Volume: ${item.value}<br/>Sentiment: ${item.sentiment}`
      },
    },
    grid: { left: 118, right: 28, top: 18, bottom: 28 },
    xAxis: {
      type: 'value',
      axisLabel: { color: '#9aa6bf' },
      splitLine: { lineStyle: { color: 'rgba(154, 166, 191, 0.12)' } },
    },
    yAxis: {
      type: 'category',
      data: topics.map((item) => item.name),
      axisLabel: { color: '#c9d4ea', overflow: 'truncate', width: 142 },
      axisLine: { lineStyle: { color: '#283043' } },
    },
    series: [
      {
        type: 'bar',
        data: topics.map((item) => {
          const sentiment = Number(item.sentiment_score ?? 0)
          return {
            value: item.value ?? 0,
            name: item.name,
            sentiment: sentiment.toFixed(2),
            itemStyle: {
              color: sentiment < -0.2 ? '#ff5d8f' : sentiment > 0.2 ? '#54f5a8' : '#f5c44b',
              borderRadius: [0, 6, 6, 0],
            },
          }
        }),
        barWidth: 18,
        label: {
          show: true,
          position: 'right',
          color: '#c9d4ea',
        },
      },
    ],
  }

  return (
    <ChartFrame title="Topic Clusters" description="Volume by detected topic" empty={!data.length}>
      <ReactECharts option={option} className="chart-surface" notMerge />
    </ChartFrame>
  )
}
