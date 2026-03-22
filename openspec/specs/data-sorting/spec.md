# Data Sorting and Pivot Grouping

## Purpose

Sort HCA devices for the RAW sheet and build pivot groups for the PIVOT summary. Handles deduplication of same-name devices within apartments.

## Requirements

### Requirement: RAW Sheet Sorting

The sorter SHALL order HCA devices by `device_detail` descending first, then by `device_description` ascending within each detail group.

#### Scenario: Multiple detail groups

- **WHEN** HCA devices belong to different `device_detail` values
- **THEN** devices are sorted with highest detail value first
- **AND** within each detail group, devices are sorted alphabetically by `device_description`

#### Scenario: Single detail group

- **WHEN** all HCA devices share the same `device_detail`
- **THEN** devices are sorted alphabetically by `device_description`

### Requirement: Pivot Group Construction

The sorter SHALL group HCA devices by the compound key (`device_detail`, `device_description`) and produce a list of `PivotGroup` objects, each containing the apartment name, detail value, device list, and subtotal.

#### Scenario: Grouping by apartment

- **WHEN** multiple HCA devices share the same `device_description`
- **THEN** they are grouped into a single `PivotGroup`
- **AND** the group's `total` equals the sum of all `hca_current` values

### Requirement: Device Deduplication Within Pivot

The sorter SHALL deduplicate devices with the same `name` within a pivot group by summing their `hca_current` values.

#### Scenario: Duplicate device names

- **WHEN** two HCA devices in the same apartment have the same `name`
- **THEN** they appear as a single entry in the pivot group with their HCA values summed

### Requirement: Pivot Group Sorting

The pivot groups SHALL be sorted by `device_detail` descending, then by `device_description` (apartment) ascending. Within each group, individual devices are sorted alphabetically by name.

#### Scenario: Pivot output order

- **WHEN** pivot groups are built from unsorted devices
- **THEN** the returned list is ordered by detail descending, then apartment ascending
- **AND** device entries within each group are sorted alphabetically by name
