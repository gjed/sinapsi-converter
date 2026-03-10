# 🔄 sinapsi-converter

Converts **Sinapsi RAW report** CSV files into professionally formatted XLSX workbooks with a pivot summary sheet.

[![CI](https://github.com/gjed/sinapsi-converter/actions/workflows/ci.yml/badge.svg)](https://github.com/gjed/sinapsi-converter/actions/workflows/ci.yml)

## ✨ Features

- **Two-sheet output** — PIVOT summary with apartment totals + full raw data sheet
- **Professional formatting** — dark headers, alternating rows, auto-fit columns, freeze panes
- **Auto-filter** — dropdown filters on every column of the HCA data table
- **Drag-and-drop** — Windows users drop a CSV onto the `.exe`, done
- **Cross-platform** — runs on Linux and macOS for development, Windows for end users

## Quick Start

```bash
pip install -e .
python -m sinapsi_converter path/to/RAW_report.csv
```

Output appears next to the input file as `MERC  LETTURE  <code>_<date>.xlsx`.

## Windows (.exe)

Build a standalone executable for non-technical users:

```bash
pip install -e ".[dev]"
pyinstaller --onefile --name sinapsi-converter src/sinapsi_converter/__main__.py
```

The `.exe` lands in `dist/`. Users drag a CSV onto it — the XLSX appears next to the CSV.

## Development

```bash
pip install -e ".[dev]"
pytest
```

### Project Structure

```
src/sinapsi_converter/
  __main__.py    → CLI entry point (drag-and-drop)
  models.py      → Data classes (no I/O)
  parser.py      → CSV parsing (BOM, semicolons, comma decimals)
  sorter.py      → Sorting + pivot grouping with dedup
  styles.py      → XLSX formatting (fonts, fills, borders)
  writer.py      → XLSX generation (two sheets, formulas, filters)
tests/
  fixtures/      → Anonymized test CSV
  test_parser.py → 8 tests
  test_sorter.py → 6 tests
  test_writer.py → 13 tests (content + formatting)
```

See [docs/development.md](docs/development.md) for module responsibilities, UI swap guide, and CSV format reference.

## 📚 Documentation

- [docs/uso.md](docs/uso.md) — Guida utente (italiano)
- [docs/development.md](docs/development.md) — Developer guide
