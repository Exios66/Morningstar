# Schema — JSON Validation Schemas

> *Structure ensures consistency. Consistency enables automation.*

This directory contains JSON Schema definitions for validating MORNINGSTAR data structures. These schemas ensure that state files, session reports, and assessments maintain consistent formats.

---

## Contents

| File | Validates | Used By |
|------|-----------|---------|
| `state.schema.json` | `state/current.md` (parsed) | `tools/state.py`, `tools/validate.py` |
| `session.schema.json` | Session reports | `tools/session.py` |
| `deliberation.schema.json` | Deliberation outputs | Manual validation |
| `assessment.schema.json` | MFAF assessments | `tools/assess.py` |

---

## Schema Descriptions

### `state.schema.json`

Validates the parsed state object from `state/current.md`.

**Required fields:**
- `lastUpdated` — ISO 8601 timestamp
- `activeWork` — Array of strings
- `decisions` — Array of decision objects
- `outstandingIssues` — Array of issue objects

**Decision object:**
```json
{
  "topic": "string",
  "decision": "string",
  "rationale": "string",
  "risk": "string",
  "votes": {
    "Architect": "YES|NO|ABSTAIN|RECUSED",
    "Engineer": "YES|NO|ABSTAIN|RECUSED",
    "Debugger": "YES|NO|ABSTAIN|RECUSED",
    "Prophet": "YES|NO|ABSTAIN|RECUSED"
  },
  "dissents": [
    {
      "personality": "Architect|Engineer|Debugger|Prophet",
      "opinion": "string"
    }
  ]
}
```

**Issue object:**
```json
{
  "issue": "string",
  "severity": "Low|Medium|High|Critical"
}
```

### `session.schema.json`

Validates session report structure.

**Required fields:**
- `sessionId` — Unique identifier
- `startTime` — ISO 8601 timestamp
- `endTime` — ISO 8601 timestamp
- `workCompleted` — Array of strings

**Optional fields:**
- `decisionsMade` — Array of decision objects
- `newIssues` — Array of issue objects

### `deliberation.schema.json`

Validates deliberation output structure.

**Fields:**
- `matter` — What was being decided
- `timestamp` — When deliberation occurred
- `arguments` — Object with personality arguments
- `votes` — Vote by each personality
- `outcome` — APPROVED/REJECTED/TIE
- `ruling` — Decision, rationale, risk
- `dissents` — Array of dissenting opinions

### `assessment.schema.json`

Validates MFAF assessment structure.

**Required fields:**
- `proposal` — What's being assessed
- `baseRating` — F0-F5
- `riskVectors` — Object of boolean flags
- `effectiveRating` — Calculated rating
- `effortBand` — S/M/L/XL
- `recommendation` — PROCEED/REVIEW/DELIBERATE/ARCHIVE_F0

---

## Using Schemas

### CLI Validation

```bash
# Validate current state
morningstar validate
```

### Python Validation

```python
from tools.validate import validate_state, validate_assessment

# Validate state
state = read_state()
is_valid, errors = validate_state(state)

if not is_valid:
    for error in errors:
        print(f"Validation error: {error}")
```

### Manual Validation

Using `jsonschema` directly:

```python
import json
from jsonschema import validate, ValidationError

# Load schema
with open('schema/state.schema.json') as f:
    schema = json.load(f)

# Validate data
try:
    validate(instance=data, schema=schema)
    print("Valid")
except ValidationError as e:
    print(f"Invalid: {e.message}")
```

### Command Line Validation

Using `jsonschema` CLI:

```bash
# If you have jsonschema CLI installed
jsonschema -i data.json schema/state.schema.json
```

---

## Schema Format

All schemas use [JSON Schema Draft-07](http://json-schema.org/draft-07/schema#).

**Common patterns:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["field1", "field2"],
  "properties": {
    "field1": {
      "type": "string",
      "description": "Description of field"
    },
    "field2": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

---

## Modifying Schemas

When changing a schema:

1. **Update the schema file**
2. **Test against existing data** — Ensure backward compatibility
3. **Update related code** — `tools/*.py` files that use the schema
4. **Update documentation** — This README, any affected docs
5. **Log in changelog** — Record the schema change

### Adding a Field

```json
{
  "properties": {
    "newField": {
      "type": "string",
      "description": "New field description"
    }
  }
}
```

Note: Don't add to `required` unless you'll update all existing data.

### Making a Field Required

```json
{
  "required": ["existingField", "newRequiredField"]
}
```

⚠️ **Warning:** This is a breaking change. Ensure all existing data has this field.

---

## Validation Errors

Common errors and solutions:

### "Required property 'X' is missing"

**Cause:** Data is missing a required field.
**Solution:** Add the field, or remove from `required` in schema.

### "Type 'X' is not valid under any of the given schemas"

**Cause:** Field value doesn't match expected type.
**Solution:** Check the data type (string vs number, etc.).

### "Enum value not allowed"

**Cause:** Value isn't in the allowed enum list.
**Solution:** Use one of the allowed values, or extend the enum.

---

## Schema Reference

### Common Types

| JSON Type | Description |
|-----------|-------------|
| `string` | Text |
| `number` | Numeric (integer or float) |
| `integer` | Whole numbers only |
| `boolean` | true/false |
| `array` | List of items |
| `object` | Key-value pairs |
| `null` | Null value |

### Common Keywords

| Keyword | Purpose |
|---------|---------|
| `type` | Expected data type |
| `required` | Required properties |
| `properties` | Object property definitions |
| `items` | Array item schema |
| `enum` | Allowed values |
| `format` | String format (date-time, email, etc.) |
| `description` | Human-readable description |

---

## Integration with Tools

### `tools/validate.py`

Provides validation functions:

```python
def validate_state(state: dict) -> tuple[bool, list]:
    """Validate state against schema."""
    # Returns (is_valid, list_of_errors)

def validate_assessment(assessment: dict) -> tuple[bool, list]:
    """Validate MFAF assessment."""
```

### `tools/state.py`

Uses schema for:
- Validating parsed state before write
- Type hints derived from schema

### `tools/assess.py`

Uses schema for:
- Validating created assessments
- Ensuring consistent structure

---

*Schemas are contracts. Honor them.*
