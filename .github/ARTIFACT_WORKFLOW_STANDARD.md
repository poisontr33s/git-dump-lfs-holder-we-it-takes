# Artifact Workflow Standard

## Overview

This document establishes the permanent convention for artifact management in the PsychoNoir-Kontrapunkt repository. All workflows must follow these standards to ensure consistency, reliability, and maintainability.

## Core Requirements

### 1. Action Versions
- **REQUIRED**: Use `actions/upload-artifact@v4` exclusively
- **REQUIRED**: Use `actions/download-artifact@v4` exclusively
- **FORBIDDEN**: Using deprecated versions (v2, v3) is not allowed

### 2. Artifact Naming Conventions

#### Basic Naming
- Use descriptive, lowercase names with hyphens
- Include the purpose and context
- Examples: `build-output`, `test-results`, `coverage-report`

#### Matrix Job Naming
- **REQUIRED**: Include matrix variables in artifact names for uniqueness
- Pattern: `{artifact-type}-{matrix-variable1}-{matrix-variable2}`
- Examples:
  - `build-ubuntu-latest-node18`
  - `test-results-macos-latest-python39`
  - `coverage-windows-latest-ruby31`

#### Version-specific Naming
- Include version information when relevant
- Pattern: `{artifact-type}-v{version}-{matrix-variables}`
- Example: `release-bundle-v1.2.3-linux-x64`

### 3. Standard Artifact Types

#### Build Artifacts
```yaml
- name: Upload build artifacts
  uses: actions/upload-artifact@v4
  with:
    name: build-${{ matrix.os }}-${{ matrix.node-version }}
    path: |
      dist/
      build/
      *.tar.gz
    retention-days: 30
```

#### Test Results
```yaml
- name: Upload test results
  uses: actions/upload-artifact@v4
  with:
    name: test-results-${{ matrix.os }}-${{ matrix.language }}
    path: |
      test-results/
      coverage/
      *.xml
      *.json
    retention-days: 7
```

#### Documentation
```yaml
- name: Upload documentation
  uses: actions/upload-artifact@v4
  with:
    name: docs-${{ github.sha }}
    path: docs/
    retention-days: 90
```

#### Python Package Artifacts
```yaml
- name: Upload Python packages
  uses: actions/upload-artifact@v4
  with:
    name: python-packages-${{ matrix.python-version }}
    path: |
      dist/*.whl
      dist/*.tar.gz
    retention-days: 30
```

### 4. Retention Policies

| Artifact Type | Retention Days | Justification |
|---------------|----------------|---------------|
| Build outputs | 30 | Intermediate builds for debugging |
| Test results | 7 | Short-term debugging needs |
| Release packages | 90 | Long-term distribution |
| Documentation | 90 | Reference material |
| Temporary files | 1 | Immediate debugging only |

### 5. Download Patterns

#### Single Artifact Download
```yaml
- name: Download build artifacts
  uses: actions/download-artifact@v4
  with:
    name: build-${{ matrix.os }}-${{ matrix.node-version }}
    path: ./artifacts/
```

#### Multiple Artifact Download
```yaml
- name: Download all test artifacts
  uses: actions/download-artifact@v4
  with:
    pattern: test-results-*
    path: ./test-artifacts/
    merge-multiple: true
```

#### Cross-job Artifact Sharing
```yaml
# Job 1: Build
build:
  runs-on: ubuntu-latest
  strategy:
    matrix:
      node-version: [18, 20]
  steps:
    - name: Upload build
      uses: actions/upload-artifact@v4
      with:
        name: build-${{ matrix.node-version }}
        path: dist/

# Job 2: Test (depends on build)
test:
  needs: build
  runs-on: ubuntu-latest
  strategy:
    matrix:
      node-version: [18, 20]
  steps:
    - name: Download build
      uses: actions/download-artifact@v4
      with:
        name: build-${{ matrix.node-version }}
        path: dist/
```

## Project-Specific Standards

### Frontend Build Artifacts
- HTML/CSS/JS bundles: `frontend-build-${{ matrix.browser }}`
- Minified assets: `frontend-minified-${{ github.sha }}`
- Source maps: `frontend-sourcemaps-${{ matrix.environment }}`

### Backend Python Artifacts
- Compiled packages: `backend-python-${{ matrix.python-version }}`
- Requirements freeze: `python-deps-${{ matrix.os }}`
- Model files: `ml-models-${{ github.sha }}`

### Test and Quality Artifacts
- Jest test results: `jest-results-${{ matrix.node-version }}`
- Python test coverage: `pytest-coverage-${{ matrix.python-version }}`
- CodeQL results: `codeql-${{ matrix.language }}`
- Linting reports: `lint-${{ matrix.tool }}-${{ matrix.language }}`

## Error Handling

### Conditional Upload
```yaml
- name: Upload artifacts on failure
  uses: actions/upload-artifact@v4
  if: failure()
  with:
    name: failure-logs-${{ matrix.os }}-${{ github.run_number }}
    path: |
      logs/
      *.log
    retention-days: 3
```

### Graceful Download
```yaml
- name: Download optional artifacts
  uses: actions/download-artifact@v4
  continue-on-error: true
  with:
    name: optional-cache-${{ matrix.os }}
    path: ./cache/
```

## Validation Checklist

Before merging any workflow changes, ensure:

- [ ] All artifact actions use v4
- [ ] No deprecated v2/v3 references exist
- [ ] Matrix job artifacts include matrix variables in names
- [ ] Retention days are set appropriately
- [ ] Artifact paths are correctly specified
- [ ] Download patterns match upload names
- [ ] Error handling is implemented where needed

## Migration from Legacy Versions

If updating existing workflows:

1. Replace `actions/upload-artifact@v2` → `actions/upload-artifact@v4`
2. Replace `actions/upload-artifact@v3` → `actions/upload-artifact@v4`
3. Replace `actions/download-artifact@v2` → `actions/download-artifact@v4`
4. Replace `actions/download-artifact@v3` → `actions/download-artifact@v4`
5. Add matrix variables to artifact names if using matrix strategy
6. Update retention-days to match this standard
7. Test the workflow to ensure artifacts are properly uploaded/downloaded

## Examples

See the following workflow files for reference implementations:
- `.github/workflows/ci.yml` - Complete CI with artifact management
- `.github/workflows/codeql.yml` - Security scanning with result artifacts

## Support

For questions about this standard or help implementing artifact workflows, please:
1. Check existing workflow files for examples
2. Review GitHub Actions documentation for actions/upload-artifact@v4
3. Open an issue with the `workflow` label

---

**Last Updated**: $(date)
**Version**: 1.0.0