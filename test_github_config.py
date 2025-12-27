#!/usr/bin/env python3

"""
Test script to verify GitHub configuration files are properly set up.
"""

import os
import yaml
import json

def test_dependabot_config():
    """Test Dependabot configuration."""
    print("🔍 Testing Dependabot configuration...")
    
    config_path = '.github/dependabot.yml'
    if not os.path.exists(config_path):
        print("❌ Dependabot config file not found!")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Check for duplicate configurations
        pip_configs = [item for item in config['updates'] if item['package-ecosystem'] == 'pip']
        if len(pip_configs) > 1:
            print("❌ Duplicate pip configurations found!")
            return False
        
        # Check if lukew2580 is assigned
        for update in config['updates']:
            if 'assignees' in update and 'lukew2580' not in update['assignees']:
                print(f"❌ lukew2580 not assigned in {update['package-ecosystem']} config")
                return False
        
        print("✅ Dependabot configuration is valid!")
        return True
    except Exception as e:
        print(f"❌ Error reading Dependabot config: {e}")
        return False

def test_workflow_files():
    """Test GitHub workflow files."""
    print("🔍 Testing workflow files...")
    
    workflow_dir = '.github/workflows'
    if not os.path.exists(workflow_dir):
        print("❌ Workflows directory not found!")
        return False
    
    workflow_files = [
        'automated_review.yml',
        'github_sync.yml', 
        'daily_sync.yml'
    ]
    
    for workflow_file in workflow_files:
        file_path = os.path.join(workflow_dir, workflow_file)
        if not os.path.exists(file_path):
            print(f"❌ Workflow file {workflow_file} not found!")
            return False
        
        try:
            with open(file_path, 'r') as f:
                workflow = yaml.safe_load(f)
            
            # Check for absolute paths (should not contain /home/workspace)
            if '/home/workspace/' in json.dumps(workflow):
                print(f"❌ Absolute paths found in {workflow_file}")
                return False
            
            print(f"✅ {workflow_file} is valid!")
        except Exception as e:
            print(f"❌ Error reading {workflow_file}: {e}")
            return False
    
    return True

def test_issue_template():
    """Test issue template configuration."""
    print("🔍 Testing issue template...")
    
    config_path = '.github/ISSUE_TEMPLATE/config.yml'
    if not os.path.exists(config_path):
        print("❌ Issue template config file not found!")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        if 'contact_links' not in config:
            print("❌ No contact links found in issue template!")
            return False
        
        print("✅ Issue template is valid!")
        return True
    except Exception as e:
        print(f"❌ Error reading issue template: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting GitHub configuration tests...\n")
    
    tests = [
        test_dependabot_config,
        test_workflow_files,
        test_issue_template
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    if all(results):
        print("🎉 All GitHub configuration tests passed!")
        return True
    else:
        print("❌ Some tests failed. Please check the configuration files.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
