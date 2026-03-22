# Packaging and CI/CD

## Purpose

Package the converter as a standalone Windows .exe via PyInstaller, run CI tests across Python 3.10-3.13, and automate releases via tag-triggered GitHub Actions workflows.

## Requirements

### Requirement: PyInstaller Entry Point

The PyInstaller build SHALL use `scripts/pyinstaller_entry.py` with absolute imports (not `__main__.py` with relative imports) and `--paths src` to resolve modules correctly.

#### Scenario: PyInstaller build succeeds

- **WHEN** PyInstaller builds with `--onefile` using `scripts/pyinstaller_entry.py`
- **THEN** the resulting executable runs without `ImportError`
- **AND** relative import issues are avoided

### Requirement: Catch-All Exception Handler

The PyInstaller entry point SHALL wrap the main function in a try/except that catches all exceptions, prints the error, and pauses on Windows before exiting.

#### Scenario: Unhandled exception on Windows

- **WHEN** the .exe encounters an unhandled exception on Windows
- **THEN** the error is printed to the console
- **AND** the program pauses so the user can read the message before the window closes

### Requirement: CI Test Matrix

GitHub Actions CI SHALL run pytest with coverage on Python 3.10, 3.11, 3.12, and 3.13 on every push and pull request.

#### Scenario: CI pipeline

- **WHEN** a push or PR is made to the repository
- **THEN** tests run on all four Python versions
- **AND** coverage is reported

### Requirement: Tag-Triggered Release

GitHub Actions SHALL trigger a release workflow on tags matching `v*`. The workflow SHALL: run tests, build PyInstaller executables for Windows and Linux, and create a GitHub Release with the artifacts attached.

#### Scenario: Version tag pushed

- **WHEN** a tag like `v0.5.0` is pushed
- **THEN** the release workflow runs tests
- **AND** builds Windows and Linux executables via PyInstaller
- **AND** creates a GitHub Release with both artifacts

### Requirement: Cross-Platform Execution

The Python source SHALL run on both Linux (for development and CI) and Windows (for end users). PyInstaller packaging targets Windows primarily.

#### Scenario: Linux development

- **WHEN** a developer runs the project on Linux
- **THEN** all modules, tests, and CLI mode work without modification

#### Scenario: Windows end user

- **WHEN** an end user runs the .exe on Windows
- **THEN** drag-and-drop mode and GUI mode both work

### Requirement: CODEOWNERS

The repository SHALL have a `CODEOWNERS` file assigning `@gjed` as the owner of all files.

#### Scenario: Pull request review

- **WHEN** a pull request is opened
- **THEN** `@gjed` is automatically requested as a reviewer
