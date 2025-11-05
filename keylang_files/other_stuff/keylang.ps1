Param(
    [Parameter(Mandatory = $true)]
    [string]$Path
)

if (!(Test-Path $Path)) {
    Write-Error "File not found: $Path"
    exit 1
}

$klFull = (Resolve-Path $Path).Path
$pyFull = [System.IO.Path]::ChangeExtension($klFull, ".py")

$preOut = Get-Content -Raw $klFull | & python "$PSScriptRoot\preprocess.py"
$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    Write-Error "Preprocess failed with exit code $exitCode"
    exit $exitCode
}

$preOut = Get-Content $klFull | python .\preprocess.py
$joined = ($preOut -join "`r`n")
[System.IO.File]::WriteAllText($pyFull, $joined, (New-Object System.Text.UTF8Encoding($false)))



python "$pyFull"

exit $LASTEXITCODE
