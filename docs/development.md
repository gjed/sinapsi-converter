# Development Guide

## Setup

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run the converter (use any Sinapsi RAW report CSV)
python -m sinapsi_converter path/to/RAW_report.csv
```

## Project Structure

```
src/sinapsi_converter/
  __init__.py          # Package marker
  __main__.py          # Entry point: CLI args, drag-and-drop, error display
  models.py            # Data classes (no I/O, no logic)
  parser.py            # CSV parsing: raw text -> data models
  sorter.py            # Sorting/grouping for both output sheets
  styles.py            # XLSX formatting: fonts, fills, borders, row heights
  writer.py            # XLSX generation with openpyxl
tests/
  fixtures/            # Anonymized test CSV
  test_parser.py       # CSV parsing tests
  test_sorter.py       # Sorting/grouping tests
  test_writer.py       # XLSX output tests (content + formatting)
```

### Module Responsibilities

- **models.py**: Pure data structures. `ReportHeader`, `ConcentratorDevice`,
  `HCADevice`, `ParsedReport`, `PivotGroup`. No I/O, no dependencies.

- **parser.py**: Reads raw Sinapsi CSV (semicolon-delimited, repeating
  header/blank/data blocks). Returns `ParsedReport`. Handles BOM, comma
  decimals, blank rows.

- **sorter.py**: Takes device list, produces sorted structures for both
  sheets. Raw sheet: group by apartment, sort by count. Pivot: alphabetical
  grouping with subtotals, deduplicates devices with same name.

- **styles.py**: Reusable XLSX formatting. Aptos Narrow font, dark/accent
  fills, alternating rows, auto-fit columns, freeze panes, row heights.
  Called by `writer.py` — no direct I/O.

- **writer.py**: Takes sorted data, builds XLSX with openpyxl. Two sheets:
  raw data (with SUM formulas, auto-filter) and PIVOT summary.

- **__main__.py**: Wires everything together. Handles CLI args and
  drag-and-drop. This is the ONLY module that changes when swapping UI
  approaches.

## Building the Windows .exe

```bash
pip install pyinstaller
pyinstaller --onefile --paths src --name sinapsi-converter scripts/pyinstaller_entry.py
```

The .exe will be in `dist/sinapsi-converter.exe`.

## UI Approach

Currently: **drag-and-drop / CLI argument**.

The UI is isolated in `__main__.py`. To change it:

| Approach | What to change |
|----------|---------------|
| **Drag-and-drop** (current) | User drags CSV onto .exe. `sys.argv[1]` gets the path. |
| **File picker dialog** | Replace `_get_input_path()` with `tkinter.filedialog.askopenfilename()`. Triggered when no args provided. |
| **Simple GUI** | Replace `__main__.py` entirely with a tkinter window: Browse button + Convert button. Import `parser`, `sorter`, `writer` as-is. |
| **Web UI** | Add a Flask/FastAPI wrapper. Import the same modules. |

No other module needs changes for any UI swap.

## CSV Format Reference

The Sinapsi RAW_report CSV has this structure:

```
Row 1: File header labels (;-separated)
Row 2: File header values
Row 3: blank
Row 4+: Repeating blocks of 3 rows per device:
  - Column header row (starts with "count;")
  - Data row
  - Blank row
```

Devices come in two types:
- **Concentrators**: 12 columns, no HCA data (serial starts with "RM")
- **HCA devices**: 19 columns, includes heat cost allocator readings

HCA columns 13-19: HCA current, HCA prev season, date, HCA, date, date, datetime.
