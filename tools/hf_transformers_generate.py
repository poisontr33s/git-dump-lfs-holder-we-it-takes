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
        # simple heuristic: cpu -> try 4bit; cuda -> fp16
        if device == 'cpu':
            load_in_4bit = True
        elif device == 'cuda':
            torch_dtype = torch.float16

    trust = (args.trust_remote_code.lower() == 'true')

    try:
        tok = AutoTokenizer.from_pretrained(args.model, use_fast=True, trust_remote_code=trust)
        model = AutoModelForCausalLM.from_pretrained(
            args.model,
            device_map='auto' if device != 'cpu' else None,
            torch_dtype=torch_dtype,
            load_in_8bit=load_in_8bit if device != 'mps' else False,
            load_in_4bit=load_in_4bit if device != 'mps' else False,
            trust_remote_code=trust
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
