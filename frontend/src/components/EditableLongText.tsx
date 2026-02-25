import { useState, useRef, useEffect } from 'react'
import { useSiteCopy } from '../SiteCopyContext'
import { getByPath } from '../utils/pathUtils'

interface EditableLongTextProps {
  path: string
  renderPreview: (content: string) => React.ReactNode
  minRows?: number
}

/** Renders long/multiline content that becomes editable when edit mode is on. Click to edit in textarea. */
export function EditableLongText({ path, renderPreview, minRows = 8 }: EditableLongTextProps) {
  const { siteCopy, isEditMode, setTextAtPath } = useSiteCopy()
  const [editing, setEditing] = useState(false)
  const [value, setValue] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const displayValue = String(getByPath(siteCopy, path) ?? '')

  useEffect(() => {
    if (editing && textareaRef.current) {
      textareaRef.current.focus()
      textareaRef.current.select()
    }
  }, [editing])

  const handleClick = () => {
    if (isEditMode && !editing) {
      setValue(displayValue)
      setEditing(true)
    }
  }

  const handleSave = () => {
    setTextAtPath(path, value)
    setEditing(false)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      setValue(displayValue)
      setEditing(false)
    }
  }

  if (!isEditMode) {
    return (
      <div onClick={handleClick} style={{ cursor: 'pointer' }}>
        {renderPreview(displayValue)}
      </div>
    )
  }

  if (editing) {
    return (
      <div
        style={{
          marginBottom: '1rem',
          outline: '2px dashed rgba(196,18,48,0.6)',
          borderRadius: 8,
          padding: '0.5rem',
          background: '#fef2f2',
        }}
      >
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onBlur={handleSave}
          onKeyDown={handleKeyDown}
          rows={minRows}
          style={{
            width: '100%',
            minHeight: 120,
            padding: '0.75rem',
            fontSize: '0.85rem',
            fontFamily: 'ui-monospace, "SF Mono", Monaco, Consolas, monospace',
            border: '2px solid #c41230',
            borderRadius: 8,
            resize: 'vertical',
            boxSizing: 'border-box',
          }}
        />
        <div style={{ fontSize: '0.75rem', color: '#6b7280', marginTop: '0.25rem' }}>
          Click outside or press Escape to save
        </div>
      </div>
    )
  }

  return (
    <div
      onClick={handleClick}
      style={{
        cursor: 'pointer',
        outline: '1px dashed rgba(196,18,48,0.5)',
        outlineOffset: 2,
        borderRadius: 4,
        padding: '0.25rem 0',
      }}
      title="Click to edit"
    >
      {renderPreview(displayValue)}
    </div>
  )
}
