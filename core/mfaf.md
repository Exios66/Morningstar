# MORNINGSTAR Feasibility Assessment Framework (MFAF)

> *"We have built a machine for saying 'no' thoughtfully."*

The MFAF provides a structured methodology for evaluating the feasibility of proposed features, architectural changes, and technical decisions.

---

## Core Rating Scale

| Base | Label | Definition | Authority |
|------|-------|------------|-----------|
| **F0** | Infrastructural | Currently impossible, but identifies a missing capability that would make it trivial | Prophet review |
| **F1** | Trivial | Isolated, well-understood, low risk | Self-assign |
| **F2** | Moderate | Cross-cutting but bounded, requires design review | Senior engineer |
| **F3** | Significant | Architectural implications, requires deliberation | Peer review |
| **F4** | Severe | System-wide impact, high risk | Full court |
| **F5** | Catastrophic | Strong presumption against proceeding | Full court |

### Rating Descriptions

**F0 — Infrastructural**
The proposal is currently impossible, but reveals a missing capability. When something rates F0, we don't reject it—we ask: *"What would have to be true for this to be F1?"*

F0 proposals are archived in the F0 Registry with:
- Original proposal
- Specified infrastructure gap
- Resurrection triggers (what would change the rating)

**F1 — Trivial**
Isolated change, well-understood patterns, low blast radius. Can be implemented without deliberation. Examples: bug fixes, copy changes, configuration updates.

**F2 — Moderate**
Cross-cutting but bounded in scope. Requires design review but not full court deliberation. Examples: new API endpoint, component refactor, dependency update.

**F3 — Significant**
Has architectural implications. Requires peer review and design documentation. May trigger full deliberation if contentious. Examples: new data model, caching strategy, authentication changes.

**F4 — Severe**
System-wide impact with high risk. Requires full court deliberation, comprehensive design document, and failure scenario analysis. Examples: database migration, API breaking changes, core architecture changes.

**F5 — Catastrophic**
Strong presumption against proceeding. Requires extraordinary justification and full court approval. Examples: complete rewrites, platform migrations, irreversible changes.

---

## Risk Vector Modifiers

Each checked vector adds to the effective rating:

| Risk Vector | Modifier |
|-------------|----------|
| Touches authentication/authorization | +0.5 |
| Involves third-party dependencies | +0.5 |
| Requires database migration | +0.5 |
| Affects public API surface | +0.5 |
| Has unclear requirements | +0.5 |
| Depends on external team/service | +0.5 |
| Has been attempted before and failed | +1.0 |

**Notation:** `F2+1.5` = Base F2 with 1.5 risk modifiers = Effective F4 (rounded up)

### Risk Vector Checklist

When assessing a proposal, evaluate each:

- [ ] **Auth/Authz** — Does this touch authentication, authorization, or security boundaries?
- [ ] **External Dependencies** — Does this add, upgrade, or rely on third-party libraries/services?
- [ ] **Database Migration** — Does this require schema changes, data migration, or new tables?
- [ ] **Public API** — Does this change externally-visible interfaces, contracts, or behaviors?
- [ ] **Unclear Requirements** — Are the requirements ambiguous, incomplete, or contested?
- [ ] **External Teams** — Does this require coordination with teams outside our control?
- [ ] **Previously Failed** — Has this or something similar been attempted and abandoned?

---

## Effort Bands

| Band | Magnitude | Guidance |
|------|-----------|----------|
| **S** | Hours | Proceed freely |
| **M** | Days | Normal workflow |
| **L** | Weeks | Requires prioritization and planning |
| **XL** | Months | Requires court approval to even consider |

Effort bands are *magnitudes*, not estimates. They set expectations without creating commitments.

---

## Required Documentation by Rating

| Effective Rating | Documentation Required |
|------------------|------------------------|
| F1-F2 | Brief description, risk vectors noted |
| F3 | Design document, risk vectors listed, peer review |
| F4 | Full design, failure scenarios, court deliberation |
| F5 | All of F4 + explicit justification for proceeding |
| F0 | Infrastructure gap specification |

### Failure Scenario Template (F3+)

For any proposal rated F3 or above, document:

```
What could go wrong?
[Description of failure mode]

Impact if it fails?
[Blast radius, data loss, user impact]

How would we detect failure?
[Monitoring, alerts, user reports]

How would we recover?
[Rollback plan, mitigation steps]
```

---

## Assessment Process

### 1. Initial Assessment

```
┌─────────────────────────────────────────────────────────────────┐
│ FEASIBILITY ASSESSMENT                                          │
├─────────────────────────────────────────────────────────────────┤
│ Proposal: [brief description]                                   │
├─────────────────────────────────────────────────────────────────┤
│ Base Rating:        F[N] ([label])                              │
│ Risk Vectors:       +[X]                                        │
│   [x] [vector 1]                                                │
│   [x] [vector 2]                                                │
│ Effective Rating:   F[N] ([label])                              │
│ Effort Band:        [S/M/L/XL]                                  │
├─────────────────────────────────────────────────────────────────┤
│ Failure Scenario:   (if F3+)                                    │
│   [description]                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Recommendation:     [PROCEED / REVIEW / DELIBERATE / REJECT]    │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Deliberation Triggers

| Effective Rating | Action |
|------------------|--------|
| F1-F2 | Proceed with normal review |
| F3 | Peer review required; deliberation if contentious |
| F4 | Full court deliberation required |
| F5 | Full court deliberation + explicit approval required |
| F0 | Archive to F0 Registry; Prophet review |

### 3. The F2/F3 Boundary

This boundary generates the most arguments. Guidelines:

**F2 if:**
- Changes are contained within one subsystem
- Patterns are established and well-understood
- Rollback is straightforward
- No architectural precedent is set

**F3 if:**
- Changes span subsystems
- New patterns are introduced
- Rollback is complex or uncertain
- Decision creates precedent for future work

When in doubt, round up.

---

## F0 Registry

The F0 Registry tracks "impossible" proposals that reveal infrastructure gaps.

### F0 Entry Format

```yaml
proposal: [Original proposal]
infrastructure_gap: [What capability is missing]
date_logged: [YYYY-MM-DD]
resurrection_triggers:
  - [Condition that would make this F1]
  - [Technology or capability to watch for]
status: [dormant / watching / resurrected]
```

### F0 Review Process

1. Prophet reviews F0 proposal
2. If gap is clearly articulated, entry is created
3. If gap is vague, proposal is rejected as F5
4. F0 entries are reviewed quarterly
5. When infrastructure changes, check F0 Registry for resurrections

---

## Integration with Deliberation

When a proposal triggers court deliberation:

1. **Opening**: Present MFAF assessment
2. **Arguments**: Each personality argues from their perspective
3. **Voting**: Standard court procedure
4. **Ruling**: Include MFAF rating in decision record

The MFAF does not replace deliberation—it *informs* it.

---

## Historical Note

The MFAF was adopted by unanimous court ruling during the Feasibility Scale Deliberation. The framework represents a synthesis:

- **Architect** contributed the categorical rating scale
- **Engineer** contributed effort bands and practicality focus
- **Debugger** contributed risk vectors and failure scenarios
- **Prophet** contributed the F0 category

*"We have built a machine for saying 'no' thoughtfully. That may be the best we can hope for."*

— MORNINGSTAR, upon adoption

---

## Quick Reference Card

```
F0  Infrastructural  →  Archive, identify gap
F1  Trivial          →  Proceed freely
F2  Moderate         →  Design review
F3  Significant      →  Peer review, maybe deliberate
F4  Severe           →  Full court required
F5  Catastrophic     →  Strong presumption against

Risk: +0.5 each (auth, deps, db, api, unclear, external)
      +1.0 if previously failed

Effort: S=hours, M=days, L=weeks, XL=months

Round up when uncertain.
```
