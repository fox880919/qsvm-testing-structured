import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { SiteCopyProvider } from './SiteCopyContext'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <SiteCopyProvider>
      <App />
    </SiteCopyProvider>
  </StrictMode>,
)
