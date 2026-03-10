"""Tests for sorting and grouping logic."""

from sinapsi_converter.models import HCADevice
from sinapsi_converter.sorter import build_pivot_groups, sort_for_raw_sheet


def _make_device(
    count: int, name: str, description: str, hca: float = 0.0
) -> HCADevice:
    """Create a minimal HCA device for testing."""
    return HCADevice(
        count=count,
        primary_address="",
        serial_number="12345",
        name=name,
        description=description,
        detail="",
        measure_hex="",
        wired_wireless="",
        model_id="",
        readout_date="",
        readout_time="",
        communication_status="Ok",
        hca_current=hca,
        hca_previous_season=0.0,
        date_1="",
        hca_3=0.0,
        date_2="",
        date_3="",
        datetime_1="",
    )


def test_sort_groups_by_description():
    """Devices should be grouped by description."""
    devices = [
        _make_device(3, "B Room", "2 APT B"),
        _make_device(1, "A Room", "1 APT A"),
        _make_device(2, "A Kitchen", "1 APT A"),
    ]
    result = sort_for_raw_sheet(devices)
    assert [d.description for d in result] == [
        "1 APT A",
        "1 APT A",
        "2 APT B",
    ]


def test_sort_by_count_within_group():
    """Within a group, devices should be sorted by count."""
    devices = [
        _make_device(10, "Room B", "1 APT A"),
        _make_device(3, "Room A", "1 APT A"),
        _make_device(7, "Room C", "1 APT A"),
    ]
    result = sort_for_raw_sheet(devices)
    assert [d.count for d in result] == [3, 7, 10]


def test_pivot_groups_alphabetical():
    """Pivot groups should be sorted alphabetically by apartment."""
    devices = [
        _make_device(1, "Room", "2 BBB", hca=10.0),
        _make_device(2, "Room", "1 AAA", hca=20.0),
    ]
    groups = build_pivot_groups(devices)
    assert [g.apartment for g in groups] == ["1 AAA", "2 BBB"]


def test_pivot_devices_alphabetical():
    """Devices within a pivot group should be sorted alphabetically."""
    devices = [
        _make_device(1, "Cucina", "1 APT", hca=5.0),
        _make_device(2, "Bagno", "1 APT", hca=3.0),
        _make_device(3, "Salotto", "1 APT", hca=7.0),
    ]
    groups = build_pivot_groups(devices)
    assert len(groups) == 1
    names = [name for name, _ in groups[0].devices]
    assert names == ["Bagno", "Cucina", "Salotto"]


def test_pivot_totals():
    """Pivot group total should be the sum of HCA values."""
    devices = [
        _make_device(1, "Room A", "1 APT", hca=10.0),
        _make_device(2, "Room B", "1 APT", hca=20.0),
    ]
    groups = build_pivot_groups(devices)
    assert groups[0].total == 30.0


def test_pivot_deduplicates_by_name():
    """Devices with the same name in the same apartment should be summed."""
    devices = [
        _make_device(1, "CAMERA MATR", "1 APT", hca=5.0),
        _make_device(2, "CAMERA MATR", "1 APT", hca=3.0),
    ]
    groups = build_pivot_groups(devices)
    assert len(groups[0].devices) == 1
    assert groups[0].devices[0] == ("CAMERA MATR", 8.0)
    assert groups[0].total == 8.0
