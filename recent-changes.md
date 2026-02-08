# Recent Changes

## 2026-02-08
- Selected and documented the tech stack as **Python 3.11+ with Ursina 6.1.2** in `developer-guide.md`.
- Created initial project structure directories: `src/`, `assets/`, `config/`, and `tests/`.
- Added placeholder keep files for empty directories: `src/.gitkeep`, `assets/.gitkeep`, and `tests/.gitkeep`.
- Added `requirements.txt` with the pinned core dependency: `ursina==6.1.2`.
- Implemented base configuration module at `config/config.py` with frozen dataclasses for game and economy constants (`GAME_CONFIG`, `ECONOMY_CONFIG`).
- Added folder-level documentation in `config/developer-guide.md` and root architecture documentation in `developer-guide.md`.

## 2026-02-08 (Test Update)
- Added `pytest` to `requirements.txt` as the chosen testing framework.
- Created `tests/developer-guide.md` to document testing strategy.
- Created `tests/test_config.py` to verify configuration constants and immutability.
- Added `config/__init__.py` to establish the `config` folder as a Python package.

