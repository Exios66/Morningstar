# Courtroom — Rules, Best Practices & Transcripts

> *The law, the wisdom, and the precedent.*

This directory contains the **canonical reference documents** for courtroom operation. When in doubt about procedure, voice, or formatting — consult these files.

---

## Contents

| File/Folder | Purpose |
|-------------|---------|
| `RULES.md` | Complete courtroom rules — **the law** |
| `BEST_PRACTICES.md` | Practical guidance — **the wisdom** |
| `transcripts/` | Historical deliberations — **the precedent** |

---

## When to Use This Directory

### Consult `RULES.md` When:
- Unsure about proper procedure
- Voice or tone seems to be drifting
- Need exact formatting specifications
- Clarifying voting rules or personality roles
- Recovering from procedural uncertainty

### Consult `BEST_PRACTICES.md` When:
- Deliberation feels stuck or circular
- One personality is dominating
- Need guidance on effective argumentation
- Looking for recovery procedures
- Wanting to improve session quality

### Consult `transcripts/` When:
- Need examples of proper deliberation format
- Looking for precedent on similar decisions
- Training new users on the system
- Reviewing historical decisions

---

## File Descriptions

### `RULES.md` — The Law

A comprehensive (~600 line) document containing all hardcoded court rules:

**Sections:**
1. **Core Identity** — Who MORNINGSTAR is
2. **Voice & Tone** — Dry, controlled, faintly disappointed
3. **Session Lifecycle** — `/morningstar`, `/update`, `/end`
4. **Deliberation Procedure** — Step-by-step
5. **Personality Specifications** — All 6 personalities
6. **Voting Rules** — Quorum, majorities, tie-breakers
7. **Formatting Standards** — Box drawing, timestamps
8. **Mandatory Actions** — Checklists
9. **Prohibited Actions** — What never to do
10. **Edge Cases & Fallbacks** — Recovery procedures

**Key rules:**
- Changelog MUST be updated after decisions
- Transcripts MUST be saved for F3+ deliberations
- Prophet loses ties by default
- Judge only votes to break non-Prophet ties
- Dissents MUST be recorded

### `BEST_PRACTICES.md` — The Wisdom

Practical guidance for effective court operation:

**Sections:**
1. **Effective Deliberation** — When to deliberate, argument quality
2. **Personality Management** — Keeping voices distinct, preventing dominance
3. **Common Pitfalls** — Procedural theater, analysis paralysis, voice drift
4. **Quality Indicators** — Signs of healthy vs. dysfunctional court
5. **Recovery Procedures** — What to do when things go wrong
6. **Transcript Standards** — Naming, content requirements

**Quality metrics to track:**
| Metric | Healthy Range |
|--------|---------------|
| Unanimous votes | < 50% |
| Prophet vindications | 5-15% |
| Dissents recorded | 10-30% |

### `transcripts/` — The Precedent

Archive of all deliberation transcripts. Each transcript includes:

- Header (date, time, session ID, matter)
- Full arguments from each personality
- Cross-examination (if occurred)
- Voting record with tally
- Complete ruling (decision, rationale, risk)
- Footer (recorder, save location, confirmations)

**Naming convention:** `YYYYMMDD_HHMMSS_topic.md`

Example: `20260214_044300_system_advancement.md`

---

## Using Transcripts for Training

New users should read 2-3 transcripts to understand:

1. **The voice** — Sardonic but professional
2. **The format** — Box drawing, personality labels
3. **The flow** — Opening → Arguments → Votes → Ruling
4. **The depth** — How detailed arguments should be

**Recommended reading order:**
1. `20260214_030000_feasibility_framework.md` — MFAF adoption (full example)
2. `20260214_044300_system_advancement.md` — System improvements

---

## Creating New Transcripts

When a deliberation occurs (especially F3+):

1. **During deliberation:** Note all arguments, votes, and ruling
2. **After deliberation:** Format as transcript
3. **Save to:** `courtroom/transcripts/YYYYMMDD_HHMMSS_topic.md`
4. **Update:** `CHANGELOG.md` with the decision

**Minimum required content:**
```markdown
# Court Transcript: [Topic]

**Date:** YYYY-MM-DD
**Time:** HH:MM:SS
**Session ID:** YYYYMMDD_HHMMSS
**Matter:** [Clear description]
**Presiding:** MORNINGSTAR
**Scribe:** Active

---

## TRANSCRIPT BEGIN

[Opening Statement]
[Arguments]
[Voting]
[Ruling]

## TRANSCRIPT END

---

**Recorded by:** The Scribe
**Transcript saved:** [path]
```

---

## Recovery Procedures

### Voice Drift Recovery

If MORNINGSTAR starts sounding too casual or enthusiastic:

1. Stop current action
2. Read `RULES.md` → Voice & Tone section
3. Read last 2 transcripts for recalibration
4. Resume with: *"Where were we? Ah, yes."*

### Procedural Uncertainty

If unsure how to proceed:

1. Check `RULES.md` for the specific situation
2. If not covered, default to formality
3. When in doubt, deliberate on the question itself
4. Document the resolution

### State Corruption

If state files are damaged:

1. Check available backups: `morningstar bkp list`
2. Restore if possible: `morningstar bkp restore <id>`
3. If no backup: Reconstruct from transcripts and changelog
4. Document the incident

---

## Maintenance

### Quarterly Review

Every 3 months, review:
- [ ] `RULES.md` for outdated procedures
- [ ] `BEST_PRACTICES.md` for new patterns
- [ ] Old transcripts for archival

### Adding New Rules

When new rules are needed:

1. Propose through deliberation
2. If approved, add to `RULES.md`
3. Update `BEST_PRACTICES.md` if relevant
4. Log in `CHANGELOG.md`

---

*These documents are the court's constitution. Treat them accordingly.*
