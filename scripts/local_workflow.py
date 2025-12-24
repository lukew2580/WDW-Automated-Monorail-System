#!/usr/bin/env python3

"""
Local Workflow Script
This script provides a local backup mechanism for GitHub operations.
"""

import os
import subprocess
import time
from datetime import datetime

# Configuration
REPO_DIR = "/home/workspace/WDW-Automated-Monorail-System"
BACKUP_DIR = "/home/workspace/WDW-Automated-Monorail-System-backup"
LOG_FILE = "/home/workspace/WDW-Automated-Monorail-System/github_sync.log"


def log(message):
    """Log a message to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")


def run_command(command, cwd=None):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        log(f"Error running command: {command}")
        log(f"Error output: {e.stderr}")
        raise


def backup_repository():
    """Create a backup of the repository."""
    log("Creating backup...")
    if os.path.exists(BACKUP_DIR):
        run_command(f"rm -rf {BACKUP_DIR}")
    run_command(f"cp -r {REPO_DIR} {BACKUP_DIR}")
    log("Backup created successfully.")


def sync_with_github():
    """Sync the repository with GitHub."""
    log("Syncing with GitHub...")
    os.chdir(REPO_DIR)
    
    # Pull latest changes
    run_command("git pull origin main")
    
    # Add and commit changes
    run_command("git add .")
    run_command("git commit -m 'chore: automated sync'")
    
    # Push changes
    run_command("git push origin main")
    
    log("Sync with GitHub completed successfully.")


def main():
    """Main function to run the local workflow."""
    log("Starting local workflow...")
    
    try:
        backup_repository()
        sync_with_github()
        log("Local workflow completed successfully.")
    except Exception as e:
        log(f"Local workflow failed: {e}")
        # Restore from backup if available
        if os.path.exists(BACKUP_DIR):
            log("Restoring from backup...")
            run_command(f"rm -rf {REPO_DIR}")
            run_command(f"cp -r {BACKUP_DIR} {REPO_DIR}")
            log("Restore completed.")
        else:
            log("No backup available for restore.")


if __name__ == "__main__":
    main()

