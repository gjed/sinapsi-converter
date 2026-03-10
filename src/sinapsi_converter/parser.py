"""Parse Sinapsi RAW report CSV files.

The CSV format uses semicolons as delimiters and has a repeating structure:
- Rows 1-2: File header (metadata about the report)
- Row 3: blank
- Then repeating blocks of 3 rows per device:
    - Header row (column names)
    - Data row (device values)
    - Blank row

Devices come in two types:
- Concentrators/gateways: 12 columns, no HCA data
- HCA devices: 19 columns, with heat cost allocator readings
"""

from __future__ import annotations

from pathlib import Path

from .models import (
    ConcentratorDevice,
    HCADevice,
    ParsedReport,
    ReportHeader,
)


def parse_csv(path: Path) -> ParsedReport:
    """Parse a Sinapsi RAW report CSV file.

    Args:
        path: Path to the CSV file.

    Returns:
        ParsedReport with header, concentrators, and HCA devices.

    Raises:
        ValueError: If the file format is not recognized.
    """
    text = path.read_text(encoding="utf-8-sig")
    lines = text.strip().split("\n")

    if len(lines) < 4:
        msg = f"File too short ({len(lines)} lines), expected at least 4"
        raise ValueError(msg)

    header = _parse_header(lines[0], lines[1])
    concentrators: list[ConcentratorDevice] = []
    hca_devices: list[HCADevice] = []

    i = 3  # Skip to first device block (after header rows + blank line)
    while i < len(lines):
        line = lines[i].strip()

        # Skip blank lines
        if not line or line.replace(";", "") == "":
            i += 1
            continue

        # Check if this is a header row (starts with "count;")
        if line.startswith("count;"):
            # Next non-blank line should be the data row
            i += 1
            if i >= len(lines):
                break

            data_line = lines[i].strip()
            if not data_line or data_line.replace(";", "") == "":
                i += 1
                continue

            fields = data_line.split(";")
            device = _parse_device(fields)
            if isinstance(device, ConcentratorDevice):
                concentrators.append(device)
            else:
                hca_devices.append(device)

            i += 1
            continue

        i += 1

    return ParsedReport(
        header=header,
        concentrators=concentrators,
        hca_devices=hca_devices,
    )


def _parse_header(header_line: str, values_line: str) -> ReportHeader:
    """Parse the two header rows into a ReportHeader."""
    values = values_line.split(";")

    return ReportHeader(
        filename=values[0],
        report_date=values[1],
        report_time=values[2],
        building_reference=values[3],
        description=values[4],
        total_wired=_safe_int(values[5]),
        total_wireless=_safe_int(values[6]),
        total_not_received=_safe_int(values[7]),
        total_concentrators=_safe_int(values[8]),
    )


def _parse_device(
    fields: list[str],
) -> ConcentratorDevice | HCADevice:
    """Parse a device data row into the appropriate device type.

    Concentrators have 12 meaningful fields and no HCA data.
    HCA devices have 19 fields including HCA readings.
    """
    # Check if this row has HCA data (fields beyond index 12 are non-empty)
    has_hca = len(fields) > 12 and any(f.strip() for f in fields[12:])

    if has_hca:
        return HCADevice(
            count=_safe_int(fields[0]),
            primary_address=fields[1],
            serial_number=fields[2],
            name=fields[3],
            description=fields[4],
            detail=fields[5],
            measure_hex=fields[6],
            wired_wireless=fields[7],
            model_id=fields[8].strip(),
            readout_date=fields[9],
            readout_time=fields[10],
            communication_status=fields[11],
            hca_current=_safe_float(fields[12]),
            hca_previous_season=_safe_float(fields[13]),
            date_1=fields[14],
            hca_3=_safe_float(fields[15]),
            date_2=fields[16],
            date_3=fields[17] if len(fields) > 17 else "",
            datetime_1=fields[18] if len(fields) > 18 else "",
        )

    return ConcentratorDevice(
        count=_safe_int(fields[0]),
        primary_address=fields[1],
        serial_number=fields[2],
        name=fields[3],
        description=fields[4],
        detail=fields[5],
        measure_hex=fields[6],
        wired_wireless=fields[7],
        model_id=fields[8].strip(),
        readout_date=fields[9],
        readout_time=fields[10],
        communication_status=fields[11],
    )


def _safe_int(value: str) -> int:
    """Convert a string to int, returning 0 for empty/invalid values."""
    value = value.strip()
    if not value:
        return 0
    try:
        return int(value)
    except ValueError:
        return 0


def _safe_float(value: str) -> float:
    """Convert a string to float, handling comma decimals.

    Sinapsi CSV uses comma as decimal separator (e.g. "118,00").
    """
    value = value.strip()
    if not value:
        return 0.0
    try:
        return float(value.replace(",", "."))
    except ValueError:
        return 0.0
