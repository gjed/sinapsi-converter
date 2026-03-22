# Dual-Mode User Interface

## Purpose

Support two usage modes: headless CLI/drag-and-drop when arguments are provided, and a tkinter GUI when run without arguments. All user-facing text is in Italian.

## Requirements

### Requirement: CLI and Drag-and-Drop Mode

The program SHALL accept a CSV file path as a command-line argument and run the conversion headlessly. This supports both direct CLI usage and Windows drag-and-drop onto the .exe.

#### Scenario: CLI with valid CSV

- **WHEN** the program is invoked with a path to a valid CSV file
- **THEN** the conversion runs without GUI
- **AND** status messages are printed to stdout in Italian

#### Scenario: File not found

- **WHEN** the provided path does not exist
- **THEN** an error message is printed in Italian
- **AND** the program exits with code 1

#### Scenario: Non-CSV file

- **WHEN** the provided file does not have a `.csv` extension
- **THEN** an error message is printed in Italian
- **AND** the program exits with code 1

### Requirement: GUI Mode

The program SHALL launch a tkinter GUI window when run without arguments (e.g. double-clicking the .exe on Windows).

#### Scenario: No arguments provided

- **WHEN** the program is started with no command-line arguments
- **THEN** a tkinter window opens with title "Sinapsi Converter" at size 500x200
- **AND** the window is not resizable

### Requirement: GUI File Picker

The GUI SHALL provide a file browse button that opens a file dialog filtered to CSV files.

#### Scenario: Browse for file

- **WHEN** the user clicks "Sfoglia..."
- **THEN** a file dialog opens with filter for `*.csv` files
- **AND** the selected path is displayed in a read-only text field

### Requirement: GUI Convert Button

The GUI SHALL provide a "Converti" button that runs the conversion pipeline on the selected file.

#### Scenario: Successful conversion

- **WHEN** the user selects a valid CSV and clicks "Converti"
- **THEN** the status bar shows "Conversione in corso..."
- **AND** on completion, a success dialog shows the output filename
- **AND** the status bar shows "Completato: <filename>"

#### Scenario: No file selected

- **WHEN** the user clicks "Converti" without selecting a file
- **THEN** a warning dialog says "Seleziona un file CSV."

#### Scenario: Conversion error

- **WHEN** the conversion fails with an exception
- **THEN** an error dialog shows the exception message
- **AND** the status bar shows "Errore durante la conversione."

### Requirement: Windows Console Pause

On Windows, the CLI mode SHALL pause with "Premi Invio per chiudere..." before exiting, so drag-and-drop users can read output before the console window closes.

#### Scenario: Windows drag-and-drop

- **WHEN** running on Windows (`sys.platform == "win32"`) in CLI mode
- **THEN** the program waits for Enter before exiting

#### Scenario: Non-Windows platform

- **WHEN** running on Linux or macOS
- **THEN** no pause is added; the program exits normally

### Requirement: Italian User-Facing Text

All user-facing text (labels, messages, errors) SHALL be in Italian.

#### Scenario: GUI labels

- **WHEN** the GUI is displayed
- **THEN** labels read "File CSV:", button reads "Sfoglia..." and "Converti", status reads "In attesa..."
