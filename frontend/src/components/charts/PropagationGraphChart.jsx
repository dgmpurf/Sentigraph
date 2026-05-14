import ReactECharts from 'echarts-for-react'

import { ChartFrame } from './ChartFrame.jsx'

const platformColor = {
  bilibili: '#7dd3fc',
  douban: '#54f5a8',
  douyin: '#f472b6',
  kuaishou: '#f59e0b',
  reddit: '#ff8a4c',
  toutiao: '#f87171',
  weibo: '#ff5d8f',
  xiaohongshu: '#fb7185',
  youtube: '#f5c44b',
  zhihu: '#60a5fa',
}

export function PropagationGraphChart({ graph }) {
  const nodes = graph?.nodes || []
  const edges = graph?.edges || []
  const platforms = [...new Set(nodes.map((node) => node.platform || 'unknown'))]
  const categories = platforms.map((platform) => ({
    name: platform,
    itemStyle: {
      color: platformColor[platform] || '#42f5d7',
    },
  }))
  const option = {
    color: ['#42f5d7', '#ff5d8f', '#f5c44b'],
    legend: {
      top: 0,
      right: 0,
      data: platforms,
      textStyle: { color: '#9aa6bf' },
    },
    tooltip: {
      formatter: (params) => {
        if (params.dataType === 'edge') {
          return `${params.data.source} -> ${params.data.target}<br/>${params.data.relation}<br/>Weight ${params.data.value}`
        }
        return [
          params.data.name,
          `Platform: ${params.data.platform}`,
          `Type: ${params.data.nodeType}`,
          `Sentiment: ${params.data.sentiment}`,
          `Influence: ${params.data.influence}`,
        ].join('<br/>')
      },
    },
    series: [
      {
        type: 'graph',
        layout: 'force',
        roam: true,
        categories,
        force: {
          repulsion: nodes.length <= 8 ? 320 : 210,
          edgeLength: nodes.length <= 8 ? 140 : 96,
        },
        label: {
          show: true,
          color: '#f4f7fb',
          formatter: '{b}',
          fontSize: 11,
        },
        lineStyle: {
          color: 'rgba(201, 212, 234, 0.42)',
          curveness: 0.18,
        },
        edgeSymbol: ['none', 'arrow'],
        edgeSymbolSize: [0, 8],
        data: nodes.map((node) => {
          const influence = Number(node.influence_score ?? 0)
          const sentiment = Number(node.sentiment_score ?? 0)
          const platform = node.platform || 'unknown'
          return {
            name: node.node_id,
            value: influence,
            category: platform,
            content: node.content || '',
            nodeType: node.type || 'node',
            platform,
            sentiment: sentiment.toFixed(2),
            influence: influence.toFixed(2),
            symbol: node.type === 'post' ? 'roundRect' : 'circle',
            symbolSize: 38 + influence * 28,
            itemStyle: {
              color: platformColor[platform] || '#42f5d7',
              shadowBlur: 18,
              shadowColor: platformColor[platform] || '#42f5d7',
              borderColor: sentiment < -0.2 ? '#ff5d8f' : '#42f5d7',
              borderWidth: 2,
            },
          }
        }),
        links: edges.map((edge) => ({
          source: edge.source,
          target: edge.target,
          value: edge.weight ?? 0,
          relation: edge.relation || 'relation',
          lineStyle: {
            width: 1 + Number(edge.weight || 0) * 3,
            opacity: 0.62,
          },
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
