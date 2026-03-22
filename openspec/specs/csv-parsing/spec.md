# CSV Parsing

## Purpose

Parse Sinapsi RAW report CSV files into structured data models. Handles BOM encoding, semicolon delimiters, comma decimal separators, and two device types (concentrators and HCA devices).

## Requirements

### Requirement: BOM-Encoded Semicolon-Delimited CSV

The parser SHALL read CSV files encoded as UTF-8 with BOM, using semicolons as field delimiters.

#### Scenario: Standard Sinapsi CSV file

- **WHEN** a CSV file exported from Sinapsi is provided
- **THEN** the file is read with `utf-8-sig` encoding
- **AND** fields are split on semicolons

#### Scenario: File too short

- **WHEN** a CSV file has fewer than 4 lines
- **THEN** a `ValueError` is raised with a descriptive message

### Requirement: File Header Parsing

The parser SHALL extract report metadata from the first two rows into a `ReportHeader` model with fields: filename, report_date, report_time, building_reference, description, total_wired, total_wireless, total_not_received, total_concentrators.

#### Scenario: Valid header rows

- **WHEN** the first two rows contain 9 semicolon-separated values
- **THEN** a `ReportHeader` is populated with the correct values
- **AND** numeric fields are converted to integers (0 for empty/invalid)

### Requirement: Device Block Parsing

The parser SHALL recognize repeating 3-row device blocks (header row starting with `count;`, data row, blank row) and parse them into device objects.

#### Scenario: Concentrator device (12 columns)

- **WHEN** a data row has 12 meaningful fields and no HCA data beyond column 12
- **THEN** a `ConcentratorDevice` is created with all 12 fields populated

#### Scenario: HCA device (19 columns)

- **WHEN** a data row has non-empty fields beyond column 12
- **THEN** an `HCADevice` is created with all 19 fields populated
- **AND** the `hca_current` field (column M / index 12) contains the "Attuale" reading

### Requirement: Comma Decimal Conversion

The parser SHALL convert comma-separated decimal numbers (e.g. `118,00`) to Python floats.

#### Scenario: Comma decimal value

- **WHEN** a numeric field contains `118,00`
- **THEN** it is converted to `118.0`

#### Scenario: Empty numeric field

- **WHEN** a numeric field is empty or whitespace
- **THEN** it returns `0` (int) or `0.0` (float)

### Requirement: Parsed Report Assembly

The parser SHALL return a `ParsedReport` containing the header, a list of concentrators, and a list of HCA devices.

#### Scenario: Complete report

- **WHEN** a valid CSV is parsed
- **THEN** the `ParsedReport` contains a populated `ReportHeader`, zero or more `ConcentratorDevice` entries, and zero or more `HCADevice` entries
