import { createContext, useContext, useState, useCallback, type ReactNode } from 'react'
import { SITE_COPY as DEFAULT_SITE_COPY } from './siteCopy'
import { DEFAULT_NOTEBOOK_SECTIONS } from './notebookData'
import { setByPath } from './utils/pathUtils'

const STORAGE_KEY = 'qsvm_site_copy'

export type SiteCopy = typeof DEFAULT_SITE_COPY

function mergeWithDefaults(stored: SiteCopy | null): SiteCopy {
  if (!stored) return JSON.parse(JSON.stringify(DEFAULT_SITE_COPY))
  const merged = JSON.parse(JSON.stringify(stored)) as SiteCopy
  const nb = merged.notebook as { sections?: unknown[]; tabs?: unknown[] } | undefined
  if (!nb?.sections?.length) {
    ;(merged as Record<string, unknown>).notebook = {
      ...(nb ?? {}),
      sections: JSON.parse(JSON.stringify(DEFAULT_NOTEBOOK_SECTIONS)),
      tabs: nb?.tabs?.length ? nb.tabs : DEFAULT_SITE_COPY.notebook.tabs,
    }
  }
  return merged
}

interface SiteCopyContextValue {
  siteCopy: SiteCopy
  saveSiteCopy: (copy: SiteCopy) => void
  setTextAtPath: (path: string, value: unknown) => void
  resetToDefaults: () => void
  isEditMode: boolean
  setEditMode: (v: boolean) => void
  isEditPanelOpen: boolean
  setEditPanelOpen: (v: boolean) => void
}

const SiteCopyContext = createContext<SiteCopyContextValue | null>(null)

function loadFromStorage(): SiteCopy | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    return JSON.parse(raw) as SiteCopy
  } catch {
    return null
  }
}

export function SiteCopyProvider({ children }: { children: ReactNode }) {
  const [siteCopy, setSiteCopyState] = useState<SiteCopy>(() => {
    const stored = loadFromStorage()
    return mergeWithDefaults(stored)
  })
  const [isEditMode, setEditMode] = useState(false)
  const [isEditPanelOpen, setEditPanelOpen] = useState(false)

  const saveSiteCopy = useCallback((copy: SiteCopy) => {
    setSiteCopyState(copy)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(copy))
  }, [])

  const resetToDefaults = useCallback(() => {
    setSiteCopyState(JSON.parse(JSON.stringify(DEFAULT_SITE_COPY)))
    localStorage.removeItem(STORAGE_KEY)
  }, [])

  const setTextAtPath = useCallback((path: string, value: unknown) => {
    setSiteCopyState((prev) => {
      const next = setByPath(prev, path, value)
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
      return next
    })
  }, [])

  return (
    <SiteCopyContext.Provider
      value={{
        siteCopy,
        saveSiteCopy,
        setTextAtPath,
        resetToDefaults,
        isEditMode,
        setEditMode,
        isEditPanelOpen,
        setEditPanelOpen,
      }}
    >
      {children}
    </SiteCopyContext.Provider>
  )
}

export function useSiteCopy() {
  const ctx = useContext(SiteCopyContext)
  if (!ctx) throw new Error('useSiteCopy must be used within SiteCopyProvider')
  return ctx
}
