$ErrorActionPreference = "Stop"

Write-Host "Creating virtual environment..."
$venv = Join-Path $PWD ".venv"
$python = Join-Path $venv "Scripts\python.exe"
if (Test-Path $python) {
    $version = & $python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    if ($version.Trim() -ne "3.11") {
        Write-Host "Existing virtual environment uses Python $version; recreating with Python 3.11."
        Remove-Item -Recurse -Force $venv
    }
}
if (-not (Test-Path $python)) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3.11 -m venv $venv
    } elseif (Get-Command python3.11 -ErrorAction SilentlyContinue) {
        python3.11 -m venv $venv
    } else {
        throw "Python 3.11 is required but was not found."
    }
}

Write-Host "Upgrading pip..."
& $python -m pip install --upgrade pip

Write-Host "Installing dependencies..."
& $python -m pip install -r requirements.txt

Write-Host "Validating installed UI and test dependencies..."
& $python -c "import PySide6, moderngl, pytest; print('PySide6-Essentials, moderngl, and pytest are available.')"
if ($LASTEXITCODE -ne 0) {
    throw "Dependency validation failed."
}

Write-Host ""
Write-Host "Setup complete."
Write-Host "Activate with: .\.venv\Scripts\Activate.ps1"