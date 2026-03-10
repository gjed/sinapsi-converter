"""Tests for the CSV parser."""

from pathlib import Path

import pytest

from sinapsi_converter.parser import parse_csv

FIXTURES = Path(__file__).parent / "fixtures"
SAMPLE_CSV = FIXTURES / "RAW_report_9999_2026-01-15_10-00.csv"


@pytest.fixture
def report():
    """Parse the sample CSV once for all tests."""
    return parse_csv(SAMPLE_CSV)


def test_header_parsed(report):
    """Report header should contain correct metadata."""
    h = report.header
    assert h.filename == "RAW_report_9999_2026-01-15_10-00"
    assert h.report_date == "2026-01-15"
    assert h.report_time == "10:00"
    assert h.building_reference == "CONDOMINIO GARIBALDI"
    assert h.total_wireless == 10
    assert h.total_concentrators == 2


def test_concentrators_count(report):
    """Should parse exactly 2 concentrators."""
    assert len(report.concentrators) == 2


def test_concentrator_fields(report):
    """Concentrator devices should have correct fields."""
    conc = report.concentrators[0]
    assert conc.count == 0
    assert conc.serial_number == "GW00110001"
    assert conc.model_id == "SIN.EQRPT868XM"
    assert conc.communication_status == "Ok"


def test_hca_device_count(report):
    """Should parse exactly 10 HCA devices (including the VERDI CAMERA duplicate)."""
    assert len(report.hca_devices) == 10


def test_hca_device_fields(report):
    """HCA devices should have correct fields including readings."""
    rossi_bagno = next(d for d in report.hca_devices if d.name == "ROSSI BAGNO")
    assert rossi_bagno.count == 2
    assert rossi_bagno.serial_number == "30001001"
    assert rossi_bagno.description == "1 ROSSI INT 1 civ 42 "
    assert rossi_bagno.hca_current == 118.0
    assert rossi_bagno.hca_previous_season == 525.0
    assert rossi_bagno.communication_status == "Ok"


def test_hca_comma_decimal(report):
    """Parser should handle comma decimal separators correctly."""
    device = next(d for d in report.hca_devices if d.name == "ROSSI BAGNO")
    # "118,00" should become 118.0
    assert device.hca_current == 118.0


def test_error_status_parsed(report):
    """Communication errors should be parsed correctly."""
    conc_err = report.concentrators[1]
    assert conc_err.communication_status == "Errore di comunicazione"

    # BIANCHI SALOTTO has "Errore permanente | Errore temporaneo"
    bianchi = next(d for d in report.hca_devices if d.name == "BIANCHI SALOTTO")
    assert "Errore permanente" in bianchi.communication_status


def test_short_file_raises():
    """Parser should reject files that are too short."""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("a;b;c\n")
        f.flush()
        with pytest.raises(ValueError, match="too short"):
            parse_csv(Path(f.name))
