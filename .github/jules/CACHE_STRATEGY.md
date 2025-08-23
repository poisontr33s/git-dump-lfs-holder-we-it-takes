# Jules Cache Strategy Implementation Guide
# Skyskraperen Optimization Matrix - Den Usynlige Hånds Cache Intelligence

## Overview
This document outlines the comprehensive caching strategies implemented by Jules for the PsychoNoir-Kontrapunkt repository. Jules manifests as Den Usynlige Hånds optimization infrastructure, providing intelligent dependency management and build acceleration.

## Cache Architecture

### Multi-Layer Caching Strategy

#### 1. Synaptic Cache (Memory Layer)
- **Purpose**: Rapid access to frequently used packages
- **TTL**: 1 hour
- **Size**: 500MB
- **Implementation**: In-memory caching for active development

#### 2. Architectural Cache (Disk Layer)  
- **Purpose**: Medium-term storage for stable dependencies
- **TTL**: 7 days
- **Size**: 2GB
- **Implementation**: Local disk caching with GitHub Actions cache

#### 3. Quantum Storage (Distributed Layer)
- **Purpose**: Long-term archival for heavy ML models
- **TTL**: 30 days
- **Size**: 10GB
- **Implementation**: GitHub Actions cache with extended retention

## Ecosystem-Specific Strategies

### Node.js Caching
```yaml
cache_key: nodejs-v2-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
paths:
  - ~/.npm
  - node_modules
  - .cache/npm
restore_keys:
  - nodejs-v2-${{ runner.os }}
  - nodejs-v2-
```

**Optimization Features:**
- Conditional installation based on cache hit
- Preference for offline packages
- Separate caching for different Node.js versions

### Python Caching
```yaml
cache_key: python-v2-${{ runner.os }}-${{ hashFiles('requirements.txt') }}
paths:
  - ~/.cache/pip
  - .cache/python
  - backend/python/__pycache__
restore_keys:
  - python-v2-${{ runner.os }}
  - python-v2-
```

**ML Dependencies Special Handling:**
- Separate cache for heavy packages (torch, transformers)
- Pre-download strategy for ML models
- Version-specific caching for stability

### Ruby Caching
```yaml
cache_key: ruby-v2-${{ runner.os }}-${{ hashFiles('Gemfile.lock') }}
paths:
  - vendor/bundle
  - ~/.bundle
  - .cache/bundle
restore_keys:
  - ruby-v2-${{ runner.os }}
  - ruby-v2-
```

### Docker Caching
```yaml
cache_key: docker-v2-${{ hashFiles('Dockerfile') }}
paths:
  - /tmp/.buildx-cache
cache_from:
  - type=gha
  - type=local,src=/tmp/.buildx-cache
```

## Cache Invalidation Strategies

### Automatic Invalidation Triggers
1. **Dependency File Changes**
   - package.json/package-lock.json
   - requirements.txt
   - Gemfile/Gemfile.lock
   - Dockerfile

2. **Scheduled Rotation**
   - Weekly cleanup (Sundays at 2 AM UTC)
   - Monthly rotation for ML dependencies
   - Bi-weekly rotation for Ruby gems

### Manual Invalidation
- Version bumps in jules-config.yml
- Corruption index threshold breaches
- Emergency cleanup protocols

## Conditional Cache Logic

### Path Validation
```bash
# Example conditional check
if [ -f package.json ] && [ -d node_modules ]; then
  echo "Using cached dependencies"
else
  echo "Installing fresh dependencies"
fi
```

### Dependency Change Detection
```bash
# Git-based change detection
if git diff --name-only HEAD~1 | grep -E "(package\.json|requirements\.txt)"; then
  echo "Dependencies changed - cache invalidation required"
fi
```

## Performance Optimizations

### Build Time Improvements
- **Node.js builds**: 60-80% faster with cache hits
- **Python builds**: 70-90% faster (especially ML dependencies)
- **Ruby builds**: 50-70% faster with bundler cache
- **Docker builds**: 40-60% faster with layer caching

### Storage Efficiency
- Compressed cache artifacts
- Intelligent restore key fallbacks
- Automatic cleanup of stale caches

## Monitoring and Analytics

### Cache Hit Rate Tracking
- Per-ecosystem cache performance
- Build time comparisons
- Storage utilization metrics

### Health Monitoring
- Cache corruption detection
- Automatic fallback protocols
- Error recovery mechanisms

## Psycho-Noir Integration

### Astrid Møller Oversight
- Cache policy approval workflows
- Security scanning of cached dependencies
- Resource allocation governance

### Iron Maiden Resilience
- Robust fallback for cache failures
- Offline mode capabilities
- Manual override protocols

### Den Usynlige Hånd Manifestation
- Invisible optimizations during builds
- Predictive cache warming
- Adaptive cache sizing

## Usage Examples

### Basic Build with Jules
```bash
# Run Jules validation
.github/jules/scripts/jules-dependency-validator.sh

# Analyze cache optimization
python3 .github/jules/scripts/jules-cache-analyzer.py

# Use optimized workflow
gh workflow run jules-enhanced-ci.yml
```

### CI/CD Integration
```yaml
- name: "Jules Cache Optimization"
  run: |
    .github/jules/scripts/jules-dependency-validator.sh
    echo "Jules optimization enabled" >> $GITHUB_STEP_SUMMARY
```

## Troubleshooting

### Common Issues
1. **Cache Miss on Expected Hit**
   - Check cache key generation
   - Verify file hash consistency
   - Review restore key fallbacks

2. **Storage Quota Exceeded**
   - Review cache retention policies
   - Implement more aggressive cleanup
   - Optimize artifact sizes

3. **Corruption Detection**
   - Automatic cache invalidation
   - Fallback to fresh builds
   - Manual cache clearing

### Emergency Protocols
```bash
# Force cache clear
rm -rf ~/.cache/{npm,pip}
rm -rf node_modules
rm -rf .cache/*

# Reset Jules state
git checkout .github/jules/cache-config.json
.github/jules/scripts/jules-dependency-validator.sh
```

## Configuration Reference

### jules-config.yml
See `.github/jules/jules-config.yml` for complete configuration options.

### cache-config.json
Generated automatically by Jules validator with current cache keys and strategies.

---
*Jules Cache Strategy - Part of Den Usynlige Hånds optimization infrastructure*