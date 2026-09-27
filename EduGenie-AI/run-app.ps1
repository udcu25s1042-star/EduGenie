$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $projectRoot '.venv\Scripts\python.exe'

$pythonCandidates = @(
    $venvPython,
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python39\python.exe"
)

$pythonExe = $null
foreach ($candidate in $pythonCandidates) {
    if ($candidate -and (Test-Path $candidate)) {
        $pythonExe = $candidate
        break
    }
}

if (-not $pythonExe) {
    try {
        & py -3.12 -c "print('python3.12 found')" *> $null
        $pythonExe = 'py'
    }
    catch {
        Write-Error "No compatible Python interpreter was found. Install Python 3.12 and try again."
        exit 1
    }
}

if (-not (Test-Path $venvPython)) {
    if ($pythonExe -eq 'py') {
        & py -3.12 -m venv (Join-Path $projectRoot '.venv')
    }
    else {
        & $pythonExe -m venv (Join-Path $projectRoot '.venv')
    }
}

$finalPython = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $finalPython)) {
    Write-Error "Virtual environment was not created successfully."
    exit 1
}

& $finalPython -m pip install --upgrade pip
& $finalPython -m pip install -r (Join-Path $projectRoot 'requirements.txt')
& $finalPython -m uvicorn main:app --host 127.0.0.1 --port 8000
