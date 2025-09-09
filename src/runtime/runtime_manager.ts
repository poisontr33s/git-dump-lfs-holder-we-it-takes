// 🧠 RUNTIME MANAGER (Tier 1 orchestration layer)
// Centralizes lazy loading and caching of concrete ModelRunner instances.

import { promises as fs } from "fs";
import { LlamaCppHTTPRunner } from "../../llm/runners/llama_cpp_http_runner.js";
import { ModelRunner } from "./model_runner.js";

export interface RegistryModelEntry {
  id: string;
  backend?: string; // e.g. "llama.cpp-http" | "synthetic"
  params_b?: number;
  artifacts?: { primary?: string };
  modalities?: { text?: boolean; vision?: boolean };
  serving?: { endpoint?: string };
  quantizations?: string[];
}

export class RuntimeManager {
  private runners = new Map<string, ModelRunner>();
  private registry: RegistryModelEntry[] = [];
  private registryPath: string;

  constructor(registryPath = 'model_registry.json') {
    this.registryPath = registryPath;
  }

  async loadRegistry() {
    try {
      const raw = await fs.readFile(this.registryPath,'utf-8');
      const arr = JSON.parse(raw);
      if (Array.isArray(arr)) this.registry = arr; else this.registry = [];
    } catch { this.registry = []; }
  }

  getEntry(id: string) { return this.registry.find(r => r.id === id); }

  async getRunner(id: string): Promise<ModelRunner | null> {
    if (this.runners.has(id)) return this.runners.get(id)!;
    if (!this.registry.length) await this.loadRegistry();
    const entry = this.getEntry(id);
    if (!entry) return null;
    const backend = entry.backend || 'synthetic';
    let runner: ModelRunner | null = null;
    if (backend === 'llama.cpp-http') {
      const endpoint = entry.serving?.endpoint || 'http://127.0.0.1:8080';
      runner = new LlamaCppHTTPRunner({ modelId: entry.id, params_b: entry.params_b || null, baseUrl: endpoint, quantization: entry.quantizations?.[0] });
    }
    if (!runner) return null; // unsupported backend yet
    await runner.init().catch(()=>{});
    if (runner.ready) {
      this.runners.set(id, runner);
      return runner;
    }
    return null;
  }
}

export default RuntimeManager;
