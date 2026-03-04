import { useState, useEffect } from 'react'
import { useSiteCopy } from '../SiteCopyContext'
import { EditableText } from './EditableText'

const API_BASE = import.meta.env.VITE_API_URL || ''
const LATEX_FILE = 'progress_report_8'

interface LatexFileResponse {
  filename: string
  content: string
}

export function ReportPage() {
  const { siteCopy } = useSiteCopy()
  const [content, setContent] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [pdfError, setPdfError] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)
  const [saveMessage, setSaveMessage] = useState<string | null>(null)

  const pdfUrl = `/api/report/latex/${LATEX_FILE}/pdf`

  const saveAndRecompile = async () => {
    setSaving(true)
    setSaveMessage(null)
    setError(null)
    try {
      const saveRes = await fetch(`${API_BASE}/api/report/latex/${LATEX_FILE}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content }),
      })
      if (!saveRes.ok) {
        const err = await saveRes.json().catch(() => ({}))
        throw new Error(err.detail || 'Failed to save')
      }
      const compileRes = await fetch(`${API_BASE}/api/report/latex/${LATEX_FILE}/compile`, {
        method: 'POST',
      })
      const compileData = await compileRes.json().catch(() => ({}))
      if (!compileData.success) {
        throw new Error(compileData.error || 'PDF compilation failed')
      }
      setSaveMessage(siteCopy.report.saveSuccessMessage)
      setPdfError(null)
      openPdf(pdfUrl)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Save failed')
    } finally {
      setSaving(false)
    }
  }

  const openPdf = async (path: string) => {
    setPdfError(null)
    try {
      const url = `${API_BASE}${path}?t=${Date.now()}`
      const res = await fetch(url, { cache: 'no-store' })
      if (!res.ok) {
        const text = await res.text()
        throw new Error(res.status === 404 ? 'PDF not found' : text || `HTTP ${res.status}`)
      }
      const blob = await res.blob()
      const blobUrl = URL.createObjectURL(blob)
      window.open(blobUrl, '_blank')
      setTimeout(() => URL.revokeObjectURL(blobUrl), 60000)
    } catch (e) {
      setPdfError(e instanceof Error ? e.message : 'Failed to load PDF')
    }
  }

  useEffect(() => {
    setLoading(true)
    setError(null)
    fetch(`${API_BASE}/api/report/latex/${LATEX_FILE}`)
      .then((r) => {
        if (!r.ok) throw new Error(r.status === 404 ? 'File not found' : 'Failed to load')
        return r.json()
      })
      .then((data: LatexFileResponse) => {
        setContent(data.content || '')
      })
      .catch((e) => {
        setError(e.message || 'Failed to load LaTeX file')
        setContent('')
      })
      .finally(() => setLoading(false))
  }, [])

  return (
    <section
      className="app-card"
      style={{
        background: 'white',
        color: '#333',
        borderRadius: 12,
        boxShadow: '0 10px 40px rgba(0,0,0,0.12)',
        padding: '2rem 2.5rem',
      }}
    >
      <h2
        className="app-card-title"
        style={{
          fontSize: '1.25rem',
          fontWeight: 700,
          marginBottom: '1rem',
          paddingBottom: '0.5rem',
          borderBottom: '2px solid #c41230',
          display: 'inline-block',
        }}
      >
        <EditableText path="report.title" />
      </h2>
      <p style={{ color: '#666', marginBottom: '1.5rem', lineHeight: 1.6 }}>
        <EditableText path="report.description" />
      </p>

      <div style={{ marginBottom: '1.5rem', display: 'flex', gap: '0.75rem', flexWrap: 'wrap', alignItems: 'center' }}>
        <button
          type="button"
          onClick={saveAndRecompile}
          disabled={saving || !content}
          style={{
            padding: '0.6rem 1.25rem',
            borderRadius: 8,
            background: '#16a34a',
            color: 'white',
            fontWeight: 600,
            fontSize: '0.9rem',
            border: 'none',
            cursor: saving ? 'wait' : 'pointer',
            opacity: saving || !content ? 0.7 : 1,
          }}
        >
          {saving ? <EditableText path="report.savingButton" /> : <EditableText path="report.saveButton" />}
        </button>
        <button
          type="button"
          onClick={() => openPdf(pdfUrl)}
          style={{
            padding: '0.6rem 1.25rem',
            borderRadius: 8,
            background: '#c41230',
            color: 'white',
            fontWeight: 600,
            fontSize: '0.9rem',
            border: 'none',
            cursor: 'pointer',
          }}
        >
          <EditableText path="report.viewPdfButton" />
        </button>
        {saveMessage && (
          <span style={{ color: '#16a34a', fontSize: '0.875rem' }}>{saveMessage}</span>
        )}
        {pdfError && (
          <span style={{ color: '#c41230', fontSize: '0.875rem' }}>{pdfError}</span>
        )}
      </div>

      {error && (
        <div
          style={{
            padding: '1rem',
            borderRadius: 8,
            background: 'rgba(196, 18, 48, 0.1)',
            color: '#c41230',
            marginBottom: '1rem',
          }}
        >
          {error}
        </div>
      )}

      {loading && <p style={{ color: '#666' }}><EditableText path="report.loadingText" /></p>}

      {!loading && content && (
        <div
          style={{
            borderRadius: 8,
            overflow: 'hidden',
            border: '1px solid #e5e7eb',
            maxHeight: '70vh',
            overflowY: 'auto',
            background: '#1e1e1e',
            color: '#d4d4d4',
          }}
        >
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            style={{
              width: '100%',
              minHeight: '60vh',
              margin: 0,
              padding: '1rem',
              fontSize: '0.8rem',
              lineHeight: 1.5,
              fontFamily: 'ui-monospace, "SF Mono", Monaco, Consolas, monospace',
              background: '#1e1e1e',
              color: '#d4d4d4',
              border: 'none',
              resize: 'vertical',
              boxSizing: 'border-box',
            }}
            spellCheck={false}
          />
        </div>
      )}

      {!loading && !content && !error && (
        <p style={{ color: '#999', fontSize: '0.875rem' }}>
          <EditableText path="report.fileNotFound" />
        </p>
      )}
    </section>
  )
}
