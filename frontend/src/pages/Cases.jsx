import { Alert, Button, Card, Checkbox, Empty, Form, Input, InputNumber, Select, Space, Table, Tag, Typography, Upload } from 'antd'
import { CheckCircle2, Download, FileText, Link2, PlayCircle, PlusCircle, RefreshCw, UploadCloud } from 'lucide-react'

import { riskTone } from '../utils/formatters.js'
import { getAnalysisSourceStatus } from '../utils/dataSourceStatus.js'
import {
  attachCaseEvidence,
  commitCaseEvidenceImport,
  getCase,
  getCaseEvidenceReviewAuditSummary,
  getCaseEvidenceReviewQueue,
  getCaseEvidenceReviewTimeline,
  getEvidenceImportTemplateCsvUrl,
  previewCaseEvidenceImport,
  reviewCaseEvidence,
} from '../api/sentigraphApi.js'
import { useEffect, useState } from 'react'

const { Text, Title } = Typography
const { Dragger } = Upload
const { TextArea } = Input

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
  const provenanceTypes = {}
  const trustLabels = {}
  const verificationStatuses = {}
  const reviewStatuses = {}
  const riskFlags = {}
  let sourceUrlPresent = 0
  let sourceUrlMissing = 0
  let reviewNeeded = 0
  let duplicateItems = 0
  const titles = []
  const comments = []
  for (const item of Array.isArray(items) ? items : []) {
    const source = item.source_type || 'unknown'
    const type = item.evidence_type || 'unknown'
    const acquisitionMode = item.acquisition_mode || 'unknown'
    sourceDistribution[source] = (sourceDistribution[source] || 0) + 1
    typeCounts[type] = (typeCounts[type] || 0) + 1
    acquisitionModes[acquisitionMode] = (acquisitionModes[acquisitionMode] || 0) + 1
    const provenanceType = item.provenance_type || 'unknown'
    const trustLabel = item.trust_label || 'unknown'
    const verificationStatus = item.verification_status || 'unknown'
    const reviewStatus = item.review_status || 'not_reviewed'
    provenanceTypes[provenanceType] = (provenanceTypes[provenanceType] || 0) + 1
    trustLabels[trustLabel] = (trustLabels[trustLabel] || 0) + 1
    verificationStatuses[verificationStatus] = (verificationStatuses[verificationStatus] || 0) + 1
    reviewStatuses[reviewStatus] = (reviewStatuses[reviewStatus] || 0) + 1
    if (item.source_url_present || item.source_url || item.url) sourceUrlPresent += 1
    else sourceUrlMissing += 1
    if (['low', 'unverified', 'rejected'].includes(trustLabel) || verificationStatus === 'needs_review') reviewNeeded += 1
    const duplicateCount = Number(item.duplicate_count || 1)
    if (duplicateCount > 1) duplicateItems += duplicateCount - 1
    for (const flag of Array.isArray(item.risk_flags) ? item.risk_flags : []) {
      riskFlags[flag] = (riskFlags[flag] || 0) + 1
    }
    if (item.title && !titles.includes(item.title)) titles.push(item.title)
    const comment = item.comment_text || item.body_text
    if (comment && !comments.includes(comment)) comments.push(comment)
  }
  return {
    acquisitionModes,
    comments: comments.slice(0, 3),
    duplicateItems,
    provenanceTypes,
    reviewNeeded,
    reviewStatuses,
    riskFlags,
    sourceDistribution,
    sourceUrlMissing,
    sourceUrlPresent,
    titles: titles.slice(0, 3),
    trustLabels,
    typeCounts,
    verificationStatuses,
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
  ['provenance_type', 'provenance_type'],
  ['verification_status', 'verification_status'],
  ['source_capture_method', 'source_capture_method'],
  ['user_attestation', 'user_attestation'],
]

const manualEvidenceTypes = [
  { label: '文章 article', value: 'article' },
  { label: '视频 video', value: 'video' },
  { label: '帖子 post', value: 'post' },
  { label: '评论 comment', value: 'comment' },
  { label: '回复 reply', value: 'reply' },
  { label: '互动指标 interaction_metric', value: 'interaction_metric' },
]

const manualSourceTypes = [
  { label: 'public_web', value: 'public_web' },
  { label: 'news_site', value: 'news_site' },
  { label: 'forum', value: 'forum' },
  { label: 'youtube', value: 'youtube' },
  { label: 'uploaded_dataset', value: 'uploaded_dataset' },
]

function trimValue(value) {
  return typeof value === 'string' ? value.trim() : ''
}

function evidenceTextPreview(item = {}) {
  return item.comment_text || item.body_text || item.title || item.url || ''
}

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

function ManualEvidencePanel({ currentCase, onCaseReady, onRunCase }) {
  const [form] = Form.useForm()
  const [manualLoading, setManualLoading] = useState(false)
  const [manualError, setManualError] = useState('')
  const [manualResult, setManualResult] = useState(null)

  if (!currentCase?.case_id) return null

  const latestEvidence = manualResult?.evidence_items?.[manualResult.evidence_items.length - 1]
  const manualSummary = buildEvidenceSummary(manualResult?.evidence_items || [])

  const handleAttach = async (values) => {
    setManualError('')
    setManualResult(null)
    const title = trimValue(values.title)
    const bodyText = trimValue(values.body_text)
    const commentText = trimValue(values.comment_text)
    if (!title && !bodyText && !commentText) {
      setManualError('请至少填写标题、正文/摘要或评论内容之一。')
      return
    }

    const platform = trimValue(values.platform) || 'manual_url'
    const sourceType = values.source_type || 'public_web'
    const userAttested = Boolean(values.user_attestation)
    const sourceCaptureMethod = trimValue(values.source_capture_method) || 'manual_entry'
    const evidenceItem = {
      platform,
      source_type: sourceType,
      acquisition_mode: 'manual_url',
      evidence_type: values.evidence_type || 'comment',
      title: title || null,
      body_text: bodyText || null,
      comment_text: commentText || null,
      parent_id: trimValue(values.parent_id) || null,
      root_id: trimValue(values.root_id) || null,
      author_id: trimValue(values.author_id) || null,
      author_name: trimValue(values.author_name) || null,
      url: trimValue(values.url) || null,
      created_at: trimValue(values.created_at) || null,
      like_count: Number(values.like_count || 0),
      reply_count: Number(values.reply_count || 0),
      share_count: Number(values.share_count || 0),
      view_count: Number(values.view_count || 0),
      language: trimValue(values.language) || 'unknown',
      content_visibility: 'public_or_user_provided',
      access_scope: 'manual_url_user_provided',
      provenance_type: sourceCaptureMethod === 'screenshot_transcription' ? 'screenshot_transcription' : 'manual_url',
      verification_status: 'needs_review',
      source_url: trimValue(values.url) || null,
      source_url_present: Boolean(trimValue(values.url)),
      source_platform_claim: platform,
      source_capture_method: sourceCaptureMethod,
      user_attestation_required: true,
      user_attestation_text: userAttested
        ? 'User confirmed lawful source/right to submit this public-opinion evidence.'
        : null,
      raw_data_safe: {
        manual_entry: true,
        no_url_fetch: true,
        no_scraping: true,
        user_attested_public_or_lawful_source: userAttested,
      },
    }

    setManualLoading(true)
    try {
      const result = await attachCaseEvidence(currentCase.case_id, {
        source: {
          platform,
          source_type: sourceType,
          acquisition_mode: 'manual_url',
          source_name: 'Manual URL evidence',
          source_url: trimValue(values.url) || null,
          access_scope: 'manual_url_user_provided',
          credential_present: false,
          notes: 'User-entered public evidence text only; Sentigraph does not fetch this URL.',
        },
        evidence_items: [evidenceItem],
      })
      setManualResult(result)
      const refreshedCase = await getCase(currentCase.case_id)
      onCaseReady?.(refreshedCase)
      form.resetFields()
    } catch (error) {
      setManualError(error?.response?.data?.detail?.message || error?.message || 'Manual evidence attach failed.')
    } finally {
      setManualLoading(false)
    }
  }

  return (
    <Card className="panel-card">
      <Space direction="vertical" className="full-width" size={14}>
        <div className="panel-heading">
          <Space>
            <Link2 size={18} />
            <Title level={4}>手动添加证据</Title>
          </Space>
          <Space wrap>
            <Tag color="cyan">manual_url</Tag>
            <Tag color="green">normalized EvidenceItem</Tag>
            <Tag color="purple">no fetch</Tag>
          </Space>
        </div>
        <Alert
          message="手动 URL / 单条证据录入"
          description={
            <Space direction="vertical" size={2}>
              <Text>本功能不会自动抓取网页内容，请手动粘贴你有权使用的公开证据文本。</Text>
              <Text>系统只保存规范化 EvidenceItem，不保存凭证、Cookie 或密钥。</Text>
              <Text>用户需确保数据来源合法合规。</Text>
            </Space>
          }
          showIcon
          type="info"
        />
        {manualError ? <Alert message="手动证据添加失败" description={manualError} type="error" showIcon /> : null}
        <Form
          form={form}
          initialValues={{
            acquisition_mode: 'manual_url',
          evidence_type: 'comment',
          platform: 'manual_url',
          source_type: 'public_web',
          source_capture_method: 'manual_entry',
          user_attestation: false,
        }}
          layout="vertical"
          onFinish={handleAttach}
        >
          <div className="evidence-manual-grid">
            <Form.Item label="URL" name="url">
              <Input placeholder="https://example.com/public-post" />
            </Form.Item>
            <Form.Item label="平台" name="platform">
              <Input placeholder="manual_url / youtube / news_site" />
            </Form.Item>
            <Form.Item label="来源类型" name="source_type">
              <Select options={manualSourceTypes} />
            </Form.Item>
            <Form.Item label="证据类型" name="evidence_type">
              <Select options={manualEvidenceTypes} />
            </Form.Item>
            <Form.Item label="来源捕获方式" name="source_capture_method">
              <Select
                options={[
                  { label: 'manual_entry', value: 'manual_entry' },
                  { label: 'screenshot_transcription', value: 'screenshot_transcription' },
                  { label: 'manual_copy_from_public_page', value: 'manual_copy_from_public_page' },
                ]}
              />
            </Form.Item>
            <Form.Item label="标题" name="title">
              <Input placeholder="公开文章、视频或帖子标题" />
            </Form.Item>
            <Form.Item label="作者" name="author_name">
              <Input placeholder="公开作者名或来源名，可留空" />
            </Form.Item>
            <Form.Item className="evidence-manual-wide" label="正文 / 摘要" name="body_text">
              <TextArea autoSize={{ minRows: 3, maxRows: 6 }} placeholder="手动粘贴公开正文、摘要或视频描述" />
            </Form.Item>
            <Form.Item className="evidence-manual-wide" label="评论内容" name="comment_text">
              <TextArea autoSize={{ minRows: 3, maxRows: 6 }} placeholder="手动粘贴公开评论或回复内容" />
            </Form.Item>
            <Form.Item label="父级ID" name="parent_id">
              <Input placeholder="回复所属评论 ID，可留空" />
            </Form.Item>
            <Form.Item label="根证据ID" name="root_id">
              <Input placeholder="文章/视频/帖子 ID，可留空" />
            </Form.Item>
            <Form.Item label="作者ID" name="author_id">
              <Input placeholder="公开作者 ID，可留空" />
            </Form.Item>
            <Form.Item label="发布时间" name="created_at">
              <Input placeholder="2026-05-25T09:00:00Z" />
            </Form.Item>
            <Form.Item label="点赞数" name="like_count">
              <InputNumber className="full-width" min={0} precision={0} />
            </Form.Item>
            <Form.Item label="回复数" name="reply_count">
              <InputNumber className="full-width" min={0} precision={0} />
            </Form.Item>
            <Form.Item label="分享数" name="share_count">
              <InputNumber className="full-width" min={0} precision={0} />
            </Form.Item>
            <Form.Item label="浏览数" name="view_count">
              <InputNumber className="full-width" min={0} precision={0} />
            </Form.Item>
            <Form.Item label="语言" name="language">
              <Input placeholder="zh-CN / en-US，可留空自动推断" />
            </Form.Item>
          </div>
          <Form.Item name="user_attestation" valuePropName="checked">
            <Checkbox>我确认该证据来源合法，且有权提交用于分析</Checkbox>
          </Form.Item>
          <Text type="secondary">
            未勾选时仍可保存，但会标记为 needs_review / user_attestation_missing；截图转录不会被自动视为已验证。
          </Text>
          <Text type="secondary">
            Screenshot/transcribed evidence is not automatically verified by Sentigraph.
          </Text>
          <Space wrap>
            <Button htmlType="submit" icon={<PlusCircle size={15} />} loading={manualLoading} type="primary">
              添加到案例
            </Button>
            <Button
              disabled={!manualResult?.evidence_item_count && !currentCase.evidence_item_count}
              icon={<PlayCircle size={15} />}
              onClick={() => onRunCase?.(currentCase.case_id, 'analysis')}
            >
              添加后运行分析
            </Button>
          </Space>
        </Form>
        {manualResult ? (
          <Alert
            message="手动证据已添加"
            description={
              <Space direction="vertical" size={6}>
                <Space wrap>
                  <Tag color="green">evidence_count: {manualResult.evidence_item_count}</Tag>
                  <DistributionTags color="purple" values={manualResult.evidence_type_counts} />
                  <DistributionTags color="geekblue" values={manualResult.source_distribution} />
                  <DistributionTags color="magenta" values={manualSummary.provenanceTypes} />
                  <DistributionTags color="magenta" values={manualResult.trust_summary?.trust_label_distribution} />
                  <DistributionTags color="blue" values={manualResult.trust_summary?.verification_status_distribution} />
                  <Tag color={manualSummary.sourceUrlMissing ? 'orange' : 'green'}>
                    source_url_present: {manualSummary.sourceUrlPresent}/{manualResult.evidence_item_count || 0}
                  </Tag>
                  <Tag color={manualResult.trust_summary?.review_needed_count ? 'orange' : 'green'}>
                    review_needed: {manualResult.trust_summary?.review_needed_count || 0}
                  </Tag>
                  <Tag color={manualSummary.riskFlags?.user_attestation_missing ? 'orange' : 'green'}>
                    attestation_missing: {manualSummary.riskFlags?.user_attestation_missing || 0}
                  </Tag>
                  <Tag color={manualResult.deduplication_summary?.duplicate_items ? 'orange' : 'default'}>
                    duplicates: {manualResult.deduplication_summary?.duplicate_items || 0}
                  </Tag>
                  <Tag color="gold">acquisition_mode=manual_url</Tag>
                </Space>
                {latestEvidence ? (
                  <Text type="secondary">Latest evidence: {evidenceTextPreview(latestEvidence)}</Text>
                ) : null}
                {manualResult.warnings?.length ? (
                  <Space wrap size={[4, 4]}>
                    {manualResult.warnings.map((warning) => (
                      <Tag color="orange" key={warning}>{warning}</Tag>
                    ))}
                  </Space>
                ) : null}
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
          {record.trust_label ? <Tag color={record.trust_label === 'high' ? 'green' : record.trust_label === 'medium' ? 'blue' : 'orange'}>{record.trust_label}</Tag> : null}
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
                  <DistributionTags color="magenta" values={buildEvidenceSummary(commitResult.evidence_items).trustLabels} />
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

const reviewFilterOptions = [
  { label: 'all', value: 'all' },
  { label: 'needs_review', value: 'needs_review' },
  { label: 'low_trust', value: 'low_trust' },
  { label: 'screenshot', value: 'screenshot' },
  { label: 'missing_source', value: 'missing_source' },
  { label: 'duplicates', value: 'duplicates' },
  { label: 'rejected', value: 'rejected' },
  { label: 'approved', value: 'approved' },
]

const reviewActionOptions = [
  { label: '通过', value: 'approve' },
  { label: '驳回', value: 'reject' },
  { label: '标记为弱证据', value: 'mark_weak' },
  { label: '要求补充来源', value: 'request_more_source' },
  { label: '合并重复', value: 'merge_duplicate' },
  { label: '重置', value: 'reset_review' },
]

function trustColor(value) {
  if (value === 'high') return 'green'
  if (value === 'medium') return 'blue'
  if (value === 'low') return 'orange'
  if (value === 'rejected') return 'red'
  return 'default'
}

function reviewStatusColor(value) {
  if (value === 'approved') return 'green'
  if (value === 'rejected') return 'red'
  if (value === 'marked_weak') return 'orange'
  if (value === 'needs_more_source') return 'gold'
  if (value === 'duplicate_merged') return 'purple'
  if (value === 'review_needed') return 'volcano'
  return 'default'
}

function matchesReviewFilter(item, filter) {
  if (filter === 'all') return true
  if (filter === 'needs_review') return item.review_status === 'review_needed' || item.review_reason_codes.length > 0
  if (filter === 'low_trust') return ['low', 'unverified', 'rejected'].includes(item.trust_label)
  if (filter === 'screenshot') return item.provenance_type === 'screenshot_transcription'
  if (filter === 'missing_source') return !item.source_url_present
  if (filter === 'duplicates') return Number(item.duplicate_count || 1) > 1
  if (filter === 'rejected') return item.review_status === 'rejected'
  if (filter === 'approved') return item.review_status === 'approved'
  return true
}

function EvidenceReviewQueuePanel({ currentCase, onCaseReady }) {
  const [filter, setFilter] = useState('all')
  const [queueSummary, setQueueSummary] = useState(null)
  const [reviewTimeline, setReviewTimeline] = useState(null)
  const [auditSummary, setAuditSummary] = useState(null)
  const [reviewNote, setReviewNote] = useState('')
  const [queueLoading, setQueueLoading] = useState(false)
  const [decisionLoadingId, setDecisionLoadingId] = useState('')
  const [queueError, setQueueError] = useState('')
  const [queueSuccess, setQueueSuccess] = useState('')

  const caseId = currentCase?.case_id

  useEffect(() => {
    if (!caseId) {
      setQueueSummary(null)
      setReviewTimeline(null)
      setAuditSummary(null)
      return
    }
    let cancelled = false
    const loadReviewState = async () => {
      setQueueLoading(true)
      setQueueError('')
      try {
        const [queueResult, timelineResult, auditResult] = await Promise.all([
          getCaseEvidenceReviewQueue(caseId),
          getCaseEvidenceReviewTimeline(caseId),
          getCaseEvidenceReviewAuditSummary(caseId),
        ])
        if (!cancelled) {
          setQueueSummary(queueResult)
          setReviewTimeline(timelineResult)
          setAuditSummary(auditResult)
        }
      } catch (error) {
        if (!cancelled) setQueueError(error?.message || 'Evidence review queue load failed.')
      } finally {
        if (!cancelled) setQueueLoading(false)
      }
    }
    void loadReviewState()
    return () => {
      cancelled = true
    }
  }, [caseId, currentCase?.evidence_item_count, currentCase?.updated_at])

  if (!caseId) return null

  const filteredItems = (queueSummary?.queue_items || []).filter((item) => matchesReviewFilter(item, filter))

  const refreshQueue = async () => {
    const [queueResult, timelineResult, auditResult] = await Promise.all([
      getCaseEvidenceReviewQueue(caseId),
      getCaseEvidenceReviewTimeline(caseId),
      getCaseEvidenceReviewAuditSummary(caseId),
    ])
    setQueueSummary(queueResult)
    setReviewTimeline(timelineResult)
    setAuditSummary(auditResult)
  }

  const handleDecision = async (item, decision) => {
    setQueueError('')
    setQueueSuccess('')
    setDecisionLoadingId(`${item.evidence_id}:${decision}`)
    try {
      const result = await reviewCaseEvidence(caseId, item.evidence_id, {
        decision,
        reviewer_label: 'local_human_reviewer',
        notes: reviewNote.trim() || undefined,
      })
      setQueueSummary(result.summary)
      setQueueSuccess(`${item.evidence_id} -> ${result.review_status}`)
      setReviewNote('')
      const refreshedCase = await getCase(caseId)
      onCaseReady?.(refreshedCase)
      await refreshQueue()
    } catch (error) {
      setQueueError(error?.response?.data?.detail || error?.message || 'Review decision failed.')
    } finally {
      setDecisionLoadingId('')
    }
  }

  const columns = [
    {
      title: 'Evidence',
      key: 'evidence',
      render: (_, record) => (
        <Space direction="vertical" size={3}>
          <Space wrap>
            <Tag color="purple">{record.evidence_type}</Tag>
            <Tag>{record.platform}</Tag>
          </Space>
          {record.title ? <Text strong>{record.title}</Text> : null}
          <Text type="secondary">{record.comment_text_preview || record.body_text_preview || record.url || '-'}</Text>
        </Space>
      ),
    },
    {
      title: 'Trust',
      key: 'trust',
      width: 220,
      render: (_, record) => (
        <Space direction="vertical" size={4}>
          <Tag color={trustColor(record.trust_label)}>{record.trust_label}</Tag>
          <Tag color="blue">{record.verification_status}</Tag>
          <Tag color="magenta">{record.provenance_type}</Tag>
          <Tag color={record.source_url_present ? 'green' : 'orange'}>
            {record.source_url_present ? 'source URL present' : 'source URL missing'}
          </Tag>
        </Space>
      ),
    },
    {
      title: 'Review',
      key: 'review',
      width: 260,
      render: (_, record) => (
        <Space direction="vertical" size={4}>
          <Tag color={reviewStatusColor(record.review_status)}>{record.review_status}</Tag>
          {record.duplicate_count > 1 ? <Tag color="orange">duplicate x{record.duplicate_count}</Tag> : null}
          <Space wrap size={[4, 4]}>
            {record.review_reason_codes.slice(0, 4).map((code) => (
              <Tag color="orange" key={`${record.evidence_id}-${code}`}>{code}</Tag>
            ))}
          </Space>
          {record.user_attestation_required ? (
            <Tag color={record.user_attestation_text ? 'green' : 'orange'}>
              {record.user_attestation_text ? 'attested' : 'attestation missing'}
            </Tag>
          ) : null}
        </Space>
      ),
    },
    {
      title: 'Actions',
      key: 'actions',
      width: 300,
      render: (_, record) => (
        <Space wrap size={[4, 4]}>
          {reviewActionOptions.map((action) => (
            <Button
              danger={action.value === 'reject'}
              key={action.value}
              loading={decisionLoadingId === `${record.evidence_id}:${action.value}`}
              onClick={() => handleDecision(record, action.value)}
              size="small"
              type={action.value === 'approve' ? 'primary' : 'default'}
            >
              {action.label}
            </Button>
          ))}
        </Space>
      ),
    },
  ]

  const historyColumns = [
    {
      title: 'Decision',
      key: 'decision',
      width: 180,
      render: (_, record) => (
        <Space direction="vertical" size={3}>
          <Tag color={reviewStatusColor(record.new_review_status)}>{record.decision}</Tag>
          <Text type="secondary">{record.reason_code || '-'}</Text>
        </Space>
      ),
    },
    {
      title: 'Status',
      key: 'status',
      width: 210,
      render: (_, record) => (
        <Space direction="vertical" size={3}>
          <Text>{record.previous_review_status || 'not_reviewed'} -&gt; {record.new_review_status || 'not_reviewed'}</Text>
          <Tag color="blue">{record.analysis_effect || 'included_in_analysis'}</Tag>
        </Space>
      ),
    },
    {
      title: 'Evidence',
      key: 'evidence',
      render: (_, record) => (
        <Space direction="vertical" size={3}>
          <Text code>{record.evidence_id}</Text>
          <Text type="secondary">{record.note || 'No reviewer note.'}</Text>
        </Space>
      ),
    },
    {
      title: 'Reviewer',
      key: 'reviewer',
      width: 190,
      render: (_, record) => (
        <Space direction="vertical" size={3}>
          <Text>{record.reviewer_label || 'local_human_reviewer'}</Text>
          <Text type="secondary">{formatDate(record.reviewed_at)}</Text>
        </Space>
      ),
    },
  ]

  return (
    <Card className="panel-card">
      <Space direction="vertical" className="full-width" size={14}>
        <div className="panel-heading">
          <Space>
            <CheckCircle2 size={18} />
            <Title level={4}>Evidence Review / 证据复核</Title>
          </Space>
          <Space wrap>
            <Tag color="cyan">human review only</Tag>
            <Tag color="purple">AI not used for authenticity</Tag>
            <Tag color="orange">rejected excluded from analysis</Tag>
          </Space>
        </div>
        <Alert
          message="Human review queue"
          description={
            <Space direction="vertical" size={2}>
              <Text>截图或转录内容不能自动视为真实，需要人工核验。AI 未参与真实性验证。</Text>
              <Text>被驳回证据默认不进入分析；重复证据会折叠，不会重复放大情绪或风险。</Text>
            </Space>
          }
          showIcon
          type="warning"
        />
        {queueError ? <Alert message="Evidence review queue error" description={String(queueError)} type="error" showIcon /> : null}
        {queueSuccess ? <Alert message="Review decision saved" description={queueSuccess} type="success" showIcon /> : null}
        <Space size={[8, 8]} wrap>
          <Tag color="cyan">queue: {queueSummary?.queue_count || 0}</Tag>
          <Tag color="orange">needs_review: {queueSummary?.review_needed_count || 0}</Tag>
          <Tag color="gold">low_trust: {queueSummary?.low_trust_count || 0}</Tag>
          <Tag color="purple">duplicate_groups: {queueSummary?.duplicate_group_count || 0}</Tag>
          <Tag color="green">approved: {queueSummary?.approved_count || 0}</Tag>
          <Tag color="red">rejected: {queueSummary?.rejected_count || 0}</Tag>
          <Tag color="orange">marked_weak: {queueSummary?.marked_weak_count || 0}</Tag>
          <Tag color="geekblue">needs_more_source: {queueSummary?.needs_more_source_count || 0}</Tag>
        </Space>
        <Space size={[8, 8]} wrap>
          <Tag color="cyan">review events: {auditSummary?.total_review_events || 0}</Tag>
          <Tag color="green">approved history: {auditSummary?.approved_count || 0}</Tag>
          <Tag color="red">rejected history: {auditSummary?.rejected_count || 0}</Tag>
          <Tag color="orange">weak history: {auditSummary?.marked_weak_count || 0}</Tag>
          <Tag color="gold">source requested: {auditSummary?.needs_more_source_count || 0}</Tag>
          <Tag color="purple">merged history: {auditSummary?.duplicate_merged_count || 0}</Tag>
          <Tag color="default">latest: {formatDate(auditSummary?.latest_reviewed_at)}</Tag>
        </Space>
        <Space direction="vertical" className="full-width" size={4}>
          <Text strong>Review note</Text>
          <TextArea
            allowClear
            autoSize={{ minRows: 2, maxRows: 4 }}
            onChange={(event) => setReviewNote(event.target.value)}
            placeholder="Optional audit note, for example: source URL missing, mark as weak evidence."
            value={reviewNote}
          />
        </Space>
        <Space wrap>
          <Select options={reviewFilterOptions} value={filter} onChange={setFilter} style={{ width: 190 }} />
          <Button loading={queueLoading} onClick={refreshQueue} icon={<RefreshCw size={15} />}>
            Refresh review queue
          </Button>
        </Space>
        <Table
          columns={columns}
          dataSource={filteredItems}
          loading={queueLoading}
          locale={{ emptyText: 'No evidence currently needs human review.' }}
          pagination={{ pageSize: 5 }}
          rowKey="evidence_id"
          size="small"
        />
        <Alert
          message="Review history / audit timeline"
          description="Audit records only capture human review decisions. They do not mean the platform officially verified the evidence. The system does not fetch URLs or use AI to verify screenshot authenticity."
          showIcon
          type="info"
        />
        <Table
          columns={historyColumns}
          dataSource={reviewTimeline?.entries || []}
          loading={queueLoading}
          locale={{ emptyText: 'No review history yet.' }}
          pagination={{ pageSize: 5 }}
          rowKey="review_event_id"
          size="small"
        />
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
      width: 270,
      render: (_, record) => (
        <Space>
          <Button
            icon={<Link2 size={15} />}
            onClick={() => {
              void getCase(record.case_id).then((caseDetail) => onCaseReady?.(caseDetail))
            }}
            size="small"
          >
            打开
          </Button>
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
                <DistributionTags color="magenta" values={evidenceSummary.provenanceTypes} />
                <DistributionTags color="lime" values={evidenceSummary.trustLabels} />
                <DistributionTags color="blue" values={evidenceSummary.verificationStatuses} />
                <DistributionTags color="volcano" values={evidenceSummary.reviewStatuses} />
                <Tag color={evidenceSummary.sourceUrlMissing ? 'orange' : 'green'}>
                  source_url_present: {evidenceSummary.sourceUrlPresent}/{currentCase.evidence_item_count}
                </Tag>
                <Tag color={evidenceSummary.reviewNeeded ? 'orange' : 'green'}>review_needed: {evidenceSummary.reviewNeeded}</Tag>
                <Tag color={evidenceSummary.riskFlags?.user_attestation_missing ? 'orange' : 'green'}>
                  attestation_missing: {evidenceSummary.riskFlags?.user_attestation_missing || 0}
                </Tag>
                <Tag color={evidenceSummary.duplicateItems ? 'orange' : 'default'}>duplicates collapsed: {evidenceSummary.duplicateItems}</Tag>
              </Space>
              <Text type="secondary">
                Evidence attachment normalizes already available public or user-provided material; it does not fetch external sources or expose credentials. Low-trust or unverified evidence requires human review.
              </Text>
              {Object.keys(evidenceSummary.riskFlags).length ? (
                <Space size={[4, 4]} wrap>
                  <Text type="secondary">Review flags:</Text>
                  <DistributionTags color="orange" values={evidenceSummary.riskFlags} />
                </Space>
              ) : null}
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
        <EvidenceReviewQueuePanel currentCase={currentCase} onCaseReady={onCaseReady} />
      ) : null}

      {currentCase ? (
        <ManualEvidencePanel currentCase={currentCase} onCaseReady={onCaseReady} onRunCase={onRunCase} />
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
