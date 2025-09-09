# 🛰️ GEMMA MOBILE RESEARCH INTEL MATRIX

Purpose: Structured tracking of external authoritative updates for Gemma / Gemma Mobile integration.
Scope: Deployment modes, quantization formats, memory/perf benchmarks, API/MCP server evolution, safety & licensing deltas.

## 🔍 Core Research Axes
- Model Variants: sizes, context windows, release tags, checksum verification
- Quantization: Q4_K_M, Q4_0, Q5_K_M, activation-aware, AWQ, GPTQ, GGUF vs safetensors pipeline
- Inference Backends: llama.cpp, execuTorch, MLC, WebGPU wasm runtime, Bun-native FFI prospects
- Mobile Optimization: scheduler choices, prompt caching, KV reuse, speculative decoding viability
- Safety / Policy: updated usage constraints, disallowed content guidelines, license clarifications
- Tooling: Official HF MCP capability changes, Google/Gemma docs new endpoints, embedding alignment notes

## 🧩 Open Questions (To Validate Externally)
1. Latest recommended minimal RAM envelope for 300M / 500M / 1B quantized.
2. Does official Gemma Mobile provide tokenizer delta or uses standard SentencePiece variant unchanged?
3. Changes in prompt formatting (system / user / safety blocks) for mobile vs flagship variants.
4. Official position on speculative decoding pipeline for sub‑1B deployments.
5. Any reference throughput metrics (tokens/sec) published for edge SoCs (A18, Snapdragon X Elite, Exynos 2500) under Q4_K_M.
6. WebGPU compatibility target matrix (Chrome, Edge, Safari Tech Preview) for wasm+SIMD activation.
7. Recommended max streaming chunk policy to reduce perceived latency.
8. Embedding / alignment shift logs (if new embedding model recommended alongside Gemma newer patch).

## 📦 Artifact Tracking
| Artifact | Desired Source | Status | Notes |
|----------|----------------|--------|-------|
| Official Model Card (latest) | google gemma docs | TODO | Capture version hash only |
| Quantization Guidelines | google optimization doc | TODO | Check for new tables |
| Inference Guide | google inference doc | TODO | Compare with existing assumptions |
| Safety Addendum | responsible usage doc | TODO | Flag deltas |
| HF MCP Tool Changes | HF MCP repo | TODO | Enumerate new tool names |
| Mobile Benchmarks | blog / release notes | TODO | FPS vs tok/s cross-check |

## 🧪 Planned Internal Experiments
- Token latency micro-bench harness (Bun + mock streaming to compare real later)
- ArchetypeBias injection position A/B test (pre vs mid prompt)
- KV cache retention across multi-turn simulated conversation
- Memory watermark logging (RSS snapshots every 250 tokens) once real backend integrated

## ⚠️ Risk Register
| Risk | Impact | Mitigation |
|------|--------|------------|
| Relying on mock engine too long | Divergence from real perf envelope | Timebox integration; set backend milestone |
| License drift unnoticed | Compliance issues | Scheduled diff of license text hash |
| Prompt format mismatch | Degraded generation quality | Track official formatting snippet |
| Over-aggressive archetype bias | Style collapse | Add bias attenuation curve |

## 🗓️ Update Cadence
- Weekly external sweep (HF model list, official docs, community benchmark threads)
- Hash commit any doc delta into `intel/` with summary

## ✅ Immediate Next Steps
1. Integrate optional HF token usage into oracle server (gated model meta).
2. Add placeholder real backend adapter interface in `gemma_mobile_engine.ts`.
3. Create benchmarking harness skeleton (`scripts/gemma_latency_probe.ts`).
4. Implement `.env` auto-loader for Bun servers.

---
Generated scaffold – ready for iterative population.
