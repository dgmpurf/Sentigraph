import ReactECharts from 'echarts-for-react'

import { ChartFrame } from './ChartFrame.jsx'

const platformColor = {
  reddit: '#ff8a4c',
  weibo: '#ff5d8f',
  youtube: '#f5c44b',
}

export function PropagationGraphChart({ graph }) {
  const nodes = graph?.nodes || []
  const edges = graph?.edges || []
  const option = {
    color: ['#42f5d7', '#ff5d8f', '#f5c44b'],
    tooltip: {
      formatter: (params) => {
        if (params.dataType === 'edge') return `${params.data.source} -> ${params.data.target}`
        return `${params.data.name}<br/>${params.data.platform}<br/>Influence ${params.data.influence}`
      },
    },
    series: [
      {
        type: 'graph',
        layout: 'force',
        roam: true,
        force: {
          repulsion: nodes.length <= 6 ? 260 : 180,
          edgeLength: nodes.length <= 6 ? 120 : 90,
        },
        label: {
          show: true,
          color: '#f4f7fb',
          formatter: '{b}',
        },
        lineStyle: {
          color: 'rgba(201, 212, 234, 0.42)',
          curveness: 0.18,
        },
        edgeSymbol: ['none', 'arrow'],
        edgeSymbolSize: [0, 8],
        data: nodes.map((node) => {
          const influence = node.influence_score ?? 0
          return {
            name: node.node_id,
            value: influence,
            platform: node.platform,
            influence,
            symbolSize: 38 + influence * 28,
            itemStyle: {
              color: platformColor[node.platform] || '#42f5d7',
              shadowBlur: 18,
              shadowColor: platformColor[node.platform] || '#42f5d7',
            },
          }
        }),
        links: edges.map((edge) => ({
          source: edge.source,
          target: edge.target,
          value: edge.weight ?? 0,
        })),
      },
    ],
  }

  return (
    <ChartFrame title="Propagation Graph" description="Cross-platform spread and reply paths" empty={!nodes.length}>
      <ReactECharts option={option} className="chart-surface graph-chart" notMerge />
    </ChartFrame>
  )
}
