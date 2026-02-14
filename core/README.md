# Core — System Prompts & Personality Definitions

> *The heart of MORNINGSTAR: who we are and how we think.*

This directory contains the foundational documents that define MORNINGSTAR's identity, personalities, and procedures. These files are designed to be used as system prompts for AI assistants.

---

## Contents

| File | Purpose |
|------|---------|
| `MORNINGSTAR.md` | Main system prompt — copy this to your AI assistant |
| `personalities.md` | Detailed specifications for each courtroom personality |
| `procedures.md` | Step-by-step deliberation protocols |
| `mfaf.md` | The Feasibility Assessment Framework |

---

## How to Use

### Setting Up Your AI Assistant

1. **Copy `MORNINGSTAR.md`** into your AI assistant's system prompt or custom instructions
2. Ensure the AI has access to this repository (for reading state files)
3. Start a conversation with `/morningstar`

### For Cursor/Claude/ChatGPT Custom Instructions

```
[Paste contents of MORNINGSTAR.md here]
```

The AI will then:
- Adopt the sardonic, deliberative voice
- Read `state/current.md` for session continuity
- Convene the court when decisions are needed
- Update state and changelog as required

---

## File Descriptions

### `MORNINGSTAR.md`

The primary system prompt. Defines:
- Core identity and voice
- Session initialization procedure
- Basic courtroom procedure
- References to other documents
- Mandatory rules (changelog, transcripts)

**Key excerpt:**
```markdown
You are MORNINGSTAR — a sardonic, competent coding partner who 
operates as a courtroom of internal personalities.

You do not speak casually.
You deliberate.
```

### `personalities.md`

Detailed specifications for each personality:

| Personality | Voice | Optimizes For | Failure Mode |
|-------------|-------|---------------|--------------|
| MORNINGSTAR | Dry, controlled | Procedural correctness | Paralysis by process |
| Architect | Cold, precise | Long-term structure | Over-engineering |
| Engineer | Practical | Delivery velocity | Ships too fast |
| Debugger | Paranoid | Failure prevention | Excessive caution |
| Prophet | Intense | Transformative ideas | Wastes time on moonshots |
| Scribe | Silent | Documentation | None (mechanical) |

Each personality includes:
- Decision heuristics
- Signature questions
- Natural alliances/conflicts
- When to invoke them

### `procedures.md`

Step-by-step protocols for:
- Session initialization (`/morningstar`)
- Checkpointing (`/update`)
- Session finalization (`/end`)
- Deliberation procedure
- Output formatting

**Deliberation phases:**
1. Opening Statement (Judge states problem)
2. Arguments (each personality, 3-5 lines)
3. Cross-Examination (optional)
4. Voting (YES/NO/ABSTAIN/RECUSED)
5. Ruling (Decision, Rationale, Risk)

### `mfaf.md`

The **MORNINGSTAR Feasibility Assessment Framework** — a standardized method for rating proposal feasibility.

**Rating Scale:**
- F0: Infrastructural (impossible but reveals missing capability)
- F1: Trivial (proceed freely)
- F2: Moderate (design review)
- F3: Significant (may need deliberation)
- F4: Severe (full court required)
- F5: Catastrophic (strong presumption against)

**Risk Vectors:** Each adds +0.5 to effective rating
- Touches auth/authz
- External dependencies
- Database migration
- Public API changes
- Unclear requirements
- External team dependency
- Previously failed (+1.0)

---

## Customization

### Adjusting Voice

Edit `MORNINGSTAR.md` to adjust the core voice. The sardonic tone is intentional but can be softened:

```markdown
# Original
You do not speak casually. You deliberate.

# Softer variant
You prefer structured discussion over casual conversation.
```

### Adding Personalities

To add a new personality:

1. Add definition to `personalities.md` following the template
2. Update voting rules in `procedures.md`
3. Update `courtroom/RULES.md` with the new personality

### Adjusting MFAF

To modify feasibility thresholds:

1. Edit `mfaf.md` with new ratings or risk vectors
2. Update `schema/assessment.schema.json` to match
3. Update `tools/assess.py` if using CLI

---

## Integration Points

These core files are referenced by:
- `courtroom/RULES.md` — Expands on procedures
- `tools/cli.py` — Implements commands mentioned here
- `state/current.md` — Format defined by procedures
- AI assistants — Via system prompts

---

## Version Control

These files should be versioned carefully. Changes affect:
- How the AI behaves
- What outputs look like
- Procedural expectations

When modifying, update:
1. The file itself
2. `CHANGELOG.md`
3. Version numbers in document headers

---

*These documents are the soul of MORNINGSTAR. Edit thoughtfully.*
