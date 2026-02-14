# Domain Expert Registry

> *"Expertise is welcome. Arrogance is not."*

This directory contains the registry of Subject Matter Experts available to the Morningstar Court.

---

## Overview

The court operates with four core voting personalities (Architect, Engineer, Debugger, Prophet). When matters require domain expertise beyond traditional software engineering, the court may summon **Expert Witnesses** or seat **Specialists**.

This registry defines who can be summoned and what they know.

---

## Files

| File | Purpose |
|------|---------|
| `experts.yaml` | Domain definitions, heuristics, and metadata |

---

## Quick Reference

### Available Domains

| Domain | Witness | Specialist | Primary Scope |
|--------|:-------:|:----------:|---------------|
| `security` | ✓ | ✓ | Auth, encryption, vulnerabilities |
| `database` | ✓ | ✓ | Queries, schema, replication |
| `compliance` | ✓ | ✓ | GDPR, HIPAA, SOC2 |
| `infrastructure` | ✓ | ✓ | K8s, cloud, networking |
| `performance` | ✓ | ✓ | Profiling, caching, optimization |
| `accessibility` | ✓ | ✓ | WCAG, screen readers |
| `ux` | ✓ | — | User research, patterns |
| `legal` | ✓ | — | Licensing, IP, contracts |
| `cryptography` | ✓ | ✓ | Algorithms, key management |
| `api_design` | ✓ | ✓ | REST, versioning, contracts |
| `testing` | ✓ | ✓ | Test strategy, coverage |

### Summoning Commands

```bash
# Summon as Expert Witness (any personality or Judge)
/summon security-expert

# Seat as Specialist (Judge only, F3+ matters)
/seat database-specialist
```

---

## Using the Registry

### Reading Domain Definitions

Each domain in `experts.yaml` includes:

```yaml
domain_name:
  name: Display name
  available_as: [witness, specialist]
  scope: What expertise this covers
  heuristics:
    - Decision principle 1
    - Decision principle 2
  signature_questions:
    - What they always ask
  failure_mode: How this expert goes wrong
  voice: Characteristic tone
  external_enrichment: true/false
  notes: Usage guidance
```

### Choosing Between Witness and Specialist

| Factor | Expert Witness | Specialist Seat |
|--------|---------------|-----------------|
| Voting power | 0 | 1 |
| Invoked by | Any personality | Judge only |
| For matters rated | Any | F3+ |
| Role in decision | Advisory | Participatory |
| Use when | Need information | Need domain judgment |

---

## Adding New Domains

### Prerequisites

- Identified recurring need for domain expertise
- Domain is distinct from existing entries
- Clear scope boundaries defined

### Process

1. **Draft definition** following the schema in `experts.yaml`
2. **Submit for deliberation** (F2 minimum)
3. **Upon approval**, add to `experts.yaml`
4. **Update metadata** (version, review date)
5. **Update this README** quick reference table

### Definition Requirements

All domains must specify:

- [ ] `name` — Human-readable name
- [ ] `available_as` — `[witness]` or `[witness, specialist]`
- [ ] `scope` — Clear boundaries of expertise
- [ ] `heuristics` — 3-5 decision principles
- [ ] `signature_questions` — What they always ask
- [ ] `failure_mode` — How they go wrong (every expert has blind spots)
- [ ] `voice` — Characteristic tone for roleplay
- [ ] `external_enrichment` — Whether external lookup is permitted
- [ ] `notes` — Usage guidance and caveats

---

## Maintenance

### Quarterly Review

Every quarter, the Scribe reviews:

- [ ] Are all domains still relevant?
- [ ] Are any domains missing that have been requested?
- [ ] Have failure modes been observed? Update accordingly.
- [ ] Are heuristics still current?

### Version Control

When modifying the registry:

1. Increment version in `_metadata`
2. Update `next_review` date
3. Note changes in `CHANGELOG.md`

---

## Document Control

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Created** | 2026-02-14 |
| **Next Review** | 2026-05-14 |
| **Maintainer** | The Scribe |

---

*The court's expertise has boundaries. This registry maps them.*
