#!/usr/bin/env node
const { spawn } = require('child_process')
const readline = require('readline')

const mode = process.argv[2]?.toLowerCase()

if (mode === 'web' || mode === 'electron') {
  run(mode)
} else {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout })
  console.log('\n  QSVM Structure Testing\n')
  console.log('  1) Web    - Run in browser (http://localhost:5173)')
  console.log('  2) Electron - Run as desktop app\n')
  rl.question('  Choose [1/2]: ', (answer) => {
    rl.close()
    const n = answer.trim()
    if (n === '2') run('electron')
    else run('web')
  })
}

function run(mode) {
  const isWin = process.platform === 'win32'
  const cmd = isWin ? 'npm.cmd' : 'npm'
  const args = ['run', mode]
  const child = spawn(cmd, args, {
    stdio: 'inherit',
    shell: isWin,
    cwd: __dirname,
  })
  child.on('exit', (code) => process.exit(code ?? 0))
}
