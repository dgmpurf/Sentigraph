import ReactECharts from 'echarts-for-react'

import { ChartFrame } from './ChartFrame.jsx'

export function PlatformHeatmapChart({ data = [] }) {
  const platforms = [...new Set(data.map((item) => item.platform))]
  const timeBuckets = [...new Set(data.map((item) => item.time_bucket))]
  const heatmapData = data.map((item) => [
    timeBuckets.indexOf(item.time_bucket),
    platforms.indexOf(item.platform),
    item.intensity,
  ])
  const option = {
    tooltip: {
      position: 'top',
      formatter: (params) => `${platforms[params.value[1]]} ${timeBuckets[params.value[0]]}: ${params.value[2]}`,
    },
    grid: { left: 72, right: 24, top: 24, bottom: 32 },
    xAxis: {
      type: 'category',
      data: timeBuckets,
      axisLabel: { color: '#9aa6bf' },
      splitArea: { show: true },
    },
    yAxis: {
      type: 'category',
      data: platforms,
      axisLabel: { color: '#c9d4ea' },
      splitArea: { show: true },
    },
    visualMap: {
      min: 0,
      max: 100,
      calculable: false,
      orient: 'horizontal',
      left: 'center',
      bottom: 0,
      textStyle: { color: '#9aa6bf' },
      inRange: { color: ['#162033', '#42f5d7', '#f5c44b', '#ff5d8f'] },
    },
    series: [
      {
        type: 'heatmap',
        data: heatmapData,
        label: { show: false },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(66, 245, 215, 0.45)',
          },
        },
      },
    ],
  }

  return (
    <ChartFrame title="Platform Heatmap" description="Conversation intensity by hour" empty={!data.length}>
      <ReactECharts option={option} className="chart-surface" notMerge />
    </ChartFrame>
  )
}

