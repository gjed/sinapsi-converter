"""PyInstaller entry point.

Thin wrapper that uses absolute imports (required for --onefile builds)
and ensures the console stays open on Windows if anything goes wrong.
"""

import sys

if __name__ == "__main__":
    try:
        from sinapsi_converter.__main__ import main

        main()
    except Exception:
        import traceback

        traceback.print_exc()
        if sys.platform == "win32":
            input("\nPremi Invio per chiudere...")
        sys.exit(1)
