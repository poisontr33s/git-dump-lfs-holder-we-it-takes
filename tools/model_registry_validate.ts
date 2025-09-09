#!/usr/bin/env bun
// 🔍 MODEL REGISTRY VALIDATION RITUAL
// Ensures registry entries conform to expected schema; emits psycho‑noir diagnostics.

import { promises as fs } from 'fs';

interface RegistryEntry {
  id: string; family: string; params_b: number | null; modalities: any; quantizations: string[];
  artifacts: any; license?: string; authenticity_ref?: string | null; tokenizer_ref?: string | null; last_benchmark?: any;
}

function validateEntry(e: any, i: number, errors: string[]) {
  function req(cond: boolean, msg: string) { if (!cond) errors.push(`ENTRY_${i}::${e.id || 'UNKNOWN'} => ${msg}`); }
  req(typeof e.id === 'string' && e.id.length > 3, 'INVALID_ID');
  req(typeof e.family === 'string', 'MISSING_FAMILY');
  req(e.params_b === null || typeof e.params_b === 'number', 'BAD_params_b');
  req(e.modalities && typeof e.modalities === 'object', 'MISSING_MODALITIES');
  req(Array.isArray(e.quantizations), 'MISSING_QUANTIZATIONS');
  req(e.artifacts && typeof e.artifacts === 'object', 'MISSING_ARTIFACTS');
}

async function main() {
  const raw = await fs.readFile('model_registry.json','utf-8').catch(()=>null);
  if (!raw) { console.error('REGISTRY_ABSENT'); process.exit(2); }
  let parsed: RegistryEntry[] = [];
  try { parsed = JSON.parse(raw); } catch { console.error('JSON_PARSE_FAILURE'); process.exit(2); }
  if (!Array.isArray(parsed)) { console.error('REGISTRY_NOT_ARRAY'); process.exit(2); }
  const errors: string[] = [];
  parsed.forEach((e,i)=> validateEntry(e,i,errors));
  if (errors.length) {
    console.error(JSON.stringify({ validation_status: 'REGISTRY_INVALID', error_count: errors.length, errors }, null, 2));
    process.exit(1);
  }
  console.log(JSON.stringify({ validation_status: 'REGISTRY_HEALTHY', entries: parsed.length }, null, 2));
}

main().catch(e => { console.error('VALIDATION_RITUAL_FAILURE', e); process.exit(3); });
