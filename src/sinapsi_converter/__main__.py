"""Entry point for the Sinapsi converter.

Supports three usage modes:
1. Drag-and-drop: user drags a CSV file onto the .exe (Windows)
2. CLI argument: `sinapsi-converter path/to/file.csv`
3. Module execution: `python -m sinapsi_converter path/to/file.csv`

Output file is placed next to the input CSV with the naming convention:
  MERC  LETTURE  <building_code>_<date>.xlsx

UI APPROACH NOTES (for future changes):
  Currently uses drag-and-drop / CLI args. To switch to a different UI:
  - Simple GUI: replace this file with a tkinter-based version that uses
    a file dialog and a "Convert" button. All logic stays in parser/sorter/writer.
  - File picker on double-click: replace sys.argv handling with
    tkinter.filedialog.askopenfilename() when no args are provided.
  The rest of the codebase (parser, sorter, writer, models) needs no changes.
"""

from __future__ import annotations

import sys
from pathlib import Path

from .parser import parse_csv
from .sorter import build_pivot_groups, sort_for_raw_sheet
from .writer import write_xlsx


def main() -> None:
    """Run the converter."""
    input_path = _get_input_path()
    if input_path is None:
        _show_usage()
        _wait_if_windows()
        sys.exit(1)

    try:
        _convert(input_path)
    except Exception as exc:
        print(f"Errore: {exc}")
        _wait_if_windows()
        sys.exit(1)


def _convert(input_path: Path) -> None:
    """Run the full conversion pipeline."""
    print(f"Lettura: {input_path.name}")

    report = parse_csv(input_path)
    print(
        f"  {len(report.concentrators)} concentratori, "
        f"{len(report.hca_devices)} dispositivi HCA"
    )

    sorted_hca = sort_for_raw_sheet(report.hca_devices)
    pivot_groups = build_pivot_groups(report.hca_devices)

    output_path = _build_output_path(input_path, report.header.filename)
    write_xlsx(report, sorted_hca, pivot_groups, output_path)

    print(f"Output: {output_path.name}")
    _wait_if_windows()


def _get_input_path() -> Path | None:
    """Get input CSV path from command-line arguments.

    Returns None if no valid path is provided.
    """
    if len(sys.argv) < 2:
        return None

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File non trovato: {path}")
        return None

    if not path.suffix.lower() == ".csv":
        print(f"Il file deve essere un CSV: {path}")
        return None

    return path


def _build_output_path(input_path: Path, report_filename: str) -> Path:
    """Build the output XLSX path.

    Extracts the building code from the report filename and builds the
    output name following the convention:
      MERC  LETTURE  <code>_<date>.xlsx

    The building code is the 4-digit number after "report_" in the filename.
    """
    # Extract building code: "RAW_report_1703_2026-03-02_08-29" -> "1703"
    parts = report_filename.split("_")
    building_code = "0000"
    for i, part in enumerate(parts):
        if part == "report" and i + 1 < len(parts):
            building_code = parts[i + 1]
            break

    # Extract date from report filename
    # "RAW_report_1703_2026-03-02_08-29" -> "2026-03-02"
    report_date = ""
    for part in parts:
        if len(part) == 10 and part[4] == "-" and part[7] == "-":
            report_date = part
            break

    output_name = f"MERC  LETTURE  {building_code}_{report_date}.xlsx"
    return input_path.parent / output_name


def _show_usage() -> None:
    """Print usage instructions."""
    print("Sinapsi Converter - Converte report CSV in XLSX")
    print()
    print("Uso:")
    print("  sinapsi-converter <file.csv>")
    print()
    print("Oppure trascina un file CSV sull'icona del programma.")


def _wait_if_windows() -> None:
    """Pause on Windows so the user can read the console output.

    When running via drag-and-drop, the console window closes immediately
    after the script finishes. This pause gives the user time to read
    any messages.
    """
    if sys.platform == "win32":
        input("\nPremi Invio per chiudere...")


if __name__ == "__main__":
    main()
