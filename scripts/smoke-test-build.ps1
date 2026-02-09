param(
    [string]$OutputDir = "dist",
    [string]$ArtifactPrefix = "fps-bot-arena",
    [string]$ArtifactPath = ""
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$outputPath = if ([System.IO.Path]::IsPathRooted($OutputDir)) { $OutputDir } else { Join-Path $repoRoot $OutputDir }

if ([string]::IsNullOrWhiteSpace($ArtifactPath)) {
    $buildScriptPath = Join-Path $PSScriptRoot "build.ps1"
    & $buildScriptPath -OutputDir $OutputDir -ArtifactPrefix $ArtifactPrefix | Out-Null

    $artifact = Get-ChildItem -Path $outputPath -Filter "$ArtifactPrefix-*.zip" -File |
        Sort-Object LastWriteTimeUtc -Descending |
        Select-Object -First 1
    if ($null -eq $artifact) {
        throw "No build artifact found in $outputPath"
    }
}
else {
    $resolvedArtifactPath = if ([System.IO.Path]::IsPathRooted($ArtifactPath)) { $ArtifactPath } else { Join-Path $repoRoot $ArtifactPath }
    if (-not (Test-Path $resolvedArtifactPath)) {
        throw "Artifact not found: $resolvedArtifactPath"
    }

    $artifact = Get-Item $resolvedArtifactPath
}

$tempExtractPath = Join-Path ([System.IO.Path]::GetTempPath()) ("fps-bot-arena-smoke-" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $tempExtractPath -Force | Out-Null

try {
    Expand-Archive -Path $artifact.FullName -DestinationPath $tempExtractPath -Force

    $env:FPS_BOT_ARENA_PACKAGE_ROOT = $tempExtractPath
    python -c "import os,sys;root=os.environ['FPS_BOT_ARENA_PACKAGE_ROOT'];sys.path.insert(0,root);import config.config,src.core,src.player,src.weapons,src.projectiles,src.ai,src.economy,src.environment,src.glitch,src.menus,src.audio,src.ui,src.hud,src.graphics;print('Build smoke test passed:', root)"
    if ($LASTEXITCODE -ne 0) {
        throw "Smoke test failed for artifact: $($artifact.FullName)"
    }
}
finally {
    if (Test-Path $tempExtractPath) {
        Remove-Item -Recurse -Force $tempExtractPath
    }
    Remove-Item Env:FPS_BOT_ARENA_PACKAGE_ROOT -ErrorAction SilentlyContinue
}

Write-Output "Validated artifact: $($artifact.FullName)"
