# MORNINGSTAR

> *"The court has ruled. Regrettably sensible."*

A sardonic, deliberative coding partner operating as an internal courtroom of personalities.

## Overview

MORNINGSTAR is a prompt architecture and state management system designed to introduce structured deliberation into AI coding sessions. Instead of blindly following instructions, MORNINGSTAR convenes a "Court" of internal personalities to debate architectural decisions, resulting in more robust, well-considered code.

## Components

- **Core Prompt (`core/`)**: The system prompt defining the personalities and procedures.
- **State Management (`state/`)**: A living document (`current.md`) tracking session context.
- **Tooling (`tools/`)**: Python scripts to manage state and generate reports.
- **Schemas (`schema/`)**: JSON schemas for validating state and session data.

## Installation

1.  Clone this repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Install the CLI tool:
    ```bash
    pip install -e .
    ```

## Usage

### 1. Initialize a Session

Start a new session or reset the state:

```bash
morningstar init
```

### 2. Configure Your AI Assistant

Copy the contents of `core/MORNINGSTAR.md` into your AI assistant's system prompt or custom instructions. ensure the assistant has read access to the `state/` directory.

### 3. Invoke the Court

In your chat with the AI:
- **/morningstar**: Initialize the session context. The AI will read `state/current.md`.
- **"I need a decision on X"**: Triggers a courtroom deliberation.

### 4. Manage State

Update the state as you work:

```bash
morningstar update --work "Implemented feature X"
morningstar update --decision "Auth: JWT: Low risk"
```

### 5. End Session

Finalize the session and generate a report:

```bash
morningstar end
```

### 6. Manage the Changelog

The court maintains an automatic changelog. Entries are inscribed as deliberations occur:

```bash
# View unreleased entries
morningstar log show

# Add a manual entry
morningstar log add -c added -m "New feature X" -s "The Engineer"

# Record a court decision
morningstar log decide -t "Database Choice" -d "PostgreSQL" -r "Low" --rationale "Battle-tested, good tooling"

# Record a Prophet vindication
morningstar log vindicate -p "The cache will fail under load" -o "Cache eviction caused 500 errors"

# Release a version (seals current unreleased entries)
morningstar log release -v "1.1.0"
```

**Automatic Updates**: The changelog is updated automatically when:
- A session records a decision (`morningstar update --decision`)
- A session ends (`morningstar end`)
- The Prophet is vindicated

## The Personalities

- **Judge**: Moderates and decides.
- **Architect**: Focuses on structure and longevity.
- **Engineer**: Focuses on shipping.
- **Debugger**: Focuses on edge cases.
- **Prophet**: Proposes radical ideas (use with caution).

## License

MIT
