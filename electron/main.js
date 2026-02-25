const { app, BrowserWindow } = require('electron')
const path = require('path')
const { spawn } = require('child_process')

const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged
const PORT = 8000
const VITE_PORT = 5173

let backendProcess = null

function getBackendPath() {
  const root = process.cwd()
  const isWin = process.platform === 'win32'
  const pythonPath = isWin
    ? path.join(root, 'venv', 'Scripts', 'python.exe')
    : path.join(root, 'venv', 'bin', 'python')
  return pythonPath
}

function startBackend() {
  return new Promise((resolve, reject) => {
    const pythonPath = getBackendPath()
    const backend = spawn(pythonPath, ['-m', 'uvicorn', 'api.server:app', '--host', '127.0.0.1', '--port', String(PORT)], {
      cwd: process.cwd(),
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

    // Wait for backend to be ready
    const check = () => {
      const http = require('http')
      const req = http.get(`http://127.0.0.1:${PORT}/api/health`, (res) => {
        if (res.statusCode === 200) resolve()
        else setTimeout(check, 200)
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
