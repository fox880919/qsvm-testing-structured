import { useState, useRef, useEffect } from 'react'
import { useSiteCopy } from '../SiteCopyContext'
import { getByPath } from '../utils/pathUtils'

interface EditableTextProps {
  path: string
  children?: React.ReactNode
  as?: React.ElementType
  style?: React.CSSProperties
  className?: string
}

/** Renders text that becomes editable when edit mode is on. Click to edit inline. */
export function EditableText({ path, children, as: Tag = 'span', style, className }: EditableTextProps) {
  const { siteCopy, isEditMode, setTextAtPath } = useSiteCopy()
  const [editing, setEditing] = useState(false)
  const [value, setValue] = useState('')
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const raw = getByPath(siteCopy, path)
  const displayValue = String(raw ?? (typeof children === 'string' ? children : '') ?? '')

  useEffect(() => {
    if (editing && inputRef.current) {
      inputRef.current.focus()
      inputRef.current.select()
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
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSave()
    }
    if (e.key === 'Escape') {
      setValue(displayValue)
      setEditing(false)
    }
  }

  if (!isEditMode) {
    return <Tag style={style} className={className}>{displayValue || children}</Tag>
  }

  if (editing) {
    return (
      <span style={{ position: 'relative', display: 'inline-block', minWidth: 60 }}>
        <textarea
          ref={inputRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onBlur={handleSave}
          onKeyDown={handleKeyDown}
          style={{
            position: 'absolute',
            left: 0,
            top: 0,
            minWidth: 200,
            minHeight: 60,
            padding: '0.5rem',
            fontSize: 'inherit',
            fontFamily: 'inherit',
            border: '2px solid #c41230',
            borderRadius: 8,
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            zIndex: 10000,
            background: 'white',
          }}
        />
      </span>
    )
  }

  return (
    <Tag
      style={{
        ...style,
        cursor: 'pointer',
        outline: '1px dashed rgba(196,18,48,0.5)',
        outlineOffset: 2,
        borderRadius: 2,
      }}
      className={className}
      onClick={handleClick}
      title="Click to edit"
    >
      {displayValue || children}
    </Tag>
  )
}
