from __future__ import annotations

import subprocess
import zipfile
from pathlib import Path


def test_build_artifact_contains_runtime_files_only(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    output_dir = tmp_path / "dist"
    build_script = repo_root / "scripts" / "build.ps1"

    subprocess.run(
        [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(build_script),
            "-OutputDir",
            str(output_dir),
            "-ArtifactPrefix",
            "test-fps-bot-arena",
        ],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )

    artifacts = sorted(output_dir.glob("test-fps-bot-arena-*.zip"))
    assert artifacts, "Expected a build artifact to be generated."
    artifact_path = artifacts[-1]

    hash_sidecar = Path(f"{artifact_path}.sha256")
    assert hash_sidecar.exists(), "Expected SHA256 sidecar file for artifact integrity checks."

    with zipfile.ZipFile(artifact_path) as artifact_zip:
        entries = artifact_zip.namelist()

    assert "src/core/game_loop.py" in entries
    assert "config/config.py" in entries
    assert "requirements.txt" in entries
    assert "README.md" in entries
    assert "GAMEPLAY.md" in entries
    assert "build-manifest.txt" in entries

    assert all("__pycache__/" not in entry for entry in entries)
    assert all(not entry.endswith(".pyc") for entry in entries)
    assert all(not entry.endswith("developer-guide.md") for entry in entries)
