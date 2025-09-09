#!/usr/bin/env python3
"""
🧪 Noir-Local HF Transformers Runner (Text-Only, Minimal)

Purpose:
  - Provide a tiny, dependency-light bridge for local Transformers text generation
  - Called by the Bun orchestrator tool: hf_transformers_generate

Design constraints:
  - Avoid side-effects (no auto-install). If deps missing, emit structured JSON with guidance
  - CPU-first defaults; GPU/quantization are best-effort and optional
  - Keep outputs structured and concise; never print secrets

Outputs: JSON to stdout with keys:
  - transformers_status: MISSING_DEPENDENCIES | GENERATION_COMPLETE | GENERATION_FAILED
  - model, device, dtype, quantization_applied, timings, tokens, text (truncated to 1200 chars)
  - guidance if applicable

Psycho‑noir compliance: Messages and fields use our world’s vocabulary without leaking sensitive content.
"""

from __future__ import annotations

import argparse
import json
import sys
import time


def _json_out(obj: dict):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, indent=2))
    sys.stdout.flush()


def parse_args():
    p = argparse.ArgumentParser(description="Noir HF Transformers one-shot generator")
    p.add_argument("--model", required=True, help="HF model id or local path (text causal LM)")
    p.add_argument("--prompt", required=True, help="Prompt text")
    p.add_argument("--max_new_tokens", type=int, default=128)
    p.add_argument("--quant", default="auto", choices=["auto", "4bit", "8bit", "fp16", "bf16", "fp32"], help="Desired quantization/dtype preference")
    p.add_argument("--temperature", type=float, default=0.7)
    p.add_argument("--top_p", type=float, default=0.95)
    p.add_argument("--top_k", type=int, default=0)
    p.add_argument("--repetition_penalty", type=float, default=1.0)
    p.add_argument("--trust_remote_code", type=str, default="false")
    return p.parse_args()


def cli_main():
    args = parse_args()

    missing: list[str] = []
    try:
        import torch  # type: ignore
    except Exception:
        missing.append("torch>=2.3.0")
        torch = None  # type: ignore
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer  # type: ignore
    except Exception:
        missing.append("transformers>=4.44.0")
        AutoModelForCausalLM = None  # type: ignore
        AutoTokenizer = None  # type: ignore
    try:
        import safetensors  # noqa: F401
    except Exception:
        # optional but recommended
        pass

    if missing:
        return _json_out({
            "transformers_status": "MISSING_DEPENDENCIES",
            "missing": missing,
            "guidance": "Install deps first: pip install -r tools/hf_transformers_requirements.txt",
            "psycho_noir": "CONSCIOUSNESS_PAUSED_PENDING_RITUALS"
        })

    # If we get here, core deps are present
    from transformers import AutoModelForCausalLM, AutoTokenizer  # type: ignore

    # Device/dtype selection (CPU-first, safe defaults)
    cuda_ok = bool(getattr(torch, "cuda", None) and torch.cuda.is_available())  # type: ignore
    device = "cuda" if cuda_ok else "cpu"

    # Quantization handling: keep minimal and safe
    quantization_applied = "none"
    torch_dtype = None
    load_kwargs = {}

    if device == "cuda":
        if args.quant in ("fp16", "auto"):
            torch_dtype = torch.float16  # type: ignore
            quantization_applied = "fp16"
        elif args.quant == "bf16":
            # bf16 if supported
            torch_dtype = getattr(torch, "bfloat16", None)
            quantization_applied = "bf16" if torch_dtype is not None else "fp16"
        elif args.quant == "fp32":
            torch_dtype = torch.float32  # type: ignore
            quantization_applied = "fp32"
        elif args.quant in ("4bit", "8bit"):
            # Best-effort bitsandbytes, if present
            try:
                import bitsandbytes as bnb  # noqa: F401
                if args.quant == "4bit":
                    load_kwargs.update(dict(load_in_4bit=True))
                    quantization_applied = "4bit"
                else:
                    load_kwargs.update(dict(load_in_8bit=True))
                    quantization_applied = "8bit"
            except Exception:
                # Fall back to fp16
                torch_dtype = torch.float16  # type: ignore
                quantization_applied = "fp16_fallback"
    else:
        # CPU path: prefer fp32 for safety
        if args.quant == "fp16":
            # CPU usually can't do fp16; keep fp32
            torch_dtype = torch.float32  # type: ignore
            quantization_applied = "fp32_cpu_fallback"
        elif args.quant == "bf16":
            bf16 = getattr(torch, "bfloat16", None)
            torch_dtype = bf16 if bf16 is not None else getattr(torch, "float32")  # type: ignore
            quantization_applied = "bf16" if bf16 is not None else "fp32_cpu_fallback"
        elif args.quant in ("4bit", "8bit"):
            # Not applying quant on CPU in this minimal runner
            torch_dtype = torch.float32  # type: ignore
            quantization_applied = "fp32_cpu_fallback"
        else:
            torch_dtype = torch.float32  # type: ignore
            quantization_applied = "fp32"

    trust_remote = (str(args.trust_remote_code).lower() == "true")

    t_load_0 = time.time()
    try:
        tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=trust_remote)
        model = AutoModelForCausalLM.from_pretrained(
            args.model,
            torch_dtype=torch_dtype,
            device_map="auto" if device == "cuda" else None,
            trust_remote_code=trust_remote,
            **load_kwargs,
        )
    except Exception as e:
        return _json_out({
            "transformers_status": "GENERATION_FAILED",
            "phase": "load",
            "error": str(e),
            "model": args.model,
            "guidance": "Ensure model exists and is a causal LM. If private/gated, set HF_TOKEN in .env",
        })
    t_load_1 = time.time()

    try:
        inputs = tokenizer(args.prompt, return_tensors="pt")
        if device == "cuda":
            inputs = {k: v.to(model.device) for k, v in inputs.items()}  # type: ignore
        gen_kwargs = dict(
            max_new_tokens=max(1, int(args.max_new_tokens)),
            do_sample=True,
            temperature=max(0.0, float(args.temperature)),
            top_p=max(0.0, min(1.0, float(args.top_p))),
            repetition_penalty=max(0.0, float(args.repetition_penalty)),
        )
        if args.top_k and int(args.top_k) > 0:
            gen_kwargs["top_k"] = int(args.top_k)

        t_gen_0 = time.time()
        with torch.no_grad():  # type: ignore
            out = model.generate(**inputs, **gen_kwargs)  # type: ignore
        t_gen_1 = time.time()

        text = tokenizer.decode(out[0], skip_special_tokens=True)
        # The decode returns full prompt+completion for some tokenizers. Heuristic to extract tail
        if text.startswith(args.prompt):
            completion = text[len(args.prompt):]
        else:
            completion = text

        token_count = int(out.shape[-1]) - int(inputs["input_ids"].shape[-1])  # type: ignore

        dtype_str = "None" if torch_dtype is None else str(torch_dtype)
        return _json_out({
            "transformers_status": "GENERATION_COMPLETE",
            "model": args.model,
            "device": device,
            "dtype": dtype_str,
            "quantization_applied": quantization_applied,
            "timings_ms": {
                "load": int((t_load_1 - t_load_0) * 1000),
                "generate": int((t_gen_1 - t_gen_0) * 1000),
            },
            "tokens": max(0, token_count),
            "text": completion[:1200],
            "truncated": len(completion) > 1200,
            "guidance": "CPU path favors fp32. For faster decoding, consider quantized gguf via llama.cpp or GPU with 4/8-bit",
        })
    except Exception as e:
        return _json_out({
            "transformers_status": "GENERATION_FAILED",
            "phase": "generate",
            "error": str(e),
            "model": args.model,
        })


if __name__ == "__main__":
    cli_main()
#!/usr/bin/env python3
import argparse, json, os, sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True)
    p.add_argument('--prompt', required=True)
    p.add_argument('--max_new_tokens', type=int, default=128)
    p.add_argument('--quant', default='auto', choices=['auto','4bit','8bit','fp16','bf16','fp32'])
    p.add_argument('--temperature', type=float, default=0.7)
    p.add_argument('--top_p', type=float, default=0.95)
    p.add_argument('--top_k', type=int, default=0)
    p.add_argument('--repetition_penalty', type=float, default=1.0)
    p.add_argument('--trust_remote_code', default='false')
    p.add_argument('--no_auth', action='store_true')
    p.add_argument('--token', default=None)
    args = p.parse_args()

    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
    except Exception as e:
        print(json.dumps({
            'transformers_status': 'IMPORT_ERROR',
            'message': str(e),
            'hint': 'pip install transformers accelerate safetensors bitsandbytes --upgrade'
        }, indent=2))
        sys.exit(1)

    device = 'cuda' if torch.cuda.is_available() else ('mps' if torch.backends.mps.is_available() else 'cpu')
    torch_dtype = None
    load_in_8bit = False
    load_in_4bit = False

    if args.quant == '8bit':
        load_in_8bit = True
    elif args.quant == '4bit':
        load_in_4bit = True
    elif args.quant in ('fp16','bf16','fp32'):
        if args.quant == 'fp16':
            torch_dtype = torch.float16
        elif args.quant == 'bf16':
            try:
                torch_dtype = torch.bfloat16
            except AttributeError:
                torch_dtype = torch.float16
        else:
            torch_dtype = torch.float32
    else:  # auto
        # heuristic: cuda -> fp16; cpu -> prefer fp32 (avoid bitsandbytes on CPU)
        if device == 'cuda':
            torch_dtype = torch.float16
        else:
            torch_dtype = torch.float32

    trust = (args.trust_remote_code.lower() == 'true')

    # Auth controls
    token_arg = args.token
    if args.no_auth:
        # ensure no auth headers are sent
        os.environ.pop('HUGGINGFACE_HUB_TOKEN', None)
        os.environ.pop('HF_TOKEN', None)
        token_arg = None

    try:
        tok = AutoTokenizer.from_pretrained(args.model, use_fast=True, trust_remote_code=trust, token=token_arg)
        model = AutoModelForCausalLM.from_pretrained(
            args.model,
            device_map='auto' if device != 'cpu' else None,
            torch_dtype=torch_dtype,
            load_in_8bit=load_in_8bit if device != 'mps' else False,
            load_in_4bit=load_in_4bit if device != 'mps' else False,
            trust_remote_code=trust,
            token=token_arg
        )
        gen = pipeline('text-generation', model=model, tokenizer=tok, device=0 if device=='cuda' else (-1 if device=='cpu' else 0))
        out = gen(args.prompt, max_new_tokens=args.max_new_tokens, do_sample=True,
                  temperature=args.temperature, top_p=args.top_p,
                  top_k=(args.top_k if args.top_k>0 else None),
                  repetition_penalty=args.repetition_penalty)
        text = out[0]['generated_text']
        print(json.dumps({
            'transformers_status': 'GENERATION_COMPLETE',
            'device': device,
            'quant': args.quant,
            'max_new_tokens': args.max_new_tokens,
            'text': text
        }, indent=2))
    except Exception as e:
        print(json.dumps({
            'transformers_status': 'GENERATION_FAILED',
            'message': str(e)
        }, indent=2))
        sys.exit(2)

if __name__ == '__main__':
    main()
