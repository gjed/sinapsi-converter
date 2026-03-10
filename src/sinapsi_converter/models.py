"""Data models for Sinapsi report data."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ReportHeader:
    """Top-level report metadata (first 2 rows of the CSV)."""

    filename: str
    report_date: str
    report_time: str
    building_reference: str
    description: str
    total_wired: int
    total_wireless: int
    total_not_received: int
    total_concentrators: int


@dataclass
class ConcentratorDevice:
    """A concentrator or gateway device (no HCA readings)."""

    count: int
    primary_address: str
    serial_number: str
    name: str
    description: str
    detail: str
    measure_hex: str
    wired_wireless: str
    model_id: str
    readout_date: str
    readout_time: str
    communication_status: str


@dataclass
class HCADevice:
    """A heat cost allocator device with HCA readings."""

    count: int
    primary_address: str
    serial_number: str
    name: str
    description: str
    detail: str
    measure_hex: str
    wired_wireless: str
    model_id: str
    readout_date: str
    readout_time: str
    communication_status: str
    hca_current: float
    hca_previous_season: float
    date_1: str
    hca_3: float
    date_2: str
    date_3: str
    datetime_1: str


@dataclass
class ParsedReport:
    """Complete parsed report containing header and all devices."""

    header: ReportHeader
    concentrators: list[ConcentratorDevice] = field(default_factory=list)
    hca_devices: list[HCADevice] = field(default_factory=list)


@dataclass
class PivotGroup:
    """A group of devices for one apartment in the pivot table."""

    apartment: str  # device_description, e.g. "1 GUERRESCHI INT 1 civ 7 "
    devices: list[tuple[str, float]] = field(
        default_factory=list
    )  # (name, hca_current)
    total: float = 0.0
