Write-Host "Installing ThoughtStream..."

# Check for Python
$pythonVersion = python --version
if ($LASTEXITCODE -ne 0) {
    Write-Error "Python not found."
    exit 1
}
Write-Host "Found $pythonVersion"

# Create venv
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate venv (for this script scope)
$env:VIRTUAL_ENV = "$PWD\venv"
$env:Path = "$PWD\venv\Scripts;$env:Path"

# Install dependencies
Write-Host "Installing dependencies..."
pip install -e .

# Setup config
$configDir = "$env:USERPROFILE\.config\thoughtstream"
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Force -Path $configDir | Out-Null
}

$configFile = "$configDir\config.yaml"
if (-not (Test-Path $configFile)) {
    Copy-Item "config.yaml.example" -Destination $configFile
    Write-Host "Created config at $configFile"
}

Write-Host "Installation complete. Run 'thoughtstream daemon' to start."

