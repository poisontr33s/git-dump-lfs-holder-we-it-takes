// 🦙 DUMMY LLAMA.CPP RUNNER (Tier 0 placeholder)
// Emits NOT_IMPLEMENTED for real inference; used to validate orchestration plumbing.

import { AbstractModelRunner, NoirGenerationResult, NoirMultimodalGenerationRequest, NoirTextGenerationRequest, NotSupportedError } from "../../src/runtime/model_runner.js";

export class DummyLlamaCppRunner extends AbstractModelRunner {
  constructor(id: string, paramsB: number | null, modalities: { text: boolean; vision?: boolean }) {
    super({ id, family: 'llama', params_b: paramsB, modalities, quantizations: ['q4_k_m'], license: 'apache-2.0', authenticity_ref: null, tokenizer_ref: null });
  }
  async init() {
    // Simulate setup latency
    await Bun.sleep(30);
    this.ready = true;
  }
  async generateText(req: NoirTextGenerationRequest): Promise<NoirGenerationResult> {
    this.ensureReady();
    return {
      text: `[DUMMY_LLAMA_CPP:${this.id}] TOKEN_STREAM_NOT_WIRED: prompt='${req.prompt.slice(0,60)}'...`,
      tokens: 0,
      modality: 'text'
    };
  }
  async generateMultimodal(_req: NoirMultimodalGenerationRequest): Promise<NoirGenerationResult> {
    throw new NotSupportedError('MULTIMODAL_NOT_SUPPORTED_IN_DUMMY_LLAMA_CPP_RUNNER');
  }
}

export default DummyLlamaCppRunner;
