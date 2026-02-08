# Developer Guide

## Purpose
`config/` contains centralized, importable configuration for gameplay and economy values.

## Files
- `config.py`: frozen dataclass-based configuration models and exported singleton config objects.

## How To Use
- Import `GAME_CONFIG` for core player/runtime constants.
- Import `ECONOMY_CONFIG` for weapon price progression values.
- Prefer updating values here rather than scattering literals across systems.
