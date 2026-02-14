"""
Automatic changelog management for MORNINGSTAR sessions.

The court maintains a living record of its proceedings.
Each session's verdicts, changes, and warnings are inscribed for posterity.
"""

import os
import re
from datetime import datetime
from typing import Optional

CHANGELOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'CHANGELOG.md')

# Change categories following Keep a Changelog conventions
CATEGORIES = {
    'added': 'Added',
    'changed': 'Changed',
    'deprecated': 'Deprecated',
    'removed': 'Removed',
    'fixed': 'Fixed',
    'security': 'Security',
    'decided': 'Decided',  # MORNINGSTAR-specific: court rulings
    'warned': 'Warned',    # MORNINGSTAR-specific: prophet vindications
}


def read_changelog() -> str:
    """Read the current changelog contents."""
    if not os.path.exists(CHANGELOG_FILE):
        return _create_initial_changelog()
    
    with open(CHANGELOG_FILE, 'r') as f:
        return f.read()


def write_changelog(content: str) -> None:
    """Write the changelog to disk."""
    with open(CHANGELOG_FILE, 'w') as f:
        f.write(content)


def _create_initial_changelog() -> str:
    """Create an initial changelog structure."""
    content = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

*The court maintains this record. Each entry is a verdict inscribed for posterity.*

## [Unreleased]

"""
    write_changelog(content)
    return content


def _find_unreleased_section(content: str) -> tuple[int, int]:
    """
    Find the start and end positions of the [Unreleased] section.
    Returns (start_of_content, end_of_section).
    """
    unreleased_match = re.search(r'^## \[Unreleased\]\s*\n', content, re.MULTILINE)
    if not unreleased_match:
        return -1, -1
    
    start = unreleased_match.end()
    
    # Find next version section or end of file
    next_version = re.search(r'^## \[\d', content[start:], re.MULTILINE)
    if next_version:
        end = start + next_version.start()
    else:
        end = len(content)
    
    return start, end


def _get_or_create_category_in_section(section_content: str, category: str) -> tuple[str, int]:
    """
    Find a category heading in section content, or determine where to add it.
    Returns (updated_section, insertion_point_for_item).
    """
    category_heading = f"### {CATEGORIES.get(category, category.title())}"
    pattern = rf'^{re.escape(category_heading)}\s*\n'
    match = re.search(pattern, section_content, re.MULTILINE)
    
    if match:
        # Category exists, find where to insert new item
        insert_point = match.end()
        return section_content, insert_point
    else:
        # Category doesn't exist, add it at the beginning of section
        new_section = f"{category_heading}\n\n{section_content}"
        # Insert point is right after the heading and newline
        return new_section, len(category_heading) + 1


def add_entry(
    category: str,
    description: str,
    source: Optional[str] = None,
    to_unreleased: bool = True
) -> None:
    """
    Add a new entry to the changelog.
    
    Args:
        category: One of 'added', 'changed', 'deprecated', 'removed', 'fixed', 
                  'security', 'decided', 'warned'
        description: The change description
        source: Optional attribution (e.g., personality name, session ID)
        to_unreleased: If True, add to [Unreleased]; otherwise add to latest version
    """
    content = read_changelog()
    
    if source:
        entry = f"- {description} *({source})*\n"
    else:
        entry = f"- {description}\n"
    
    start, end = _find_unreleased_section(content)
    
    if start == -1:
        # No unreleased section, create one
        # Find first version heading
        first_version = re.search(r'^## \[\d', content, re.MULTILINE)
        if first_version:
            insert_at = first_version.start()
            unreleased_section = f"## [Unreleased]\n\n### {CATEGORIES.get(category, category.title())}\n{entry}\n"
            content = content[:insert_at] + unreleased_section + content[insert_at:]
        else:
            # No versions at all, append
            content += f"\n## [Unreleased]\n\n### {CATEGORIES.get(category, category.title())}\n{entry}\n"
    else:
        section_content = content[start:end]
        category_heading = f"### {CATEGORIES.get(category, category.title())}"
        
        # Check if category exists in section
        pattern = rf'^{re.escape(category_heading)}\s*\n'
        match = re.search(pattern, section_content, re.MULTILINE)
        
        if match:
            # Insert after heading
            insert_point = start + match.end()
            content = content[:insert_point] + entry + content[insert_point:]
        else:
            # Add new category section at start of unreleased content
            new_category = f"{category_heading}\n{entry}\n"
            content = content[:start] + new_category + content[start:]
    
    write_changelog(content)


def add_decision(topic: str, decision: str, risk: str, rationale: Optional[str] = None) -> None:
    """
    Record a court decision in the changelog.
    
    Args:
        topic: What was being decided
        decision: The ruling
        risk: Risk level or notes
        rationale: Optional explanation
    """
    if rationale and rationale != "See logs":
        description = f"**{topic}**: {decision} — *Risk: {risk}. {rationale}*"
    else:
        description = f"**{topic}**: {decision} — *Risk: {risk}*"
    
    add_entry('decided', description, source="The Court")


def add_prophet_vindication(prediction: str, outcome: str) -> None:
    """
    Record when the Prophet was proven right.
    
    Args:
        prediction: What the Prophet warned about
        outcome: What actually happened
    """
    description = f"The Prophet warned of *\"{prediction}\"* — and so it came to pass: {outcome}"
    add_entry('warned', description, source="The Prophet, Vindicated")


def add_work_completed(work_items: list[str], session_id: Optional[str] = None) -> None:
    """
    Record completed work items from a session.
    
    Args:
        work_items: List of work items completed
        session_id: Optional session identifier
    """
    source = f"Session {session_id}" if session_id else "Session"
    for item in work_items:
        add_entry('added', item, source=source)


def add_fix(description: str, source: Optional[str] = None) -> None:
    """Record a bug fix."""
    add_entry('fixed', description, source=source)


def add_change(description: str, source: Optional[str] = None) -> None:
    """Record a change to existing functionality."""
    add_entry('changed', description, source=source)


def release_version(version: str, date: Optional[str] = None) -> None:
    """
    Convert the [Unreleased] section to a versioned release.
    
    Args:
        version: Version number (e.g., "1.0.0")
        date: Release date (defaults to today)
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    content = read_changelog()
    
    # Find unreleased section
    unreleased_pattern = r'^## \[Unreleased\]\s*\n'
    match = re.search(unreleased_pattern, content, re.MULTILINE)
    
    if not match:
        print("No [Unreleased] section found.")
        return
    
    # Replace [Unreleased] with version, add new empty unreleased
    new_version_heading = f"## [{version}] - {date}\n"
    new_unreleased = "## [Unreleased]\n\n"
    
    content = content[:match.start()] + new_unreleased + new_version_heading + content[match.end():]
    
    write_changelog(content)
    print(f"Released version {version}")


def get_unreleased_summary() -> dict:
    """
    Get a summary of unreleased changes.
    
    Returns:
        Dict with category names as keys and lists of entries as values
    """
    content = read_changelog()
    start, end = _find_unreleased_section(content)
    
    if start == -1:
        return {}
    
    section = content[start:end]
    summary = {}
    
    current_category = None
    for line in section.split('\n'):
        if line.startswith('### '):
            current_category = line[4:].strip()
            summary[current_category] = []
        elif line.startswith('- ') and current_category:
            summary[current_category].append(line[2:].strip())
    
    return summary


def format_session_changelog_entry(state: dict) -> str:
    """
    Format a session's state as changelog entries.
    Called by session.end_session() to inscribe the session's record.
    
    Args:
        state: The session state dictionary
        
    Returns:
        Summary of what was added to changelog
    """
    entries_added = []
    
    # Record decisions
    for decision in state.get('decisions', []):
        add_decision(
            topic=decision.get('topic', 'Unknown'),
            decision=decision.get('decision', 'Unknown'),
            risk=decision.get('risk', 'Unknown'),
            rationale=decision.get('rationale')
        )
        entries_added.append(f"Decision: {decision.get('topic')}")
    
    # Record prophet vindications
    for vindication in state.get('prophetVindications', []):
        # Vindications are stored as simple strings; parse if possible
        if ' — ' in vindication:
            prediction, outcome = vindication.split(' — ', 1)
            add_prophet_vindication(prediction, outcome)
        else:
            add_entry('warned', vindication, source="The Prophet")
        entries_added.append(f"Vindication: {vindication[:30]}...")
    
    # Record completed work (from activeWork that's being closed out)
    work_items = state.get('activeWork', [])
    if work_items:
        timestamp = state.get('lastUpdated', datetime.now().isoformat())
        session_marker = timestamp[:10]  # Just the date
        for item in work_items:
            # Only log substantive work, not meta-tasks
            if item and not item.lower().startswith('initialize'):
                add_entry('added', item, source=f"Session {session_marker}")
                entries_added.append(f"Work: {item[:30]}...")
    
    return entries_added
