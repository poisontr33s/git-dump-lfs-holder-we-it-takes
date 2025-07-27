# GitHub Workflows Documentation

This directory contains the standardized GitHub Actions workflows for the PsychoNoir-Kontrapunkt repository. All workflows follow the [Artifact Workflow Standard](./ARTIFACT_WORKFLOW_STANDARD.md).

## Workflows Overview

### 1. CodeQL Advanced (`codeql.yml`)
**Purpose**: Security scanning and vulnerability detection
**Triggers**: Push to main, PRs to main, weekly schedule
**Languages**: Python, Ruby
**Artifacts**:
- `codeql-results-{language}-{run_number}` - Raw analysis results
- `codeql-summary-{language}-{run_number}` - Analysis summaries  
- `codeql-consolidated-report-{sha}` - Combined report from all languages

### 2. CI - Build and Test (`ci.yml`)
**Purpose**: Comprehensive build, test, and integration pipeline
**Triggers**: Push to main/develop, PRs to main
**Matrix Strategies**:
- Frontend: Multiple browsers × Node.js versions
- Backend: Multiple OS × Python versions
- Testing: Multiple OS × Node.js versions

**Artifacts**:
- `frontend-build-{browser}-node{version}` - Frontend builds
- `backend-python-{os}-py{version}` - Python packages
- `test-results-python-{os}-py{version}` - Python test results
- `test-results-jest-{os}-node{version}` - Jest test results
- `integration-report-{sha}` - Combined integration report
- `deployment-package-{sha}` - Production deployment package

## Artifact Naming Convention

All artifacts follow the pattern: `{type}-{matrix-variables}-{version/identifier}`

Examples:
- ✅ `build-ubuntu-latest-node18`
- ✅ `test-results-windows-latest-py3.11`
- ✅ `codeql-results-python-12345`
- ❌ `build` (missing matrix variables)
- ❌ `test-results` (missing specificity)

## Matrix Strategy Best Practices

### Frontend Matrix
```yaml
strategy:
  matrix:
    browser: [chrome, firefox, safari]
    node-version: [18, 20]
# Artifact name: frontend-build-${{ matrix.browser }}-node${{ matrix.node-version }}
```

### Backend Matrix
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ['3.9', '3.10', '3.11']
# Artifact name: backend-python-${{ matrix.os }}-py${{ matrix.python-version }}
```

## Artifact Lifecycle

1. **Build Jobs**: Create artifacts with matrix-specific names
2. **Integration Jobs**: Download multiple artifacts using patterns
3. **Deployment Jobs**: Select specific artifacts for production
4. **Cleanup**: Automatic retention based on artifact type

## Adding New Workflows

When creating new workflows:

1. Follow the [Artifact Workflow Standard](./ARTIFACT_WORKFLOW_STANDARD.md)
2. Use `actions/upload-artifact@v4` and `actions/download-artifact@v4` exclusively
3. Include matrix variables in artifact names for uniqueness
4. Set appropriate retention days
5. Add error handling for critical paths
6. Update this documentation

## Common Patterns

### Conditional Upload
```yaml
- name: Upload on failure
  uses: actions/upload-artifact@v4
  if: failure()
  with:
    name: failure-logs-${{ matrix.os }}-${{ github.run_number }}
    path: logs/
    retention-days: 3
```

### Cross-job Dependencies
```yaml
job2:
  needs: job1
  steps:
    - name: Download from job1
      uses: actions/download-artifact@v4
      with:
        name: output-${{ matrix.variable }}
        path: ./input/
```

### Pattern-based Download
```yaml
- name: Download all test results
  uses: actions/download-artifact@v4
  with:
    pattern: test-results-*
    path: ./all-tests/
    merge-multiple: true
```

## Troubleshooting

### Common Issues

1. **Artifact Not Found**
   - Check artifact name matches exactly (case-sensitive)
   - Verify the uploading job completed successfully
   - Ensure matrix variables are included in name

2. **Matrix Variable Conflicts**
   - Use unique combinations in artifact names
   - Include all relevant matrix dimensions
   - Test with minimal matrix first

3. **Retention Exceeded**
   - Check retention-days setting
   - Download artifacts before they expire
   - Use appropriate retention for artifact type

### Debugging Tips

1. Use `continue-on-error: true` for optional downloads
2. Add `if: always()` to upload debug artifacts
3. List available artifacts in consolidation jobs
4. Use descriptive artifact names for easier identification

## Security Considerations

- Never upload secrets or credentials as artifacts
- Use appropriate retention periods to minimize exposure
- Be mindful of artifact size limits (10GB per artifact)
- Consider who has access to workflow artifacts

## Performance Tips

- Use `merge-multiple: true` when downloading many artifacts
- Compress large artifacts before upload
- Use specific patterns instead of downloading all artifacts
- Set shorter retention for temporary/debug artifacts

---

For more detailed information, see the [Artifact Workflow Standard](./ARTIFACT_WORKFLOW_STANDARD.md).