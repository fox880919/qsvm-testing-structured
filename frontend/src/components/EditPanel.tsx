import { useState, useEffect } from 'react'
import { useSiteCopy } from '../SiteCopyContext'

export function EditPanel() {
  const { siteCopy, saveSiteCopy, resetToDefaults, setEditPanelOpen } = useSiteCopy()
  const [text, setText] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    setText(JSON.stringify(siteCopy, null, 2))
    setError(null)
  }, [siteCopy])

  const handleSave = () => {
    setError(null)
    try {
      const parsed = JSON.parse(text) as typeof siteCopy
      saveSiteCopy(parsed)
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Invalid JSON')
    }
  }

  const handleReset = () => {
    if (confirm('Reset all text to defaults? This cannot be undone.')) {
      resetToDefaults()
      setEditPanelOpen(false)
    }
  }

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 9999,
        background: 'rgba(0,0,0,0.5)',
        display: 'flex',
        alignItems: 'stretch',
        justifyContent: 'flex-end',
      }}
      onClick={() => setEditPanelOpen(false)}
    >
      <div
        style={{
          width: 'min(90vw, 640px)',
          maxWidth: 640,
          background: 'white',
          boxShadow: '-4px 0 24px rgba(0,0,0,0.2)',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div
          style={{
            padding: '1rem 1.5rem',
            borderBottom: '2px solid #e5e7eb',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '1rem',
            flexWrap: 'wrap',
          }}
        >
          <h2 style={{ margin: 0, fontSize: '1.25rem', fontWeight: 700, color: '#111' }}>
            Edit Site Text
          </h2>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button
              onClick={handleReset}
              style={{
                padding: '0.5rem 1rem',
                borderRadius: 8,
                border: '1px solid #dc2626',
                background: 'white',
                color: '#dc2626',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Reset to Defaults
            </button>
            <button
              onClick={handleSave}
              style={{
                padding: '0.5rem 1rem',
                borderRadius: 8,
                border: 'none',
                background: saved ? '#16a34a' : '#c41230',
                color: 'white',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              {saved ? 'Saved!' : 'Save'}
            </button>
            <button
              onClick={() => setEditPanelOpen(false)}
              style={{
                padding: '0.5rem 1rem',
                borderRadius: 8,
                border: '1px solid #6b7280',
                background: 'white',
                color: '#374151',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Close
            </button>
          </div>
        </div>

        <p style={{ padding: '0.75rem 1.5rem', margin: 0, fontSize: '0.875rem', color: '#6b7280' }}>
          Edit the JSON below to change any text on the website. Save to apply changes.
        </p>

        {error && (
          <div
            style={{
              margin: '0 1.5rem',
              padding: '0.75rem 1rem',
              background: '#fef2f2',
              color: '#dc2626',
              borderRadius: 8,
              fontSize: '0.875rem',
            }}
          >
            {error}
          </div>
        )}

        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          spellCheck={false}
          style={{
            flex: 1,
            minHeight: 400,
            margin: '0 1.5rem 1.5rem',
            padding: '1rem',
            fontFamily: 'ui-monospace, "SF Mono", Monaco, Consolas, monospace',
            fontSize: '0.8rem',
            lineHeight: 1.5,
            border: '2px solid #e5e7eb',
            borderRadius: 8,
            resize: 'vertical',
          }}
        />
      </div>
    </div>
  )
}
