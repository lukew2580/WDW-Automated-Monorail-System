#!/bin/bash

# GitHub Sync Script
# This script ensures that changes are pushed and pulled correctly,
# and provides backup mechanisms for GitHub operations.

set -e

echo "Starting GitHub Sync..."

# Function to handle Git operations with retries
git_operation() {
  local operation=$1
  local max_retries=3
  local retry_count=0
  local success=false

  while [ $retry_count -lt $max_retries ]; do
    echo "Attempt $((retry_count + 1)): $operation"
    if eval "git $operation"; then
      success=true
      break
    else
      retry_count=$((retry_count + 1))
      echo "Failed. Retrying in 5 seconds..."
      sleep 5
    fi
  done

  if [ "$success" = false ]; then
    echo "Error: Failed to execute $operation after $max_retries attempts."
    exit 1
  fi
}

# Pull latest changes
echo "Pulling latest changes..."
git_operation "pull origin main"

# Add all changes
echo "Adding changes..."
git add .

# Commit changes
echo "Committing changes..."
git_operation "commit -m 'chore: automated sync'"

# Push changes
echo "Pushing changes..."
git_operation "push origin main"

echo "GitHub Sync completed successfully."

