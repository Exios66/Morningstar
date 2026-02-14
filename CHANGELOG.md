# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

*The court maintains this record. Each entry is a verdict inscribed for posterity.*

## [Unreleased]

### Added

- **Judicial Consultant — Edward Cullen**: Non-voting advisory role attached to the Judge *(The Court — Unanimous)*
  - Advises on perspective beyond immediate technical concerns
  - Capability: "The Perspective" — once per deliberation, may observe what remains unspoken
  - Not subject to cross-examination; advises the Judge privately
  - Distinct from SME Framework (*sui generis*)
  - Voice: Quiet, ancient, perceptive
  - Key phrase: *"What remains unspoken here speaks loudest."*
- **Judge Title Formalization**: Judge now formally titled "The Honorable Lucius J. Morningstar" in formal contexts *(The Court — Unanimous)*
  - Formal usage: deliberation headers, session reports, RULES.md
  - Informal usage: "MORNINGSTAR" or "the Judge" remains acceptable
- **Subject Matter Expert (SME) Framework**: Complete system for admitting domain experts into courtroom proceedings *(The Court — Unanimous)*
  - **Expert Witness Protocol**: Advisory testimony from domain experts (no voting power)
  - **Specialist Seat Protocol**: Fifth voting position for F3+ matters requiring deep domain expertise
  - **Domain Registry**: 11 defined domains (`domains/experts.yaml`) with heuristics, failure modes, and scope
  - **SME Documentation**: Complete protocol documentation (`core/sme-framework.md`)
  - **SME Testimony Template**: Template for recording expert involvement (`templates/sme-testimony.md`)
  - **Updated Rules**: SME admission procedures added to `courtroom/RULES.md`
  - **Updated Procedures**: Expert testimony phase added to `core/procedures.md`
  - **Updated Personalities**: SME framework section added to `core/personalities.md`
- **Comprehensive README Documentation**: README.md files for every directory explaining usage, commands, and implementation *(The Scribe)*
  - Root `README.md` — Complete quick-start guide and overview
  - `core/README.md` — System prompt usage and customization
  - `courtroom/README.md` — Rules, best practices, and transcripts guide
  - `courtroom/transcripts/README.md` — Transcript format and standards
  - `tools/README.md` — Complete CLI command reference
  - `schema/README.md` — JSON schema documentation
  - `state/README.md` — Active state file management
  - `sessions/README.md` — Session report archival
  - `templates/README.md` — Template usage guide
  - `examples/README.md` — Learning from examples
  - `examples/discussions/README.md` — Extended deliberation examples
  - `backups/README.md` — Backup and restore procedures
- **Courtroom Procedures Directory**: New `courtroom/` folder establishing canonical reference documents *(The Scribe)*
  - `RULES.md` — Complete hardcoded courtroom rules (the law)
  - `BEST_PRACTICES.md` — Practical guidance and recovery procedures (the wisdom)
  - `transcripts/` — Archive of all deliberation transcripts (the precedent)
- **Deliberation Transcripts**: Direct printed transcripts of courtroom proceedings *(The Scribe)*
  - `20260214_030000_feasibility_framework.md` — MFAF adoption
  - `20260214_044300_system_advancement.md` — System advancement session
- **Mandatory Transcript Rule**: All F3+ deliberations SHALL be transcribed to `courtroom/transcripts/` *(The Court)*
- **Deliberation Templates**: New `templates/` directory with reusable templates for common deliberation types *(The Architect — Court Approved)*
  - `architecture-decision.md` — For architectural choices
  - `feature-assessment.md` — For new feature proposals
  - `incident-review.md` — For post-incident analysis
  - `prophet-vindication.md` — For documenting when the Prophet was right
- **CLI `oracle` Command**: Invoke only the Prophet for radical thinking — includes mandatory disclaimer about ~10% accuracy rate (`morningstar oracle <question>`) *(The Prophet — Resurrected from F0)*
- **CLI `decide` Command**: Quick command for recording decisions without full update syntax (`morningstar decide "topic" -d "decision" --risk low`) *(The Engineer)*
- **Backup/Restore System**: New `tools/backup.py` module with full backup and restore functionality *(The Debugger)*
  - `morningstar bkp create` — Create timestamped backups
  - `morningstar bkp list` — List available backups
  - `morningstar bkp restore` — Restore from backup (with safety backup)
  - `morningstar bkp delete` — Remove old backups
  - `morningstar bkp prune` — Keep only N most recent backups
- **Export System**: New `tools/export.py` module for state and session export *(The Engineer)*
  - `morningstar export state` — Export state to JSON
  - `morningstar export session` — Export sessions to styled HTML
  - `morningstar export list` — List exportable sessions
- **Mandatory Changelog Rule**: Explicit rule added to `procedures.md` and `MORNINGSTAR.md` requiring changelog updates at the end of each courtroom session *(The Court — Unanimous)*
- **Enhanced Personality Definitions**: Comprehensive personality documentation with decision heuristics, failure modes, signature questions, natural alliances, and invocation guidelines (`core/personalities.md`) *(The Court — Unanimous)*
- **Dissent Tracking**: New `dissents` and `dissentVindications` fields in state schema for recording minority opinions (`schema/state.schema.json`, `tools/state.py`) *(The Court — 3-0-1)*
- **State Parser Robustness**: Added `validate_state()`, `repair_state()`, strict mode parsing, and graceful error handling to `state.py` *(The Court — 3-0-1)*
- **MFAF Reference Document**: Complete Feasibility Assessment Framework documentation (`core/mfaf.md`) with quick reference card *(The Court — Unanimous)*
- **MFAF Schema**: JSON schema for assessment validation (`schema/assessment.schema.json`) *(The Engineer)*
- **F0 Registry**: Registry for "infrastructural" proposals that reveal missing capabilities (`state/f0-registry.md`) *(The Prophet)*
- **MFAF Assessment Module**: New `tools/assess.py` with rating calculations, risk vector processing, and interactive assessment *(The Engineer)*
- **CLI `convene` Command**: Display courtroom header for new deliberations *(The Court — Unanimous)*
- **CLI `history` Command**: List past session reports with timestamps *(The Court — Unanimous)*
- **CLI `recall` Command**: Load and display past session reports by index or filename *(The Court — Unanimous)*
- **CLI `doctor` Command**: Diagnostic tool for checking installation health and common issues *(The Debugger)*
- **CLI `assess` Command Group**: MFAF assessment tools including `assess new`, `assess list`, and `assess f0` *(The Court — Unanimous)*
- Automatic changelog management system (`tools/changelog.py`) *(The Scribe)*
- CLI commands for changelog operations: `log show`, `log add`, `log decide`, `log vindicate`, `log release` *(The Court)*
- Integration of changelog updates with session lifecycle *(Session Management)*

### Changed

- **Deliberation Schema**: Added `RECUSED` vote option, `dissents` array, `timestamp` field, and updated decision enum values (`schema/deliberation.schema.json`) *(The Architect)*
- **State Schema**: Extended with vote tallies per decision, dissent tracking, and dissent vindication records (`schema/state.schema.json`) *(The Architect)*
- **State Parser**: Rewritten with type hints, better error handling, section recognition for new fields, and validation utilities (`tools/state.py`) *(The Debugger)*
- **CLI Structure**: Reorganized with command groups, improved help text, and consistent formatting (`tools/cli.py`) *(The Engineer)*

### Decided

- **Judicial Consultant Addition**: Edward Cullen appointed as non-voting Judicial Consultant with "The Perspective" capability — *Risk: Low. Role creep possible if boundaries erode; mitigated by explicit documentation.* *(The Court — Unanimous)*
- **Judge Title Formalization**: Title changed to "The Honorable Lucius J. Morningstar" for formal contexts — *Risk: Low. Ceremonial change with clear usage guidelines.* *(The Court — Unanimous)*
- **SME Framework Adoption**: Two-tier system for domain expertise — Expert Witnesses (advisory) and Specialist Seats (voting) — *Risk: Medium. Novel mechanism; voting dynamics may shift; requires maintenance.* *(The Court — Unanimous)*
- **Test Decision**: Approved for testing — *Risk: Low. To verify CLI works* *(The Court)*
- **System Advancement Package**: Court approved Tier 1 and Tier 2 proposals for implementation — *Risk: Low. Addresses practical gaps without architectural risk.* *(The Court — Unanimous)*
- **Oracle Command Resurrection**: The Prophet's F0 proposal for the Oracle command was resurrected and implemented — *Risk: Low, with mandatory disclaimer.* *(The Court — Unanimous)*
- **Deliberation Templates**: Standardized templates for common deliberation types — *Risk: Low. Templates may become stale, mitigated by review dates.* *(The Court — Unanimous)*
- **Backup/Restore Capability**: State backup and restore functionality for recovery scenarios — *Risk: Low. The Debugger's insurance policy.* *(The Court — Unanimous)*
- **Mandatory Changelog Rule**: Changelog updates SHALL occur at the end of each courtroom session when decisions are made — *Risk: Low. Codifies existing practice.* *(The Court — Unanimous)*
- **Enhanced Personality Definitions**: Personalities now include decision heuristics, failure modes, alliances, and invocation guidelines — *Risk: Low. Improves deliberation quality.* *(The Court — Unanimous)*
- **Dissent Tracking**: Minority opinions are recorded for institutional learning — *Risk: Low. Dissents today may become doctrine tomorrow.* *(The Court — 3-0-1, Engineer abstained)*
- **State Parser Improvements**: Keep markdown format, add validation and repair utilities — *Risk: Low. Prophet's YAML proposal logged as F0.* *(The Court — 3-0-1, Prophet abstained)*
- **MFAF Integration**: Framework moved from examples to core, CLI tooling added — *Risk: Low. Operationalizes existing unanimous decision.* *(The Court — Unanimous)*
- **Session Archival**: History and recall commands for institutional memory — *Risk: Low. Prophet's cross-referencing proposal logged as F0.* *(The Court — Unanimous)*
- **CLI Completeness**: Added convene, doctor, assess, history, recall commands — *Risk: Low. Prophet's "oracle" command logged as F0.* *(The Court — Unanimous)*
- **Changelog Architecture**: Automatic updates triggered by session events and deliberations — *Risk: Low. The court's proceedings should be recorded as they happen, not reconstructed from memory.* *(The Court)*

### Warned

- **Consultant's Perspective**: The Prophet proposed that Edward Cullen should have "the right to name the unspoken"—psychological insight beyond domain expertise. Adopted in constrained form as the Consultant's "Perspective" capability. *(The Prophet — Partially Vindicated 2026-02-14)*
- **Specialist Seat**: The Prophet proposed that domain experts should sit on the bench with full voting power rather than merely testify as witnesses. Adopted unanimously. *(The Prophet — Vindicated 2026-02-14)*

### F0 Registry Entries

**New:**

- **Personality-Driven Analysis**: Automated analysis powered by each personality's bias *(The Prophet)*
- **Deliberation Replay**: Replay old deliberations with new context to track decision drift *(The Prophet)*

**Resurrected:**

- **The Oracle Command**: ✓ Implemented as `morningstar oracle <question>` *(The Prophet — Vindicated)*

**Existing:**

- **Session Cross-Referencing**: Sessions should reference each other for institutional memory web *(The Prophet)*
- **YAML State Format**: Migrate from markdown to YAML for better complex content handling *(The Prophet)*

## [0.1.0] - 2026-02-14

### Added

- Core system prompt architecture (`core/`) *(Initial Implementation)*
- JSON Schemas for state validation (`schema/`) *(Initial Implementation)*
- Python tooling for session management (`tools/`) *(Initial Implementation)*
- Initial documentation and personality definitions *(Initial Implementation)*
