"""Entry point for the Sinapsi converter.

Supports two usage modes — both go through the GUI:
1. Drag-and-drop / CLI argument: launches GUI with file pre-filled and
   auto-converts immediately.
2. Double-click (no arguments): launches GUI for manual file selection.

Output file is placed next to the input CSV with the naming convention:
  MERC  LETTURE  <building_code>_<date>.xlsx
"""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> None:
    """Run the converter.

    With arguments: launch GUI with pre-filled path and auto-convert.
    Without arguments: launch the GUI window for manual file selection.
    """
    from .gui import launch_gui

    if len(sys.argv) >= 2:
        launch_gui(initial_path=sys.argv[1])
    else:
        launch_gui()


def _build_output_path(input_path: Path, report_filename: str) -> Path:
    """Build the output XLSX path.

    Extracts the building code and date from the **input file name** (not the
    CSV-internal report_filename) and builds the output name following the
    convention:
      MERC  LETTURE  <code>_<date>.xlsx

    The building code is the 4-digit number after "report_" in the filename.
    """
    # Use the actual input filename, not the CSV-internal one
    parts = input_path.stem.split("_")
    building_code = "0000"
    for i, part in enumerate(parts):
        if part == "report" and i + 1 < len(parts):
            building_code = parts[i + 1]
            break

    # Extract date from input filename
    # "RAW_report_1703_2026-03-02_08-29" -> "2026-03-02"
    report_date = ""
    for part in parts:
        if len(part) == 10 and part[4] == "-" and part[7] == "-":
            report_date = part
            break

    output_name = f"MERC  LETTURE  {building_code}_{report_date}.xlsx"
    return input_path.parent / output_name


if __name__ == "__main__":
    main()
