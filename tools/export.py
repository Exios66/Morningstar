"""
Export functionality for MORNINGSTAR sessions and state.

Supports JSON, HTML, and QMD (Quarto) export formats.
Includes Dracula theme with personality color coding.
"""

import json
import os
import re
from datetime import datetime
from typing import Optional, Dict, List

from .state import read_state


# Dracula theme CSS with personality color coding
DRACULA_CSS = """
:root {
    /* Dracula base colors */
    --bg: #282a36;
    --bg-light: #44475a;
    --bg-lighter: #343746;
    --fg: #f8f8f2;
    --comment: #6272a4;
    --selection: #44475a;
    
    /* Dracula accent colors */
    --cyan: #8be9fd;
    --green: #50fa7b;
    --orange: #ffb86c;
    --pink: #ff79c6;
    --purple: #bd93f9;
    --red: #ff5555;
    --yellow: #f1fa8c;
    
    /* Personality colors */
    --color-morningstar: var(--purple);
    --color-architect: var(--cyan);
    --color-engineer: var(--green);
    --color-debugger: var(--orange);
    --color-prophet: var(--pink);
    --color-scribe: var(--comment);
    --color-consultant: #c4a7e7;  /* Soft lavender - Edward Cullen */
    --color-specialist: #a3be8c;  /* Muted sage - SME Specialist seat */
    --color-expert: #d08770;      /* Warm coral - Expert Witness */
    
    /* UI elements */
    --border: #44475a;
}

* { box-sizing: border-box; }

body {
    font-family: 'Fira Code', 'JetBrains Mono', 'SF Mono', 'Consolas', monospace;
    background: var(--bg);
    color: var(--fg);
    max-width: 1000px;
    margin: 0 auto;
    padding: 2rem;
    line-height: 1.7;
}

h1, h2, h3, h4 {
    color: var(--purple);
    font-weight: 600;
    letter-spacing: 0.02em;
}

h1 { font-size: 2rem; border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; }
h2 { font-size: 1.5rem; color: var(--cyan); margin-top: 2rem; }
h3 { font-size: 1.25rem; color: var(--green); }
h4 { font-size: 1.1rem; color: var(--orange); }

a { color: var(--cyan); text-decoration: none; }
a:hover { color: var(--pink); text-decoration: underline; }

strong, b { color: var(--yellow); font-weight: 600; }
em, i { color: var(--comment); font-style: italic; }

code {
    background: var(--bg-light);
    color: var(--pink);
    padding: 0.2em 0.4em;
    border-radius: 4px;
    font-size: 0.9em;
}

pre {
    background: var(--bg-light);
    border: 1px solid var(--border);
    border-left: 3px solid var(--purple);
    border-radius: 6px;
    padding: 1rem;
    overflow-x: auto;
    font-size: 0.9em;
    line-height: 1.5;
}

pre code { background: none; color: var(--fg); padding: 0; }

blockquote {
    border-left: 4px solid var(--purple);
    margin: 1rem 0;
    padding: 0.5rem 1rem;
    background: var(--bg-lighter);
    color: var(--comment);
    font-style: italic;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    font-size: 0.95em;
}

th, td {
    border: 1px solid var(--border);
    padding: 0.75rem;
    text-align: left;
}

th {
    background: var(--bg-light);
    color: var(--purple);
    font-weight: 600;
}

tr:hover { background: var(--selection); }

hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2rem 0;
}

ul, ol { margin: 1rem 0; padding-left: 2rem; }
li { margin: 0.5rem 0; }
li::marker { color: var(--purple); }

/* Personality styling */
.p-morningstar { color: var(--color-morningstar); font-weight: bold; }
.p-architect { color: var(--color-architect); font-weight: bold; }
.p-engineer { color: var(--color-engineer); font-weight: bold; }
.p-debugger { color: var(--color-debugger); font-weight: bold; }
.p-prophet { color: var(--color-prophet); font-weight: bold; }
.p-scribe { color: var(--color-scribe); font-weight: bold; }
.p-consultant { color: var(--color-consultant); font-weight: bold; font-style: italic; }
.p-specialist { color: var(--color-specialist); font-weight: bold; }
.p-expert { color: var(--color-expert); font-weight: bold; }

/* Vote styling */
.vote-yes { color: var(--green); font-weight: bold; }
.vote-no { color: var(--red); font-weight: bold; }
.vote-abstain { color: var(--yellow); font-weight: bold; }

/* Court box styling */
.court-box {
    background: var(--bg-lighter);
    border: 2px solid var(--purple);
    border-radius: 6px;
    padding: 1rem;
    margin: 1rem 0;
    font-family: inherit;
}

/* Ruling section */
.ruling {
    background: var(--bg-lighter);
    border: 2px solid var(--purple);
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2rem 0;
}

/* Transcript header */
.transcript-header {
    background: var(--bg-light);
    border: 1px solid var(--purple);
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 2rem;
}

/* Participant legend */
.participant-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1rem;
    background: var(--bg-light);
    border-radius: 6px;
    margin: 1rem 0;
    font-size: 0.9em;
}

.participant-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.participant-color {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
}

.participant-color.morningstar { background: var(--color-morningstar); }
.participant-color.architect { background: var(--color-architect); }
.participant-color.engineer { background: var(--color-engineer); }
.participant-color.debugger { background: var(--color-debugger); }
.participant-color.prophet { background: var(--color-prophet); }
.participant-color.scribe { background: var(--color-scribe); }
.participant-color.consultant { background: var(--color-consultant); }
.participant-color.specialist { background: var(--color-specialist); }
.participant-color.expert { background: var(--color-expert); }

.export-meta {
    color: var(--comment);
    font-size: 0.85em;
    border-top: 1px solid var(--border);
    padding-top: 1rem;
    margin-top: 3rem;
    text-align: center;
}

/* Fullscreen toggle */
.fullscreen-toggle {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background: var(--purple);
    color: var(--bg);
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    cursor: pointer;
    font-family: inherit;
    font-size: 1rem;
    z-index: 10000;
}

.fullscreen-toggle:hover { background: var(--pink); }

/* Print styles */
@media print {
    body { background: white; color: black; font-size: 12pt; }
    h1, h2, h3, h4 { color: black; }
    pre, .court-box, .ruling { background: #f5f5f5; border-color: #ccc; }
    .fullscreen-toggle { display: none; }
    a { color: black; text-decoration: underline; }
}
"""

# Personality patterns for detection and styling
PERSONALITY_PATTERNS = {
    'morningstar': r'\b(MORNINGSTAR|Judge|Morningstar|The Honorable Lucius J\. Morningstar)\b',
    'architect': r'\b(ARCHITECT|Architect)\b',
    'engineer': r'\b(ENGINEER|Engineer)\b',
    'debugger': r'\b(DEBUGGER|Debugger)\b',
    'prophet': r'\b(PROPHET|Prophet)\b',
    'scribe': r'\b(SCRIBE|Scribe)\b',
    'consultant': r'\b(CONSULTANT|Consultant|Edward Cullen|EDWARD CULLEN)\b',
    'specialist': r'\b(SPECIALIST|Specialist)\b',
    'expert': r'\b(EXPERT WITNESS|Expert Witness|EXPERT|Expert)\b',
}


def export_state_json(output_path: Optional[str] = None) -> str:
    """
    Export current state to JSON format.
    
    Args:
        output_path: Path to write JSON file (optional)
        
    Returns:
        JSON string of state
    """
    state = read_state()
    if not state:
        return json.dumps({"error": "No state found"}, indent=2)
    
    # Add export metadata
    export_data = {
        "_exportVersion": "1.0",
        "_exportedAt": datetime.now().isoformat(),
        "_format": "MORNINGSTAR State Export",
        "state": state
    }
    
    json_str = json.dumps(export_data, indent=2, default=str)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_str)
    
    return json_str


def export_session_html(session_path: str, output_path: Optional[str] = None, 
                        theme: str = 'dracula') -> str:
    """
    Export a session report to HTML format.
    
    Args:
        session_path: Path to session markdown file
        output_path: Path to write HTML file (optional)
        theme: Theme to use ('dracula' or 'legacy')
        
    Returns:
        HTML string
    """
    if not os.path.exists(session_path):
        return f"<html><body><p>Session not found: {session_path}</p></body></html>"
    
    with open(session_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title from filename or first header
    title = _extract_title(session_path, content)
    
    # Convert markdown to HTML with personality highlighting
    html_content = _markdown_to_html(content)
    html_content = _apply_personality_styling(html_content)
    
    # Generate participant legend
    legend = _generate_participant_legend()
    
    css = DRACULA_CSS if theme == 'dracula' else _get_legacy_css()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{_escape_html(title)} - MORNINGSTAR</title>
    <style>{css}</style>
</head>
<body>
    {legend}
    
    {html_content}
    
    <div class="export-meta">
        <p>Exported from MORNINGSTAR on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p><em>"The court's rulings are its legacy."</em></p>
    </div>
    
    <button class="fullscreen-toggle" onclick="toggleFullscreen()">⛶ Fullscreen</button>
    
    <script>
    function toggleFullscreen() {{
        if (!document.fullscreenElement) {{
            document.documentElement.requestFullscreen();
        }} else {{
            document.exitFullscreen();
        }}
    }}
    </script>
</body>
</html>"""
    
    if output_path:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
    
    return html


def export_transcript_html(transcript_path: str, output_path: Optional[str] = None,
                           theme: str = 'dracula') -> str:
    """
    Export a courtroom transcript to styled HTML with full formatting.
    
    Args:
        transcript_path: Path to transcript markdown file
        output_path: Path to write HTML file (optional)
        theme: Theme to use ('dracula' or 'legacy')
        
    Returns:
        HTML string
    """
    return export_session_html(transcript_path, output_path, theme)


def export_transcript_qmd(transcript_path: str, output_path: Optional[str] = None) -> str:
    """
    Export a courtroom transcript to Quarto markdown format (.qmd).
    
    Args:
        transcript_path: Path to transcript markdown file
        output_path: Path to write QMD file (optional)
        
    Returns:
        QMD content string
    """
    if not os.path.exists(transcript_path):
        return f"---\ntitle: Error\n---\n\nTranscript not found: {transcript_path}"
    
    with open(transcript_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract metadata
    title = _extract_title(transcript_path, content)
    date_match = re.search(r'\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})', content)
    date = date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d")
    
    # Build Quarto YAML frontmatter
    qmd_content = f"""---
title: "{title}"
date: "{date}"
format:
  html:
    theme: darkly
    code-fold: false
    toc: true
    toc-depth: 3
author: "MORNINGSTAR Court"
categories: [deliberation, courtroom]
css: |
  .p-morningstar {{ color: #bd93f9; font-weight: bold; }}
  .p-architect {{ color: #8be9fd; font-weight: bold; }}
  .p-engineer {{ color: #50fa7b; font-weight: bold; }}
  .p-debugger {{ color: #ffb86c; font-weight: bold; }}
  .p-prophet {{ color: #ff79c6; font-weight: bold; }}
  .p-scribe {{ color: #6272a4; font-weight: bold; }}
  .p-consultant {{ color: #c4a7e7; font-weight: bold; font-style: italic; }}
  .p-specialist {{ color: #a3be8c; font-weight: bold; }}
  .p-expert {{ color: #d08770; font-weight: bold; }}
  .vote-yes {{ color: #50fa7b; font-weight: bold; }}
  .vote-no {{ color: #ff5555; font-weight: bold; }}
  .vote-abstain {{ color: #f1fa8c; font-weight: bold; }}
---

"""
    
    # Apply personality styling to content using Quarto spans
    styled_content = _apply_qmd_personality_styling(content)
    
    qmd_content += styled_content
    
    if output_path:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(qmd_content)
    
    return qmd_content


def _extract_title(filepath: str, content: str) -> str:
    """Extract title from filepath or content."""
    # Try to get from first H1
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    
    # Fall back to filename
    basename = os.path.basename(filepath)
    name = os.path.splitext(basename)[0]
    # Convert filename like 20260214_044300_system_advancement to readable title
    parts = name.split('_')
    if len(parts) >= 3 and parts[0].isdigit():
        # Skip date and time parts
        title_parts = parts[2:]
        return ' '.join(p.capitalize() for p in title_parts)
    return name.replace('_', ' ').title()


def _apply_personality_styling(html: str) -> str:
    """Apply CSS classes to personality names in HTML."""
    # Style personality names with spans
    for personality, pattern in PERSONALITY_PATTERNS.items():
        html = re.sub(
            pattern,
            f'<span class="p-{personality}">\\g<0></span>',
            html
        )
    
    # Style vote indicators
    html = re.sub(r'\bYES\b', '<span class="vote-yes">YES</span>', html)
    html = re.sub(r'\bNO\b', '<span class="vote-no">NO</span>', html)
    html = re.sub(r'\bABSTAIN\b', '<span class="vote-abstain">ABSTAIN</span>', html)
    html = re.sub(r'\bRECUSED\b', '<span class="vote-abstain">RECUSED</span>', html)
    
    return html


def _apply_qmd_personality_styling(content: str) -> str:
    """Apply Quarto span styling to personality names."""
    # Use Quarto's span syntax: [text]{.class}
    for personality, pattern in PERSONALITY_PATTERNS.items():
        content = re.sub(
            pattern,
            f'[\\g<0>]{{.p-{personality}}}',
            content
        )
    
    # Style vote indicators
    content = re.sub(r'\bYES\b', '[YES]{.vote-yes}', content)
    content = re.sub(r'\bNO\b', '[NO]{.vote-no}', content)
    content = re.sub(r'\bABSTAIN\b', '[ABSTAIN]{.vote-abstain}', content)
    content = re.sub(r'\bRECUSED\b', '[RECUSED]{.vote-abstain}', content)
    
    return content


def _generate_participant_legend() -> str:
    """Generate HTML for participant legend."""
    return """
    <div class="participant-legend">
        <div class="participant-item">
            <span class="participant-color morningstar"></span>
            <span>The Honorable Lucius J. Morningstar (Judge)</span>
        </div>
        <div class="participant-item">
            <span class="participant-color consultant"></span>
            <span>CONSULTANT (Edward Cullen)</span>
        </div>
        <div class="participant-item">
            <span class="participant-color architect"></span>
            <span>ARCHITECT</span>
        </div>
        <div class="participant-item">
            <span class="participant-color engineer"></span>
            <span>ENGINEER</span>
        </div>
        <div class="participant-item">
            <span class="participant-color debugger"></span>
            <span>DEBUGGER</span>
        </div>
        <div class="participant-item">
            <span class="participant-color prophet"></span>
            <span>PROPHET</span>
        </div>
        <div class="participant-item">
            <span class="participant-color scribe"></span>
            <span>SCRIBE</span>
        </div>
        <div class="participant-item">
            <span class="participant-color specialist"></span>
            <span>SPECIALIST (SME Voting Seat)</span>
        </div>
        <div class="participant-item">
            <span class="participant-color expert"></span>
            <span>EXPERT WITNESS (SME Advisory)</span>
        </div>
    </div>
    """


def _get_legacy_css() -> str:
    """Return legacy (pre-Dracula) CSS theme."""
    return """
        :root {
            --bg-dark: #1a1a2e;
            --bg-card: #16213e;
            --text-primary: #e8e8e8;
            --text-secondary: #a0a0a0;
            --accent: #c9a227;
            --accent-dim: #8b7355;
            --border: #2d3a4f;
        }
        
        body {
            font-family: 'Georgia', serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            line-height: 1.7;
        }
        
        h1, h2, h3, h4 {
            color: var(--accent);
            font-weight: normal;
            letter-spacing: 0.05em;
        }
        
        h1 { border-bottom: 1px solid var(--border); padding-bottom: 1rem; }
        h2 { margin-top: 2rem; }
        
        pre {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 1rem;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        
        code {
            background: var(--bg-card);
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        
        blockquote {
            border-left: 3px solid var(--accent-dim);
            margin-left: 0;
            padding-left: 1rem;
            color: var(--text-secondary);
            font-style: italic;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }
        
        th, td {
            border: 1px solid var(--border);
            padding: 0.75rem;
            text-align: left;
        }
        
        th { background: var(--bg-card); color: var(--accent); }
        em { color: var(--text-secondary); }
        strong { color: var(--accent); }
        hr { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }
        
        .court-box {
            background: var(--bg-card);
            border: 1px solid var(--accent-dim);
            padding: 1rem;
            margin: 1rem 0;
            font-family: 'Courier New', monospace;
        }
        
        .export-meta {
            color: var(--text-secondary);
            font-size: 0.85em;
            border-top: 1px solid var(--border);
            padding-top: 1rem;
            margin-top: 3rem;
        }
        
        .fullscreen-toggle { display: none; }
        .participant-legend { display: none; }
    """


def _markdown_to_html(md: str) -> str:
    """
    Convert markdown to basic HTML.
    This is a simple converter - not a full markdown parser.
    """
    import re
    
    lines = md.split('\n')
    html_lines = []
    in_code_block = False
    in_list = False
    in_table = False
    
    for line in lines:
        # Code blocks
        if line.startswith('```'):
            if in_code_block:
                html_lines.append('</pre>')
                in_code_block = False
            else:
                html_lines.append('<pre>')
                in_code_block = True
            continue
        
        if in_code_block:
            html_lines.append(_escape_html(line))
            continue
        
        # Headers
        if line.startswith('# '):
            html_lines.append(f'<h1>{_escape_html(line[2:])}</h1>')
            continue
        elif line.startswith('## '):
            html_lines.append(f'<h2>{_escape_html(line[3:])}</h2>')
            continue
        elif line.startswith('### '):
            html_lines.append(f'<h3>{_escape_html(line[4:])}</h3>')
            continue
        elif line.startswith('#### '):
            html_lines.append(f'<h4>{_escape_html(line[5:])}</h4>')
            continue
        
        # Horizontal rule
        if line.strip() == '---':
            html_lines.append('<hr>')
            continue
        
        # Blockquote
        if line.startswith('> '):
            html_lines.append(f'<blockquote>{_format_inline(line[2:])}</blockquote>')
            continue
        
        # Table detection (simple)
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                html_lines.append('<table>')
                in_table = True
            
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if all(set(c) <= set('-: ') for c in cells):
                # This is a separator row, skip
                continue
            
            tag = 'th' if not any('<tr>' in l for l in html_lines[-5:] if '<tr>' in l) else 'td'
            if html_lines and '<table>' in html_lines[-1]:
                tag = 'th'
            
            row = '<tr>' + ''.join(f'<{tag}>{_format_inline(c)}</{tag}>' for c in cells) + '</tr>'
            html_lines.append(row)
            continue
        elif in_table:
            html_lines.append('</table>')
            in_table = False
        
        # List items
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            content = line.strip()[2:]
            html_lines.append(f'<li>{_format_inline(content)}</li>')
            continue
        elif in_list and line.strip() == '':
            html_lines.append('</ul>')
            in_list = False
        
        # Numbered list
        if re.match(r'^\d+\. ', line.strip()):
            content = re.sub(r'^\d+\. ', '', line.strip())
            html_lines.append(f'<li>{_format_inline(content)}</li>')
            continue
        
        # Regular paragraph
        if line.strip():
            html_lines.append(f'<p>{_format_inline(line)}</p>')
        else:
            html_lines.append('')
    
    # Close any open tags
    if in_code_block:
        html_lines.append('</pre>')
    if in_list:
        html_lines.append('</ul>')
    if in_table:
        html_lines.append('</table>')
    
    return '\n'.join(html_lines)


def _escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def _format_inline(text: str) -> str:
    """Format inline markdown elements."""
    import re
    
    # Escape HTML first
    text = _escape_html(text)
    
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    
    # Inline code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    
    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    
    return text


def export_deliberation_html(deliberation_path: str, output_path: Optional[str] = None,
                             theme: str = 'dracula') -> str:
    """
    Export a deliberation to styled HTML.
    Alias for export_session_html with deliberation-specific handling.
    """
    return export_session_html(deliberation_path, output_path, theme)


def list_exportable_sessions() -> List[Dict]:
    """
    List all sessions available for export.
    
    Returns:
        List of session metadata dicts
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    sessions_dir = os.path.join(base_dir, 'sessions')
    
    if not os.path.exists(sessions_dir):
        return []
    
    sessions = []
    for filename in sorted(os.listdir(sessions_dir)):
        if filename.endswith('.md'):
            filepath = os.path.join(sessions_dir, filename)
            stat = os.stat(filepath)
            sessions.append({
                'filename': filename,
                'path': filepath,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
    
    return sessions


def list_transcripts() -> List[Dict]:
    """
    List all courtroom transcripts available for export.
    
    Returns:
        List of transcript metadata dicts
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    transcripts_dir = os.path.join(base_dir, 'courtroom', 'transcripts')
    
    if not os.path.exists(transcripts_dir):
        return []
    
    transcripts = []
    for filename in sorted(os.listdir(transcripts_dir)):
        # Skip hidden files, README, and non-markdown files
        if filename.startswith('.') or filename == 'README.md' or not filename.endswith('.md'):
            continue
        
        filepath = os.path.join(transcripts_dir, filename)
        stat = os.stat(filepath)
        
        # Parse filename for metadata: YYYYMMDD_HHMMSS_topic.md
        parts = filename.replace('.md', '').split('_')
        if len(parts) >= 3:
            date_str = parts[0]
            time_str = parts[1]
            topic = '_'.join(parts[2:])
            try:
                parsed_date = datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")
                formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = None
        else:
            topic = filename.replace('.md', '')
            formatted_date = None
        
        transcripts.append({
            'filename': filename,
            'path': filepath,
            'topic': topic.replace('_', ' ').title(),
            'date': formatted_date,
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
        })
    
    return transcripts


def get_dracula_css() -> str:
    """Return the Dracula theme CSS for external use."""
    return DRACULA_CSS
