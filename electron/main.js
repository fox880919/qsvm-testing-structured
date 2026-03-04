const { app, BrowserWindow, dialog } = require('electron')
const path = require('path')
const fs = require('fs')
const { spawn } = require('child_process')

const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged
const PORT = 8000
const VITE_PORT = 5173
const BACKEND_TIMEOUT_MS = 45000

let backendProcess = null

function getAppRoot() {
  if (!app.isPackaged) return process.cwd()
  const resourcesPath = process.resourcesPath
  // extraResources: app has api, classes, *.py, progress report, frontend/dist
  const appDir = path.join(resourcesPath, 'app')
  if (fs.existsSync(appDir)) return appDir
  // Fallback: app.asar.unpacked (if api was packed)
  const unpacked = path.join(resourcesPath, 'app.asar.unpacked')
  if (fs.existsSync(unpacked)) return unpacked
  return resourcesPath
}

function findPythonExe(dir) {
  const bin = path.join(dir, 'bin')
  const scripts = path.join(dir, 'Scripts')
  if (fs.existsSync(bin)) {
    const files = fs.readdirSync(bin)
    const py = files.find(f => /^python3?\.?\d*$/.test(f) || f === 'python')
    if (py) return path.join(bin, py)
  }
  const py = path.join(scripts, 'python.exe')
  if (fs.existsSync(scripts) && fs.existsSync(py)) return py
  return null
}

function getBackendPath() {
  const root = getAppRoot()
  const resourcesPath = app.isPackaged ? process.resourcesPath : process.cwd()
  const isWin = process.platform === 'win32'
  // Prefer bundled python (relocatable) over venv
  const pythonDir = path.join(resourcesPath, 'python')
  const venvDir = path.join(resourcesPath, 'venv')
  const bundled = findPythonExe(pythonDir)
  if (bundled) return bundled
  // Fallback: venv
  return isWin
    ? path.join(venvDir, 'Scripts', 'python.exe')
    : path.join(venvDir, 'bin', 'python')
}

function startBackend() {
  return new Promise((resolve, reject) => {
    const root = getAppRoot()
    const pythonPath = getBackendPath()

    if (!fs.existsSync(pythonPath)) {
      reject(new Error(`Python not found at: ${pythonPath}\nApp root: ${root}\nEnsure you ran: npm run electron:build (with asarUnpack)`))
      return
    }

    const backend = spawn(pythonPath, ['-m', 'uvicorn', 'api.server:app', '--host', '127.0.0.1', '--port', String(PORT)], {
      cwd: root,
      env: { ...process.env, PYTHONUNBUFFERED: '1' },
    })
    backendProcess = backend

    backend.stdout?.on('data', (d) => process.env.DEBUG_ELECTRON && console.log(d.toString()))
    backend.stderr?.on('data', (d) => process.env.DEBUG_ELECTRON && console.error(d.toString()))
    backend.on('error', (err) => reject(err))
    backend.on('exit', (code) => {
      backendProcess = null
      if (code !== 0 && code !== null) process.env.DEBUG_ELECTRON && console.error('Backend exited:', code)
    })

    const timeout = setTimeout(() => {
      if (backendProcess) {
        backendProcess.kill()
        backendProcess = null
      }
      reject(new Error(`Backend did not start within ${BACKEND_TIMEOUT_MS / 1000}s. Check that venv and api are in app.asar.unpacked.`))
    }, BACKEND_TIMEOUT_MS)

    const check = () => {
      const http = require('http')
      const req = http.get(`http://127.0.0.1:${PORT}/api/health`, (res) => {
        if (res.statusCode === 200) {
          clearTimeout(timeout)
          resolve()
        } else {
          setTimeout(check, 200)
        }
      })
      req.on('error', () => setTimeout(check, 200))
      req.setTimeout(5000, () => { req.destroy(); setTimeout(check, 200) })
    }
    setTimeout(check, 500)
  })
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
    title: "QSVM Structure Testing | King's College London",
  })

  const loadUrl = isDev
    ? `http://localhost:${VITE_PORT}/`
    : `http://127.0.0.1:${PORT}/`

  win.loadURL(loadUrl).catch(() => {
    win.loadURL(loadUrl)
  })

  if (isDev && process.env.DEBUG_ELECTRON) {
    win.webContents.openDevTools()
  }
}

app.whenReady().then(async () => {
  try {
    await startBackend()
    createWindow()
  } catch (err) {
    console.error('Failed to start backend:', err)
    const msg = err && err.message ? err.message : String(err)
    await dialog.showMessageBox({
      type: 'error',
      title: 'QSVM Structure Testing - Startup Error',
      message: 'Failed to start the Python backend.',
      detail: msg + '\n\nTo debug: run the app from Terminal to see full logs.',
      buttons: ['OK'],
    }).catch(() => {})
    app.quit()
  }
})

app.on('window-all-closed', () => {
  if (backendProcess) {
    backendProcess.kill()
    backendProcess = null
  }
  app.quit()
})
