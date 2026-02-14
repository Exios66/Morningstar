# F0 Registry

> *"The graveyard has value. It tells us what we're leaving on the table."*
> — The Prophet

This registry tracks proposals rated F0 (Infrastructural): ideas that are currently impossible but reveal missing capabilities that would make them trivial.

---

## Active Entries

### Entry: Session Cross-Referencing

```yaml
proposal: Sessions should be able to reference each other, creating a web of institutional memory
infrastructure_gap: No session linking mechanism; sessions are isolated documents
date_logged: 2026-02-14
resurrection_triggers:
  - Implementation of session metadata with reference fields
  - Graph-based session storage
  - Search/recall system that surfaces related sessions
status: dormant
filed_by: Prophet
```

### Entry: YAML State Format

```yaml
proposal: Migrate state format from markdown to YAML for better multi-line support
infrastructure_gap: Current markdown parser is fragile with complex content
date_logged: 2026-02-14
resurrection_triggers:
  - Major state format revision
  - Addition of complex nested data structures to state
  - Widespread parsing failures
status: watching
filed_by: Prophet
notes: Court chose to improve markdown parser robustness instead. Revisit if issues persist.
```

### Entry: Personality-Driven Analysis

```yaml
proposal: Each personality should automatically contribute analysis based on their bias
infrastructure_gap: No AI/ML integration for automated code analysis
date_logged: 2026-02-14
resurrection_triggers:
  - Integration with static analysis tools
  - AI-powered code review capabilities
  - Personality-specific analysis engines
status: dormant
filed_by: Prophet
notes: >
  When analyzing code/decisions, personalities would contribute automatically:
  - Architect: Detect coupling, suggest abstractions
  - Engineer: Estimate effort based on codebase patterns
  - Debugger: Identify error handling gaps, edge cases
  - Prophet: Suggest F0-style "what if" alternatives
```

### Entry: Deliberation Replay

```yaml
proposal: Old deliberations should be replayable with new context
infrastructure_gap: No context-aware deliberation engine
date_logged: 2026-02-14
resurrection_triggers:
  - Implementation of AI-powered deliberation
  - Context storage and retrieval system
  - Decision drift tracking capability
status: dormant
filed_by: Prophet
notes: >
  Feed the same input to the court and see if the ruling would change 
  given new context. Track decision drift over time.
```

---

## Resurrected Entries

### Entry: The Oracle Command ✓

```yaml
proposal: CLI command that invokes only the Prophet for radical suggestions
infrastructure_gap: No mechanism for isolated personality invocation
date_logged: 2026-02-14
resurrected_date: 2026-02-14
resurrection_trigger: Court Advancement Session approved implementation
status: RESURRECTED → IMPLEMENTED
filed_by: Prophet
implementation: morningstar oracle <question>
notes: >
  The Prophet's optimism was justified. The Oracle command was approved 
  unanimously and implemented the same day. Includes mandatory disclaimer
  about the Prophet's ~10% accuracy rate.
```

---

## Quarterly Review

Last reviewed: 2026-02-14
Next review: 2026-05-14

Review process:
1. Check each dormant entry against current capabilities
2. Update status if infrastructure has changed
3. Resurrect any entries that can now be rated F1-F2
4. Archive permanently dead entries (>1 year dormant with no activity)
