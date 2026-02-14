import click
import os
import glob as globlib
from datetime import datetime
from tools import session, state, validate, changelog, backup, export as export_module

# Base directory for the project
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


@click.group()
def cli():
    """MORNINGSTAR - Sardonic deliberative coding partner."""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# Session Commands
# ─────────────────────────────────────────────────────────────────────────────

@cli.command()
def init():
    """Initialize a new Morningstar session."""
    session.init_state()
    click.echo("Morningstar session initialized.")


@cli.command()
def status():
    """Display current session status."""
    s = state.read_state()
    if not s:
        click.echo("No active session.")
        return
    
    click.echo(f"Last Updated: {s.get('lastUpdated')}")
    click.echo("\nActive Work:")
    for w in s.get('activeWork', []):
        click.echo(f"- {w}")
    
    click.echo("\nDecisions Made:")
    for d in s.get('decisions', []):
        click.echo(f"- {d.get('topic', 'Unknown')}: {d.get('decision', 'Unknown')}")
    
    click.echo("\nOutstanding Issues:")
    for i in s.get('outstandingIssues', []):
        click.echo(f"- {i.get('issue', 'Unknown')} ({i.get('severity', 'Medium')})")


@cli.command()
@click.option('--work', help='Add work item')
@click.option('--decision', help='Record decision (topic:decision:risk)')
@click.option('--issue', help='Report issue (issue:severity)')
def update(work, decision, issue):
    """Update session state."""
    d = None
    if decision:
        parts = decision.split(':')
        if len(parts) >= 3:
            d = {"topic": parts[0], "decision": parts[1], "rationale": "See logs", "risk": parts[2]}
            
    i = None
    if issue:
        parts = issue.split(':')
        if len(parts) >= 2:
            i = {"issue": parts[0], "severity": parts[1]}
            
    session.update_session(work_item=work, decision=d, issue=i)


@cli.command()
def end():
    """End the current session and generate a report."""
    session.end_session()


@cli.command()
@click.argument('topic')
@click.option('--decision', '-d', required=True, help='The ruling/decision made')
@click.option('--rationale', '-r', help='Explanation for the decision')
@click.option('--risk', default='Low', type=click.Choice(['Low', 'Medium', 'High', 'Critical']), 
              help='Risk level')
def decide(topic, decision, rationale, risk):
    """Quick command to record a decision.
    
    Example: morningstar decide "Database Choice" -d "PostgreSQL" -r "Battle-tested" --risk Low
    """
    decision_obj = {
        "topic": topic,
        "decision": decision,
        "rationale": rationale or "See logs",
        "risk": risk
    }
    session.update_session(decision=decision_obj)
    click.echo(f"\n*The Court has ruled on '{topic}': {decision}*")
    click.echo(f"Risk: {risk}")


@cli.command('validate')
def validate_schema():
    """Validate current state against JSON schema."""
    s = state.read_state()
    if not s:
        click.echo("No state to validate.")
        return
        
    valid, error = validate.validate_state(s)
    if valid:
        click.echo("State is valid.")
    else:
        click.echo(f"Validation failed: {error}")


# ─────────────────────────────────────────────────────────────────────────────
# Court Commands
# ─────────────────────────────────────────────────────────────────────────────

@cli.command()
def convene():
    """Display the courtroom header for a new deliberation."""
    click.echo("")
    click.echo("┌─────────────────────────────────────────────────────────────────┐")
    click.echo("│ THE COURT IS NOW IN SESSION                                     │")
    click.echo("│ MORNINGSTAR presiding                                           │")
    click.echo("└─────────────────────────────────────────────────────────────────┘")
    click.echo("")
    click.echo("*sighs*")
    click.echo("")
    click.echo("The personalities are assembled:")
    click.echo("  • ARCHITECT  — Cold, precise, conservative")
    click.echo("  • ENGINEER   — Practical, delivery-focused")
    click.echo("  • DEBUGGER   — Paranoid, detail-obsessed")
    click.echo("  • PROPHET    — Unstable, brilliant, dangerous")
    click.echo("  • SCRIBE     — Silent, recording")
    click.echo("")
    click.echo("State the matter before the court.")
    click.echo("")


@cli.command()
@click.argument('question')
def oracle(question):
    """Invoke ONLY the Prophet for radical thinking.
    
    ⚠️  WARNING: The Prophet is wrong approximately 90% of the time.
    This command explicitly opts into radical, unconventional ideas.
    
    Example: morningstar oracle "How might we approach caching?"
    """
    click.echo("")
    click.echo("┌─────────────────────────────────────────────────────────────────┐")
    click.echo("│ THE ORACLE SPEAKS                                               │")
    click.echo("│ ⚠️  WARNING: The Prophet's accuracy rate is ~10%                 │")
    click.echo("└─────────────────────────────────────────────────────────────────┘")
    click.echo("")
    click.echo(f"*The Prophet considers: \"{question}\"*")
    click.echo("")
    click.echo("───────────────────────────────────────────────────────────────────")
    click.echo("")
    click.echo("PROPHET:")
    click.echo("")
    click.echo("  Objection. We are thinking too small.")
    click.echo("")
    click.echo("  The obvious approach to this question assumes constraints that")
    click.echo("  may not be real. Consider:")
    click.echo("")
    click.echo("  • What assumption are we not questioning?")
    click.echo("  • What would make this problem trivial?")
    click.echo("  • What's the 10x solution, not the 10% improvement?")
    click.echo("  • What infrastructure gap does this reveal?")
    click.echo("")
    click.echo("  *draws fractals on a napkin*")
    click.echo("")
    click.echo("  If you find yourself dismissing this as impractical,")
    click.echo("  ask: is it impractical, or merely uncomfortable?")
    click.echo("")
    click.echo("───────────────────────────────────────────────────────────────────")
    click.echo("")
    click.echo("*The Prophet returns to contemplation.*")
    click.echo("")
    click.echo("⚠️  REMINDER: Log promising ideas to the F0 Registry with:")
    click.echo("   morningstar assess f0")
    click.echo("")


# ─────────────────────────────────────────────────────────────────────────────
# History Commands
# ─────────────────────────────────────────────────────────────────────────────

@cli.command()
@click.option('--limit', '-n', default=10, help='Number of sessions to show')
def history(limit):
    """List past session reports."""
    sessions_dir = os.path.join(BASE_DIR, 'sessions')
    
    if not os.path.exists(sessions_dir):
        click.echo("No session history found.")
        return
    
    reports = sorted(globlib.glob(os.path.join(sessions_dir, 'report_*.md')), reverse=True)
    
    if not reports:
        click.echo("No session reports found.")
        return
    
    click.echo("\n┌─────────────────────────────────────────────────────────────────┐")
    click.echo("│ SESSION HISTORY                                                 │")
    click.echo("└─────────────────────────────────────────────────────────────────┘\n")
    
    for i, report_path in enumerate(reports[:limit]):
        filename = os.path.basename(report_path)
        # Extract timestamp from filename: report_YYYYMMDD_HHMMSS.md
        timestamp_str = filename.replace('report_', '').replace('.md', '')
        try:
            dt = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            formatted = timestamp_str
        
        click.echo(f"  [{i+1}] {formatted}  →  {filename}")
    
    click.echo(f"\nUse 'morningstar recall <filename>' to view a specific session.")


@cli.command()
@click.argument('identifier')
def recall(identifier):
    """Load and display a past session report."""
    sessions_dir = os.path.join(BASE_DIR, 'sessions')
    
    # Allow numeric index or filename
    if identifier.isdigit():
        reports = sorted(globlib.glob(os.path.join(sessions_dir, 'report_*.md')), reverse=True)
        index = int(identifier) - 1
        if 0 <= index < len(reports):
            report_path = reports[index]
        else:
            click.echo(f"Invalid index: {identifier}")
            return
    else:
        # Treat as filename
        if not identifier.endswith('.md'):
            identifier += '.md'
        report_path = os.path.join(sessions_dir, identifier)
    
    if not os.path.exists(report_path):
        click.echo(f"Session not found: {identifier}")
        return
    
    click.echo("")
    click.echo("┌─────────────────────────────────────────────────────────────────┐")
    click.echo("│ SESSION RECALL                                                  │")
    click.echo("└─────────────────────────────────────────────────────────────────┘")
    click.echo("")
    
    with open(report_path, 'r', encoding='utf-8') as f:
        click.echo(f.read())


# ─────────────────────────────────────────────────────────────────────────────
# Doctor Command
# ─────────────────────────────────────────────────────────────────────────────

@cli.command()
def doctor():
    """Diagnose common issues with the Morningstar installation."""
    click.echo("")
    click.echo("┌─────────────────────────────────────────────────────────────────┐")
    click.echo("│ MORNINGSTAR DIAGNOSTIC                                          │")
    click.echo("└─────────────────────────────────────────────────────────────────┘")
    click.echo("")
    
    issues = []
    warnings = []
    
    # Check state file
    state_file = os.path.join(BASE_DIR, 'state', 'current.md')
    if os.path.exists(state_file):
        click.echo("  [✓] State file exists")
        # Try to parse it
        s = state.read_state()
        if s:
            click.echo("  [✓] State file parses successfully")
            # Check for parse warnings
            parse_warnings = s.get('_parseWarnings', [])
            if parse_warnings:
                for w in parse_warnings[:3]:  # Show first 3
                    warnings.append(f"State parse warning: {w}")
            # Validate structure
            is_valid, errors = state.validate_state(s)
            if is_valid:
                click.echo("  [✓] State structure is valid")
            else:
                for error in errors:
                    issues.append(f"State validation: {error}")
        else:
            issues.append("State file exists but failed to parse")
    else:
        warnings.append("No state file found (run 'morningstar init')")
    
    # Check core files
    core_files = ['MORNINGSTAR.md', 'personalities.md', 'procedures.md', 'mfaf.md']
    for filename in core_files:
        filepath = os.path.join(BASE_DIR, 'core', filename)
        if os.path.exists(filepath):
            click.echo(f"  [✓] core/{filename} exists")
        else:
            issues.append(f"Missing core file: core/{filename}")
    
    # Check courtroom files
    courtroom_files = ['RULES.md', 'BEST_PRACTICES.md']
    for filename in courtroom_files:
        filepath = os.path.join(BASE_DIR, 'courtroom', filename)
        if os.path.exists(filepath):
            click.echo(f"  [✓] courtroom/{filename} exists")
        else:
            issues.append(f"Missing courtroom file: courtroom/{filename}")
    
    # Check transcripts directory
    transcripts_dir = os.path.join(BASE_DIR, 'courtroom', 'transcripts')
    if os.path.exists(transcripts_dir):
        transcript_count = len(globlib.glob(os.path.join(transcripts_dir, '*.md')))
        click.echo(f"  [✓] Courtroom transcripts directory exists")
        click.echo(f"      ({transcript_count} transcripts found)")
    else:
        warnings.append("Courtroom transcripts directory does not exist")
    
    # Check schema files
    schema_files = ['state.schema.json', 'session.schema.json', 'deliberation.schema.json', 'assessment.schema.json']
    for filename in schema_files:
        filepath = os.path.join(BASE_DIR, 'schema', filename)
        if os.path.exists(filepath):
            click.echo(f"  [✓] schema/{filename} exists")
        else:
            warnings.append(f"Missing schema file: schema/{filename}")
    
    # Check sessions directory
    sessions_dir = os.path.join(BASE_DIR, 'sessions')
    if os.path.exists(sessions_dir):
        click.echo("  [✓] Sessions directory exists")
        report_count = len(globlib.glob(os.path.join(sessions_dir, 'report_*.md')))
        click.echo(f"      ({report_count} session reports found)")
    else:
        warnings.append("Sessions directory does not exist")
    
    # Check changelog
    changelog_file = os.path.join(BASE_DIR, 'CHANGELOG.md')
    if os.path.exists(changelog_file):
        click.echo("  [✓] Changelog exists")
    else:
        warnings.append("CHANGELOG.md not found")
    
    # Check F0 registry
    f0_file = os.path.join(BASE_DIR, 'state', 'f0-registry.md')
    if os.path.exists(f0_file):
        click.echo("  [✓] F0 Registry exists")
    else:
        warnings.append("F0 Registry not found (optional)")
    
    # Summary
    click.echo("")
    
    if issues:
        click.echo("ISSUES FOUND:")
        for issue in issues:
            click.echo(f"  [!] {issue}")
    
    if warnings:
        click.echo("\nWARNINGS:")
        for warning in warnings:
            click.echo(f"  [~] {warning}")
    
    if not issues and not warnings:
        click.echo("All systems operational.")
        click.echo("*The court is prepared to convene.*")
    elif not issues:
        click.echo("\nNo critical issues. The court may proceed.")
    else:
        click.echo("\nCritical issues detected. Address before proceeding.")


# ─────────────────────────────────────────────────────────────────────────────
# Changelog Commands - The Court's Chronicle
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# MFAF Assessment Commands
# ─────────────────────────────────────────────────────────────────────────────

@cli.group()
def assess():
    """MFAF feasibility assessment tools."""
    pass


@assess.command('new')
@click.argument('proposal')
@click.option('--base', '-b', type=click.Choice(['F0', 'F1', 'F2', 'F3', 'F4', 'F5']), 
              help='Base rating (skips interactive)')
@click.option('--effort', '-e', type=click.Choice(['S', 'M', 'L', 'XL']),
              help='Effort band (skips interactive)')
@click.option('--save/--no-save', default=True, help='Save assessment to file')
def assess_new(proposal, base, effort, save):
    """Create a new feasibility assessment."""
    from tools import assess as assess_module
    
    if base and effort:
        # Non-interactive mode
        risk_vectors = {k: False for k in assess_module.RISK_VECTORS.keys()}
        assessment = assess_module.create_assessment(
            proposal=proposal,
            base_rating=base,
            risk_vectors=risk_vectors,
            effort_band=effort,
            assessor="CLI (quick)"
        )
        click.echo(assess_module.format_assessment(assessment))
    else:
        # Interactive mode
        assessment = assess_module.run_interactive_assessment(proposal)
    
    if save:
        filepath = assess_module.save_assessment(assessment)
        click.echo(f"\n*Assessment saved to {filepath}*")


@assess.command('list')
@click.option('--limit', '-n', default=10, help='Number of assessments to show')
def assess_list(limit):
    """List recent assessments."""
    from tools import assess as assess_module
    
    assessments = assess_module.load_assessments()
    
    if not assessments:
        click.echo("No assessments found.")
        return
    
    click.echo("\n┌─────────────────────────────────────────────────────────────────┐")
    click.echo("│ RECENT ASSESSMENTS                                              │")
    click.echo("└─────────────────────────────────────────────────────────────────┘\n")
    
    for i, a in enumerate(assessments[-limit:]):
        proposal = a.get('proposal', 'Unknown')[:40]
        rating = a.get('effectiveRating', '?')
        rec = a.get('recommendation', '?')
        click.echo(f"  [{i+1}] {rating} | {rec:<12} | {proposal}")


@assess.command('f0')
def assess_f0():
    """View the F0 Registry (impossible ideas with potential)."""
    f0_file = os.path.join(BASE_DIR, 'state', 'f0-registry.md')
    
    if not os.path.exists(f0_file):
        click.echo("F0 Registry not found.")
        return
    
    with open(f0_file, 'r', encoding='utf-8') as f:
        click.echo(f.read())


# ─────────────────────────────────────────────────────────────────────────────
# Changelog Commands - The Court's Chronicle
# ─────────────────────────────────────────────────────────────────────────────

@cli.group()
def log():
    """Manage the changelog - the court's chronicle of proceedings."""
    pass


@log.command('show')
def log_show():
    """Display unreleased changelog entries."""
    summary = changelog.get_unreleased_summary()
    if not summary:
        click.echo("*The chronicle awaits new entries.*")
        return
    
    click.echo("\n┌─────────────────────────────────────────────────────────────────┐")
    click.echo("│ UNRELEASED ENTRIES                                              │")
    click.echo("└─────────────────────────────────────────────────────────────────┘\n")
    
    for category, entries in summary.items():
        click.echo(f"### {category}")
        for entry in entries:
            click.echo(f"  - {entry}")
        click.echo("")


@log.command('add')
@click.option('--category', '-c', type=click.Choice(['added', 'changed', 'fixed', 'removed', 'deprecated', 'security']), 
              default='added', help='Type of change')
@click.option('--message', '-m', required=True, help='Description of the change')
@click.option('--source', '-s', help='Attribution (e.g., personality name)')
def log_add(category, message, source):
    """Add an entry to the changelog."""
    changelog.add_entry(category, message, source=source)
    click.echo(f"*Inscribed to the chronicle: [{category}] {message}*")


@log.command('decide')
@click.option('--topic', '-t', required=True, help='Topic of the decision')
@click.option('--decision', '-d', required=True, help='The ruling')
@click.option('--risk', '-r', default='Low', help='Risk level')
@click.option('--rationale', help='Explanation for the decision')
def log_decide(topic, decision, risk, rationale):
    """Record a court decision in the changelog."""
    changelog.add_decision(topic, decision, risk, rationale)
    click.echo(f"*The Court has ruled on '{topic}'. So it is written.*")


@log.command('vindicate')
@click.option('--prediction', '-p', required=True, help='What the Prophet warned about')
@click.option('--outcome', '-o', required=True, help='What actually happened')
def log_vindicate(prediction, outcome):
    """Record a Prophet vindication."""
    changelog.add_prophet_vindication(prediction, outcome)
    click.echo(f"*The Prophet's warning has been vindicated. Let the record show.*")


@log.command('release')
@click.option('--version', '-v', required=True, help='Version number (e.g., 1.0.0)')
@click.option('--date', '-d', help='Release date (YYYY-MM-DD, defaults to today)')
def log_release(version, date):
    """Convert unreleased entries to a versioned release."""
    changelog.release_version(version, date)
    click.echo(f"*Version {version} has been sealed in the chronicle.*")


# ─────────────────────────────────────────────────────────────────────────────
# Backup Commands - The Debugger's Insurance
# ─────────────────────────────────────────────────────────────────────────────

@cli.group()
def bkp():
    """Backup and restore functionality."""
    pass


@bkp.command('create')
@click.option('--description', '-d', help='Description for this backup')
def bkp_create(description):
    """Create a backup of current state."""
    path = backup.create_backup(description)
    click.echo(f"\n✓ Backup created: {os.path.basename(path)}")
    click.echo(f"  Path: {path}")


@bkp.command('list')
def bkp_list():
    """List available backups."""
    backups = backup.list_backups()
    
    if not backups:
        click.echo("No backups found.")
        return
    
    click.echo("\n┌─────────────────────────────────────────────────────────────────┐")
    click.echo("│ AVAILABLE BACKUPS                                               │")
    click.echo("└─────────────────────────────────────────────────────────────────┘\n")
    
    for i, b in enumerate(backups, 1):
        click.echo(f"  [{i}] {b['name']}")
        click.echo(f"      Created: {b['timestamp']}")
        click.echo(f"      Description: {b['description']}")
        click.echo(f"      Files: {b['file_count']}")
        click.echo("")


@bkp.command('restore')
@click.argument('identifier')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation prompt')
def bkp_restore(identifier, force):
    """Restore state from a backup.
    
    IDENTIFIER can be a backup name or index number (1-based).
    """
    success = backup.restore_backup(identifier, confirm=force)
    if not success:
        raise SystemExit(1)


@bkp.command('delete')
@click.argument('identifier')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation prompt')
def bkp_delete(identifier, force):
    """Delete a backup."""
    success = backup.delete_backup(identifier, confirm=force)
    if not success:
        raise SystemExit(1)


@bkp.command('prune')
@click.option('--keep', '-k', default=10, help='Number of backups to keep')
def bkp_prune(keep):
    """Remove old backups, keeping the most recent N."""
    deleted = backup.prune_backups(keep)
    click.echo(f"Pruned {deleted} old backup(s). Keeping {keep} most recent.")


# ─────────────────────────────────────────────────────────────────────────────
# Export Commands
# ─────────────────────────────────────────────────────────────────────────────

@cli.group()
def export():
    """Export state and sessions to various formats."""
    pass


@export.command('state')
@click.option('--output', '-o', help='Output file path')
@click.option('--format', '-f', 'fmt', type=click.Choice(['json']), default='json',
              help='Export format')
def export_state(output, fmt):
    """Export current state to JSON."""
    if fmt == 'json':
        json_str = export_module.export_state_json(output)
        if output:
            click.echo(f"State exported to: {output}")
        else:
            click.echo(json_str)


@export.command('session')
@click.argument('session_file')
@click.option('--output', '-o', help='Output file path')
@click.option('--format', '-f', 'fmt', type=click.Choice(['html']), default='html',
              help='Export format')
def export_session(session_file, output, fmt):
    """Export a session or deliberation to HTML.
    
    SESSION_FILE can be a filename in sessions/ or a full path.
    """
    # Resolve session file path
    if not os.path.isabs(session_file):
        session_path = os.path.join(BASE_DIR, 'sessions', session_file)
        if not os.path.exists(session_path):
            session_path = os.path.join(BASE_DIR, session_file)
    else:
        session_path = session_file
    
    if not os.path.exists(session_path):
        click.echo(f"Session file not found: {session_file}")
        raise SystemExit(1)
    
    if fmt == 'html':
        if not output:
            output = session_path.replace('.md', '.html')
        
        export_module.export_session_html(session_path, output)
        click.echo(f"Session exported to: {output}")


@export.command('list')
def export_list():
    """List sessions available for export."""
    sessions = export_module.list_exportable_sessions()
    
    if not sessions:
        click.echo("No sessions found.")
        return
    
    click.echo("\n┌─────────────────────────────────────────────────────────────────┐")
    click.echo("│ EXPORTABLE SESSIONS                                             │")
    click.echo("└─────────────────────────────────────────────────────────────────┘\n")
    
    for s in sessions:
        click.echo(f"  • {s['filename']}")
        click.echo(f"    Modified: {s['modified']}")
        click.echo("")


if __name__ == '__main__':
    cli()
