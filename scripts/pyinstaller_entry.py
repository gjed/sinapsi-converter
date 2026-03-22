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
            from tkinter import messagebox

            messagebox.showerror("Sinapsi Converter", msg)
        except Exception:
            # tkinter itself failed — last resort
            print(msg, file=sys.stderr)
        sys.exit(1)
