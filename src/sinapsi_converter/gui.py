"""Simple tkinter GUI for the Sinapsi converter.

Launched when the program is run without arguments (double-click the .exe).
Provides a file picker and convert button — same pipeline as CLI mode.
"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from .parser import parse_csv
from .sorter import build_pivot_groups, sort_for_raw_sheet
from .writer import write_xlsx

_WINDOW_TITLE = "Sinapsi Converter"
_WINDOW_SIZE = "500x200"


def launch_gui() -> None:
    """Create and run the main GUI window."""
    root = tk.Tk()
    root.title(_WINDOW_TITLE)
    root.geometry(_WINDOW_SIZE)
    root.resizable(False, False)

    _build_ui(root)
    root.mainloop()


def _build_ui(root: tk.Tk) -> None:
    """Build the GUI widgets."""
    # -- File selection row --
    frame_file = tk.Frame(root, padx=16, pady=12)
    frame_file.pack(fill="x")

    tk.Label(frame_file, text="File CSV:", anchor="w").pack(fill="x")

    frame_entry = tk.Frame(frame_file)
    frame_entry.pack(fill="x", pady=(4, 0))

    file_var = tk.StringVar()
    entry = tk.Entry(frame_entry, textvariable=file_var, state="readonly")
    entry.pack(side="left", fill="x", expand=True)

    def browse() -> None:
        path = filedialog.askopenfilename(
            title="Seleziona file CSV",
            filetypes=[("File CSV", "*.csv"), ("Tutti i file", "*.*")],
        )
        if path:
            file_var.set(path)

    tk.Button(frame_entry, text="Sfoglia...", command=browse).pack(
        side="right", padx=(8, 0)
    )

    # -- Convert button --
    frame_btn = tk.Frame(root, padx=16)
    frame_btn.pack()

    status_var = tk.StringVar(value="In attesa...")

    def convert() -> None:
        csv_path = file_var.get()
        if not csv_path:
            messagebox.showwarning(_WINDOW_TITLE, "Seleziona un file CSV.")
            return

        input_path = Path(csv_path)
        if not input_path.exists():
            messagebox.showerror(_WINDOW_TITLE, f"File non trovato:\n{input_path}")
            return

        status_var.set("Conversione in corso...")
        root.update_idletasks()

        try:
            output_path = _run_conversion(input_path)
            status_var.set(f"Completato: {output_path.name}")
            messagebox.showinfo(_WINDOW_TITLE, f"File creato:\n{output_path}")
        except Exception as exc:
            status_var.set("Errore durante la conversione.")
            messagebox.showerror(_WINDOW_TITLE, f"Errore:\n{exc}")

    tk.Button(frame_btn, text="Converti", command=convert, width=20).pack(pady=8)

    # -- Status bar --
    frame_status = tk.Frame(root, padx=16, pady=(0, 12))
    frame_status.pack(fill="x", side="bottom")

    tk.Label(frame_status, textvariable=status_var, anchor="w", fg="gray").pack(
        fill="x"
    )


def _run_conversion(input_path: Path) -> Path:
    """Run the full conversion pipeline. Returns the output path."""
    report = parse_csv(input_path)
    sorted_hca = sort_for_raw_sheet(report.hca_devices)
    pivot_groups = build_pivot_groups(report.hca_devices)
    output_path = _build_output_path(input_path, report.header.filename)
    write_xlsx(report, sorted_hca, pivot_groups, output_path)
    return output_path


def _build_output_path(input_path: Path, report_filename: str) -> Path:
    """Build the output XLSX path from the report filename."""
    parts = report_filename.split("_")

    building_code = "0000"
    for i, part in enumerate(parts):
        if part == "report" and i + 1 < len(parts):
            building_code = parts[i + 1]
            break

    report_date = ""
    for part in parts:
        if len(part) == 10 and part[4] == "-" and part[7] == "-":
            report_date = part
            break

    output_name = f"MERC  LETTURE  {building_code}_{report_date}.xlsx"
    return input_path.parent / output_name
