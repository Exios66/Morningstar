#!/usr/bin/env python3
"""
Portal Generator for MORNINGSTAR Courtroom

This script wraps gitmal to generate a static site with:
- Dracula theme for code highlighting
- Post-processing to inject custom CSS for courtroom formatting
- Generated index page linking to transcripts

Usage:
    python portal/generate.py [--theme dracula] [--output portal/output]
    
Or via CLI:
    morningstar portal generate --theme dracula
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Get the base directory (Morningstar root)
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
PORTAL_DIR = SCRIPT_DIR
OUTPUT_DIR = PORTAL_DIR / 'output'

# Dracula theme CSS injection for courtroom formatting
COURTROOM_CSS = """
/* MORNINGSTAR Courtroom Portal - Injected Styles */
<style>
/* Personality Colors */
.p-morningstar { color: #bd93f9 !important; font-weight: bold; }
.p-architect { color: #8be9fd !important; font-weight: bold; }
.p-engineer { color: #50fa7b !important; font-weight: bold; }
.p-debugger { color: #ffb86c !important; font-weight: bold; }
.p-prophet { color: #ff79c6 !important; font-weight: bold; }
.p-scribe { color: #6272a4 !important; font-weight: bold; }

/* Vote Styling */
.vote-yes { color: #50fa7b !important; font-weight: bold; }
.vote-no { color: #ff5555 !important; font-weight: bold; }
.vote-abstain { color: #f1fa8c !important; font-weight: bold; }

/* Court Box Enhancement */
pre:has(code) {
    border-left: 3px solid #bd93f9 !important;
}

/* Courtroom Banner */
.courtroom-banner {
    background: linear-gradient(135deg, #282a36 0%, #44475a 100%);
    border: 1px solid #bd93f9;
    border-radius: 8px;
    padding: 1rem 2rem;
    margin-bottom: 2rem;
    text-align: center;
}

.courtroom-banner h1 {
    color: #bd93f9;
    margin: 0;
    font-size: 1.5rem;
}

.courtroom-banner p {
    color: #6272a4;
    margin: 0.5rem 0 0 0;
    font-style: italic;
}

/* Transcript List Styling */
.transcript-list {
    list-style: none;
    padding: 0;
}

.transcript-list li {
    background: #44475a;
    border-radius: 6px;
    margin: 0.5rem 0;
    padding: 1rem;
    transition: transform 0.2s;
}

.transcript-list li:hover {
    transform: translateX(5px);
    background: #6272a4;
}

.transcript-list a {
    color: #f8f8f2;
    text-decoration: none;
    display: block;
}

.transcript-date {
    color: #6272a4;
    font-size: 0.85em;
}
</style>
"""

# Personality patterns for HTML injection
PERSONALITY_PATTERNS = {
    'morningstar': r'\b(MORNINGSTAR|Morningstar)\b(?![^<]*>)',
    'architect': r'\b(ARCHITECT|Architect)\b(?![^<]*>)',
    'engineer': r'\b(ENGINEER|Engineer)\b(?![^<]*>)',
    'debugger': r'\b(DEBUGGER|Debugger)\b(?![^<]*>)',
    'prophet': r'\b(PROPHET|Prophet)\b(?![^<]*>)',
    'scribe': r'\b(SCRIBE|Scribe)\b(?![^<]*>)',
}


def check_gitmal():
    """Check if gitmal is installed and return its path."""
    gitmal_path = shutil.which('gitmal')
    if not gitmal_path:
        print("Error: gitmal is not installed.")
        print("\nInstall with:")
        print("  go install github.com/antonmedv/gitmal@latest")
        sys.exit(1)
    return gitmal_path


def run_gitmal(theme='dracula', output=None, minify=False, gzip=False):
    """Run gitmal to generate the static site."""
    output_path = output or str(OUTPUT_DIR)
    
    cmd = [
        'gitmal', '.',
        '--theme', theme,
        '--output', output_path
    ]
    
    if minify:
        cmd.append('--minify')
    if gzip:
        cmd.append('--gzip')
    
    print(f"Running: {' '.join(cmd)}")
    
    result = subprocess.run(
        cmd,
        cwd=str(BASE_DIR),
        capture_output=False
    )
    
    return result.returncode == 0, output_path


def inject_courtroom_css(output_dir):
    """Inject courtroom CSS into all generated HTML files."""
    output_path = Path(output_dir)
    html_files = list(output_path.rglob('*.html'))
    
    print(f"\nInjecting courtroom CSS into {len(html_files)} HTML files...")
    
    injected = 0
    for html_file in html_files:
        try:
            content = html_file.read_text(encoding='utf-8')
            
            # Inject CSS before </head>
            if '</head>' in content and COURTROOM_CSS not in content:
                content = content.replace('</head>', f'{COURTROOM_CSS}\n</head>')
                html_file.write_text(content, encoding='utf-8')
                injected += 1
        except Exception as e:
            print(f"  Warning: Could not process {html_file}: {e}")
    
    print(f"  Injected CSS into {injected} files")
    return injected


def apply_personality_styling(output_dir):
    """Apply personality styling to transcript HTML files."""
    output_path = Path(output_dir)
    
    # Focus on courtroom transcripts
    transcript_files = list(output_path.glob('**/courtroom/transcripts/*.html'))
    
    if not transcript_files:
        # Try alternate paths
        transcript_files = list(output_path.rglob('*transcripts*.html'))
    
    print(f"\nApplying personality styling to {len(transcript_files)} transcript files...")
    
    styled = 0
    for html_file in transcript_files:
        try:
            content = html_file.read_text(encoding='utf-8')
            original = content
            
            # Apply personality patterns
            for personality, pattern in PERSONALITY_PATTERNS.items():
                content = re.sub(
                    pattern,
                    f'<span class="p-{personality}">\\1</span>',
                    content
                )
            
            # Apply vote styling
            content = re.sub(
                r'\bYES\b(?![^<]*>)',
                '<span class="vote-yes">YES</span>',
                content
            )
            content = re.sub(
                r'\bNO\b(?![^<]*>)',
                '<span class="vote-no">NO</span>',
                content
            )
            content = re.sub(
                r'\bABSTAIN\b(?![^<]*>)',
                '<span class="vote-abstain">ABSTAIN</span>',
                content
            )
            
            if content != original:
                html_file.write_text(content, encoding='utf-8')
                styled += 1
        except Exception as e:
            print(f"  Warning: Could not style {html_file}: {e}")
    
    print(f"  Styled {styled} files")
    return styled


def generate_transcript_index(output_dir):
    """Generate an index page for courtroom transcripts."""
    output_path = Path(output_dir)
    
    # Find transcript files
    transcripts_dir = BASE_DIR / 'courtroom' / 'transcripts'
    if not transcripts_dir.exists():
        print("No transcripts directory found.")
        return
    
    transcripts = []
    for md_file in sorted(transcripts_dir.glob('*.md')):
        if md_file.name == 'README.md':
            continue
        
        # Parse filename: YYYYMMDD_HHMMSS_topic.md
        name = md_file.stem
        parts = name.split('_')
        
        if len(parts) >= 3:
            date_str = parts[0]
            time_str = parts[1]
            topic = '_'.join(parts[2:])
            
            try:
                dt = datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")
                formatted_date = dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                formatted_date = "Unknown"
        else:
            topic = name
            formatted_date = "Unknown"
        
        transcripts.append({
            'filename': md_file.name,
            'topic': topic.replace('_', ' ').title(),
            'date': formatted_date,
            'html_name': name + '.html'
        })
    
    if not transcripts:
        print("No transcripts found to index.")
        return
    
    # Generate index HTML
    transcript_items = '\n'.join([
        f'''        <li>
            <a href="courtroom/transcripts/{t['html_name']}">
                <strong>{t['topic']}</strong>
                <span class="transcript-date">{t['date']}</span>
            </a>
        </li>'''
        for t in transcripts
    ])
    
    index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MORNINGSTAR Courtroom Transcripts</title>
    <style>
        :root {{
            --bg: #282a36;
            --bg-light: #44475a;
            --fg: #f8f8f2;
            --comment: #6272a4;
            --purple: #bd93f9;
            --cyan: #8be9fd;
            --green: #50fa7b;
            --pink: #ff79c6;
        }}
        
        * {{ box-sizing: border-box; }}
        
        body {{
            font-family: 'Fira Code', 'JetBrains Mono', monospace;
            background: var(--bg);
            color: var(--fg);
            margin: 0;
            padding: 2rem;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            padding: 2rem 0;
            border-bottom: 2px solid var(--purple);
            margin-bottom: 2rem;
        }}
        
        .header h1 {{
            color: var(--purple);
            font-size: 2.5rem;
            margin: 0;
            letter-spacing: 0.1em;
        }}
        
        .header p {{
            color: var(--comment);
            font-style: italic;
            margin: 0.5rem 0 0 0;
        }}
        
        .transcript-list {{
            list-style: none;
            padding: 0;
        }}
        
        .transcript-list li {{
            background: var(--bg-light);
            border-radius: 8px;
            margin: 1rem 0;
            transition: all 0.2s;
            border-left: 3px solid transparent;
        }}
        
        .transcript-list li:hover {{
            border-left-color: var(--purple);
            transform: translateX(5px);
        }}
        
        .transcript-list a {{
            display: block;
            padding: 1rem 1.5rem;
            color: var(--fg);
            text-decoration: none;
        }}
        
        .transcript-list strong {{
            display: block;
            color: var(--cyan);
            margin-bottom: 0.25rem;
        }}
        
        .transcript-date {{
            color: var(--comment);
            font-size: 0.85em;
        }}
        
        .nav {{
            margin-bottom: 2rem;
        }}
        
        .nav a {{
            color: var(--cyan);
            text-decoration: none;
        }}
        
        .nav a:hover {{
            color: var(--pink);
        }}
        
        .footer {{
            text-align: center;
            color: var(--comment);
            font-size: 0.85em;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid var(--bg-light);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>MORNINGSTAR</h1>
            <p>"The court has ruled. Regrettably sensible."</p>
        </header>
        
        <nav class="nav">
            <a href="index.html">&larr; Back to Repository</a>
        </nav>
        
        <h2 style="color: var(--purple);">Courtroom Transcripts</h2>
        
        <ul class="transcript-list">
{transcript_items}
        </ul>
        
        <footer class="footer">
            <p>Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p><em>The court's rulings are its legacy.</em></p>
        </footer>
    </div>
</body>
</html>'''
    
    # Write index file
    index_path = output_path / 'transcripts.html'
    index_path.write_text(index_html, encoding='utf-8')
    print(f"\nGenerated transcript index: {index_path}")
    
    return str(index_path)


def main():
    parser = argparse.ArgumentParser(
        description='Generate MORNINGSTAR Courtroom Portal with gitmal'
    )
    parser.add_argument(
        '--theme', '-t',
        default='dracula',
        help='Code highlighting theme (default: dracula)'
    )
    parser.add_argument(
        '--output', '-o',
        default=str(OUTPUT_DIR),
        help=f'Output directory (default: {OUTPUT_DIR})'
    )
    parser.add_argument(
        '--minify',
        action='store_true',
        help='Minify generated HTML files'
    )
    parser.add_argument(
        '--gzip',
        action='store_true',
        help='Compress generated HTML files'
    )
    parser.add_argument(
        '--skip-gitmal',
        action='store_true',
        help='Skip gitmal generation (only post-process existing output)'
    )
    
    args = parser.parse_args()
    
    print("=" * 65)
    print(" MORNINGSTAR COURTROOM PORTAL GENERATOR")
    print("=" * 65)
    print()
    
    if not args.skip_gitmal:
        # Check gitmal installation
        gitmal_path = check_gitmal()
        print(f"[✓] gitmal found: {gitmal_path}")
        
        # Run gitmal
        print(f"\n[→] Generating static site with theme '{args.theme}'...")
        success, output_path = run_gitmal(
            theme=args.theme,
            output=args.output,
            minify=args.minify,
            gzip=args.gzip
        )
        
        if not success:
            print("\n[!] gitmal generation failed")
            sys.exit(1)
        
        print(f"\n[✓] Static site generated: {output_path}")
    else:
        output_path = args.output
        print(f"[→] Skipping gitmal, post-processing: {output_path}")
    
    # Post-processing
    print("\n[→] Post-processing...")
    
    # Inject courtroom CSS
    inject_courtroom_css(output_path)
    
    # Apply personality styling
    apply_personality_styling(output_path)
    
    # Generate transcript index
    generate_transcript_index(output_path)
    
    print("\n" + "=" * 65)
    print(" GENERATION COMPLETE")
    print("=" * 65)
    print(f"\nOutput: {output_path}")
    print("\nTo view the portal:")
    print(f"  1. Open {output_path}/index.html in a browser")
    print("  2. Or run: python -m http.server 8080 -d", output_path)
    print("  3. Or run: morningstar portal serve")
    print()


if __name__ == '__main__':
    main()
