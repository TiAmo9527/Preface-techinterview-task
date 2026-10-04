// Presentation only: the service supplies every proposed and committed effect.
import {state, subscribe, updateImport, setPreview, setCounts, beginRead, currentRead} from './state.js';
import {upload, write, read} from './request.js';
import {translate} from './i18n.js';

const t = key => translate(key, state.language);
const escape = value => String(value).replace(/[&<>"']/g, char => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[char]));
let root;
let controls;
let review;
let sequence;
const countKeys = ['properties_inserted', 'rooms_inserted', 'assets_inserted', 'invoice_items_inserted',
  'assets_updated', 'historical_only_items', 'skips', 'warnings', 'blockers'];
const fieldKeys = ['asset_name', 'purchase_date', 'installation_date', 'useful_life_months', 'acquisition_cost', 'currency'];
const display = value => value === null ? t('importAbsent') : typeof value === 'object' ? JSON.stringify(value) : String(value);
function counts(values, title) {
  return `<section class="panel" aria-label="${escape(t(title))}"><h2>${escape(t(title))}</h2><dl class="counts">` +
    countKeys.map(key => `<div><dt>${escape(t('importCount.' + key))}</dt><dd data-count="${key}">${values[key]}</dd></div>`).join('') + '</dl></section>';
}
function diagnostics(items) {
  if (!items.length) return '';
  return `<section class="panel"><h2>${escape(t('importDiagnostics'))}</h2><ul>` + items.map(item =>
    `<li><strong>${escape(t('importSeverity.' + item.severity))}</strong>: ${escape(item.reason)}
    <dl><dt>${escape(t('importSource'))}</dt><dd>${escape([item.file, item.sheet, item.row == null ? null : `${t('importRow')} ${item.row}`].filter(value => value != null).join(' · '))}</dd>
    <dt>${escape(t('importField'))}</dt><dd>${escape(item.field)}</dd>
    <dt>${escape(t('importEntity'))}</dt><dd>${escape(item.entity)}</dd>
    <dt>${escape(t('importIdentity'))}</dt><dd>${escape(item.identity ?? t('importAbsent'))}</dd>
    <dt>${escape(t('importValue'))}</dt><dd>${escape(display(item.value))}</dd></dl></li>`).join('') + '</ul></section>';
}
function changes(items) {
  return items.map(item => `<section class="panel"><h3>${escape(item.asset_id)}</h3>
    <p>${escape(t(item.clears_override ? 'importClearsOverride' : 'importKeepsOverride'))}</p>
    <div class="table-scroll" role="region" tabindex="0" aria-label="${escape(t('importChanges'))}: ${escape(item.asset_id)}">
    <table><caption>${escape(t('importChanges'))}</caption><thead><tr><th scope="col">${escape(t('importField'))}</th><th scope="col">${escape(t('importBefore'))}</th><th scope="col">${escape(t('importAfter'))}</th></tr></thead><tbody>` +
    item.changes.map(change => `<tr><th scope="row">${escape(fieldKeys.includes(change.field) ? t('importField.' + change.field) : change.field)}</th><td>${escape(display(change.before))}</td><td>${escape(display(change.after))}</td></tr>`).join('') + '</tbody></table></div></section>').join('');
}
function render() {
  if (!root) return;
  const current = state.importReview;
  const preview = state.preview;
  controls.querySelector('#import-workflow').value = current.workflow;
  // Preserve the actual file input DOM node across preferences, feedback and review updates.
  if (!current.file) controls.querySelector('#import-file').value = '';
  controls.querySelector('#import-selected').textContent = current.file ? `${t('importSelected')}: ${current.file.name}` : t('importNoFile');
  controls.querySelector('#import-prerequisite').textContent = t(current.workflow === 'INVOICES' ? 'importInvoiceHelp' : 'importAssetsHelp');
  controls.querySelectorAll('input, select, button').forEach(control => { control.disabled = current.pending; });
  controls.querySelector('#import-preview').disabled = current.pending || !current.file;
  let html = current.error ? `<p role="alert">${escape(t(current.error))}</p>` : '';
  if (current.pending) html += `<p role="status">${escape(t(current.submission ? 'importSaving' : 'importLoading'))}</p>`;
  if (preview) {
    html += counts(preview.counts, 'importProposed') + diagnostics(preview.diagnostics) + changes(preview.asset_changes);
    html += `<p>${escape(t(preview.counts.blockers ? 'importBlocked' : preview.counts.warnings ? 'importWarningsHelp' : 'importReviewHelp'))}</p>`;
    html += `<div class="actions"><button id="import-confirm" class="primary" ${current.pending || preview.counts.blockers || current.result ? 'disabled' : ''}>${escape(t(current.error && current.submission ? 'importRetry' : 'importConfirm'))}</button>
      <button id="import-cancel" ${current.pending ? 'disabled' : ''}>${escape(t('importCancel'))}</button></div>`;
  }
  if (current.result) html += `<p role="status">${escape(t('importSuccess'))}</p>` + counts(current.result.counts, 'importActual') +
    `<p>${escape(t('importUpload'))}: ${escape(current.result.upload_id ?? t('importNoUpload'))}</p>`;
  if (current.result && current.error === 'importRefreshFailed') html += `<button id="import-refresh">${escape(t('importRefresh'))}</button>`;
  review.innerHTML = html;
  review.querySelector('#import-confirm')?.addEventListener('click', confirm);
  review.querySelector('#import-refresh')?.addEventListener('click', async () => { updateImport({error: null}); await refreshPortfolio(); });
  review.querySelector('#import-cancel')?.addEventListener('click', () => {
    invalidate(); updateImport({error: 'importCancelled'}); controls.querySelector('#import-preview').focus();
  });
}
function invalidate() {
  sequence = beginRead('import');
  setPreview(null);
  updateImport({submission: null, result: null, error: null});
}
async function preview() {
  invalidate();
  const token = sequence;
  const {file, workflow} = state.importReview;
  updateImport({pending: true});
  try {
    const result = await upload(file, workflow);
    if (!currentRead(token)) return;
    if (result.generation_id !== state.generation) { updateImport({error: 'errors.stale_store'}); return; }
    setPreview(result);
  } catch (error) { if (currentRead(token)) updateImport({error: error.key || 'network'}); }
  finally { updateImport({pending: false}); }
}
function refreshPortfolio() {
  return read('/', 'portfolio', result => setCounts(result.counts), () => updateImport({error: 'importRefreshFailed'}));
}
async function confirm() {
  const current = state.importReview;
  if (current.pending || !state.preview || state.preview.counts.blockers || current.result) return;
  const payload = current.submission ?? {generation_id: state.preview.generation_id,
    submission_id: crypto.randomUUID(), preview_id: state.preview.preview_id};
  const token = beginRead('import'); sequence = token;
  updateImport({pending: true, submission: payload, error: null});
  try {
    const result = await write('/api/imports/confirm', payload);
    if (!currentRead(token)) return;
    if (result.generation_id !== state.generation) { updateImport({error: 'errors.stale_store'}); return; }
    updateImport({result});
    setCounts(null);
    await refreshPortfolio();
  } catch (error) {
    if (!currentRead(token)) return;
    if (error.key === 'errors.stale_preview' && error.details.details?.preview) {
      setPreview(error.details.details.preview);
      updateImport({submission: null, error: 'importRenewed'});
    } else updateImport({error: error.unknown ? 'importUnknown' : error.key || 'network'});
  } finally { updateImport({pending: false}); }
}
export function mountImport(container) {
  if (!root) {
    root = document.createElement('div');
    controls = document.createElement('section'); controls.className = 'panel';
    controls.innerHTML = `<h2>${escape(t('importChoose'))}</h2><div class="fields">
      <label>${escape(t('importWorkflow'))}<select id="import-workflow" aria-label="${escape(t('importWorkflow'))}"><option value="ASSETS">${escape(t('importAssets'))}</option><option value="INVOICES">${escape(t('importInvoices'))}</option></select></label>
      <label>${escape(t('importFile'))}<input id="import-file" type="file" accept=".xlsx" aria-describedby="import-selected import-file-help"></label></div>
      <p id="import-file-help">${escape(t('importFileHelp'))}</p><p id="import-selected"></p><p id="import-prerequisite"></p>
      <button id="import-preview" class="primary">${escape(t('importPreview'))}</button>`;
    review = document.createElement('div'); root.append(controls, review);
    controls.querySelector('#import-workflow').onchange = event => { const workflow = event.target.value; invalidate(); updateImport({workflow}); };
    controls.querySelector('#import-file').onchange = event => { const file = event.target.files[0] ?? null; updateImport({file}); invalidate(); };
    controls.querySelector('#import-preview').onclick = preview;
    subscribe(render);
  }
  container.append(root); render();
}
