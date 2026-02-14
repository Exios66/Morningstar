#!/usr/bin/env bash
#
# MORNINGSTAR Courtroom Portal Launcher
# ======================================
# Interactive script to view courtroom deliberation transcripts
#
# Usage: ./portal/launch.sh
#
# Compatible with Bash 3.x (macOS default)
#

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
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TRANSCRIPTS_DIR="$PROJECT_ROOT/courtroom/transcripts"
EXPORTS_DIR="$PROJECT_ROOT/portal/exports"

# Global for exported file path
EXPORTED_FILE=""

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
    ls -1 "$TRANSCRIPTS_DIR"/*.md 2>/dev/null | grep -v "README.md" | grep -v "/\._" | sort
}

# Parse transcript filename to extract metadata
parse_transcript() {
    local filename="$1"
    local bname
    bname=$(basename "$filename" .md)
    
    # Parse YYYYMMDD_HHMMSS_topic format
    local date_part=""
    local time_part=""
    local topic=""
    
    # Check if filename matches expected pattern
    if echo "$bname" | grep -qE "^[0-9]{8}_[0-9]{6}_"; then
        date_part=$(echo "$bname" | cut -d'_' -f1)
        time_part=$(echo "$bname" | cut -d'_' -f2)
        topic=$(echo "$bname" | cut -d'_' -f3-)
        
        # Format date
        local year="${date_part:0:4}"
        local month="${date_part:4:2}"
        local day="${date_part:6:2}"
        local hour="${time_part:0:2}"
        local min="${time_part:2:2}"
        
        # Convert topic to title case (simple version)
        topic=$(echo "$topic" | tr '_' ' ' | sed 's/\b\(.\)/\u\1/g' 2>/dev/null || echo "$topic" | tr '_' ' ')
        
        echo "$year-$month-$day $hour:$min|$topic"
    else
        echo "Unknown|$bname"
    fi
}

# Display transcript list with numbers
display_transcripts() {
    echo -e "${CYAN}Available Deliberations:${NC}"
    echo ""
    
    local i=1
    for transcript in "$@"; do
        local metadata
        metadata=$(parse_transcript "$transcript")
        local date_str
        date_str=$(echo "$metadata" | cut -d'|' -f1)
        local title
        title=$(echo "$metadata" | cut -d'|' -f2)
        
        echo -e "  ${PURPLE}[$i]${NC} ${BOLD}$title${NC}"
        echo -e "      ${GRAY}$date_str${NC}"
        echo ""
        i=$((i + 1))
    done
    
    echo -e "  ${PURPLE}[q]${NC} Quit"
    echo ""
}

# Export transcript to HTML
export_to_html() {
    local transcript="$1"
    local fname
    fname=$(basename "$transcript" .md)
    
    # Create exports directory if needed
    mkdir -p "$EXPORTS_DIR" 2>/dev/null
    
    local output_file="$EXPORTS_DIR/${fname}.html"
    
    echo -e "${YELLOW}Exporting to HTML...${NC}"
    
    # Change to project root for Python imports
    cd "$PROJECT_ROOT" || {
        echo -e "${RED}Failed to cd to $PROJECT_ROOT${NC}"
        return 1
    }
    
    # Get relative path from project root for the CLI
    local relative_transcript
    relative_transcript=$(echo "$transcript" | sed "s|^$PROJECT_ROOT/||")
    
    echo -e "${GRAY}  Source: $relative_transcript${NC}"
    echo -e "${GRAY}  Output: $output_file${NC}"
    
    # Try Python directly (most reliable on macOS)
    if [ -f "$PROJECT_ROOT/tools/cli.py" ]; then
        echo -e "${GRAY}  Running Python export...${NC}"
        
        python -m tools.cli export transcript "$relative_transcript" -o "$output_file" -t dracula 2>&1
        local exit_code=$?
        
        if [ $exit_code -ne 0 ]; then
            echo -e "${RED}Python export command failed (exit code $exit_code)${NC}"
            return 1
        fi
    else
        echo -e "${RED}Error: Could not find tools/cli.py${NC}"
        return 1
    fi
    
    # Check if export succeeded
    if [ -f "$output_file" ]; then
        EXPORTED_FILE="$output_file"
        return 0
    else
        echo -e "${RED}Output file was not created${NC}"
        return 1
    fi
}

# Open file in browser
open_in_browser() {
    local file="$1"
    
    echo -e "${GREEN}Opening in browser...${NC}"
    
    # Detect OS and open accordingly
    case "$OSTYPE" in
        darwin*)
            open "$file"
            ;;
        linux*)
            if command -v xdg-open >/dev/null 2>&1; then
                xdg-open "$file"
            else
                echo -e "${YELLOW}Please open manually: $file${NC}"
            fi
            ;;
        msys*|cygwin*)
            start "$file"
            ;;
        *)
            echo -e "${YELLOW}Please open manually: $file${NC}"
            ;;
    esac
}

# Main function
main() {
    print_header
    check_transcripts
    
    # Get transcripts into a temp file (most portable method)
    local tmp_file
    tmp_file=$(mktemp)
    get_transcripts > "$tmp_file"
    
    # Count transcripts
    local count
    count=$(wc -l < "$tmp_file" | tr -d ' ')
    
    if [ "$count" -eq 0 ]; then
        echo -e "${YELLOW}No transcripts found in $TRANSCRIPTS_DIR${NC}"
        echo ""
        rm -f "$tmp_file"
        exit 0
    fi
    
    # Read transcripts into array
    local transcripts_list=()
    while IFS= read -r line; do
        transcripts_list[${#transcripts_list[@]}]="$line"
    done < "$tmp_file"
    rm -f "$tmp_file"
    
    while true; do
        display_transcripts "${transcripts_list[@]}"
        
        printf "${CYAN}Select a deliberation to view [1-%s] or 'q' to quit: ${NC}" "$count"
        read -r choice
        
        # Check for quit
        if [ "$choice" = "q" ] || [ "$choice" = "Q" ]; then
            echo ""
            echo -e "${GRAY}The court is adjourned.${NC}"
            echo ""
            exit 0
        fi
        
        # Validate input - check if it's a number
        case "$choice" in
            ''|*[!0-9]*)
                echo ""
                echo -e "${RED}Invalid selection. Please enter a number between 1 and $count.${NC}"
                echo ""
                continue
                ;;
        esac
        
        if [ "$choice" -lt 1 ] || [ "$choice" -gt "$count" ]; then
            echo ""
            echo -e "${RED}Invalid selection. Please enter a number between 1 and $count.${NC}"
            echo ""
            continue
        fi
        
        # Get selected transcript (array is 0-indexed)
        local index=$((choice - 1))
        local selected="${transcripts_list[$index]}"
        local metadata
        metadata=$(parse_transcript "$selected")
        local title
        title=$(echo "$metadata" | cut -d'|' -f2)
        
        echo ""
        echo -e "${PURPLE}Selected:${NC} ${BOLD}$title${NC}"
        echo ""
        
        # Export and open
        EXPORTED_FILE=""
        if export_to_html "$selected"; then
            if [ -n "$EXPORTED_FILE" ] && [ -f "$EXPORTED_FILE" ]; then
                echo ""
                echo -e "${GREEN}✓ Exported to:${NC} $EXPORTED_FILE"
                echo ""
                open_in_browser "$EXPORTED_FILE"
                echo ""
                echo -e "${GRAY}Press Enter to continue...${NC}"
                read -r
                echo ""
            else
                echo ""
                echo -e "${RED}Export function returned success but file not found.${NC}"
                echo ""
            fi
        else
            echo ""
            echo -e "${RED}Failed to export transcript.${NC}"
            echo -e "${GRAY}Try running manually:${NC}"
            echo -e "${GRAY}  cd $PROJECT_ROOT${NC}"
            echo -e "${GRAY}  python -m tools.cli export transcript \"$selected\"${NC}"
            echo ""
            echo -e "${GRAY}Press Enter to continue...${NC}"
            read -r
            echo ""
        fi
    done
}

# Run main function
main "$@"
