@echo off
echo Building QSVM Structure Testing for Windows...
if not exist "python" (
  echo python/ not found. Run setup-python.bat first.
  exit /b 1
)
call npm run electron:build -- --win
if %ERRORLEVEL% NEQ 0 (
  echo Build failed.
  exit /b 1
)
echo.
echo Done. Output in dist-electron/
