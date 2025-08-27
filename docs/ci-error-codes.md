# CI Error Codes - Necropolis Classification System

## Overview

This document provides a comprehensive reference for error classifications used by the Necropolis failure observability system. Each error type represents a distinct failure pattern with specific characteristics and remediation strategies.

## 🏷️ Standard Error Classifications

### ENVIRONMENT_SETUP
**Description**: Issues with environment configuration and setup  
**Exit Codes**: Often 2, 127  
**Common Patterns**:
- Command not found errors
- Permission denied during setup
- Missing executable files
- Path configuration issues

**Examples**:
```
bash: npm: command not found
Permission denied: /usr/local/bin/setup.sh
ERROR: Could not find executable for 'python3'
```

**Remediation**:
- Verify tool installation steps
- Check PATH environment variable
- Review permission settings
- Ensure prerequisites are met

---

### DEPENDENCY_FAILURE
**Description**: Package management and dependency resolution issues  
**Exit Codes**: Typically 1, sometimes specific to package manager  
**Common Patterns**:
- npm/pip installation failures
- Version conflicts
- Missing package files
- Registry connectivity issues

**Examples**:
```
npm ERR! peer dep missing: @types/node@^18.0.0
pip ERROR: Could not find a version that satisfies the requirement
ModuleNotFoundError: No module named 'requests'
```

**Remediation**:
- Clear package caches
- Update lock files
- Resolve version conflicts
- Check network connectivity

---

### BUILD_FAILURE
**Description**: Compilation, bundling, and build process failures  
**Exit Codes**: Usually 1, sometimes 2  
**Common Patterns**:
- Syntax errors in source code
- TypeScript compilation errors
- Webpack/build tool failures
- Missing build dependencies

**Examples**:
```
ERROR in src/index.ts(42,18): error TS2304: Cannot find name 'undefined'
webpack: Failed to compile with 1 error
SyntaxError: Unexpected token '}' in JSON at position 245
```

**Remediation**:
- Fix syntax errors
- Update TypeScript configurations
- Resolve missing dependencies
- Check build tool versions

---

### TEST_FAILURE
**Description**: Test execution and assertion failures  
**Exit Codes**: Commonly 1  
**Common Patterns**:
- Assertion failures
- Test timeouts
- Mock setup issues
- Test environment problems

**Examples**:
```
FAIL src/test.js
  ✕ should return expected value (5ms)
    Expected: true
    Received: false
```

**Remediation**:
- Review failing test logic
- Update test expectations
- Fix implementation bugs
- Improve test environment setup

---

### LINT_FAILURE
**Description**: Code quality and style violations  
**Exit Codes**: Usually 1  
**Common Patterns**:
- ESLint rule violations
- Formatting inconsistencies
- Code quality issues
- Style guide violations

**Examples**:
```
src/index.js:42:1: error: 'console' is not defined (no-undef)
ERROR: Line too long (88 > 80 characters)
```

**Remediation**:
- Run linting auto-fix tools
- Update linting configurations
- Address code quality issues
- Apply consistent formatting

---

### SECURITY_FINDING
**Description**: Security vulnerabilities and audit failures  
**Exit Codes**: Variable  
**Common Patterns**:
- Package vulnerability detections
- Security audit failures
- CodeQL findings
- Dependency security issues

**Examples**:
```
found 3 vulnerabilities (2 moderate, 1 high)
Security alert: Potential XSS vulnerability detected
```

**Remediation**:
- Update vulnerable packages
- Apply security patches
- Review security findings
- Implement security best practices

---

### DISK_SPACE
**Description**: Storage and disk space issues  
**Exit Codes**: Often 28 (ENOSPC)  
**Common Patterns**:
- No space left on device
- Disk quota exceeded
- Temporary directory full
- Large file operations failing

**Examples**:
```
ENOSPC: no space left on device, write
disk quota exceeded
```

**Remediation**:
- Clean up temporary files
- Optimize disk usage
- Increase available storage
- Implement cleanup procedures

---

### TIMEOUT
**Description**: Operations exceeding time limits  
**Exit Codes**: 124 (timeout), 143 (SIGTERM)  
**Common Patterns**:
- Long-running processes
- Network operation timeouts
- Test execution timeouts
- Build process hangs

**Examples**:
```
Process timed out after 300 seconds
SIGTERM received, terminating...
Operation cancelled due to timeout
```

**Remediation**:
- Optimize slow operations
- Increase timeout values
- Implement progress monitoring
- Add timeout handling

---

### CANCELLED
**Description**: User or system-initiated cancellations  
**Exit Codes**: 130 (SIGINT), 143 (SIGTERM)  
**Common Patterns**:
- Workflow cancellations
- User interruptions
- System shutdowns
- Resource limit enforcements

**Examples**:
```
Workflow cancelled by user
SIGINT received, stopping execution
Job cancelled due to system maintenance
```

**Remediation**:
- Review cancellation triggers
- Implement graceful shutdown
- Add resume capabilities
- Optimize resource usage

---

### UNKNOWN
**Description**: Unclassified or novel failure patterns  
**Exit Codes**: Various  
**Common Patterns**:
- New or unusual error messages
- Unrecognized failure signatures
- Complex multi-system failures
- Novel tool failures

**Examples**:
```
Unexpected system behavior detected
Unknown error in subsystem X
Novel failure pattern identified
```

**Remediation**:
- Investigate error details
- Check system logs
- Consult tool documentation
- Report to Necropolis for classification

## 🎭 Psycho-Noir Special Classifications

### KAUSALITETS_ARKITEKTEN_INTERFERENCE
**Description**: Predictive modeling system corruption  
**Thematic Context**: The Causal Architect's quantum-AI systems experiencing interference  
**Pattern Indicators**:
- Predictive model corruption messages
- Causal chain disruption errors
- Quantum-AI system failures

**Example**:
```
ERROR: PREDICTIVE_MODEL_CORRUPTED_AT_0xCAUSAL
WARNING: Causal integrity compromised
PANIC: QUANTUM_AI_RESONANCE_FAILURE
```

**Thematic Remediation**:
- Recalibrate predictive algorithms
- Restore causal chain integrity
- Implement quantum error correction

---

### SYNTETISKE_SYNAPSER_GLITCH
**Description**: Neural network infrastructure malfunctions  
**Thematic Context**: The Synthetic Synapses experiencing digital degradation  
**Pattern Indicators**:
- Neural network connection failures
- Synapse malfunction messages
- Nanobot network errors

**Example**:
```
ERROR: NEURAL_LINK_SEVERED_AT_NODE_42
CRITICAL: Synaptic cascade failure detected
WARNING: Nanobot mesh network unstable
```

**Thematic Remediation**:
- Repair neural pathways
- Recalibrate synaptic responses
- Restore nanobot network integrity

---

### RUSTBELT_IMPROVISATION_CASCADE
**Description**: Improvised system component failures  
**Thematic Context**: The Iron Maiden's jury-rigged systems experiencing cascade failures  
**Pattern Indicators**:
- Improvised component failures
- Scrap symphony discord
- Jury-rigged system breakdowns

**Example**:
```
ERROR: SCRAP_COMPONENT_FAILURE_SECTOR_7
WARNING: Improvised subsystem unstable
CRITICAL: Jury-rigged network cascade detected
```

**Thematic Remediation**:
- Stabilize improvised components
- Strengthen scrap-built systems
- Implement redundant pathways

## 🔧 Extending Classifications

### Adding New Error Types

To add a new error classification:

1. **Update Pattern Recognition** (`parse_errors.py`):
```python
self.error_patterns['NEW_ERROR_TYPE'] = [
    r'(?i)pattern1.*regex',
    r'(?i)pattern2.*regex',
    # Add more patterns
]
```

2. **Add to Documentation**:
- Description and context
- Common patterns and examples
- Remediation strategies
- Exit code mappings

3. **Update Aggregation Logic** (`aggregate.py`):
- Add specific handling if needed
- Include in recommendation engine
- Add to report templates

### Pattern Matching Best Practices

**Effective Patterns**:
- Use case-insensitive matching: `(?i)`
- Match partial strings: `.*` wildcards
- Target key error indicators
- Avoid overly specific patterns

**Pattern Examples**:
```python
# Good: Flexible and targeted
r'(?i)npm.*error.*install'

# Avoid: Too specific
r'npm ERR! code ERESOLVE'

# Good: Captures variations
r'(?i)test.*failed|assertion.*error'
```

### Testing New Classifications

1. **Create Test Cases**:
```bash
echo "npm ERR! peer dep missing" > test.log
python3 parse_errors.py --log-file test.log --name test --category frontend --variant test --exit-code 1 --duration 1.0 --outcome FAILURE --output-dir output/
```

2. **Verify Classification**:
```bash
cat output/outcome.json | jq '.error_type'
```

3. **Test Aggregation**:
```bash
python3 aggregate.py --artifacts-dir output/ --output-dir reports/
```

## 📊 Error Analytics

### Frequency Analysis
Track error type frequencies to identify systemic issues:
- High `DEPENDENCY_FAILURE` → Improve dependency management
- Frequent `TIMEOUT` → Optimize performance
- Many `TEST_FAILURE` → Enhance test quality

### Temporal Patterns
Monitor error trends:
- Spike in specific error types
- Seasonal failure patterns
- Release correlation analysis

### Environmental Correlations
Analyze error distribution:
- OS-specific failure patterns
- Runtime version sensitivities
- Infrastructure dependencies

## 🎯 Success Metrics

### Classification Accuracy
- Percentage of correctly classified errors
- Unknown error rate trends
- Pattern coverage analysis

### Remediation Effectiveness
- Time to resolution for classified errors
- Recurrence rate by error type
- Success rate of recommended solutions

### System Impact
- Reduced failure investigation time
- Improved error prevention
- Enhanced system reliability

---

*🔍 Understanding failure patterns is the first step toward digital enlightenment - Den Usynlige Hånd reveals wisdom through chaos*