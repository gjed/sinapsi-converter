# 🔄 sinapsi-converter

[![CI](https://github.com/gjed/sinapsi-converter/actions/workflows/ci.yml/badge.svg)](https://github.com/gjed/sinapsi-converter/actions/workflows/ci.yml) [![codecov](https://codecov.io/gh/gjed/sinapsi-converter/branch/main/graph/badge.svg)](https://codecov.io/gh/gjed/sinapsi-converter) [![GitHub Release](https://img.shields.io/github/v/release/gjed/sinapsi-converter)](https://github.com/gjed/sinapsi-converter/releases/latest) [![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://github.com/gjed/sinapsi-converter) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)

[Sinapsi](https://www.sinapsitech.it/) is an Italian company that manufactures **thermal energy meters (heat cost allocators)** used in condominiums to measure individual apartment heating consumption and fairly split shared heating expenses.

This tool converts **Sinapsi RAW report** CSV files into professionally formatted XLSX workbooks with a pivot summary sheet.

> [Sinapsi](https://www.sinapsitech.it/) è un'azienda italiana che produce **contatori di energia termica (ripartitori di calore)** utilizzati nei condomini per misurare il consumo di riscaldamento dei singoli appartamenti e suddividere equamente le spese di riscaldamento.
>
> Questo strumento converte i file CSV dei **report RAW Sinapsi** in cartelle di lavoro XLSX formattate professionalmente con un foglio di riepilogo pivot.

## ✨ Features / Funzionalità

- **Two-sheet output** — PIVOT summary with apartment totals + full raw data sheet
  > **Output a due fogli** — riepilogo PIVOT con i totali per appartamento + foglio dati grezzi completo
- **Professional formatting** — dark headers, alternating rows, auto-fit columns, freeze panes
  > **Formattazione professionale** — intestazioni scure, righe alternate, colonne adattate automaticamente, riquadri bloccati
- **Auto-filter** — dropdown filters on every column of the HCA data table
  > **Filtro automatico** — filtri a tendina su ogni colonna della tabella dati HCA
- **Drag-and-drop** — Windows users drop a CSV onto the `.exe`, done
  > **Trascina e rilascia** — gli utenti Windows trascinano un CSV sull'`.exe`, fatto
- **Cross-platform** — runs on Linux and macOS for development, Windows for end users
  > **Multipiattaforma** — funziona su Linux e macOS per lo sviluppo, Windows per gli utenti finali

## Quick Start / Avvio rapido

```bash
pip install -e .
python -m sinapsi_converter path/to/RAW_report.csv
```

Output appears next to the input file as `MERC  LETTURE  <code>_<date>.xlsx`.

> L'output viene creato nella stessa cartella del file di input come `MERC  LETTURE  <code>_<data>.xlsx`.

## Windows (.exe)

Build a standalone executable for non-technical users:

Crea un eseguibile standalone per utenti non tecnici:

```bash
pip install -e ".[dev]"
pyinstaller --onefile --paths src --name sinapsi-converter scripts/pyinstaller_entry.py
```

The `.exe` lands in `dist/`. Users drag a CSV onto it — the XLSX appears next to the CSV.

L'`.exe` viene creato in `dist/`. Gli utenti trascinano un CSV sull'eseguibile — il file XLSX appare accanto al CSV.

## Development

```bash
pip install -e ".[dev]"
pytest
```

### Project Structure

```text
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
