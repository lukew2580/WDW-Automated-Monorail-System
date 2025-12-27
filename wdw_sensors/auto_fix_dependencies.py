#!/usr/bin/env python3
"""
Auto-Fix Dependencies Script
Automatically updates dependencies and commits changes.
"""

import subprocess
import yaml
import os

def update_dependencies():
    """Update dependencies and commit changes"""
    # Read dependabot.yml
    with open(".github/dependabot.yml", "r") as f:
        dependabot_config = yaml.safe_load(f)
    
    # Check for outdated dependencies
    result = subprocess.run(["pip", "list", "--outdated"], capture_output=True, text=True)
    if not result.stdout.strip():
        print("No outdated dependencies found.")
        return
    
    # Auto-update
    subprocess.run(["pip", "install", "--upgrade", "-r", "requirements.txt"], check=True)
    
    # Commit changes
    subprocess.run(["git", "add", "requirements.txt"], check=True)
    subprocess.run(["git", "commit", "-m", "chore: update dependencies"], check=True)
    subprocess.run(["git", "push"], check=True)
    
    print("Dependencies updated successfully.")

if __name__ == "__main__":
    update_dependencies()
