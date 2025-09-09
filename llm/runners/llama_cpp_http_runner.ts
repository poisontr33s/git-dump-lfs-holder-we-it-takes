// 🦙 REAL LLAMA.CPP HTTP RUNNER (Tier 1 activation)
// Bridges to a running llama.cpp server (started externally with --server --port <port> --host 127.0.0.1)
// Provides streaming + latency metrics; falls back gracefully if server unreachable.

import { AbstractModelRunner, NoirGenerationResult, NoirMultimodalGenerationRequest, NoirTextGenerationRequest, NoirTokenChunk } from "../../src/runtime/model_runner.js";

interface LlamaCppHTTPRunnerOptions {
  baseUrl?: string; // e.g. http://127.0.0.1:8080
  modelId: string;
  params_b: number | null;
  quantization?: string;
  timeoutMs?: number;
}

interface LlamaCppServerResponseToken {
  content: string;
  stop: boolean;
}

export class LlamaCppHTTPRunner extends AbstractModelRunner {
  private baseUrl: string;
  private timeoutMs: number;
  constructor(opts: LlamaCppHTTPRunnerOptions) {
    super({
      id: opts.modelId,
      family: 'llama.cpp',
      params_b: opts.params_b,
      modalities: { text: true },
      quantizations: [opts.quantization || 'unknown'],
      license: undefined,
      authenticity_ref: null,
      tokenizer_ref: null
    });
    this.baseUrl = opts.baseUrl || 'http://127.0.0.1:8080';
    this.timeoutMs = opts.timeoutMs || 60000;
  }
  async init() {
    // Probe server /health or root (llama.cpp uses / for simple status sometimes)
    try {
      const ctl = new AbortController();
      const t = setTimeout(()=> ctl.abort(), 2500);
      const resp = await fetch(this.baseUrl + '/health', { signal: ctl.signal }).catch(()=> fetch(this.baseUrl + '/', { signal: ctl.signal }));
      clearTimeout(t);
      if (resp && resp.ok) this.ready = true; else this.ready = false;
    } catch { this.ready = false; }
  }

  private async *streamTokens(prompt: string, maxTokens: number | undefined) : AsyncGenerator<LlamaCppServerResponseToken, void, unknown> {
    const body = JSON.stringify({ prompt, n_predict: maxTokens || 128, stream: true });
    const resp = await fetch(this.baseUrl + '/completion', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body });
    if (!resp.ok || !resp.body) throw new Error('LLAMACPP_STREAM_FAILURE');
    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      // llama.cpp server streams lines like: {"content":"...","stop":false}\n
      let idx;
      while ((idx = buffer.indexOf('\n')) !== -1) {
        const line = buffer.slice(0, idx).trim();
        buffer = buffer.slice(idx + 1);
        if (!line) continue;
        try {
          const parsed = JSON.parse(line);
          if (typeof parsed.content === 'string') {
            yield { content: parsed.content, stop: !!parsed.stop };
            if (parsed.stop) return;
          }
        } catch { /* swallow parse errors */ }
      }
    }
  }

  async generateText(req: NoirTextGenerationRequest, onToken?: (c: NoirTokenChunk) => void): Promise<NoirGenerationResult> {
    this.ensureReady();
    const t0 = performance.now();
    let firstTokenAt: number | undefined;
    let full = '';
    let index = 0;
    try {
      for await (const tk of this.streamTokens(req.prompt, req.maxTokens)) {
        if (firstTokenAt === undefined) firstTokenAt = performance.now();
        full += tk.content;
        if (onToken) onToken({ token: tk.content, index, done: tk.stop });
        index++;
      }
    } catch (e) {
      return { text: full, tokens: index, modality: 'text', meta: { error: String(e) } };
    }
    const end = performance.now();
    return {
      text: full,
      tokens: index,
      modality: 'text',
      firstTokenLatencyMs: firstTokenAt ? +(firstTokenAt - t0).toFixed(2) : undefined,
      totalLatencyMs: +(end - t0).toFixed(2),
      tokensPerSecond: index > 1 && firstTokenAt ? +((index-1)/((end - firstTokenAt)/1000)).toFixed(2) : undefined,
      meta: { backend: 'llama.cpp', baseUrl: this.baseUrl }
    };
  }

  async generateMultimodal(_req: NoirMultimodalGenerationRequest): Promise<NoirGenerationResult> {
    throw new Error('LLAMACPP_HTTP_RUNNER_MULTIMODAL_UNSUPPORTED');
  }
}

export default LlamaCppHTTPRunner;
