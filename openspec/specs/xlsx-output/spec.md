# XLSX Output

## Purpose

Generate a formatted XLSX workbook with two sheets: a PIVOT summary grouped by apartment with HCA totals, and a RAW data sheet with file header, concentrators, and sorted HCA device data. Uses Aptos Narrow font and professional formatting.

## Requirements

### Requirement: Two-Sheet Workbook

The writer SHALL produce an XLSX workbook with exactly two sheets: a PIVOT sheet (first/active) and a RAW data sheet.

#### Scenario: Standard conversion

- **WHEN** a parsed report with HCA devices is written
- **THEN** the workbook contains exactly two sheets
- **AND** the PIVOT sheet is the active sheet (appears first)

### Requirement: PIVOT Sheet Structure

The PIVOT sheet SHALL be titled "PIVOT " and contain: header row at row 3 with "Etichette di riga" and "Somma di HCA", detail section headers, apartment subtotal rows, individual device rows, and a grand total row.

#### Scenario: Pivot with multiple apartments

- **WHEN** pivot groups span multiple apartments
- **THEN** each apartment has a subtotal row followed by individual device rows
- **AND** apartment totals are displayed as integers
- **AND** a "Totale complessivo" row at the bottom shows the grand total

#### Scenario: Detail section headers

- **WHEN** the `device_detail` value changes between consecutive groups
- **THEN** a detail section header row is emitted

### Requirement: RAW Sheet Structure

The RAW sheet SHALL be named with "MERC " prefix followed by the report filename, truncated to 31 characters. It SHALL contain: file header (rows 1-2), blank row, concentrator blocks (each with header + data + blank), separator, HCA sub-headers, HCA column headers, sorted HCA data rows, and SUM formula row.

#### Scenario: Sheet name truncation

- **WHEN** the report filename combined with "MERC " prefix exceeds 31 characters
- **THEN** the sheet name is truncated to exactly 31 characters

#### Scenario: Concentrator blocks

- **WHEN** the report contains concentrator devices
- **THEN** each concentrator is written as a header row + data row + blank row

#### Scenario: HCA data section

- **WHEN** HCA devices are present
- **THEN** "Attuale" and "Es.Prec" sub-headers appear above the HCA table
- **AND** a full column header row precedes the data rows
- **AND** data rows follow the sorting order from the sorter module

### Requirement: SUM Formulas

The writer SHALL append a row with Excel SUM formulas for columns M (HCA current), N (HCA previous season), and P (HCA 3) below the last HCA data row.

#### Scenario: Formula row

- **WHEN** HCA data rows span from row X to row Y
- **THEN** cells M, N, and P in the formula row contain `=SUM(M{X}:M{Y})`, `=SUM(N{X}:N{Y})`, `=SUM(P{X}:P{Y})`

### Requirement: Auto-Filter and Sort State

The writer SHALL apply auto-filter on the HCA table from the header row through the last data row, with sort state configured for device_detail (col F) descending and device_description (col E) ascending.

#### Scenario: Auto-filter applied

- **WHEN** the RAW sheet is written
- **THEN** the auto-filter range covers columns A through S from the HCA header row to the last HCA data row
- **AND** the sort state has two conditions: column F descending, column E ascending

### Requirement: Aptos Narrow Font

All cells in the workbook SHALL use the Aptos Narrow font.

#### Scenario: Font consistency

- **WHEN** any cell is styled
- **THEN** the font name is "Aptos Narrow"

### Requirement: Professional Formatting

The writer SHALL apply: dark/accent header fills, alternating row shading on data rows, auto-fit column widths, freeze panes below header rows, and taller header rows.

#### Scenario: Header row styling

- **WHEN** a header row is written
- **THEN** it has a dark fill color, white bold font, and increased row height

#### Scenario: Alternating row shading

- **WHEN** data rows are written
- **THEN** odd and even rows have visually distinct background colors

#### Scenario: Freeze panes

- **WHEN** the sheet is written
- **THEN** panes are frozen below the column header row so headers remain visible on scroll

### Requirement: Serial Numbers as Integers

The writer SHALL convert purely numeric serial numbers and model IDs to integers before writing to cells.

#### Scenario: Numeric serial number

- **WHEN** a serial number is `"12345678"`
- **THEN** it is written as integer `12345678`

#### Scenario: Non-numeric serial number

- **WHEN** a serial number contains non-digit characters
- **THEN** it is written as a string

### Requirement: Output File Naming

The output XLSX file SHALL be named `MERC  LETTURE  <building_code>_<date>.xlsx` and placed in the same directory as the input CSV.

#### Scenario: Output file path

- **WHEN** the input is `RAW_report_1703_2026-03-02_08-29.csv`
- **THEN** the output is `MERC  LETTURE  1703_2026-03-02.xlsx` in the same directory
