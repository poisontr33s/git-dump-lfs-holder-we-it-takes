#!/usr/bin/env python3
"""
Test script to validate artifact workflow standards compliance.
"""

import re
import yaml
import sys
from pathlib import Path

def test_artifact_naming():
    """Test that all artifact names follow the standard pattern."""
    workflows_dir = Path('.github/workflows')
    
    # Pattern for valid artifact names (should include matrix variables)
    valid_patterns = [
        r'.*-\$\{\{ matrix\.\w+ \}\}.*',  # Contains matrix variable
        r'.*-\$\{\{ github\.(sha|run_number) \}\}.*',  # Contains commit/run identifier
        r'.*-\$\{\{ \w+\.\w+ \}\}.*',  # Contains some dynamic variable
    ]
    
    issues = []
    
    for workflow_file in workflows_dir.glob('*.yml'):
        print(f"Checking {workflow_file}...")
        
        with open(workflow_file, 'r') as f:
            content = yaml.safe_load(f)
        
        # Find all upload-artifact and download-artifact actions
        def find_artifacts(obj, path=""):
            if isinstance(obj, dict):
                if obj.get('uses', '').startswith('actions/upload-artifact@'):
                    name = obj.get('with', {}).get('name', '')
                    if name:
                        # Check if name follows pattern
                        if not any(re.search(pattern, name) for pattern in valid_patterns):
                            issues.append(f"{workflow_file}:{path} - Artifact name '{name}' doesn't include matrix variables")
                
                if obj.get('uses', '').startswith('actions/download-artifact@'):
                    name = obj.get('with', {}).get('name', '')
                    pattern = obj.get('with', {}).get('pattern', '')
                    if name and not any(re.search(p, name) for p in valid_patterns):
                        # Skip pattern-based downloads and hardcoded production builds
                        if not pattern and 'production' not in path.lower() and 'deploy' not in path.lower():
                            issues.append(f"{workflow_file}:{path} - Download artifact name '{name}' doesn't include matrix variables")
                
                for key, value in obj.items():
                    find_artifacts(value, f"{path}.{key}" if path else key)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    find_artifacts(item, f"{path}[{i}]")
        
        find_artifacts(content)
    
    return issues

def test_action_versions():
    """Test that all artifact actions use v4."""
    workflows_dir = Path('.github/workflows')
    issues = []
    
    for workflow_file in workflows_dir.glob('*.yml'):
        with open(workflow_file, 'r') as f:
            content = f.read()
        
        # Find deprecated versions
        deprecated_patterns = [
            r'actions/upload-artifact@v[23]',
            r'actions/download-artifact@v[23]'
        ]
        
        for pattern in deprecated_patterns:
            matches = re.findall(pattern, content)
            if matches:
                issues.append(f"{workflow_file} - Found deprecated artifact action: {matches}")
        
        # Ensure v4 is used
        if 'upload-artifact@' in content or 'download-artifact@' in content:
            if 'upload-artifact@v4' not in content and 'download-artifact@v4' not in content:
                issues.append(f"{workflow_file} - Artifact actions found but not using v4")
    
    return issues

def test_matrix_uniqueness():
    """Test that matrix jobs have unique artifact names."""
    workflows_dir = Path('.github/workflows')
    issues = []
    
    for workflow_file in workflows_dir.glob('*.yml'):
        with open(workflow_file, 'r') as f:
            content = yaml.safe_load(f)
        
        def check_job_matrix(job_name, job_data):
            strategy = job_data.get('strategy', {})
            matrix = strategy.get('matrix', {})
            
            if matrix and isinstance(matrix, dict):
                # This job uses matrix strategy
                matrix_vars = [key for key in matrix.keys() if key != 'include']
                
                # Find upload artifacts in this job
                def find_uploads(obj):
                    uploads = []
                    if isinstance(obj, dict):
                        if obj.get('uses', '').startswith('actions/upload-artifact@'):
                            name = obj.get('with', {}).get('name', '')
                            uploads.append(name)
                        for value in obj.values():
                            uploads.extend(find_uploads(value))
                    elif isinstance(obj, list):
                        for item in obj:
                            uploads.extend(find_uploads(item))
                    return uploads
                
                uploads = find_uploads(job_data)
                
                for upload_name in uploads:
                    if upload_name:
                        # Check if any matrix variable is referenced
                        matrix_referenced = any(f'matrix.{var}' in upload_name for var in matrix_vars)
                        if not matrix_referenced and matrix_vars:
                            issues.append(f"{workflow_file}:{job_name} - Matrix job artifact '{upload_name}' doesn't reference matrix variables {matrix_vars}")
        
        jobs = content.get('jobs', {})
        for job_name, job_data in jobs.items():
            check_job_matrix(job_name, job_data)
    
    return issues

def main():
    """Run all tests."""
    print("🧪 Testing Artifact Workflow Standards Compliance")
    print("=" * 50)
    
    all_issues = []
    
    print("\n1. Testing artifact naming patterns...")
    naming_issues = test_artifact_naming()
    all_issues.extend(naming_issues)
    
    print("\n2. Testing action versions...")
    version_issues = test_action_versions()
    all_issues.extend(version_issues)
    
    print("\n3. Testing matrix uniqueness...")
    matrix_issues = test_matrix_uniqueness()
    all_issues.extend(matrix_issues)
    
    print("\n" + "=" * 50)
    
    if all_issues:
        print("❌ Issues found:")
        for issue in all_issues:
            print(f"  - {issue}")
        return 1
    else:
        print("✅ All tests passed! Workflows comply with artifact standards.")
        return 0

if __name__ == '__main__':
    sys.exit(main())