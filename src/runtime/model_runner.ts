// 🧬 MODEL RUNNER INTERFACE RITUAL (Tier 0)
// Psycho‑Noir Contract: Stable abstraction before summoning real inference engines.

export type NoirModality = 'text' | 'vision' | 'audio';

export interface NoirGenerationCommon {
  maxTokens?: number;
  temperature?: number;
  topK?: number;
  topP?: number;
  stream?: boolean;
  seed?: number;
}

export interface NoirTextGenerationRequest extends NoirGenerationCommon {
  prompt: string;
}

export interface NoirMultimodalGenerationRequest extends NoirGenerationCommon {
  text?: string;
  images?: Array<Uint8Array | string>; // raw bytes or URI/path placeholders
  // future: audio, video frames
}

export interface NoirTokenChunk {
  token: string;
  index: number;
  done?: boolean;
}

export interface NoirGenerationResult {
  text: string;
  tokens?: number;
  firstTokenLatencyMs?: number;
  totalLatencyMs?: number;
  tokensPerSecond?: number;
  modality?: string;
  meta?: Record<string, any>;
}

export interface ModelCapabilities {
  id: string;
  family: string;
  params_b: number | null;
  modalities: { text: boolean; vision?: boolean; audio?: boolean };
  quantizations: string[];
  license?: string;
  authenticity_ref?: string | null;
  tokenizer_ref?: string | null;
}

export interface ModelRunner {
  id: string;
  ready: boolean;
  capabilities(): ModelCapabilities;
  init(): Promise<void>;
  supports(modality: NoirModality): boolean;
  generateText(req: NoirTextGenerationRequest, onToken?: (c: NoirTokenChunk) => void): Promise<NoirGenerationResult>;
  generateMultimodal(req: NoirMultimodalGenerationRequest, onToken?: (c: NoirTokenChunk) => void): Promise<NoirGenerationResult>;
  unload(): Promise<void>;
}

export class NotSupportedError extends Error {
  constructor(message: string) { super(message); this.name = 'NotSupportedError'; }
}

export class ModelNotReadyError extends Error {
  constructor(message: string) { super(message); this.name = 'ModelNotReadyError'; }
}

// Base skeleton helper for simple runners
export abstract class AbstractModelRunner implements ModelRunner {
  public id: string;
  public ready = false;
  protected _caps: ModelCapabilities;

  constructor(caps: ModelCapabilities) {
    this.id = caps.id;
    this._caps = caps;
  }
  capabilities() { return this._caps; }
  supports(modality: NoirModality): boolean { return !!(this._caps.modalities as any)[modality]; }
  async init(): Promise<void> { this.ready = true; }
  async unload(): Promise<void> { this.ready = false; }
  protected ensureReady() { if (!this.ready) throw new ModelNotReadyError(`MODEL_NOT_READY: ${this.id}`); }
  abstract generateText(req: NoirTextGenerationRequest, onToken?: (c: NoirTokenChunk) => void): Promise<NoirGenerationResult>;
  abstract generateMultimodal(req: NoirMultimodalGenerationRequest, onToken?: (c: NoirTokenChunk) => void): Promise<NoirGenerationResult>;
}
