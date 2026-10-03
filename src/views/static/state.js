// All tab context, drafts, versions and response sequencing belong here.
const listeners = new Set();
const sequences = new Map();
const drafts = new Map();
let epoch = 0;
let channel;
let storageFailed = false;
const sessionKey = 'hotel.context.v1';
const prefix = 'hotel.tab:';
export const routes = ['overview', 'maintenance', 'import', 'assumptions'];
export const state = {
  config: null, generation: null, context: null,
  language: 'en', currency: 'USD', preview: null, counts: null,
};
function storageRead(storage, key) {
  try { return window[storage].getItem(key); } catch { storageFailed = true; return null; }
}
function storageWrite(storage, key, value) {
  try { window[storage].setItem(key, value); } catch { storageFailed = true; }
}
function persist() { storageWrite('sessionStorage', sessionKey, JSON.stringify(state.context)); }
function emit() { listeners.forEach(listener => listener()); }
export function subscribe(listener) { listeners.add(listener); return () => listeners.delete(listener); }
export function hasStorageFailure() { return storageFailed; }
export function validDate(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value) || value.startsWith('0000')) return false;
  const date = new Date(`${value}T00:00:00Z`);
  return !Number.isNaN(date.valueOf()) && date.toISOString().slice(0, 10) === value;
}
function fresh(today) {
  return {tab: crypto.randomUUID(), route: 'overview', filters: {}, search: '', representation: 'MAP',
    selection: null, financialDate: today, returnContext: null, scroll: 0};
}
async function ownsTab(context) {
  if (!context || window.name !== prefix + context.tab) return false;
  if (!('BroadcastChannel' in window)) return !window.opener;
  let duplicate = false;
  const probe = crypto.randomUUID();
  const receiver = event => {
    if (event.data?.kind === 'owned' && event.data.probe === probe) duplicate = true;
  };
  channel.addEventListener('message', receiver);
  channel.postMessage({kind: 'probe', tab: context.tab, probe});
  await new Promise(resolve => setTimeout(resolve, 120));
  channel.removeEventListener('message', receiver);
  return !duplicate;
}
export async function initialize(config, bootstrap) {
  if ('BroadcastChannel' in window) channel = new BroadcastChannel('hotel.tabs.v1');
  let saved;
  try { saved = JSON.parse(storageRead('sessionStorage', sessionKey)); } catch { saved = null; }
  const valid = saved && typeof saved.tab === 'string' && routes.includes(saved.route)
    && validDate(saved.financialDate) && ['MAP', 'LIST'].includes(saved.representation)
    && typeof saved.search === 'string' && saved.filters && typeof saved.filters === 'object'
    && !Array.isArray(saved.filters);
  const owned = valid && await ownsTab(saved);
  state.context = owned ? saved : fresh(config.operational_date);
  window.name = prefix + state.context.tab;
  if (channel) channel.onmessage = event => {
    if (event.data?.kind === 'probe' && event.data.tab === state.context.tab)
      channel.postMessage({kind: 'owned', probe: event.data.probe});
  };
  state.config = config;
  state.generation = config.generation_id;
  const language = storageRead('localStorage', 'hotel.language');
  // Only English is delivered in F001C.
  state.language = language === 'en' ? language : 'en';
  const currency = storageRead('localStorage', 'hotel.currency');
  state.currency = ['USD', 'LOCAL'].includes(currency) ? currency : 'USD';
  state.counts = bootstrap?.generation_id === state.generation ? bootstrap.counts : null;
  if (!owned) history.replaceState(null, '', '#overview');
  persist(); emit();
}
export function setPreference(name, value) {
  if (name === 'language' && value !== 'en') return;
  if (name === 'currency' && !['USD', 'LOCAL'].includes(value)) return;
  if (!['language', 'currency'].includes(name)) return;
  state[name] = value;
  storageWrite('localStorage', `hotel.${name}`, value); emit();
}
export function setContext(patch) {
  if ('financialDate' in patch && !validDate(patch.financialDate)) throw new Error('invalidDate');
  if ('route' in patch && !routes.includes(patch.route)) throw new Error('invalid route');
  Object.assign(state.context, patch); persist(); emit();
}
export function beginRead(key) {
  const sequence = (sequences.get(key) || 0) + 1;
  sequences.set(key, sequence);
  return {key, sequence, epoch};
}
export function currentRead(token) { return token.epoch === epoch && sequences.get(token.key) === token.sequence; }
export function invalidateReads() { epoch += 1; sequences.clear(); }
export function adoptConfiguration(config) {
  const changed = state.generation && config.generation_id !== state.generation;
  state.config = config;
  if (changed) {
    invalidateReads(); state.preview = null; state.counts = null;
    drafts.forEach(draft => { draft.invalid = true; });
    state.context.selection = null;
  }
  state.generation = config.generation_id;
  if (changed) { persist(); emit(); }
  return changed;
}
export function loadDraft(key, values, version) {
  drafts.set(key, {values: structuredClone(values), version, generation: state.generation,
    dirty: false, invalid: false, submission: null}); emit();
}
export function editDraft(key, values) {
  const draft = drafts.get(key);
  Object.assign(draft.values, structuredClone(values)); draft.dirty = true; draft.submission = null; emit();
}
export function getDraft(key) { return drafts.get(key); }
export function allDrafts() { return [...drafts.values()]; }
export function isDirty() { return allDrafts().some(draft => draft.dirty || draft.invalid); }
export function discardDrafts() { drafts.clear(); emit(); }
export function prepareSubmission(key) {
  const draft = drafts.get(key);
  if (!draft || draft.invalid || draft.generation !== state.generation) throw new Error('errors.stale_store');
  draft.submission ??= {generation_id: draft.generation, submission_id: crypto.randomUUID(),
    expected_version: draft.version, ...structuredClone(draft.values)};
  return structuredClone(draft.submission);
}
export function completedReset(result, config) {
  invalidateReads(); drafts.clear(); state.preview = null;
  state.generation = result.generation_id; state.config = config; state.counts = result.counts;
  state.context = {...fresh(config.operational_date), tab: state.context.tab};
  persist(); history.replaceState(null, '', '#overview'); emit();
}
