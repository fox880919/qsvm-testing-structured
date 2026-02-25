import { useSiteCopy } from '../SiteCopyContext'
import { EditableText } from './EditableText'

type TabId = 'home' | 'experiment' | 'notebook' | 'report'

interface HeaderProps {
  activeTab: TabId
  onTabChange: (tab: TabId) => void
  logoError: boolean
  setLogoError: (v: boolean) => void
}

export function Header({ activeTab, onTabChange, logoError, setLogoError }: HeaderProps) {
  const { siteCopy, isEditMode, setEditMode, setEditPanelOpen } = useSiteCopy()
  const TABS: { id: TabId; labelKey: string }[] = [
    { id: 'home', labelKey: 'header.tabs.home' },
    { id: 'experiment', labelKey: 'header.tabs.experiment' },
    { id: 'notebook', labelKey: 'header.tabs.notebook' },
    { id: 'report', labelKey: 'header.tabs.report' },
  ]
  return (
    <header className="app-header" style={{
      backgroundColor: '#9e0e26',
      padding: '1rem 1.5rem',
      borderBottom: '2px solid rgba(255,255,255,0.3)',
    }}>
      <div style={{ maxWidth: '56rem', margin: '0 auto' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1rem', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', minHeight: 56 }}>
            {!logoError ? (
              <img
                src="/kings-logo.png"
                alt={siteCopy.header.logoAlt as string}
                style={{ height: 56, objectFit: 'contain' }}
                onError={(e) => {
                  const img = e.currentTarget
                  if (img.src.endsWith('.png')) {
                    img.src = '/kings-logo.svg'
                  } else {
                    setLogoError(true)
                  }
                }}
              />
            ) : (
              <div style={{ fontFamily: 'Georgia, serif' }}>
                <EditableText path="headerFallback.kings" style={{ fontSize: '1.5rem', fontWeight: 700, letterSpacing: '-0.02em' }} />
                <EditableText path="headerFallback.college" style={{ fontSize: '1.125rem', fontStyle: 'italic', marginLeft: 4 }} />
                <EditableText path="headerFallback.london" style={{ fontSize: '1.5rem', fontWeight: 700, display: 'block' }} />
              </div>
            )}
          </div>
          <div style={{ textAlign: 'right' }}>
            <h1 style={{ fontSize: '1.125rem', fontWeight: 700 }}><EditableText path="header.title" /></h1>
            <p style={{ fontSize: '0.875rem', color: 'rgba(255,255,255,0.9)' }}><EditableText path="header.subtitle" /></p>
          </div>
        </div>
        <nav className="app-nav" style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '1rem' }}>
          {TABS.map(({ id, labelKey }) => (
            <button
              key={id}
              onClick={() => onTabChange(id)}
              className={activeTab === id ? 'app-nav-btn active' : 'app-nav-btn'}
              style={{
                padding: '0.5rem 1rem',
                borderRadius: 8,
                fontWeight: 600,
                cursor: 'pointer',
                border: 'none',
                backgroundColor: activeTab === id ? 'white' : 'rgba(255,255,255,0.15)',
                color: activeTab === id ? '#c41230' : 'white',
              }}
            >
              <EditableText path={labelKey} />
            </button>
          ))}
          <button
            onClick={() => setEditMode(!isEditMode)}
            style={{
              padding: '0.5rem 1rem',
              borderRadius: 8,
              border: '1px solid rgba(255,255,255,0.5)',
              background: isEditMode ? 'white' : 'rgba(255,255,255,0.1)',
              color: isEditMode ? '#c41230' : 'white',
              fontWeight: 600,
              cursor: 'pointer',
              marginLeft: 'auto',
            }}
            title={isEditMode ? 'Done editing' : 'Edit site text'}
          >
            {isEditMode ? 'Done' : 'Edit'}
          </button>
          {isEditMode && (
            <button
              onClick={() => setEditPanelOpen(true)}
              style={{
                padding: '0.5rem 1rem',
                borderRadius: 8,
                border: '1px solid rgba(255,255,255,0.5)',
                background: 'rgba(255,255,255,0.1)',
                color: 'white',
                fontWeight: 600,
                cursor: 'pointer',
              }}
              title="Edit all text as JSON"
            >
              Edit all (JSON)
            </button>
          )}
        </nav>
      </div>
    </header>
  )
}
