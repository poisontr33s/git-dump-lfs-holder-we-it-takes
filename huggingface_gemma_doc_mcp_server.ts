#!/usr/bin/env bun
/**
 * 🛰️🔮 HUGGINGFACE + GEMMA MOBILE DOCUMENT ORACLE (BUN MCP SERVER)
 * Purpose: Provide psycho‑noir aligned tooling to query lightweight Hugging Face model metadata
 *          and surface curated Gemma Mobile reference links WITHOUT needing a VS Code extension
 *          or external MCP repo cloning.
 * Design Tenets:
 *  - Zero extension scaffolding; pure Bun + MCP server
 *  - Respect licensing / avoid raw copyrighted model card dumps (truncate + attribute)
 *  - Caching of HF metadata within process (ephemeral) to reduce network hits
 *  - Forward‑compatible hooks for Google / Gemma official doc enrichment (no scraping)
 *  - Psycho‑noir narrative lexicon retained
 */
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ErrorCode, ListToolsRequestSchema, McpError, type CallToolRequest } from "@modelcontextprotocol/sdk/types.js";

interface HFModelMetaCacheEntry {
  fetchedAt: number; // epoch ms
  data: any;         // raw JSON from HF API
}

class HuggingFaceGemmaOracleServer {
  private server: Server;
  private hfCache: Map<string, HFModelMetaCacheEntry> = new Map();
  private hfTtlMs = 5 * 60 * 1000; // 5 minutes TTL

  constructor() {
    this.server = new Server({ name: "huggingface-gemma-oracle", version: "0.1.0" }, { capabilities: { tools: {} } });
    this.register();
  }

  private tools() {
    return [
      {
        name: "huggingface_model_info",
        description: "Retrieve high-level Hugging Face model metadata (psycho-noir sanitized)",
        inputSchema: {
          type: "object",
          properties: {
            repo_id: { type: "string", description: "huggingface repo id e.g. google/gemma-2b" },
            include_card_excerpt: { type: "boolean" }
          },
          required: ["repo_id"]
        }
      },
      {
        name: "huggingface_model_card_excerpt",
        description: "Truncated sanitized model card excerpt (non-copyright infringing summary)",
        inputSchema: {
          type: "object",
          properties: {
            repo_id: { type: "string" },
            max_chars: { type: "number", minimum: 100, maximum: 4000 }
          },
          required: ["repo_id"]
        }
      },
      {
        name: "gemma_reference_links",
        description: "Curated official Gemma + Gemma Mobile reference constellation (no scraping)",
        inputSchema: { type: "object", properties: { minimal: { type: "boolean" } }, required: [] }
      },
      {
        name: "gemma_mobile_setup_advice",
        description: "Operational guidance for embedding a tiny Gemma variant on-device (original summary)",
        inputSchema: { type: "object", properties: { target_device_class: { type: "string" } }, required: [] }
      },
      {
        name: "google_gemma_search_stub",
        description: "Stub for future Google programmable search API integration (returns NOT_CONFIGURED)",
        inputSchema: { type: "object", properties: { query: { type: "string" } }, required: ["query"] }
      }
    ];
  }

  private register() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: this.tools() }));
    this.server.setRequestHandler(CallToolRequestSchema, async (req: CallToolRequest) => {
      const name = req.params.name;
      const args: any = req.params.arguments || {};
      try {
        switch (name) {
          case "huggingface_model_info":
            return { content: [ { type: "text", text: await this.hfModelInfo(args.repo_id, !!args.include_card_excerpt) } ] };
          case "huggingface_model_card_excerpt":
            return { content: [ { type: "text", text: await this.hfModelCardExcerpt(args.repo_id, args.max_chars) } ] };
          case "gemma_reference_links":
            return { content: [ { type: "text", text: this.gemmaReferenceLinks(!!args.minimal) } ] };
          case "gemma_mobile_setup_advice":
            return { content: [ { type: "text", text: this.gemmaSetupAdvice(args.target_device_class) } ] };
          case "google_gemma_search_stub":
            return { content: [ { type: "text", text: this.googleStub(args.query) } ] };
          default:
            throw new McpError(ErrorCode.MethodNotFound, `UNKNOWN_ORACLE_INSTRUMENT: ${name}`);
        }
      } catch (e) {
        const msg = e instanceof Error ? e.message : String(e);
        throw new McpError(ErrorCode.InternalError, `ORACLE_FAILURE: ${msg}`);
      }
    });
  }

  private async hfFetch(repoId: string): Promise<any> {
    const key = repoId.toLowerCase();
    const cached = this.hfCache.get(key);
    const now = Date.now();
    if (cached && (now - cached.fetchedAt) < this.hfTtlMs) return cached.data;
    const url = `https://huggingface.co/api/models/${encodeURIComponent(repoId)}`;
    const resp = await fetch(url, { headers: { 'Accept': 'application/json' } });
    if (!resp.ok) throw new Error(`HF_API_ERROR ${resp.status}`);
    const json = await resp.json();
    this.hfCache.set(key, { fetchedAt: now, data: json });
    return json;
  }

  private async hfModelInfo(repoId: string, includeCard: boolean): Promise<string> {
    if (!repoId) return "MISSING_REPO_ID";
    const data = await this.hfFetch(repoId);
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
      card_excerpt: includeCard && typeof data.cardData?.license === 'string'
        ? `LICENSE: ${data.cardData.license}`
        : undefined
    };
    return JSON.stringify({ meta_status: "HF_MODEL_META", psycho_noir_resonance: "STABLE", ...sanitized }, null, 2);
  }

  private async hfModelCardExcerpt(repoId: string, maxChars?: number): Promise<string> {
    if (!repoId) return "MISSING_REPO_ID";
    const data = await this.hfFetch(repoId);
    const raw = data.cardData?.model_card || data.cardData?.summary || "(no model card summary)";
    const limit = Math.min(Math.max(maxChars || 800, 100), 4000);
    // Truncate to avoid wholesale reproduction; attribute source.
    const excerpt = raw.slice(0, limit);
    return JSON.stringify({
      card_excerpt_status: "HF_MODEL_CARD_EXCERPT",
      repo: data.id,
      chars: excerpt.length,
      excerpt,
      attribution: "Source: Hugging Face model card (truncated, transformed)"
    }, null, 2);
  }

  private gemmaReferenceLinks(minimal: boolean): string {
    const links = [
      { title: "Gemma Official Landing", url: "https://ai.google.dev/gemma" },
      { title: "Gemma Model Card (Google AI)", url: "https://ai.google.dev/gemma/docs/model_card" },
      { title: "Responsible Usage Guide", url: "https://ai.google.dev/gemma/docs/responsible" },
      { title: "Inference Guide", url: "https://ai.google.dev/gemma/docs/inference" },
      { title: "Quantization Techniques", url: "https://ai.google.dev/gemma/docs/optimization" },
      { title: "Hugging Face Gemma Collection", url: "https://huggingface.co/collections/google/gemma-65d4b5d08d9b4e7f5c3e2b6a" }
    ];
    const selected = minimal ? links.slice(0, 3) : links;
    return JSON.stringify({ reference_status: "GEMMA_REFERENCE_LINKS", minimal, count: selected.length, links: selected }, null, 2);
  }

  private gemmaSetupAdvice(target?: string): string {
    return JSON.stringify({
      advisory_status: "GEMMA_MOBILE_SETUP_ADVICE",
      target_device_class: target || "unspecified",
      phases: [
        "Select quantized variant (Q4_K_M or Q4_0 for 300M–500M edge).",
        "Allocate memory: ensure >= model_size * 1.3 in RAM headroom.",
        "Warm load + verify tokenization parity with reference implementation.",
        "Stream tokens early to maintain interactive latency < 300ms first token.",
        "Apply archetypeBias pre-prompt injection carefully to avoid style collapse.",
        "Future: integrate embedding similarity guard before output for IP safety."
      ],
      caution: "Do not embed full proprietary model card text; reference links only.",
      optimization_hint: "Consider WebGPU path once wasm+SIMD baseline validated."
    }, null, 2);
  }

  private googleStub(query: string): string {
    return JSON.stringify({
      google_search_status: "NOT_CONFIGURED",
      query,
      guidance: "Provide GOOGLE_API_KEY + SEARCH_ENGINE_ID env vars in future enhancement to enable live programmable search.",
      next_step: "Implement fetch to https://www.googleapis.com/customsearch/v1 with sanitized summarization pipeline."
    }, null, 2);
  }

  async start() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("🛰️🔮 HUGGINGFACE + GEMMA ORACLE SERVER OPERATIONAL");
  }
}

async function main() {
  // Minimal .env autoload (shared pattern)
  try {
    const envPath = process.cwd() + '/.env';
    const text = await Bun.file(envPath).text().catch(()=>"");
    if (text) {
      for (const line of text.split(/\r?\n/)) {
        if (!line || line.startsWith('#')) continue;
        const eq = line.indexOf('=');
        if (eq === -1) continue;
        const k = line.slice(0, eq).trim();
        if (!k || process.env[k]) continue;
        const v = line.slice(eq+1).trim();
        process.env[k] = v;
      }
    }
  } catch (e) {
    console.error('ENV_AUTOLOAD_WARNING', e);
  }
  const server = new HuggingFaceGemmaOracleServer();
  await server.start();
}

if (import.meta.main) {
  main().catch(e => {
    console.error("ORACLE_BOOT_FAILURE", e);
    process.exit(1);
  });
}

export { HuggingFaceGemmaOracleServer };
