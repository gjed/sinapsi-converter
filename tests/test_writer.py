"""Tests for the XLSX writer."""

import tempfile
from pathlib import Path

import openpyxl

from sinapsi_converter.models import (
    ConcentratorDevice,
    HCADevice,
    ParsedReport,
    PivotGroup,
    ReportHeader,
)
from sinapsi_converter.writer import write_xlsx


def _make_report() -> tuple[ParsedReport, list[HCADevice], list[PivotGroup]]:
    """Create minimal test data."""
    header = ReportHeader(
        filename="RAW_report_9999_2026-01-01_09-00",
        report_date="2026-01-01",
        report_time="09:00",
        building_reference="TEST BUILDING",
        description="via test 1",
        total_wired=0,
        total_wireless=2,
        total_not_received=0,
        total_concentrators=1,
    )

    concentrator = ConcentratorDevice(
        count=0,
        primary_address="",
        serial_number="RM0001",
        name="RM0001",
        description="",
        detail="",
        measure_hex="",
        wired_wireless="2-RM0001",
        model_id="SIN.EQRPT868XM",
        readout_date="2026-01-01",
        readout_time="09:00:00",
        communication_status="Ok",
    )

    hca1 = HCADevice(
        count=1,
        primary_address="",
        serial_number="12345",
        name="ROOM A",
        description="1 TENANT INT 1",
        detail="Via Test 1",
        measure_hex="08|UDR",
        wired_wireless="",
        model_id="6251",
        readout_date="2026-01-01",
        readout_time="10:00:00",
        communication_status="Ok",
        hca_current=100.0,
        hca_previous_season=50.0,
        date_1="31/10/2025",
        hca_3=80.0,
        date_2="31/12/2025",
        date_3="31/MM/yy",
        datetime_1="01/01/2026 09:00",
    )

    hca2 = HCADevice(
        count=2,
        primary_address="",
        serial_number="12346",
        name="ROOM B",
        description="1 TENANT INT 1",
        detail="Via Test 1",
        measure_hex="08|UDR",
        wired_wireless="",
        model_id="6251",
        readout_date="2026-01-01",
        readout_time="10:05:00",
        communication_status="Ok",
        hca_current=200.0,
        hca_previous_season=150.0,
        date_1="31/10/2025",
        hca_3=180.0,
        date_2="31/12/2025",
        date_3="31/MM/yy",
        datetime_1="01/01/2026 09:05",
    )

    report = ParsedReport(
        header=header,
        concentrators=[concentrator],
        hca_devices=[hca1, hca2],
    )

    sorted_hca = [hca1, hca2]

    pivot_groups = [
        PivotGroup(
            apartment="1 TENANT INT 1",
            devices=[("ROOM A", 100.0), ("ROOM B", 200.0)],
            total=300.0,
        )
    ]

    return report, sorted_hca, pivot_groups


def test_creates_xlsx_file():
    """Writer should create an XLSX file."""
    report, sorted_hca, pivot_groups = _make_report()

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.xlsx"
        write_xlsx(report, sorted_hca, pivot_groups, out)
        assert out.exists()
        assert out.stat().st_size > 0


def test_has_two_sheets():
    """Output should have PIVOT and raw data sheets."""
    report, sorted_hca, pivot_groups = _make_report()

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.xlsx"
        write_xlsx(report, sorted_hca, pivot_groups, out)
        wb = openpyxl.load_workbook(out)
        assert len(wb.sheetnames) == 2
        assert wb.sheetnames[0] == "PIVOT "


def test_pivot_content():
    """PIVOT sheet should contain correct groups and totals."""
    report, sorted_hca, pivot_groups = _make_report()

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.xlsx"
        write_xlsx(report, sorted_hca, pivot_groups, out)
        wb = openpyxl.load_workbook(out)
        ws = wb["PIVOT "]

        # Row 3: headers
        assert ws.cell(row=3, column=1).value == "Etichette di riga"
        assert ws.cell(row=3, column=2).value == "Somma di HCA"

        # Row 4: apartment total
        assert ws.cell(row=4, column=1).value == "1 TENANT INT 1"
        assert ws.cell(row=4, column=2).value == 300

        # Row 5-6: devices
        assert ws.cell(row=5, column=1).value == "ROOM A"
        assert ws.cell(row=5, column=2).value == 100
        assert ws.cell(row=6, column=1).value == "ROOM B"
        assert ws.cell(row=6, column=2).value == 200

        # Row 7: grand total
        assert ws.cell(row=7, column=1).value == "Totale complessivo"
        assert ws.cell(row=7, column=2).value == 300


def test_raw_sheet_header():
    """Raw sheet should have correct file header."""
    report, sorted_hca, pivot_groups = _make_report()

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.xlsx"
        write_xlsx(report, sorted_hca, pivot_groups, out)
        wb = openpyxl.load_workbook(out)
        ws = wb[wb.sheetnames[1]]

        assert ws.cell(row=1, column=1).value == "Nome file"
        assert ws.cell(row=2, column=1).value == "RAW_report_9999_2026-01-01_09-00"
        assert ws.cell(row=2, column=4).value == "TEST BUILDING"


def test_raw_sheet_sum_formulas():
    """Raw sheet should have SUM formulas at the bottom."""
    report, sorted_hca, pivot_groups = _make_report()

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.xlsx"
        write_xlsx(report, sorted_hca, pivot_groups, out)
        wb = openpyxl.load_workbook(out)
        ws = wb[wb.sheetnames[1]]

        # Find the last row with data
        last_row = ws.max_row
        # Column M (13) should have a SUM formula
        val = ws.cell(row=last_row, column=13).value
        assert val is not None and "SUM" in str(val)
