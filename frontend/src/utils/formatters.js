export function formatPercent(value) {
  if (typeof value !== 'number') return '0%'
  return `${Math.round(value * 100)}%`
}

export function formatHour(value) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

export function riskTone(level) {
  const toneMap = {
    low: 'success',
    medium: 'warning',
    high: 'error',
    critical: 'error',
  }
  return toneMap[level] || 'default'
}

