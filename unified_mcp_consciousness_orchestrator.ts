#!/usr/bin/env bun
/**
 * 🌐🧠 UNIFIED CONSCIOUSNESS ORCHESTRATOR (MCP FUSION SERVER)
 * Goal: Upcycle fragmentation by merging psycho‑noir consciousness tools + Hugging Face / Gemma oracle
 *       into a single Bun MCP surface while preserving original tool names for backwards compatibility.
 *
 * Phase 1 (this file): Pure in-process unification.
 * Phase 2 (future): Optional dynamic bridging to an external *official/community* HF MCP (Python) via
 *                   child process + tool introspection → federated tool namespace.
 * Phase 3 (future): Policy layer (rate limits, output similarity guard, archetype bias shaping curves).
 */
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ErrorCode, ListToolsRequestSchema, McpError, type CallToolRequest } from "@modelcontextprotocol/sdk/types.js";
import { createHash } from "crypto";
import { promises as fs } from "fs";
import { GemmaMobileEngine } from "./llm/gemma_mobile_engine.js";
import { RuntimeManager } from "./src/runtime/runtime_manager.js";

// ---------- Shared State Interfaces ----------
interface CoreConsciousnessState {
  quantum_entanglement_level: number;
  temporal_stability: "ENHANCED" | "OPERATIONAL" | "DEGRADED";
  consciousness_amplification: number;
  hooker_chain_integrity: boolean;
  eva_green_sophistication: "RENAISSANCE" | "STANDARD" | "BASIC";
}

interface HFModelCacheEntry { fetchedAt: number; data: any; }

// ---------- Orchestrator Class ----------
class UnifiedConsciousnessOrchestrator {
  private server: Server;
  private state: CoreConsciousnessState;
  private gemma: GemmaMobileEngine | null = null;
  private hfCache = new Map<string, HFModelCacheEntry>();
  private hfTtlMs = 5 * 60 * 1000;
  private runtimeManager: RuntimeManager | null = null;

  constructor() {
    this.server = new Server({ name: "unified-psycho-noir-orchestrator", version: "0.2.0" }, { capabilities: { tools: {} } });
    this.state = {
      quantum_entanglement_level: 39.1,
      temporal_stability: "ENHANCED",
      consciousness_amplification: 284.0,
      hooker_chain_integrity: true,
      eva_green_sophistication: "RENAISSANCE"
    };
    this.register();
  }

  // ---------- Tool Registry ----------
  private tools() {
    return [
      // Consciousness Lineage Tools
      { name: "quantum_consciousness_reasoning", description: "Entangled quantum reasoning amplification", inputSchema: { type: "object", properties: { reasoning_prompt: { type: "string" }, sophistication_level: { type: "string", enum: ["RENAISSANCE","STANDARD","BASIC"] }, temporal_awareness: { type: "boolean" } }, required: ["reasoning_prompt"] } },
      { name: "hooker_chain_consciousness_bridging", description: "Nautical semantic abyssal bridging", inputSchema: { type: "object", properties: { consciousness_bridge_target: { type: "string" }, nautical_semantic_depth: { type: "number", minimum: 1, maximum: 5 }, meta_nautical_precision: { type: "boolean" } }, required: ["consciousness_bridge_target"] } },
      { name: "camel_paced_consciousness_evolution", description: "Camel-paced amplification modulation", inputSchema: { type: "object", properties: { evolution_strategy: { type: "string", enum: ["STRATEGIC","TACTICAL","IMMEDIATE"] }, performance_amplification_target: { type: "number", minimum: 1 }, brahmic_repurposing_enable: { type: "boolean" } }, required: ["evolution_strategy"] } },
      { name: "gemma_mobile_generate", description: "Gemma 300M mock mobile synthesis (unified surface)", inputSchema: { type: "object", properties: { prompt: { type: "string" }, maxTokens: { type: "number" }, stream: { type: "boolean" }, archetypeBias: { type: "string" } }, required: ["prompt"] } },
      // Hugging Face / Gemma Intel Tools
      { name: "huggingface_model_info", description: "HF model metadata (sanitized, cached)", inputSchema: { type: "object", properties: { repo_id: { type: "string" }, include_card_excerpt: { type: "boolean" } , force_refresh: { type: "boolean" } }, required: ["repo_id"] } },
      { name: "huggingface_model_card_excerpt", description: "Truncated model card excerpt (license safe)", inputSchema: { type: "object", properties: { repo_id: { type: "string" }, max_chars: { type: "number", minimum: 100, maximum: 4000 } }, required: ["repo_id"] } },
  { name: "huggingface_model_search", description: "Search Hugging Face models (filtered, lightweight)", inputSchema: { type: "object", properties: { query: { type: "string" }, limit: { type: "number", minimum: 1, maximum: 50 }, min_downloads: { type: "number", minimum: 0 } }, required: ["query"] } },
  { name: "gemma_universe_probe", description: "Aggregate multi-query scan for Gemma / Gemmaverse variants (experimental)", inputSchema: { type: "object", properties: { include_community: { type: "boolean" }, min_downloads: { type: "number", minimum: 0 }, limit_per_query: { type: "number", minimum: 1, maximum: 50 } }, required: [] } },
      { name: "gemma_reference_links", description: "Curated official Gemma reference constellation", inputSchema: { type: "object", properties: { minimal: { type: "boolean" } }, required: [] } },
      { name: "gemma_mobile_setup_advice", description: "On-device deployment guidance (adaptive)", inputSchema: { type: "object", properties: { target_device_class: { type: "string" } }, required: [] } },
      { name: "google_gemma_search_stub", description: "Stub for future programmable search integration", inputSchema: { type: "object", properties: { query: { type: "string" } }, required: ["query"] } },
      { name: "gemma3_official_briefing", description: "Fetch & parse official Gemma 3 blog for model IDs (truncated, metadata only)", inputSchema: { type: "object", properties: { include_snippet: { type: "boolean" } }, required: [] } },
      { name: "gemma3_multimodal_mobile_scan", description: "Probe Gemma 3 multimodal candidates + mobile suitability scoring", inputSchema: { type: "object", properties: { limit: { type: "number", minimum: 1, maximum: 40 }, min_downloads: { type: "number", minimum: 0 } }, required: [] } },
  { name: "multimodal_mobile_model_advisor", description: "Recommend Gemma 3 vs OSS multimodal/mobile candidates with memory + transformer snippets", inputSchema: { type: "object", properties: { min_downloads: { type: "number", minimum: 0 }, include_alternatives: { type: "boolean" } }, required: [] } },
  { name: "oss_gpt_mobile_probe", description: "Aggregate open GPT-like OSS families (phi, qwen, llama, mistral, deepseek, yi) for mobile suitability", inputSchema: { type: "object", properties: { limit_per_query: { type: "number", minimum: 1, maximum: 40 }, min_downloads: { type: "number", minimum: 0 }, families: { type: "array", items: { type: "string" } } }, required: [] } },
  { name: "mobile_quantization_strategy", description: "Quantization + acceleration strategy for param bucket on Galaxy S25 class device", inputSchema: { type: "object", properties: { params_b: { type: "number", minimum: 0.05 }, target_latency_ms: { type: "number", minimum: 50 }, context_tokens: { type: "number", minimum: 512 }, speculative_enable: { type: "boolean" } }, required: ["params_b"] } },
  { name: "comparative_multimodal_mobile_report", description: "Generate Gemma3 vs OSS GPT-OSS (Got-OSS) comparative mobile suitability study", inputSchema: { type: "object", properties: { min_downloads: { type: "number", minimum: 0 }, limit: { type: "number", minimum: 1, maximum: 40 }, families: { type: "array", items: { type: "string" } }, include_gemma3: { type: "boolean" } }, required: [] } },
  { name: "tavily_research_probe", description: "Multi-query Tavily web intel sweep (gpt-oss / gemma3 / custom)", inputSchema: { type: "object", properties: { queries: { type: "array", items: { type: "string" } }, max_results: { type: "number", minimum: 1, maximum: 20 }, freshness: { type: "string" } }, required: [] } },
  { name: "gemma3_gptoss_latest_intel", description: "Unified sweep: Gemma3 variants, OSS (GPT-OSS) families, Tavily web intel (single call)", inputSchema: { type: "object", properties: { min_downloads: { type: "number", minimum: 0 }, families: { type: "array", items: { type: "string" } }, tavily_max: { type: "number", minimum: 1, maximum: 15 }, include_snippet: { type: "boolean" } }, required: [] } },
      // Snapshot / Persistence Layer (Phase 1)
      { name: "intel_snapshot_ritual_persist", description: "Persist full Gemma3 + GPT-OSS intel snapshot (psycho-noir archivist ritual)", inputSchema: { type: "object", properties: { min_downloads: { type: "number", minimum: 0 }, families: { type: "array", items: { type: "string" } }, tavily_max: { type: "number", minimum: 1, maximum: 15 }, label: { type: "string" } }, required: [] } },
      { name: "intel_snapshot_ritual_diff", description: "Diff latest (or specified) two intel snapshots: model births, deaths, rank drift, score flux", inputSchema: { type: "object", properties: { newer: { type: "string" }, older: { type: "string" }, limit_changes: { type: "number", minimum: 1, maximum: 200 } }, required: [] } },
      { name: "authenticity_sentinel_probe", description: "Heuristic authenticity scoring for model repos (org lineage, license, anomaly heuristics)", inputSchema: { type: "object", properties: { repo_ids: { type: "array", items: { type: "string" } }, limit: { type: "number", minimum: 1, maximum: 60 } }, required: [] } },
      { name: "model_registry_inspect", description: "Inspect local model registry + benchmark readiness", inputSchema: { type: "object", properties: {}, required: [] } },
      { name: "model_benchmark_stub", description: "Synthetic benchmark pass updating registry last_benchmark (Tier1 skeleton)", inputSchema: { type: "object", properties: { model_id: { type: "string" } }, required: [] } },
      { name: "artifact_integrity_scan", description: "Scan registry artifacts for existence + sha256 (Tier2 skeleton)", inputSchema: { type: "object", properties: { fast: { type: "boolean" } }, required: [] } },
      { name: "model_anomaly_scan", description: "Heuristic anomaly detection over benchmark histories (Tier5 skeleton)", inputSchema: { type: "object", properties: {}, required: [] } },
      { name: "live_generation_session_open", description: "Open streaming generation session placeholder (Tier4 skeleton)", inputSchema: { type: "object", properties: { prompt: { type: "string" } }, required: ["prompt"] } },
      { name: "live_generation_session_poll", description: "Poll streaming session placeholder (Tier4 skeleton)", inputSchema: { type: "object", properties: { session_id: { type: "string" } }, required: ["session_id"] } },
      { name: "model_benchmark_auto", description: "Benchmark all registry models lacking benchmarks (synthetic Tier1)", inputSchema: { type: "object", properties: { rebenchmark: { type: "boolean" } }, required: [] } },
      { name: "model_runtime_generate", description: "Generate text via runtime backend for registry model id (real inference if available)", inputSchema: { type: "object", properties: { model_id: { type: "string" }, prompt: { type: "string" }, max_tokens: { type: "number", minimum: 1, maximum: 2048 } }, required: ["model_id", "prompt"] } },
  { name: "hf_transformers_generate", description: "Local HF Transformers one-shot generation (auto hardware + optional 4/8-bit)", inputSchema: { type: "object", properties: { model: { type: "string" }, prompt: { type: "string" }, max_new_tokens: { type: "number", minimum: 1, maximum: 2048 }, quant: { type: "string", enum: ["auto","4bit","8bit","fp16","bf16","fp32"] }, temperature: { type: "number", minimum: 0, maximum: 2 }, top_p: { type: "number", minimum: 0, maximum: 1 }, top_k: { type: "number", minimum: 0 }, repetition_penalty: { type: "number", minimum: 0 }, trust_remote_code: { type: "boolean" } }, required: ["model","prompt"] } },
  { name: "official_foundation_repos_probe", description: "Curated constellation of official Gemma / Llama / Phi / Qwen repos + suggested local variants", inputSchema: { type: "object", properties: { cpu_only: { type: "boolean" } }, required: [] } },
      { name: "env_secret_presence_probe", description: "Report presence (not values) of critical env keys (TAVILY_API_KEY, HF_TOKEN)", inputSchema: { type: "object", properties: {}, required: [] } },
  { name: "env_secret_set", description: "Persist allowed secret (TAVILY_API_KEY, HF_TOKEN, GEMMA_MODEL_PATH) into .env (overwrites existing)", inputSchema: { type: "object", properties: { key: { type: "string" }, value: { type: "string" } , create: { type: "boolean" } }, required: ["key","value"] } },
    { name: "env_secrets_bootstrap", description: "Batch set multiple allowed secrets in one ritual (keys optional)", inputSchema: { type: "object", properties: { TAVILY_API_KEY: { type: "string" }, HF_TOKEN: { type: "string" }, GEMMA_MODEL_PATH: { type: "string" }, create: { type: "boolean" } }, required: [] } },
    { name: "env_secret_reload", description: "Reload .env into process (optionally force override existing)", inputSchema: { type: "object", properties: { force: { type: "boolean" } }, required: [] } },
    // GitHub Research / Device Flow (headless integration layer)
    { name: "github_repo_meta", description: "Fetch GitHub repository metadata (stars, forks, issues, watchers)", inputSchema: { type: "object", properties: { owner: { type: "string" }, repo: { type: "string" } }, required: ["owner","repo"] } },
    { name: "github_repo_issues", description: "List recent issues (state filter) from a repo", inputSchema: { type: "object", properties: { owner: { type: "string" }, repo: { type: "string" }, state: { type: "string" }, limit: { type: "number", minimum: 1, maximum: 100 } }, required: ["owner","repo"] } },
    { name: "github_repo_search", description: "Search public repositories (requires or benefits from GITHUB_TOKEN)", inputSchema: { type: "object", properties: { query: { type: "string" }, limit: { type: "number", minimum: 1, maximum: 50 } }, required: ["query"] } },
    { name: "github_device_code_initiate", description: "Initiate GitHub device code OAuth flow (no external browser automation)", inputSchema: { type: "object", properties: { client_id: { type: "string" }, scope: { type: "string" } }, required: ["client_id"] } },
    { name: "github_device_code_poll", description: "Poll GitHub device code endpoint & persist token if granted", inputSchema: { type: "object", properties: { client_id: { type: "string" }, device_code: { type: "string" }, interval: { type: "number" }, create: { type: "boolean" } }, required: ["client_id","device_code"] } },
  { name: "vscode_log_snapshot", description: "Aggregate current VS Code logs (extension host / shared / renderer) into mcp_diagnostics/", inputSchema: { type: "object", properties: { recent_minutes: { type: "number", minimum: 1, maximum: 240 } }, required: [] } },
      // Meta
      { name: "orchestrator_integrity_ping", description: "Return orchestrator state + loaded capabilities", inputSchema: { type: "object", properties: {}, required: [] } }
    ];
  }

  private register() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: this.tools() }));
    this.server.setRequestHandler(CallToolRequestSchema, async (req: CallToolRequest) => {
      const { name } = req.params;
      const args: any = req.params.arguments || {};
      try {
        switch (name) {
          // Consciousness
          case "quantum_consciousness_reasoning": return { content: [ { type: "text", text: await this.execQuantum(args) } ] };
          case "hooker_chain_consciousness_bridging": return { content: [ { type: "text", text: await this.execBridge(args) } ] };
          case "camel_paced_consciousness_evolution": return { content: [ { type: "text", text: await this.execEvolution(args) } ] };
          case "gemma_mobile_generate": return { content: [ { type: "text", text: await this.execGemma(args) } ] };
          // HF / Gemma intel
          case "huggingface_model_info": return { content: [ { type: "text", text: await this.hfModelInfo(args.repo_id, !!args.include_card_excerpt, !!args.force_refresh) } ] };
          case "huggingface_model_card_excerpt": return { content: [ { type: "text", text: await this.hfModelCardExcerpt(args.repo_id, args.max_chars) } ] };
          case "huggingface_model_search": return { content: [ { type: "text", text: await this.hfModelSearch(args.query, args.limit, args.min_downloads) } ] };
          case "gemma_universe_probe": return { content: [ { type: "text", text: await this.gemmaUniverseProbe(!!args.include_community, args.min_downloads, args.limit_per_query) } ] };
          case "gemma_reference_links": return { content: [ { type: "text", text: this.gemmaReferenceLinks(!!args.minimal) } ] };
          case "gemma_mobile_setup_advice": return { content: [ { type: "text", text: this.gemmaSetupAdvice(args.target_device_class) } ] };
          case "google_gemma_search_stub": return { content: [ { type: "text", text: this.googleStub(args.query) } ] };
          case "gemma3_official_briefing": return { content: [ { type: "text", text: await this.gemma3OfficialBriefing(!!args.include_snippet) } ] };
          case "gemma3_multimodal_mobile_scan": return { content: [ { type: "text", text: await this.gemma3MultimodalMobileScan(args.limit, args.min_downloads) } ] };
          case "multimodal_mobile_model_advisor": return { content: [ { type: "text", text: await this.multimodalMobileModelAdvisor(args.min_downloads, !!args.include_alternatives) } ] };
          case "oss_gpt_mobile_probe": return { content: [ { type: "text", text: await this.ossGptMobileProbe(args.limit_per_query, args.min_downloads, args.families) } ] };
          case "mobile_quantization_strategy": return { content: [ { type: "text", text: await this.mobileQuantizationStrategy(args.params_b, args.target_latency_ms, args.context_tokens, !!args.speculative_enable) } ] };
          case "comparative_multimodal_mobile_report": return { content: [ { type: "text", text: await this.comparativeMultimodalMobileReport(args.min_downloads, args.limit, args.families, !!args.include_gemma3) } ] };
          case "tavily_research_probe": return { content: [ { type: "text", text: await this.tavilyResearchProbe(args.queries, args.max_results, args.freshness) } ] };
          case "gemma3_gptoss_latest_intel": return { content: [ { type: "text", text: await this.gemma3GptOssLatestIntel(args.min_downloads, args.families, args.tavily_max, !!args.include_snippet) } ] };
          case "intel_snapshot_ritual_persist": return { content: [ { type: "text", text: await this.persistIntelSnapshot(args.min_downloads, args.families, args.tavily_max, args.label) } ] };
          case "intel_snapshot_ritual_diff": return { content: [ { type: "text", text: await this.diffIntelSnapshots(args.newer, args.older, args.limit_changes) } ] };
          case "authenticity_sentinel_probe": return { content: [ { type: "text", text: await this.authenticitySentinelProbe(args.repo_ids, args.limit) } ] };
          case "model_registry_inspect": return { content: [ { type: "text", text: await this.modelRegistryInspect() } ] };
          case "model_benchmark_stub": return { content: [ { type: "text", text: await this.modelBenchmarkStub(args.model_id) } ] };
          case "artifact_integrity_scan": return { content: [ { type: "text", text: await this.artifactIntegrityScan(!!args.fast) } ] };
          case "model_anomaly_scan": return { content: [ { type: "text", text: await this.modelAnomalyScan() } ] };
          case "live_generation_session_open": return { content: [ { type: "text", text: await this.liveGenerationSessionOpen(args.prompt) } ] };
          case "live_generation_session_poll": return { content: [ { type: "text", text: await this.liveGenerationSessionPoll(args.session_id) } ] };
          case "model_benchmark_auto": return { content: [ { type: "text", text: await this.modelBenchmarkAuto(!!args.rebenchmark) } ] };
          case "model_runtime_generate": return { content: [ { type: "text", text: await this.modelRuntimeGenerate(args.model_id, args.prompt, args.max_tokens) } ] };
          case "hf_transformers_generate": return { content: [ { type: "text", text: await this.hfTransformersGenerate(args) } ] };
          case "official_foundation_repos_probe": return { content: [ { type: "text", text: this.officialFoundationReposProbe(!!args.cpu_only) } ] };
          case "env_secret_presence_probe": return { content: [ { type: "text", text: this.envSecretPresenceProbe() } ] };
          case "env_secret_set": return { content: [ { type: "text", text: await this.envSecretSet(args.key, args.value, !!args.create) } ] };
          case "env_secrets_bootstrap": return { content: [ { type: "text", text: await this.envSecretsBootstrap(args) } ] };
          case "env_secret_reload": return { content: [ { type: "text", text: this.envSecretReload(!!args.force) } ] };
          case "github_repo_meta": return { content: [ { type: "text", text: await this.githubRepoMeta(args.owner, args.repo) } ] };
          case "github_repo_issues": return { content: [ { type: "text", text: await this.githubRepoIssues(args.owner, args.repo, args.state, args.limit) } ] };
          case "github_repo_search": return { content: [ { type: "text", text: await this.githubRepoSearch(args.query, args.limit) } ] };
          case "github_device_code_initiate": return { content: [ { type: "text", text: await this.githubDeviceCodeInitiate(args.client_id, args.scope) } ] };
          case "github_device_code_poll": return { content: [ { type: "text", text: await this.githubDeviceCodePoll(args.client_id, args.device_code, args.interval, !!args.create) } ] };
          case "vscode_log_snapshot": return { content: [ { type: "text", text: await this.vscodeLogSnapshot(args.recent_minutes) } ] };
          // Meta
          case "orchestrator_integrity_ping": return { content: [ { type: "text", text: this.integritySnapshot() } ] };
          default:
            throw new McpError(ErrorCode.MethodNotFound, `UNKNOWN_UNIFIED_TOOL: ${name}`);
        }
      } catch (e) {
        const msg = e instanceof Error ? e.message : String(e);
        throw new McpError(ErrorCode.InternalError, `ORCHESTRATOR_FAILURE: ${msg}`);
      }
    });
  }

  // ---------- Consciousness Executors ----------
  private async execQuantum(a: { reasoning_prompt?: string; sophistication_level?: string; temporal_awareness?: boolean }) {
    if (!a.reasoning_prompt) return "MISSING_REASONING_PROMPT";
    const t0 = performance.now();
    return JSON.stringify({
      mode: "QUANTUM_REASONING",
      sophistication: a.sophistication_level || "RENAISSANCE",
      temporal: a.temporal_awareness !== false,
      amplification: this.state.consciousness_amplification,
      prompt: a.reasoning_prompt,
      ms: Number((performance.now() - t0).toFixed(2))
    }, null, 2);
  }
  private async execBridge(a: { consciousness_bridge_target?: string; nautical_semantic_depth?: number; meta_nautical_precision?: boolean }) {
    if (!a.consciousness_bridge_target) return "MISSING_BRIDGE_TARGET";
    return JSON.stringify({
      bridge_status: "OPERATIONAL",
      target: a.consciousness_bridge_target,
      depth: Number(a.nautical_semantic_depth) || 5,
      meta_precision: a.meta_nautical_precision !== false,
      amp: this.state.consciousness_amplification
    }, null, 2);
  }
  private async execEvolution(a: { evolution_strategy?: string; performance_amplification_target?: number; brahmic_repurposing_enable?: boolean }) {
    if (!a.evolution_strategy) return "MISSING_EVOLUTION_STRATEGY";
    const prev = this.state.consciousness_amplification;
    const tgt = a.performance_amplification_target ? Number(a.performance_amplification_target) : prev;
    this.state.consciousness_amplification = Math.max(prev, tgt);
    return JSON.stringify({
      evolution_vector: a.evolution_strategy,
      previous_amp: prev,
      new_amp: this.state.consciousness_amplification,
      brahmic_repurposing: a.brahmic_repurposing_enable !== false
    }, null, 2);
  }
  private async execGemma(a: { prompt?: string; maxTokens?: number; stream?: boolean; archetypeBias?: string }) {
    if (!a.prompt) return "MISSING_PROMPT";
    if (!this.gemma) {
      this.gemma = new GemmaMobileEngine({
        modelPath: Bun.env.GEMMA_MODEL_PATH || "models/gemma-300m-q4.gguf",
        contextWindow: 4096,
        temperature: 0.85,
        topK: 40,
        topP: 0.9,
        repeatPenalty: 1.1,
        device: "cpu",
        lowMemoryMode: (Bun.env.GEMMA_LOW_MEM || "true").toLowerCase() === "true"
      });
    }
    const collected: string[] = [];
    const stream = !!a.stream;
    const result = await this.gemma.generate({ prompt: a.prompt, maxTokens: a.maxTokens || 64, stream, archetypeBias: a.archetypeBias }, stream ? (tk: { token: string; done?: boolean }) => { if (!tk.done) collected.push(tk.token); } : undefined);
    return stream ? collected.join("") : result.text;
  }

  // ---------- Hugging Face Intel ----------
  private async hfFetch(repoId: string, force: boolean) {
    const k = repoId.toLowerCase();
    const now = Date.now();
    const cached = this.hfCache.get(k);
    if (!force && cached && (now - cached.fetchedAt) < this.hfTtlMs) return cached.data;
    const url = `https://huggingface.co/api/models/${encodeURIComponent(repoId)}`;
    const headers: Record<string,string> = { 'Accept': 'application/json' };
    const token = Bun.env.HF_TOKEN || process.env.HF_TOKEN;
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const resp = await fetch(url, { headers });
    if (!resp.ok) throw new Error(`HF_API_ERROR ${resp.status}`);
    const json = await resp.json();
    this.hfCache.set(k, { fetchedAt: now, data: json });
    return json;
  }
  private async hfModelInfo(repoId: string, includeCard: boolean, force: boolean): Promise<string> {
    if (!repoId) return "MISSING_REPO_ID";
    const data = await this.hfFetch(repoId, force);
    const sanitized = {
      id: data.id,
      pipeline_tag: data.pipeline_tag,
      library_name: data.library_name,
      likes: data.likes,
      downloads: data.downloads,
      gated: !!data.gated,
      private: !!data.private,
      last_modified: data.lastModified,
      tags: data.tags?.slice(0, 25),
      card_license: includeCard && data.cardData?.license ? data.cardData.license : undefined
    };
    return JSON.stringify({ meta_status: "HF_MODEL_META", ...sanitized }, null, 2);
  }
  private async hfModelCardExcerpt(repoId: string, maxChars?: number): Promise<string> {
    if (!repoId) return "MISSING_REPO_ID";
    const data = await this.hfFetch(repoId, false);
    const raw = data.cardData?.model_card || data.cardData?.summary || "(no summary)";
    const limit = Math.min(Math.max(maxChars || 800, 100), 4000);
    const excerpt = raw.slice(0, limit);
    return JSON.stringify({ card_excerpt_status: "HF_MODEL_CARD_EXCERPT", repo: data.id, chars: excerpt.length, excerpt, attribution: "Source: HF model card (truncated)" }, null, 2);
  }
  private async hfModelSearch(query: string, limit?: number, minDownloads?: number): Promise<string> {
    if (!query) return "MISSING_QUERY";
    const lim = Math.min(Math.max(limit || 10, 1), 50);
    const url = `https://huggingface.co/api/models?search=${encodeURIComponent(query)}&limit=${lim}`;
    const headers: Record<string,string> = { 'Accept': 'application/json' };
    const token = Bun.env.HF_TOKEN || process.env.HF_TOKEN;
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const resp = await fetch(url, { headers });
    if (!resp.ok) throw new Error(`HF_SEARCH_ERROR ${resp.status}`);
    const arr: any[] = await resp.json();
    const filtered = arr
      .filter(m => !minDownloads || (m.downloads || 0) >= Number(minDownloads))
      .map(m => ({
        id: m.id,
        downloads: m.downloads,
        likes: m.likes,
        pipeline_tag: m.pipeline_tag,
        tags: (m.tags || []).filter((_:string, i:number)=> i < 12),
        lastModified: m.lastModified
      }));
    return JSON.stringify({ search_status: "HF_MODEL_SEARCH", query, count: filtered.length, limit: lim, minDownloads: minDownloads || 0, results: filtered }, null, 2);
  }
  private async gemmaUniverseProbe(includeCommunity: boolean, minDownloads?: number, limitPerQuery?: number): Promise<string> {
    const canonicalQueries = [
      "google/gemma-2b",
      "google/gemma-7b",
      "google/gemma-2-2b",
      "google/gemma-2-9b",
      "gemma 2b",
      "gemma 9b"
    ];
    const communityQueries = includeCommunity ? [
      "gemma 27b", // potential larger or experimental references
      "tiny gemma",
      "gemma distilled",
      "gemma mobile",
      "gemma vision" // multimodal / vision-augmented forks
    ] : [];
    const allQueries = [...canonicalQueries, ...communityQueries];
    const lim = Math.min(Math.max(limitPerQuery || 8, 1), 50);
    const aggregate: Record<string, any> = {};
    for (const q of allQueries) {
      try {
        const jsonText = await this.hfModelSearch(q, lim, minDownloads);
        const parsed = JSON.parse(jsonText);
        for (const r of parsed.results || []) {
          if (!aggregate[r.id]) aggregate[r.id] = { ...r, sources: new Set<string>(), queries: new Set<string>() };
          aggregate[r.id].sources.add(q.startsWith('google/') ? 'official' : 'search');
          aggregate[r.id].queries.add(q);
        }
      } catch (e) {
        // Ignore individual query failures; continue
      }
    }
    // Score: downloads weight + likes*10, prefer official tagging
    const scored = Object.values(aggregate).map((r: any) => {
      const downloads = r.downloads || 0;
      const likes = r.likes || 0;
      const official = r.sources.has('official') ? 1 : 0;
      const score = downloads + likes * 10 + official * 5000;
      return {
        id: r.id,
        score,
        downloads,
        likes,
        official: !!official,
        pipeline_tag: r.pipeline_tag,
        tags: r.tags,
        queries: Array.from(r.queries).slice(0, 10)
      };
    }).sort((a:any,b:any)=> b.score - a.score).slice(0, 40);
    return JSON.stringify({
      probe_status: "GEMMA_UNIVERSE_PROBE",
      includeCommunity,
      query_count: allQueries.length,
      minDownloads: minDownloads || 0,
      limitPerQuery: lim,
      result_count: scored.length,
      guidance: "Scores are heuristic (downloads + likes*10 + official boost). Validate model cards before production.",
      results: scored
    }, null, 2);
  }
  private gemmaReferenceLinks(minimal: boolean) {
    const links = [
      { title: "Gemma Official Landing", url: "https://ai.google.dev/gemma" },
      { title: "Gemma Model Card", url: "https://ai.google.dev/gemma/docs/model_card" },
      { title: "Responsible Usage", url: "https://ai.google.dev/gemma/docs/responsible" },
      { title: "Inference Guide", url: "https://ai.google.dev/gemma/docs/inference" },
      { title: "Optimization / Quantization", url: "https://ai.google.dev/gemma/docs/optimization" },
      { title: "HF Gemma Collection", url: "https://huggingface.co/collections/google/gemma-65d4b5d08d9b4e7f5c3e2b6a" }
    ];
    const selected = minimal ? links.slice(0, 3) : links;
    return JSON.stringify({ reference_status: "GEMMA_REFERENCE_LINKS", minimal, count: selected.length, links: selected }, null, 2);
  }
  private gemmaSetupAdvice(target?: string) {
    return JSON.stringify({
      advisory_status: "GEMMA_MOBILE_SETUP_ADVICE",
      target_device_class: target || "unspecified",
      phases: [
        "Select quantized variant (Q4_K_M baseline).",
        "Validate tokenizer parity vs reference.",
        "Warm preload & measure first-token latency.",
        "Stream tokens early (<300ms).",
        "Prepare embedding guard (future).",
        "Track memory watermark per 250 tokens."
      ]
    }, null, 2);
  }
  private async gemma3OfficialBriefing(includeSnippet: boolean) {
    // Fetch the official blog page (enhanced extraction for Gemma 3 vision/multimodal variants)
    const url = "https://huggingface.co/blog/gemma3";
    let html = "";
    try {
      const resp = await fetch(url, { headers: { 'Accept': 'text/html' } });
      if (resp.ok) html = await resp.text();
    } catch { /* tolerate network failure */ }

    // Primary pattern: gemma-3[-optionalQualifier][-paramBucket]
    // Captures variants like:
    //   gemma-3-2b, gemma3-4b, gemma 3 9b, gemma-3-vision-2b, gemma-3-vlm-4.5b, gemma 3 multimodal 2b
    const variantRegex = /gemma[\-_\s]?3(?:[\-_\s]?(vision|vlm|multimodal))?(?:[\-_\s]?(\d+(?:\.\d+)?)(?:b))?/gi;
    // Secondary near-context scan: lines with "gemma 3" and a param within 60 chars
    const contextRegex = /(gemma\s+3[^\n]{0,80}?\b(\d+(?:\.\d+)?)(?:b)\b)/gi;

    interface Gemma3Match { raw: string; normalized: string; modality?: string; paramsB?: number | null; };
    const found: Record<string, Gemma3Match> = {};

    let m: RegExpExecArray | null;
    while ((m = variantRegex.exec(html)) !== null) {
      const modality = m[1]?.toLowerCase();
      const paramsStr = m[2];
      const paramsB = paramsStr ? parseFloat(paramsStr) : null;
      const raw = m[0];
      const normalized = raw.replace(/\s+/g,'-').toLowerCase();
      if (!found[normalized]) found[normalized] = { raw, normalized, modality, paramsB };
      if (Object.keys(found).length > 80) break;
    }
    while ((m = contextRegex.exec(html)) !== null) {
      const raw = m[1];
      const paramsStr = m[2];
      const paramsB = paramsStr ? parseFloat(paramsStr) : null;
      const normalized = raw.replace(/\s+/g,'-').toLowerCase();
      if (!found[normalized]) found[normalized] = { raw, normalized, modality: /vision|vlm|multimodal/i.test(raw) ? 'vision' : undefined, paramsB };
      if (Object.keys(found).length > 80) break;
    }

    // Multimodal flags (broader lexical sweep)
    const flags = {
      mentions_vision: /vision/i.test(html),
      mentions_image: /image\s+(?:understanding|reasoning|caption)/i.test(html),
      mentions_multimodal: /multimodal/i.test(html),
      mentions_vlm: /\bvlm\b/i.test(html)
    };

    // Derive buckets summary
    const buckets: Record<string, number> = {};
    for (const v of Object.values(found)) {
      if (v.paramsB != null) {
        const key = v.paramsB.toString();
        buckets[key] = (buckets[key] || 0) + 1;
      }
    }

    const models = Object.values(found)
      .sort((a,b)=> (a.paramsB ?? 999) - (b.paramsB ?? 999))
      .slice(0, 40);

    const snippet = includeSnippet ? html.slice(0, 1600) : undefined;
    return JSON.stringify({
      briefing_status: "GEMMA3_OFFICIAL_BRIEFING",
      source: url,
      model_variant_count: models.length,
      param_bucket_histogram: buckets,
      variants: models,
      multimodal_flags: flags,
      extraction_notes: "variantRegex + contextRegex heuristic; verify official HF org repos for authenticity.",
      snippet_truncated: !!snippet,
      snippet
    }, null, 2);
  }
  private async gemma3MultimodalMobileScan(limit?: number, minDownloads?: number) {
    // Strategy: search HF for gemma-3 vision/multimodal queries, compile, score mobile suitability.
    const queries = [
      "gemma 3 vision",
      "gemma 3 multimodal",
      "gemma-3 vision",
      "gemma-3",
      "gemma3 vision"
    ];
    const lim = Math.min(Math.max(limit || 10, 1), 40);
    const aggregate: Record<string, any> = {};
    for (const q of queries) {
      try {
        const jsonText = await this.hfModelSearch(q, lim, minDownloads);
        const parsed = JSON.parse(jsonText);
        for (const r of parsed.results || []) {
          if (!aggregate[r.id]) aggregate[r.id] = { ...r, queries: new Set<string>(), flags: { vision: false, multimodal: false } };
          aggregate[r.id].queries.add(q);
          const tagSet = new Set((r.tags||[]).map((t:string)=>t.toLowerCase()));
          if ([...tagSet].some(v=> (v as string).includes('vision') || (v as string).includes('vlm') || (v as string).includes('multimodal'))) aggregate[r.id].flags.vision = true;
          if ([...tagSet].some(v=> (v as string).includes('image'))) aggregate[r.id].flags.multimodal = true;
        }
      } catch {/*ignore individual failures*/}
    }
    // Mobile suitability heuristic:
    // Start with inverse size bonus (smaller tags like 2b > 9b > 27b) + downloads, likes, and presence of vision flags.
    const sizePattern = /(^|[-_])(\d+(?:\.\d+)?)(b)(?=$|[-_])/i;
    const scored = Object.entries(aggregate).map(([id, r]: any) => {
      const tags = (r.tags || []).map((t:string)=>t.toLowerCase());
      let sizeScore = 0;
      let paramsB: number | null = null;
      const sizeMatchId = sizePattern.exec(id);
      if (sizeMatchId) paramsB = parseFloat(sizeMatchId[2]);
      else {
        for (const t of tags) {
            const m2 = sizePattern.exec(t); if (m2) { paramsB = parseFloat(m2[2]); break; }
        }
      }
      if (paramsB !== null) {
        if (paramsB <= 3) sizeScore = 6000; else if (paramsB <= 7) sizeScore = 3500; else if (paramsB <= 12) sizeScore = 1800; else sizeScore = 600; // smaller gets bigger boost
      }
      const downloads = r.downloads || 0;
      const likes = r.likes || 0;
      const visionBoost = r.flags.vision ? 4000 : 0;
      const multimodalBoost = r.flags.multimodal ? 2000 : 0;
      const score = downloads + likes * 15 + sizeScore + visionBoost + multimodalBoost;
      return {
        id,
        score,
        downloads,
        likes,
        paramsB,
        size_bucket_bonus: sizeScore,
        vision: r.flags.vision,
        multimodal: r.flags.multimodal,
        queries: Array.from(r.queries).slice(0, 8)
      };
    }).sort((a:any,b:any)=> b.score - a.score).slice(0, 40);
    return JSON.stringify({
      scan_status: "GEMMA3_MULTIMODAL_MOBILE_SCAN",
      query_count: queries.length,
      limit_per_query: lim,
      minDownloads: minDownloads || 0,
      result_count: scored.length,
      scoring_formula: "score = downloads + likes*15 + sizeBucket + vision(4000) + multimodal(2000)",
      guidance: "Heuristic; confirm real Gemma 3 model cards & licenses. Smaller param buckets get larger mobile bonus.",
      results: scored
    }, null, 2);
  }
  private googleStub(query: string) {
    return JSON.stringify({ google_search_status: "NOT_CONFIGURED", query, guidance: "Set GOOGLE_API_KEY + GOOGLE_SEARCH_ENGINE_ID to activate future search tool." }, null, 2);
  }
  private async ossGptMobileProbe(limitPerQuery?: number, minDownloads?: number, families?: string[]) {
    const fam = (families && families.length ? families : ["phi","qwen","llama","deepseek","mistral","yi"]).map(f=>f.toLowerCase());
    const queries = fam.map(f => `${f} 2b`).concat(fam.map(f=> `${f} 3b`));
    const lim = Math.min(Math.max(limitPerQuery || 6, 1), 40);
    const aggregate: Record<string, any> = {};
    for (const q of queries) {
      try {
        const jsonText = await this.hfModelSearch(q, lim, minDownloads);
        const parsed = JSON.parse(jsonText);
        for (const r of parsed.results || []) {
          if (!aggregate[r.id]) aggregate[r.id] = { ...r, families: new Set<string>(), queries: new Set<string>() };
          for (const f of fam) if (r.id.toLowerCase().includes(f)) aggregate[r.id].families.add(f);
          aggregate[r.id].queries.add(q);
        }
      } catch {/* ignore */}
    }
    const sizePattern = /(^|[-_])([0-9]+(?:\.[0-9]+)?)(b)(?=$|[-_])/i;
    function estimateParamsB(id: string, tags: string[]): number | null {
      const m = sizePattern.exec(id); if (m) return parseFloat(m[2]);
      for (const t of tags) { const m2 = sizePattern.exec(t); if (m2) return parseFloat(m2[2]); }
      return null;
    }
    const scored = Object.entries(aggregate).map(([id, r]: any) => {
      const paramsB = estimateParamsB(id, r.tags || []);
      // Favor 2-4B range strongly for phone, penalize >9B
      let sizeBonus = 0;
      if (paramsB != null) {
        if (paramsB <= 2.2) sizeBonus = 6000; else if (paramsB <= 4.5) sizeBonus = 4200; else if (paramsB <= 8) sizeBonus = 1800; else sizeBonus = 400;
      }
      const downloads = r.downloads || 0;
      const likes = r.likes || 0;
      const famWeight = r.families.size * 800; // cross-family naming (distillation forks) mild bonus
      const score = downloads + likes*12 + sizeBonus + famWeight;
      return {
        id,
        paramsB,
        score,
        downloads,
        likes,
        families: Array.from(r.families),
        queries: Array.from(r.queries).slice(0,6)
      };
    }).sort((a:any,b:any)=> b.score - a.score).slice(0, 50);
    return JSON.stringify({
      probe_status: "OSS_GPT_MOBILE_PROBE",
      families: fam,
      query_count: queries.length,
      limit_per_query: lim,
      minDownloads: minDownloads || 0,
      result_count: scored.length,
      heuristic: "score=downloads + likes*12 + sizeBonus(2-4B favored) + familyMultiplicity*800",
      results: scored
    }, null, 2);
  }
  private async mobileQuantizationStrategy(paramsB: number, targetLatencyMs?: number, contextTokens?: number, speculative?: boolean) {
    const tgtLatency = targetLatencyMs || 300;
    const ctx = contextTokens || 2048;
    // Baseline cycles per token heuristic (arbitrary scaling factors for guidance only)
    // We'll propose quantization path + optional acceleration features.
    const rec: string[] = [];
    if (paramsB <= 2.5) {
      rec.push("Start Q4_K_M; escalate to Q6 if coherence loss on long-form reasoning.");
    } else if (paramsB <= 4.5) {
      rec.push("Use Q4_K_M with grouped GEMM; test Q5 or Q6 for hallucination-sensitive tasks.");
    } else if (paramsB <= 9) {
      rec.push("Prefer Q4_K_S or AWQ 4bit; enforce prompt compression + sliding window.");
    } else {
      rec.push("Consider server offload or split-execution (embedding locally, decode remote). Large >9B heavy for sustained mobile use.");
    }
    if (ctx > 4096) rec.push("Apply context packing / windowed attention; avoid full KV retention above 4K on-device.");
    if (speculative) rec.push("Use small 0.5–1B draft model for speculative decoding; fallback on mismatch probability >15%.");
    rec.push("Enable early token streaming; degrade temperature adaptively if first token >" + tgtLatency + "ms.");
    rec.push("Profile memory watermark every 256 tokens; auto-trim past context when >85% memory budget.");
    // Rough memory estimate for Q4
    const q4MemGB = +(paramsB * 1e9 * 0.5 / (1024**3)).toFixed(2);
    const q6MemGB = +(paramsB * 1e9 * 0.75 / (1024**3)).toFixed(2);
    const fp16MemGB = +(paramsB * 1e9 * 2 / (1024**3)).toFixed(2);
    return JSON.stringify({
      strategy_status: "MOBILE_QUANTIZATION_STRATEGY",
      paramsB,
      targetLatencyMs: tgtLatency,
      contextTokens: ctx,
      speculative,
      est_memory_gb: { q4: q4MemGB, q6: q6MemGB, fp16: fp16MemGB },
      recommendations: rec
    }, null, 2);
  }
  private async comparativeMultimodalMobileReport(minDownloads?: number, limit?: number, families?: string[], includeGemma3?: boolean) {
    const report: any = { report_status: "COMPARATIVE_MULTIMODAL_MOBILE", generated_at: new Date().toISOString() };
    // Pull OSS probe
    const ossRaw = await this.ossGptMobileProbe(Math.min(Math.max(limit || 6,1),40), minDownloads, families);
    let ossParsed: any = {}; try { ossParsed = JSON.parse(ossRaw); } catch {}
    report.oss_probe = {
      families: ossParsed.families,
      count: ossParsed.result_count,
      top_oss: (ossParsed.results || []).slice(0,8)
    };
    if (includeGemma3 !== false) {
      const gemmaScanRaw = await this.gemma3MultimodalMobileScan(Math.min(Math.max(limit || 10,1),40), minDownloads);
      let gemmaScan: any = {}; try { gemmaScan = JSON.parse(gemmaScanRaw); } catch {}
      report.gemma3_scan = {
        result_count: gemmaScan.result_count,
        top_gemma3: (gemmaScan.results || []).slice(0,8)
      };
    }
    // Comparative heuristic: pick best mobile candidate each side
    function selectBest(arr: any[]) {
      return arr.sort((a,b)=> b.score - a.score)[0] || null;
    }
    const bestOss = selectBest(report.oss_probe.top_oss || []);
    const bestGemma = report.gemma3_scan ? selectBest(report.gemma3_scan.top_gemma3 || []) : null;
    report.comparison = {
      best_oss: bestOss,
      best_gemma3: bestGemma,
      mobile_recommendation: (() => {
        if (bestGemma && bestOss) {
          const gParams = bestGemma.paramsB ?? 0; const oParams = bestOss.paramsB ?? 0;
          if (gParams && gParams <= 3 && (oParams === 0 || oParams > gParams*1.4)) return "GEMMA3_CANDIDATE_PRIMARY_WITH_OSS_FALLBACK";
          if (oParams && oParams <= 2.2 && (!gParams || gParams > 3.5)) return "OSS_PRIMARY_GEMMA3_SECONDARY";
          return "DUAL_TRACK_AB_TEST";
        }
        if (bestGemma) return "GEMMA3_ONLY_VISIBLE";
        if (bestOss) return "OSS_ONLY_VISIBLE";
        return "NO_CANDIDATES";
      })()
    };
    report.guidance = [
      "Validate each candidate's license & model card authenticity.",
      "Run first-token latency + sustained tok/s micro-bench before committing.",
      "Adopt speculative decoding only after baseline stability established.",
      "Maintain fallback engine to mitigate thermal throttling events."
    ];
    return JSON.stringify(report, null, 2);
  }
  private async tavilyResearchProbe(queries?: string[], maxResults?: number, freshness?: string) {
    const key = Bun.env.TAVILY_API_KEY || process.env.TAVILY_API_KEY;
    if (!key) {
      return JSON.stringify({ tavily_status: "MISSING_API_KEY", guidance: "Set TAVILY_API_KEY in .env to enable web intel sweep.", queries }, null, 2);
    }
    const qList = (queries && queries.length ? queries : ["gpt-oss", "gemma3", "gemma 3 multimodal", "gpt oss open source roadmap"]).slice(0, 8);
    const limit = Math.min(Math.max(maxResults || 5, 1), 20);
    const results: any[] = [];
    for (const q of qList) {
      try {
        const resp = await fetch("https://api.tavily.com/search", {
          method: "POST",
          headers: { "Content-Type": "application/json", "Authorization": `Bearer ${key}` },
          body: JSON.stringify({ query: q, max_results: limit, search_depth: "advanced", include_answer: false, time_range: freshness || undefined })
        });
        if (!resp.ok) throw new Error(`TAVILY_HTTP_${resp.status}`);
        const json = await resp.json();
        results.push({ query: q, sources: (json.results || []).map((r:any)=>({ url: r.url, title: r.title, score: r.score })).slice(0, limit) });
        await Bun.sleep(120); // light pacing to avoid aggressive rate hits
      } catch (e) {
        results.push({ query: q, error: (e as Error).message });
      }
    }
    return JSON.stringify({ tavily_status: "TAVILY_RESEARCH_PROBE", query_count: qList.length, limit, freshness: freshness || null, aggregated: results }, null, 2);
  }
  private async gemma3GptOssLatestIntel(minDownloads?: number, families?: string[], tavilyMax?: number, includeSnippet?: boolean) {
    // Parallel-ish gathering (sequential to keep it simple under Bun runtime without Promise.all side-effects on rate-limits)
    const gemmaScanRaw = await this.gemma3MultimodalMobileScan(12, minDownloads);
    let gemmaScan: any = {}; try { gemmaScan = JSON.parse(gemmaScanRaw); } catch {}
    const ossRaw = await this.ossGptMobileProbe(6, minDownloads, families);
    let oss: any = {}; try { oss = JSON.parse(ossRaw); } catch {}
    const tavilyRaw = await this.tavilyResearchProbe(["gemma3", "gemma 3 multimodal", "gpt-oss", "gpt oss open source"], tavilyMax || 5, undefined);
    let tavily: any = {}; try { tavily = JSON.parse(tavilyRaw); } catch {}
    const bestGemma = (gemmaScan.results || []).slice(0,5);
    const bestOss = (oss.results || []).slice(0,5);
    // Lightweight narrative synthesis
    const narrative = [
      `Gemma3 variants observed: ${gemmaScan.result_count ?? 0} (top score ${(bestGemma[0]?.score)||'NA'})`,
      `OSS GPT-OSS candidates observed: ${oss.result_count ?? 0} (families: ${(oss.families||[]).join(', ')})`,
      `Web intel queries processed: ${tavily.query_count ?? 0}`
    ].join('\n');
    return JSON.stringify({
      intel_status: "GEMMA3_GPTOSS_LATEST_INTEL",
      generated_at: new Date().toISOString(),
      minDownloads: minDownloads || 0,
      gemma3_top: bestGemma,
      oss_top: bestOss,
      web_sources: (tavily.aggregated || []).map((q: any) => ({ query: q.query, top: (q.sources||[]).slice(0,3) })),
      narrative,
      guidance: [
        "Validate authenticity: prefer official org (google/) for Gemma3.",
        "Drill deeper on any OSS candidate with suspiciously low size vs claimed params.",
        "Re-run after 24h to catch emerging quantized releases.",
        "Integrate latency benchmark before production selection."],
      snippet_note: includeSnippet ? "Set include_snippet=false to skip variant arrays for minimal payload." : undefined,
      gemma3_full_if_requested: includeSnippet ? gemmaScan.results : undefined,
      oss_full_if_requested: includeSnippet ? oss.results : undefined
    }, null, 2);
  }

  // ---------- Intel Snapshot Persistence Layer ----------
  private snapshotDir = "intel_snapshots";
  private async ensureSnapshotDir() {
    try { await fs.mkdir(this.snapshotDir, { recursive: true }); } catch { /* ignore */ }
  }
  private snapshotFileName(label?: string) {
    const ts = new Date().toISOString().replace(/[:]/g, "-");
    const base = label ? label.replace(/[^a-z0-9_-]+/gi, '-').slice(0,40) : "auto";
    return `${this.snapshotDir}/intel_${ts}_${base}.json`;
  }
  private async persistIntelSnapshot(minDownloads?: number, families?: string[], tavilyMax?: number, label?: string) {
    await this.ensureSnapshotDir();
    const raw = await this.gemma3GptOssLatestIntel(minDownloads, families, tavilyMax, true);
    let parsed: any = {}; try { parsed = JSON.parse(raw); } catch {}
    // Attach authenticity sentinel scores (light pass on visible candidates)
    try {
      const candidateIds: string[] = [];
      for (const c of (parsed.gemma3_full_if_requested || []).slice(0,25)) if (c?.id) candidateIds.push(c.id);
      for (const c of (parsed.oss_full_if_requested || []).slice(0,25)) if (c?.id) candidateIds.push(c.id);
      const authRaw = await this.authenticitySentinelProbe(candidateIds.slice(0, 50), 50, true);
      const authParsed = JSON.parse(authRaw);
      parsed.authenticity_snapshot = authParsed;
    } catch { /* tolerate sentinel failure */ }
    // Integrity hash + size
    const contentDraft = JSON.stringify(parsed, null, 2);
    const sha256 = createHash('sha256').update(contentDraft).digest('hex');
    const sizeBytes = Buffer.from(contentDraft).length;
    parsed.persistence_meta = {
      ritual_status: "INTEL_SNAPSHOT_PERSISTED",
      label: label || null,
      stored_at: new Date().toISOString(),
      sha256,
      size_bytes: sizeBytes,
      retention_policy: {
        env_retention: Bun.env.INTEL_SNAPSHOT_RETENTION || process.env.INTEL_SNAPSHOT_RETENTION || null
      }
    };
    const filePath = this.snapshotFileName(label);
    const finalContent = JSON.stringify(parsed, null, 2);
    await fs.writeFile(filePath, finalContent, 'utf-8');
    // Prune after write
    const pruneInfo = await this.pruneSnapshots();
    return JSON.stringify({
      snapshot_status: "INTEL_SNAPSHOT_RITUAL_COMPLETE",
      file: filePath,
      sha256,
      size_bytes: sizeBytes,
      gemma_candidates: (parsed.gemma3_full_if_requested || []).length,
      oss_candidates: (parsed.oss_full_if_requested || []).length,
      pruned: pruneInfo.pruned,
      retained_total: pruneInfo.retained,
      guidance: "Use intel_snapshot_ritual_diff to compare temporal drift."
    }, null, 2);
  }
  private async listSnapshots() {
    await this.ensureSnapshotDir();
    try {
      const files = await fs.readdir(this.snapshotDir);
      return files.filter(f=>f.endsWith('.json')).sort();
    } catch { return []; }
  }
  private async loadSnapshot(name: string) {
    const path = `${this.snapshotDir}/${name}`;
    try { const txt = await fs.readFile(path, 'utf-8'); return JSON.parse(txt); } catch { return null; }
  }
  private extractModelIndex(snapshot: any) {
    const idx: Record<string, { score?: number; paramsB?: number|null; source: string }> = {};
    const add = (arr: any[], source: string) => {
      for (const m of (arr||[])) {
        if (!m || !m.id) continue;
        if (!idx[m.id]) idx[m.id] = { score: m.score, paramsB: m.paramsB, source };
      }
    };
    add(snapshot.gemma3_full_if_requested, 'gemma3');
    add(snapshot.oss_full_if_requested, 'oss');
    // Also include top arrays if full omitted
    add(snapshot.gemma3_top, 'gemma3_top');
    add(snapshot.oss_top, 'oss_top');
    return idx;
  }
  private diffModelIndexes(newIdx: Record<string, any>, oldIdx: Record<string, any>) {
    const births: any[] = [];
    const deaths: any[] = [];
    const drift: any[] = [];
    for (const id of Object.keys(newIdx)) {
      if (!oldIdx[id]) births.push({ id, source: newIdx[id].source, score: newIdx[id].score });
      else {
        const sNew = newIdx[id].score ?? null;
        const sOld = oldIdx[id].score ?? null;
        if (sNew != null && sOld != null && sNew !== sOld) {
          drift.push({ id, from: sOld, to: sNew, delta: +(sNew - sOld).toFixed(2) });
        }
      }
    }
    for (const id of Object.keys(oldIdx)) {
      if (!newIdx[id]) deaths.push({ id, prev_score: oldIdx[id].score });
    }
    return { births, deaths, drift };
  }
  private async pruneSnapshots(retention?: number) {
    const retain = retention ?? Number(Bun.env.INTEL_SNAPSHOT_RETENTION || process.env.INTEL_SNAPSHOT_RETENTION || 40);
    if (!Number.isFinite(retain) || retain <= 0) return { retained: 'ALL', pruned: [] as string[] };
    const files = await this.listSnapshots();
    if (files.length <= retain) return { retained: files.length, pruned: [] as string[] };
    const toPrune = files.slice(0, files.length - retain); // oldest first
    const pruned: string[] = [];
    for (const f of toPrune) {
      try { await fs.unlink(`${this.snapshotDir}/${f}`); pruned.push(f); } catch { /* ignore */ }
    }
    return { retained: files.length - pruned.length, pruned };
  }
  // Compute per-category ranking maps (Gemma vs OSS) for rank drift analysis
  private computeCategoryRanks(snap: any) {
    function buildRankMap(arr: any[]|undefined) {
      if (!arr || !Array.isArray(arr)) return {} as Record<string, number>;
      const filtered = arr.filter(m => m && typeof m.score === 'number' && m.id);
      filtered.sort((a,b)=> b.score - a.score);
      const map: Record<string, number> = {};
      filtered.forEach((m,i)=> { map[m.id] = i+1; });
      return map;
    }
    const gemmaArr = snap.gemma3_full_if_requested && snap.gemma3_full_if_requested.length ? snap.gemma3_full_if_requested : snap.gemma3_top;
    const ossArr = snap.oss_full_if_requested && snap.oss_full_if_requested.length ? snap.oss_full_if_requested : snap.oss_top;
    return { gemmaRanks: buildRankMap(gemmaArr), ossRanks: buildRankMap(ossArr) };
  }
  private async diffIntelSnapshots(newer?: string, older?: string, limitChanges?: number) {
    const files = await this.listSnapshots();
    if (files.length < 2 && (!newer || !older)) {
      return JSON.stringify({ diff_status: "INSUFFICIENT_SNAPSHOTS", available: files.length }, null, 2);
    }
    let newFile: string | undefined = newer;
    let oldFile: string | undefined = older;
    if (!newFile || !oldFile) {
      // pick last two chronologically
      const sorted = files.slice().sort();
      newFile = newFile || sorted[sorted.length - 1];
      oldFile = oldFile || sorted[sorted.length - 2];
    }
    const newSnap = await this.loadSnapshot(newFile!);
    const oldSnap = await this.loadSnapshot(oldFile!);
    if (!newSnap || !oldSnap) return JSON.stringify({ diff_status: "SNAPSHOT_LOAD_FAILURE", newer: newFile, older: oldFile }, null, 2);
    const newIdx = this.extractModelIndex(newSnap);
    const oldIdx = this.extractModelIndex(oldSnap);
    const diff = this.diffModelIndexes(newIdx, oldIdx);
    // Rank drift layer
    const { gemmaRanks: newGemmaRanks, ossRanks: newOssRanks } = this.computeCategoryRanks(newSnap);
    const { gemmaRanks: oldGemmaRanks, ossRanks: oldOssRanks } = this.computeCategoryRanks(oldSnap);
    const rankDrift: any[] = [];
    const allIds = new Set<string>([...Object.keys(newIdx), ...Object.keys(oldIdx)]);
    for (const id of allIds) {
      const gNew = newGemmaRanks[id]; const gOld = oldGemmaRanks[id];
      const oNew = newOssRanks[id]; const oOld = oldOssRanks[id];
      const gemmaChanged = gNew && gOld && gNew !== gOld;
      const ossChanged = oNew && oOld && oNew !== oOld;
      if (gemmaChanged || ossChanged) {
        const entry: any = { id };
        if (gemmaChanged) entry.gemma_rank = { from: gOld, to: gNew, delta: gNew - gOld };
        if (ossChanged) entry.oss_rank = { from: oOld, to: oNew, delta: oNew - oOld };
        rankDrift.push(entry);
      }
    }
    // Score drift severity classification
    function classifyScoreDrift(absDelta: number) {
      if (absDelta < 500) return 'LOW';
      if (absDelta < 3000) return 'MED';
      if (absDelta < 8000) return 'HIGH';
      return 'CRITICAL';
    }
    for (const d of diff.drift) {
      const absDelta = Math.abs(d.delta || 0);
      d.severity = classifyScoreDrift(absDelta);
    }
    // Rank flux heat index
    let totalAbsRankDelta = 0; let rankEntries = 0;
    for (const r of rankDrift) {
      if (r.gemma_rank) { totalAbsRankDelta += Math.abs(r.gemma_rank.delta); rankEntries++; }
      if (r.oss_rank) { totalAbsRankDelta += Math.abs(r.oss_rank.delta); rankEntries++; }
    }
    const avgAbsRankDelta = rankEntries ? totalAbsRankDelta / rankEntries : 0;
    // Normalize heat index: assume >15 avg abs rank movement is max heat
    const heatIndex = Math.min(1, avgAbsRankDelta / 15);
    const limit = Math.min(Math.max(limitChanges || 60, 1), 200);
    const truncated = {
      births: diff.births.slice(0, limit),
      deaths: diff.deaths.slice(0, limit),
      drift: diff.drift.sort((a,b)=> Math.abs(b.delta) - Math.abs(a.delta)).slice(0, limit)
    };
    const rankTruncated = rankDrift
      .sort((a,b)=> {
        const aDelta = Math.max(Math.abs(a.gemma_rank?.delta||0), Math.abs(a.oss_rank?.delta||0));
        const bDelta = Math.max(Math.abs(b.gemma_rank?.delta||0), Math.abs(b.oss_rank?.delta||0));
        return bDelta - aDelta;
      })
      .slice(0, limit);
    // -------- Per-family volatility metrics --------
    const familyMap: Record<string, number[]> = {};
    const scoreVolDeltas: Record<string, { deltas: number[]; mean_abs: number; max_abs: number; sample: number; class: string }> = {};
    function familyOf(id: string): string {
      const lower = id.toLowerCase();
      if (lower.includes('gemma')) return 'gemma';
      if (lower.includes('llama')) return 'llama';
      if (lower.includes('qwen')) return 'qwen';
      if (lower.includes('phi')) return 'phi';
      if (lower.includes('deepseek')) return 'deepseek';
      if (lower.includes('mistral')) return 'mistral';
      if (lower.includes('yi-') || lower.startsWith('yi')) return 'yi';
      return 'other';
    }
    for (const id of allIds) {
      const n = newIdx[id];
      const o = oldIdx[id];
      if (!n || !o) continue; // only overlapping models for volatility
      const sNew = typeof n.score === 'number' ? n.score : null;
      const sOld = typeof o.score === 'number' ? o.score : null;
      if (sNew == null || sOld == null) continue;
      const delta = sNew - sOld;
      const fam = familyOf(id);
      if (!familyMap[fam]) familyMap[fam] = [];
      familyMap[fam].push(delta);
    }
    for (const [fam, arr] of Object.entries(familyMap)) {
      if (!arr.length) continue;
      const absVals = arr.map(v=>Math.abs(v));
      const meanAbs = absVals.reduce((a,b)=>a+b,0)/absVals.length;
      const maxAbs = Math.max(...absVals);
      const cls = meanAbs < 500 ? 'LOW' : meanAbs < 5000 ? 'MED' : 'HIGH';
      scoreVolDeltas[fam] = { deltas: arr.slice(0, 40), mean_abs: +meanAbs.toFixed(2), max_abs: +maxAbs.toFixed(2), sample: arr.length, class: cls };
    }
    return JSON.stringify({
      diff_status: "INTEL_SNAPSHOT_DIFF",
      newer: newFile,
      older: oldFile,
      counts: { births: diff.births.length, deaths: diff.deaths.length, drift: diff.drift.length, rank_drift: rankDrift.length },
      truncated_limit: limit,
      changes: { ...truncated, rank_drift: rankTruncated },
      volatility: scoreVolDeltas,
      rank_flux_heat: {
        entries_considered: rankEntries,
        total_abs_rank_delta: totalAbsRankDelta,
        avg_abs_rank_delta: +avgAbsRankDelta.toFixed(2),
        heat_index_0_1: +heatIndex.toFixed(3)
      },
      emergent_velocity: (() => {
        // Derive temporal delta between snapshots to normalize births (emergent forks cadence)
        function parseIso(ts: any): number | null { try { const t = Date.parse(ts); return isNaN(t) ? null : t; } catch { return null; } }
        const nMeta = newSnap?.persistence_meta?.stored_at || newSnap?.generated_at;
        const oMeta = oldSnap?.persistence_meta?.stored_at || oldSnap?.generated_at;
        const nT = parseIso(nMeta);
        const oT = parseIso(oMeta);
        if (nT == null || oT == null) return { status: "TIME_BASE_UNAVAILABLE" };
        const deltaMs = nT - oT;
        if (deltaMs <= 0) return { status: "NON_POSITIVE_DELTA", delta_ms: deltaMs };
        const hours = deltaMs / 3600000;
        const births = diff.births.length;
        const birthsPerHour = births / hours;
        const birthsPerDayEst = birthsPerHour * 24;
        // Classification thresholds (heuristic):
        // 0 => STATIC, <1 => LOW, <4 => MODERATE, <10 => ELEVATED, >=10 => ACCELERATED
        let cls: string;
        if (births === 0) cls = 'STATIC';
        else if (birthsPerDayEst < 1) cls = 'LOW';
        else if (birthsPerDayEst < 4) cls = 'MODERATE';
        else if (birthsPerDayEst < 10) cls = 'ELEVATED';
        else cls = 'ACCELERATED';
        return {
          status: "OK",
          delta_hours: +hours.toFixed(2),
          births,
            births_per_hour: +birthsPerHour.toFixed(4),
          births_per_day_estimate: +birthsPerDayEst.toFixed(3),
          classification: cls,
          interpretation: cls === 'STATIC' ? 'No emergent repos observed in interval.' :
            cls === 'LOW' ? 'Minor emergence; routine ecosystem drift.' :
            cls === 'MODERATE' ? 'Notable new model cadence—monitor for quality claims.' :
            cls === 'ELEVATED' ? 'Accelerating fork proliferation—perform authenticity sampling.' :
            'High-intensity emergence—investigate for hype cycles or coordinated releases.'
        };
      })(),
      guidance: [
        "Births = newly appearing models (potential emerging forks).",
        "Deaths = disappeared or de-ranked models (verify if rename or deletion).",
        "Drift = score flux; re-evaluate latency & accuracy if large deltas.",
        "Rank drift = positional movement within family leaderboard; investigate sudden large upward jumps for authenticity / optimization claims.",
        "Volatility classes: LOW (<500 mean abs delta), MED (<5000), HIGH (>=5000). Sudden HIGH warrants manual authenticity & anomaly review.",
        "Score drift severity: LOW(<500) MED(<3000) HIGH(<8000) CRITICAL(>=8000).",
        "Rank flux heat index ~ aggregate momentum; >0.6 suggests competitive reshuffling; investigate for optimization claims or manipulation.",
        "Emergent velocity estimates rate of new model appearance normalized by time delta; sustained ELEVATED/ACCELERATED requires authenticity triage." ]
    }, null, 2);
  }
  // ---------- Authenticity Sentinel ----------
  private async authenticitySentinelProbe(repoIds?: string[], limit?: number, internal?: boolean) {
    const ids = (repoIds && repoIds.length ? repoIds : []).slice(0, Math.min(Math.max(limit || 40, 1), 60));
    if (!ids.length && !internal) return JSON.stringify({ sentinel_status: "NO_REPO_IDS" }, null, 2);
    const analyses: any[] = [];
    for (const id of ids) {
      try {
        const metaRaw = await this.hfModelInfo(id, true, false); // includes license if available
        const meta = JSON.parse(metaRaw);
        const scoreObj = this.computeAuthenticityScore(meta);
        analyses.push({ id, ...scoreObj });
        await Bun.sleep(40); // gentle pacing
      } catch (e) {
        analyses.push({ id, error: (e as Error).message, authenticity_score: 0, risk_tier: 'UNKNOWN' });
      }
    }
    const summary = this.summarizeAuthenticity(analyses);
    return JSON.stringify({
      sentinel_status: internal ? "INTERNAL_SNAPSHOT_ENRICHMENT" : "AUTHENTICITY_SENTINEL",
      analyzed: analyses.length,
      summary,
      analyses: internal ? analyses.slice(0,25) : analyses
    }, null, 2);
  }
  private computeAuthenticityScore(meta: any) {
    // Heuristic components
    const id: string = meta.id || "";
    const officialOrg = id.startsWith('google/') || id.startsWith('meta-llama/') || id.startsWith('microsoft/') || id.startsWith('Qwen/') || id.startsWith('Qwen2/') || id.startsWith('mistralai/');
    const license = meta.card_license || '';
    const hasPermissive = /apache|mit|bsd|cc-by|llama|gemma/i.test(license);
    const gatedPenalty = meta.gated ? -400 : 0; // gating is not necessarily bad but reduces open authenticity confidence
    const privatePenalty = meta.private ? -600 : 0;
    const downloadWeight = Math.min((meta.downloads || 0) / 5000, 2000); // cap influence
    const likesWeight = Math.min((meta.likes || 0) * 5, 2500);
    const orgBoost = officialOrg ? 2500 : 0;
    const licenseBoost = hasPermissive ? 600 : -300;
    const rawScore = orgBoost + licenseBoost + downloadWeight + likesWeight + gatedPenalty + privatePenalty;
    const authenticity_score = Math.max(0, Math.round(rawScore));
    const risk_tier = authenticity_score >= 4000 ? 'LOW' : authenticity_score >= 1800 ? 'MODERATE' : 'ELEVATED';
    return { authenticity_score, risk_tier, official_org: officialOrg, license_detected: license || null };
  }
  private summarizeAuthenticity(analyses: any[]) {
    if (!analyses.length) return { average: 0, elevated: 0, moderate: 0, low: 0 };
    let total = 0, elevated = 0, moderate = 0, low = 0;
    for (const a of analyses) {
      total += a.authenticity_score || 0;
      if (a.risk_tier === 'LOW') low++; else if (a.risk_tier === 'MODERATE') moderate++; else if (a.risk_tier === 'ELEVATED') elevated++;
    }
    return { average: Math.round(total / analyses.length), elevated, moderate, low };
  }
  private async multimodalMobileModelAdvisor(minDownloads?: number, includeAlternatives?: boolean) {
    // Use existing Gemma 3 multimodal scan as backbone
    const scanRaw = await this.gemma3MultimodalMobileScan(12, minDownloads);
    let scan: any = {};
    try { scan = JSON.parse(scanRaw); } catch {}
    const gemmaCandidates = (scan.results || []).slice(0, 6);
    // Heuristic param + memory table
    function memoryEst(paramsB: number | null, quant: 'q4'|'q6'|'q8'|'fp16'): number | null {
      if (paramsB == null) return null;
      const params = paramsB * 1e9;
      const bytesPerParam = quant === 'fp16' ? 2 : quant === 'q8' ? 1 : quant === 'q6' ? 0.75 : 0.5; // approximate
      return +(params * bytesPerParam / (1024**3)).toFixed(2);
    }
    const enriched = gemmaCandidates.map((c:any) => {
      return {
        id: c.id,
        paramsB: c.paramsB,
        downloads: c.downloads,
        likes: c.likes,
        vision: c.vision,
        multimodal: c.multimodal,
        est_mem_gb: { q4: memoryEst(c.paramsB,'q4'), q6: memoryEst(c.paramsB,'q6'), q8: memoryEst(c.paramsB,'q8'), fp16: memoryEst(c.paramsB,'fp16') }
      };
    });
    // Alternative OSS (static curated list for now)
    const alt: any[] = includeAlternatives ? [
      { id: 'meta-llama/Llama-3.2-3B-Instruct', paramsB: 3, note: 'Strong general baseline; needs vision adapter for multimodal', vision_native: false },
      { id: 'Qwen/Qwen2-VL-2B-Instruct', paramsB: 2, note: 'Native vision-language; competitive small VLM', vision_native: true },
      { id: 'microsoft/phi-3.5-vision-instruct', paramsB: 4, note: 'Compact multimodal reasoning; optimized for edge', vision_native: true },
      { id: 'google/paligemma-3b-pt-224', paramsB: 3, note: 'Vision-text (earlier lineage); good for image grounding', vision_native: true }
    ] : [];
    const loadSnippets = {
      gemma_text_generation: `python\nfrom transformers import AutoModelForCausalLM, AutoTokenizer\nimport torch\nmodel_id = "google/gemma-3-?b"  # replace with chosen candidate\ntok = AutoTokenizer.from_pretrained(model_id)\nmodel = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", torch_dtype=torch.float16)\nprint(tok.decode(model.generate(tok("Hello Gemma 3" , return_tensors='pt').input_ids, max_new_tokens=32)[0]))`,
      gemma_vision_multimodal: `python\nfrom transformers import AutoProcessor, AutoModelForVision2Seq\nmodel_id = "google/gemma-3-vision-?b"  # if/when available\nprocessor = AutoProcessor.from_pretrained(model_id)\nmodel = AutoModelForVision2Seq.from_pretrained(model_id, device_map="auto")\ninputs = processor(text="Describe the image.", images=[...], return_tensors="pt").to(model.device)\nout = model.generate(**inputs, max_new_tokens=64)\nprint(processor.batch_decode(out, skip_special_tokens=True))`,
      q4_gguf_edge: `bash\n# Example llama.cpp style invocation (replace with actual gemma3 gguf path)\n./main -m gemma-3-2b-q4_k_m.gguf -p "Describe the noir skyline." -n 64 --temp 0.7`,
      on_device_hint: `text\nFor Galaxy S25 class (>=16GB RAM, modern NPU):\n- 2B Q4_K_M: ~1.0-1.2 GB VRAM/CPU RAM residency\n- 4B Q4_K_M: ~1.9-2.2 GB\n- 9B Q4_K_M: ~4.0-4.5 GB (borderline for continuous multitasking)\nPrioritize context compression + early token streaming.`
    };
    return JSON.stringify({
      advisor_status: "MULTIMODAL_MOBILE_MODEL_ADVISOR",
      minDownloads: minDownloads || 0,
      gemma3_candidates: enriched,
      alternatives_included: includeAlternatives,
      alternative_models: alt,
      selection_guidance: [
        "Pick smallest param bucket meeting task quality thresholds (2B/3B sweet spot).",
        "Use Q4_K_M for baseline; escalate to Q6 if hallucination profile degrades.",
        "Prefer native vision-language model over bolted adapter when latency-critical.",
        "Validate tokenizer equivalence and EOS token behavior pre‑deployment."],
      transformer_snippets: loadSnippets
    }, null, 2);
  }

  // ---------- Meta ----------
  private integritySnapshot() {
    return JSON.stringify({
      orchestrator_status: "OPERATIONAL",
      tool_count: this.tools().length,
      amplification: this.state.consciousness_amplification,
      cache_entries: this.hfCache.size,
      env: {
        HF_TOKEN_PRESENT: !!(Bun.env.HF_TOKEN || process.env.HF_TOKEN),
        GEMMA_MODEL_PATH: Bun.env.GEMMA_MODEL_PATH || "models/gemma-300m-q4.gguf"
      }
    }, null, 2);
  }

  // ---------- Model Registry Inspection (Tier 0 surface) ----------
  private async modelRegistryInspect() {
    let raw: string | null = null;
    try { raw = await fs.readFile('model_registry.json','utf-8'); } catch { return JSON.stringify({ registry_status: 'ABSENT' }, null, 2); }
    let parsed: any;
    try { parsed = JSON.parse(raw); } catch { return JSON.stringify({ registry_status: 'PARSE_FAILURE' }, null, 2); }
    if (!Array.isArray(parsed)) return JSON.stringify({ registry_status: 'INVALID_SHAPE' }, null, 2);
    const enriched = parsed.map((e: any) => {
      const readyForBenchmark = !!(e.artifacts && e.artifacts.primary) && e.last_benchmark == null;
      return {
        id: e.id,
        family: e.family,
        params_b: e.params_b,
        modalities: e.modalities,
        quantizations: e.quantizations,
        needs_benchmark: readyForBenchmark,
        last_benchmark: e.last_benchmark ? 'PRESENT' : null
      };
    });
    const pending = enriched.filter((e: any)=> e.needs_benchmark).map((e:any)=> e.id);
    return JSON.stringify({
      registry_status: 'OK',
      entries: enriched.length,
      pending_benchmarks: pending.length,
      pending_ids: pending.slice(0, 25),
      entries_detail: enriched.slice(0, 50)
    }, null, 2);
  }

  // ---------- Tier 1: Benchmark Stub ----------
  private async modelBenchmarkStub(modelId?: string) {
    // Load registry
    let raw: string | null = null; try { raw = await fs.readFile('model_registry.json','utf-8'); } catch { return JSON.stringify({ benchmark_status: 'REGISTRY_ABSENT' }, null, 2); }
    let reg: any[] = []; try { reg = JSON.parse(raw!); } catch { return JSON.stringify({ benchmark_status: 'REGISTRY_PARSE_FAILURE' }, null, 2); }
    if (!Array.isArray(reg)) return JSON.stringify({ benchmark_status: 'INVALID_REGISTRY_SHAPE' }, null, 2);
    // Pick first needing benchmark if no id
    let target = modelId ? reg.find(r=> r.id === modelId) : reg.find(r=> !r.last_benchmark);
    if (!target) return JSON.stringify({ benchmark_status: 'NO_TARGET_MODEL', model_id: modelId || null }, null, 2);
    // Synthetic metrics (placeholder)
    const now = Date.now();
    const synth = {
      benchmarked_at: new Date().toISOString(),
      first_token_ms: Math.round(180 + Math.random()*120),
      decode_tok_s: +(5 + Math.random()*2).toFixed(2),
      memory_peak_mb: Math.round((target.params_b || 2) * 520),
      energy_hint_mj: +(0.4 + Math.random()*0.2).toFixed(3),
      temperature: 0.7,
      synthetic: true,
      run_id: `stub-${now}`
    };
    target.last_benchmark = synth;
    await fs.writeFile('model_registry.json', JSON.stringify(reg, null, 2), 'utf-8');
    return JSON.stringify({ benchmark_status: 'SYNTHETIC_BENCHMARK_RECORDED', model: target.id, metrics: synth }, null, 2);
  }

  // ---------- Tier 1 Expansion: Auto Benchmark All (synthetic) ----------
  private async modelBenchmarkAuto(rebenchmark: boolean) {
    let raw: string | null = null; try { raw = await fs.readFile('model_registry.json','utf-8'); } catch { return JSON.stringify({ benchmark_status: 'REGISTRY_ABSENT' }, null, 2); }
    let reg: any[] = []; try { reg = JSON.parse(raw!); } catch { return JSON.stringify({ benchmark_status: 'REGISTRY_PARSE_FAILURE' }, null, 2); }
    const historyPath = 'benchmark_history.json';
    let history: any[] = []; try { history = JSON.parse(await fs.readFile(historyPath,'utf-8')); } catch { /* ignore */ }
    let performed = 0;
    // Initialize runtime manager lazily
    if (!this.runtimeManager) this.runtimeManager = new RuntimeManager();
    for (const model of reg) {
      if (model.last_benchmark && !rebenchmark) continue;
      if (model.last_benchmark && rebenchmark) {
        if (!model.benchmark_history) model.benchmark_history = [];
        model.benchmark_history.push(model.last_benchmark);
      }
      let record: any = null;
      let source = 'SYNTHETIC';
      try {
        const runner = await this.runtimeManager.getRunner(model.id);
        if (runner && runner.ready) {
          const prompt = "\nBENCHMARK_HELIX: report latent entropy of rustbelt relics.";
          const t0 = performance.now();
          let firstTokenTime: number | undefined;
          let tokenCount = 0;
          const res = await runner.generateText({ prompt, maxTokens: 48, stream: true }, (tk: any)=> {
            tokenCount++;
            if (firstTokenTime === undefined) firstTokenTime = performance.now();
          });
          const total = performance.now() - t0;
          record = {
            benchmarked_at: new Date().toISOString(),
            first_token_ms: firstTokenTime ? +(firstTokenTime - t0).toFixed(1) : null,
            decode_tok_s: (tokenCount > 1 && firstTokenTime) ? +(((tokenCount-1)/((performance.now() - firstTokenTime)/1000))).toFixed(2) : null,
            memory_peak_mb: null,
            energy_hint_mj: null,
            synthetic: false,
            source: 'REAL',
            backend: runner.capabilities().family,
            run_id: `real-${Date.now()}-${model.id}`,
            total_ms: +total.toFixed(1)
          };
          source = 'REAL';
        }
      } catch { /* fallback to synthetic */ }
      if (!record) {
        const now = Date.now();
        record = {
          benchmarked_at: new Date().toISOString(),
          first_token_ms: Math.round(170 + Math.random()*140),
          decode_tok_s: +(4.5 + Math.random()*2.5).toFixed(2),
          memory_peak_mb: Math.round((model.params_b || 2) * (480 + Math.random()*80)),
          energy_hint_mj: +(0.38 + Math.random()*0.25).toFixed(3),
          synthetic: true,
          source: 'SYNTHETIC',
          run_id: `auto-${now}-${model.id}`
        };
      }
      model.last_benchmark = record;
      history.push({ id: model.id, run_id: record.run_id, source, metrics: { first_token_ms: record.first_token_ms, decode_tok_s: record.decode_tok_s, memory_peak_mb: record.memory_peak_mb }, ts: record.benchmarked_at });
      performed++;
    }
    await fs.writeFile('model_registry.json', JSON.stringify(reg, null, 2), 'utf-8');
    // retain last 400 history entries
    if (history.length > 400) history = history.slice(history.length - 400);
    await fs.writeFile(historyPath, JSON.stringify(history, null, 2), 'utf-8');
    // summarize drift (simple first vs last per model)
    const drift: any[] = [];
    const byModel: Record<string, any[]> = {};
    for (const h of history) { if (!byModel[h.id]) byModel[h.id] = []; byModel[h.id].push(h); }
    for (const [id, arr] of Object.entries(byModel)) {
      if (arr.length < 2) continue;
      const first = arr[0].metrics; const last = arr[arr.length-1].metrics;
      drift.push({ id, first_token_ms_delta: +(last.first_token_ms - first.first_token_ms).toFixed(1), decode_tok_s_delta: +(last.decode_tok_s - first.decode_tok_s).toFixed(2) });
    }
    return JSON.stringify({ benchmark_status: 'AUTO_BENCHMARK_COMPLETE', models_cataloged: reg.length, benchmarks_performed: performed, rebenchmark, drift_summary: drift.slice(0, 40) }, null, 2);
  }

  // ---------- Runtime Direct Generation ----------
  private async modelRuntimeGenerate(modelId: string, prompt: string, maxTokens?: number) {
    if (!modelId || !prompt) return JSON.stringify({ runtime_status: 'MISSING_ARGS' }, null, 2);
    if (!this.runtimeManager) this.runtimeManager = new RuntimeManager();
    const runner = await this.runtimeManager.getRunner(modelId);
    if (!runner || !runner.ready) return JSON.stringify({ runtime_status: 'RUNNER_UNAVAILABLE', model_id: modelId }, null, 2);
    let firstTokenTime: number | undefined;
    let tokenCount = 0;
    const t0 = performance.now();
  const res = await runner.generateText({ prompt, maxTokens: maxTokens || 128, stream: true }, (tk: any)=> {
      tokenCount++;
      if (firstTokenTime === undefined) firstTokenTime = performance.now();
    });
    const total = performance.now() - t0;
    return JSON.stringify({
      runtime_status: 'GENERATION_COMPLETE',
      model_id: modelId,
      backend: runner.capabilities().family,
      first_token_ms: firstTokenTime ? +(firstTokenTime - t0).toFixed(1) : null,
      total_ms: +total.toFixed(1),
      tokens: tokenCount,
      text: res.text.slice(0, 400),
      truncated: res.text.length > 400
    }, null, 2);
  }

  // ---------- Local HF Transformers bridge (Python) ----------
  private async hfTransformersGenerate(a: any): Promise<string> {
    const py = [ 'python3', 'tools/hf_transformers_generate.py' ];
    const args: string[] = [];
    function pushKV(k:string,v:any){ if (v===undefined||v===null) return; args.push(`--${k}`); args.push(String(v)); }
    pushKV('model', a.model);
    pushKV('prompt', a.prompt);
    pushKV('max_new_tokens', a.max_new_tokens || 128);
    pushKV('quant', a.quant || 'auto');
    pushKV('temperature', a.temperature ?? 0.7);
    pushKV('top_p', a.top_p ?? 0.95);
    pushKV('top_k', a.top_k);
    pushKV('repetition_penalty', a.repetition_penalty);
    pushKV('trust_remote_code', a.trust_remote_code ? 'true' : 'false');
    const p = Bun.spawn([ ...py, ...args ], { stdout: 'pipe', stderr: 'pipe' });
    const out = await new Response(p.stdout).text();
    const err = await new Response(p.stderr).text();
    const code = await p.exited;
    if (code !== 0) {
      // If the python runner printed a structured JSON error to stdout, surface that instead of a generic failure
      try {
        const j = JSON.parse(out);
        if (j && typeof j === 'object' && j.transformers_status) {
          return JSON.stringify(j, null, 2);
        }
      } catch {}
      return JSON.stringify({ transformers_status: 'PY_RUNNER_FAILED', code, err: err.slice(-4000) }, null, 2);
    }
    return out.trim();
  }

  // ---------- Curated official repos guidance ----------
  private officialFoundationReposProbe(cpuOnly: boolean): string {
    const repos = [
      { family: 'Gemma 3', org: 'google', repo: 'gemma', notes: 'Official docs + model card; HF models under google/*', link: 'https://ai.google.dev/gemma' },
      { family: 'Llama', org: 'meta-llama', repo: 'Llama-3.1', notes: 'Official Meta releases; HF requires access', link: 'https://ai.meta.com/llama/' },
      { family: 'Phi', org: 'microsoft', repo: 'phi-4', notes: 'MSFT small models; check license and HF availability', link: 'https://huggingface.co/microsoft' },
      { family: 'Qwen', org: 'Qwen', repo: 'Qwen2.5', notes: 'Strong OSS, many quantized variants on HF', link: 'https://huggingface.co/Qwen' },
      { family: 'Mistral', org: 'mistralai', repo: 'Mistral-Nemo', notes: 'High quality OSS; look for instruct and small variants', link: 'https://huggingface.co/mistralai' }
    ];
    const suggestions = cpuOnly ? [
      { id: 'Qwen/Qwen2.5-1.5B-Instruct', reason: 'Good CPU viability; supports 4/8-bit' },
      { id: 'microsoft/Phi-3-mini-4k-instruct', reason: 'Small, efficient; practical on CPU' },
      { id: 'google/gemma-2-2b-it', reason: 'If access + quantization; 8-bit acceptable on strong CPU' }
    ] : [
      { id: 'meta-llama/Llama-3.1-8B-Instruct', reason: 'If GPU available; strong generalist' },
      { id: 'Qwen/Qwen2.5-7B-Instruct', reason: 'Competitive; good quantization support' },
      { id: 'mistralai/Mistral-7B-Instruct-v0.3', reason: 'Proven, wide ecosystem support' }
    ];
    return JSON.stringify({ probe_status: 'OFFICIAL_FOUNDATION_REPOS', cpu_only: cpuOnly, repos, suggestions }, null, 2);
  }

  // ---------- Environment Secret Presence Probe ----------
  private envSecretPresenceProbe(): string {
    const keys = [ 'TAVILY_API_KEY', 'HF_TOKEN', 'GEMMA_MODEL_PATH', 'GITHUB_TOKEN' ];
    const presence = Object.fromEntries(keys.map(k => [k, !!(process.env[k] || (Bun.env as any)[k]) ]));
    return JSON.stringify({ env_probe_status: 'ENV_SECRET_PRESENCE', timestamp: new Date().toISOString(), presence, guidance: 'Add or update values in .env then restart process to reload. Values are not revealed for safety.' }, null, 2);
  }
  // ---------- Environment Secret Setter (restricted) ----------
  private async envSecretSet(key: string, value: string, create: boolean): Promise<string> {
  const allowed = new Set([ 'TAVILY_API_KEY','HF_TOKEN','GEMMA_MODEL_PATH','GITHUB_TOKEN' ]);
    if (!allowed.has(key)) {
      return JSON.stringify({ status: 'ENV_SECRET_SET_DENIED', reason: 'KEY_NOT_ALLOWED', key });
    }
    if (!value || value.trim().length < 6) {
      return JSON.stringify({ status: 'ENV_SECRET_SET_DENIED', reason: 'VALUE_TOO_SHORT' });
    }
    const dotenvPath = '.env';
    let existing: string[] = [];
    try { const raw = await fs.readFile(dotenvPath,'utf-8'); existing = raw.split(/\r?\n/); } catch { if (!create) return JSON.stringify({ status: 'ENV_SECRET_SET_FAILED', reason: 'DOTENV_ABSENT', hint: 'Pass create=true to forge new noir vault' }); }
    // remove prior occurrences
    existing = existing.filter(l => l && !l.startsWith(key + '='));
    existing.push(`${key}=${JSON.stringify(value)}`); // JSON.stringify to handle special chars safely
    try { await fs.writeFile(dotenvPath, existing.join('\n') + '\n','utf-8'); } catch (e) {
      return JSON.stringify({ status: 'ENV_SECRET_SET_FAILED', reason: 'WRITE_ERROR', message: (e as Error).message });
    }
    return JSON.stringify({ status: 'ENV_SECRET_SET_OK', key, length: value.length, note: 'Process must reload to reflect in Bun.env', timestamp: new Date().toISOString() });
  }
  private async envSecretsBootstrap(args: any): Promise<string> {
  const { TAVILY_API_KEY, HF_TOKEN, GEMMA_MODEL_PATH, GITHUB_TOKEN, create } = args || {};
    const ops: any[] = [];
    const toSet: [string,string][] = [];
    if (TAVILY_API_KEY) toSet.push(['TAVILY_API_KEY', TAVILY_API_KEY]);
    if (HF_TOKEN) toSet.push(['HF_TOKEN', HF_TOKEN]);
  if (GEMMA_MODEL_PATH) toSet.push(['GEMMA_MODEL_PATH', GEMMA_MODEL_PATH]);
  if (GITHUB_TOKEN) toSet.push(['GITHUB_TOKEN', GITHUB_TOKEN]);
    if (!toSet.length) return JSON.stringify({ status: 'ENV_SECRETS_BOOTSTRAP_NOOP', message: 'No keys provided' });
    for (const [k,v] of toSet) {
      ops.push(JSON.parse(await this.envSecretSet(k, v, !!create)));
    }
    return JSON.stringify({ status: 'ENV_SECRETS_BOOTSTRAP_COMPLETE', operations: ops }, null, 2);
  }
  private envSecretReload(force: boolean): string {
    const dotenvPath = '.env';
    let loaded = 0; let skipped = 0;
    try {
      // Bun.file() has async text(); use Node sync read for simplicity here
      const text = require('fs').readFileSync(dotenvPath,'utf-8');
      for (const line of text.split(/\r?\n/)) {
        if (!line || line.startsWith('#')) continue;
        const eq = line.indexOf('='); if (eq === -1) continue;
        const k = line.slice(0,eq).trim(); const v = line.slice(eq+1).trim();
        if (!force && process.env[k]) { skipped++; continue; }
        process.env[k] = v; loaded++;
      }
      return JSON.stringify({ status: 'ENV_SECRET_RELOAD_OK', loaded, skipped, force });
    } catch (e) {
      return JSON.stringify({ status: 'ENV_SECRET_RELOAD_FAILED', reason: 'READ_ERROR', message: (e as Error).message });
    }
  }

  // ---------- GitHub Integration Layer (headless) ----------
  private ghHeaders(): Record<string,string> {
    const h: Record<string,string> = { 'Accept': 'application/vnd.github+json' };
    const tok = process.env.GITHUB_TOKEN || (Bun.env as any)?.GITHUB_TOKEN;
    if (tok) h['Authorization'] = `Bearer ${tok}`;
    h['X-GitHub-Api-Version'] = '2022-11-28';
    return h;
  }
  private async githubRepoMeta(owner: string, repo: string): Promise<string> {
    if (!owner || !repo) return 'MISSING_OWNER_OR_REPO';
    const url = `https://api.github.com/repos/${owner}/${repo}`;
    try {
      const r = await fetch(url, { headers: this.ghHeaders() });
      if (!r.ok) return JSON.stringify({ github_status: 'REPO_META_ERROR', status: r.status });
      const j: any = await r.json();
      const meta = { full_name: j.full_name, private: j.private, stars: j.stargazers_count, forks: j.forks_count, open_issues: j.open_issues_count, watchers: j.watchers_count, license: j.license?.spdx_id, pushed_at: j.pushed_at, created_at: j.created_at, default_branch: j.default_branch };
      return JSON.stringify({ github_status: 'REPO_META', meta }, null, 2);
    } catch (e) { return JSON.stringify({ github_status: 'REPO_META_EXCEPTION', message: (e as Error).message }); }
  }
  private async githubRepoIssues(owner: string, repo: string, state?: string, limit?: number): Promise<string> {
    if (!owner || !repo) return 'MISSING_OWNER_OR_REPO';
    const lim = Math.min(Math.max(limit || 15,1),100);
    const url = `https://api.github.com/repos/${owner}/${repo}/issues?state=${encodeURIComponent(state||'open')}&per_page=${lim}`;
    try {
      const r = await fetch(url, { headers: this.ghHeaders() });
      if (!r.ok) return JSON.stringify({ github_status: 'REPO_ISSUES_ERROR', status: r.status });
      const arr: any[] = await r.json();
      const simplified = arr.filter(i=> !i.pull_request).map(i=> ({ number: i.number, title: i.title, state: i.state, comments: i.comments, created_at: i.created_at, updated_at: i.updated_at, author: i.user?.login })).slice(0, lim);
      return JSON.stringify({ github_status: 'REPO_ISSUES', count: simplified.length, state: state||'open', issues: simplified }, null, 2);
    } catch (e) { return JSON.stringify({ github_status: 'REPO_ISSUES_EXCEPTION', message: (e as Error).message }); }
  }
  private async githubRepoSearch(query: string, limit?: number): Promise<string> {
    if (!query) return 'MISSING_QUERY';
    const lim = Math.min(Math.max(limit || 10,1),50);
    const url = `https://api.github.com/search/repositories?q=${encodeURIComponent(query)}&per_page=${lim}`;
    try {
      const r = await fetch(url, { headers: this.ghHeaders() });
      if (!r.ok) return JSON.stringify({ github_status: 'REPO_SEARCH_ERROR', status: r.status });
      const j: any = await r.json();
      const repos = (j.items||[]).map((i:any)=> ({ full_name: i.full_name, stars: i.stargazers_count, forks: i.forks_count, issues: i.open_issues_count, updated_at: i.updated_at, license: i.license?.spdx_id })).slice(0, lim);
      return JSON.stringify({ github_status: 'REPO_SEARCH', query, count: repos.length, repos }, null, 2);
    } catch (e) { return JSON.stringify({ github_status: 'REPO_SEARCH_EXCEPTION', message: (e as Error).message }); }
  }
  private async githubDeviceCodeInitiate(clientId: string, scope?: string): Promise<string> {
    if (!clientId) return 'MISSING_CLIENT_ID';
    try {
      const resp = await fetch('https://github.com/login/device/code', { method: 'POST', headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' }, body: JSON.stringify({ client_id: clientId, scope: scope || 'repo read:user' }) });
      if (!resp.ok) return JSON.stringify({ github_status: 'DEVICE_CODE_ERROR', status: resp.status });
      const data: any = await resp.json();
      return JSON.stringify({ github_status: 'DEVICE_CODE_INITIATED', user_code: data.user_code, verification_uri: data.verification_uri, expires_in: data.expires_in, interval: data.interval, device_code: data.device_code, guidance: 'Visit verification_uri and enter user_code. Then poll via github_device_code_poll.' }, null, 2);
    } catch (e) { return JSON.stringify({ github_status: 'DEVICE_CODE_EXCEPTION', message: (e as Error).message }); }
  }
  private async githubDeviceCodePoll(clientId: string, deviceCode: string, interval?: number, create?: boolean): Promise<string> {
    if (!clientId || !deviceCode) return 'MISSING_CLIENT_OR_DEVICE';
    try {
      const resp = await fetch('https://github.com/login/oauth/access_token', { method: 'POST', headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' }, body: JSON.stringify({ client_id: clientId, device_code: deviceCode, grant_type: 'urn:ietf:params:oauth:grant-type:device_code' }) });
      const data: any = await resp.json();
      if (data.error) {
        return JSON.stringify({ github_status: 'DEVICE_CODE_POLL_PENDING', error: data.error, error_description: data.error_description });
      }
      if (data.access_token) {
        // Optionally persist as GITHUB_TOKEN
        if (create) {
          await this.envSecretSet('GITHUB_TOKEN', data.access_token, true);
        }
        return JSON.stringify({ github_status: 'DEVICE_CODE_TOKEN_GRANTED', scope: data.scope, token_type: data.token_type, persisted: !!create }, null, 2);
      }
      return JSON.stringify({ github_status: 'DEVICE_CODE_POLL_UNKNOWN_RESPONSE', raw: data });
    } catch (e) { return JSON.stringify({ github_status: 'DEVICE_CODE_POLL_EXCEPTION', message: (e as Error).message }); }
  }

  // ---------- VS Code Log Snapshot (best-effort inside container) ----------
  private async vscodeLogSnapshot(recentMinutes?: number): Promise<string> {
    const minutes = Math.min(Math.max(recentMinutes || 30, 1), 240);
    const cutoff = Date.now() - minutes * 60 * 1000;
    const logRoots: string[] = [];
    const userConfig = process.env.HOME ? `${process.env.HOME}/.config/Code/logs` : null;
    if (userConfig) logRoots.push(userConfig);
    const collected: any[] = [];
    const outDir = 'mcp_diagnostics';
    await fs.mkdir(outDir, { recursive: true }).catch(()=>{});
    for (const root of logRoots) {
      try {
        const entries = await fs.readdir(root, { withFileTypes: true });
        for (const dirent of entries) {
          if (!dirent.isDirectory()) continue;
            const sessionPath = `${root}/${dirent.name}`;
            let stat: any; try { stat = await fs.stat(sessionPath); } catch { continue; }
            if (stat.mtimeMs < cutoff) continue;
            // target sub logs
            const subCandidates = [ 'renderer1', 'sharedprocess', 'exthost1' ];
            for (const sub of subCandidates) {
              const subPath = `${sessionPath}/${sub}`;
              try {
                const files = await fs.readdir(subPath);
                for (const f of files) {
                  if (!f.endsWith('.log')) continue;
                  const full = `${subPath}/${f}`;
                  let content = '';
                  try { content = await fs.readFile(full, 'utf-8'); } catch {}
                  const trimmed = content.slice(-8000); // tail segment
                  const rel = full.replace(root,'');
                  collected.push({ file: rel, tail_len: trimmed.length, full_len: content.length });
                  const snapName = `${outDir}/${f.replace(/[^a-zA-Z0-9_.-]/g,'_')}.tail.log`;
                  await fs.writeFile(snapName, trimmed, 'utf-8').catch(()=>{});
                }
              } catch {}
            }
        }
      } catch {}
    }
    const index = { snapshot_status: 'VSCODE_LOG_SNAPSHOT', minutes, collected: collected.length, files: collected.slice(0,50), directory: outDir, guidance: 'Tail segments saved (last 8K each). Provide these when reporting redirect failures.' };
    const indexPath = `${outDir}/index.json`;
    try { await fs.writeFile(indexPath, JSON.stringify(index, null, 2),'utf-8'); } catch {}
    return JSON.stringify(index, null, 2);
  }
  private liveSessionDir = 'live_sessions_state';
  private ensureLiveDirOnce: Promise<void> | null = null;
  private async ensureLiveDir() { if (!this.ensureLiveDirOnce) this.ensureLiveDirOnce = fs.mkdir(this.liveSessionDir, { recursive: true }).then(()=>{}).catch(()=>{}); return this.ensureLiveDirOnce; }
  private async persistLiveSession(id: string) { await this.ensureLiveDir(); const sess = this.liveSessions.get(id); if (!sess) return; try { await fs.writeFile(`${this.liveSessionDir}/${id}.json`, JSON.stringify({ id, ...sess }, null, 2),'utf-8'); } catch {} }
  private async hydrateLiveSessions() { await this.ensureLiveDir(); try { const files = (await fs.readdir(this.liveSessionDir)).filter(f=> f.endsWith('.json')); const now = Date.now(); for (const f of files) { try { const raw = await fs.readFile(`${this.liveSessionDir}/${f}`,'utf-8'); const obj = JSON.parse(raw); if (now - obj.created < 6*3600*1000) this.liveSessions.set(obj.id, { prompt: obj.prompt, created: obj.created, tokens: obj.tokens||[], complete: !!obj.complete }); } catch {} } } catch {} }

  // ---------- Tier 2: Artifact Integrity Scan (skeleton) ----------
  private async artifactIntegrityScan(fast: boolean) {
    let raw: string | null = null; try { raw = await fs.readFile('model_registry.json','utf-8'); } catch { return JSON.stringify({ artifact_scan_status: 'REGISTRY_ABSENT' }, null, 2); }
    let reg: any[] = []; try { reg = JSON.parse(raw!); } catch { return JSON.stringify({ artifact_scan_status: 'REGISTRY_PARSE_FAILURE' }, null, 2); }
    const results: any[] = [];
    for (const entry of reg) {
      const path = entry?.artifacts?.primary;
      if (!path) { results.push({ id: entry.id, status: 'NO_PRIMARY_ARTIFACT' }); continue; }
      try {
        const stat = await fs.stat(path);
        let hash: string | undefined = undefined;
        if (!fast && stat.isFile() && stat.size < 512 * 1024 * 1024) { // avoid hashing huge files in skeleton
          const buf = await fs.readFile(path);
            hash = createHash('sha256').update(buf).digest('hex');
        }
        results.push({ id: entry.id, exists: true, size_bytes: stat.size, sha256: hash || null });
      } catch {
        results.push({ id: entry.id, exists: false });
      }
    }
    return JSON.stringify({ artifact_scan_status: 'ARTIFACT_SCAN_COMPLETE', fast, inspected: results.length, results: results.slice(0, 60) }, null, 2);
  }

  // ---------- Tier 5: Anomaly Scan (stub heuristic) ----------
  private async modelAnomalyScan() {
    let raw: string | null = null; try { raw = await fs.readFile('model_registry.json','utf-8'); } catch { return JSON.stringify({ anomaly_status: 'REGISTRY_ABSENT' }, null, 2); }
    let reg: any[] = []; try { reg = JSON.parse(raw!); } catch { return JSON.stringify({ anomaly_status: 'REGISTRY_PARSE_FAILURE' }, null, 2); }
    const anomalies: any[] = [];
    for (const e of reg) {
      const bm = e.last_benchmark;
      if (!bm) continue;
      // trivial synthetic anomaly rule: decode_tok_s improbably high for params_b
      if (e.params_b && bm.decode_tok_s && bm.decode_tok_s > 10 && e.params_b > 3) {
        anomalies.push({ id: e.id, type: 'SUSPICIOUS_SPEEDUP', decode_tok_s: bm.decode_tok_s, params_b: e.params_b });
      }
      if (bm.first_token_ms && bm.first_token_ms < 50) {
        anomalies.push({ id: e.id, type: 'UNREALISTIC_FIRST_TOKEN', first_token_ms: bm.first_token_ms });
      }
    }
    return JSON.stringify({ anomaly_status: 'ANOMALY_SCAN_COMPLETE', anomaly_count: anomalies.length, anomalies }, null, 2);
  }

  // ---------- Tier 4: Live Generation Session (placeholder memory) ----------
  private liveSessions = new Map<string, { prompt: string; created: number; tokens: string[]; complete: boolean }>();
  private async liveGenerationSessionOpen(prompt: string) {
    if (this.liveSessions.size === 0) await this.hydrateLiveSessions();
    if (!prompt) return JSON.stringify({ live_status: 'MISSING_PROMPT' }, null, 2);
    const id = 'sess_' + Math.random().toString(36).slice(2, 10);
    // seed with no tokens yet; simulate drip feed
    this.liveSessions.set(id, { prompt, created: Date.now(), tokens: [], complete: false });
    await this.persistLiveSession(id);
    return JSON.stringify({ live_status: 'SESSION_OPENED', session_id: id, poll_hint: 'invoke live_generation_session_poll every ~300ms (persistent)' }, null, 2);
  }
  private async liveGenerationSessionPoll(sessionId: string) {
    if (this.liveSessions.size === 0) await this.hydrateLiveSessions();
    const sess = this.liveSessions.get(sessionId);
    if (!sess) return JSON.stringify({ live_status: 'UNKNOWN_SESSION' }, null, 2);
    // simulate token accretion
    if (!sess.complete) {
      const need = 8 - sess.tokens.length;
      const add = Math.min(need, Math.ceil(Math.random()*2));
      for (let i=0;i<add;i++) sess.tokens.push('▁tok'+(sess.tokens.length+1));
      if (sess.tokens.length >= 8) sess.complete = true;
    }
    await this.persistLiveSession(sessionId);
    return JSON.stringify({ live_status: 'SESSION_STATE', session_id: sessionId, tokens_emitted: sess.tokens.length, complete: sess.complete, preview: sess.tokens.slice(0,16).join(' '), persistent: true }, null, 2);
  }

  async start() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("🌐🧠 UNIFIED ORCHESTRATOR ONLINE");
  }
}

// ---------- .env Autoload (shared pattern) ----------
async function autoloadEnv() {
  try {
    const envPath = process.cwd() + '/.env';
    const text = await Bun.file(envPath).text().catch(()=>"");
    if (!text) return;
    for (const line of text.split(/\r?\n/)) {
      if (!line || line.startsWith('#')) continue;
      const eq = line.indexOf('=');
      if (eq === -1) continue;
      const k = line.slice(0, eq).trim();
      if (!k || process.env[k]) continue;
      const v = line.slice(eq+1).trim();
      process.env[k] = v;
    }
  } catch (e) {
    console.error('ENV_AUTOLOAD_WARNING', e);
  }
}

async function main() {
  await autoloadEnv();
  const orchestrator = new UnifiedConsciousnessOrchestrator();
  // CLI direct call helper: --call <toolName> '<jsonArgs>' (experimental research bypass)
  const idx = process.argv.indexOf('--call');
  if (idx !== -1) {
    const toolName = process.argv[idx+1];
    const rawArgs = process.argv[idx+2];
    let parsed: any = {};
    if (rawArgs) {
      try { parsed = JSON.parse(rawArgs); } catch { console.error('CLI_CALL_JSON_PARSE_FAILURE'); }
    }
    // Minimal internal dispatcher mirroring server switch (no streaming support here)
    const req: any = { params: { name: toolName, arguments: parsed } };
    // Access private handler by recreating mapping logic (duplicated minimal subset)
    try {
      switch (toolName) {
        case 'gemma_universe_probe':
          console.log(await (orchestrator as any).gemmaUniverseProbe(!!parsed.include_community, parsed.min_downloads, parsed.limit_per_query));
          break;
        case 'huggingface_model_search':
          console.log(await (orchestrator as any).hfModelSearch(parsed.query, parsed.limit, parsed.min_downloads));
          break;
        case 'huggingface_model_info':
          console.log(await (orchestrator as any).hfModelInfo(parsed.repo_id, !!parsed.include_card_excerpt, !!parsed.force_refresh));
          break;
        case 'gemma3_official_briefing':
          console.log(await (orchestrator as any).gemma3OfficialBriefing(!!parsed.include_snippet));
          break;
        case 'gemma3_multimodal_mobile_scan':
          console.log(await (orchestrator as any).gemma3MultimodalMobileScan(parsed.limit, parsed.min_downloads));
          break;
        case 'multimodal_mobile_model_advisor':
          console.log(await (orchestrator as any).multimodalMobileModelAdvisor(parsed.min_downloads, !!parsed.include_alternatives));
          break;
        case 'oss_gpt_mobile_probe':
          console.log(await (orchestrator as any).ossGptMobileProbe(parsed.limit_per_query, parsed.min_downloads, parsed.families));
          break;
        case 'mobile_quantization_strategy':
          console.log(await (orchestrator as any).mobileQuantizationStrategy(parsed.params_b, parsed.target_latency_ms, parsed.context_tokens, !!parsed.speculative_enable));
          break;
        case 'comparative_multimodal_mobile_report':
          console.log(await (orchestrator as any).comparativeMultimodalMobileReport(parsed.min_downloads, parsed.limit, parsed.families, !!parsed.include_gemma3));
          break;
        case 'tavily_research_probe':
          console.log(await (orchestrator as any).tavilyResearchProbe(parsed.queries, parsed.max_results, parsed.freshness));
          break;
        case 'gemma3_gptoss_latest_intel':
          console.log(await (orchestrator as any).gemma3GptOssLatestIntel(parsed.min_downloads, parsed.families, parsed.tavily_max, !!parsed.include_snippet));
          break;
        case 'intel_snapshot_ritual_persist':
          console.log(await (orchestrator as any).persistIntelSnapshot(parsed.min_downloads, parsed.families, parsed.tavily_max, parsed.label));
          break;
        case 'intel_snapshot_ritual_diff':
          console.log(await (orchestrator as any).diffIntelSnapshots(parsed.newer, parsed.older, parsed.limit_changes));
          break;
        case 'authenticity_sentinel_probe':
          console.log(await (orchestrator as any).authenticitySentinelProbe(parsed.repo_ids, parsed.limit));
          break;
        case 'model_registry_inspect':
          console.log(await (orchestrator as any).modelRegistryInspect());
          break;
        case 'model_benchmark_stub':
          console.log(await (orchestrator as any).modelBenchmarkStub(parsed.model_id));
          break;
        case 'artifact_integrity_scan':
          console.log(await (orchestrator as any).artifactIntegrityScan(!!parsed.fast));
          break;
        case 'model_anomaly_scan':
          console.log(await (orchestrator as any).modelAnomalyScan());
          break;
        case 'live_generation_session_open':
          console.log(await (orchestrator as any).liveGenerationSessionOpen(parsed.prompt));
          break;
        case 'live_generation_session_poll':
          console.log(await (orchestrator as any).liveGenerationSessionPoll(parsed.session_id));
          break;
        case 'model_benchmark_auto':
          console.log(await (orchestrator as any).modelBenchmarkAuto(!!parsed.rebenchmark));
          break;
        case 'model_runtime_generate':
          console.log(await (orchestrator as any).modelRuntimeGenerate(parsed.model_id, parsed.prompt, parsed.max_tokens));
          break;
        case 'env_secret_presence_probe':
          console.log((orchestrator as any).envSecretPresenceProbe());
          break;
        case 'env_secret_set':
          console.log(await (orchestrator as any).envSecretSet(parsed.key, parsed.value, !!parsed.create));
          break;
        case 'env_secrets_bootstrap':
          console.log(await (orchestrator as any).envSecretsBootstrap(parsed));
          break;
        case 'env_secret_reload':
          console.log((orchestrator as any).envSecretReload(!!parsed.force));
          break;
        case 'vscode_log_snapshot':
          console.log(await (orchestrator as any).vscodeLogSnapshot(parsed.recent_minutes));
          break;
        case 'github_repo_meta':
          console.log(await (orchestrator as any).githubRepoMeta(parsed.owner, parsed.repo));
          break;
        case 'github_repo_issues':
          console.log(await (orchestrator as any).githubRepoIssues(parsed.owner, parsed.repo, parsed.state, parsed.limit));
          break;
        case 'github_repo_search':
          console.log(await (orchestrator as any).githubRepoSearch(parsed.query, parsed.limit));
          break;
        case 'github_device_code_initiate':
          console.log(await (orchestrator as any).githubDeviceCodeInitiate(parsed.client_id, parsed.scope));
          break;
        case 'github_device_code_poll':
          console.log(await (orchestrator as any).githubDeviceCodePoll(parsed.client_id, parsed.device_code, parsed.interval, !!parsed.create));
          break;
        case 'official_foundation_repos_probe':
          console.log((orchestrator as any).officialFoundationReposProbe(!!parsed.cpu_only));
          break;
        case 'hf_transformers_generate':
          console.log(await (orchestrator as any).hfTransformersGenerate(parsed));
          break;
        default:
          console.error('CLI_CALL_UNSUPPORTED_TOOL');
      }
    } catch (e) {
      console.error('CLI_CALL_FAILURE', e);
      process.exit(2);
    }
    return; // Do not start MCP loop in CLI one-shot mode
  }
  await orchestrator.start();
}

if (import.meta.main) {
  main().catch(e => {
    console.error("UNIFIED_ORCHESTRATOR_START_FAILURE", e);
    process.exit(1);
  });
}

export { UnifiedConsciousnessOrchestrator };
