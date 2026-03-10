"""Tests for the CSV parser."""

from pathlib import Path

import pytest

from sinapsi_converter.parser import parse_csv

ASSETS = Path(__file__).parent.parent / "assets"
SAMPLE_CSV = ASSETS / "RAW_report_1703_2026-03-02_08-29.csv"


@pytest.fixture
def report():
    """Parse the sample CSV once for all tests."""
    return parse_csv(SAMPLE_CSV)


def test_header_parsed(report):
    """Report header should contain correct metadata."""
    h = report.header
    assert h.filename == "RAW_report_1703_2026-03-02_08-29"
    assert h.report_date == "2026-03-02"
    assert h.report_time == "08:29"
    assert h.building_reference == "CONDOMINIO MERCANTINI"
    assert h.total_wireless == 105
    assert h.total_concentrators == 2


def test_concentrators_count(report):
    """Should parse exactly 2 concentrators."""
    assert len(report.concentrators) == 2


def test_concentrator_fields(report):
    """Concentrator devices should have correct fields."""
    conc = report.concentrators[0]
    assert conc.count == 0
    assert conc.serial_number == "RM23490160"
    assert conc.model_id == "SIN.EQRPT868XM"
    assert conc.communication_status == "Ok"


def test_hca_device_count(report):
    """Should parse exactly 105 HCA devices (including the MAZZI duplicate)."""
    assert len(report.hca_devices) == 105


def test_hca_device_fields(report):
    """HCA devices should have correct fields including readings."""
    # Find DOINA BAGNO (count=2, first HCA device in the CSV)
    doina_bagno = next(d for d in report.hca_devices if d.name == "DOINA BAGNO")
    assert doina_bagno.count == 2
    assert doina_bagno.serial_number == "16218294"
    assert doina_bagno.description == "8 TRAINOTTI INT 8 civ 7 "
    assert doina_bagno.hca_current == 118.0
    assert doina_bagno.hca_previous_season == 525.0
    assert doina_bagno.communication_status == "Ok"


def test_hca_comma_decimal(report):
    """Parser should handle comma decimal separators correctly."""
    device = next(d for d in report.hca_devices if d.name == "DOINA BAGNO")
    # "118,00" should become 118.0
    assert device.hca_current == 118.0


def test_error_status_parsed(report):
    """Communication errors should be parsed correctly."""
    conc_err = report.concentrators[1]
    assert conc_err.communication_status == "Errore di comunicazione"

    # GELSO SALOTTO has "Errore permanente | Errore temporaneo"
    gelso = next(d for d in report.hca_devices if d.name == "GELSO  SALOTTO")
    assert "Errore permanente" in gelso.communication_status


def test_short_file_raises():
    """Parser should reject files that are too short."""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("a;b;c\n")
        f.flush()
        with pytest.raises(ValueError, match="too short"):
            parse_csv(Path(f.name))
