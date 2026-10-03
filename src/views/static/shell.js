import {state, routes, initialize, subscribe, setPreference, setContext, hasStorageFailure,
  validDate, isDirty, discardDrafts, allDrafts, invalidateReads, completedReset} from './state.js';
import {configuration, write} from './request.js';
import {translate, assumptionSections} from './i18n.js';

const workspace = document.querySelector('#workspace');
const dialog = document.querySelector('#confirmation');
const feedback = document.querySelector('#feedback');
let transitionPending = false;
let renderedKey = null;
const t = key => translate(key, state.language);
const escape = value => String(value).replace(/[&<>"']/g, char => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[char]));
export function announce(key) { feedback.textContent = t(key); }
function closeDialog(trigger) {
  dialog.close(); dialog.replaceChildren();
  (trigger?.isConnected ? trigger : workspace).focus();
}
function showDialog(title, text, buttons, trigger) {
  dialog.innerHTML = `<h2 id="dialog-heading" tabindex="-1">${escape(t(title))}</h2><p>${escape(t(text))}</p><div class="actions"></div>`;
  const actions = dialog.querySelector('.actions');
  for (const [key, callback, primary] of buttons) {
    const button = document.createElement('button'); button.textContent = t(key);
    if (primary) button.className = 'primary';
    button.addEventListener('click', callback); actions.append(button);
  }
  dialog.oncancel = event => { event.preventDefault(); closeDialog(trigger); transitionPending = false; };
  dialog.showModal(); dialog.querySelector('h2').focus();
}
export function guardTransition(action, trigger = document.activeElement) {
  if (transitionPending) return;
  if (!isDirty()) { action(); return; }
  transitionPending = true;
  showDialog('dirty', 'dirtyText', [
    ['continue', () => { transitionPending = false; closeDialog(trigger); }],
    ['discard', () => { transitionPending = false; discardDrafts(); closeDialog(trigger); action(); }],
  ], trigger);
}
function navigate(route, trigger, focus = true) {
  if (!routes.includes(route)) route = 'overview';
  guardTransition(() => {
    invalidateReads(); setContext({route, selection: null});
    history.pushState(null, '', `#${route}`);
    if (focus) workspace.querySelector('h1')?.focus();
  }, trigger);
}
function dateFields() {
  return `<section class="panel"><h2>${escape(t('supporting'))}</h2>
    <div class="fields"><label>${escape(t('reporting'))}<input id="financial-date" type="date" value="${escape(state.context.financialDate)}" aria-describedby="date-help date-error"></label>
    <button id="today">${escape(t('today'))}</button></div><p id="date-error" role="alert"></p>
    <p id="date-help" class="muted">${escape(t('noHistory'))}</p></section>`;
}
function assumptions() {
  const config = state.config;
  let html = assumptionSections.map(([heading, text, source]) => `<section class="panel"><h2>${escape(heading)}</h2><p>${escape(text)}</p><cite>${escape(source)}</cite></section>`).join('');
  html += `<section class="panel"><h2>${escape(t('loadedConfig'))}</h2>`;
  html += `<p>${escape(t('configVersion'))}: ${escape(config.configuration_version)}. ${escape(t('schemaVersion'))}: ${escape(config.schema_version)}.</p>`;
  html += `<h3>${escape(t('owners'))}</h3><ul>` + config.owners.map(owner => `<li>${escape(owner.display_name)} (${escape(owner.owner_id)})</li>`).join('') + '</ul>';
  html += `<h3>${escape(t('fixedFx'))}</h3>`;
  if (config.fx) {
    html += `<p>${escape(t('fxDate'))}: ${escape(config.fx.as_of_date)}. ${escape(config.fx.disclaimer)}</p>
      <div class="table-scroll" role="region" aria-label="${escape(t('rateRegion'))}" tabindex="0"><table><thead><tr><th scope="col">${escape(t('currencyLabel'))}</th><th scope="col">${escape(t('rateUnit'))}</th></tr></thead><tbody>`;
    html += Object.entries(config.fx.usd_per_unit).map(([currency, rate]) => `<tr><th scope="row">${escape(currency)}</th><td class="numeric">${escape(rate)}</td></tr>`).join('') + '</tbody></table></div>';
  } else {
    html += `<p role="alert">${escape(t('invalidFx'))}</p>`;
    html += '<ul>' + config.diagnostics.map(item => `<li>${escape(item.field)}: ${escape(item.reason)}</li>`).join('') + '</ul>';
    html += `<pre>${escape(JSON.stringify(config.configured_fx, null, 2))}</pre>`;
  }
  html += `<cite>${escape(t('configSource'))}</cite></section>`;
  html += `<section class="panel"><h2>${escape(t('demoStore'))}</h2><p>${escape(t('resetText'))}</p><button id="reset">${escape(t('reset'))}</button></section>`;
  return html;
}
function render() {
  if (!state.context) return;
  document.documentElement.lang = state.language;
  document.title = t('title');
  document.querySelector('#app-title').textContent = t('title');
  document.querySelector('#app-subtitle').textContent = t('subtitle');
  document.querySelector('#language').value = state.language;
  document.querySelector('#currency').value = state.currency;
  document.querySelectorAll('nav a').forEach(link => {
    link.textContent = t(link.dataset.route);
    if (link.dataset.route === state.context.route) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });
  let html = `<h1 tabindex="-1">${escape(t(state.context.route))}</h1><p class="muted">${escape(t('operational'))}: ${escape(state.config.operational_date)} · ${escape(state.config.operational_time)}</p>`;
  if (state.context.route === 'overview') {
    if (state.counts) {
      html += `<section class="panel"><h2>${escape(t('savedPortfolio'))}</h2><dl class="counts">`;
      for (const [key, label] of [['properties', 'countProperties'], ['rooms', 'countRooms'], ['assets', 'countAssets'], ['tickets', 'countTickets']])
        html += `<div><dt>${escape(t(label))}</dt><dd>${state.counts[key]}</dd></div>`;
      html += '</dl>';
      if (state.counts.properties === 0) html += `<p>${escape(t('empty'))}</p><a class="primary" href="#import" data-route="import">${escape(t('importAssets'))}</a>`;
      html += '</section>';
    }
    html += `<p>${escape(t('reportingPending'))}</p>${dateFields()}`;
  } else if (state.context.route === 'assumptions') html += assumptions();
  else html += `<section class="panel"><p>${escape(t('unavailable'))}</p></section>`;
  const renderKey = JSON.stringify([state.context, state.config, state.counts, state.language, state.currency]);
  if (renderedKey !== renderKey) {
  renderedKey = renderKey;
  workspace.innerHTML = html;
  workspace.querySelector('#financial-date')?.addEventListener('change', event => {
    const value = event.target.value;
    if (!validDate(value)) { document.querySelector('#date-error').textContent = t('invalidDate'); event.target.setAttribute('aria-invalid', 'true'); event.target.focus(); return; }
    invalidateReads(); setContext({financialDate: value});
  });
  workspace.querySelector('#today')?.addEventListener('click', async () => {
    try { const config = await configuration(); if (config) { invalidateReads(); setContext({financialDate: config.operational_date}); } }
    catch (error) { announce(error.key); }
  });
  workspace.querySelector('#reset')?.addEventListener('click', event => guardTransition(() => resetDialog(event.target), event.target));
  }
  const invalid = allDrafts().filter(draft => draft.invalid);
  const container = document.querySelector('#obsolete-draft'); container.hidden = !invalid.length;
  container.replaceChildren();
  if (invalid.length) {
    const message = document.createElement('p'); message.textContent = t('stale'); container.append(message);
    const values = document.createElement('pre'); values.textContent = invalid.map(draft => JSON.stringify(draft.values, null, 2)).join('\n'); container.append(values);
    const button = document.createElement('button'); button.textContent = t('discard'); button.onclick = discardDrafts; container.append(button);
  }
}
function resetDialog(trigger) {
  const payload = {generation_id: state.generation, confirm: true};
  let savedResult = null;
  let busy = false;
  showDialog('resetTitle', 'resetText', [
    ['cancel', () => closeDialog(trigger)],
    ['reset', async () => {
      if (busy) return;
      busy = true;
      const buttons = [...dialog.querySelectorAll('button')]; buttons.forEach(button => { button.disabled = true; });
      announce('saving');
      try {
        savedResult ??= await write('/api/reset', payload);
        const config = await configuration();
        if (!config) throw new Error('configuration replaced');
        // Another reset may have happened while this response was in flight.
        if (config.generation_id !== savedResult.generation_id) {
          announce('errors.stale_store'); closeDialog(trigger); return;
        }
        completedReset(savedResult, config); closeDialog(null); workspace.querySelector('h1')?.focus(); announce('success');
      } catch (error) {
        if (savedResult) announce('confirmedRefresh');
        else if (error.unknown) {
          announce('unknown');
          try { await configuration(); } catch { /* Keep the original payload for explicit retry. */ }
        } else announce(error.key || 'network');
      } finally {
        busy = false; buttons.forEach(button => { button.disabled = false; });
        if (savedResult && dialog.open) buttons[1].textContent = t('retry');
      }
    }, true],
  ], trigger);
  dialog.oncancel = event => { event.preventDefault(); if (!busy) closeDialog(trigger); };
}

// Reusable card primitive. Downstream views supply their actual content and actions.
export function openCard({heading, content, trigger = document.activeElement, close = () => {}}) {
  const narrow = matchMedia('(max-width: 1199px)').matches;
  const card = document.createElement(narrow ? 'dialog' : 'aside');
  card.className = 'detail-card'; card.setAttribute('aria-label', heading);
  const header = document.createElement('div'); header.className = 'card-heading';
  const title = document.createElement('h2'); title.tabIndex = -1; title.textContent = heading;
  const button = document.createElement('button'); button.textContent = t('close'); header.append(title, button);
  const central = document.createElement('div');
  if (!narrow) { central.className = 'central-content'; central.append(...workspace.childNodes); workspace.append(central); }
  card.append(header, content); workspace.append(card);
  if (!narrow) workspace.classList.add('workspace-with-card');
  const finish = () => {
    if (narrow) card.close(); card.remove(); workspace.classList.remove('workspace-with-card');
    if (central.isConnected) central.replaceWith(...central.childNodes);
    close(); (trigger?.isConnected ? trigger : workspace).focus();
  };
  button.onclick = () => guardTransition(finish, button);
  card.addEventListener('keydown', event => { if (event.key === 'Escape') { event.preventDefault(); guardTransition(finish, button); } });
  if (narrow) { card.oncancel = event => { event.preventDefault(); guardTransition(finish, button); }; card.showModal(); }
  title.focus(); return card;
}
document.addEventListener('click', event => {
  const link = event.target.closest('[data-route]');
  if (!link || !state.context) return;
  event.preventDefault(); navigate(link.dataset.route, link);
});
window.addEventListener('hashchange', () => {
  if (!state.context) return;
  const wanted = location.hash.slice(1);
  history.replaceState(null, '', `#${state.context.route}`);
  navigate(wanted, workspace);
});
window.addEventListener('beforeunload', event => { if (isDirty()) { event.preventDefault(); event.returnValue = ''; } });
window.addEventListener('focus', async () => {
  if (!state.context) return;
  try { await configuration(); } catch (error) { announce(error.key); }
});
document.querySelector('#language').onchange = event => setPreference('language', event.target.value);
document.querySelector('#currency').onchange = event => setPreference('currency', event.target.value);
subscribe(render);
async function start() {
  try {
    const config = await configuration();
    if (!config) return;
    await initialize(config, JSON.parse(document.querySelector('#bootstrap').textContent));
    render();
    history.replaceState(null, '', `#${state.context.route}`);
    if (hasStorageFailure()) announce('storage');
  } catch (error) {
    workspace.innerHTML = `<h1 tabindex="-1">${escape(t('configHeading'))}</h1><p>${escape(t(error.key || 'network'))}</p><button id="retry">${escape(t('retry'))}</button>`;
    document.querySelector('#retry').onclick = start;
  }
}
await start();
