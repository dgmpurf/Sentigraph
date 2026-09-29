import React from 'react'
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react'
import { afterEach, beforeEach, expect, it, vi } from 'vitest'

vi.mock('../components/charts/PlatformHeatmapChart.jsx', () => ({ PlatformHeatmapChart: () => null }))
vi.mock('../components/charts/RiskRadarChart.jsx', () => ({ RiskRadarChart: () => null }))
vi.mock('../components/charts/SentimentTrendChart.jsx', () => ({ SentimentTrendChart: () => null }))

import { RiskMonitor } from './RiskMonitor.jsx'

const selectedCase = {
  case_id: 'case_synthetic', title: 'Synthetic case', status: 'completed',
  analysis_revision: 2, analysis_run_id: 'run_b',
}

const currentSnapshot = {
  snapshot_id: 'current', lineage_status: 'CURRENT', risk_score: 12,
  risk_level: 'low', created_at: '2026-09-29T00:00:00Z', top_risk_topics: [],
}

const historicalSnapshot = {
  snapshot_id: 'historical', lineage_status: 'HISTORICAL', risk_score: 99,
  risk_level: 'critical', created_at: '2026-09-29T01:00:00Z', top_risk_topics: [],
}

const currentAlert = {
  alert_id: 'current_alert', lineage_status: 'CURRENT', level: 'info',
  message: 'Current signal', reason: 'Current reason',
}

const historicalAlert = {
  alert_id: 'historical_alert', lineage_status: 'HISTORICAL', level: 'critical',
  message: 'Historical signal', reason: 'Historical reason',
}

const currentNotification = {
  notification_id: 'current_notice', case_id: 'case_synthetic', lineage_status: 'CURRENT',
  level: 'info', title: 'Current notice', message: 'Current notification message',
  status: 'pending', channel_type: 'in_app', read_at: null,
}

const historicalNotification = {
  notification_id: 'historical_notice', case_id: 'case_synthetic', lineage_status: 'HISTORICAL',
  level: 'critical', title: 'Historical notice', message: 'Historical notification message',
  status: 'pending', channel_type: 'in_app', read_at: null,
}

function renderMonitor(overrides = {}) {
  const actions = {
    onMarkNotificationRead: vi.fn(), onSimulateSendNotification: vi.fn(),
    onSimulateSendPendingNotifications: vi.fn(), onRunForecast: vi.fn(),
    onRunMonitoringCheck: vi.fn(), onEnableMonitoring: vi.fn(),
    onDisableMonitoring: vi.fn(), onRunDueMonitoringJobs: vi.fn(),
  }
  render(<RiskMonitor
    currentCase={selectedCase}
    analysis={{ summary: 'Selected analysis' }}
    visualization={{ risk_score: 12, risk_level: 'low' }}
    caseSnapshots={[historicalSnapshot, currentSnapshot]}
    alerts={[historicalAlert, currentAlert]}
    notifications={[historicalNotification, currentNotification]}
    notificationOutboxStatus={{ current_pending: 0, current_unread: 0, pending: 5, unread: 4, mock_only: true }}
    {...actions}
    {...overrides}
  />)
  return actions
}

beforeEach(() => {
  vi.stubGlobal('ResizeObserver', class { observe() {} unobserve() {} disconnect() {} })
  vi.stubGlobal('matchMedia', (query) => ({
    matches: false, media: query, onchange: null,
    addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {}, dispatchEvent() { return false },
  }))
})

afterEach(() => { cleanup(); vi.unstubAllGlobals() })

it('uses only CURRENT artifacts for risk, alerts and operational notification actions', () => {
  const actions = renderMonitor()
  const hero = screen.getByText('当前监控风险 / Monitor current risk').closest('.risk-monitor-hero')
  expect(hero.querySelector('.ant-statistic-content-value').textContent).toBe('12.0')
  expect(hero.querySelector('.ant-statistic-content-value').textContent).not.toBe('99.0')
  expect(screen.getAllByText('Current reason').length).toBeGreaterThan(0)
  expect(screen.getByText('0 未读通知')).toBeTruthy()
  expect(screen.getByText('0 待模拟发送')).toBeTruthy()
  expect(screen.getByTestId('notification-send-pending-button').disabled).toBe(true)
  expect(screen.getByTestId('notification-mark-read-button').disabled).toBe(false)
  expect(screen.getByTestId('notification-simulate-send-button').disabled).toBe(false)
  fireEvent.click(screen.getByTestId('notification-mark-read-button'))
  expect(actions.onMarkNotificationRead).toHaveBeenCalledWith('current_notice')
  expect(actions.onMarkNotificationRead).toHaveBeenCalledTimes(1)

  const history = screen.getByText('历史与未绑定旧记录').closest('.ant-card')
  expect(within(history).getByTestId('historical-snapshot-list').textContent).toContain('99.0/100')
  expect(within(history).getByText('Historical reason')).toBeTruthy()
  expect(within(history).getByText('Historical notice')).toBeTruthy()
  expect(within(history).getByTestId('historical-notification-mark-read-button').disabled).toBe(true)
  expect(within(history).getByTestId('historical-notification-simulate-send-button').disabled).toBe(true)
})

it('keeps history visible but does not promote it when the selected case has no current baseline', () => {
  renderMonitor({ analysis: null, visualization: null, caseSnapshots: [historicalSnapshot],
    alerts: [historicalAlert], notifications: [historicalNotification] })
  expect(screen.getByText(/当前分析没有可用的 current 监控产物/)).toBeTruthy()
  expect(screen.getByText('Historical reason')).toBeTruthy()
  expect(screen.queryByText('当前监控风险 / Monitor current risk')).toBeNull()
  expect(screen.getByTestId('historical-notification-mark-read-button').disabled).toBe(true)
})

it('rejects stale forecast and monitoring status for the selected analysis pair', () => {
  const stale = {
    case_id: 'case_synthetic', source_analysis_revision: 1, source_analysis_run_id: 'run_a',
    forecast_status: 'ready', predicted_risk_score: 88, message: 'Stale pair status',
  }
  renderMonitor({ caseForecast: stale, monitoringStatus: stale })
  expect(screen.queryByText('Stale pair status')).toBeNull()
  expect(screen.getByText('尚未运行本轮监控检查。')).toBeTruthy()
})
