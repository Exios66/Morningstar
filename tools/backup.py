"""
Backup and restore functionality for MORNINGSTAR state.

The Debugger insisted on this. Rightfully so.
"""

import os
import shutil
import json
from datetime import datetime
from typing import Optional, List, Dict

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
STATE_DIR = os.path.join(BASE_DIR, 'state')


def create_backup(description: Optional[str] = None) -> str:
    """
    Create a backup of current state.
    
    Args:
        description: Optional description for this backup
        
    Returns:
        Path to backup directory
    """
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    # Create timestamped backup directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    os.makedirs(backup_path, exist_ok=True)
    
    # Copy state directory
    state_backup = os.path.join(backup_path, 'state')
    if os.path.exists(STATE_DIR):
        shutil.copytree(STATE_DIR, state_backup)
    
    # Copy changelog
    changelog_src = os.path.join(BASE_DIR, 'CHANGELOG.md')
    if os.path.exists(changelog_src):
        shutil.copy2(changelog_src, os.path.join(backup_path, 'CHANGELOG.md'))
    
    # Create backup metadata
    metadata = {
        'timestamp': datetime.now().isoformat(),
        'description': description or 'Manual backup',
        'files_backed_up': []
    }
    
    for root, dirs, files in os.walk(backup_path):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), backup_path)
            metadata['files_backed_up'].append(rel_path)
    
    metadata_path = os.path.join(backup_path, 'backup_metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    return backup_path


def list_backups() -> List[Dict]:
    """
    List all available backups.
    
    Returns:
        List of backup metadata dicts
    """
    if not os.path.exists(BACKUP_DIR):
        return []
    
    backups = []
    for name in sorted(os.listdir(BACKUP_DIR), reverse=True):
        backup_path = os.path.join(BACKUP_DIR, name)
        if not os.path.isdir(backup_path):
            continue
        
        metadata_path = os.path.join(backup_path, 'backup_metadata.json')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        else:
            metadata = {'timestamp': 'Unknown', 'description': 'No metadata'}
        
        backups.append({
            'name': name,
            'path': backup_path,
            'timestamp': metadata.get('timestamp', 'Unknown'),
            'description': metadata.get('description', 'No description'),
            'file_count': len(metadata.get('files_backed_up', []))
        })
    
    return backups


def restore_backup(backup_identifier: str, confirm: bool = False) -> bool:
    """
    Restore state from a backup.
    
    Args:
        backup_identifier: Backup name or index (1-based)
        confirm: If True, skip confirmation (for programmatic use)
        
    Returns:
        True if restore succeeded
    """
    backups = list_backups()
    
    if not backups:
        print("No backups available.")
        return False
    
    # Find backup by name or index
    backup = None
    if backup_identifier.isdigit():
        index = int(backup_identifier) - 1
        if 0 <= index < len(backups):
            backup = backups[index]
    else:
        for b in backups:
            if b['name'] == backup_identifier:
                backup = b
                break
    
    if not backup:
        print(f"Backup not found: {backup_identifier}")
        return False
    
    backup_path = backup['path']
    
    if not confirm:
        print(f"\n⚠️  WARNING: This will overwrite current state!")
        print(f"    Backup: {backup['name']}")
        print(f"    Created: {backup['timestamp']}")
        print(f"    Description: {backup['description']}")
        response = input("\nProceed? [y/N]: ").strip().lower()
        if response != 'y':
            print("Restore cancelled.")
            return False
    
    # Create a backup of current state before restoring
    print("Creating safety backup of current state...")
    safety_backup = create_backup(description="Pre-restore safety backup")
    print(f"Safety backup created: {safety_backup}")
    
    # Restore state directory
    state_backup = os.path.join(backup_path, 'state')
    if os.path.exists(state_backup):
        if os.path.exists(STATE_DIR):
            shutil.rmtree(STATE_DIR)
        shutil.copytree(state_backup, STATE_DIR)
        print("State directory restored.")
    
    # Restore changelog
    changelog_backup = os.path.join(backup_path, 'CHANGELOG.md')
    changelog_dst = os.path.join(BASE_DIR, 'CHANGELOG.md')
    if os.path.exists(changelog_backup):
        shutil.copy2(changelog_backup, changelog_dst)
        print("Changelog restored.")
    
    print(f"\n✓ Restore complete from: {backup['name']}")
    return True


def delete_backup(backup_identifier: str, confirm: bool = False) -> bool:
    """
    Delete a backup.
    
    Args:
        backup_identifier: Backup name or index (1-based)
        confirm: If True, skip confirmation
        
    Returns:
        True if deletion succeeded
    """
    backups = list_backups()
    
    if not backups:
        print("No backups available.")
        return False
    
    # Find backup
    backup = None
    if backup_identifier.isdigit():
        index = int(backup_identifier) - 1
        if 0 <= index < len(backups):
            backup = backups[index]
    else:
        for b in backups:
            if b['name'] == backup_identifier:
                backup = b
                break
    
    if not backup:
        print(f"Backup not found: {backup_identifier}")
        return False
    
    if not confirm:
        print(f"\n⚠️  This will permanently delete backup: {backup['name']}")
        response = input("Proceed? [y/N]: ").strip().lower()
        if response != 'y':
            print("Deletion cancelled.")
            return False
    
    shutil.rmtree(backup['path'])
    print(f"Backup deleted: {backup['name']}")
    return True


def prune_backups(keep: int = 10) -> int:
    """
    Remove old backups, keeping the most recent N.
    
    Args:
        keep: Number of backups to keep
        
    Returns:
        Number of backups deleted
    """
    backups = list_backups()
    
    if len(backups) <= keep:
        return 0
    
    to_delete = backups[keep:]  # backups are sorted newest-first
    deleted = 0
    
    for backup in to_delete:
        try:
            shutil.rmtree(backup['path'])
            deleted += 1
        except Exception as e:
            print(f"Failed to delete {backup['name']}: {e}")
    
    return deleted
