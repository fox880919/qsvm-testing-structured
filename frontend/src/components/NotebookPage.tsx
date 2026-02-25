import { useState } from 'react'
import { useSiteCopy } from '../SiteCopyContext'
import { EditableText } from './EditableText'
import { EditableLongText } from './EditableLongText'

const API_BASE = import.meta.env.VITE_API_URL || ''

type CellType = 'markdown' | 'code'

interface NotebookCell {
  id: string
  type: CellType
  content: string
}

interface NotebookSection {
  id: string
  title: string
  experiment?: 1 | 2 | 3
  cells: NotebookCell[]
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

const SECTION_COLORS: Record<number, string> = {
  1: '#16a34a',
  2: '#c41230',
  3: '#2563eb',
}

function CodeCell({ code, onOutput }: { code: string; onOutput: (out: string, err: string) => void }) {
  const [output, setOutput] = useState('')
  const [error, setError] = useState('')
  const [running, setRunning] = useState(false)

  const handleRun = async () => {
    setRunning(true)
    setOutput('')
    setError('')
    try {
      const res = await fetch(`${API_BASE}/api/notebook/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code }),
      })
      const data = await res.json()
      const out = data.stdout || ''
      const err = data.stderr || (data.error ? `Error: ${data.error}` : '')
      setOutput(out)
      setError(err)
      onOutput(out, err)
    } catch (e) {
      const msg = e instanceof Error ? e.message : 'Request failed'
      setError(msg)
      onOutput('', msg)
    } finally {
      setRunning(false)
    }
  }

  return (
    <div style={{ marginTop: '0.5rem' }}>
      <pre style={{
        background: '#1e293b',
        color: '#e2e8f0',
        padding: '1rem',
        borderRadius: 8,
        fontSize: '0.8rem',
        overflow: 'auto',
        marginBottom: '0.5rem',
      }}>
        {code}
      </pre>
      <button
        onClick={(e) => { e.stopPropagation(); handleRun() }}
        disabled={running}
        style={{
          padding: '0.5rem 1rem',
          borderRadius: 8,
          background: '#c41230',
          color: 'white',
          fontWeight: 600,
          border: 'none',
          cursor: running ? 'not-allowed' : 'pointer',
          opacity: running ? 0.7 : 1,
        }}
      >
        {running ? 'Running...' : 'Run'}
      </button>
      {(output || error) && (
        <pre style={{
          marginTop: '1rem',
          padding: '1rem',
          background: '#111827',
          color: output ? '#4ade80' : '#f87171',
          fontSize: '0.8rem',
          borderRadius: 8,
          overflow: 'auto',
          maxHeight: 200,
          fontFamily: 'monospace',
        }}>
          {output || error}
        </pre>
      )}
    </div>
  )
}

function MarkdownCell({ content }: { content: string }) {
  const lines = content.split('\n')
  const elements: React.ReactNode[] = []
  let i = 0
  while (i < lines.length) {
    const line = lines[i]
    if (line.startsWith('## ')) {
      elements.push(<h3 key={i} style={{ fontSize: '1.1rem', fontWeight: 700, margin: '1rem 0 0.5rem' }}>{line.slice(3)}</h3>)
    } else if (line.startsWith('### ')) {
      elements.push(<h4 key={i} style={{ fontSize: '1rem', fontWeight: 600, margin: '0.75rem 0 0.25rem' }}>{line.slice(4)}</h4>)
    } else if (line.startsWith('| ')) {
      const rows: string[] = [line]
      while (i + 1 < lines.length && lines[i + 1].startsWith('| ')) {
        i++
        rows.push(lines[i])
      }
      const parsed = rows.map(r => r.split('|').slice(1, -1).map(c => c.trim()))
      const isSeparator = (row: string[]) => row.every(c => /^-+$/.test(c))
      const dataRows = parsed.filter(row => !isSeparator(row))
      const headerRow = dataRows[0]
      const bodyRows = dataRows.slice(1)
      elements.push(
        <table key={i} style={{ borderCollapse: 'collapse', margin: '0.5rem 0', fontSize: '0.875rem' }}>
          {headerRow && (
            <thead>
              <tr>
                {headerRow.map((cell, ci) => (
                  <th key={ci} style={{ border: '1px solid #e5e7eb', padding: '0.35rem 0.75rem', fontWeight: 600, textAlign: 'left' }}>{cell}</th>
                ))}
              </tr>
            </thead>
          )}
          <tbody>
            {bodyRows.map((row, ri) => (
              <tr key={ri}>
                {row.map((cell, ci) => (
                  <td key={ci} style={{ border: '1px solid #e5e7eb', padding: '0.35rem 0.75rem' }}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )
    } else if (line.startsWith('```')) {
      const codeLines: string[] = []
      i++
      while (i < lines.length && !lines[i].startsWith('```')) {
        codeLines.push(lines[i])
        i++
      }
      if (i < lines.length) i++
      elements.push(
        <pre key={i} style={{ background: '#1e293b', color: '#e2e8f0', padding: '1rem', borderRadius: 8, fontSize: '0.8rem', overflow: 'auto', margin: '0.5rem 0' }}>
          <code>{codeLines.join('\n')}</code>
        </pre>
      )
    } else if (line.startsWith('- ')) {
      const items = [line.slice(2)]
      while (i + 1 < lines.length && lines[i + 1].startsWith('- ')) {
        i++
        items.push(lines[i].slice(2))
      }
      elements.push(<ul key={i} style={{ margin: '0.5rem 0', paddingLeft: '1.5rem' }}>{items.map((item, j) => <li key={j}>{item}</li>)}</ul>)
    } else if (line.trim()) {
      const parts = line.split(/(`[^`]+`|\*\*[^*]+\*\*)/g)
      elements.push(<p key={i} style={{ margin: '0.5rem 0', lineHeight: 1.6 }}>{parts.map((p, j) => {
        if (p.startsWith('`') && p.endsWith('`')) return <code key={j} style={{ background: '#f1f5f9', padding: '0.1rem 0.3rem', borderRadius: 4 }}>{p.slice(1, -1)}</code>
        if (p.startsWith('**') && p.endsWith('**')) return <strong key={j}>{p.slice(2, -2)}</strong>
        return p
      })}</p>)
    } else {
      elements.push(<br key={i} />)
    }
    i++
  }
  return <div style={{ lineHeight: 1.6, color: '#444' }}>{elements}</div>
}

export function NotebookPage() {
  const { siteCopy, isEditMode } = useSiteCopy()
  const [activeSubsection, setActiveSubsection] = useState<string>('intro')

  const sections = (siteCopy.notebook as { sections?: NotebookSection[] }).sections ?? []
  const tabs = (siteCopy.notebook as { tabs?: { id: string; label: string }[] }).tabs ?? []
  const activeSection = sections.find((s) => s.id === activeSubsection) ?? sections[0]

  if (sections.length === 0) {
    return (
      <div style={{ maxWidth: '72rem', margin: 0 }}>
        <section style={cardStyle}>
          <p style={{ color: '#666' }}>Notebook data is loading...</p>
        </section>
      </div>
    )
  }

  return (
    <div style={{ maxWidth: '72rem', margin: 0 }}>
      <section style={cardStyle}>
        <h2 style={titleStyle}><EditableText path="notebook.title" /></h2>
        <p style={{ color: '#666', marginBottom: '1rem' }}>
          <EditableText path="notebook.intro" />
        </p>

        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '0.5rem',
            marginBottom: '1.5rem',
            paddingBottom: '1rem',
            borderBottom: '2px solid #e5e7eb',
          }}
        >
          {tabs.map((tab, tabIdx) => {
            const section = sections.find((s) => s.id === tab.id)
            const isActive = activeSubsection === tab.id
            const color = section?.experiment ? SECTION_COLORS[section.experiment] : '#6b7280'
            return (
              <button
                key={tab.id}
                type="button"
                onClick={() => setActiveSubsection(tab.id)}
                style={{
                  padding: '0.5rem 1rem',
                  borderRadius: 8,
                  border: `2px solid ${isActive ? color : '#e5e7eb'}`,
                  background: isActive ? (section?.experiment ? `${color}15` : '#f9fafb') : 'white',
                  color: isActive ? (section?.experiment ? color : '#333') : '#6b7280',
                  fontWeight: isActive ? 700 : 500,
                  cursor: 'pointer',
                  fontSize: '0.9rem',
                }}
              >
                {isEditMode ? <EditableText path={`notebook.tabs.${tabIdx}.label`} /> : tab.label}
              </button>
            )
          })}
        </div>

        <div
          key={activeSection.id}
          style={{
            paddingTop: activeSection.experiment ? '0.5rem' : 0,
            borderTop: activeSection.experiment ? `3px solid ${SECTION_COLORS[activeSection.experiment]}` : 'none',
          }}
        >
          <h3
            style={{
              fontSize: '1.15rem',
              fontWeight: 700,
              marginBottom: '1rem',
              color: activeSection.experiment ? SECTION_COLORS[activeSection.experiment] : '#333',
            }}
          >
            {isEditMode ? (
              <EditableText path={`notebook.sections.${sections.indexOf(activeSection)}.title`} />
            ) : (
              activeSection.title
            )}
          </h3>
          {activeSection.cells.map((cell, cellIdx) => {
            const sectionIdx = sections.indexOf(activeSection)
            const contentPath = `notebook.sections.${sectionIdx}.cells.${cellIdx}.content`
            return (
              <div key={cell.id} style={{ marginBottom: '1.5rem' }}>
                {cell.type === 'markdown' ? (
                  <EditableLongText
                    path={contentPath}
                    renderPreview={(content) => <MarkdownCell content={content} />}
                    minRows={8}
                  />
                ) : (
                  <EditableLongText
                    path={contentPath}
                    renderPreview={(content) => <CodeCell code={content} onOutput={() => {}} />}
                    minRows={6}
                  />
                )}
              </div>
            )
          })}
        </div>
      </section>
    </div>
  )
}
