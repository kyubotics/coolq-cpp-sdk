$originDir = Get-Location
$projectDir = Split-Path $PSScriptRoot -Parent

# 辅助函数

function Write-Success
{
    param ($InputObject)
    Write-Host  "$InputObject" -ForegroundColor Green
}

function Write-Failure
{
    param ($InputObject)
    Write-Host  "$InputObject" -ForegroundColor Red
}

function SafeExit
{
    param ($ExitCode)
    Set-Location $originDir
    exit $ExitCode
}
