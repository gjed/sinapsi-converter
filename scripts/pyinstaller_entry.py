"""PyInstaller entry point.

Thin wrapper that uses absolute imports (required for --onefile builds)
and shows errors via messagebox on Windows (no console with --noconsole).
"""

import sys

if __name__ == "__main__":
    try:
        from sinapsi_converter.__main__ import main

        main()
    except Exception:
        import traceback

        msg = traceback.format_exc()
        # With --noconsole on Windows there is no console to print to,
        # so show a messagebox instead.
        try:
            import tkinter as tk
            from tkinter import messagebox

            root = tk.Tk()
            root.withdraw()  # hide the empty root window
            messagebox.showerror("Sinapsi Converter", msg)
            root.destroy()
        except Exception:
            # tkinter itself failed — last resort
            print(msg, file=sys.stderr)
        sys.exit(1)
