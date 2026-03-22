# Project Context

## Purpose

Convert Sinapsi RAW report CSV files into formatted XLSX workbooks with a PIVOT summary sheet. The tool is used by building administrators in Italy to process heat cost allocator (HCA) readout data from the Sinapsi telemetry platform.

## Tech Stack

- Python 3.10+ (minimum supported version)
- openpyxl — XLSX generation
- tkinter — GUI (stdlib, no extra deps)
- pytest + pytest-cov — testing
- PyInstaller — Windows .exe packaging
- GitHub Actions — CI (test matrix 3.10–3.13) and Release (tag-triggered)

## Project Conventions

### Code Style

- Modules under `src/sinapsi_converter/`; one concern per file
- Type hints everywhere (`from __future__ import annotations`)
- Dataclasses for models (no Pydantic, no attrs)
- User-facing text in Italian
- Font for XLSX output: Aptos Narrow (all cells)

### Architecture Patterns

- Pipeline: CSV → parse → sort/group → write XLSX
- Parser, sorter, writer are stateless functions (no class hierarchy)
- Styles module provides reusable openpyxl formatting helpers
- GUI and CLI share the same conversion pipeline

### Testing Strategy

- pytest with fixtures in `tests/fixtures/`
- Anonymized test CSV (`RAW_report_9999_2026-01-15_10-00.csv`) — never use real client data
- Tests cover parser (8), sorter (8), writer (15+) — 33 total
- Coverage reported in CI

### Git Workflow

- Conventional Commits: `<type>(<scope>): <description>`
- Single `main` branch; tags `v*` trigger release builds
- CODEOWNERS: `@gjed`
- `assets/` in `.gitignore` (confidential data purged from history)

## Domain Context

- **Sinapsi**: Italian building telemetry platform that exports CSV reports
- **HCA**: Heat Cost Allocator — device measuring radiator usage per apartment
- **Concentrators**: Gateway devices that aggregate HCA readings (no HCA data themselves)
- **CSV format**: Semicolon-delimited, BOM-encoded, comma decimal separators (e.g. `118,00`)
- **PIVOT sheet**: Summary grouped by apartment showing per-device HCA totals
- **RAW sheet**: Full device dump with file header, concentrator blocks, and HCA data table

## Important Constraints

- Output must match the formatting conventions expected by the end users (specific column headers in Italian, sheet naming with "MERC " prefix)
- Serial numbers must be written as integers when purely numeric
- Excel sheet names are limited to 31 characters
- PyInstaller `--onefile` requires `scripts/pyinstaller_entry.py` with absolute imports (relative imports break at runtime)
- Windows exe needs catch-all exception handler with pause before exit

## External Dependencies

- Sinapsi platform (CSV export is the input; no API integration)
- GitHub Actions for CI/CD
- PyPI packages: openpyxl only (runtime)
