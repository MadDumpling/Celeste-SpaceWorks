$ErrorActionPreference = "Stop"
$env:QT_QPA_PLATFORM = "offscreen"

$python = Join-Path $PWD ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    throw "Virtual environment not found. Run .\setup.ps1 first."
}

& $python -m pytest -v