import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { useSiteCopy } from '../SiteCopyContext'
import { EditableText } from './EditableText'

const API_BASE = import.meta.env.VITE_API_URL || ''

const cardStyle = {
  background: 'white',
  color: '#333',
  borderRadius: 12,
  boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
  padding: '1.25rem',
  marginBottom: '1rem',
}

const titleStyle = {
  fontSize: '1rem',
  fontWeight: 700,
  marginBottom: '0.75rem',
  paddingBottom: '0.4rem',
  borderBottom: '2px solid #c41230',
}

interface PipelineSummary {
  dataset_name: string
  n_samples: number
  n_features_raw: number
  n_classes: number
  always_use_pca: boolean
  pca_components: number
  pca_applied: boolean
  n_features_after_pca: number
}

interface Step1Analysis {
  equivalent: number
  killed: number
  survived: number
  crashed: number
  total: number
  rows: Record<string, unknown>[]
}

interface Step2Analysis {
  modes: string[]
  defect_combos: string[]
  caught_rates: number[]
  rows: Record<string, unknown>[]
}

interface FiguresAvailable {
  experiment2_heatmap: boolean
  experiment2_pie: boolean
  experiment3_detection: boolean
  experiment3_heatmap: boolean
}

export function ExperimentPipelineVisualization({ dataset }: { dataset: number }) {
  const { siteCopy } = useSiteCopy()
  const [summary, setSummary] = useState<PipelineSummary | null>(null)
  const [circuitAmp, setCircuitAmp] = useState<string | null>(null)
  const [circuitAng, setCircuitAng] = useState<string | null>(null)
  const [step1, setStep1] = useState<Step1Analysis | null>(null)
  const [step2, setStep2] = useState<Step2Analysis | null>(null)
  const [figuresAvailable, setFiguresAvailable] = useState<FiguresAvailable | null>(null)
  const [generatingCharts, setGeneratingCharts] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refetchFigures = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/figures/available`)
      if (res.ok) setFiguresAvailable(await res.json())
    } catch {
      /* ignore */
    }
  }

  const handleGenerateCharts = async () => {
    setGeneratingCharts(true)
    try {
      const res = await fetch(`${API_BASE}/api/figures/generate`, { method: 'POST' })
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.detail || 'Chart generation failed')
      }
      await refetchFigures()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate charts')
    } finally {
      setGeneratingCharts(false)
    }
  }

  useEffect(() => {
    const fetchAll = async () => {
      setLoading(true)
      setError(null)
      try {
        const [sumRes, ampRes, angRes, s1Res, s2Res, figRes] = await Promise.all([
          fetch(`${API_BASE}/api/pipeline/summary?dataset=${dataset}`),
          fetch(`${API_BASE}/api/pipeline/circuits/0`),
          fetch(`${API_BASE}/api/pipeline/circuits/1`),
          fetch(`${API_BASE}/api/pipeline/step1`),
          fetch(`${API_BASE}/api/pipeline/step2`),
          fetch(`${API_BASE}/api/figures/available`),
        ])
        const sumData = await sumRes.json()
        const ampData = ampRes.ok ? await ampRes.json() : null
        const angData = angRes.ok ? await angRes.json() : null
        const s1Data = s1Res.ok ? await s1Res.json() : null
        const s2Data = s2Res.ok ? await s2Res.json() : null
        const figData = figRes.ok ? await figRes.json() : null

        setSummary(sumData)
        setCircuitAmp(ampData?.image ?? null)
        setCircuitAng(angData?.image ?? null)
        setStep1(s1Data)
        setStep2(s2Data)
        setFiguresAvailable(figData)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load pipeline')
      } finally {
        setLoading(false)
      }
    }
    fetchAll()
  }, [dataset])

  if (loading) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center', color: '#6b7280' }}>
        <EditableText path="pipeline.loadingPipeline" />
      </div>
    )
  }

  if (error) {
    return (
      <div style={{ padding: '1rem', borderRadius: 8, background: 'rgba(127,29,29,0.2)', color: '#b91c1c' }}>
        {error}
      </div>
    )
  }

  const mutationChartData = step1
    ? [
        { name: 'Equivalent', count: step1.equivalent, fill: '#16a34a' },
        { name: 'Killed', count: step1.killed, fill: '#c41230' },
        { name: 'Survived', count: step1.survived, fill: '#f59e0b' },
        { name: 'Crashed', count: step1.crashed, fill: '#6b7280' },
      ].filter((d) => d.count > 0)
    : []

  const exp1Style = { ...cardStyle, borderLeft: '4px solid #c41230' }
  const exp2Style = { ...cardStyle, borderLeft: '4px solid #2563eb' }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Pipeline overview */}
      <div style={cardStyle}>
        <h3 style={titleStyle}><EditableText path="pipeline.overviewTitle" /></h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
            <span style={{ ...exp1Badge, background: 'rgba(34,197,94,0.15)', color: '#16a34a' }}>
              Baseline
            </span>
            <span style={arrowStyle}>→</span>
            <span style={stepBadge}>Baseline</span>
            <span style={arrowStyle}>→</span>
            <span style={stepBadge}>MR1 (Scaling) + MR2 (Rotation)</span>
            <span style={arrowStyle}>→</span>
            <span style={stepBadge}>MTS=0 Check</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
            <span style={{ ...exp1Badge, background: 'rgba(196,18,48,0.15)', color: '#c41230' }}>
              Statistical Testing
            </span>
            <span style={arrowStyle}>→</span>
            <span style={stepBadge}>Data</span>
            <span style={arrowStyle}>→</span>
            <span style={stepBadge}>PCA</span>
            <span style={arrowStyle}>→</span>
            <span style={stepBadge}>Feature Map</span>
            <span style={arrowStyle}>→</span>
            <span style={stepBadge}>QSVM</span>
            <span style={arrowStyle}>→</span>
            <span style={stepBadge}>Statistical Testing (30 mutants, 12 MRs)</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
            <span style={{ ...exp1Badge, background: 'rgba(37,99,235,0.15)', color: '#2563eb' }}>
              Kernel Testing
            </span>
            <span style={arrowStyle}>→</span>
            <span style={stepBadge}>Golden Matrix</span>
            <span style={arrowStyle}>→</span>
            <span style={stepBadge}>Kernel Testing (14 MRs)</span>
          </div>
        </div>
        <div style={{ marginTop: '1rem', display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
          <button
            type="button"
            onClick={handleGenerateCharts}
            disabled={generatingCharts}
            style={{
              padding: '0.5rem 1rem',
              borderRadius: 8,
              background: generatingCharts ? '#9ca3af' : '#c41230',
              color: 'white',
              fontWeight: 600,
              border: 'none',
              cursor: generatingCharts ? 'not-allowed' : 'pointer',
              fontSize: '0.875rem',
            }}
          >
            {generatingCharts ? siteCopy.pipeline.generateFiguresRunning : <EditableText path="pipeline.generateFigures" />}
          </button>
          <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>
            <EditableText path="pipeline.runAfterHint" />
          </span>
        </div>
      </div>

      {/* ========== Baseline ========== */}
      <div style={{ borderTop: '2px solid #16a34a', paddingTop: '1rem', marginTop: '0.5rem' }}>
        <h2 style={{ ...titleStyle, fontSize: '1.1rem', color: '#16a34a', marginBottom: '1rem' }}>
          <EditableText path="pipeline.exp1Title" />
        </h2>
        <p style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '1rem' }}>
          <EditableText path="pipeline.exp1Desc" />
        </p>
        <div style={{ ...cardStyle, borderLeft: '4px solid #16a34a' }}>
          <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
            <EditableText path="pipeline.exp1NoFigures" />
          </p>
        </div>
      </div>

      {/* ========== Statistical Testing ========== */}
      <div style={{ borderTop: '2px solid #c41230', paddingTop: '1rem', marginTop: '0.5rem' }}>
        <h2 style={{ ...titleStyle, fontSize: '1.1rem', color: '#c41230', marginBottom: '1rem' }}>
          <EditableText path="pipeline.exp2Title" />
        </h2>
        <p style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '1rem' }}>
          <EditableText path="pipeline.exp2Desc" />
        </p>

      {/* Data extraction */}
      {summary && (
        <div style={exp1Style}>
          <h3 style={titleStyle}><EditableText path="pipeline.dataExtraction" /></h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '0.75rem' }}>
            <div>
              <span style={{ color: '#6b7280', fontSize: '0.75rem' }}><EditableText path="pipeline.dataset" /></span>
              <div style={{ fontWeight: 600 }}>{summary.dataset_name}</div>
            </div>
            <div>
              <span style={{ color: '#6b7280', fontSize: '0.75rem' }}><EditableText path="pipeline.samples" /></span>
              <div style={{ fontWeight: 600 }}>{summary.n_samples}</div>
            </div>
            <div>
              <span style={{ color: '#6b7280', fontSize: '0.75rem' }}><EditableText path="pipeline.featuresRaw" /></span>
              <div style={{ fontWeight: 600 }}>{summary.n_features_raw}</div>
            </div>
            <div>
              <span style={{ color: '#6b7280', fontSize: '0.75rem' }}><EditableText path="pipeline.classes" /></span>
              <div style={{ fontWeight: 600 }}>{summary.n_classes}</div>
            </div>
          </div>
        </div>
      )}

      {/* PCA */}
      {summary && (
        <div style={exp1Style}>
          <h3 style={titleStyle}><EditableText path="pipeline.pcaTitle" /></h3>
          {summary.pca_applied ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <div>Applied: <strong>Yes</strong> — {summary.pca_components} components</div>
              <div>Features after PCA: <strong>{summary.n_features_after_pca}</strong></div>
            </div>
          ) : (
            <div><EditableText path="pipeline.pcaNotApplied" /></div>
          )}
        </div>
      )}

      {/* Feature map circuits */}
      <div style={exp1Style}>
        <h3 style={titleStyle}><EditableText path="pipeline.featureMapTitle" /></h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
          {circuitAmp && (
            <div>
              <div style={{ fontWeight: 600, marginBottom: '0.5rem' }}><EditableText path="pipeline.amplitudeEmbedding" /></div>
              <img
                src={`data:image/png;base64,${circuitAmp}`}
                alt="Amplitude circuit"
                style={{ width: '100%', maxWidth: 320, borderRadius: 8, border: '1px solid #e5e7eb' }}
              />
            </div>
          )}
          {circuitAng && (
            <div>
              <div style={{ fontWeight: 600, marginBottom: '0.5rem' }}><EditableText path="pipeline.angleEmbedding" /></div>
              <img
                src={`data:image/png;base64,${circuitAng}`}
                alt="Angle circuit"
                style={{ width: '100%', maxWidth: 320, borderRadius: 8, border: '1px solid #e5e7eb' }}
              />
            </div>
          )}
        </div>
      </div>

      {/* Training & accuracy placeholder */}
      <div style={exp1Style}>
        <h3 style={titleStyle}><EditableText path="pipeline.qsvmTraining" /></h3>
        <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
          <EditableText path="pipeline.qsvmTrainingDesc" />
        </p>
      </div>

      {/* Mutation analysis chart */}
      {step1 && step1.total > 0 && (
        <div style={exp1Style}>
          <h3 style={titleStyle}><EditableText path="pipeline.mutationResults" /></h3>
          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'flex-start' }}>
            <div style={{ flex: '1 1 280px', minHeight: 220 }}>
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={mutationChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Bar dataKey="count" name="Mutants" radius={[4, 4, 0, 0]}>
                    {mutationChartData.map((entry, i) => (
                      <Cell key={i} fill={entry.fill} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem', minWidth: 140 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ width: 12, height: 12, borderRadius: 2, background: '#16a34a' }} />
                <span>Equivalent: {step1.equivalent}</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ width: 12, height: 12, borderRadius: 2, background: '#c41230' }} />
                <span>Killed: {step1.killed}</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ width: 12, height: 12, borderRadius: 2, background: '#f59e0b' }} />
                <span>Survived: {step1.survived}</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ width: 12, height: 12, borderRadius: 2, background: '#6b7280' }} />
                <span>Crashed: {step1.crashed}</span>
              </div>
              <div style={{ marginTop: '0.5rem', fontWeight: 600 }}>Total: {step1.total}</div>
            </div>
          </div>
        </div>
      )}

      {(!step1 || step1.total === 0) && (
        <div style={exp1Style}>
          <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
            <EditableText path="pipeline.runTestsForExp2" />
          </p>
        </div>
      )}

      {/* Statistical Testing report figures */}
      {(figuresAvailable?.experiment2_heatmap || figuresAvailable?.experiment2_pie) && (
        <div style={exp1Style}>
          <h3 style={titleStyle}><EditableText path="pipeline.reportFigures" /></h3>
          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'flex-start' }}>
            {figuresAvailable.experiment2_heatmap && (
              <div>
                <div style={{ fontWeight: 600, marginBottom: '0.5rem' }}><EditableText path="pipeline.mutantHeatmap" /></div>
                <img
                  src={`${API_BASE}/api/figures/experiment2/heatmap`}
                  alt="Mutant outcome heatmap"
                  style={{ maxWidth: '100%', width: 480, borderRadius: 8, border: '1px solid #e5e7eb' }}
                />
              </div>
            )}
            {figuresAvailable.experiment2_pie && (
              <div>
                <div style={{ fontWeight: 600, marginBottom: '0.5rem' }}><EditableText path="pipeline.detectionCoverage" /></div>
                <img
                  src={`${API_BASE}/api/figures/experiment2/pie`}
                  alt="Mutant detection coverage pie chart"
                  style={{ maxWidth: '100%', width: 320, borderRadius: 8, border: '1px solid #e5e7eb' }}
                />
              </div>
            )}
          </div>
        </div>
      )}
      </div>

      {/* ========== Kernel Testing ========== */}
      <div style={{ borderTop: '2px solid #2563eb', paddingTop: '1rem', marginTop: '0.5rem' }}>
        <h2 style={{ ...titleStyle, fontSize: '1.1rem', color: '#2563eb', marginBottom: '1rem' }}>
          <EditableText path="pipeline.exp3Title" />
        </h2>
        <p style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '1rem' }}>
          <EditableText path="pipeline.exp3Desc" />
        </p>

      {/* Golden matrix & kernel testing */}
      {step2 && step2.rows.length > 0 && (
        <div style={exp2Style}>
          <h3 style={{ ...titleStyle, borderBottomColor: '#2563eb' }}><EditableText path="pipeline.goldenMatrixTitle" /></h3>
          <p style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '1rem' }}>
            <EditableText path="pipeline.goldenMatrixDesc" />
          </p>
          <div style={{ overflowX: 'auto', maxHeight: 320, overflowY: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.75rem' }}>
              <thead>
                <tr style={{ background: '#f9fafb', position: 'sticky', top: 0 }}>
                  <th style={thStyle}><EditableText path="pipeline.mode" /></th>
                  <th style={thStyle}><EditableText path="pipeline.defects" /></th>
                  <th style={thStyle}><EditableText path="pipeline.caughtRate" /></th>
                </tr>
              </thead>
              <tbody>
                {step2.rows.slice(0, 15).map((row, i) => {
                  const caughtRate = row.Caught_Rate
                  const rateStr = typeof caughtRate === 'number' ? caughtRate.toFixed(3) : String(caughtRate ?? '')
                  return (
                    <tr key={i} style={{ borderBottom: '1px solid #e5e7eb' }}>
                      <td style={tdStyle}>{String(row.Mode ?? '')}</td>
                      <td style={tdStyle}>{String(row.Defects ?? '')}</td>
                      <td style={tdStyle}>{rateStr}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {(!step2 || step2.rows.length === 0) && (
        <div style={exp2Style}>
          <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
            <EditableText path="pipeline.runTestsForExp3" />
          </p>
        </div>
      )}

      {/* Kernel Testing report figures */}
      {(figuresAvailable?.experiment3_detection || figuresAvailable?.experiment3_heatmap) && (
        <div style={exp2Style}>
          <h3 style={{ ...titleStyle, borderBottomColor: '#2563eb' }}><EditableText path="pipeline.reportFigures" /></h3>
          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'flex-start' }}>
            {figuresAvailable.experiment3_detection && (
              <div>
                <div style={{ fontWeight: 600, marginBottom: '0.5rem' }}><EditableText path="pipeline.statisticalDetection" /></div>
                <img
                  src={`${API_BASE}/api/figures/experiment3/detection`}
                  alt="Detection confidence by mode"
                  style={{ maxWidth: '100%', width: 480, borderRadius: 8, border: '1px solid #e5e7eb' }}
                />
              </div>
            )}
            {figuresAvailable.experiment3_heatmap && (
              <div>
                <div style={{ fontWeight: 600, marginBottom: '0.5rem' }}><EditableText path="pipeline.mrEfficiency" /></div>
                <img
                  src={`${API_BASE}/api/figures/experiment3/heatmap`}
                  alt="MR efficiency heatmap"
                  style={{ maxWidth: '100%', width: 480, borderRadius: 8, border: '1px solid #e5e7eb' }}
                />
              </div>
            )}
          </div>
        </div>
      )}
      </div>
    </div>
  )
}

const stepBadge = {
  padding: '0.35rem 0.75rem',
  background: '#f3f4f6',
  borderRadius: 8,
  fontWeight: 600,
} as const

const exp1Badge = {
  padding: '0.35rem 0.75rem',
  borderRadius: 8,
  fontWeight: 700,
  fontSize: '0.8rem',
} as const

const arrowStyle = { color: '#9ca3af', fontSize: '1rem' } as const

const thStyle = { padding: '0.5rem 0.75rem', textAlign: 'left' as const } as const
const tdStyle = { padding: '0.5rem 0.75rem' } as const
