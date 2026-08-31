import { useEffect, useRef, useState } from 'react'
import { Alert, Button, Card, Col, Descriptions, Input, List, Row, Select, Space, Tag, Typography } from 'antd'
import { Eye, Lock, ShieldCheck, TriangleAlert } from 'lucide-react'

import {
  getInternalAlphaGovernedReviewFormalState,
  getInternalAlphaIdentityReadyGovernedReviewDecisionAuditHistory,
  getInternalAlphaIdentityReadyGovernedReviewDecisionAuditProjection,
  getInternalAlphaLocalExchangeIdentityReadyV02Projection,
  getInternalAlphaLocalExchangeProjection,
  getInternalAlphaLocalExchangeSampleCatalog,
  getInternalAlphaReviewConsoleProjection,
  INTERNAL_ALPHA_LOCAL_EXCHANGE_IDENTITY_READY_V02_SAMPLE_HANDLE,
  INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_TYPES,
  INTERNAL_ALPHA_GOVERNED_RECORD_REVIEW_PROJECTION_ID,
  INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_PROJECTION_IDS,
  postInternalAlphaIdentityReadyGovernedReviewDecision,
  postInternalAlphaGovernedReviewDecision,
} from '../api/sentigraphApi.js'
import { INTERNAL_ALPHA_REVIEW_CONSOLE_STATIC_FIXTURE } from '../data/internalAlphaReviewConsoleStaticFixture.js'
import {
  buildInternalAlphaIdentityReadyReviewDecisionCandidate,
  INTERNAL_ALPHA_IDENTITY_READY_REVIEW_DECISION_TYPES,
} from '../utils/internalAlphaIdentityReadyReviewDecisionCandidate.js'

const { Paragraph, Text, Title } = Typography
const GOVERNED_REVIEW_CONSOLE_PROJECTION_ID = INTERNAL_ALPHA_GOVERNED_RECORD_REVIEW_PROJECTION_ID
const SAFE_REVIEW_CONSOLE_PROJECTION_ID = GOVERNED_REVIEW_CONSOLE_PROJECTION_ID
const REVIEW_CONSOLE_PROJECTION_ALLOWLIST = INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_PROJECTION_IDS
const LEGACY_SYNTHETIC_SELECTION_REFERENCE = 'INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_PROJECTION_IDS[0]'
const STATIC_SOURCE_CHAIN_BOUNDARY_LABEL =
  'source_chain_boundary = evidence_layer_write_candidate_boundary'
const GOVERNED_RECORD_REVIEW_VIEW = 'governedRecordReview'
const LOCAL_EXCHANGE_PROJECTION_REVIEW_VIEW = 'internalAlphaLocalExchangeProjectionReview'
const LOCAL_EXCHANGE_IDENTITY_READY_V02_REVIEW_VIEW =
  'internalAlphaLocalExchangeIdentityReadyV02Review'
const IDENTITY_READY_DURABLE_DECISION_AUDIT_READBACK_VIEW =
  'identityReadyDurableDecisionAuditReadback'

const INITIAL_LOCAL_EXCHANGE_CATALOG_STATE = Object.freeze({
  catalogPhase: 'loading',
  catalog: null,
  errorCode: null,
})

const INITIAL_LOCAL_EXCHANGE_PROJECTION_STATE = Object.freeze({
  requestPhase: 'idle',
  projectionPhase: null,
  projection: null,
  errorCode: null,
})

const INITIAL_LOCAL_EXCHANGE_IDENTITY_READY_V02_STATE = Object.freeze({
  requestPhase: 'idle',
  projection: null,
})

const LOCAL_EXCHANGE_PROJECTION_PHASES = Object.freeze([
  'manual_review_required',
  'blocked_upstream',
  'projection_unavailable',
  'ready_for_human_review',
])

const REVIEW_SURFACE_OPTIONS = Object.freeze([
  {
    value: GOVERNED_RECORD_REVIEW_VIEW,
    label: 'Governed record review (default)',
  },
  {
    value: LOCAL_EXCHANGE_PROJECTION_REVIEW_VIEW,
    label: 'Local-exchange projection review',
  },
  {
    value: LOCAL_EXCHANGE_IDENTITY_READY_V02_REVIEW_VIEW,
    label: 'Local-exchange identity-ready review v0.2',
  },
  {
    value: IDENTITY_READY_DURABLE_DECISION_AUDIT_READBACK_VIEW,
    label: 'Identity-ready durable decision audit readback',
  },
])

const GOVERNED_REVIEW_DECISION_OPTIONS = Object.freeze(
  INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_TYPES.map((decisionType) => ({
    value: decisionType,
    label: decisionType,
  })),
)

const IDENTITY_READY_REVIEW_DECISION_OPTIONS = Object.freeze([
  {
    value: 'keep_pending_human_review',
    label: 'Keep pending human review',
  },
  {
    value: 'request_more_governance_review',
    label: 'Request more governance review',
  },
])

const LOWER_HEX_64_PATTERN = /^[0-9a-f]{64}$/


const SAFE_METADATA_FIELDS = Object.freeze([
  'persisted_record_id',
  'attempt_reservation_id',
  'candidate_identity_digest',
  'input_safe_hash',
  'gate_contract_safe_hash',
  'activation_decision_safe_hash',
  'record_snapshot_digest',
  'reservation_snapshot_digest',
])

const GOVERNED_STATUS_DETAILS = Object.freeze({
  governed_record_review_ready: {
    statusLabel: 'governed record ready for human review',
    tagColor: 'cyan',
    description: 'The exact governed nonproduction record is available as bounded read-only metadata.',
  },
  governed_record_absent: {
    statusLabel: 'governed record absent',
    tagColor: 'default',
    description: 'No expected governed record or reservation is present.',
  },
  governed_record_missing_after_consumed_attempt: {
    statusLabel: 'record missing after consumed attempt',
    tagColor: 'orange',
    description: 'The expected reservation is present while the governed record is absent.',
  },
  governed_record_inconsistent: {
    statusLabel: 'governed record state inconsistent',
    tagColor: 'orange',
    description: 'The bounded reader could not safely classify the governed record state.',
  },
  governed_record_read_blocked_sidecar_present: {
    statusLabel: 'read blocked because a sidecar is present',
    tagColor: 'orange',
    description: 'Read-only review is blocked while a prohibited sidecar state is present.',
  },
  governed_record_target_unavailable: {
    statusLabel: 'governed target unavailable',
    tagColor: 'default',
    description: 'Target identity or metadata could not be safely verified.',
  },
  governed_record_read_only_audit_failed: {
    statusLabel: 'bounded read-only audit failed',
    tagColor: 'default',
    description: 'The bounded reader failed closed without exposing target details.',
  },
})

const STATIC_FALLBACK_ROUTE_STATE = {
  status: 'checking',
  statusLabel: 'checking disabled backend route',
  routeBackendConnection: 'static_fallback_active_not_connected',
  tagColor: 'default',
  description: 'static fallback active; backend route disabled / not connected state is handled safely.',
  detail: 'route_disabled and unsupported_projection responses remain safe not-connected state.',
  projection: null,
}

function staticRouteState({
  status,
  statusLabel,
  routeBackendConnection,
  description,
  detail,
}) {
  return {
    status,
    statusLabel,
    routeBackendConnection,
    tagColor: 'default',
    description,
    detail,
    projection: null,
  }
}

function describeRouteState(payload) {
  if (payload?.error === 'route_disabled') {
    return staticRouteState({
      status: 'disabled',
      statusLabel: 'backend route disabled',
      routeBackendConnection: 'backend_route_disabled_static_fallback',
      description: 'backend route disabled / not connected / static fallback active.',
      detail: 'route_disabled response keeps the page in safe not-connected state.',
    })
  }

  if (payload?.error === 'governed_record_projection_disabled') {
    return staticRouteState({
      status: 'governed_disabled',
      statusLabel: 'governed record projection disabled',
      routeBackendConnection: 'governed_record_projection_disabled_static_fallback',
      description: 'governed record projection disabled; static fallback remains active.',
      detail: 'The second read-only gate is disabled and no governed target reader was called.',
    })
  }

  if (payload?.error === 'unsupported_projection') {
    return staticRouteState({
      status: 'unsupported',
      statusLabel: 'unsupported projection',
      routeBackendConnection: 'unsupported_projection_static_fallback',
      description: 'unsupported_projection response keeps static fallback active.',
      detail: 'No alternate projection is loaded automatically.',
    })
  }

  const projectionStatus = payload?.projection_status
  const statusDetail = GOVERNED_STATUS_DETAILS[projectionStatus]
  const projection = payload?.projection
  if (
    payload?.projection_id === GOVERNED_REVIEW_CONSOLE_PROJECTION_ID &&
    projection &&
    statusDetail
  ) {
    return {
      status: projectionStatus,
      statusLabel: statusDetail.statusLabel,
      routeBackendConnection: 'governed_record_read_only_projection',
      tagColor: statusDetail.tagColor,
      description: statusDetail.description,
      detail: 'One internal GET returned the bounded governed-record projection; this is not operator runtime.',
      projection,
    }
  }

  return staticRouteState({
    status: 'unavailable',
    statusLabel: 'backend route unavailable',
    routeBackendConnection: 'backend_route_unavailable_static_fallback',
    description: 'backend route unavailable / not connected / static fallback active.',
    detail: 'Unexpected response shape is treated as safe not-connected state.',
  })
}

function BooleanTag({ label, value }) {
  return (
    <Tag color={value ? 'cyan' : 'default'}>
      {label} = {String(value)}
    </Tag>
  )
}

function SummaryCard({ icon, title, children }) {
  return (
    <Card className="panel-card internal-alpha-review-card">
      <Space direction="vertical" size={12} className="full-width">
        <Space>
          {icon}
          <Title level={4}>{title}</Title>
        </Space>
        {children}
      </Space>
    </Card>
  )
}

function displaySafeValue(value) {
  return typeof value === 'string' && value ? value : 'not available in this state'
}

function describeLocalExchangeProjection(projection) {
  const projectionPhase = projection.projection_status
  if (!LOCAL_EXCHANGE_PROJECTION_PHASES.includes(projectionPhase)) {
    return {
      requestPhase: 'bounded_error',
      projectionPhase: null,
      projection: null,
      errorCode: 'frontend_projection_contract_mismatch',
    }
  }
  return {
    requestPhase: projectionPhase === 'projection_unavailable' ? 'unavailable' : 'loaded',
    projectionPhase,
    projection,
    errorCode: projection.projection_error_code,
  }
}

export function InternalAlphaReviewConsole() {
  const fixture = INTERNAL_ALPHA_REVIEW_CONSOLE_STATIC_FIXTURE
  const [routeState, setRouteState] = useState(STATIC_FALLBACK_ROUTE_STATE)
  const [selectedReviewView, setSelectedReviewView] = useState(GOVERNED_RECORD_REVIEW_VIEW)
  const [selectedGovernedDecisionType, setSelectedGovernedDecisionType] = useState(null)
  const [governedDecisionRequestState, setGovernedDecisionRequestState] = useState({
    phase: 'idle',
    result: null,
  })
  const [governedFormalStateRequestState, setGovernedFormalStateRequestState] = useState({
    phase: 'loading',
    result: null,
  })
  const [localExchangeCatalogState, setLocalExchangeCatalogState] = useState(
    INITIAL_LOCAL_EXCHANGE_CATALOG_STATE,
  )
  const [selectedLocalExchangeSampleHandle, setSelectedLocalExchangeSampleHandle] = useState(null)
  const [localExchangeProjectionStateByHandle, setLocalExchangeProjectionStateByHandle] = useState({})
  const [localExchangeIdentityReadyV02State, setLocalExchangeIdentityReadyV02State] = useState(
    INITIAL_LOCAL_EXCHANGE_IDENTITY_READY_V02_STATE,
  )
  const [selectedIdentityReadyDecisionType, setSelectedIdentityReadyDecisionType] =
    useState(null)
  const [identityReadyDecisionCandidateState, setIdentityReadyDecisionCandidateState] =
    useState({ phase: 'idle', candidate: null })
  const [identityReadyDecisionPersistenceState, setIdentityReadyDecisionPersistenceState] =
    useState({ phase: 'idle', result: null })
  const [identityReadyAuditDecisionIdInput, setIdentityReadyAuditDecisionIdInput] =
    useState('')
  const [identityReadyDecisionAuditState, setIdentityReadyDecisionAuditState] =
    useState({ phase: 'idle', result: null })
  const [identityReadyDecisionHistoryState, setIdentityReadyDecisionHistoryState] =
    useState({ phase: 'not_loaded', result: null })
  const requestedLocalExchangeHandles = useRef(new Set())
  const localExchangeIdentityReadyV02RequestStarted = useRef(false)
  const identityReadyDecisionCandidateBuildStarted = useRef(false)
  const identityReadyDecisionPersistencePostStarted = useRef(false)
  const identityReadyDecisionAuditGetStarted = useRef(false)
  const identityReadyDecisionHistoryGetStarted = useRef(false)
  const localExchangeCatalogRequestStarted = useRef(false)
  const governedDecisionPostAttemptStarted = useRef(false)
  const governedFormalStateGetAttemptStarted = useRef(false)
  const governedProjectionGetAttemptStarted = useRef(false)
  const pageIsMounted = useRef(true)
  const localExchangeCatalog = localExchangeCatalogState.catalog
  const catalogPhase = localExchangeCatalogState.catalogPhase
  const selectedLocalExchangeSample = localExchangeCatalog?.samples.find(
    (sample) => sample.sample_handle === selectedLocalExchangeSampleHandle,
  )
  const identityReadyV02Sample = localExchangeCatalog?.samples.find(
    (sample) =>
      sample.sample_handle ===
      INTERNAL_ALPHA_LOCAL_EXCHANGE_IDENTITY_READY_V02_SAMPLE_HANDLE,
  )
  const localExchangeSampleOptions = localExchangeCatalog
    ? localExchangeCatalog.samples.map((sample) => ({
        value: sample.sample_handle,
        label: sample.display_label,
        title: sample.sample_role,
        disabled: !sample.enabled,
      }))
    : []

  useEffect(() => {
    pageIsMounted.current = true
    return () => {
      pageIsMounted.current = false
    }
  }, [])

  useEffect(() => {
    if (governedFormalStateGetAttemptStarted.current) return
    governedFormalStateGetAttemptStarted.current = true

    getInternalAlphaGovernedReviewFormalState()
      .then((result) => {
        if (!pageIsMounted.current) return
        setGovernedFormalStateRequestState({
          phase: 'bounded_result',
          result,
        })
      })
      .catch(() => {
        if (!pageIsMounted.current) return
        setGovernedFormalStateRequestState({
          phase: 'bounded_error',
          result: null,
        })
      })
  }, [])

  useEffect(() => {
    if (localExchangeCatalogRequestStarted.current) return
    localExchangeCatalogRequestStarted.current = true

    getInternalAlphaLocalExchangeSampleCatalog()
      .then((catalog) => {
        if (!pageIsMounted.current) return
        const defaultSample = catalog.samples.find((sample) => sample.is_default)
        setLocalExchangeCatalogState({
          catalogPhase: 'loaded',
          catalog,
          errorCode: null,
        })
        setSelectedLocalExchangeSampleHandle(defaultSample.sample_handle)
        setLocalExchangeProjectionStateByHandle(
          Object.fromEntries(
            catalog.samples.map((sample) => [
              sample.sample_handle,
              INITIAL_LOCAL_EXCHANGE_PROJECTION_STATE,
            ]),
          ),
        )
      })
      .catch(() => {
        if (!pageIsMounted.current) return
        setLocalExchangeCatalogState({
          catalogPhase: 'unavailable',
          catalog: null,
          errorCode: 'sample_catalog_unavailable',
        })
        setSelectedLocalExchangeSampleHandle(null)
        setLocalExchangeProjectionStateByHandle({})
      })
  }, [])

  useEffect(() => {
    if (governedProjectionGetAttemptStarted.current) return
    governedProjectionGetAttemptStarted.current = true

    getInternalAlphaReviewConsoleProjection(GOVERNED_REVIEW_CONSOLE_PROJECTION_ID)
      .then((payload) => {
        if (!pageIsMounted.current) return
        setRouteState(describeRouteState(payload))
      })
      .catch(() => {
        if (!pageIsMounted.current) return
        setRouteState(
          staticRouteState({
            status: 'unavailable',
            statusLabel: 'backend route unavailable',
            routeBackendConnection: 'backend_route_unavailable_static_fallback',
            description: 'backend route unavailable / not connected / static fallback active.',
            detail: 'Network or local backend absence keeps this shell in safe not-connected state.',
          }),
        )
      })
  }, [])

  useEffect(() => {
    if (selectedReviewView !== LOCAL_EXCHANGE_PROJECTION_REVIEW_VIEW) return
    if (catalogPhase !== 'loaded' || !selectedLocalExchangeSample?.enabled) return
    if (typeof selectedLocalExchangeSampleHandle !== 'string') return
    if (requestedLocalExchangeHandles.current.has(selectedLocalExchangeSampleHandle)) return

    requestedLocalExchangeHandles.current.add(selectedLocalExchangeSampleHandle)
    setLocalExchangeProjectionStateByHandle((currentStateByHandle) => ({
      ...currentStateByHandle,
      [selectedLocalExchangeSampleHandle]: {
        requestPhase: 'loading',
        projectionPhase: null,
        projection: null,
        errorCode: null,
      },
    }))
    getInternalAlphaLocalExchangeProjection(selectedLocalExchangeSampleHandle)
      .then((projection) => {
        if (!pageIsMounted.current) return
        setLocalExchangeProjectionStateByHandle((currentStateByHandle) => ({
          ...currentStateByHandle,
          [selectedLocalExchangeSampleHandle]: describeLocalExchangeProjection(projection),
        }))
      })
      .catch(() => {
        if (!pageIsMounted.current) return
        setLocalExchangeProjectionStateByHandle((currentStateByHandle) => ({
          ...currentStateByHandle,
          [selectedLocalExchangeSampleHandle]: {
            requestPhase: 'bounded_error',
            projectionPhase: null,
            projection: null,
            errorCode: 'frontend_projection_contract_mismatch',
          },
        }))
      })
  }, [
    catalogPhase,
    selectedLocalExchangeSample?.enabled,
    selectedLocalExchangeSampleHandle,
    selectedReviewView,
  ])

  useEffect(() => {
    if (selectedReviewView !== LOCAL_EXCHANGE_IDENTITY_READY_V02_REVIEW_VIEW) return
    if (catalogPhase !== 'loaded' || !identityReadyV02Sample?.enabled) return
    if (localExchangeIdentityReadyV02RequestStarted.current) return

    localExchangeIdentityReadyV02RequestStarted.current = true
    setLocalExchangeIdentityReadyV02State({
      requestPhase: 'loading',
      projection: null,
    })
    getInternalAlphaLocalExchangeIdentityReadyV02Projection(
      INTERNAL_ALPHA_LOCAL_EXCHANGE_IDENTITY_READY_V02_SAMPLE_HANDLE,
    )
      .then((projection) => {
        if (!pageIsMounted.current) return
        setLocalExchangeIdentityReadyV02State({
          requestPhase: 'loaded',
          projection,
        })
      })
      .catch(() => {
        if (!pageIsMounted.current) return
        setLocalExchangeIdentityReadyV02State({
          requestPhase: 'bounded_unavailable',
          projection: null,
        })
      })
  }, [catalogPhase, identityReadyV02Sample?.enabled, selectedReviewView])

  const governedProjection = routeState.projection
  const governedAllowedActionsAreBounded = Array.isArray(governedProjection?.allowed_actions)
  const governedAllowedActions = governedAllowedActionsAreBounded
    ? governedProjection.allowed_actions
    : []
  const governedDecisionSurfaceReady =
    selectedReviewView === GOVERNED_RECORD_REVIEW_VIEW &&
    governedProjection !== null &&
    routeState.status === 'governed_record_review_ready' &&
    governedProjection.projection_status === 'governed_record_review_ready' &&
    governedProjection.human_review_required === true &&
    governedProjection.no_automatic_trust_upgrade === true &&
    governedAllowedActionsAreBounded
  const selectedGovernedDecisionIsAllowed =
    governedDecisionSurfaceReady &&
    INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_TYPES.includes(selectedGovernedDecisionType) &&
    governedAllowedActions.includes(selectedGovernedDecisionType)
  const identityReadyProjection = localExchangeIdentityReadyV02State.projection
  const identityReadyReviewSubjectIdentity = identityReadyProjection?.review_subject_identity
  const identityReadyDecisionSurfaceReady =
    selectedReviewView === LOCAL_EXCHANGE_IDENTITY_READY_V02_REVIEW_VIEW &&
    localExchangeIdentityReadyV02State.requestPhase === 'loaded' &&
    identityReadyProjection?.projection_status === 'ready_for_human_review' &&
    identityReadyProjection?.review_status === 'ready_for_human_review' &&
    identityReadyReviewSubjectIdentity?.identity_schema ===
      'sentigraph_b05_review_subject_identity_v0_1' &&
    identityReadyReviewSubjectIdentity?.identity_version === '0.1' &&
    identityReadyReviewSubjectIdentity?.identity_status === 'ready' &&
    identityReadyReviewSubjectIdentity?.sample_handle ===
      INTERNAL_ALPHA_LOCAL_EXCHANGE_IDENTITY_READY_V02_SAMPLE_HANDLE &&
    LOWER_HEX_64_PATTERN.test(
      identityReadyReviewSubjectIdentity?.review_subject_binding_safe_hash ?? '',
    )
  const selectedIdentityReadyDecisionIsAllowed =
    identityReadyDecisionSurfaceReady &&
    INTERNAL_ALPHA_IDENTITY_READY_REVIEW_DECISION_TYPES.includes(
      selectedIdentityReadyDecisionType,
    )

  const handleIdentityReadyDecisionSelection = (decisionType) => {
    if (
      identityReadyDecisionCandidateBuildStarted.current ||
      !INTERNAL_ALPHA_IDENTITY_READY_REVIEW_DECISION_TYPES.includes(decisionType)
    ) {
      return
    }
    setSelectedIdentityReadyDecisionType(decisionType)
    setIdentityReadyDecisionCandidateState({ phase: 'idle', candidate: null })
    setIdentityReadyDecisionPersistenceState({ phase: 'idle', result: null })
  }

  const handleIdentityReadyDecisionConfirmation = () => {
    if (
      !selectedIdentityReadyDecisionIsAllowed ||
      identityReadyDecisionCandidateBuildStarted.current
    ) {
      return
    }

    identityReadyDecisionCandidateBuildStarted.current = true
    setIdentityReadyDecisionCandidateState({ phase: 'building', candidate: null })
    try {
      const candidate = buildInternalAlphaIdentityReadyReviewDecisionCandidate(
        identityReadyReviewSubjectIdentity,
        selectedIdentityReadyDecisionType,
      )
      setIdentityReadyDecisionCandidateState({ phase: 'candidate_ready', candidate })
    } catch {
      setIdentityReadyDecisionCandidateState({ phase: 'bounded_error', candidate: null })
    }
  }

  const handleIdentityReadyDecisionPersistenceConfirmation = async () => {
    const candidate = identityReadyDecisionCandidateState.candidate
    if (
      identityReadyDecisionCandidateState.phase !== 'candidate_ready' ||
      candidate === null ||
      identityReadyDecisionPersistencePostStarted.current
    ) {
      return
    }

    identityReadyDecisionPersistencePostStarted.current = true
    setIdentityReadyDecisionPersistenceState({ phase: 'posting', result: null })
    try {
      const result = await postInternalAlphaIdentityReadyGovernedReviewDecision(candidate)
      if (!pageIsMounted.current) return
      const success = ['created', 'already_exists'].includes(result.request_status)
      setIdentityReadyDecisionPersistenceState({
        phase: success ? 'bounded_success' : 'bounded_unavailable',
        result: success ? result : null,
      })
    } catch {
      if (!pageIsMounted.current) return
      setIdentityReadyDecisionPersistenceState({ phase: 'bounded_error', result: null })
    }
  }

  const boundedReceiptDecisionId =
    identityReadyDecisionPersistenceState.phase === 'bounded_success'
      ? identityReadyDecisionPersistenceState.result?.decision_id
      : null
  const identityReadyAuditDecisionId = identityReadyAuditDecisionIdInput.trim()
  const identityReadyAuditDecisionIdIsValid =
    /^irghrd-[0-9a-f]{32}$/.test(identityReadyAuditDecisionId)

  const handleUseBoundedReceiptDecisionId = () => {
    if (
      identityReadyDecisionAuditGetStarted.current ||
      typeof boundedReceiptDecisionId !== 'string' ||
      !/^irghrd-[0-9a-f]{32}$/.test(boundedReceiptDecisionId)
    ) {
      return
    }
    setIdentityReadyAuditDecisionIdInput(boundedReceiptDecisionId)
    setIdentityReadyDecisionAuditState({ phase: 'idle', result: null })
  }

  const handleIdentityReadyDecisionAuditReadback = async () => {
    if (
      !identityReadyAuditDecisionIdIsValid ||
      identityReadyDecisionAuditGetStarted.current
    ) {
      return
    }
    identityReadyDecisionAuditGetStarted.current = true
    setIdentityReadyDecisionAuditState({ phase: 'loading', result: null })
    try {
      const result =
        await getInternalAlphaIdentityReadyGovernedReviewDecisionAuditProjection(
          identityReadyAuditDecisionId,
        )
      if (!pageIsMounted.current) return
      setIdentityReadyDecisionAuditState({
        phase:
          result.readback_status === 'decision_audit_ready'
            ? 'bounded_success'
            : 'bounded_result',
        result,
      })
    } catch {
      if (!pageIsMounted.current) return
      setIdentityReadyDecisionAuditState({ phase: 'bounded_error', result: null })
    }
  }

  const handleIdentityReadyDecisionHistoryLoad = async () => {
    if (identityReadyDecisionHistoryGetStarted.current) return
    identityReadyDecisionHistoryGetStarted.current = true
    setIdentityReadyDecisionHistoryState({ phase: 'loading', result: null })
    try {
      const result =
        await getInternalAlphaIdentityReadyGovernedReviewDecisionAuditHistory(20)
      if (!pageIsMounted.current) return
      setIdentityReadyDecisionHistoryState({
        phase:
          result.history_status === 'decision_history_ready'
            ? 'bounded_success'
            : 'bounded_result',
        result,
      })
    } catch {
      if (!pageIsMounted.current) return
      setIdentityReadyDecisionHistoryState({ phase: 'bounded_error', result: null })
    }
  }

  const handleGovernedDecisionSelection = (decisionType) => {
    if (governedDecisionPostAttemptStarted.current) return
    setSelectedGovernedDecisionType(decisionType)
    setGovernedDecisionRequestState({ phase: 'idle', result: null })
  }

  const handleGovernedDecisionConfirmation = async () => {
    if (
      !selectedGovernedDecisionIsAllowed ||
      governedDecisionPostAttemptStarted.current
    ) {
      return
    }

    governedDecisionPostAttemptStarted.current = true
    setGovernedDecisionRequestState({ phase: 'posting', result: null })
    try {
      const result = await postInternalAlphaGovernedReviewDecision(
        selectedGovernedDecisionType,
      )
      if (!pageIsMounted.current) return
      const success = ['created', 'already_exists'].includes(result.request_status)
      setGovernedDecisionRequestState({
        phase: success ? 'bounded_success' : 'bounded_unavailable',
        result: success ? result : null,
      })
    } catch {
      if (!pageIsMounted.current) return
      setGovernedDecisionRequestState({ phase: 'bounded_error', result: null })
    }
  }

  const reviewSurfaceSelector = (
    <Card className="panel-card internal-alpha-review-card">
      <Space wrap align="center">
        <Text strong>Read-only review surface</Text>
        <Select
          aria-label="Read-only review surface"
          value={selectedReviewView}
          options={REVIEW_SURFACE_OPTIONS}
          onChange={setSelectedReviewView}
          style={{ minWidth: 320 }}
        />
        <Text type="secondary">Selection changes presentation only and grants no authority.</Text>
      </Space>
    </Card>
  )

  if (selectedReviewView === IDENTITY_READY_DURABLE_DECISION_AUDIT_READBACK_VIEW) {
    return (
      <div className="page-stack internal-alpha-review-shell-page">
        {reviewSurfaceSelector}

        <section className="internal-alpha-review-hero">
          <div>
            <Space wrap>
              <Tag color="cyan">internal alpha</Tag>
              <Tag color="cyan">exact decision-id read-only audit</Tag>
              <Tag color="default">disabled by default</Tag>
              <Tag color="default">explicit action only</Tag>
            </Space>
            <Title level={1}>Identity-ready durable decision audit readback</Title>
            <Paragraph>
              This independent surface performs one bounded read-only audit projection for one exact
              identity-ready decision identifier. Selecting this view performs no request.
            </Paragraph>
          </div>
          <Card className="panel-card internal-alpha-review-status-card">
            <Space direction="vertical" size={12} className="full-width">
              <Text type="secondary">Readback phase</Text>
              <Title level={2}>{identityReadyDecisionAuditState.phase}</Title>
              <Text>GET is permitted only by the explicit readback action below.</Text>
            </Space>
          </Card>
        </section>

        <Card className="panel-card internal-alpha-review-card">
          <Title level={4}>Exact durable decision identifier</Title>
          <Paragraph>
            Enter one exact identity-ready decision identifier or copy it from the bounded receipt retained
            in this page mount. No sample lookup, list, history, fallback, or POST is performed.
          </Paragraph>
          <Space wrap align="center">
            <Input
              aria-label="Identity-ready durable decision audit identifier"
              value={identityReadyAuditDecisionIdInput}
              onChange={(event) => {
                if (identityReadyDecisionAuditGetStarted.current) return
                setIdentityReadyAuditDecisionIdInput(event.target.value)
                setIdentityReadyDecisionAuditState({ phase: 'idle', result: null })
              }}
              disabled={identityReadyDecisionAuditGetStarted.current}
              placeholder="irghrd-0123456789abcdef0123456789abcdef"
              style={{ minWidth: 420 }}
            />
            {typeof boundedReceiptDecisionId === 'string' && (
              <Button
                onClick={handleUseBoundedReceiptDecisionId}
                disabled={identityReadyDecisionAuditGetStarted.current}
              >
                Use bounded receipt decision ID
              </Button>
            )}
            <Button
              type="primary"
              onClick={handleIdentityReadyDecisionAuditReadback}
              disabled={
                !identityReadyAuditDecisionIdIsValid ||
                identityReadyDecisionAuditGetStarted.current
              }
              loading={identityReadyDecisionAuditState.phase === 'loading'}
            >
              Read exact audit projection
            </Button>
          </Space>
          {!identityReadyAuditDecisionIdIsValid && (
            <Paragraph type="secondary">
              A lowercase identifier matching irghrd plus 32 hexadecimal characters is required.
            </Paragraph>
          )}

          {identityReadyDecisionAuditState.phase === 'bounded_error' && (
            <Alert
              showIcon
              type="error"
              message="Durable decision audit readback failed closed"
              description="No retry, fallback, POST, raw error, database path, or protected value is exposed."
            />
          )}
          {identityReadyDecisionAuditState.phase === 'bounded_result' && (
            <Alert
              showIcon
              type="warning"
              message="Durable decision audit readback unavailable"
              description={`readback_status = ${identityReadyDecisionAuditState.result.readback_status}`}
            />
          )}
          {identityReadyDecisionAuditState.phase === 'bounded_success' && (
            <Descriptions column={1} size="small" title="Safe durable decision audit projection">
              <Descriptions.Item label="readback_status">
                {identityReadyDecisionAuditState.result.readback_status}
              </Descriptions.Item>
              <Descriptions.Item label="decision_id">
                {identityReadyDecisionAuditState.result.decision_id}
              </Descriptions.Item>
              <Descriptions.Item label="audit_receipt_reference">
                {identityReadyDecisionAuditState.result.audit_receipt_reference}
              </Descriptions.Item>
              <Descriptions.Item label="sample_handle">
                {identityReadyDecisionAuditState.result.sample_handle}
              </Descriptions.Item>
              <Descriptions.Item label="decision_type">
                {identityReadyDecisionAuditState.result.decision_type}
              </Descriptions.Item>
              <Descriptions.Item label="decision_status">
                {identityReadyDecisionAuditState.result.decision_status}
              </Descriptions.Item>
              <Descriptions.Item label="recorded_at">
                {identityReadyDecisionAuditState.result.recorded_at}
              </Descriptions.Item>
              <Descriptions.Item label="human_review_required">
                {String(identityReadyDecisionAuditState.result.human_review_required)}
              </Descriptions.Item>
              <Descriptions.Item label="no_automatic_trust_upgrade">
                {String(identityReadyDecisionAuditState.result.no_automatic_trust_upgrade)}
              </Descriptions.Item>
              <Descriptions.Item label="production_object_enabled">
                {String(identityReadyDecisionAuditState.result.production_object_enabled)}
              </Descriptions.Item>
              <Descriptions.Item label="review_queue_runtime_enabled">
                {String(identityReadyDecisionAuditState.result.review_queue_runtime_enabled)}
              </Descriptions.Item>
              <Descriptions.Item label="evidence_layer_write_performed">
                {String(identityReadyDecisionAuditState.result.evidence_layer_write_performed)}
              </Descriptions.Item>
              <Descriptions.Item label="provider_or_b05_called">
                {String(identityReadyDecisionAuditState.result.provider_or_b05_called)}
              </Descriptions.Item>
              <Descriptions.Item label="analysis_triggered">
                {String(identityReadyDecisionAuditState.result.analysis_triggered)}
              </Descriptions.Item>
              <Descriptions.Item label="report_triggered">
                {String(identityReadyDecisionAuditState.result.report_triggered)}
              </Descriptions.Item>
            </Descriptions>
          )}
        </Card>

        <Card className="panel-card internal-alpha-review-card">
          <Space direction="vertical" size={12} className="full-width">
            <Space wrap align="center">
              <Title level={4} style={{ margin: 0 }}>Recent auditable decisions</Title>
              <Tag color="cyan">internal only</Tag>
              <Tag color="default">bounded to 20</Tag>
              <Tag color="default">read only</Tag>
            </Space>
            <Paragraph>
              Load a deterministic safe history projection only after explicit action. This control
              performs no point-lookup fan-out, persistence, trust upgrade, analysis, or report action.
            </Paragraph>
            <Space wrap align="center">
              <Button
                onClick={handleIdentityReadyDecisionHistoryLoad}
                disabled={identityReadyDecisionHistoryGetStarted.current}
                loading={identityReadyDecisionHistoryState.phase === 'loading'}
              >
                Load recent auditable decisions
              </Button>
              <Text type="secondary">
                history_state = {identityReadyDecisionHistoryState.phase}
              </Text>
            </Space>

            {identityReadyDecisionHistoryState.phase === 'bounded_error' && (
              <Alert
                showIcon
                type="error"
                message="Decision history read failed closed"
                description="No retry, fallback, point-lookup fan-out, raw row, or protected value is exposed."
              />
            )}
            {identityReadyDecisionHistoryState.phase === 'bounded_result' && (
              <Alert
                showIcon
                type="warning"
                message="Decision history unavailable"
                description={`history_status = ${identityReadyDecisionHistoryState.result.history_status}`}
              />
            )}
            {identityReadyDecisionHistoryState.phase === 'bounded_success' &&
              identityReadyDecisionHistoryState.result.returned_count === 0 && (
                <Alert
                  showIcon
                  type="info"
                  message="No recent auditable decisions"
                  description="The bounded read-only history contains zero safe rows."
                />
              )}
            {identityReadyDecisionHistoryState.phase === 'bounded_success' &&
              identityReadyDecisionHistoryState.result.returned_count > 0 && (
                <List
                  aria-label="Recent auditable decision history"
                  dataSource={identityReadyDecisionHistoryState.result.decisions}
                  renderItem={(decision) => (
                    <List.Item key={decision.decision_id}>
                      <Descriptions column={1} size="small">
                        <Descriptions.Item label="decision_id">
                          {decision.decision_id}
                        </Descriptions.Item>
                        <Descriptions.Item label="audit_receipt_reference">
                          {decision.audit_receipt_reference}
                        </Descriptions.Item>
                        <Descriptions.Item label="sample_handle">
                          {decision.sample_handle}
                        </Descriptions.Item>
                        <Descriptions.Item label="decision_type">
                          {decision.decision_type}
                        </Descriptions.Item>
                        <Descriptions.Item label="decision_status">
                          {decision.decision_status}
                        </Descriptions.Item>
                        <Descriptions.Item label="recorded_at">
                          {decision.recorded_at}
                        </Descriptions.Item>
                        <Descriptions.Item label="human_review_required">
                          {String(decision.human_review_required)}
                        </Descriptions.Item>
                        <Descriptions.Item label="no_automatic_trust_upgrade">
                          {String(decision.no_automatic_trust_upgrade)}
                        </Descriptions.Item>
                        <Descriptions.Item label="production_object_enabled">
                          {String(decision.production_object_enabled)}
                        </Descriptions.Item>
                        <Descriptions.Item label="provider_or_b05_called">
                          {String(decision.provider_or_b05_called)}
                        </Descriptions.Item>
                        <Descriptions.Item label="analysis_triggered">
                          {String(decision.analysis_triggered)}
                        </Descriptions.Item>
                        <Descriptions.Item label="report_triggered">
                          {String(decision.report_triggered)}
                        </Descriptions.Item>
                      </Descriptions>
                    </List.Item>
                  )}
                />
              )}
          </Space>
        </Card>

        <Card className="panel-card internal-alpha-review-card">
          <Space wrap>
            <Tag color="cyan">read_only = true</Tag>
            <Tag color="cyan">exact_decision_id_only = true</Tag>
            <Tag color="default">mount_get = 0</Tag>
            <Tag color="default">selection_get = 0</Tag>
            <Tag color="default">post = 0</Tag>
            <Tag color="default">fallback = 0</Tag>
          </Space>
        </Card>
      </div>
    )
  }

  if (selectedReviewView === LOCAL_EXCHANGE_IDENTITY_READY_V02_REVIEW_VIEW) {
    const identityProjection = identityReadyProjection
    const reviewSubjectIdentity = identityProjection?.review_subject_identity

    return (
      <div className="page-stack internal-alpha-review-shell-page">
        {reviewSurfaceSelector}

        <section className="internal-alpha-review-hero">
          <div>
            <Space wrap>
              <Tag color="cyan">internal alpha</Tag>
              <Tag color="cyan">B05 identity-ready v0.2</Tag>
              <Tag color="default">display-only</Tag>
              <Tag color="default">human review required</Tag>
            </Space>
            <Title level={1}>Local-exchange identity-ready review v0.2</Title>
            <Paragraph>
              This separately selected panel displays one bounded identity-ready projection in page-local memory.
              It grants no review decision, persistence, analysis, publication, export, or delivery authority.
            </Paragraph>
            <Alert
              className="internal-alpha-review-boundary-alert"
              showIcon
              type="info"
              message="Identity-ready read-only boundary"
              description={
                <Space direction="vertical" size={2}>
                  <Text>Human review required.</Text>
                  <Text>Metadata-only.</Text>
                  <Text>In-memory-only.</Text>
                  <Text>No automatic trust upgrade.</Text>
                  <Text>Not full-web coverage.</Text>
                  <Text>Not full-platform coverage.</Text>
                  <Text>Not official verification.</Text>
                  <Text>No decision has yet been made.</Text>
                </Space>
              }
            />
          </div>

          <Card className="panel-card internal-alpha-review-status-card">
            <Space direction="vertical" size={12} className="full-width">
              <Text type="secondary">Request phase</Text>
              <Title level={2}>{localExchangeIdentityReadyV02State.requestPhase}</Title>
              <Text>
                Curated display label = {identityReadyV02Sample?.display_label ?? 'not available'}
              </Text>
              <Text>
                sample_handle = {INTERNAL_ALPHA_LOCAL_EXCHANGE_IDENTITY_READY_V02_SAMPLE_HANDLE}
              </Text>
            </Space>
          </Card>
        </section>

        <Card className="panel-card internal-alpha-review-card">
          <Descriptions column={1} size="small">
            <Descriptions.Item label="projection_schema">
              {identityProjection?.projection_schema ?? 'not loaded'}
            </Descriptions.Item>
            <Descriptions.Item label="projection_version">
              {identityProjection?.projection_version ?? 'not loaded'}
            </Descriptions.Item>
            <Descriptions.Item label="projection_status">
              {identityProjection?.projection_status ?? 'not loaded'}
            </Descriptions.Item>
            <Descriptions.Item label="review_status">
              {identityProjection?.review_status ?? 'not loaded'}
            </Descriptions.Item>
            <Descriptions.Item label="identity_schema">
              {reviewSubjectIdentity?.identity_schema ?? 'not loaded'}
            </Descriptions.Item>
            <Descriptions.Item label="identity_version">
              {reviewSubjectIdentity?.identity_version ?? 'not loaded'}
            </Descriptions.Item>
            <Descriptions.Item label="identity_status">
              {reviewSubjectIdentity?.identity_status ?? 'not loaded'}
            </Descriptions.Item>
            <Descriptions.Item label="review_subject_binding_safe_hash">
              {reviewSubjectIdentity?.review_subject_binding_safe_hash ?? 'not loaded'}
            </Descriptions.Item>
          </Descriptions>
        </Card>

        <Card className="panel-card internal-alpha-review-card">
          <Title level={4}>Governed human-review decision candidate</Title>
          <Paragraph>
            This explicit confirmation creates one deterministic, immutable candidate in page-local memory only.
            It performs no backend write, persistence, trust upgrade, analysis, publication, export, or delivery.
          </Paragraph>
          <Space wrap align="center">
            <Select
              aria-label="Identity-ready human-review decision candidate action"
              value={selectedIdentityReadyDecisionType ?? undefined}
              options={IDENTITY_READY_REVIEW_DECISION_OPTIONS}
              onChange={handleIdentityReadyDecisionSelection}
              disabled={
                !identityReadyDecisionSurfaceReady ||
                identityReadyDecisionCandidateBuildStarted.current
              }
              placeholder="Select one bounded action"
              style={{ minWidth: 320 }}
            />
            <Button
              type="primary"
              onClick={handleIdentityReadyDecisionConfirmation}
              disabled={
                !selectedIdentityReadyDecisionIsAllowed ||
                identityReadyDecisionCandidateBuildStarted.current
              }
            >
              Confirm local decision candidate
            </Button>
          </Space>
          <Paragraph type="secondary">
            Selecting an action does not create a candidate. Confirmation is explicit and limited to one candidate
            per page mount.
          </Paragraph>

          {!identityReadyDecisionSurfaceReady && (
            <Alert
              showIcon
              type="warning"
              message="Decision candidate control unavailable"
              description="The control remains inactive unless the exact identity-ready projection and safe binding are valid."
            />
          )}
          {identityReadyDecisionCandidateState.phase === 'bounded_error' && (
            <Alert
              showIcon
              type="error"
              message="Decision candidate creation failed closed"
              description="No candidate was retained and no persistence or backend action was attempted."
            />
          )}
          {identityReadyDecisionCandidateState.phase === 'candidate_ready' && (
            <>
              <Descriptions column={1} size="small" title="Local decision candidate">
                <Descriptions.Item label="schema">
                  {identityReadyDecisionCandidateState.candidate.schema}
                </Descriptions.Item>
                <Descriptions.Item label="mode">
                  {identityReadyDecisionCandidateState.candidate.mode}
                </Descriptions.Item>
                <Descriptions.Item label="decision_type">
                  {identityReadyDecisionCandidateState.candidate.decision_type}
                </Descriptions.Item>
                <Descriptions.Item label="sample_handle">
                  {identityReadyDecisionCandidateState.candidate.sample_handle}
                </Descriptions.Item>
                <Descriptions.Item label="review_subject_binding_safe_hash">
                  {
                    identityReadyDecisionCandidateState.candidate
                      .review_subject_binding_safe_hash
                  }
                </Descriptions.Item>
              </Descriptions>
              <Space wrap>
                <Tag color="cyan">candidate_only = true</Tag>
                <Tag color="default">persisted = false</Tag>
                <Tag color="default">trust_upgraded = false</Tag>
                <Tag color="default">production_object = false</Tag>
                <Tag color="cyan">human_review_required = true</Tag>
                <Tag color="cyan">no_automatic_trust_upgrade = true</Tag>
              </Space>
              <Paragraph type="secondary">
                The local candidate remains nonpersistent until a second explicit action requests one
                append-only nonproduction auditable decision record.
              </Paragraph>
              <Button
                type="primary"
                onClick={handleIdentityReadyDecisionPersistenceConfirmation}
                disabled={identityReadyDecisionPersistencePostStarted.current}
                loading={identityReadyDecisionPersistenceState.phase === 'posting'}
              >
                Record auditable nonproduction decision
              </Button>
              {identityReadyDecisionPersistenceState.phase === 'bounded_unavailable' && (
                <Alert
                  showIcon
                  type="warning"
                  message="Auditable decision request unavailable"
                  description="The bounded request was not accepted. No retry, candidate mutation, analysis, or report action was performed."
                />
              )}
              {identityReadyDecisionPersistenceState.phase === 'bounded_error' && (
                <Alert
                  showIcon
                  type="error"
                  message="Auditable decision request failed closed"
                  description="Only a bounded frontend state is shown. The local candidate remains unchanged and no raw backend error is exposed."
                />
              )}
              {identityReadyDecisionPersistenceState.phase === 'bounded_success' && (
                <Descriptions column={1} size="small" title="Bounded auditable decision receipt">
                  <Descriptions.Item label="request_status">
                    {identityReadyDecisionPersistenceState.result.request_status}
                  </Descriptions.Item>
                  <Descriptions.Item label="decision_id">
                    {identityReadyDecisionPersistenceState.result.decision_id}
                  </Descriptions.Item>
                  <Descriptions.Item label="audit_receipt_reference">
                    {identityReadyDecisionPersistenceState.result.audit_receipt_reference}
                  </Descriptions.Item>
                  <Descriptions.Item label="decision_status">
                    {identityReadyDecisionPersistenceState.result.decision_status}
                  </Descriptions.Item>
                  <Descriptions.Item label="outcome">
                    {identityReadyDecisionPersistenceState.result.outcome}
                  </Descriptions.Item>
                  <Descriptions.Item label="decision_ledger_write_performed">
                    {String(
                      identityReadyDecisionPersistenceState.result
                        .decision_ledger_write_performed,
                    )}
                  </Descriptions.Item>
                  <Descriptions.Item label="production_object_enabled">
                    {String(
                      identityReadyDecisionPersistenceState.result.production_object_enabled,
                    )}
                  </Descriptions.Item>
                  <Descriptions.Item label="analysis_triggered">
                    {String(identityReadyDecisionPersistenceState.result.analysis_triggered)}
                  </Descriptions.Item>
                  <Descriptions.Item label="report_triggered">
                    {String(identityReadyDecisionPersistenceState.result.report_triggered)}
                  </Descriptions.Item>
                </Descriptions>
              )}
            </>
          )}
        </Card>

        <Card className="panel-card internal-alpha-review-card">
          <Space wrap>
            <Tag color="cyan">metadata_only = true</Tag>
            <Tag color="cyan">review_only = true</Tag>
            <Tag color="cyan">human_review_required = true</Tag>
            <Tag color="cyan">candidate_persistence = in_memory_only</Tag>
            <Tag color="default">
              review_decision_write ={' '}
              {identityReadyDecisionPersistenceState.phase === 'bounded_success'
                ? String(
                    identityReadyDecisionPersistenceState.result
                      .decision_ledger_write_performed,
                  )
                : 'false'}
            </Tag>
            <Tag color="default">analysis_result_created = false</Tag>
            <Tag color="default">public_output_enabled = false</Tag>
            <Tag color="default">export_delivery_enabled = false</Tag>
          </Space>
        </Card>
      </div>
    )
  }

  if (selectedReviewView === LOCAL_EXCHANGE_PROJECTION_REVIEW_VIEW) {
    const localExchangeProjectionState =
      localExchangeProjectionStateByHandle[selectedLocalExchangeSampleHandle] ??
      INITIAL_LOCAL_EXCHANGE_PROJECTION_STATE
    const localProjection = localExchangeProjectionState.projection
    const localWarnings = localProjection?.warnings ?? []
    const localBlockers = localProjection?.blockers ?? []

    return (
      <div className="page-stack internal-alpha-review-shell-page">
        {reviewSurfaceSelector}

        <Card className="panel-card internal-alpha-review-card">
          <Space wrap align="center">
            <Text strong>Read-only local-exchange sample</Text>
            <Select
              aria-label="Read-only local-exchange sample"
              value={selectedLocalExchangeSampleHandle ?? undefined}
              options={localExchangeSampleOptions}
              onChange={setSelectedLocalExchangeSampleHandle}
              disabled={catalogPhase !== 'loaded'}
              placeholder="Sample catalog unavailable"
              notFoundContent="No enabled samples available"
              style={{ minWidth: 280 }}
            />
            <Text type="secondary">
              Selected sample handle = {selectedLocalExchangeSampleHandle ?? 'not available'}. Selection is read-only
              and cached for this page mount.
            </Text>
          </Space>
        </Card>

        {catalogPhase !== 'loaded' && (
          <Alert
            showIcon
            type={catalogPhase === 'loading' ? 'info' : 'warning'}
            message={catalogPhase === 'loading' ? 'Loading sample catalog' : 'Sample catalog unavailable'}
            description="No local-exchange projection request is made until a valid backend catalog is loaded."
          />
        )}

        <section className="internal-alpha-review-hero">
          <div>
            <Space wrap>
              <Tag color="cyan">internal alpha</Tag>
              <Tag color="cyan">B05 local-exchange projection</Tag>
              <Tag color="default">read-only</Tag>
              <Tag color="default">human review required</Tag>
            </Space>
            <Title level={1}>Local-exchange projection review</Title>
            <Paragraph>
              A separately selected, bounded B03 projection view. It is not the governed-record review surface and
              exposes no mutation authority.
            </Paragraph>
            <Alert
              className="internal-alpha-review-boundary-alert"
              showIcon
              type="info"
              message="B05 read-only boundary"
              description={
                <Space direction="vertical" size={2}>
                  <Text>Real metadata compatibility demonstrated for one approved sample.</Text>
                  <Text>Read-only and human-review-only.</Text>
                  <Text>Not a persisted governed record.</Text>
                  <Text>Not trust approval.</Text>
                  <Text>Not production readiness.</Text>
                  <Text>Not full-web or full-platform coverage.</Text>
                </Space>
              }
            />
          </div>

          <Card className="panel-card internal-alpha-review-status-card">
            <Space direction="vertical" size={12} className="full-width">
              <Text type="secondary">Request phase</Text>
              <Title level={2}>{localExchangeProjectionState.requestPhase}</Title>
              <Text>
                projection phase = {localExchangeProjectionState.projectionPhase ?? 'not available'}
              </Text>
              <Text>error code = {localExchangeProjectionState.errorCode ?? 'none'}</Text>
              <BooleanTag label="human_review_required" value={localProjection?.human_review_required ?? true} />
              <BooleanTag
                label="no_automatic_trust_upgrade"
                value={localProjection?.no_automatic_trust_upgrade ?? true}
              />
            </Space>
          </Card>
        </section>

        <Row gutter={[16, 16]}>
          <Col xs={24} lg={12}>
            <SummaryCard icon={<Eye size={18} />} title="Bounded projection status">
              <Descriptions column={1} size="small">
                <Descriptions.Item label="projection_status">
                  {localProjection?.projection_status ?? 'not loaded'}
                </Descriptions.Item>
                <Descriptions.Item label="reader_status">
                  {localProjection?.reader_status ?? 'not available'}
                </Descriptions.Item>
                <Descriptions.Item label="adapter_status">
                  {localProjection?.adapter_status ?? 'not available'}
                </Descriptions.Item>
                <Descriptions.Item label="provider_result_status">
                  {localProjection?.provider_result_status ?? 'not available'}
                </Descriptions.Item>
                <Descriptions.Item label="package_resolution_status">
                  {localProjection?.package_resolution_status ?? 'not available'}
                </Descriptions.Item>
                <Descriptions.Item label="candidate_count">
                  {localProjection?.candidate_count ?? 0}
                </Descriptions.Item>
                <Descriptions.Item label="review_status">
                  {localProjection?.review_status ?? 'not available'}
                </Descriptions.Item>
                <Descriptions.Item label="promotion_status">
                  {localProjection?.promotion_status ?? 'not available'}
                </Descriptions.Item>
                <Descriptions.Item label="staging_status">
                  {localProjection?.staging_status ?? 'not available'}
                </Descriptions.Item>
              </Descriptions>
            </SummaryCard>
          </Col>

          <Col xs={24} lg={12}>
            <SummaryCard icon={<Lock size={18} />} title="Warnings and blockers">
              <Text strong>Warnings</Text>
              <List
                size="small"
                dataSource={localWarnings}
                locale={{ emptyText: 'none' }}
                renderItem={(item) => (
                  <List.Item>
                    <Text>{item}</Text>
                  </List.Item>
                )}
              />
              <Text strong>Blockers</Text>
              <List
                size="small"
                dataSource={localBlockers}
                locale={{ emptyText: 'none' }}
                renderItem={(item) => (
                  <List.Item>
                    <Text>{item}</Text>
                  </List.Item>
                )}
              />
            </SummaryCard>
          </Col>
        </Row>

        <Card className="panel-card internal-alpha-review-card">
          <Space wrap>
            <Tag color="cyan">metadata_only = true</Tag>
            <Tag color="cyan">review_only = true</Tag>
            <Tag color="default">persistent_staging_write = false</Tag>
            <Tag color="default">review_decision_write = false</Tag>
            <Tag color="default">production_ready = false</Tag>
            <Tag color="default">public_output_enabled = false</Tag>
          </Space>
        </Card>
      </div>
    )
  }

  const projection = routeState.projection
  const allowedActions = projection?.allowed_actions ?? fixture.allowed_actions
  const blockedActions = projection?.blocked_actions ?? fixture.blocked_actions
  const sourceBoundary = projection?.source_chain_boundary ?? fixture.source_chain_boundary
  const humanReviewRequired = projection?.human_review_required ?? fixture.human_review_required
  const noAutomaticTrustUpgrade =
    projection?.no_automatic_trust_upgrade ?? fixture.no_automatic_trust_upgrade

  return (
    <div className="page-stack internal-alpha-review-shell-page">
      {reviewSurfaceSelector}

      <Card className="panel-card internal-alpha-review-card">
        <Space direction="vertical" size={12} className="full-width">
          <Title level={4}>Formal decision state (read-only)</Title>
          <Paragraph>
            This separate, bounded projection may restore the established formal human-review state after reload.
            It performs no write, creates no POST authority, and never exposes a decision identifier or raw ledger
            row.
          </Paragraph>
          {governedFormalStateRequestState.phase === 'loading' && (
            <Text type="secondary">Loading bounded formal state</Text>
          )}
          {governedFormalStateRequestState.phase === 'bounded_error' && (
            <Alert
              showIcon
              type="warning"
              message="Formal decision state failed closed"
              description="Only a bounded frontend state is shown. No raw backend error or ledger identity is exposed."
            />
          )}
          {governedFormalStateRequestState.phase === 'bounded_result' && (
            <Descriptions column={1} size="small" title="Bounded formal-state projection">
              <Descriptions.Item label="projection_status">
                {governedFormalStateRequestState.result.projection_status}
              </Descriptions.Item>
              <Descriptions.Item label="projection_error_code">
                {governedFormalStateRequestState.result.projection_error_code ?? 'none'}
              </Descriptions.Item>
              <Descriptions.Item label="formal_decision_count">
                {governedFormalStateRequestState.result.formal_decision_count}
              </Descriptions.Item>
              <Descriptions.Item label="formal_first_decision_present">
                {String(governedFormalStateRequestState.result.formal_first_decision_present)}
              </Descriptions.Item>
              <Descriptions.Item label="formal_second_decision_present">
                {String(governedFormalStateRequestState.result.formal_second_decision_present)}
              </Descriptions.Item>
              <Descriptions.Item label="formal_second_decision_type">
                {governedFormalStateRequestState.result.formal_second_decision_type ?? 'none'}
              </Descriptions.Item>
              <Descriptions.Item label="human_review_required">
                {String(governedFormalStateRequestState.result.human_review_required)}
              </Descriptions.Item>
              <Descriptions.Item label="no_automatic_trust_upgrade">
                {String(governedFormalStateRequestState.result.no_automatic_trust_upgrade)}
              </Descriptions.Item>
            </Descriptions>
          )}
        </Space>
      </Card>

      <Card className="panel-card internal-alpha-review-card">
        <Space direction="vertical" size={12} className="full-width">
          <Title level={4}>Governed human-review decision</Title>
          <Paragraph>
            This internal, nonproduction control targets an append-only human-review decision ledger. It does not
            approve trust, upgrade trust automatically, mutate the governed evidence record, or start analysis or
            report generation. It creates no production, public, export, or delivery output. The backend decision
            route is disabled by default and requires separate runtime authorization before real use.
          </Paragraph>
          <Space wrap align="center">
            <Select
              aria-label="Governed human-review decision type"
              value={selectedGovernedDecisionType ?? undefined}
              options={GOVERNED_REVIEW_DECISION_OPTIONS}
              onChange={handleGovernedDecisionSelection}
              disabled={
                !governedDecisionSurfaceReady ||
                governedDecisionPostAttemptStarted.current
              }
              placeholder="Select one governed decision"
              style={{ minWidth: 360 }}
            />
            <Button
              type="primary"
              onClick={handleGovernedDecisionConfirmation}
              disabled={
                !selectedGovernedDecisionIsAllowed ||
                governedDecisionPostAttemptStarted.current
              }
              loading={governedDecisionRequestState.phase === 'posting'}
            >
              Confirm governed decision
            </Button>
          </Space>
          <Text type="secondary">
            Select one server-allowed decision, then confirm explicitly. A page mount permits at most one POST
            attempt and never retries or performs a GET-after-POST verification.
          </Text>
          {!governedDecisionSurfaceReady && (
            <Alert
              showIcon
              type="info"
              message="Governed decision control unavailable"
              description="The control remains inactive unless the governed-record projection is ready and all human-review safety invariants hold."
            />
          )}
          {governedDecisionRequestState.phase === 'bounded_unavailable' && (
            <Alert
              showIcon
              type="warning"
              message="Governed decision request unavailable"
              description="The bounded request was not accepted. No automatic retry or follow-up request was made."
            />
          )}
          {governedDecisionRequestState.phase === 'bounded_error' && (
            <Alert
              showIcon
              type="warning"
              message="Governed decision request failed closed"
              description="Only a bounded frontend state is shown. No raw backend error or receipt is exposed."
            />
          )}
          {governedDecisionRequestState.phase === 'bounded_success' && (
            <Descriptions column={1} size="small" title="Bounded decision result">
              <Descriptions.Item label="request_status">
                {governedDecisionRequestState.result.request_status}
              </Descriptions.Item>
              <Descriptions.Item label="decision_id">
                {governedDecisionRequestState.result.decision_id}
              </Descriptions.Item>
              <Descriptions.Item label="decision_type">
                {governedDecisionRequestState.result.decision_type}
              </Descriptions.Item>
              <Descriptions.Item label="decision_status">
                {governedDecisionRequestState.result.decision_status}
              </Descriptions.Item>
              <Descriptions.Item label="outcome">
                {governedDecisionRequestState.result.outcome}
              </Descriptions.Item>
              <Descriptions.Item label="decision_ledger_write_performed">
                {String(governedDecisionRequestState.result.decision_ledger_write_performed)}
              </Descriptions.Item>
              <Descriptions.Item label="human_review_required">
                {String(governedDecisionRequestState.result.human_review_required)}
              </Descriptions.Item>
              <Descriptions.Item label="no_automatic_trust_upgrade">
                {String(governedDecisionRequestState.result.no_automatic_trust_upgrade)}
              </Descriptions.Item>
              <Descriptions.Item label="production_ready">
                {String(governedDecisionRequestState.result.production_ready)}
              </Descriptions.Item>
            </Descriptions>
          )}
        </Space>
      </Card>

      <section className="internal-alpha-review-hero">
        <div>
          <Space wrap>
            <Tag color="cyan">internal alpha</Tag>
            <Tag color="cyan">governed nonproduction only</Tag>
            <Tag color="default">read-only route smoke</Tag>
            <Tag color="default">static fallback preserved</Tag>
            <Tag color="default">not operator runtime</Tag>
          </Space>
          <Title level={1}>Internal Alpha Review Console static preview</Title>
          <Paragraph>
            This static internal frontend shell presents bounded governance metadata for pending human review. It
            preserves the selected sample / no-write / no-production boundary and the safe static fallback when
            either backend gate is disabled or the backend is unavailable; this shell is not operator runtime.
          </Paragraph>
          <Alert
            className="internal-alpha-review-boundary-alert"
            showIcon
            type="info"
            message={
              projection
                ? 'source_chain_boundary = ' + sourceBoundary
                : STATIC_SOURCE_CHAIN_BOUNDARY_LABEL
            }
            description={
              'route_backend_connection = ' +
              routeState.routeBackendConnection +
              '; ' +
              routeState.description
            }
          />
        </div>
        <Card className="panel-card internal-alpha-review-status-card">
          <Space direction="vertical" size={12} className="full-width">
            <Text type="secondary">Shell status</Text>
            <Title level={2}>{routeState.status}</Title>
            <Text>{routeState.statusLabel}</Text>
            <Text>pending human review</Text>
            <Text>no automatic trust upgrade</Text>
            <Text>human_review_required = true</Text>
            <Text>no_automatic_trust_upgrade = true</Text>
            <Text>no Review Queue or operator runtime</Text>
            <Text>no production or public readiness</Text>
            <BooleanTag label="human_review_required" value={humanReviewRequired} />
            <BooleanTag label="no_automatic_trust_upgrade" value={noAutomaticTrustUpgrade} />
          </Space>
        </Card>
      </section>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={8}>
          <SummaryCard icon={<ShieldCheck size={18} />} title="Boundary flags">
            <Space wrap>
              <Tag color="cyan">no actual write</Tag>
              <Tag color="cyan">no production object</Tag>
              <Tag color="cyan">no Review Queue runtime</Tag>
              <Tag color="cyan">no Source 11 / FinalSummaryReport runtime</Tag>
            </Space>
            <Paragraph>{fixture.source_count_summary.note}</Paragraph>
          </SummaryCard>
        </Col>
        <Col xs={24} lg={8}>
          <SummaryCard icon={<TriangleAlert size={18} />} title="Governed counts">
            <Descriptions column={1} size="small">
              <Descriptions.Item label="record_count_class">
                {projection?.record_count_class ?? 'not available in static fallback'}
              </Descriptions.Item>
              <Descriptions.Item label="reservation_count_class">
                {projection?.reservation_count_class ?? 'not available in static fallback'}
              </Descriptions.Item>
              <Descriptions.Item label="blocker_count">
                {projection?.blockers?.length ?? fixture.blocker_count}
              </Descriptions.Item>
            </Descriptions>
          </SummaryCard>
        </Col>
        <Col xs={24} lg={8}>
          <SummaryCard icon={<Lock size={18} />} title="Backend connection">
            <Tag color={routeState.tagColor}>{routeState.routeBackendConnection}</Tag>
            <Paragraph>{routeState.detail}</Paragraph>
            <Paragraph>
              Safe projection id: {SAFE_REVIEW_CONSOLE_PROJECTION_ID}. Allowlisted projection count:{' '}
              {REVIEW_CONSOLE_PROJECTION_ALLOWLIST.length}. The page calls no platform service, collector,
              provider, model, or write path. Legacy synthetic selection reference:{' '}
              {LEGACY_SYNTHETIC_SELECTION_REFERENCE}.
            </Paragraph>
          </SummaryCard>
        </Col>
      </Row>

      <Card className="panel-card internal-alpha-review-card">
        <Space direction="vertical" size={12} className="full-width">
          <Title level={4}>Approved opaque metadata only</Title>
          <Paragraph>
            Only the eight P1-approved opaque identifiers, hashes, and digests may appear here. Non-ready and
            fallback states display no values.
          </Paragraph>
          <Descriptions column={{ xs: 1, lg: 2 }} size="small">
            {SAFE_METADATA_FIELDS.map((field) => (
              <Descriptions.Item key={field} label={field}>
                <Text code>{displaySafeValue(projection?.[field])}</Text>
              </Descriptions.Item>
            ))}
          </Descriptions>
        </Space>
      </Card>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <SummaryCard icon={<Eye size={18} />} title="Allowed actions labels only">
            <List
              size="small"
              dataSource={allowedActions}
              renderItem={(item) => (
                <List.Item>
                  <Text>{item}</Text>
                </List.Item>
              )}
            />
          </SummaryCard>
        </Col>
        <Col xs={24} lg={12}>
          <SummaryCard icon={<Lock size={18} />} title="Blocked actions labels only">
            <List
              size="small"
              dataSource={blockedActions}
              renderItem={(item) => (
                <List.Item>
                  <Text>{item}</Text>
                </List.Item>
              )}
            />
          </SummaryCard>
        </Col>
      </Row>

      <Card className="panel-card internal-alpha-review-card">
        <Space direction="vertical" size={12} className="full-width">
          <Title level={4}>Coverage and validation summaries</Title>
          <Space wrap>
            {fixture.coverage_note_summary.map((item) => (
              <Tag key={item} color="default">
                {item}
              </Tag>
            ))}
          </Space>
          <List
            size="small"
            dataSource={fixture.validation_summary}
            renderItem={(item) => (
              <List.Item>
                <Text>{item}</Text>
              </List.Item>
            )}
          />
        </Space>
      </Card>
    </div>
  )
}
