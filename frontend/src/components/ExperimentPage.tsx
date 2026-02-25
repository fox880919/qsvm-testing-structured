import { useState, useEffect, useRef, useLayoutEffect } from 'react'
import { useSiteCopy } from '../SiteCopyContext'
import { EditableText } from './EditableText'
import { ExperimentPipelineVisualization } from './ExperimentPipelineVisualization'

const API_BASE = import.meta.env.VITE_API_URL || ''

/** Collapse consecutive "Computed row X/Y" progress lines into the latest one (terminal-style). */
function collapseProgressLines(lines: string[]): string[] {
  const progressRe = /^Computed row \d+\/\d+/
  const out: string[] = []
  for (const line of lines) {
    if (progressRe.test(line)) {
      if (out.length > 0 && progressRe.test(out[out.length - 1])) {
        out[out.length - 1] = line
      } else {
        out.push(line)
      }
    } else {
      out.push(line)
    }
  }
  return out
}

interface StatusResponse {
  status: string
  phase: string
  phase_detail: string
  log: string[]
  returncode: number | null
  step1_exists: boolean
  step2_exists: boolean
}

const cardStyle = {
  background: 'white',
  color: '#333',
  borderRadius: 12,
  boxShadow: '0 10px 40px rgba(0,0,0,0.12)',
  padding: '1.5rem 2rem',
  marginBottom: '1.5rem',
}

const titleStyle = {
  fontSize: '1.25rem',
  fontWeight: 700,
  marginBottom: '1rem',
  paddingBottom: '0.5rem',
  borderBottom: '2px solid #c41230',
}

const btnStyle = {
  padding: '0.75rem 1.5rem',
  borderRadius: 8,
  background: '#c41230',
  color: 'white',
  fontWeight: 700,
  border: 'none',
  cursor: 'pointer',
}

function QSVMVisualization({ dataset, disabled }: { dataset: number; disabled: boolean }) {
  const { siteCopy } = useSiteCopy()
  const [vizType, setVizType] = useState<0 | 1>(0)
  const [image, setImage] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchViz = async (featureMapType: 0 | 1) => {
    if (dataset !== 0) {
      setError(siteCopy.experiment.vizOnlyWine)
      return
    }
    setLoading(true)
    setError(null)
    setImage(null)
    try {
      const res = await fetch(`${API_BASE}/api/visualization`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dataset: 0, feature_map_type: featureMapType }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Failed to generate visualization')
      setImage(data.image)
      setVizType(featureMapType)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        <button
          onClick={() => fetchViz(0)}
          disabled={disabled || loading}
          style={{
            ...btnStyle,
            opacity: (disabled || loading) ? 0.7 : 1,
            background: vizType === 0 && image ? '#16a34a' : '#c41230',
          }}
        >
          {loading ? siteCopy.experiment.vizGenerating : <EditableText path="experiment.vizAmplitude" />}
        </button>
        <button
          onClick={() => fetchViz(1)}
          disabled={disabled || loading}
          style={{
            ...btnStyle,
            opacity: (disabled || loading) ? 0.7 : 1,
            background: vizType === 1 && image ? '#16a34a' : '#c41230',
          }}
        >
          {loading ? siteCopy.experiment.vizGenerating : <EditableText path="experiment.vizAngle" />}
        </button>
      </div>
      {error && (
        <div style={{ padding: '0.75rem', borderRadius: 8, background: 'rgba(127,29,29,0.2)', color: '#b91c1c' }}>
          {error}
        </div>
      )}
      {image && (
        <div style={{ borderRadius: 8, overflow: 'hidden', border: '2px solid #e5e7eb' }}>
          <img
            src={`data:image/png;base64,${image}`}
            alt={siteCopy.experiment.vizAlt}
            style={{ width: '100%', maxWidth: 560, height: 'auto', display: 'block' }}
          />
        </div>
      )}
      {dataset !== 0 && (
        <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
          <EditableText path="experiment.vizSwitchWine" />
        </p>
      )}
    </div>
  )
}

export function ExperimentPage() {
  const { siteCopy } = useSiteCopy()
  const DATASET_OPTIONS = siteCopy.experiment.datasetOptions as Record<number, string>
  const EXPERIMENT_OPTIONS = siteCopy.experiment.experimentOptions as Record<string, string>
  const PHASES = siteCopy.experiment.phases

  const [dataset, setDataset] = useState<number>(0)
  const [kfold, setKfold] = useState(5)
  const [experiment, setExperiment] = useState<string>('all')
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState<StatusResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null)
  const logEndRef = useRef<HTMLSpanElement>(null)

  useLayoutEffect(() => {
    if (status?.log?.length && (loading || status?.status === 'running')) {
      logEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
    }
  }, [status?.log?.length, loading, status?.status])

  const stopPolling = () => {
    if (pollRef.current) {
      clearInterval(pollRef.current)
      pollRef.current = null
    }
  }

  const pollStatus = () => {
    fetch(`${API_BASE}/api/status`)
      .then((r) => r.json())
      .then((data: StatusResponse) => {
        setStatus(data)
        if (data.status === 'completed' || data.status === 'failed' || data.status === 'cancelled') {
          stopPolling()
          setLoading(false)
        }
      })
      .catch(() => stopPolling())
  }

  const handleCancel = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/cancel`, { method: 'POST' })
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        setError(err.detail || 'Failed to cancel')
      }
    } catch {
      setError('Network error')
    }
  }

  const handleRun = async () => {
    setLoading(true)
    setStatus(null)
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/api/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dataset, kfold, experiment }),
      })
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.detail || 'Failed to start tests')
      }
      setStatus({
        status: 'running',
        phase: 'config',
        phase_detail: `Dataset: ${DATASET_OPTIONS[dataset]}, K-fold: ${kfold}, ${EXPERIMENT_OPTIONS[experiment]}`,
        log: [],
        returncode: null,
        step1_exists: false,
        step2_exists: false,
      })
      pollRef.current = setInterval(pollStatus, 500)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Network error')
      setLoading(false)
    }
  }

  useEffect(() => () => stopPolling(), [])

  const downloadStep1 = () => window.open(`${API_BASE}/api/results/step1`, '_blank')
  const downloadStep2 = () => window.open(`${API_BASE}/api/results/step2`, '_blank')

  const getPhaseStatus = (phaseId: string): 'pending' | 'active' | 'done' | 'cancelled' => {
    if (!status) return 'pending'
    const order = ['config', 'step1', 'step2', 'step3', 'done']
    const currentIdx = order.indexOf(status.phase)
    const phaseIdx = order.indexOf(phaseId)
    if (status.status === 'cancelled') {
      if (phaseIdx < currentIdx) return 'done'
      if (phaseIdx === currentIdx) return 'cancelled'
      return 'pending'
    }
    if (phaseIdx < currentIdx) return 'done'
    if (phaseIdx === currentIdx) return status.status === 'running' ? 'active' : 'done'
    return 'pending'
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <section style={cardStyle}>
        <h2 style={titleStyle}><EditableText path="experiment.configTitle" /></h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 600, marginBottom: '0.5rem' }}><EditableText path="experiment.datasetLabel" /></label>
            <select
              value={dataset}
              onChange={(e) => setDataset(Number(e.target.value))}
              style={{ width: '100%', padding: '0.5rem 1rem', borderRadius: 8, border: '2px solid #ddd', fontSize: '1rem' }}
            >
              {Object.entries(DATASET_OPTIONS).map(([val, label]) => (
                <option key={val} value={val}>{label}</option>
              ))}
            </select>
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 600, marginBottom: '0.5rem' }}><EditableText path="experiment.runLabel" /></label>
            <select
              value={experiment}
              onChange={(e) => setExperiment(e.target.value)}
              style={{ width: '100%', padding: '0.5rem 1rem', borderRadius: 8, border: '2px solid #ddd', fontSize: '1rem' }}
            >
              {Object.entries(EXPERIMENT_OPTIONS).map(([val, label]) => (
                <option key={val} value={val}>{label}</option>
              ))}
            </select>
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 600, marginBottom: '0.5rem' }}><EditableText path="experiment.kfoldLabel" />: {kfold}</label>
            <input
              type="range"
              min={2}
              max={20}
              value={kfold}
              onChange={(e) => setKfold(Number(e.target.value))}
              style={{ width: '100%', accentColor: '#c41230' }}
            />
          </div>
        </div>
        <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem', flexWrap: 'wrap' }}>
          <button
            onClick={handleRun}
            disabled={loading}
            style={{
              ...btnStyle,
              flex: 1,
              minWidth: 140,
              opacity: loading ? 0.7 : 1,
              cursor: loading ? 'not-allowed' : 'pointer',
            }}
          >
            {loading ? <EditableText path="experiment.runningButton" /> : <EditableText path="experiment.runButton" />}
          </button>
          {loading && (
            <button
              onClick={handleCancel}
              style={{
                ...btnStyle,
                background: '#6b7280',
                minWidth: 140,
              }}
            >
              <EditableText path="experiment.cancelButton" />
            </button>
          )}
        </div>
      </section>

      {/* Live Progress - first thing users see when running */}
      {(loading || status) && (
        <section style={{
          ...cardStyle,
          ...(loading || status?.status === 'running'
            ? { border: '2px solid #c41230', boxShadow: '0 0 0 4px rgba(196,18,48,0.15)' }
            : {}),
        }}>
          <h2 style={titleStyle}>
            {loading || status?.status === 'running' ? (
              <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#c41230' }} />
                <EditableText path="experiment.liveProgressTitle" />
              </span>
            ) : (
              <EditableText path="experiment.runOutputTitle" />
            )}
          </h2>
          {(loading || status?.status === 'running') && status?.phase_detail && (
            <div style={{
              marginBottom: '1rem',
              padding: '0.75rem 1rem',
              background: 'rgba(196,18,48,0.08)',
              borderRadius: 8,
              borderLeft: '4px solid #c41230',
              fontWeight: 600,
              color: '#c41230',
            }}>
              {status.phase_detail}
            </div>
          )}
          <pre
            style={{
              padding: '1rem',
              background: '#111827',
              color: '#4ade80',
              fontSize: '0.8rem',
              lineHeight: 1.5,
              borderRadius: 8,
              overflow: 'auto',
              maxHeight: loading || status?.status === 'running' ? 400 : 320,
              fontFamily: 'monospace',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word',
            }}
          >
            {status?.log?.length ? collapseProgressLines(status.log).join('\n') : (loading ? siteCopy.experiment.starting : '')}
            <span ref={logEndRef} />
          </pre>
        </section>
      )}

      {(loading || status) && (
        <section style={cardStyle}>
          <h2 style={titleStyle}><EditableText path="experiment.pipelineTitle" /></h2>
          <p style={{ marginBottom: '1rem', fontSize: '0.875rem', color: '#6b7280' }}>
            <EditableText path="experiment.pipelineDesc" />
          </p>
          <ExperimentPipelineVisualization dataset={dataset} />
        </section>
      )}

      {(loading || status) && (
        <section style={cardStyle}>
          <h2 style={titleStyle}><EditableText path="experiment.vizTitle" /></h2>
          <p style={{ marginBottom: '1rem', fontSize: '0.875rem', color: '#6b7280' }}>
            <EditableText path="experiment.vizDesc" />
          </p>
          <QSVMVisualization dataset={dataset} disabled={loading} />
        </section>
      )}

      {(loading || status) && (
        <section style={cardStyle}>
          <h2 style={titleStyle}><EditableText path="experiment.phasesTitle" /></h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {PHASES.map((p, i) => {
              const phaseStatus = getPhaseStatus(p.id)
              const phaseBoxStyle: React.CSSProperties = {
                padding: '1rem',
                borderRadius: 8,
                border: '2px solid',
                ...(phaseStatus === 'active'
                  ? { borderColor: '#c41230', background: 'rgba(196,18,48,0.08)' }
                  : phaseStatus === 'done'
                    ? { borderColor: '#16a34a', background: '#f0fdf4' }
                    : phaseStatus === 'cancelled'
                      ? { borderColor: '#6b7280', background: '#f3f4f6' }
                      : { borderColor: '#e5e7eb', background: '#f9fafb' }),
              }
              return (
                <div key={p.id} style={phaseBoxStyle}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <span
                      style={{
                        width: 32,
                        height: 32,
                        borderRadius: '50%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '0.875rem',
                        fontWeight: 700,
                        ...(phaseStatus === 'done'
                          ? { background: '#16a34a', color: 'white' }
                          : phaseStatus === 'active'
                            ? { background: '#c41230', color: 'white' }
                            : phaseStatus === 'cancelled'
                              ? { background: '#6b7280', color: 'white' }
                              : { background: '#e5e7eb', color: '#6b7280' }),
                      }}
                    >
                      {phaseStatus === 'done' ? '✓' : phaseStatus === 'active' ? '...' : phaseStatus === 'cancelled' ? '✕' : '—'}
                    </span>
                    <h3 style={{ fontWeight: 700, margin: 0 }}><EditableText path={`experiment.phases.${i}.title`} /></h3>
                  </div>
                  <p style={{ margin: '0.5rem 0 0 2.75rem', fontSize: '0.875rem', color: '#6b7280', lineHeight: 1.5 }}><EditableText path={`experiment.phases.${i}.description`} /></p>
                  {status?.phase === p.id && status.phase_detail && (
                    <p style={{ margin: '0.5rem 0 0 2.75rem', fontSize: '0.875rem', color: '#c41230', fontWeight: 500 }}>{status.phase_detail}</p>
                  )}
                </div>
              )
            })}
          </div>
        </section>
      )}

      {error && (
        <div style={{ padding: '1rem', borderRadius: 8, background: 'rgba(127,29,29,0.9)', color: 'white' }}>{error}</div>
      )}

      {status?.status === 'completed' && (
        <section style={cardStyle}>
          <h2 style={titleStyle}><EditableText path="experiment.resultsTitle" /></h2>
          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
            <button
              onClick={downloadStep1}
              disabled={!status.step1_exists}
              style={{ ...btnStyle, opacity: status.step1_exists ? 1 : 0.5 }}
            >
              <EditableText path="experiment.downloadStep1" />
            </button>
            <button
              onClick={downloadStep2}
              disabled={!status.step2_exists}
              style={{ ...btnStyle, opacity: status.step2_exists ? 1 : 0.5 }}
            >
              <EditableText path="experiment.downloadStep2" />
            </button>
          </div>
        </section>
      )}

      {status?.status === 'cancelled' && (
        <div style={{ padding: '1rem', borderRadius: 8, background: 'rgba(107,114,128,0.9)', color: 'white' }}>
          <EditableText path="experiment.runCancelled" />
        </div>
      )}

      {status?.status === 'failed' && (
        <div style={{ padding: '1rem', borderRadius: 8, background: 'rgba(146,64,14,0.9)', color: 'white' }}>
          <EditableText path="experiment.runFailed" />
        </div>
      )}

    </div>
  )
}
