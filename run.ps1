Write-Host "Starting ThoughtStream..."
$env:PYTHONPATH = "$PWD"
$env:VIRTUAL_ENV = "$PWD\venv"
$env:Path = "$PWD\venv\Scripts;$env:Path"

python -m thoughtstream.daemon $args

