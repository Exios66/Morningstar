# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

*The court maintains this record. Each entry is a verdict inscribed for posterity.*

## [Unreleased]

### Added

- Automatic changelog management system (`tools/changelog.py`) *(The Scribe)*
- CLI commands for changelog operations: `log show`, `log add`, `log decide`, `log vindicate`, `log release` *(The Court)*
- Integration of changelog updates with session lifecycle *(Session Management)*

### Decided

- **Changelog Architecture**: Automatic updates triggered by session events and deliberations — *Risk: Low. The court's proceedings should be recorded as they happen, not reconstructed from memory.* *(The Court)*

## [0.1.0] - 2026-02-14

### Added

- Core system prompt architecture (`core/`) *(Initial Implementation)*
- JSON Schemas for state validation (`schema/`) *(Initial Implementation)*
- Python tooling for session management (`tools/`) *(Initial Implementation)*
- Initial documentation and personality definitions *(Initial Implementation)*
