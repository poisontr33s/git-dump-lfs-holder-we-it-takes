# 🧠 LLM Runner Constellation

This directory houses progressively more real ModelRunner implementations.

| Runner | Status | Purpose |
|--------|--------|---------|
| `dummy_llama_cpp_runner.ts` | placeholder | Validates orchestration plumbing without real inference |
| `llama_cpp_http_runner.ts` | initial real | Streams tokens from an already-running `llama.cpp --server` process |

## Llama.cpp HTTP Runner
Launch llama.cpp separately (example minimal command):
```
./main -m models/your-model.gguf --server --port 8080 --threads 8 --ctx-size 4096
```
Then orchestrator can instantiate the runner:
- Ensure registry entry contains correct artifact path
- Add future wiring to auto-detect server availability

## Planned
- vLLM sidecar runner
- Transformers subprocess bridge runner (Python spawn)
- Multimodal vision runner for image-grounded inference
