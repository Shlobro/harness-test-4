# Scripts Developer Guide

## Purpose
`scripts/` contains operational tooling for packaging and release workflows.

## Files
- `build.ps1`: builds a production-ready zip artifact under `dist/`.
- `smoke-test-build.ps1`: performs build + import smoke test on the packaged artifact.

## Build Script Behavior
- Stages runtime files into `dist/package/`.
- Packages `src/`, `config/`, `assets/`, `requirements.txt`, `README.md`, and `GAMEPLAY.md`.
- Excludes non-runtime payload from the artifact (`__pycache__/`, `*.pyc`, `*.pyo`, and `developer-guide.md`).
- Writes `build-manifest.txt` with artifact metadata, packaged file count, and packaged byte size.
- Produces a timestamped zip artifact: `dist/fps-bot-arena-<timestamp>.zip`.
- Writes a checksum sidecar: `dist/fps-bot-arena-<timestamp>.zip.sha256`.

## Usage
From repository root:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build.ps1
```

Optional overrides:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build.ps1 -OutputDir dist -ArtifactPrefix fps-bot-arena
```

Smoke-test the packaged output:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\smoke-test-build.ps1
```

Validate an existing artifact:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\smoke-test-build.ps1 -ArtifactPath dist\fps-bot-arena-<timestamp>.zip
```
