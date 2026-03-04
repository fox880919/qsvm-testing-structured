#!/usr/bin/env node
/**
 * Downloads python-build-standalone and installs requirements.
 * Bundles a relocatable Python so the app works without system Python.
 *
 * Usage: node scripts/prepare-python.js [--all]
 *   --all  Prepare python-darwin-arm64, python-darwin-x64, python-win32-x64 (for cross-build)
 *
 * Output: python/ (or python-{platform}/ when using --all)
 */

const fs = require('fs')
const path = require('path')
const { execSync } = require('child_process')
const https = require('https')

const RELEASE = '20260211'
const PYTHON_VERSION = '3.13.12'
const BASE_URL = `https://github.com/astral-sh/python-build-standalone/releases/download/${RELEASE}`

const PLATFORMS = {
  'darwin-arm64': `cpython-${PYTHON_VERSION}+${RELEASE}-aarch64-apple-darwin-install_only.tar.gz`,
  'darwin-x64': `cpython-${PYTHON_VERSION}+${RELEASE}-x86_64-apple-darwin-install_only.tar.gz`,
  'win32-x64': `cpython-${PYTHON_VERSION}+${RELEASE}-x86_64-pc-windows-msvc-install_only.tar.gz`,
}

function download(url, dest) {
  return new Promise((resolve, reject) => {
    const request = (u) => {
      const file = fs.createWriteStream(dest)
      https.get(u, (res) => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          file.close()
          try { fs.unlinkSync(dest) } catch {}
          request(res.headers.location)
          return
        }
        if (res.statusCode !== 200) {
          file.close()
          try { fs.unlinkSync(dest) } catch {}
          reject(new Error(`HTTP ${res.statusCode} for ${u}`))
          return
        }
        res.pipe(file)
        file.on('finish', () => { file.close(); resolve() })
        file.on('error', reject)
      }).on('error', reject)
    }
    request(url)
  })
}

function getTargets() {
  const all = process.argv.includes('--all')
  if (all) {
    return Object.entries(PLATFORMS).map(([name, archive]) => ({
      name,
      archive,
      outDir: `python-${name}`,
    }))
  }
  const platform = process.platform
  const arch = process.arch
  let key
  if (platform === 'darwin') key = arch === 'arm64' ? 'darwin-arm64' : 'darwin-x64'
  else if (platform === 'win32') key = 'win32-x64'
  else { console.error('Unsupported:', platform); process.exit(1) }
  return [{ name: key, archive: PLATFORMS[key], outDir: 'python' }]
}

function getPythonExe(dir) {
  const bin = path.join(dir, 'bin')
  const scripts = path.join(dir, 'Scripts')
  if (fs.existsSync(bin)) {
    for (const f of fs.readdirSync(bin)) {
      if (/^python3?\.?\d*$/.test(f) || f === 'python') return path.join(bin, f)
    }
  }
  const py = path.join(scripts, 'python.exe')
  if (fs.existsSync(scripts) && fs.existsSync(py)) return py
  const rootExe = path.join(dir, 'python.exe')
  return fs.existsSync(rootExe) ? rootExe : null
}

async function main() {
  const root = path.join(__dirname, '..')
  const targets = getTargets()

  for (const { name, archive, outDir } of targets) {
    const url = `${BASE_URL}/${encodeURIComponent(archive)}`
    const archivePath = path.join(root, archive)
    const outPath = path.join(root, outDir)

    console.log(`\n=== ${name} ===`)
    if (fs.existsSync(outPath)) {
      console.log(`Skipping ${name}: ${outDir} exists. Delete to re-download.`)
    } else {
      if (!fs.existsSync(archivePath)) {
        console.log(`Downloading ${archive}...`)
        await download(url, archivePath)
      }
      console.log(`Extracting...`)
      execSync(`tar -xzf "${archivePath}" -C "${root}"`, { stdio: 'inherit' })
      const extracted = path.join(root, 'python')
      if (outDir !== 'python' && fs.existsSync(extracted)) {
        fs.renameSync(extracted, outPath)
      }
      fs.unlinkSync(archivePath)
    }

    const pythonDir = outPath
    const pythonExe = getPythonExe(pythonDir)
    if (!pythonExe) {
      console.error(`Could not find Python in ${pythonDir}`)
      process.exit(1)
    }

    const freezePath = path.join(root, 'requirements-freeze.txt')
    const reqPath = path.join(root, 'api', 'requirements.txt')
    const reqFile = fs.existsSync(freezePath) ? freezePath : reqPath

    console.log(`Installing packages (${reqFile})...`)
    execSync(`"${pythonExe}" -m pip install --no-warn-script-location -r "${reqFile}"`, {
      stdio: 'inherit',
      cwd: root,
    })
  }

  console.log('\nDone. Add python/ to extraResources and use it in getBackendPath().')
}

main().catch((e) => { console.error(e); process.exit(1) })
