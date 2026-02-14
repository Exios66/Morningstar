# Sessions — Archived Session Reports

> *The historical record of what was accomplished.*

This directory contains **archived session reports** — summaries generated when sessions end. Unlike transcripts (which record deliberations), session reports summarize the work done during a session.

---

## Purpose

Session reports provide:

1. **Work Summary** — What was accomplished
2. **Decision Record** — What was decided
3. **Issue Tracking** — What problems remain
4. **Changelog Link** — What was inscribed

---

## File Format

**Naming:** `report_YYYYMMDD_HHMMSS.md`

**Structure:**
```markdown
# Session Report [Timestamp]

## Work Completed
- Item 1
- Item 2

## Decisions
- Topic: Decision

## Issues
- Issue: Severity

## Changelog Entries Added
- Entry 1
- Entry 2
```

---

## Creating Session Reports

Session reports are **automatically generated** when you end a session:

```bash
morningstar end
```

The report includes:
- All work items from `state/current.md`
- All decisions made during the session
- Outstanding issues
- Changelog entries that were added

---

## Viewing Session Reports

### List Available Reports

```bash
morningstar history
morningstar history -n 20  # Show more
```

Output:
```
┌─────────────────────────────────────────────────────────────────┐
│ SESSION HISTORY                                                 │
└─────────────────────────────────────────────────────────────────┘

  [1] 2026-02-14 12:34:56  →  report_20260214_123456.md
  [2] 2026-02-13 09:15:30  →  report_20260213_091530.md

Use 'morningstar recall <filename>' to view a specific session.
```

### View a Specific Report

```bash
# By index
morningstar recall 1

# By filename
morningstar recall report_20260214_123456.md
```

---

## Session Reports vs. Transcripts

| Aspect | Session Reports | Transcripts |
|--------|-----------------|-------------|
| **Location** | `sessions/` | `courtroom/transcripts/` |
| **Content** | Work summary | Full deliberation |
| **Generated** | `morningstar end` | Manual or during deliberation |
| **Purpose** | What was done | How decisions were made |
| **Detail** | Brief | Comprehensive |

**Use session reports when:**
- You want to see what was accomplished
- You need a quick summary
- You're reviewing productivity

**Use transcripts when:**
- You need to understand why a decision was made
- You're looking for precedent
- You're training someone on the court

---

## Exporting Session Reports

### To HTML

```bash
morningstar export session report_20260214_123456.md
# Creates report_20260214_123456.html
```

The HTML export includes:
- Styled dark theme
- Proper formatting
- Metadata footer

### List Exportable Sessions

```bash
morningstar export list
```

---

## Best Practices

### Meaningful Work Items

During a session, add clear work items:
```bash
morningstar update --work "Implemented user authentication with JWT"
```

Not:
```bash
morningstar update --work "stuff"
```

### End Sessions Properly

Always end sessions with `morningstar end`:
- Generates the report
- Updates changelog
- Creates clean state for next session

### Review Periodically

Check session history to:
- Track progress over time
- Identify patterns
- Find when issues were introduced

---

## Directory Maintenance

### Archival

Old sessions can be moved to a subdirectory:
```bash
mkdir sessions/2026-Q1
mv sessions/report_202601*.md sessions/2026-Q1/
```

### Cleanup

If disk space is a concern:
- Keep last 30-90 days of sessions
- Archive older ones to external storage
- Never delete — archive instead

---

## Troubleshooting

### "No session reports found"

**Cause:** No sessions have been ended yet.
**Solution:** Run `morningstar end` to generate a report.

### Report seems incomplete

**Cause:** State wasn't updated during session.
**Solution:** Use `morningstar update` frequently during sessions.

### Can't find specific session

**Cause:** May be in archive or wrong date.
**Solution:** Use `ls sessions/` to see all files, check archives.

---

## Integration

Session reports are referenced by:
- `CHANGELOG.md` — Links to relevant sessions
- `courtroom/transcripts/` — May reference session context
- Future sessions — For continuity

---

*Sessions are the rhythm of work. Reports are the proof.*
