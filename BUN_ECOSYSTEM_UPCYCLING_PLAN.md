# 🌩️ Bun Ecosystem Upcycling Plan (Psycho‑Noir Modularization Initiative)

Purpose: Extract the most generically valuable, non‑lore‑locked components from this repository into clean, reusable Bun / TypeScript packages that strengthen both the Psycho‑Noir architecture *and* the broader Bun ML + orchestration ecosystem.

---
## 1. Reality Check: Bun Package Distribution
Bun does **not** have a separate registry. It consumes the **npm registry** (and GitHub Packages optionally). So: we publish standard ESM packages with `"type": "module"` + `exports` map. No special Bun-only index required. Performance gains vs Node come for free when consumers run under Bun.

---
## 2. Candidate Modules (Phase Ordering)
| Phase | Package Name (proposed) | Scope | Stability | External Value |
|-------|-------------------------|-------|-----------|----------------|
| P0 | `@noir/runtime-contract` | `ModelRunner` interface + capabilities schema + errors | High | Provides neutral abstraction for multi-backend LLM runners |
| P0 | `@noir/model-registry` | JSON schema + loader + validation + drift-safe mutation helpers | High | Lightweight centralized registry pattern |
| P1 | `@noir/benchmark-harness` | First-token latency + throughput instrumentation helpers | Medium | Shared benchmarking primitives (pluggable runners) |
| P1 | `@noir/artifact-inspector` | GGUF (header-lite), file hashing, size classification | Medium | Universal integrity tooling |
| P2 | `@noir/intel-snapshot` | Snapshot persistence, diff (births/deaths/drift), volatility metrics | Medium | Generic time-series model meta diff engine |
| P2 | `@noir/auth-sentinel` | Authenticity + provenance heuristics (license/org risk scoring) | Medium | Helps consumers triage untrusted model repos |
| P3 | `@noir/anomaly-lab` | EWMA + percentile drift detection for latency/perplexity | Emerging | Cross-backend anomaly detection |
| P3 | `@noir/session-weaver` | Ephemeral + persistent streaming session state management | Emerging | Multi-run session continuity abstractions |

---
## 3. Extraction Strategy
1. **Neutralize Lore:** Provide a dual-export: `core` (neutral naming) + optional `psychoNoirFlavor` (decorators / narrativized wrappers).
2. **Dep Avoidance:** Zero runtime deps except `zod` (or handcrafted) for validation in early phases. Keep tree small.
3. **Unit Tests:** Use Bun test runner (`bun test`). Focus on contract invariants + edge input.
4. **Gradual Adoption:** Orchestrator updates import path module-by-module; old local copies removed only after green tests.
5. **Versioning:** Semantic (start `0.1.x`), lock internal consumers via caret; shift to `1.0.0` after 2 minor cycles without breaking change.

---
## 4. Minimal API Sketches
### `@noir/runtime-contract`
```ts
export interface ModelCapabilities { id: string; family: string; params_b: number | null; modalities: { text: boolean; vision?: boolean }; quantizations: string[]; }
export interface ModelRunner { init(): Promise<void>; ready: boolean; generateText(req: { prompt: string; maxTokens?: number; stream?: boolean }, onToken?: (t:{token:string;index:number;done?:boolean})=>void): Promise<{ text:string; tokens?:number; firstTokenLatencyMs?:number; tokensPerSecond?:number }>; unload(): Promise<void>; }
```

### `@noir/model-registry`
```ts
// load + validate
const { entries, diagnostics } = await loadRegistry({ path: 'model_registry.json' });
// safe mutation
updateBenchmark(entries, id, benchmarkRecord);
// write
await saveRegistry('model_registry.json', entries);
```

### `@noir/benchmark-harness`
```ts
await benchmarkRunner(runner, { prompt, maxTokens:64 }, { warmup: true, sample: true });
// returns { firstTokenMs, decodeTokPerSec, totalMs, tokens, meta }
```

### `@noir/artifact-inspector`
```ts
inspectArtifact('models/gemma.gguf');
// -> { exists:true, sizeBytes, sha256, gguf?: { n_vocab, n_layer, quantization }, riskFlags: [] }
```

---
## 5. Folder Layout Proposal
```
packages/
  runtime-contract/
  model-registry/
  benchmark-harness/
  artifact-inspector/
  intel-snapshot/
  auth-sentinel/
```
Root `package.json` (or create) declares workspaces; each package has:
```
package.json
src/index.ts
README.md
LICENSE
```

---
## 6. Upcycling Phases (Target Durations)
| Week | Deliverable |
|------|-------------|
| 0 | Extract runtime-contract + model-registry; orchestrator imports them |
| 1 | Add benchmark-harness + artifact-inspector with GGUF header lite parse |
| 2 | Port snapshot diff + authenticity heuristics into packages |
| 3 | Introduce anomaly lab (EWMA + band classification) + session-weaver |

Parallel: start vLLM sidecar integration after Week 1 (benchmark harness leverages real metrics).

---
## 7. Quality Gates per Package
- 100% ESM
- TypeScript strict
- No default export (clarity) except optional flavor namespace
- `exports` map + `types` field
- Bun test workflow: `bun test --coverage` (target >=85% statements core modules)

---
## 8. Community Positioning
Pitch each module as **model-backend agnostic primitives** (avoid meme naming in published API). Provide darker lore examples in README “Flavor Layer” section linking back to Psycho‑Noir main repo.

Potential tags: `llm`, `bun`, `ai-inference`, `observability`, `model-registry`, `benchmarking`.

---
## 9. Risk & Mitigation
| Risk | Mitigation |
|------|------------|
| Premature API freeze | Stay <1.0, publish CHANGELOG, gating label `@experimental` |
| Drift between internal + package copies | Immediate orchestrator migration on extraction commit |
| Slow adoption | Provide runnable example repo + copy/paste quick start |
| Over-coupling to psycho-noir vocabulary | Keep core neutral; lore adaptor wrapper adds narrative names |

---
## 10. Immediate Next Step (If Approved)
- Create `packages/runtime-contract` + `packages/model-registry` skeletons.
- Move (not copy) `src/runtime/model_runner.ts` content → runtime-contract (re-export locally for backward compatibility once).
- Add minimal test for `ModelRunner` readiness error.
- Update orchestrator imports.

Reply with: **"Commence P0 extraction"** to have it executed automatically.

---
## 11. Long-Term Evolution
- Add optional Rust-native addon (future) for artifact hashing -> fallback to JS if not present.
- Add GPU telemetry plugin interface (NVML / ROCm).
- Introduce `@noir/eval-corpora` curated small test sets (license-safe) for latency + perplexity quick probes.

---
## 12. License Strategy
Use Apache-2.0 for maximal adoption; add NOTICE referencing original psycho‑noir universe for narrative assets.

---
**Prepared for the Skyskraperen’s silent expansion. Awaiting your command to transmute code into modular soul-shards.**
