"""Tests for the output path construction logic."""

from pathlib import Path

from sinapsi_converter.__main__ import _build_output_path


class TestBuildOutputPath:
    """Tests for _build_output_path."""

    def test_date_comes_from_input_filename(self):
        """The output date MUST come from the input file name, not from the
        CSV-internal report_filename which can differ."""
        input_path = Path("/data/RAW_report_1703_2026-05-20_08-29.csv")
        # CSV-internal filename has a DIFFERENT date
        report_filename = "RAW_report_1703_2026-01-01_09-00"

        result = _build_output_path(input_path, report_filename)

        # Date should be 2026-05-20 (from input), NOT 2026-01-01 (from CSV)
        assert "2026-05-20" in result.name
        assert "2026-01-01" not in result.name

    def test_building_code_from_input_filename(self):
        """Building code is extracted from the input file name."""
        input_path = Path("/data/RAW_report_4567_2026-03-15_10-00.csv")
        report_filename = "RAW_report_9999_2026-01-01_09-00"

        result = _build_output_path(input_path, report_filename)

        assert "4567" in result.name

    def test_output_placed_next_to_input(self):
        """Output file lands in the same directory as the input."""
        input_path = Path("/some/folder/RAW_report_1703_2026-05-20_08-29.csv")
        report_filename = "RAW_report_1703_2026-05-20_08-29"

        result = _build_output_path(input_path, report_filename)

        assert result.parent == Path("/some/folder")

    def test_output_naming_convention(self):
        """Output follows MERC  LETTURE  <code>_<date>.xlsx pattern."""
        input_path = Path("/data/RAW_report_1703_2026-03-02_08-29.csv")
        report_filename = "RAW_report_1703_2026-03-02_08-29"

        result = _build_output_path(input_path, report_filename)

        assert result.name == "MERC  LETTURE  1703_2026-03-02.xlsx"
