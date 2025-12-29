#!/usr/bin/env python3
"""
Automated Daily GitHub Push
This script automates the process of pushing changes to GitHub once a day.
"""

import subprocess
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)sZ %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def run_command(command: str) -> bool:
    """Run a shell command and return True if successful."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"Command executed successfully: {command}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {command}")
        logger.error(f"Error: {e.stderr}")
        return False

def automated_github_push():
    """Automate the process of pushing changes to GitHub."""
    logger.info("Starting automated GitHub push...")
    
    # Navigate to the project directory
    project_dir = "/home/workspace/WDW-Automated-Monorail-System"
    run_command(f"cd {project_dir}")
    
    # Check for changes
    logger.info("Checking for changes...")
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    changes = result.stdout.strip()
    
    if not changes:
        logger.info("No changes detected. Skipping push.")
        return
    
    logger.info(f"Changes detected:\n{changes}")
    
    # Add all changes
    logger.info("Adding changes...")
    if not run_command("git add ."):
        logger.error("Failed to add changes.")
        return
    
    # Commit changes
    commit_message = f"Daily automated commit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    logger.info(f"Committing changes with message: {commit_message}")
    if not run_command(f"git commit -m '{commit_message}'"):
        logger.error("Failed to commit changes.")
        return
    
    # Push to GitHub
    logger.info("Pushing changes to GitHub...")
    if not run_command("git push origin main"):
        logger.error("Failed to push changes to GitHub.")
        return
    
    logger.info("Automated GitHub push completed successfully!")

if __name__ == "__main__":
    automated_github_push()

