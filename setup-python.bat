@echo off
echo Preparing bundled Python (python-build-standalone)...
call npm run prepare:python
if %ERRORLEVEL% NEQ 0 (
  echo Setup failed.
  exit /b 1
)
echo.
echo Python ready. Run build.bat to build the app.
