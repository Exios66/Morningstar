"""
Export functionality for MORNINGSTAR sessions and state.

Supports JSON and HTML export formats.
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, List

from .state import read_state


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


def export_session_html(session_path: str, output_path: Optional[str] = None) -> str:
    """
    Export a session report to HTML format.
    
    Args:
        session_path: Path to session markdown file
        output_path: Path to write HTML file (optional)
        
    Returns:
        HTML string
    """
    if not os.path.exists(session_path):
        return f"<html><body><p>Session not found: {session_path}</p></body></html>"
    
    with open(session_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Convert markdown to basic HTML
    html_content = _markdown_to_html(content)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MORNINGSTAR Session Export</title>
    <style>
        :root {{
            --bg-dark: #1a1a2e;
            --bg-card: #16213e;
            --text-primary: #e8e8e8;
            --text-secondary: #a0a0a0;
            --accent: #c9a227;
            --accent-dim: #8b7355;
            --border: #2d3a4f;
        }}
        
        body {{
            font-family: 'Georgia', serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            line-height: 1.7;
        }}
        
        h1, h2, h3, h4 {{
            color: var(--accent);
            font-weight: normal;
            letter-spacing: 0.05em;
        }}
        
        h1 {{
            border-bottom: 1px solid var(--border);
            padding-bottom: 1rem;
        }}
        
        h2 {{
            margin-top: 2rem;
        }}
        
        pre {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 1rem;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        
        code {{
            background: var(--bg-card);
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        
        blockquote {{
            border-left: 3px solid var(--accent-dim);
            margin-left: 0;
            padding-left: 1rem;
            color: var(--text-secondary);
            font-style: italic;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }}
        
        th, td {{
            border: 1px solid var(--border);
            padding: 0.75rem;
            text-align: left;
        }}
        
        th {{
            background: var(--bg-card);
            color: var(--accent);
        }}
        
        em {{
            color: var(--text-secondary);
        }}
        
        strong {{
            color: var(--accent);
        }}
        
        hr {{
            border: none;
            border-top: 1px solid var(--border);
            margin: 2rem 0;
        }}
        
        .court-box {{
            background: var(--bg-card);
            border: 1px solid var(--accent-dim);
            padding: 1rem;
            margin: 1rem 0;
            font-family: 'Courier New', monospace;
        }}
        
        .export-meta {{
            color: var(--text-secondary);
            font-size: 0.85em;
            border-top: 1px solid var(--border);
            padding-top: 1rem;
            margin-top: 3rem;
        }}
    </style>
</head>
<body>
    {html_content}
    
    <div class="export-meta">
        <p>Exported from MORNINGSTAR on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p><em>The court's rulings are its legacy.</em></p>
    </div>
</body>
</html>"""
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
    
    return html


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


def export_deliberation_html(deliberation_path: str, output_path: Optional[str] = None) -> str:
    """
    Export a deliberation to styled HTML.
    Alias for export_session_html with deliberation-specific handling.
    """
    return export_session_html(deliberation_path, output_path)


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
