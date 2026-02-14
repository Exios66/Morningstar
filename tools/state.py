import re
import os
from datetime import datetime
from dateutil import parser as date_parser
from typing import Optional, Tuple, List, Dict, Any

STATE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'state', 'current.md')

# Valid severity levels
VALID_SEVERITIES = ['Low', 'Medium', 'High', 'Critical']

# Valid vote values
VALID_VOTES = ['YES', 'NO', 'ABSTAIN', 'RECUSED']


class StateParseError(Exception):
    """Raised when state parsing fails in strict mode."""
    pass


def parse_list_item(line: str) -> str:
    """Extract content from a markdown list item."""
    return line.strip().lstrip('- ').strip()


def parse_decision(line: str) -> Dict[str, Any]:
    """
    Parse a decision line.
    Format: "- [topic]: [decision] — [risk]" or variations
    Returns a decision dict with optional votes and dissents.
    """
    item = parse_list_item(line)
    
    # Try to parse with em-dash separator
    parts = re.split(r':\s*|—\s*|--\s*', item)
    
    decision = {
        "topic": "Unknown",
        "decision": "Unknown", 
        "rationale": "See logs",
        "risk": "Unknown",
        "votes": {},
        "dissents": []
    }
    
    if len(parts) >= 3:
        decision["topic"] = parts[0].strip()
        decision["decision"] = parts[1].strip()
        decision["risk"] = parts[-1].strip()
    elif len(parts) == 2:
        decision["topic"] = parts[0].strip()
        decision["decision"] = parts[1].strip()
    elif len(parts) == 1 and parts[0]:
        decision["topic"] = parts[0].strip()
    
    return decision


def parse_issue(line: str) -> Dict[str, str]:
    """
    Parse an issue line.
    Format: "- [issue]: [severity]" or "- [issue] — [severity]"
    """
    item = parse_list_item(line)
    
    # Try multiple separators
    for sep in [':', '—', '--']:
        if sep in item:
            parts = item.rsplit(sep, 1)
            if len(parts) == 2:
                severity = parts[1].strip()
                # Validate and normalize severity
                severity = normalize_severity(severity)
                return {"issue": parts[0].strip(), "severity": severity}
    
    return {"issue": item, "severity": "Medium"}


def normalize_severity(severity: str) -> str:
    """Normalize severity to valid values."""
    severity_lower = severity.lower()
    for valid in VALID_SEVERITIES:
        if severity_lower == valid.lower():
            return valid
    # Fuzzy matching
    if 'crit' in severity_lower:
        return 'Critical'
    if 'high' in severity_lower:
        return 'High'
    if 'low' in severity_lower:
        return 'Low'
    return 'Medium'


def parse_vindication(line: str) -> str:
    """Parse a vindication entry."""
    return parse_list_item(line)


def parse_dissent_vindication(line: str) -> Optional[Dict[str, str]]:
    """
    Parse a dissent vindication line.
    Format: "- [decision]: [dissenter] predicted [prediction] — [outcome]"
    """
    item = parse_list_item(line)
    # This is complex; for now, store as string and parse later if needed
    return {"raw": item}


def read_state(strict: bool = False) -> Optional[Dict[str, Any]]:
    """
    Read and parse the state file.
    
    Args:
        strict: If True, raise StateParseError on parsing issues
        
    Returns:
        Parsed state dictionary, or None if file doesn't exist
    """
    if not os.path.exists(STATE_FILE):
        return None

    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except IOError as e:
        if strict:
            raise StateParseError(f"Failed to read state file: {e}")
        return None

    state = {
        "lastUpdated": datetime.now().isoformat(),
        "activeWork": [],
        "decisions": [],
        "outstandingIssues": [],
        "prophetVindications": [],
        "dissentVindications": [],
        "nextSession": []
    }

    current_section = None
    parse_warnings = []

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        
        # Section headers
        if line.startswith('## '):
            section_name = line[3:].lower()
            if 'last updated' in section_name:
                current_section = 'lastUpdated'
            elif 'active work' in section_name:
                current_section = 'activeWork'
            elif 'decisions' in section_name:
                current_section = 'decisions'
            elif 'outstanding' in section_name:
                current_section = 'outstandingIssues'
            elif 'prophet' in section_name and 'vindication' in section_name:
                current_section = 'prophetVindications'
            elif 'dissent' in section_name and 'vindication' in section_name:
                current_section = 'dissentVindications'
            elif 'next session' in section_name:
                current_section = 'nextSession'
            elif 'recent' in section_name:
                current_section = 'recentAdditions'  # Ignored but recognized
            else:
                current_section = None
                parse_warnings.append(f"Line {line_num}: Unrecognized section '{line}'")
            continue
        
        # List items
        if line.startswith('- ') and current_section:
            try:
                if current_section == 'activeWork':
                    state['activeWork'].append(parse_list_item(line))
                elif current_section == 'decisions':
                    state['decisions'].append(parse_decision(line))
                elif current_section == 'outstandingIssues':
                    state['outstandingIssues'].append(parse_issue(line))
                elif current_section == 'prophetVindications':
                    state['prophetVindications'].append(parse_vindication(line))
                elif current_section == 'dissentVindications':
                    vindication = parse_dissent_vindication(line)
                    if vindication:
                        state['dissentVindications'].append(vindication)
                elif current_section == 'nextSession':
                    state['nextSession'].append(parse_list_item(line))
            except Exception as e:
                parse_warnings.append(f"Line {line_num}: Failed to parse '{line[:50]}...': {e}")
                if strict:
                    raise StateParseError(f"Parse error at line {line_num}: {e}")
                    
        # Timestamp (special case - not a list item)
        elif current_section == 'lastUpdated' and not line.startswith('#'):
            try:
                clean_ts = line.strip('[]')
                date_parser.parse(clean_ts)
                state['lastUpdated'] = clean_ts
            except Exception:
                parse_warnings.append(f"Line {line_num}: Invalid timestamp '{line}'")
                if strict:
                    raise StateParseError(f"Invalid timestamp at line {line_num}: {line}")

    # Store warnings for diagnostic purposes
    state['_parseWarnings'] = parse_warnings
    
    return state


def validate_state(state: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate state structure without full JSON schema validation.
    Returns (is_valid, list_of_errors).
    """
    errors = []
    
    # Required fields
    required = ['lastUpdated', 'activeWork', 'decisions', 'outstandingIssues']
    for field in required:
        if field not in state:
            errors.append(f"Missing required field: {field}")
    
    # Type checks
    if 'activeWork' in state and not isinstance(state['activeWork'], list):
        errors.append("activeWork must be a list")
    
    if 'decisions' in state:
        if not isinstance(state['decisions'], list):
            errors.append("decisions must be a list")
        else:
            for i, d in enumerate(state['decisions']):
                if not isinstance(d, dict):
                    errors.append(f"decisions[{i}] must be a dict")
                elif 'topic' not in d:
                    errors.append(f"decisions[{i}] missing 'topic'")
    
    if 'outstandingIssues' in state:
        if not isinstance(state['outstandingIssues'], list):
            errors.append("outstandingIssues must be a list")
        else:
            for i, issue in enumerate(state['outstandingIssues']):
                if not isinstance(issue, dict):
                    errors.append(f"outstandingIssues[{i}] must be a dict")
                elif 'severity' in issue and issue['severity'] not in VALID_SEVERITIES:
                    errors.append(f"outstandingIssues[{i}] has invalid severity: {issue['severity']}")
    
    return len(errors) == 0, errors


def repair_state(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Attempt to repair common state issues.
    Returns a repaired copy of the state.
    """
    repaired = state.copy()
    
    # Ensure required fields exist
    if 'activeWork' not in repaired:
        repaired['activeWork'] = []
    if 'decisions' not in repaired:
        repaired['decisions'] = []
    if 'outstandingIssues' not in repaired:
        repaired['outstandingIssues'] = []
    if 'prophetVindications' not in repaired:
        repaired['prophetVindications'] = []
    if 'dissentVindications' not in repaired:
        repaired['dissentVindications'] = []
    if 'nextSession' not in repaired:
        repaired['nextSession'] = []
    if 'lastUpdated' not in repaired:
        repaired['lastUpdated'] = datetime.now().isoformat()
    
    # Fix severity values
    for issue in repaired.get('outstandingIssues', []):
        if 'severity' in issue:
            issue['severity'] = normalize_severity(issue['severity'])
    
    # Ensure decisions have required fields
    for decision in repaired.get('decisions', []):
        if 'topic' not in decision:
            decision['topic'] = 'Unknown'
        if 'decision' not in decision:
            decision['decision'] = 'Unknown'
        if 'rationale' not in decision:
            decision['rationale'] = 'See logs'
        if 'risk' not in decision:
            decision['risk'] = 'Unknown'
    
    return repaired

def write_state(state: Dict[str, Any]) -> None:
    """
    Write state to markdown file.
    Handles new fields like dissents and vote tallies.
    """
    lines = []
    lines.append("# Session State")
    lines.append("")
    
    lines.append("## Last Updated")
    lines.append(f"[{state.get('lastUpdated', datetime.now().isoformat())}]")
    lines.append("")

    lines.append("## Active Work")
    for item in state.get('activeWork', []):
        lines.append(f"- {item}")
    lines.append("")

    lines.append("## Decisions Made")
    for d in state.get('decisions', []):
        decision_line = f"- {d.get('topic', 'Unknown')}: {d.get('decision', 'Unknown')} — {d.get('risk', 'Unknown')}"
        
        # Add vote tally if present
        votes = d.get('votes', {})
        if votes:
            vote_str = ', '.join([f"{k}:{v}" for k, v in votes.items() if v])
            if vote_str:
                decision_line += f" [{vote_str}]"
        
        lines.append(decision_line)
        
        # Add dissents as sub-items
        for dissent in d.get('dissents', []):
            lines.append(f"  - *Dissent ({dissent.get('personality', 'Unknown')})*: {dissent.get('opinion', '')}")
    lines.append("")

    lines.append("## Outstanding Issues")
    for i in state.get('outstandingIssues', []):
        lines.append(f"- {i.get('issue', 'Unknown')}: {i.get('severity', 'Medium')}")
    lines.append("")

    lines.append("## Prophet's Vindications")
    for p in state.get('prophetVindications', []):
        lines.append(f"- {p}")
    if not state.get('prophetVindications'):
        lines.append("- None (yet)")
    lines.append("")

    lines.append("## Dissent Vindications")
    for dv in state.get('dissentVindications', []):
        if isinstance(dv, dict):
            if 'raw' in dv:
                lines.append(f"- {dv['raw']}")
            else:
                lines.append(f"- {dv.get('originalDecision', 'Unknown')}: {dv.get('dissenter', 'Unknown')} was right — {dv.get('outcome', '')}")
        else:
            lines.append(f"- {dv}")
    if not state.get('dissentVindications'):
        lines.append("- None (yet)")
    lines.append("")

    lines.append("## Next Session")
    for n in state.get('nextSession', []):
        lines.append(f"- {n}")
    lines.append("")

    # Ensure directory exists
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def init_state() -> Dict[str, Any]:
    """Initialize a fresh state file."""
    state = {
        "lastUpdated": datetime.now().isoformat(),
        "activeWork": ["Initialize Morningstar System"],
        "decisions": [],
        "outstandingIssues": [],
        "prophetVindications": [],
        "dissentVindications": [],
        "nextSession": []
    }
    write_state(state)
    return state


def add_decision(topic: str, decision: str, risk: str, rationale: str = "See logs",
                 votes: Optional[Dict[str, str]] = None, 
                 dissents: Optional[List[Dict[str, str]]] = None) -> None:
    """
    Add a decision to the current state.
    
    Args:
        topic: What was decided
        decision: The ruling
        risk: Risk level
        rationale: Explanation
        votes: Dict of personality -> vote
        dissents: List of {personality, opinion} dicts
    """
    state = read_state()
    if not state:
        state = init_state()
    
    state['lastUpdated'] = datetime.now().isoformat()
    
    new_decision = {
        "topic": topic,
        "decision": decision,
        "rationale": rationale,
        "risk": risk,
        "votes": votes or {},
        "dissents": dissents or []
    }
    
    state['decisions'].append(new_decision)
    write_state(state)


def add_dissent_vindication(original_decision: str, dissenter: str, 
                           prediction: str, outcome: str) -> None:
    """
    Record when a dissenting opinion was proven correct.
    """
    state = read_state()
    if not state:
        state = init_state()
    
    state['lastUpdated'] = datetime.now().isoformat()
    
    vindication = {
        "originalDecision": original_decision,
        "dissenter": dissenter,
        "prediction": prediction,
        "outcome": outcome
    }
    
    if 'dissentVindications' not in state:
        state['dissentVindications'] = []
    
    state['dissentVindications'].append(vindication)
    write_state(state)
