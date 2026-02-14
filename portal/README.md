# MORNINGSTAR Courtroom Portal

> *"The court's rulings are its legacy."*

The Courtroom Portal provides a front-end interface for viewing, analyzing, and exporting deliberation transcripts from the MORNINGSTAR courtroom system.

---

## Features

- **Standalone Viewer** - Local HTML page for browsing transcripts without a server
- **Gitmal Integration** - Full static site generation with Dracula theme
- **Export Formats** - HTML and Quarto (.qmd) export with personality color coding
- **Fullscreen Mode** - Immersive view for analyzing deliberations
- **Print Support** - Clean print-friendly styles for physical documentation

---

## Quick Start

### View Transcripts Locally

Open the standalone viewer in your browser:

```bash
# Via CLI
morningstar portal open

# Or directly
open portal/viewer.html
```

### Generate Full Portal

Generate a complete static site using gitmal:

```bash
# Generate with Dracula theme
morningstar portal generate --theme dracula

# Generate with compression
morningstar portal generate --minify --gzip
```

### Serve Locally

Start a local HTTP server to view the portal:

```bash
# Start server on port 8080
morningstar portal serve

# Custom port
morningstar portal serve --port 3000
```

---

## CLI Commands

### Export Commands

| Command | Description |
|---------|-------------|
| `morningstar export transcripts` | List all available transcripts |
| `morningstar export transcript <file>` | Export transcript to HTML |
| `morningstar export transcript <file> -f qmd` | Export transcript to Quarto |

### Portal Commands

| Command | Description |
|---------|-------------|
| `morningstar portal generate` | Generate static site with gitmal |
| `morningstar portal serve` | Start local HTTP server |
| `morningstar portal open` | Open viewer in browser |
| `morningstar portal export-all` | Batch export all transcripts |

---

## Export Examples

### Single Transcript to HTML

```bash
morningstar export transcript 20260214_044300_system_advancement.md
```

Output: `courtroom/transcripts/20260214_044300_system_advancement.html`

### Single Transcript to Quarto

```bash
morningstar export transcript 20260214_044300_system_advancement.md -f qmd -o deliberation.qmd
```

The QMD file includes YAML frontmatter for Quarto rendering:

```yaml
---
title: "System Advancement"
date: "2026-02-14"
format:
  html:
    theme: darkly
    toc: true
author: "MORNINGSTAR Court"
categories: [deliberation, courtroom]
---
```

### Batch Export All Transcripts

```bash
# Export all as HTML
morningstar portal export-all

# Export all as both HTML and QMD
morningstar portal export-all -f both -o exports/
```

---

## Personality Color Scheme (Dracula Theme)

The portal uses the Dracula color palette with personality-specific colors:

| Personality | Color | Hex |
|-------------|-------|-----|
| MORNINGSTAR (Judge) | Purple | `#bd93f9` |
| ARCHITECT | Cyan | `#8be9fd` |
| ENGINEER | Green | `#50fa7b` |
| DEBUGGER | Orange | `#ffb86c` |
| PROPHET | Pink | `#ff79c6` |
| SCRIBE | Gray | `#6272a4` |

### Vote Styling

| Vote | Color | Hex |
|------|-------|-----|
| YES | Green | `#50fa7b` |
| NO | Red | `#ff5555` |
| ABSTAIN | Yellow | `#f1fa8c` |

---

## Directory Structure

```
portal/
├── README.md           # This file
├── viewer.html         # Standalone transcript viewer
├── dracula.css         # Dracula theme stylesheet
├── generate.py         # Gitmal wrapper script
└── output/             # Generated static site (after running generate)
    ├── index.html
    ├── transcripts.html
    └── courtroom/
        └── transcripts/
            └── *.html
```

---

## Standalone Generator Script

The `generate.py` script can be run directly:

```bash
# Generate with defaults
python portal/generate.py

# With options
python portal/generate.py --theme dracula --minify --gzip

# Skip gitmal, only post-process
python portal/generate.py --skip-gitmal
```

### Generator Options

| Option | Default | Description |
|--------|---------|-------------|
| `--theme`, `-t` | `dracula` | Code highlighting theme |
| `--output`, `-o` | `portal/output` | Output directory |
| `--minify` | `false` | Minify generated HTML |
| `--gzip` | `false` | Compress generated HTML |
| `--skip-gitmal` | `false` | Only run post-processing |

---

## Gitmal Requirements

The portal generator requires gitmal to be installed:

```bash
# Install gitmal
go install github.com/antonmedv/gitmal@latest

# Verify installation
gitmal --help
```

Gitmal generates static HTML pages with:
- File trees and commit history
- Syntax highlighting with customizable themes
- Markdown rendering

---

## Customization

### Custom CSS

Edit `portal/dracula.css` to customize the appearance. Key sections:

- **Base Colors** - `:root` CSS variables
- **Personality Styling** - `.p-*` classes
- **Vote Styling** - `.vote-*` classes
- **Print Styles** - `@media print` section

### Theme Options

Available themes for gitmal (via `--theme`):

- `dracula` (recommended)
- `github`
- `github-dark`
- `monokai`
- `nord`
- `solarized-dark`

---

## Viewing in Full Screen

### Via Viewer

1. Open `portal/viewer.html`
2. Select a transcript
3. Click "⛶ Fullscreen" button

### Via Keyboard

- Press `F11` for native fullscreen
- Press `Escape` to exit

### Via Exported HTML

Exported HTML files include a fullscreen toggle button in the bottom-right corner.

---

## Print / PDF Export

### From Viewer

1. Open a transcript in the viewer
2. Select "Export" → "Print / PDF"
3. Use browser print dialog

### From Command Line (macOS)

```bash
# Export to HTML first
morningstar export transcript 20260214_044300_system_advancement.md

# Convert to PDF (requires wkhtmltopdf or similar)
wkhtmltopdf courtroom/transcripts/20260214_044300_system_advancement.html output.pdf
```

### From Quarto

```bash
# Export to QMD
morningstar export transcript 20260214_044300_system_advancement.md -f qmd

# Render with Quarto
quarto render deliberation.qmd --to pdf
```

---

## Troubleshooting

### "gitmal not found"

Install gitmal:

```bash
go install github.com/antonmedv/gitmal@latest
```

Ensure `$GOPATH/bin` is in your PATH.

### "No transcripts found"

Check that transcripts exist in `courtroom/transcripts/`:

```bash
ls courtroom/transcripts/*.md
```

### Viewer not loading transcripts

The standalone viewer works best when served via HTTP:

```bash
morningstar portal serve
```

Opening `viewer.html` directly (via `file://`) may have limited functionality due to browser security restrictions.

### CSS not applying

Clear browser cache or hard refresh:
- macOS: `Cmd+Shift+R`
- Windows/Linux: `Ctrl+Shift+R`

---

## Related Documentation

- **[courtroom/RULES.md](../courtroom/RULES.md)** - Courtroom procedures
- **[courtroom/transcripts/README.md](../courtroom/transcripts/README.md)** - Transcript format
- **[core/personalities.md](../core/personalities.md)** - Personality definitions

---

*"We have built a machine for saying 'no' thoughtfully. That may be the best we can hope for."*

— MORNINGSTAR
