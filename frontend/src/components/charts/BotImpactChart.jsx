import ReactECharts from 'echarts-for-react'

import { formatPercent } from '../../utils/formatters.js'
import { ChartFrame } from './ChartFrame.jsx'

export function BotImpactChart({ data }) {
  const suspected = Math.max(0, Math.min(1, data?.suspected_bot_comment_ratio ?? 0))
  const accountRatio = Math.max(0, Math.min(1, data?.suspected_bot_ratio ?? 0))
  const option = {
    color: ['#ff5d8f', '#42f5d7', '#283043'],
    tooltip: {
      formatter: '{b}: {d}%',
    },
    series: [
      {
        type: 'pie',
        radius: ['60%', '78%'],
        avoidLabelOverlap: true,
        label: {
          color: '#c9d4ea',
          formatter: '{b}\n{d}%',
        },
        data: [
          { value: suspected, name: 'Repeated comments' },
          { value: Math.max(0, 1 - suspected), name: 'Other' },
        ],
      },
    ],
    graphic: [
      {
        type: 'text',
        left: 'center',
        top: 'center',
        style: {
          text: `${formatPercent(suspected)}\ncomments\n${formatPercent(accountRatio)} accounts`,
          fill: '#f4f7fb',
          fontSize: 16,
          fontWeight: 700,
          align: 'center',
          lineHeight: 21,
        },
      },
    ],
  }

  return (
    <ChartFrame title="Bot Impact" description="Suspected automated comment share" empty={!data}>
      <ReactECharts option={option} className="chart-surface" notMerge />
    </ChartFrame>
  )
}
