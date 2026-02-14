#!/bin/bash
#
# MORNINGSTAR Courtroom Portal Launcher
# ======================================
# Interactive script to view courtroom deliberation transcripts
#
# Usage: ./portal/launch.sh
#

set -e

# Colors (Dracula theme)
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TRANSCRIPTS_DIR="$PROJECT_ROOT/courtroom/transcripts"
EXPORTS_DIR="$PROJECT_ROOT/portal/exports"

# Header
print_header() {
    echo ""
    echo -e "${PURPLE}┌─────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${PURPLE}│${NC}              ${BOLD}MORNINGSTAR COURTROOM PORTAL${NC}                      ${PURPLE}│${NC}"
    echo -e "${PURPLE}│${NC}    ${GRAY}\"The court has ruled. Regrettably sensible.\"${NC}               ${PURPLE}│${NC}"
    echo -e "${PURPLE}└─────────────────────────────────────────────────────────────────┘${NC}"
    echo ""
}

# Check if transcripts directory exists
check_transcripts() {
    if [ ! -d "$TRANSCRIPTS_DIR" ]; then
        echo -e "${RED}Error: Transcripts directory not found at $TRANSCRIPTS_DIR${NC}"
        exit 1
    fi
}

# Get list of transcripts (excluding hidden files and README)
get_transcripts() {
    find "$TRANSCRIPTS_DIR" -maxdepth 1 -name "*.md" -type f ! -name ".*" ! -name "README.md" | sort
}

# Parse transcript filename to extract metadata
parse_transcript() {
    local filename="$1"
    local basename=$(basename "$filename" .md)
    
    # Parse YYYYMMDD_HHMMSS_topic format
    if [[ $basename =~ ^([0-9]{8})_([0-9]{6})_(.+)$ ]]; then
        local date_part="${BASH_REMATCH[1]}"
        local time_part="${BASH_REMATCH[2]}"
        local topic="${BASH_REMATCH[3]}"
        
        # Format date
        local year="${date_part:0:4}"
        local month="${date_part:4:2}"
        local day="${date_part:6:2}"
        local hour="${time_part:0:2}"
        local min="${time_part:2:2}"
        
        # Convert topic to title case
        local title=$(echo "$topic" | tr '_' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')
        
        echo "$year-$month-$day $hour:$min|$title"
    else
        echo "Unknown|$basename"
    fi
}

# Display transcript list with numbers
display_transcripts() {
    local transcripts=("$@")
    local count=${#transcripts[@]}
    
    echo -e "${CYAN}Available Deliberations:${NC}"
    echo ""
    
    local i=1
    for transcript in "${transcripts[@]}"; do
        local metadata=$(parse_transcript "$transcript")
        local date=$(echo "$metadata" | cut -d'|' -f1)
        local title=$(echo "$metadata" | cut -d'|' -f2)
        
        echo -e "  ${PURPLE}[$i]${NC} ${BOLD}$title${NC}"
        echo -e "      ${GRAY}$date${NC}"
        echo ""
        ((i++))
    done
    
    echo -e "  ${PURPLE}[q]${NC} Quit"
    echo ""
}

# Export transcript to HTML
export_to_html() {
    local transcript="$1"
    local basename=$(basename "$transcript" .md)
    
    # Create exports directory if needed
    mkdir -p "$EXPORTS_DIR"
    
    local output_file="$EXPORTS_DIR/${basename}.html"
    
    echo -e "${YELLOW}Exporting to HTML...${NC}"
    
    # Check if morningstar CLI is available
    if command -v morningstar &> /dev/null; then
        morningstar export transcript "$transcript" -o "$output_file" -t dracula
    elif [ -f "$PROJECT_ROOT/tools/cli.py" ]; then
        # Fall back to running Python directly
        cd "$PROJECT_ROOT"
        python -m tools.cli export transcript "$transcript" -o "$output_file" -t dracula
    else
        echo -e "${RED}Error: Could not find morningstar CLI or tools/cli.py${NC}"
        return 1
    fi
    
    echo "$output_file"
}

# Open file in browser
open_in_browser() {
    local file="$1"
    
    echo -e "${GREEN}Opening in browser...${NC}"
    
    # Detect OS and open accordingly
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open "$file"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v xdg-open &> /dev/null; then
            xdg-open "$file"
        elif command -v gnome-open &> /dev/null; then
            gnome-open "$file"
        else
            echo -e "${YELLOW}Please open manually: $file${NC}"
        fi
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        # Windows
        start "$file"
    else
        echo -e "${YELLOW}Please open manually: $file${NC}"
    fi
}

# Main menu loop
main() {
    print_header
    check_transcripts
    
    # Get transcripts as array
    local transcripts_list
    mapfile -t transcripts_list < <(get_transcripts)
    
    local count=${#transcripts_list[@]}
    
    if [ $count -eq 0 ]; then
        echo -e "${YELLOW}No transcripts found in $TRANSCRIPTS_DIR${NC}"
        echo ""
        exit 0
    fi
    
    while true; do
        display_transcripts "${transcripts_list[@]}"
        
        echo -e -n "${CYAN}Select a deliberation to view [1-$count] or 'q' to quit: ${NC}"
        read -r choice
        
        # Check for quit
        if [[ "$choice" == "q" ]] || [[ "$choice" == "Q" ]]; then
            echo ""
            echo -e "${GRAY}The court is adjourned.${NC}"
            echo ""
            exit 0
        fi
        
        # Validate input
        if ! [[ "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -gt $count ]; then
            echo ""
            echo -e "${RED}Invalid selection. Please enter a number between 1 and $count.${NC}"
            echo ""
            continue
        fi
        
        # Get selected transcript (array is 0-indexed)
        local selected="${transcripts_list[$((choice-1))]}"
        local metadata=$(parse_transcript "$selected")
        local title=$(echo "$metadata" | cut -d'|' -f2)
        
        echo ""
        echo -e "${PURPLE}Selected:${NC} ${BOLD}$title${NC}"
        echo ""
        
        # Export and open
        local html_file
        html_file=$(export_to_html "$selected")
        
        if [ $? -eq 0 ] && [ -f "$html_file" ]; then
            echo -e "${GREEN}✓ Exported to:${NC} $html_file"
            echo ""
            open_in_browser "$html_file"
            echo ""
            echo -e "${GRAY}Press Enter to continue...${NC}"
            read -r
            echo ""
        else
            echo -e "${RED}Failed to export transcript.${NC}"
            echo ""
        fi
    done
}

# Run main function
main "$@"
