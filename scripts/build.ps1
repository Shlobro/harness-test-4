param(
    [string]$OutputDir = "dist",
    [string]$ArtifactPrefix = "fps-bot-arena"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$outputPath = if ([System.IO.Path]::IsPathRooted($OutputDir)) {
    $OutputDir
}
else {
    Join-Path $repoRoot $OutputDir
}
$stagingPath = Join-Path $outputPath "package"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$artifactName = "$ArtifactPrefix-$timestamp.zip"
$artifactPath = Join-Path $outputPath $artifactName
$artifactHashPath = "$artifactPath.sha256"

$excludedDirectoryNames = @(
    "__pycache__",
    ".pytest_cache",
    ".git",
    ".agentharness"
)

$excludedFilePatterns = @(
    "*.pyc",
    "*.pyo"
)

function Test-SkipDirectory {
    param([System.IO.DirectoryInfo]$DirectoryInfo)
    return $excludedDirectoryNames -contains $DirectoryInfo.Name
}

function Test-SkipFile {
    param([System.IO.FileInfo]$FileInfo)

    if ($FileInfo.Name -eq "developer-guide.md") {
        return $true
    }

    foreach ($pattern in $excludedFilePatterns) {
        if ($FileInfo.Name -like $pattern) {
            return $true
        }
    }

    return $false
}

function Copy-FilteredDirectory {
    param(
        [string]$SourcePath,
        [string]$DestinationPath
    )

    New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null

    foreach ($entry in Get-ChildItem -LiteralPath $SourcePath -Force) {
        $targetPath = Join-Path $DestinationPath $entry.Name
        if ($entry.PSIsContainer) {
            if (Test-SkipDirectory -DirectoryInfo $entry) {
                continue
            }

            Copy-FilteredDirectory -SourcePath $entry.FullName -DestinationPath $targetPath
            continue
        }

        if (Test-SkipFile -FileInfo $entry) {
            continue
        }

        Copy-Item -LiteralPath $entry.FullName -Destination $targetPath -Force
    }
}

if (Test-Path $stagingPath) {
    Remove-Item -Recurse -Force $stagingPath
}
if (Test-Path $artifactPath) {
    Remove-Item -Force $artifactPath
}
if (Test-Path $artifactHashPath) {
    Remove-Item -Force $artifactHashPath
}

New-Item -ItemType Directory -Path $stagingPath -Force | Out-Null

$pathsToPackage = @(
    "src",
    "config",
    "assets",
    "requirements.txt",
    "README.md",
    "GAMEPLAY.md"
)

foreach ($relativePath in $pathsToPackage) {
    $sourcePath = Join-Path $repoRoot $relativePath
    if (-not (Test-Path $sourcePath)) {
        throw "Missing required path for build artifact: $relativePath"
    }

    $destinationPath = Join-Path $stagingPath $relativePath
    if ((Get-Item $sourcePath) -is [System.IO.DirectoryInfo]) {
        Copy-FilteredDirectory -SourcePath $sourcePath -DestinationPath $destinationPath
    }
    else {
        $destinationParent = Split-Path -Parent $destinationPath
        if (-not (Test-Path $destinationParent)) {
            New-Item -ItemType Directory -Path $destinationParent -Force | Out-Null
        }
        Copy-Item -Force $sourcePath $destinationPath
    }
}

$packagedFiles = Get-ChildItem -Path $stagingPath -Recurse -File
$totalBytes = ($packagedFiles | Measure-Object -Property Length -Sum).Sum
$excludedRules = @($excludedDirectoryNames + $excludedFilePatterns + "developer-guide.md")

$manifestPath = Join-Path $stagingPath "build-manifest.txt"
@(
    "Artifact: $artifactName",
    "GeneratedAtUtc: $((Get-Date).ToUniversalTime().ToString('o'))",
    "Contents: $($pathsToPackage -join ', ')",
    "PackagedFileCount: $($packagedFiles.Count)",
    "PackagedBytes: $totalBytes",
    "ExcludedPatterns: $($excludedRules -join ', ')"
) | Set-Content -Path $manifestPath

Compress-Archive -Path (Join-Path $stagingPath '*') -DestinationPath $artifactPath -CompressionLevel Optimal

$artifactHash = (Get-FileHash -Algorithm SHA256 -Path $artifactPath).Hash.ToLowerInvariant()
"$artifactHash *$artifactName" | Set-Content -Path $artifactHashPath

Write-Output "Build complete: $artifactPath"
Write-Output "SHA256: $artifactHash"
