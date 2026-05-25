import { Alert, Button, Card, Empty, Select, Space, Table, Tag, Typography, Upload } from 'antd'
import { CheckCircle2, Download, FileText, PlayCircle, RefreshCw, UploadCloud } from 'lucide-react'

import { riskTone } from '../utils/formatters.js'
import { getAnalysisSourceStatus } from '../utils/dataSourceStatus.js'
import {
  commitCaseEvidenceImport,
  getCase,
  getEvidenceImportTemplateCsvUrl,
  previewCaseEvidenceImport,
} from '../api/sentigraphApi.js'
import { useState } from 'react'

const { Text, Title } = Typography
const { Dragger } = Upload

const riskLevelLabels = {
  low: '低风险',
  medium: '中等风险',
  high: '高风险',
  critical: '严重风险',
}

const statusLabels = {
  draft: '待运行',
  running: '运行中',
  completed: '已完成',
  failed: '失败',
}

const statusColors = {
  draft: 'default',
  running: 'processing',
  completed: 'success',
  failed: 'error',
}

function formatScore(value) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? numericValue.toFixed(1) : '-'
}

function formatDate(value) {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString()
}

function buildEvidenceSummary(items = []) {
  const sourceDistribution = {}
  const typeCounts = {}
  const acquisitionModes = {}
  const titles = []
  const comments = []
  for (const item of Array.isArray(items) ? items : []) {
    const source = item.source_type || 'unknown'
    const type = item.evidence_type || 'unknown'
    const acquisitionMode = item.acquisition_mode || 'unknown'
    sourceDistribution[source] = (sourceDistribution[source] || 0) + 1
    typeCounts[type] = (typeCounts[type] || 0) + 1
    acquisitionModes[acquisitionMode] = (acquisitionModes[acquisitionMode] || 0) + 1
    if (item.title && !titles.includes(item.title)) titles.push(item.title)
    const comment = item.comment_text || item.body_text
    if (comment && !comments.includes(comment)) comments.push(comment)
  }
  return {
    acquisitionModes,
    comments: comments.slice(0, 3),
    sourceDistribution,
    titles: titles.slice(0, 3),
    typeCounts,
  }
}

function DistributionTags({ color = 'blue', values = {} }) {
  const entries = Object.entries(values)
  if (!entries.length) return <Text type="secondary">none</Text>
  return (
    <Space size={[4, 4]} wrap>
      {entries.map(([key, value]) => (
        <Tag color={color} key={key}>
          {key}: {value}
        </Tag>
      ))}
    </Space>
  )
}

const importMappingFields = [
  ['platform', 'platform'],
  ['source_type', 'source_type'],
  ['evidence_type', 'evidence_type'],
  ['title', 'title'],
  ['body_text', 'body_text'],
  ['comment_text', 'comment_text'],
  ['parent_id', 'parent_id'],
  ['root_id', 'root_id'],
  ['author_name', 'author_name'],
  ['url', 'url'],
  ['created_at', 'created_at'],
  ['like_count', 'like_count'],
  ['reply_count', 'reply_count'],
  ['share_count', 'share_count'],
  ['view_count', 'view_count'],
  ['language', 'language'],
]

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => {
      const result = String(reader.result || '')
      resolve(result.includes(',') ? result.split(',').pop() : result)
    }
    reader.onerror = () => reject(new Error('Unable to read selected file.'))
    reader.readAsDataURL(file)
  })
}

function evidenceImportPayload(filePayload, columnMapping) {
  return {
    filename: filePayload.filename,
    content_base64: filePayload.content_base64,
    column_mapping: Object.fromEntries(
      Object.entries(columnMapping || {}).filter(([, value]) => value),
    ),
  }
}

function EvidenceImportPanel({ currentCase, onCaseReady, onRunCase }) {
  const [filePayload, setFilePayload] = useState(null)
  const [columnMapping, setColumnMapping] = useState({})
  const [preview, setPreview] = useState(null)
  const [commitResult, setCommitResult] = useState(null)
  const [importLoading, setImportLoading] = useState(false)
  const [importError, setImportError] = useState('')

  if (!currentCase?.case_id) return null

  const templateCsvUrl = getEvidenceImportTemplateCsvUrl()
  const columnOptions = (preview?.detected_columns || []).map((column) => ({ label: column, value: column }))
  const previewColumns = [
    { title: 'row', dataIndex: 'row_number', key: 'row_number', width: 70 },
    {
      title: 'type',
      key: 'type',
      width: 170,
      render: (_, record) => (
        <Space direction="vertical" size={2}>
          <Tag color="purple">{record.evidence_type}</Tag>
          <Tag color="gold">{record.acquisition_mode}</Tag>
        </Space>
      ),
    },
    {
      title: 'preview',
      key: 'preview',
      render: (_, record) => (
        <Space direction="vertical" size={2}>
          {record.title ? <Text strong>{record.title}</Text> : null}
          <Text type="secondary">{record.comment_text || record.body_text || record.url || '-'}</Text>
        </Space>
      ),
    },
    { title: 'source', dataIndex: 'source_type', key: 'source_type', width: 140 },
    {
      title: 'warnings',
      key: 'warnings',
      width: 220,
      render: (_, record) => (
        <Space wrap size={[4, 4]}>
          {(record.warnings || []).length ? (
            record.warnings.map((warning) => (
              <Tag color={warning.severity === 'error' ? 'red' : 'orange'} key={`${record.row_number}-${warning.code}`}>
                {warning.code}
              </Tag>
            ))
          ) : (
            <Tag color="green">ok</Tag>
          )}
        </Space>
      ),
    },
  ]

  const handleFile = async (file) => {
    setImportError('')
    setPreview(null)
    setCommitResult(null)
    try {
      const contentBase64 = await fileToBase64(file)
      setFilePayload({
        filename: file.name,
        content_base64: contentBase64,
      })
      setColumnMapping({})
    } catch (error) {
      setImportError(error?.message || 'File read failed.')
    }
  }

  const handlePreview = async () => {
    if (!filePayload) return
    setImportLoading(true)
    setImportError('')
    try {
      const result = await previewCaseEvidenceImport(currentCase.case_id, evidenceImportPayload(filePayload, columnMapping))
      setPreview(result)
      setColumnMapping(result.column_mapping || {})
    } catch (error) {
      setImportError(error?.response?.data?.detail?.message || error?.message || 'Import preview failed.')
    } finally {
      setImportLoading(false)
    }
  }

  const handleCommit = async () => {
    if (!filePayload) return
    setImportLoading(true)
    setImportError('')
    try {
      const result = await commitCaseEvidenceImport(currentCase.case_id, evidenceImportPayload(filePayload, columnMapping))
      setCommitResult(result)
      const refreshedCase = await getCase(currentCase.case_id)
      onCaseReady?.(refreshedCase)
    } catch (error) {
      setImportError(error?.response?.data?.detail?.message || error?.message || 'Import commit failed.')
    } finally {
      setImportLoading(false)
    }
  }

  const handleMappingChange = (field, value) => {
    setColumnMapping((current) => ({ ...current, [field]: value }))
  }

  return (
    <Card className="panel-card">
      <Space direction="vertical" className="full-width" size={14}>
        <div className="panel-heading">
          <Space>
            <UploadCloud size={18} />
            <Title level={4}>导入证据数据</Title>
          </Space>
          <Space wrap>
            <Tag color="cyan">用户上传数据</Tag>
            <Tag color="green">CSV / Excel</Tag>
            <Tag color="purple">EvidenceItem</Tag>
          </Space>
        </div>
        <Space direction="vertical" size={6}>
          <Text type="secondary">按模板填写后上传，支持评论、文章、视频、回复和互动指标。用户需确保上传数据来源合法。</Text>
          <Text type="secondary">系统不会执行公式，不保存原始文件，不读取凭证。</Text>
          <Space wrap>
            <Button
              download="sentigraph_evidence_import_template.csv"
              href={templateCsvUrl}
              icon={<Download size={15} />}
            >
              下载 CSV 模板
            </Button>
          </Space>
        </Space>
        {importError ? <Alert message="证据导入失败" description={importError} type="error" showIcon /> : null}
        <Dragger
          accept=".csv,.txt,.xlsx"
          beforeUpload={(file) => {
            void handleFile(file)
            return false
          }}
          fileList={filePayload ? [{ uid: 'evidence-import-file', name: filePayload.filename, status: 'done' }] : []}
          maxCount={1}
          onRemove={() => {
            setFilePayload(null)
            setPreview(null)
            setCommitResult(null)
          }}
        >
          <p className="ant-upload-drag-icon">
            <UploadCloud size={26} />
          </p>
          <p className="ant-upload-text">上传 CSV / Excel</p>
          <p className="ant-upload-hint">支持 UTF-8 / UTF-8-BOM / GBK CSV 和宏禁用 XLSX。仅保存规范化后的证据项。</p>
        </Dragger>
        {preview?.detected_columns?.length ? (
          <Space direction="vertical" className="full-width" size={10}>
            <Text strong>字段映射</Text>
            <div className="evidence-import-mapping-grid">
              {importMappingFields.map(([field, label]) => (
                <Space direction="vertical" size={4} key={field}>
                  <Text type="secondary">{label}</Text>
                  <Select
                    allowClear
                    className="full-width"
                    options={columnOptions}
                    placeholder="未映射"
                    value={columnMapping[field] || undefined}
                    onChange={(value) => handleMappingChange(field, value)}
                  />
                </Space>
              ))}
            </div>
          </Space>
        ) : null}
        <Space wrap>
          <Button disabled={!filePayload} loading={importLoading} onClick={handlePreview}>
            预览导入结果
          </Button>
          <Button disabled={!preview?.valid_row_count} loading={importLoading} onClick={handleCommit} type="primary">
            确认导入
          </Button>
          <Button
            disabled={!commitResult?.imported_count}
            icon={<PlayCircle size={15} />}
            onClick={() => onRunCase?.(currentCase.case_id, 'analysis')}
          >
            导入后运行分析
          </Button>
        </Space>
        {preview ? (
          <Space direction="vertical" className="full-width" size={10}>
            <Space wrap>
              <Tag color="cyan">{preview.detected_format || 'unknown'}</Tag>
              <Tag color="geekblue">rows: {preview.total_rows}</Tag>
              <Tag color="green">valid: {preview.valid_row_count}</Tag>
              <Tag color={preview.duplicate_row_count ? 'orange' : 'default'}>duplicates: {preview.duplicate_row_count}</Tag>
              <Tag color={preview.skipped_row_count ? 'orange' : 'default'}>skipped: {preview.skipped_row_count}</Tag>
            </Space>
            {preview.warnings?.length ? (
              <Space wrap size={[4, 4]}>
                {preview.warnings.slice(0, 6).map((warning, index) => (
                  <Tag color="orange" key={`${warning.code}-${index}`}>
                    {warning.code}
                  </Tag>
                ))}
              </Space>
            ) : null}
            <Table
              columns={previewColumns}
              dataSource={preview.preview_rows}
              pagination={false}
              rowKey={(record) => `${record.row_number}-${record.evidence_id}`}
              size="small"
            />
          </Space>
        ) : null}
        {commitResult ? (
          <Alert
            message="导入完成"
            description={
              <Space direction="vertical" size={6}>
                <Space wrap>
                  <Tag color="green">imported: {commitResult.imported_count}</Tag>
                  <Tag color="cyan">total evidence: {commitResult.total_evidence_item_count}</Tag>
                  <DistributionTags color="geekblue" values={commitResult.source_distribution} />
                  <DistributionTags color="purple" values={commitResult.evidence_type_counts} />
                </Space>
                <Text type="secondary">导入数据会在没有 case_raw_data 时作为 case_evidence_items 进入离线确定性分析。</Text>
              </Space>
            }
            icon={<CheckCircle2 size={16} />}
            showIcon
            type="success"
          />
        ) : null}
      </Space>
    </Card>
  )
}

export function Cases({
  cases = [],
  currentCase,
  error,
  loading,
  onCaseReady,
  onNavigateToKeyword,
  onOpenCaseReport,
  onRefreshCases,
  onRunCase,
}) {
  const sourceStatus = getAnalysisSourceStatus({
    analysis: currentCase?.analysis_result,
    currentCase,
  })
  const evidenceSummary = buildEvidenceSummary(currentCase?.evidence_items || [])

  const columns = [
    {
      title: '案例',
      dataIndex: 'title',
      key: 'title',
      width: 230,
      render: (value, record) => (
        <Space direction="vertical" size={2}>
          <Text strong>{value || record.case_id}</Text>
          <Text type="secondary">{record.case_id}</Text>
        </Space>
      ),
    },
    {
      title: '关键词',
      dataIndex: 'keyword',
      key: 'keyword',
      width: 140,
      render: (value) => <Tag color="cyan">{value}</Tag>,
    },
    {
      title: '平台',
      dataIndex: 'platforms',
      key: 'platforms',
      render: (platforms = []) => (
        <Space wrap size={[4, 4]}>
          {platforms.length ? platforms.map((platform) => <Tag key={platform}>{platform}</Tag>) : <Text type="secondary">默认 mock 平台</Text>}
        </Space>
      ),
    },
    {
      title: '风险',
      key: 'risk',
      width: 150,
      render: (_, record) => (
        <Space direction="vertical" size={2}>
          <Text strong>{formatScore(record.risk_score)}/100</Text>
          {record.risk_level ? (
            <Tag color={riskTone(record.risk_level)}>{riskLevelLabels[record.risk_level] || record.risk_level}</Tag>
          ) : (
            <Tag>未生成</Tag>
          )}
        </Space>
      ),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 110,
      render: (value) => <Tag color={statusColors[value] || 'default'}>{statusLabels[value] || value}</Tag>,
    },
    {
      title: '更新时间',
      dataIndex: 'updated_at',
      key: 'updated_at',
      width: 190,
      render: formatDate,
    },
    {
      title: '操作',
      key: 'actions',
      width: 210,
      render: (_, record) => (
        <Space>
          <Button
            icon={<PlayCircle size={15} />}
            loading={loading && currentCase?.case_id === record.case_id}
            onClick={() => onRunCase(record.case_id)}
            size="small"
            type="primary"
          >
            运行
          </Button>
          <Button
            disabled={record.status !== 'completed'}
            icon={<FileText size={15} />}
            onClick={() => onOpenCaseReport(record.case_id)}
            size="small"
          >
            报告
          </Button>
        </Space>
      ),
    },
  ]

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>分析案例</Title>
          <Text>管理本地 mock 舆情分析案例，保存关键词、平台、V1.5 风险结果和中文报告上下文。</Text>
        </div>
        <Space>
          <Button icon={<RefreshCw size={16} />} onClick={onRefreshCases}>
            刷新
          </Button>
          <Button type="primary" onClick={onNavigateToKeyword}>
            新建案例
          </Button>
        </Space>
      </div>

      {error ? <Alert message="案例数据加载失败" description={error} type="error" showIcon /> : null}

      {currentCase ? (
        <Card className="panel-card">
          <div className="panel-heading">
            <div>
              <Title level={4}>Current Case Data Source</Title>
              <Text type="secondary">{sourceStatus.analysisDescription}</Text>
            </div>
          </div>
          <Space size={[8, 8]} wrap>
            <Tag color={sourceStatus.dataTagColor}>{sourceStatus.dataLabel}</Tag>
            <Tag color="green">{sourceStatus.analysisLabel}</Tag>
            <Tag color="purple">{sourceStatus.llmLabel}</Tag>
            <Tag color="geekblue">{sourceStatus.sourceDetail}</Tag>
            {sourceStatus.isYoutubeRealData ? (
              <Tag color="red">YouTube public video/comment data</Tag>
            ) : null}
          </Space>
          {currentCase.evidence_item_count ? (
            <Space direction="vertical" className="full-width" size={8} style={{ marginTop: 14 }}>
              <Text strong>Evidence summary</Text>
              <Space size={[8, 8]} wrap>
                <Tag color="cyan">evidence_items: {currentCase.evidence_item_count}</Tag>
                <DistributionTags color="geekblue" values={evidenceSummary.sourceDistribution} />
                <DistributionTags color="purple" values={evidenceSummary.typeCounts} />
                <DistributionTags color="gold" values={evidenceSummary.acquisitionModes} />
              </Space>
              <Text type="secondary">
                Evidence attachment normalizes already available public or user-provided material; it does not fetch external sources or expose credentials.
              </Text>
              {evidenceSummary.titles.length ? (
                <Text type="secondary">Top titles: {evidenceSummary.titles.join(' / ')}</Text>
              ) : null}
              {evidenceSummary.comments.length ? (
                <Text type="secondary">Representative evidence: {evidenceSummary.comments[0]}</Text>
              ) : null}
            </Space>
          ) : null}
        </Card>
      ) : null}

      {currentCase ? (
        <EvidenceImportPanel currentCase={currentCase} onCaseReady={onCaseReady} onRunCase={onRunCase} />
      ) : null}

      <Card className="panel-card cases-panel">
        {cases.length ? (
          <Table
            columns={columns}
            dataSource={cases}
            loading={loading && !cases.length}
            pagination={false}
            rowClassName={(record) => (record.case_id === currentCase?.case_id ? 'active-case-row' : '')}
            rowKey="case_id"
          />
        ) : (
          <Empty
            description="暂无分析案例。请先在 Keyword Search 创建并运行一个 mock 案例。"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          >
            <Button type="primary" onClick={onNavigateToKeyword}>
              创建第一个案例
            </Button>
          </Empty>
        )}
      </Card>
    </div>
  )
}
