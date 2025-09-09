// 🧪 DUMMY TRANSFORMERS BRIDGE RUNNER (Tier 0 placeholder)
// Intended future: spawn python subprocess hosting HF transformers for models not supported by local C++ backend.

import { AbstractModelRunner, NoirGenerationResult, NoirMultimodalGenerationRequest, NoirTextGenerationRequest, NotSupportedError } from "../../src/runtime/model_runner.js";

export class DummyTransformersBridgeRunner extends AbstractModelRunner {
  constructor(id: string, family: string, paramsB: number | null, modalities: { text: boolean; vision?: boolean }) {
    super({ id, family, params_b: paramsB, modalities, quantizations: ['fp16'], license: 'apache-2.0', authenticity_ref: null, tokenizer_ref: null });
  }
  async init() {
    await Bun.sleep(20);
    this.ready = true;
  }
  async generateText(req: NoirTextGenerationRequest): Promise<NoirGenerationResult> {
    this.ensureReady();
    return {
      text: `[DUMMY_TRANSFORMERS:${this.capabilities().id}] SUBPROCESS_BRIDGE_NOT_ATTACHED prompt='${req.prompt.slice(0,60)}'...`,
      tokens: 0,
      modality: 'text'
    };
  }
  async generateMultimodal(_req: NoirMultimodalGenerationRequest): Promise<NoirGenerationResult> {
    throw new NotSupportedError('DUMMY_BRIDGE_MULTIMODAL_NOT_WIRED');
  }
}

export default DummyTransformersBridgeRunner;
