# State — Active Session Data

> *The living memory of the court.*

This directory contains the **active state** of MORNINGSTAR sessions. Unlike archived sessions, these files are regularly read and written during normal operation.

---

## Contents

| File/Folder | Purpose | Updated By |
|-------------|---------|------------|
| `current.md` | Current session state | `morningstar update`, `end` |
| `f0-registry.md` | Registry of F0 proposals | Manual, `morningstar assess` |
| `assessments/` | MFAF assessments | `morningstar assess new` |

---

## File Descriptions

### `current.md` — Current Session State

The primary state file. Read at session start, updated throughout, reset at session end.

**Structure:**
```markdown
# Session State

## Last Updated
[ISO 8601 timestamp]

## Active Work
- Work item 1
- Work item 2

## Decisions Made
- Topic: Decision — Risk

## Outstanding Issues
- Issue description: Severity

## Prophet's Vindications
- Prediction that came true

## Dissent Vindications
- When a dissenter was proven right

## Next Session
- Recommendation for next session
```

**Updating:**
```bash
# Add work item
morningstar update --work "Implemented feature X"

# Record decision
morningstar update --decision "Auth:JWT tokens:Low"

# Or use quick decide
morningstar decide "Auth" -d "JWT tokens" --risk Low
```

### `f0-registry.md` — F0 Proposal Registry

Tracks "infrastructural" proposals (F0-rated) — ideas that are currently impossible but reveal missing capabilities.

**Structure:**
```yaml
proposal: Description of the proposal
infrastructure_gap: What capability is missing
date_logged: YYYY-MM-DD
resurrection_triggers:
  - Condition that would make this F1
  - Technology to watch for
status: dormant | watching | resurrected
filed_by: Personality name
notes: Additional context
```

**Purpose:**
- Archive radical ideas that can't be implemented yet
- Track what infrastructure gaps exist
- Resurrect ideas when capabilities emerge

**Quarterly review:** Check if any F0 entries can be resurrected.

### `assessments/` — MFAF Assessments

Directory containing saved MFAF assessments as JSON files.

**File naming:** `assessment_YYYYMMDD_HHMMSS.json`

**Creating assessments:**
```bash
morningstar assess new "Add real-time collaboration"
```

**Viewing assessments:**
```bash
morningstar assess list
```

---

## How State is Used

### Session Start (`/morningstar`)

1. AI reads `current.md`
2. Summarizes active work, decisions, issues
3. Predicts concerns based on state

### During Session

1. Work items added via `update --work`
2. Decisions recorded via `decide` or `update --decision`
3. Issues logged via `update --issue`

### Session End (`/end`)

1. State finalized
2. Session report generated
3. Changelog updated
4. State may be reset for next session

---

## State File Format

The `current.md` file uses a simple markdown format that's parsed by `tools/state.py`.

**Key rules:**
- Section headers start with `## `
- List items start with `- `
- Timestamps in brackets: `[2026-02-14T12:00:00]`
- Decisions format: `Topic: Decision — Risk`
- Issues format: `Issue: Severity`

**Example:**
```markdown
# Session State

## Last Updated
[2026-02-14T12:00:00]

## Active Work
- Implementing authentication
- Writing tests for API

## Decisions Made
- Database: PostgreSQL — Low
- Auth: JWT tokens — Medium

## Outstanding Issues
- Memory leak in parser: High
- Documentation gaps: Low

## Prophet's Vindications
- None (yet)

## Dissent Vindications
- None (yet)

## Next Session
- Complete authentication implementation
- Address memory leak
```

---

## Backup & Recovery

State files are automatically included in backups:

```bash
# Create backup
morningstar bkp create -d "Before major changes"

# List backups
morningstar bkp list

# Restore if needed
morningstar bkp restore 1
```

**Recovery from corruption:**
1. Check backups: `morningstar bkp list`
2. Restore recent backup: `morningstar bkp restore <id>`
3. If no backup: Reconstruct from changelog and transcripts

---

## Validation

State is validated against `schema/state.schema.json`:

```bash
morningstar validate
```

**Common validation errors:**
- Missing required section
- Malformed timestamp
- Invalid severity level

---

## Best Practices

### Regular Updates

Update state frequently during sessions:
```bash
morningstar update --work "Completed task X"
```

### Clear Descriptions

Write clear, specific descriptions:
- ✅ "Implemented JWT refresh token rotation"
- ❌ "Did auth stuff"

### Decision Recording

Always include rationale:
```bash
morningstar decide "Cache Strategy" -d "Redis" -r "Need distributed caching" --risk Medium
```

### Issue Tracking

Use appropriate severity levels:
- **Low** — Minor inconvenience
- **Medium** — Should be addressed soon
- **High** — Blocking or significant risk
- **Critical** — Requires immediate attention

---

## Gitignore Considerations

By default, `state/current.md` is gitignored because:
- It contains session-specific data
- It changes frequently
- Each user/instance has their own state

The `f0-registry.md` is typically tracked because:
- It's institutional knowledge
- It's updated less frequently
- It's shared across the team

---

## Troubleshooting

### "No state found"

**Cause:** `current.md` doesn't exist.
**Solution:** Run `morningstar init`

### State not updating

**Cause:** Write permissions or path issues.
**Solution:** Check file permissions, run from correct directory.

### Parse errors

**Cause:** Malformed markdown in `current.md`.
**Solution:** Check format, restore from backup if needed.

---

*State is memory. Treat it with care.*
