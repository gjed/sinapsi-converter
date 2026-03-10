# sinapsi-converter

Converts Sinapsi RAW report CSV files into XLSX workbooks with a pivot summary sheet.

## Quick Start

```bash
pip install -e .
python -m sinapsi_converter path/to/RAW_report.csv
```

Output appears next to the input file as `MERC  LETTURE  <code>_<date>.xlsx`.

## Windows

Build a standalone `.exe` that non-technical users can use via drag-and-drop:

```bash
pip install -e ".[dev]"
pyinstaller --onefile --name sinapsi-converter src/sinapsi_converter/__main__.py
```

The `.exe` will be in `dist/`. Users drag a CSV onto it; the XLSX appears next to the CSV.

## Development

```bash
pip install -e ".[dev]"
pytest
```

See [docs/development.md](docs/development.md) for project structure, module responsibilities, and how to swap the UI approach.

## Documentation

- [docs/uso.md](docs/uso.md) — User guide (Italian)
- [docs/development.md](docs/development.md) — Developer guide
