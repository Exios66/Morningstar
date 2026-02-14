# Templates — Reusable Deliberation Templates

> *Structure accelerates thought.*

This directory contains **reusable templates** for common deliberation types. Instead of reinventing format for each deliberation, use these templates as starting points.

---

## Available Templates

| Template | Use When |
|----------|----------|
| `architecture-decision.md` | Making architectural choices |
| `feature-assessment.md` | Evaluating new feature proposals |
| `incident-review.md` | Analyzing post-incident |
| `prophet-vindication.md` | Documenting when Prophet was right |

---

## Template Descriptions

### `architecture-decision.md`

**Use for:** Choosing between architectural approaches, technology selection, design patterns.

**Includes:**
- Context and background
- Constraints listing
- Decision drivers
- Multiple options with pros/cons
- MFAF assessment per option
- Court deliberation section
- Consequences analysis
- Review schedule

**Example scenarios:**
- "Should we use PostgreSQL or MongoDB?"
- "Monolith or microservices?"
- "How should we structure the API?"

### `feature-assessment.md`

**Use for:** Evaluating whether to implement a proposed feature.

**Includes:**
- Feature overview and user story
- MFAF assessment with risk vectors
- Failure scenario (for F3+)
- Court deliberation (if required)
- Implementation plan
- Success criteria

**Example scenarios:**
- "Should we add real-time collaboration?"
- "Should we implement dark mode?"
- "Should we build an API for third parties?"

### `incident-review.md`

**Use for:** Post-incident analysis and remediation planning.

**Includes:**
- Incident summary and timeline
- Impact assessment
- Root cause analysis (Debugger-led)
- Remediation deliberation
- Action items with owners
- Prophet vindication check
- Lessons learned

**Example scenarios:**
- Production outage review
- Security incident analysis
- Data loss investigation

### `prophet-vindication.md`

**Use for:** Documenting when the Prophet's prediction came true.

**Includes:**
- Original prophecy and context
- Court's response at the time
- What actually happened
- Analysis of why Prophet was right
- Lessons for each personality
- Formal recognition

**Example scenarios:**
- "The cache did fail under load"
- "The monolith did become unmaintainable"
- "The vendor did go out of business"

---

## How to Use Templates

### 1. Copy the Template

```bash
cp templates/architecture-decision.md sessions/adr_database_choice.md
```

### 2. Fill in the Sections

Edit the copy, replacing placeholders with actual content:
- `[YYYY-MM-DD]` → Actual date
- `[problem statement]` → Your actual problem
- `[argument]` → Actual arguments

### 3. Conduct the Deliberation

Work through each section:
1. Fill in context and constraints
2. Document options
3. Have each personality argue
4. Record votes
5. Deliver ruling

### 4. Save Appropriately

- **Architecture decisions** → `sessions/` or dedicated ADR folder
- **Feature assessments** → `state/assessments/` (if using MFAF) or `sessions/`
- **Incident reviews** → `sessions/incidents/` (create if needed)
- **Vindications** → `courtroom/transcripts/` (they're deliberation records)

---

## Template Structure

All templates follow a consistent structure:

```markdown
# [Template Name]

> *Template Version: X.X | Review Date: YYYY-MM-DD*

---

## [Section 1]

[Content with placeholders]

---

## [Court Deliberation Section]

[Standard deliberation format]

---

## [Decision/Outcome Section]

[Ruling format]

---

*Recorded by the Scribe.*
```

---

## Customizing Templates

### Adding Fields

To add a field to a template:
1. Edit the template file
2. Add the new section
3. Update the template version
4. Update this README

### Creating New Templates

To create a new template:

1. **Start from existing** — Copy the closest template
2. **Maintain structure** — Keep header, deliberation section, footer
3. **Add to this README** — Document the new template
4. **Version it** — Include version and review date

### Template Header

Always include:
```markdown
> *Template Version: 1.0 | Review Date: YYYY-MM-DD*
```

---

## Best Practices

### Use Templates Consistently

Using templates ensures:
- All relevant information is captured
- Deliberations follow proper format
- Historical records are comparable

### Don't Skip Sections

If a section doesn't apply, write "N/A" rather than deleting it:
```markdown
## Failure Scenario

N/A — This is an F1 change with minimal risk.
```

### Update Templates Based on Experience

If you find yourself adding the same section repeatedly:
1. Propose adding it to the template
2. Deliberate if significant
3. Update the template

### Review Dates

Templates include review dates. When reviewing:
- Check if all sections are still relevant
- Add sections for new patterns
- Remove obsolete sections
- Update version number

---

## Template Maintenance

### Quarterly Review

Every quarter, check:
- [ ] Are templates being used?
- [ ] Are any sections consistently skipped?
- [ ] Are any sections consistently added manually?
- [ ] Do review dates need updating?

### Version History

When modifying templates:
1. Increment version (1.0 → 1.1 for minor, 2.0 for major)
2. Update review date
3. Note change in CHANGELOG.md

---

## Quick Reference

| I need to... | Use template |
|--------------|--------------|
| Choose between technologies | `architecture-decision.md` |
| Decide if we should build feature X | `feature-assessment.md` |
| Understand why production went down | `incident-review.md` |
| Record that Prophet was right | `prophet-vindication.md` |

---

*Templates are scaffolding. They support construction, then fade into the background.*
