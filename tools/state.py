import re
import os
from datetime import datetime
from dateutil import parser as date_parser

STATE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'state', 'current.md')

def parse_list_item(line):
    return line.strip().lstrip('- ').strip()

def parse_decision(line):
    # Format: "- [topic]: [decision] — [risk]" or just text if format varies
    # We'll try to split by ':' and '—'
    # Fallback to generic if parsing fails
    item = parse_list_item(line)
    parts = re.split(r':\s*|—\s*', item)
    if len(parts) >= 3:
        return {
            "topic": parts[0].strip(),
            "decision": parts[1].strip(),
            "rationale": "See logs", # Rationale often lost in summary line
            "risk": parts[-1].strip()
        }
    return {"topic": item, "decision": "Unknown", "rationale": "Unknown", "risk": "Unknown"}

def parse_issue(line):
    # Format: "- [issue]: [severity]"
    item = parse_list_item(line)
    parts = item.rsplit(':', 1)
    if len(parts) == 2:
        return {"issue": parts[0].strip(), "severity": parts[1].strip()}
    return {"issue": item, "severity": "Medium"} # Default

def read_state():
    if not os.path.exists(STATE_FILE):
        return None

    with open(STATE_FILE, 'r') as f:
        lines = f.readlines()

    state = {
        "lastUpdated": datetime.now().isoformat(),
        "activeWork": [],
        "decisions": [],
        "outstandingIssues": [],
        "prophetVindications": [],
        "nextSession": []
    }

    current_section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
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
            elif 'prophet' in section_name:
                current_section = 'prophetVindications'
            elif 'next session' in section_name:
                current_section = 'nextSession'
            continue
        
        if line.startswith('- ') and current_section:
            if current_section == 'activeWork':
                state['activeWork'].append(parse_list_item(line))
            elif current_section == 'decisions':
                state['decisions'].append(parse_decision(line))
            elif current_section == 'outstandingIssues':
                state['outstandingIssues'].append(parse_issue(line))
            elif current_section == 'prophetVindications':
                state['prophetVindications'].append(parse_list_item(line))
            elif current_section == 'nextSession':
                state['nextSession'].append(parse_list_item(line))
        elif current_section == 'lastUpdated' and not line.startswith('#'):
            try:
                # remove brackets if present [timestamp]
                clean_ts = line.strip('[]')
                # validate parsing
                date_parser.parse(clean_ts)
                state['lastUpdated'] = clean_ts
            except:
                pass

    return state

def write_state(state):
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
        lines.append(f"- {d.get('topic', 'Unknown')}: {d.get('decision', 'Unknown')} — {d.get('risk', 'Unknown')}")
    lines.append("")

    lines.append("## Outstanding Issues")
    for i in state.get('outstandingIssues', []):
        lines.append(f"- {i.get('issue', 'Unknown')}: {i.get('severity', 'Medium')}")
    lines.append("")

    lines.append("## Prophet's Vindications")
    for p in state.get('prophetVindications', []):
        lines.append(f"- {p}")
    lines.append("")

    lines.append("## Next Session")
    for n in state.get('nextSession', []):
        lines.append(f"- {n}")
    lines.append("")

    with open(STATE_FILE, 'w') as f:
        f.write('\n'.join(lines))

def init_state():
    state = {
        "lastUpdated": datetime.now().isoformat(),
        "activeWork": ["Initialize Morningstar System"],
        "decisions": [],
        "outstandingIssues": [],
        "prophetVindications": [],
        "nextSession": []
    }
    write_state(state)
    return state
