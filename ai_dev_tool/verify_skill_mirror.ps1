[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$workspaceRoot = Split-Path -Parent $PSScriptRoot
$claudeRoot = Join-Path $workspaceRoot '.claude\skills'
$codexRoot = Join-Path $workspaceRoot '.agents\skills'

if (-not (Test-Path -LiteralPath $claudeRoot -PathType Container)) {
    throw "Missing source skill directory: $claudeRoot"
}
if (-not (Test-Path -LiteralPath $codexRoot -PathType Container)) {
    throw "Missing Codex skill directory: $codexRoot"
}

function Get-SkillInventory {
    param([Parameter(Mandatory)][string]$Root)

    $resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
    $inventory = @{}
    Get-ChildItem -LiteralPath $resolvedRoot -Recurse -File |
        Where-Object {
            $_.FullName -notmatch '[\\/]__pycache__[\\/]' -and
            $_.Extension -ne '.pyc'
        } |
        ForEach-Object {
            $relativePath = $_.FullName.Substring($resolvedRoot.Length).TrimStart([char[]]'\/')
            $inventory[$relativePath] = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash
        }
    return $inventory
}

$claudeInventory = Get-SkillInventory -Root $claudeRoot
$codexInventory = Get-SkillInventory -Root $codexRoot
$allRelativePaths = @($claudeInventory.Keys + $codexInventory.Keys | Sort-Object -Unique)
$differences = foreach ($relativePath in $allRelativePaths) {
    if (-not $claudeInventory.ContainsKey($relativePath)) {
        "ONLY_CODEX $relativePath"
    }
    elseif (-not $codexInventory.ContainsKey($relativePath)) {
        "ONLY_CLAUDE $relativePath"
    }
    elseif ($claudeInventory[$relativePath] -ne $codexInventory[$relativePath]) {
        "HASH_MISMATCH $relativePath"
    }
}

if ($differences) {
    $differences | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Host "[PASS] skill mirror matches: $($claudeInventory.Count) files"
exit 0

