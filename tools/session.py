from datetime import datetime
from .state import read_state, write_state, init_state
from .changelog import format_session_changelog_entry, add_decision, add_entry

def start_session():
    state = read_state()
    if not state:
        print("No existing session state found. Initializing new session.")
        state = init_state()
    
    print("\n┌─────────────────────────────────────┐")
    print("│ MORNINGSTAR SESSION INITIALIZED     │")
    print("└─────────────────────────────────────┘")
    print(f"Last Updated: {state.get('lastUpdated', 'Unknown')}")
    
    print("\n## Active Work")
    for item in state.get('activeWork', []):
        print(f"- {item}")
        
    print("\n## Outstanding Issues")
    for issue in state.get('outstandingIssues', []):
        print(f"- {issue.get('issue')} ({issue.get('severity')})")
        
    return state

def update_session(work_item=None, decision=None, issue=None):
    state = read_state()
    if not state:
        state = init_state()
    
    state['lastUpdated'] = datetime.now().isoformat()
    
    if work_item:
        state['activeWork'].append(work_item)
        # Log work to changelog immediately
        add_entry('added', work_item, source="Session in progress")
        
    if decision:
        # Expected format: {"topic": "...", "decision": "...", "rationale": "...", "risk": "..."}
        state['decisions'].append(decision)
        # Log decision to changelog immediately
        add_decision(
            topic=decision.get('topic', 'Unknown'),
            decision=decision.get('decision', 'Unknown'),
            risk=decision.get('risk', 'Unknown'),
            rationale=decision.get('rationale')
        )
        
    if issue:
        # Expected format: {"issue": "...", "severity": "..."}
        state['outstandingIssues'].append(issue)
        
    write_state(state)
    print(f"Session state updated at {state['lastUpdated']}")
    return state

def end_session(next_steps=None):
    state = read_state()
    if not state:
        return
        
    state['lastUpdated'] = datetime.now().isoformat()
    
    if next_steps:
        state['nextSession'] = next_steps
        
    # Archive logic could go here (move current.md to sessions/timestamp.md)
    # For now, just save state
    write_state(state)
    print("Session finalized.")
    
    # Update changelog with session summary
    # Note: Individual decisions/work are logged as they happen,
    # but vindications and final summary are captured here
    changelog_entries = format_session_changelog_entry(state)
    if changelog_entries:
        print(f"\n*The Scribe has inscribed {len(changelog_entries)} entries to the chronicle.*")
    
    # Generate report
    report = f"""
# Session Report {state['lastUpdated']}

## Work Completed
{chr(10).join(['- ' + w for w in state.get('activeWork', [])])}

## Decisions
{chr(10).join(['- ' + d.get('topic', '') + ': ' + d.get('decision', '') for d in state.get('decisions', [])])}

## Issues
{chr(10).join(['- ' + i.get('issue', '') + ': ' + i.get('severity', '') for i in state.get('outstandingIssues', [])])}

## Changelog Entries Added
{chr(10).join(['- ' + e for e in changelog_entries])}
"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"sessions/report_{timestamp}.md"
    with open(report_path, "w") as f:
        f.write(report)
        
    print(f"Report saved to {report_path}")
