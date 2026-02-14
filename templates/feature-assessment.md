# Feature Assessment

> *Template Version: 1.0 | Review Date: 2026-08-14*

---

## Feature Overview

**Name:** [Feature name]  
**Date:** [YYYY-MM-DD]  
**Proposer:** [Who proposed this]  
**Status:** [Proposed | Approved | In Progress | Completed | Rejected]

### Description

[Clear, concise description of the feature]

### User Story

As a [type of user], I want [goal] so that [benefit].

---

## MFAF Assessment

```
┌─────────────────────────────────────────────────────────────────┐
│ FEASIBILITY ASSESSMENT                                          │
├─────────────────────────────────────────────────────────────────┤
│ Proposal: [Feature name]                                        │
├─────────────────────────────────────────────────────────────────┤
│ Base Rating:        F[N] ([label])                              │
│ Risk Vectors:       +[X]                                        │
│   [ ] Touches auth/authz                                        │
│   [ ] External dependencies                                     │
│   [ ] Database migration                                        │
│   [ ] Public API changes                                        │
│   [ ] Unclear requirements                                      │
│   [ ] External team dependency                                  │
│   [ ] Previously attempted                                      │
│ Effective Rating:   F[N] ([label])                              │
│ Effort Band:        [S/M/L/XL]                                  │
├─────────────────────────────────────────────────────────────────┤
│ Recommendation:     [PROCEED/REVIEW/DELIBERATE/REJECT]          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Failure Scenario (if F3+)

**What could go wrong?**
[Description]

**Impact if it fails?**
[Blast radius]

**How would we detect failure?**
[Monitoring approach]

**How would we recover?**
[Rollback plan]

---

## Court Deliberation (if required)

```
┌─────────────────────────────────────────────────────────────────┐
│ MATTER BEFORE THE COURT                                         │
│ Shall we implement [feature name]?                              │
└─────────────────────────────────────────────────────────────────┘
```

**ARCHITECT:** [Argument]

**ENGINEER:** [Argument]

**DEBUGGER:** [Argument]

**PROPHET:** [Hail-Mary pitch or alternative approach]

```
┌─────────────────────────────────────────────────────────────────┐
│ VOTES                                                           │
├─────────────────────────────────────────────────────────────────┤
│ Architect: [YES/NO/ABSTAIN]                                     │
│ Engineer:  [YES/NO/ABSTAIN]                                     │
│ Debugger:  [YES/NO/ABSTAIN]                                     │
│ Prophet:   [YES/NO/ABSTAIN]                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Decision

**Ruling:** [Approved | Rejected | Deferred]

**Rationale:** [Brief explanation]

**Conditions (if any):** [Any conditions attached to approval]

---

## Implementation Plan

### Phases

1. [Phase 1]
2. [Phase 2]
3. [Phase 3]

### Dependencies

- [Dependency 1]
- [Dependency 2]

### Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]

---

*Recorded by the Scribe.*
