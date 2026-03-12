"""Sorting and grouping logic for the output sheets.

Raw sheet: devices sorted by device_detail first, then device_description
within each detail group.

PIVOT sheet: alphabetical by device_description, then alphabetical by
device name within each group.
"""

from __future__ import annotations

from .models import HCADevice, PivotGroup


def sort_for_raw_sheet(devices: list[HCADevice]) -> list[HCADevice]:
    """Sort HCA devices for the raw data sheet.

    Sorts by device_detail first, then by device_description within each
    detail group.

    Args:
        devices: Unsorted list of HCA devices.

    Returns:
        Sorted list ready for the raw sheet.
    """
    return sorted(devices, key=lambda d: (d.detail, d.description))


def build_pivot_groups(devices: list[HCADevice]) -> list[PivotGroup]:
    """Build pivot groups from HCA devices.

    Groups devices by apartment (device_description), calculates subtotals,
    and sorts alphabetically.

    Args:
        devices: List of HCA devices (any order).

    Returns:
        List of PivotGroup, sorted alphabetically by apartment.
    """
    # First level: group by apartment
    apartment_map: dict[str, dict[str, float]] = {}

    for device in devices:
        apartment = device.description
        if apartment not in apartment_map:
            apartment_map[apartment] = {}
        # Sum HCA values for devices with the same name within an apartment
        # (handles duplicate serial numbers for the same logical device)
        name = device.name
        apartment_map[apartment][name] = (
            apartment_map[apartment].get(name, 0.0) + device.hca_current
        )

    groups: list[PivotGroup] = []
    for apartment in sorted(apartment_map.keys()):
        device_entries = sorted(apartment_map[apartment].items())
        total = sum(hca for _, hca in device_entries)
        groups.append(
            PivotGroup(
                apartment=apartment,
                devices=device_entries,
                total=total,
            )
        )

    return groups
