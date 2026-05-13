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
        if (params.dataType === 'edge') return `${params.data.source} → ${params.data.target}`
        return `${params.data.name}<br/>${params.data.platform}<br/>Influence ${params.data.influence}`
      },
    },
    series: [
      {
        type: 'graph',
        layout: 'force',
        roam: true,
        force: {
          repulsion: 180,
          edgeLength: 90,
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
        data: nodes.map((node) => ({
          name: node.node_id,
          value: node.influence_score,
          platform: node.platform,
          influence: node.influence_score,
          symbolSize: 38 + node.influence_score * 28,
          itemStyle: {
            color: platformColor[node.platform] || '#42f5d7',
            shadowBlur: 18,
            shadowColor: platformColor[node.platform] || '#42f5d7',
          },
        })),
        links: edges.map((edge) => ({
          source: edge.source,
          target: edge.target,
          value: edge.weight,
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

