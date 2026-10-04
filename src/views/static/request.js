import {state, beginRead, currentRead, adoptConfiguration, getDraft} from './state.js';

export class RequestError extends Error {
  constructor(key, details = {}, unknown = false) { super(key); this.key = key; this.details = details; this.unknown = unknown; }
}
let configSequence = 0;
const pendingWrites = new Set();
async function transport(path, options = {}) {
  let response;
  try { response = await fetch(path, {cache: 'no-store', ...options}); }
  catch { throw new RequestError('network', {}, true); }
  let body;
  try {
    if (path === '/' && response.ok) {
      const document = new DOMParser().parseFromString(await response.text(), 'text/html');
      body = JSON.parse(document.querySelector('#bootstrap').textContent);
    } else body = await response.json();
  }
  catch { throw new RequestError('network', {}, true); }
  if (!response.ok) throw new RequestError(body.message_key || 'network', body);
  return body;
}
export async function upload(file, workflow) {
  const config = await configuration();
  if (!config) throw new RequestError('network');
  const form = new FormData(); form.append('file', file); form.append('workflow', workflow);
  return transport('/api/imports/preview', {method: 'POST', body: form});
}
export async function configuration() {
  const sequence = ++configSequence;
  const config = await transport('/api/config');
  if (sequence !== configSequence) return null;
  if (state.context) adoptConfiguration(config);
  return config;
}
export async function read(path, key, accept, reject) {
  const token = beginRead(key);
  try {
    const config = await configuration();
    if (!config || !currentRead(token)) return;
    const result = await transport(path);
    if (currentRead(token) && result.generation_id === state.generation) accept(result);
    else if (currentRead(token)) await configuration();
  } catch (error) { if (currentRead(token)) reject(error); }
}
export async function write(path, payload, {method = 'POST', draftKey = null} = {}) {
  if (pendingWrites.has(path)) throw new RequestError('saving');
  pendingWrites.add(path);
  try {
    const config = await configuration();
    if (!config) throw new RequestError('network');
    const draft = draftKey ? getDraft(draftKey) : null;
    if (payload.generation_id !== config.generation_id || (draftKey && (!draft || draft.invalid)))
      throw new RequestError('errors.stale_store');
    return await transport(path, {method, headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)});
  } finally { pendingWrites.delete(path); }
}
