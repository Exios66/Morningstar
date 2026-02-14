"""
MORNINGSTAR Feasibility Assessment Framework (MFAF) Implementation.

Provides tools for evaluating proposals using the MFAF methodology.
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, List, Tuple

# Rating definitions
RATINGS = {
    'F0': {'label': 'Infrastructural', 'authority': 'Prophet review'},
    'F1': {'label': 'Trivial', 'authority': 'Self-assign'},
    'F2': {'label': 'Moderate', 'authority': 'Senior engineer'},
    'F3': {'label': 'Significant', 'authority': 'Peer review'},
    'F4': {'label': 'Severe', 'authority': 'Full court'},
    'F5': {'label': 'Catastrophic', 'authority': 'Full court'},
}

# Risk vectors with their modifiers
RISK_VECTORS = {
    'authAuthz': {'label': 'Touches authentication/authorization', 'modifier': 0.5},
    'externalDependencies': {'label': 'Involves third-party dependencies', 'modifier': 0.5},
    'databaseMigration': {'label': 'Requires database migration', 'modifier': 0.5},
    'publicApi': {'label': 'Affects public API surface', 'modifier': 0.5},
    'unclearRequirements': {'label': 'Has unclear requirements', 'modifier': 0.5},
    'externalTeam': {'label': 'Depends on external team/service', 'modifier': 0.5},
    'previouslyFailed': {'label': 'Has been attempted before and failed', 'modifier': 1.0},
}

# Effort bands
EFFORT_BANDS = {
    'S': 'Hours',
    'M': 'Days',
    'L': 'Weeks',
    'XL': 'Months',
}


def calculate_effective_rating(base_rating: str, risk_modifier: float) -> str:
    """
    Calculate effective rating after applying risk modifiers.
    
    Args:
        base_rating: Base rating (F0-F5)
        risk_modifier: Total risk modifier
        
    Returns:
        Effective rating string
    """
    if base_rating == 'F0':
        return 'F0'  # F0 is special; doesn't get modified
    
    rating_order = ['F1', 'F2', 'F3', 'F4', 'F5']
    base_index = rating_order.index(base_rating)
    
    # Each 1.0 modifier increases rating by 1 level (round up at 0.5)
    levels_to_add = int(risk_modifier + 0.5)  # Rounds 0.5 -> 1, 1.5 -> 2, etc.
    
    effective_index = min(base_index + levels_to_add, len(rating_order) - 1)
    return rating_order[effective_index]


def calculate_risk_modifier(risk_vectors: Dict[str, bool]) -> float:
    """
    Calculate total risk modifier from active vectors.
    
    Args:
        risk_vectors: Dict mapping vector names to boolean (active/inactive)
        
    Returns:
        Total modifier value
    """
    total = 0.0
    for vector, active in risk_vectors.items():
        if active and vector in RISK_VECTORS:
            total += RISK_VECTORS[vector]['modifier']
    return total


def determine_recommendation(effective_rating: str, effort_band: str) -> str:
    """
    Determine recommended action based on rating and effort.
    
    Args:
        effective_rating: Effective MFAF rating
        effort_band: Effort magnitude (S/M/L/XL)
        
    Returns:
        Recommendation string
    """
    if effective_rating == 'F0':
        return 'ARCHIVE_F0'
    elif effective_rating in ['F1', 'F2']:
        return 'PROCEED'
    elif effective_rating == 'F3':
        return 'REVIEW'
    elif effective_rating in ['F4', 'F5']:
        return 'DELIBERATE'
    
    return 'REVIEW'  # Default


def format_assessment(assessment: Dict) -> str:
    """
    Format an assessment as a displayable string.
    
    Args:
        assessment: Assessment dictionary
        
    Returns:
        Formatted string
    """
    lines = []
    lines.append("┌─────────────────────────────────────────────────────────────────┐")
    lines.append("│ FEASIBILITY ASSESSMENT                                          │")
    lines.append("├─────────────────────────────────────────────────────────────────┤")
    
    proposal = assessment.get('proposal', 'Unknown')
    # Truncate long proposals
    if len(proposal) > 55:
        proposal = proposal[:52] + "..."
    lines.append(f"│ Proposal: {proposal:<53} │")
    
    lines.append("├─────────────────────────────────────────────────────────────────┤")
    
    base = assessment.get('baseRating', 'F1')
    base_label = RATINGS.get(base, {}).get('label', 'Unknown')
    lines.append(f"│ Base Rating:        {base} ({base_label}){' ' * (35 - len(base_label))}│")
    
    modifier = assessment.get('riskModifier', 0)
    lines.append(f"│ Risk Vectors:       +{modifier:<40.1f}│")
    
    # List active risk vectors
    risk_vectors = assessment.get('riskVectors', {})
    for vector, active in risk_vectors.items():
        if active:
            label = RISK_VECTORS.get(vector, {}).get('label', vector)
            if len(label) > 50:
                label = label[:47] + "..."
            lines.append(f"│   [x] {label:<55} │")
    
    effective = assessment.get('effectiveRating', base)
    effective_label = RATINGS.get(effective, {}).get('label', 'Unknown')
    lines.append(f"│ Effective Rating:   {effective} ({effective_label}){' ' * (35 - len(effective_label))}│")
    
    effort = assessment.get('effortBand', 'M')
    effort_label = EFFORT_BANDS.get(effort, 'Unknown')
    lines.append(f"│ Effort Band:        {effort} ({effort_label}){' ' * (37 - len(effort_label))}│")
    
    lines.append("├─────────────────────────────────────────────────────────────────┤")
    
    rec = assessment.get('recommendation', 'REVIEW')
    lines.append(f"│ Recommendation:     {rec:<42} │")
    
    lines.append("└─────────────────────────────────────────────────────────────────┘")
    
    return '\n'.join(lines)


def create_assessment(
    proposal: str,
    base_rating: str,
    risk_vectors: Dict[str, bool],
    effort_band: str,
    failure_scenario: Optional[Dict[str, str]] = None,
    notes: Optional[str] = None,
    assessor: Optional[str] = None
) -> Dict:
    """
    Create a complete MFAF assessment.
    
    Args:
        proposal: What is being assessed
        base_rating: Base feasibility rating (F0-F5)
        risk_vectors: Dict of risk vector states
        effort_band: Effort magnitude (S/M/L/XL)
        failure_scenario: Optional failure scenario for F3+
        notes: Optional additional notes
        assessor: Who performed the assessment
        
    Returns:
        Complete assessment dictionary
    """
    risk_modifier = calculate_risk_modifier(risk_vectors)
    effective_rating = calculate_effective_rating(base_rating, risk_modifier)
    recommendation = determine_recommendation(effective_rating, effort_band)
    
    assessment = {
        'proposal': proposal,
        'timestamp': datetime.now().isoformat(),
        'baseRating': base_rating,
        'riskVectors': risk_vectors,
        'riskModifier': risk_modifier,
        'effectiveRating': effective_rating,
        'effortBand': effort_band,
        'recommendation': recommendation,
    }
    
    if failure_scenario:
        assessment['failureScenario'] = failure_scenario
    
    if notes:
        assessment['notes'] = notes
        
    if assessor:
        assessment['assessor'] = assessor
    
    return assessment


def save_assessment(assessment: Dict, directory: Optional[str] = None) -> str:
    """
    Save an assessment to a JSON file.
    
    Args:
        assessment: Assessment dictionary
        directory: Directory to save to (defaults to state/assessments/)
        
    Returns:
        Path to saved file
    """
    if directory is None:
        directory = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'state', 'assessments'
        )
    
    os.makedirs(directory, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"assessment_{timestamp}.json"
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(assessment, f, indent=2)
    
    return filepath


def load_assessments(directory: Optional[str] = None) -> List[Dict]:
    """
    Load all assessments from the assessments directory.
    
    Args:
        directory: Directory to load from
        
    Returns:
        List of assessment dictionaries
    """
    if directory is None:
        directory = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'state', 'assessments'
        )
    
    if not os.path.exists(directory):
        return []
    
    assessments = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    assessment = json.load(f)
                    assessment['_filename'] = filename
                    assessments.append(assessment)
            except (json.JSONDecodeError, IOError):
                continue
    
    return assessments


# Interactive assessment helpers

def interactive_base_rating() -> str:
    """Get base rating through interactive prompts."""
    print("\nSelect base feasibility rating:")
    print("  0) F0 - Infrastructural (currently impossible, identifies missing capability)")
    print("  1) F1 - Trivial (isolated, well-understood, low risk)")
    print("  2) F2 - Moderate (cross-cutting but bounded)")
    print("  3) F3 - Significant (architectural implications)")
    print("  4) F4 - Severe (system-wide impact, high risk)")
    print("  5) F5 - Catastrophic (strong presumption against)")
    
    while True:
        choice = input("\nRating [0-5]: ").strip()
        if choice in ['0', '1', '2', '3', '4', '5']:
            return f'F{choice}'
        print("Invalid choice. Enter 0-5.")


def interactive_risk_vectors() -> Dict[str, bool]:
    """Get risk vector states through interactive prompts."""
    print("\nEvaluate risk vectors (y/n for each):")
    
    vectors = {}
    for key, info in RISK_VECTORS.items():
        modifier = info['modifier']
        while True:
            response = input(f"  {info['label']}? (+{modifier}) [y/n]: ").strip().lower()
            if response in ['y', 'yes', 'n', 'no', '']:
                vectors[key] = response in ['y', 'yes']
                break
            print("  Enter y or n")
    
    return vectors


def interactive_effort_band() -> str:
    """Get effort band through interactive prompts."""
    print("\nSelect effort band:")
    print("  S) Hours")
    print("  M) Days")
    print("  L) Weeks")
    print("  X) Months (XL)")
    
    while True:
        choice = input("\nEffort [S/M/L/X]: ").strip().upper()
        if choice == 'X':
            return 'XL'
        if choice in ['S', 'M', 'L', 'XL']:
            return choice
        print("Invalid choice. Enter S, M, L, or X.")


def run_interactive_assessment(proposal: str) -> Dict:
    """
    Run a complete interactive assessment.
    
    Args:
        proposal: What is being assessed
        
    Returns:
        Complete assessment dictionary
    """
    print(f"\n{'=' * 60}")
    print("MORNINGSTAR FEASIBILITY ASSESSMENT")
    print(f"{'=' * 60}")
    print(f"\nProposal: {proposal}")
    
    base_rating = interactive_base_rating()
    risk_vectors = interactive_risk_vectors()
    effort_band = interactive_effort_band()
    
    assessment = create_assessment(
        proposal=proposal,
        base_rating=base_rating,
        risk_vectors=risk_vectors,
        effort_band=effort_band,
        assessor="Interactive CLI"
    )
    
    print("\n" + format_assessment(assessment))
    
    return assessment
