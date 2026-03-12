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

    Sorts by device_detail descending first, then by device_description
    ascending within each detail group.

    Args:
        devices: Unsorted list of HCA devices.

    Returns:
        Sorted list ready for the raw sheet.
    """
    # Two-pass stable sort: secondary key first, then primary key reversed
    by_description = sorted(devices, key=lambda d: d.description)
    return sorted(by_description, key=lambda d: d.detail, reverse=True)


def build_pivot_groups(devices: list[HCADevice]) -> list[PivotGroup]:
    """Build pivot groups from HCA devices.

    Groups devices by (device_detail, device_description), calculates subtotals.
    Sorted by device_detail descending, then device_description ascending —
    matching the raw sheet order.

    Args:
        devices: List of HCA devices (any order).

    Returns:
        List of PivotGroup, sorted by detail descending then apartment ascending.
    """
    # Group by (detail, apartment)
    key_map: dict[tuple[str, str], dict[str, float]] = {}

    for device in devices:
        key = (device.detail, device.description)
        if key not in key_map:
            key_map[key] = {}
        name = device.name
        key_map[key][name] = key_map[key].get(name, 0.0) + device.hca_current

    # Sort: detail descending, apartment ascending (two-pass stable sort)
    sorted_by_apartment = sorted(key_map.keys(), key=lambda k: k[1])
    sorted_keys = sorted(sorted_by_apartment, key=lambda k: k[0], reverse=True)

    groups: list[PivotGroup] = []
    for detail, apartment in sorted_keys:
        device_entries = sorted(key_map[(detail, apartment)].items())
        total = sum(hca for _, hca in device_entries)
        groups.append(
            PivotGroup(
                apartment=apartment,
                detail=detail,
                devices=device_entries,
                total=total,
            )
        )

    return groups
