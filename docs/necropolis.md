# Necropolis - Failure Observability System

## Overview

Necropolis is a comprehensive failure observability system for the Psycho-Noir Kontrapunkt repository that transforms every error into valuable intelligence. The system captures, classifies, and aggregates failure data to create a perpetual "errors-to-solutions" learning loop.

## 🧙‍♂️ System Architecture

Necropolis consists of four main components:

### 1. Necromancer Collector (`.github/actions/necromancer-collect`)
A composite action that wraps commands to capture:
- Exit codes and execution duration
- stdout/stderr logs with structured parsing
- Environment context (OS, runner, Git metadata)
- Error classification using pattern recognition

### 2. Error Classification Engine (`.github/scripts/necromancer/parse_errors.py`)
Advanced pattern recognition system that classifies failures into:
- **Standard Categories**: DEPENDENCY_FAILURE, BUILD_FAILURE, TEST_FAILURE, etc.
- **Psycho-Noir Signatures**: KAUSALITETS_ARKITEKTEN_INTERFERENCE, SYNTETISKE_SYNAPSER_GLITCH, RUSTBELT_IMPROVISATION_CASCADE
- **Fingerprinting**: Unique error signatures for grouping similar failures

### 3. Knowledge Base Aggregator (`.github/scripts/necromancer/aggregate.py`)
Merges distributed failure artifacts into:
- Comprehensive taxonomy reports
- Temporal failure pattern analysis
- Actionable recommendations
- Psycho-Noir thematic analysis

### 4. Workflow Orchestration
- **verify.yml**: Fast PR-time failure collection (minimal overhead)
- **necropolis.yml**: Comprehensive nightly matrix runs (extensive coverage)
- **triage-comment.yml**: Sticky PR comments with failure summaries

## 🚀 Getting Started

### Basic Usage

Wrap any command with the Necromancer collector:

```yaml
- name: Run tests with failure capture
  uses: ./.github/actions/necromancer-collect
  with:
    name: 'frontend-tests'
    run: 'npm test'
    category: 'frontend'
    variant: 'node-18'
    timeout-minutes: 10
```

### Workflow Integration

Add to your existing workflow:

```yaml
jobs:
  test-with-necropolis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install dependencies
        uses: ./.github/actions/necromancer-collect
        with:
          name: 'install-deps'
          run: 'npm ci'
          category: 'frontend'
          variant: 'production'
        continue-on-error: true  # Don't fail workflow, but capture data
```

## 📊 Understanding Reports

### Taxonomy Report Structure

```json
{
  "summary": {
    "total_outcomes": 42,
    "overall_success_rate": 85.7,
    "total_failures": 6,
    "unique_error_types": 3
  },
  "error_taxonomy": {
    "error_types": {
      "DEPENDENCY_FAILURE": 3,
      "TEST_FAILURE": 2,
      "BUILD_FAILURE": 1
    },
    "top_fingerprints": [
      {
        "fingerprint": "npm ERR! peer dep missing",
        "count": 3,
        "examples": ["npm-install", "npm-ci-cache"]
      }
    ]
  }
}
```

### Error Categories

| Category | Description | Examples |
|----------|-------------|----------|
| `ENVIRONMENT_SETUP` | Environment configuration issues | Missing executables, permission errors |
| `DEPENDENCY_FAILURE` | Package management problems | npm/pip install failures, version conflicts |
| `BUILD_FAILURE` | Compilation and build issues | TypeScript errors, webpack failures |
| `TEST_FAILURE` | Test execution problems | Assertion failures, timeout issues |
| `LINT_FAILURE` | Code quality violations | ESLint errors, formatting issues |
| `SECURITY_FINDING` | Security scan results | Vulnerability detections |
| `DISK_SPACE` | Storage-related failures | Out of space errors |
| `TIMEOUT` | Time limit exceeded | Long-running process termination |
| `CANCELLED` | User or system cancellation | Workflow cancellation |

### Psycho-Noir Signatures

Special error patterns that reflect the thematic elements of the project:

- **KAUSALITETS_ARKITEKTEN_INTERFERENCE**: Predictive system corruption
- **SYNTETISKE_SYNAPSER_GLITCH**: Neural network malfunctions  
- **RUSTBELT_IMPROVISATION_CASCADE**: Improvised system failures

## 🔧 Configuration

### Repository Variables

Configure in GitHub repository settings:

| Variable | Default | Description |
|----------|---------|-------------|
| `NECRO_BRANCH` | `necropolis` | Branch for persistent knowledge storage |
| `NECRO_ARTIFACT_RETENTION_DAYS` | `14` | Artifact retention period |
| `AI_SUGGESTIONS` | `false` | Enable AI-powered suggestions |

### Repository Secrets

Optional secrets for enhanced functionality:

| Secret | Purpose |
|--------|---------|
| `OPENAI_API_KEY` | Enable AI-powered failure analysis |

### Path Filters

Necropolis automatically detects and skips docs-only changes to minimize noise.

## 🎭 Psycho-Noir Integration

Necropolis is designed to complement the existing Neural Archaeology systems while providing deterministic, fast feedback. The thematic integration includes:

### Den Usynlige Hånd Manifestations
Unusual error patterns are flagged as potential manifestations of "Den Usynlige Hånd" - the hidden force that manipulates both domains.

### Skyskraper vs Rustbelt Analysis
Error patterns are analyzed through the lens of the project's dual-domain structure:
- **Skyskraper errors**: Clean, structured, often related to sophisticated tooling
- **Rustbelt errors**: Chaotic, improvised, resource-constrained patterns

## 🔄 Continuous Learning Loop

1. **Capture**: Every command execution is monitored
2. **Classify**: Errors are categorized and fingerprinted
3. **Aggregate**: Data is merged into comprehensive reports
4. **Learn**: Patterns inform future prevention strategies
5. **Recommend**: Actionable insights are generated
6. **Repeat**: The cycle continues with each execution

## 📈 Advanced Features

### Failure Fingerprinting
Similar failures are grouped by extracted patterns:
```
"Error: Test failed | SyntaxError: Unexpected token | npm ERR! Test failed"
```

### Multi-dimensional Analysis
- **Temporal**: Failure trends over time
- **Environmental**: OS/runtime specific patterns  
- **Categorical**: Failure type distributions
- **Thematic**: Psycho-Noir narrative elements

### Sticky Triage Comments
Automated PR comments provide:
- Immediate failure summaries
- Links to detailed reports
- Recommended remediation steps
- AI-powered suggestions (if enabled)

## 🛡️ Safety & Privacy

### No Breaking Changes
- All Necropolis functionality is additive
- Existing workflows continue unchanged
- System can be completely removed by reverting the PR

### No External Dependencies
- No external API calls without explicit secrets
- All processing happens within GitHub Actions
- Data stays within your repository ecosystem

### Resource Protection
- Comprehensive timeout protection
- Disk space monitoring and cleanup
- Memory usage safeguards in aggressive mode

## 🔍 Troubleshooting

### Common Issues

**Necromancer artifacts not found**
- Check workflow execution logs
- Verify `continue-on-error: true` is set appropriately
- Review artifact retention settings

**Classification errors**
- Examine log file content
- Check pattern matching in `parse_errors.py`
- Verify Python dependencies

**Aggregation failures**
- Confirm artifact download succeeded
- Check output directory permissions
- Review aggregation script logs

### Debug Mode

Enable verbose logging by setting environment variables:
```yaml
env:
  NECRO_DEBUG: true
  NECRO_VERBOSE: true
```

## 🌟 Contributing

Necropolis is designed to evolve with your failure patterns. To extend:

1. **Add Error Patterns**: Update `parse_errors.py` with new classifications
2. **Enhance Aggregation**: Extend `aggregate.py` with new analysis dimensions
3. **Improve Workflows**: Add new matrix combinations or test scenarios

## 📚 Related Systems

Necropolis integrates with existing Psycho-Noir Kontrapunkt systems:
- **Neural Archaeology**: Deeper behavioral analysis
- **Aggressive Failure Harvesting**: Intentional failure generation
- **Bidirectional Learning**: Solution mapping and prevention

---

*🏛️ Necropolis - Where every failure becomes wisdom in the eternal dance between order and chaos*