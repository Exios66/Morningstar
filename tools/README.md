# Tools — Python CLI & Utilities

> *The instruments for maintaining order and record.*

This directory contains the Python tooling that powers the MORNINGSTAR CLI and provides programmatic access to court functions.

---

## Contents

| File | Purpose |
|------|---------|
| `__init__.py` | Package initialization |
| `cli.py` | Command-line interface (main entry point) |
| `state.py` | State file reading/writing |
| `session.py` | Session lifecycle management |
| `changelog.py` | Automatic changelog updates |
| `validate.py` | JSON schema validation |
| `assess.py` | MFAF assessment tools |
| `backup.py` | Backup and restore functionality |
| `export.py` | State and session export |

---

## Installation

The CLI is installed via pip:

```bash
# From the Morningstar root directory
pip install -e .

# Verify installation
morningstar --help
```

---

## CLI Command Reference

### Session Management

#### `morningstar init`
Initialize a new session. Creates `state/current.md` with default values.

```bash
morningstar init
```

#### `morningstar status`
Display current session state: active work, decisions, issues.

```bash
morningstar status
```

#### `morningstar update`
Update session state with new information.

```bash
# Add work item
morningstar update --work "Implemented feature X"

# Record decision (format: topic:decision:risk)
morningstar update --decision "Auth:JWT tokens:Low"

# Report issue (format: issue:severity)
morningstar update --issue "Memory leak in parser:High"
```

#### `morningstar decide`
Quick command to record a decision (shortcut for update).

```bash
morningstar decide "Database Choice" -d "PostgreSQL" -r "ACID compliance" --risk Low
```

Options:
- `-d, --decision` — The ruling (required)
- `-r, --rationale` — Explanation
- `--risk` — Low/Medium/High/Critical (default: Low)

#### `morningstar end`
End the session, generate report, update changelog.

```bash
morningstar end
```

#### `morningstar validate`
Validate current state against JSON schema.

```bash
morningstar validate
```

---

### Court Operations

#### `morningstar convene`
Display the courtroom header for a new deliberation.

```bash
morningstar convene
```

Output:
```
┌─────────────────────────────────────────────────────────────────┐
│ THE COURT IS NOW IN SESSION                                     │
│ MORNINGSTAR presiding                                           │
└─────────────────────────────────────────────────────────────────┘

*sighs*

The personalities are assembled:
  • ARCHITECT  — Cold, precise, conservative
  • ENGINEER   — Practical, delivery-focused
  • DEBUGGER   — Paranoid, detail-obsessed
  • PROPHET    — Unstable, brilliant, dangerous
  • SCRIBE     — Silent, recording

State the matter before the court.
```

#### `morningstar oracle`
Invoke only the Prophet for radical thinking.

```bash
morningstar oracle "How might we approach caching?"
```

⚠️ **Warning:** The Prophet is wrong ~90% of the time. This command explicitly opts into radical, unconventional ideas.

#### `morningstar doctor`
Diagnose common issues with the installation.

```bash
morningstar doctor
```

Checks:
- State file exists and parses
- Core files present
- Courtroom rules present
- Schema files present
- Sessions directory exists
- Changelog exists
- F0 Registry exists

---

### MFAF Assessments

#### `morningstar assess new`
Create a new feasibility assessment.

```bash
# Interactive mode
morningstar assess new "Add real-time collaboration"

# Quick mode (non-interactive)
morningstar assess new "Add real-time collaboration" -b F3 -e L
```

Options:
- `-b, --base` — Base rating (F0-F5)
- `-e, --effort` — Effort band (S/M/L/XL)
- `--save/--no-save` — Save to file (default: save)

#### `morningstar assess list`
View recent assessments.

```bash
morningstar assess list
morningstar assess list -n 20  # Show 20 most recent
```

#### `morningstar assess f0`
View the F0 Registry (impossible ideas with potential).

```bash
morningstar assess f0
```

---

### Changelog Management

#### `morningstar log show`
Display unreleased changelog entries.

```bash
morningstar log show
```

#### `morningstar log add`
Add an entry to the changelog.

```bash
morningstar log add -c added -m "New feature X" -s "The Engineer"
```

Options:
- `-c, --category` — added/changed/fixed/removed/deprecated/security
- `-m, --message` — Description (required)
- `-s, --source` — Attribution

#### `morningstar log decide`
Record a court decision in the changelog.

```bash
morningstar log decide -t "Database" -d "PostgreSQL" -r "Low" --rationale "ACID compliance"
```

#### `morningstar log vindicate`
Record a Prophet vindication.

```bash
morningstar log vindicate -p "The cache will fail" -o "Cache caused 500 errors"
```

#### `morningstar log release`
Convert unreleased entries to a versioned release.

```bash
morningstar log release -v "1.0.0"
morningstar log release -v "1.1.0" -d "2026-03-01"  # Custom date
```

---

### History & Recall

#### `morningstar history`
List past session reports.

```bash
morningstar history
morningstar history -n 20  # Show 20 most recent
```

#### `morningstar recall`
Load and display a past session report.

```bash
morningstar recall 1                    # By index
morningstar recall report_20260214.md   # By filename
```

---

### Backup & Restore

#### `morningstar bkp create`
Create a backup of current state.

```bash
morningstar bkp create
morningstar bkp create -d "Before major refactor"
```

#### `morningstar bkp list`
List available backups.

```bash
morningstar bkp list
```

#### `morningstar bkp restore`
Restore state from a backup.

```bash
morningstar bkp restore 1                    # By index
morningstar bkp restore backup_20260214...   # By name
morningstar bkp restore 1 -f                 # Skip confirmation
```

⚠️ **Warning:** Creates a safety backup before restoring.

#### `morningstar bkp delete`
Delete a backup.

```bash
morningstar bkp delete 1
morningstar bkp delete backup_20260214... -f  # Skip confirmation
```

#### `morningstar bkp prune`
Remove old backups, keeping the most recent N.

```bash
morningstar bkp prune        # Keep 10 (default)
morningstar bkp prune -k 5   # Keep 5
```

---

### Export

#### `morningstar export state`
Export current state to JSON.

```bash
morningstar export state                    # Print to stdout
morningstar export state -o state.json      # Save to file
```

#### `morningstar export session`
Export a session to HTML.

```bash
morningstar export session report.md                    # Auto-name output
morningstar export session report.md -o report.html     # Specify output
```

#### `morningstar export list`
List sessions available for export.

```bash
morningstar export list
```

---

## Module Reference

### `state.py`

```python
from tools.state import read_state, write_state, init_state

# Read current state
state = read_state()

# Write state
write_state(state)

# Initialize fresh state
state = init_state()
```

### `session.py`

```python
from tools.session import start_session, update_session, end_session

# Start session
state = start_session()

# Update with work item
update_session(work_item="Implemented X")

# Update with decision
update_session(decision={
    "topic": "Database",
    "decision": "PostgreSQL",
    "rationale": "ACID",
    "risk": "Low"
})

# End session
end_session()
```

### `changelog.py`

```python
from tools.changelog import add_entry, add_decision, release_version

# Add changelog entry
add_entry('added', 'New feature', source='The Engineer')

# Add decision
add_decision('Topic', 'Decision', 'Low', 'Rationale')

# Release version
release_version('1.0.0')
```

### `assess.py`

```python
from tools.assess import create_assessment, format_assessment

# Create assessment
assessment = create_assessment(
    proposal="Add caching",
    base_rating="F3",
    risk_vectors={'externalDependencies': True},
    effort_band="M"
)

# Format for display
print(format_assessment(assessment))
```

### `backup.py`

```python
from tools.backup import create_backup, list_backups, restore_backup

# Create backup
path = create_backup("Before refactor")

# List backups
backups = list_backups()

# Restore (with confirmation)
restore_backup("1")
```

---

## Extending the CLI

To add a new command:

1. Edit `cli.py`
2. Add a new function with `@cli.command()` decorator
3. Use Click for options/arguments
4. Follow existing patterns

Example:
```python
@cli.command()
@click.option('--name', '-n', required=True, help='Name parameter')
def mycommand(name):
    """Description of my command."""
    click.echo(f"Hello, {name}")
```

---

## Error Handling

The CLI uses Click's built-in error handling. For custom errors:

```python
if not valid:
    click.echo("Error: Invalid input")
    raise SystemExit(1)
```

---

## Testing

Currently, tests are a Tier 3 proposal (deferred). To test manually:

```bash
# Check all commands work
morningstar --help
morningstar doctor
morningstar status
```

---

*These tools are the court's instruments. Use them wisely.*
