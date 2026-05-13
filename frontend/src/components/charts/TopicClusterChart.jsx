import ReactECharts from 'echarts-for-react'

import { ChartFrame } from './ChartFrame.jsx'

export function TopicClusterChart({ data = [] }) {
  const option = {
    color: ['#8bff72'],
    tooltip: { trigger: 'axis' },
    grid: { left: 88, right: 20, top: 18, bottom: 28 },
    xAxis: {
      type: 'value',
      axisLabel: { color: '#9aa6bf' },
      splitLine: { lineStyle: { color: 'rgba(154, 166, 191, 0.12)' } },
    },
    yAxis: {
      type: 'category',
      data: data.map((item) => item.name),
      axisLabel: { color: '#c9d4ea' },
      axisLine: { lineStyle: { color: '#283043' } },
    },
    series: [
      {
        type: 'bar',
        data: data.map((item) => item.value),
        barWidth: 18,
        itemStyle: {
          borderRadius: [0, 6, 6, 0],
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

