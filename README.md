# MORNINGSTAR

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=white)
![AI Agents](https://img.shields.io/badge/AI%20Agents-673AB7?style=for-the-badge&logo=robots&logoColor=white)

> *"The court has ruled. Regrettably sensible."*

MORNINGSTAR is a **deliberative coding framework** that transforms AI coding assistance into a structured decision-making process. Instead of receiving single-perspective answers, you engage with a **courtroom of personalities** who debate, vote, and deliver reasoned rulings.

---

![Last Commit](https://img.shields.io/github/last-commit/Exios66/Morningstar?style=flat-square)
![Stars](https://img.shields.io/github/stars/Exios66/Morningstar?style=flat-square)
![Forks](https://img.shields.io/github/forks/Exios66/Morningstar?style=flat-square)
![Open Issues](https://img.shields.io/github/issues/Exios66/Morningstar?style=flat-square)
![Version](https://img.shields.io/badge/version-0.0.1-blue?style=flat-square)

---

## What is MORNINGSTAR?

MORNINGSTAR operates as an internal courtroom with distinct personalities:

| Personality | Role | Bias |
| ----------- | ---- | ---- |
| **The Honorable Lucius J. Morningstar** | Judge | Procedural correctness |
| **Edward Cullen** | Consultant (to Judge) | Perspective on the unspoken |
| **Architect** | Voter | Long-term structure |
| **Engineer** | Voter | Practical delivery |
| **Debugger** | Voter | Failure prevention |
| **Prophet** | Voter | Radical alternatives |
| **Scribe** | Recorder | Documentation |
| **[Specialist]** | Voter (when seated) | Domain expertise |

When you face a significant decision, the court **deliberates**: each personality argues their position, votes are cast, and a ruling is delivered with rationale and acknowledged risks.

The Judge may invoke **Edward Cullen** as Judicial Consultant—once per deliberation—to offer perspective on what remains unspoken: hidden motivations, unconsidered implications, the emotional substrate beneath technical debate.

For matters requiring domain expertise outside traditional coding scope, the court may summon **Expert Witnesses** (advisory) or seat **Specialists** (voting members).

---

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <https://github.com/Exios66/Morningstar>
cd Morningstar

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install CLI tool
pip install -e .
```

### 2. Initialize Your First Session

```bash
# Initialize the court
morningstar init

# Check system health
morningstar doctor
```

### 3. Start Working with the Court

**Option A: Use with AI Assistant**

Copy the contents of `core/MORNINGSTAR.md` into your AI assistant's system prompt or custom instructions. Then in your chat:

```
/morningstar
```

The AI will adopt the MORNINGSTAR personality and begin a deliberative session.

**Option B: Use CLI Tools Directly**

```bash
# Record a decision
morningstar decide "Use PostgreSQL" -d "ACID compliance needed" --risk Low

# Check current state
morningstar status

# End session and generate report
morningstar end
```

---

## Directory Structure

```bash
Morningstar/
├── README.md                 # You are here
├── CHANGELOG.md              # Version history (auto-updated by court)
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Package configuration
│
├── core/                     # System prompt & personality definitions
│   ├── MORNINGSTAR.md        # Main system prompt
│   ├── personalities.md      # Detailed personality specs
│   ├── procedures.md         # Deliberation protocols
│   ├── mfaf.md               # Feasibility Assessment Framework
│   └── sme-framework.md      # Subject Matter Expert protocols
│
├── domains/                  # SME domain registry
│   ├── experts.yaml          # Domain definitions and heuristics
│   └── README.md             # Domain registry documentation
│
├── courtroom/                # Rules, best practices, transcripts
│   ├── RULES.md              # Complete courtroom law
│   ├── BEST_PRACTICES.md     # Practical guidance
│   └── transcripts/          # Historical deliberations
│
├── schema/                   # JSON validation schemas
│   ├── state.schema.json
│   ├── session.schema.json
│   ├── deliberation.schema.json
│   └── assessment.schema.json
│
├── state/                    # Active session data
│   ├── current.md            # Current session state
│   ├── f0-registry.md        # "Impossible" ideas registry
│   └── assessments/          # MFAF assessments
│
├── sessions/                 # Archived session reports
│
├── templates/                # Reusable deliberation templates
│
├── tools/                    # Python CLI and utilities
│
├── examples/                 # Example deliberations
│
└── backups/                  # State backups (auto-generated)
```

Each directory has its own README.md with detailed documentation.

---

## Key Commands

### Session Management

| Command | Description |
| ------- | ----------- |
| `morningstar init` | Initialize a new session |
| `morningstar status` | Display current state |
| `morningstar update --work "item"` | Add work item |
| `morningstar decide "topic" -d "decision"` | Record a decision |
| `morningstar end` | End session, generate report |

### Court Operations

| Command | Description |
| ------- | ----------- |
| `morningstar convene` | Display courtroom header |
| `morningstar oracle "question"` | Invoke only the Prophet |
| `morningstar doctor` | System health check |

### Subject Matter Experts

| Command | Description |
| ------- | ----------- |
| `/summon <domain>-expert` | Call Expert Witness (advisory) |
| `/seat <domain>-specialist` | Seat Specialist (Judge only, F3+) |
| `/dismiss <domain>` | End SME participation |

Available domains: `security`, `database`, `compliance`, `infrastructure`, `performance`, `accessibility`, `ux`, `legal`, `cryptography`, `api_design`, `testing`

### MFAF Assessments

| Command | Description |
| ------- | ----------- |
| `morningstar assess new "proposal"` | Create feasibility assessment |
| `morningstar assess list` | View recent assessments |
| `morningstar assess f0` | View F0 Registry |

### Changelog & History

| Command | Description |
| ------- | ----------- |
| `morningstar log show` | View unreleased changes |
| `morningstar log add -m "message"` | Add changelog entry |
| `morningstar log release -v "1.0.0"` | Release a version |
| `morningstar history` | List past sessions |
| `morningstar recall 1` | View a past session |

### Backup & Export

| Command | Description |
| ------- | ----------- |
| `morningstar bkp create` | Create state backup |
| `morningstar bkp list` | List backups |
| `morningstar bkp restore 1` | Restore from backup |
| `morningstar export state` | Export state to JSON |
| `morningstar export session file.md` | Export to HTML |

---

## How Deliberation Works

### 1. Opening Statement

The Judge states the problem clearly.

### 2. Arguments

Each personality argues briefly (3-5 lines) from their perspective.

### 3. Voting

Each voting personality casts: `YES`, `NO`, `ABSTAIN`, or `RECUSED`.

### 4. Ruling

The Judge delivers the decision with:

- **Decision**: What was decided
- **Rationale**: Why
- **Risk**: What could go wrong

### Example Output

```
┌─────────────────────────────────────────────────────────────────┐
│ MATTER BEFORE THE COURT                                         │
│ Which database should we use for the new service?               │
└─────────────────────────────────────────────────────────────────┘

ARCHITECT: PostgreSQL offers relational integrity we'll need as the
schema evolves. This will age well.

ENGINEER: MongoDB would ship faster. We can migrate later if needed.
Can we iterate on this?

DEBUGGER: What happens when the schema changes? MongoDB's flexibility
becomes a liability. I've seen this fail.

PROPHET: What if we don't need a database at all? Event sourcing
with append-only logs would make this trivial.

┌─────────────────────────────────────────────────────────────────┐
│ VOTES                                                           │
├─────────────────────────────────────────────────────────────────┤
│ Architect: YES (PostgreSQL)                                     │
│ Engineer:  NO  (prefers MongoDB)                                │
│ Debugger:  YES (PostgreSQL)                                     │
│ Prophet:   ABSTAIN                                              │
└─────────────────────────────────────────────────────────────────┘

RULING:
  DECISION: Use PostgreSQL
  RATIONALE: Relational integrity outweighs initial velocity
  RISK: Slower initial development; migration if wrong
```

---

## The MFAF (Feasibility Assessment Framework)

Rate proposals using standardized feasibility levels:

| Rating | Label | Meaning |
| ------ | ----- | ------- |
| **F0** | Infrastructural | Currently impossible; reveals missing capability |
| **F1** | Trivial | Safe to proceed without deliberation |
| **F2** | Moderate | Needs design review |
| **F3** | Significant | Requires deliberation |
| **F4** | Severe | Full court required |
| **F5** | Catastrophic | Strong presumption against |

**Risk vectors** add +0.5 each (auth, dependencies, database, API, unclear requirements, external teams). Previously failed attempts add +1.0.

---

## When to Use MORNINGSTAR

**Use for:**

- Architectural decisions
- Technology choices
- Complex implementation strategies
- Debugging approaches
- Any decision with trade-offs

**Skip for:**

- Trivial changes (F1)
- Single obvious solutions
- Time-critical emergencies (log for later)

---

## Philosophy

MORNINGSTAR exists because good decisions require:

1. **Multiple perspectives** — No single viewpoint captures all concerns
2. **Structured debate** — Unstructured discussion leads to loudest-voice-wins
3. **Recorded rationale** — Future you will want to know why
4. **Acknowledged risk** — Every decision has downsides; name them

The sardonic tone serves a purpose: it prevents taking ourselves too seriously while taking our work seriously.

---

## Getting Help

- **`morningstar doctor`** — Diagnose installation issues
- **`courtroom/RULES.md`** — Complete procedural reference
- **`courtroom/BEST_PRACTICES.md`** — Practical guidance
- **`courtroom/transcripts/`** — Example deliberations

---

## License

MIT

---

*"We have built a machine for saying 'no' thoughtfully. That may be the best we can hope for."*

— MORNINGSTAR
