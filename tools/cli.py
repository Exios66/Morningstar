import click
from tools import session, state, validate, changelog

@click.group()
def cli():
    pass

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
    
    click.echo("\n┌─────────────────────────────────────┐")
    click.echo("│ UNRELEASED ENTRIES                  │")
    click.echo("└─────────────────────────────────────┘\n")
    
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


if __name__ == '__main__':
    cli()
