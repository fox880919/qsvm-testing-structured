import { useState, useEffect } from 'react'
import { useSiteCopy } from './SiteCopyContext'
import { EditableText } from './components/EditableText'
import { Header } from './components/Header'
import { HomePage } from './components/HomePage'
import { ExperimentPage } from './components/ExperimentPage'
import { NotebookPage } from './components/NotebookPage'
import { ReportPage } from './components/ReportPage'
import { EditPanel } from './components/EditPanel'

type TabId = 'home' | 'experiment' | 'notebook' | 'report'

function App() {
  const { siteCopy, isEditPanelOpen } = useSiteCopy()
  const [activeTab, setActiveTab] = useState<TabId>('home')

  useEffect(() => {
    document.title = siteCopy.pageTitle
  }, [siteCopy.pageTitle])
  const [logoError, setLogoError] = useState(false)

  const renderTab = () => {
    switch (activeTab) {
      case 'home':
        return <HomePage />
      case 'experiment':
        return <ExperimentPage />
      case 'notebook':
        return <NotebookPage />
      case 'report':
        return <ReportPage />
    }
  }

  return (
    <div className="app-container" style={{ minHeight: '100vh', background: '#c41230', color: 'white', display: 'flex', flexDirection: 'column' }}>
      <Header
        activeTab={activeTab}
        onTabChange={setActiveTab}
        logoError={logoError}
        setLogoError={setLogoError}
      />

      <main className="app-main" style={{ flex: 1, padding: '1.5rem', maxWidth: '56rem', margin: '0 auto', width: '100%' }}>
        {renderTab()}
      </main>

      <footer className="app-footer" style={{ padding: '1rem', textAlign: 'center', fontSize: '0.875rem', color: 'rgba(255,255,255,0.8)' }}>
        <EditableText path="footer" />
      </footer>
      {isEditPanelOpen && <EditPanel />}
    </div>
  )
}

export default App
