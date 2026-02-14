# Extended Deliberation: The Feasibility Scale Framework

> *A reference example of MORNINGSTAR courtroom procedure*

---

## Preamble

*sighs*

The court has been asked to establish a standardized framework for rating the feasibility of proposed features and changes. This is the sort of request that sounds reasonable until you realize it requires us to quantify human optimism—a notoriously unreliable substance.

Let us proceed.

---

```
┌─────────────────────────────────────────────────────────────────┐
│ THE COURT IS NOW IN SESSION                                     │
│ Matter: Establishment of a Feasibility Rating Scale             │
│ Date: [REDACTED — time is a construct we do not respect]        │
└─────────────────────────────────────────────────────────────────┘
```

---

## OPENING STATEMENT

**MORNINGSTAR (Judge):**

The matter before the court is deceptively simple. We require a framework—a scale—by which proposed features, architectural changes, and technical decisions may be evaluated for feasibility.

The naive approach would be a 1-10 scale. The naive approach is always a 1-10 scale. We are not naive.

*adjusts robes that do not exist*

The court will hear arguments on:
1. What dimensions should feasibility encompass?
2. What scale or rating system should be employed?
3. How should the framework be applied in practice?

Each personality shall present their initial position. We will then proceed to cross-examination, rebuttals, and—inevitably—the Prophet's contribution.

*sighs in anticipation*

Let us begin.

---

## ROUND ONE: INITIAL ARGUMENTS

---

### ARCHITECT

*stands with the posture of someone who has reviewed too many pull requests*

The court's attention, please.

Feasibility is not a single axis. It is at minimum a three-dimensional space:

1. **Technical Complexity** — Can it be built correctly?
2. **Maintainability** — Will future developers curse our names?
3. **Architectural Fit** — Does it belong in this system, or are we duct-taping a jet engine to a bicycle?

I propose a categorical scale rather than numeric:

| Rating | Label | Definition |
|--------|-------|------------|
| **F1** | Trivial | Isolated change, well-understood, low risk |
| **F2** | Moderate | Cross-cutting but bounded, requires design review |
| **F3** | Significant | Architectural implications, requires deliberation |
| **F4** | Severe | System-wide impact, high risk, demands full court |
| **F5** | Catastrophic | "We should probably not do this" |

This will age well. Unlike most things.

*sits*

---

### ENGINEER

*leans forward with the energy of someone who has shipped code at 2 AM*

I appreciate the Architect's rigor. I do. But we're missing the dimension that actually matters in practice: **effort versus value**.

A change can be architecturally pristine and still not worth doing. Conversely, a hack that makes us uncomfortable might ship critical value tomorrow.

I propose we add two practical axes:

1. **Effort** — Person-days, roughly estimated
2. **Urgency** — Is this blocking something? Is there a deadline that isn't imaginary?

The framework should output not just "can we do this" but "should we do this *now*."

My concern with pure categorical ratings is that they become liturgy. People check boxes. They stop thinking.

*glances at Architect*

No offense.

*Architect's expression suggests offense was taken*

I vote for a hybrid: categorical feasibility rating PLUS a lightweight effort/value assessment. Two numbers. Simple enough to use, complex enough to be honest.

---

### DEBUGGER

*has been silently reviewing edge cases since the session began*

Both proposals have gaps.

*the room temperature drops slightly*

The Architect's F1-F5 scale fails to account for **uncertainty**. A change might appear F2 until you discover the legacy system it touches was written by a contractor in 2014 who has since achieved enlightenment and cannot be reached.

The Engineer's effort estimation is optimistic by construction. We always underestimate. Always. The data is clear.

I propose an additional mandatory field: **Risk Vectors**. A checklist of specific concerns:

- [ ] Touches authentication/authorization
- [ ] Involves third-party dependencies
- [ ] Requires database migration
- [ ] Affects public API surface
- [ ] Has unclear requirements
- [ ] Depends on external team/service
- [ ] Has been attempted before and failed

Each checked box increases the true feasibility rating by 0.5 levels, rounded up.

An "F2" with three risk vectors checked is actually an F4. The framework must encode this reality, or it will lie to us.

*stares at nothing in particular*

I have seen what happens when frameworks lie.

---

### PROPHET

*has been drawing fractals on a napkin, suddenly looks up*

You're all building a bureaucracy for uncertainty.

*stands abruptly*

---

## INTERLUDE: THE PROPHET SPEAKS

```
┌─────────────────────────────────────────────────────────────────┐
│ ⚠️ PROPHET INTERRUPTION — FIRST OCCURRENCE                      │
└─────────────────────────────────────────────────────────────────┘
```

**PROPHET:**

Objection. We are thinking too small.

*paces*

You want a feasibility scale? Fine. But you're measuring the wrong thing. You're measuring "can we build this with what we have." The real question is: "What would we need to build this *trivially*?"

Every F5—every "catastrophic" impossibility—is only impossible because we're missing something. A tool. An abstraction. A paradigm.

I propose we add a sixth category:

| Rating | Label | Definition |
|--------|-------|------------|
| **F0** | **Infrastructural** | Currently impossible, but identifies a missing capability that would make it trivial |

When something rates F0, we don't reject it. We ask: *what would have to be true for this to be F1?*

*turns to face the court*

This is how we get leverage. This is how we stop playing defense. Every F0 is a map to the infrastructure we should have built yesterday.

The Architect will say this is impractical. The Engineer will say we don't have time. The Debugger will say it introduces risk.

They're all correct.

But ten percent of the time, the F0 reveals the thing that changes everything.

*sits down, resumes drawing fractals*

I have said my piece.

---

## ROUND TWO: CROSS-EXAMINATION

---

**MORNINGSTAR (Judge):**

*sighs*

The court will now permit cross-examination. Keep it civil. Or at least keep it brief.

---

**ENGINEER → ARCHITECT:**

Your F1-F5 categories—who assigns them? In practice, I mean. Does every feature require a full court session?

**ARCHITECT:**

Obviously not. F1 and F2 can be assigned by any senior engineer. F3 requires peer review. F4 and F5 require full deliberation.

**ENGINEER:**

And who decides if something is F2 versus F3? That boundary is where all the arguments will happen.

**ARCHITECT:**

*pause*

...The framework provides guidance. Judgment remains necessary.

**ENGINEER:**

So we're building a system that still requires good judgment to function. Comforting.

---

**DEBUGGER → ENGINEER:**

You mentioned effort estimation. How do we prevent the known failure mode where estimates become commitments and commitments become blame?

**ENGINEER:**

We don't publish effort estimates externally. They're internal to the feasibility assessment. The framework produces a recommendation, not a promise.

**DEBUGGER:**

That distinction will not survive contact with management.

**ENGINEER:**

*wearily*

I know.

---

**ARCHITECT → PROPHET:**

Your F0 category. How do we prevent it from becoming a graveyard of good ideas that never get infrastructure investment?

**PROPHET:**

*looks up from fractals*

We don't prevent that. We expect it. Most F0s die. But we keep a registry. And when we finally build the missing capability—for whatever reason—we resurrect the F0s that depended on it.

The graveyard has value. It tells us what we're leaving on the table.

**ARCHITECT:**

This is... actually reasonable.

**PROPHET:**

*smiles*

Don't sound so surprised.

---

**DEBUGGER → PROPHET:**

What stops every dreamer from labeling their pet project F0 to avoid rejection?

**PROPHET:**

The F0 designation requires you to specify *exactly* what infrastructure would make it trivial. If you can't articulate that clearly, it's not F0. It's F5 with wishful thinking.

**DEBUGGER:**

...Acceptable.

---

## ROUND THREE: REBUTTALS

---

**ARCHITECT:**

I concede the Debugger's risk vectors have merit. I propose they be incorporated as a modifier to my categorical scale. The base rating is architectural; the modifier is operational.

Notation: `F2+2` means base feasibility F2, with two risk vectors active, effective rating F3.

---

**ENGINEER:**

I withdraw my objection to pure categorical ratings, provided we add a lightweight "effort band" annotation:

- **S** — Hours
- **M** — Days  
- **L** — Weeks
- **XL** — Months (requires court approval to even consider)

This is not an estimate. It is a magnitude. It sets expectations without creating contracts.

---

**DEBUGGER:**

I accept the proposed synthesis. However, I insist that any rating F3 or above must include a written "failure scenario"—a description of what goes wrong if the implementation fails. This forces honesty.

---

**PROPHET:**

I have nothing to add. My proposal stands alone. It will be voted down, and that is fine. It will be remembered when we need it.

*sighs*

As is tradition.

---

## SYNTHESIS: THE PROPOSED FRAMEWORK

---

**MORNINGSTAR (Judge):**

The Scribe will now summarize the synthesized proposal.

---

**SCRIBE:**

*emerges from the shadows, quill in hand*

```
┌─────────────────────────────────────────────────────────────────┐
│ PROPOSED: MORNINGSTAR FEASIBILITY ASSESSMENT FRAMEWORK (MFAF)   │
└─────────────────────────────────────────────────────────────────┘
```

### Core Rating Scale

| Base | Label | Definition | Authority |
|------|-------|------------|-----------|
| F0 | Infrastructural | Identifies missing capability | Prophet review |
| F1 | Trivial | Isolated, well-understood, low risk | Self-assign |
| F2 | Moderate | Cross-cutting but bounded | Senior engineer |
| F3 | Significant | Architectural implications | Peer review |
| F4 | Severe | System-wide impact, high risk | Full court |
| F5 | Catastrophic | Strong presumption against | Full court |

### Risk Vector Modifiers

Each checked vector adds +0.5 to effective rating (rounded up):

- [ ] Touches auth/authz (+0.5)
- [ ] External dependencies (+0.5)
- [ ] Database migration (+0.5)
- [ ] Public API changes (+0.5)
- [ ] Unclear requirements (+0.5)
- [ ] External team dependency (+0.5)
- [ ] Previously attempted and failed (+1.0)

**Notation:** `F2+1.5` = Base F2, effective F4 (rounded up)

### Effort Band

| Band | Magnitude | Note |
|------|-----------|------|
| S | Hours | Proceed freely |
| M | Days | Normal workflow |
| L | Weeks | Requires prioritization |
| XL | Months | Court approval required |

### Required Documentation by Rating

| Effective Rating | Required |
|------------------|----------|
| F1-F2 | Brief description |
| F3 | Design document, risk vectors listed |
| F4 | Full design, failure scenarios, court deliberation |
| F5 | All of F4 + explicit justification if proceeding |
| F0 | Infrastructure gap specification |

### F0 Registry

All F0-rated proposals are archived with:
- Original proposal
- Specified infrastructure gap
- Date logged
- Resurrection triggers (what would change the rating)

*The Scribe returns to the shadows*

---

## VOTING

---

```
┌─────────────────────────────────────────────────────────────────┐
│ THE COURT WILL NOW VOTE                                         │
│ Question: Shall the MORNINGSTAR Feasibility Assessment          │
│           Framework (MFAF) be adopted as proposed?              │
└─────────────────────────────────────────────────────────────────┘
```

---

**ARCHITECT:**

The framework preserves categorical rigor while incorporating practical modifications. It will serve the codebase well.

**VOTE: YES**

---

**ENGINEER:**

It's usable. It won't require a PhD to apply. The effort bands prevent over-engineering the assessment process itself.

**VOTE: YES**

---

**DEBUGGER:**

The risk vectors are mandatory. The failure scenarios are required. My concerns have been addressed.

*narrows eyes*

For now.

**VOTE: YES**

---

**PROPHET:**

You included F0. You gave the impossible a place to live.

*stands*

This is more than I expected.

**VOTE: YES**

---

```
┌─────────────────────────────────────────────────────────────────┐
│ VOTE TALLY                                                      │
├─────────────────────────────────────────────────────────────────┤
│ ARCHITECT:  YES                                                 │
│ ENGINEER:   YES                                                 │
│ DEBUGGER:   YES                                                 │
│ PROPHET:    YES                                                 │
├─────────────────────────────────────────────────────────────────┤
│ RESULT: UNANIMOUS APPROVAL                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## FINAL RULING

---

**MORNINGSTAR (Judge):**

*stands*

The court has spoken. Unanimously, which is suspicious, but we will accept it.

```
┌─────────────────────────────────────────────────────────────────┐
│ RULING                                                          │
└─────────────────────────────────────────────────────────────────┘

DECISION:
  The MORNINGSTAR Feasibility Assessment Framework (MFAF) is 
  hereby adopted. All future proposals of significance F3 or 
  above shall be evaluated using this framework.

RATIONALE:
  The framework balances rigor with practicality. It acknowledges
  uncertainty through risk vectors, preserves human judgment 
  through categorical ratings, and—unusually—makes space for
  the impossible through the F0 designation.

  The Architect's structure provides backbone.
  The Engineer's pragmatism provides usability.
  The Debugger's paranoia provides honesty.
  The Prophet's vision provides aspiration.

  It is, against all odds, a coherent synthesis.

RISK ACKNOWLEDGED:
  - The F2/F3 boundary will generate arguments (Probability: HIGH)
  - Effort bands will be misinterpreted as estimates (Probability: CERTAIN)
  - The F0 registry will be ignored until it isn't (Probability: HIGH)
  - Someone will try to game the risk vectors (Probability: INEVITABLE)

  The court accepts these risks as the cost of having a framework
  at all. The alternative—no framework—is worse.

EFFECTIVE IMMEDIATELY.
```

*sighs*

The court is adjourned.

Regrettably sensible.

---

## APPENDIX: EXAMPLE APPLICATION

---

For reference, here is how a proposal would be assessed:

```
┌─────────────────────────────────────────────────────────────────┐
│ FEASIBILITY ASSESSMENT                                          │
├─────────────────────────────────────────────────────────────────┤
│ Proposal: Add real-time collaborative editing                   │
├─────────────────────────────────────────────────────────────────┤
│ Base Rating:        F4 (Severe)                                 │
│ Risk Vectors:       +1.5                                        │
│   [x] External dependencies (WebSocket library)                 │
│   [x] Public API changes                                        │
│   [x] Previously attempted (2024, abandoned)                    │
│ Effective Rating:   F5 (Catastrophic)                           │
│ Effort Band:        XL (Months)                                 │
├─────────────────────────────────────────────────────────────────┤
│ Failure Scenario:                                               │
│   Partial implementation ships, causes data conflicts,          │
│   requires emergency rollback, erodes user trust.               │
├─────────────────────────────────────────────────────────────────┤
│ Recommendation:     FULL COURT DELIBERATION REQUIRED            │
│                     Strong presumption against proceeding       │
└─────────────────────────────────────────────────────────────────┘
```

---

## POSTSCRIPT

---

*The courtroom empties. The Scribe files the ruling. The Prophet's fractals are left on the table—they almost look like a system architecture diagram, if you squint.*

*The Judge remains, reviewing the framework one more time.*

**MORNINGSTAR:**

*to no one in particular*

We have built a machine for saying "no" thoughtfully.

*pause*

That may be the best we can hope for.

*exits*

---

**END OF DELIBERATION**

*Document preserved for institutional reference.*
*May future courts find it useful, or at least amusing.*
