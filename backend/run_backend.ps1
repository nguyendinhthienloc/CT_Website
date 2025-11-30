# Helper PowerShell script to create a venv (if missing), install deps, and run the backend
param()

$venv = Join-Path (Get-Location) '.venv'
$venvPython = Join-Path $venv 'Scripts\python.exe'

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating virtual environment..."
    python -m venv $venv
}

Write-Host "Installing dependencies (may take a moment)..."
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r .\requirements.txt

Write-Host "Starting backend (Ctrl+C to stop)..."
& $venvPython .\app.py
