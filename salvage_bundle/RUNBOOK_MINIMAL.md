# Minimal Runbook

Quick commands (Bun CLI one-shots):

- Integrity ping
  bun run unified_mcp_consciousness_orchestrator.ts --call orchestrator_integrity_ping

- Check env presence
  bun run unified_mcp_consciousness_orchestrator.ts --call env_secret_presence_probe

- Hardware-aware picks
  bun run unified_mcp_consciousness_orchestrator.ts --call hardware_model_recommendations '{"task_profile":"GENERAL","max_load_ms":900}'

- Exploratory loop (non-deterministic planning)
  bun run unified_mcp_consciousness_orchestrator.ts --call divergence_convergence_explore '{"seed":"What should we build next?","width":4,"depth":2}'

- Exploratory generation with degeneracy guard
  bun run unified_mcp_consciousness_orchestrator.ts --call gemma_mobile_explore '{"prompt":"Describe the noir skyline.","variants":3}'

- Persist intel snapshot
  bun run unified_mcp_consciousness_orchestrator.ts --call intel_snapshot_ritual_persist '{"label":"salvage"}'
