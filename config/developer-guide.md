# Developer Guide

## Purpose
`config/` contains centralized, importable configuration for gameplay and economy values.

## Files
- `config.py`: frozen dataclass-based configuration models and exported singleton config objects.

## How To Use
- Import `GAME_CONFIG` for core player/runtime constants.
- Import `ECONOMY_CONFIG` for weapon price progression values.
- Prefer updating values here rather than scattering literals across systems.

## Current Economy Curve
- `shotgun_price = 250`: early-upgrade tier.
- `assault_rifle_price = 800`: mid-tier target after several bot waves.
- `rpg_price = 2000`: endgame tier that gates the glitch-ending trigger.
