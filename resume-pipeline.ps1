# Resume Pipeline Runner - PowerShell version
# Generates PDFs from JSON resume files in .resumes/ directory

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPath = Join-Path $ScriptDir ".venv"
$PythonScript = Join-Path $ScriptDir ".claude\run_pipeline.py"
$Python = Join-Path $VenvPath "Scripts\python.exe"

if (-not (Test-Path $VenvPath)) {
    Write-Error "Virtual environment not found at $VenvPath"
    exit 1
}

Write-Host "[*] Running Resume Pipeline..."
& $Python $PythonScript @args
