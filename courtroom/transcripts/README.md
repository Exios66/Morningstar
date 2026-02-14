# Transcripts — Historical Deliberation Records

> *"Decisions not recorded are decisions forgotten."*

This directory contains **complete transcripts** of courtroom deliberations. These serve as both historical record and practical reference.

---

## Purpose

Transcripts serve three functions:

1. **Historical Record** — What was decided, when, and why
2. **Training Material** — Examples of proper deliberation format
3. **Precedent** — Reference for similar future decisions

---

## Current Transcripts

| Date | Topic | Outcome |
|------|-------|---------|
| 2026-02-14 03:00 | Feasibility Framework | MFAF adopted unanimously |
| 2026-02-14 04:43 | System Advancement | Tier 1-2 proposals approved |

---

## Naming Convention

**Format:** `YYYYMMDD_HHMMSS_topic.md`

- **YYYYMMDD** — Date (year, month, day)
- **HHMMSS** — Time (24-hour, with seconds)
- **topic** — Brief topic identifier (lowercase, underscores)

**Examples:**
- `20260214_030000_feasibility_framework.md`
- `20260214_044300_system_advancement.md`
- `20260215_141500_database_selection.md`

---

## Transcript Structure

Every transcript MUST include:

### 1. Header Block

```markdown
# Court Transcript: [Full Topic Title]

**Date:** YYYY-MM-DD
**Time:** HH:MM:SS
**Session ID:** YYYYMMDD_HHMMSS
**Matter:** [Clear description of what was being decided]
**Presiding:** MORNINGSTAR
**Scribe:** Active
```

### 2. Opening Statement

```markdown
## TRANSCRIPT BEGIN

### OPENING STATEMENT

**MORNINGSTAR (Judge):**

[Clear statement of the problem before the court]
[Context and constraints]
[What the court must decide]
```

### 3. Arguments

```markdown
### ROUND ONE: ARGUMENTS

**ARCHITECT:**
[3-5 line argument from Architect's perspective]

**ENGINEER:**
[3-5 line argument from Engineer's perspective]

**DEBUGGER:**
[3-5 line argument from Debugger's perspective]

**PROPHET:**
[Exactly ONE radical proposal]
```

### 4. Cross-Examination (if occurred)

```markdown
### CROSS-EXAMINATION

**ENGINEER → ARCHITECT:**
[Question]

**ARCHITECT:**
[Response]
```

### 5. Voting

```markdown
### VOTING

┌─────────────────────────────────────────────────────────────────┐
│ VOTE TALLY                                                      │
├─────────────────────────────────────────────────────────────────┤
│ Architect:  [YES/NO/ABSTAIN/RECUSED]                            │
│ Engineer:   [YES/NO/ABSTAIN/RECUSED]                            │
│ Debugger:   [YES/NO/ABSTAIN/RECUSED]                            │
│ Prophet:    [YES/NO/ABSTAIN/RECUSED]                            │
├─────────────────────────────────────────────────────────────────┤
│ RESULT: [APPROVED/REJECTED/TIE - Resolution]                    │
└─────────────────────────────────────────────────────────────────┘
```

### 6. Ruling

```markdown
### RULING

**MORNINGSTAR (Judge):**

┌─────────────────────────────────────────────────────────────────┐
│ RULING                                                          │
└─────────────────────────────────────────────────────────────────┘

DECISION:
  [Clear statement of what was decided]

RATIONALE:
  [Why this decision was made]

RISK:
  [Acknowledged risks]

DISSENT (if any):
  [Personality]: "[Their recorded objection]"
```

### 7. Footer Block

```markdown
## TRANSCRIPT END

---

**Recorded by:** The Scribe
**Transcript saved:** courtroom/transcripts/[filename]
**Changelog updated:** [Yes/No]
**State updated:** [Yes/No]
```

---

## When to Create Transcripts

**MANDATORY for:**
- F3+ rated decisions (Significant or higher)
- Any contentious deliberation (non-unanimous vote)
- Prophet vindications
- Precedent-setting decisions

**RECOMMENDED for:**
- F2 decisions with complex trade-offs
- Decisions likely to be revisited
- Educational/training examples

**OPTIONAL for:**
- F1 decisions (trivial)
- Unanimous, obvious choices
- Procedural matters

---

## Reading Transcripts

### For New Users

Read transcripts to learn:

1. **The Voice** — Notice the sardonic, formal tone
2. **The Format** — Box drawing, labels, structure
3. **Argument Quality** — Brief but substantive (3-5 lines)
4. **Ruling Format** — Decision, Rationale, Risk

### For Reference

When facing a similar decision:

1. Search transcripts for related topics
2. Review how the court reasoned previously
3. Note any dissents (they may be relevant now)
4. Consider if context has changed

---

## Searching Transcripts

**By topic:**
```bash
grep -l "database" courtroom/transcripts/*.md
```

**By date range:**
```bash
ls courtroom/transcripts/202602*.md
```

**By voting pattern:**
```bash
grep -l "Prophet.*YES" courtroom/transcripts/*.md
```

---

## Maintenance

### Never Delete Transcripts

Transcripts are permanent record. If a decision is superseded:
- Create a new transcript for the new decision
- Reference the old transcript in the new one
- Do NOT delete or modify the original

### Archival

For very old transcripts (>1 year):
- Consider moving to `courtroom/transcripts/archive/`
- Maintain the naming convention
- Keep accessible for reference

---

*The court's rulings are its legacy. These transcripts preserve that legacy.*
