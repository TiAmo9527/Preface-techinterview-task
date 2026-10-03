"""F001C browser primitives and real reset/API surfaces; full workflows are deferred."""

import json
import socket
import subprocess
import sys
import time

import httpx

from playwright.sync_api import expect
import pytest


def open_shell(page, server):
    page.goto(server['url'])
    expect(page.get_by_role('heading', name='Overview', exact=True)).to_be_visible()


def draft(page, value='Unsaved fictional draft'):
    page.evaluate("""async value => {
      const s = await import('/static/state.js');
      s.loadDraft('record', {description: 'Original'}, 3);
      s.editDraft('record', {description: value});
    }""", value)


def test_ac_demo_001(page, runtime_server, seeded_store):
    open_shell(page, runtime_server)
    page.get_by_label('Currency', exact=True).select_option('LOCAL')
    page.get_by_label('Financial reporting date', exact=True).fill('2024-02-29')
    page.get_by_label('Financial reporting date', exact=True).blur()
    generation = seeded_store.metadata().generation_id
    page.get_by_role('link', name='Debugging - Assumptions', exact=True).click()
    page.get_by_role('button', name='Reset data', exact=True).click()
    page.get_by_role('dialog').get_by_role('button', name='Reset data', exact=True).click()
    expect(page.get_by_role('status')).to_have_text('Reset saved. The shared store is empty.')
    expect(page.get_by_role('heading', name='Overview', exact=True)).to_be_visible()
    expect(page.get_by_label('Financial reporting date', exact=True)).to_have_value('2026-10-03')
    expect(page.get_by_label('Currency', exact=True)).to_have_value('LOCAL')
    expect(page.get_by_text('No imported data. Initialize the portfolio with an Assets baseline.', exact=True)).to_be_visible()
    assert seeded_store.metadata().generation_id != generation


def test_ac_infra_004_cancel(page, runtime_server, seeded_store):
    from tests.integration.test_runtime import snapshot
    before = snapshot(seeded_store)
    writes = []
    page.on('request', lambda request: writes.append(request.url) if request.method == 'POST' else None)
    open_shell(page, runtime_server)
    page.get_by_role('link', name='Debugging - Assumptions', exact=True).click()
    trigger = page.get_by_role('button', name='Reset data', exact=True)
    trigger.click()
    page.get_by_role('dialog').get_by_role('button', name='Cancel', exact=True).click()
    expect(trigger).to_be_focused()
    assert writes == [] and snapshot(seeded_store) == before


def test_ac_infra_004_rollback_retry(page, runtime_server, seeded_store, monkeypatch):
    from src.db import reset_queries
    from tests.integration.test_runtime import snapshot
    before = snapshot(seeded_store)
    original = reset_queries.DELETE_ORDER
    monkeypatch.setattr(reset_queries, 'DELETE_ORDER', original[:7] + ('missing_reset_table',))
    open_shell(page, runtime_server)
    page.get_by_role('link', name='Debugging - Assumptions', exact=True).click()
    page.get_by_role('button', name='Reset data', exact=True).click()
    confirm = page.get_by_role('dialog').get_by_role('button', name='Reset data', exact=True)
    confirm.click()
    expect(page.get_by_role('status')).to_contain_text('Nothing was saved')
    expect(confirm).to_be_enabled()
    assert snapshot(seeded_store) == before
    monkeypatch.setattr(reset_queries, 'DELETE_ORDER', original)
    confirm.click()
    expect(page.get_by_role('status')).to_contain_text('Reset saved')


def test_ac_infra_005_stale_tab(context, runtime_server, seeded_store):
    first, other = context.new_page(), context.new_page()
    open_shell(first, runtime_server)
    open_shell(other, runtime_server)
    draft(other)
    first.get_by_role('link', name='Debugging - Assumptions', exact=True).click()
    first.get_by_role('button', name='Reset data', exact=True).click()
    first.get_by_role('dialog').get_by_role('button', name='Reset data', exact=True).click()
    expect(first.get_by_role('status')).to_contain_text('Reset saved')
    other.evaluate("window.dispatchEvent(new Event('focus'))")
    expect(other.get_by_label('Invalid draft')).to_contain_text('Unsaved fictional draft')
    assert other.evaluate("""async () => {
      const s = await import('/static/state.js');
      const r = await import('/static/request.js');
      const d = s.getDraft('record');
      try { await r.write('/api/reset', {generation_id: d.generation, confirm: true}, {draftKey: 'record'}); }
      catch (error) { return error.key; }
    }""") == 'errors.stale_store'
    other.get_by_label('Invalid draft').get_by_role('button', name='Discard changes').click()
    expect(other.get_by_label('Invalid draft')).to_be_hidden()


def test_ac_infra_006_unknown_response(page, runtime_server, seeded_store):
    open_shell(page, runtime_server)
    old = seeded_store.metadata().generation_id
    calls = []
    def lose_response(route):
        calls.append(route.request.post_data_json)
        result = route.fetch()
        assert result.status == 200
        route.abort('failed')
    page.route('**/api/reset', lose_response)
    page.get_by_role('link', name='Debugging - Assumptions', exact=True).click()
    page.get_by_role('button', name='Reset data', exact=True).click()
    confirm = page.get_by_role('dialog').get_by_role('button', name='Reset data', exact=True)
    confirm.click()
    expect(page.get_by_role('status')).to_contain_text('unconfirmed')
    assert seeded_store.metadata().generation_id != old
    with seeded_store.transaction() as connection:
        connection.execute("INSERT INTO properties VALUES ('HK-P02', 'New fictional portfolio', 'HONG_KONG', 'Hong Kong')")
    page.unroute('**/api/reset', lose_response)
    confirm.click()
    expect(page.get_by_role('status')).to_contain_text('old request cannot be saved')
    assert len(calls) == 1 and calls[0]['generation_id'] == old
    with seeded_store.transaction(write=False) as connection:
        assert connection.execute('SELECT COUNT(*) FROM properties').fetchone()[0] == 1


@pytest.mark.parametrize('old_error', [False, True])
def test_ac_infra_003(page, runtime_server, old_error):
    open_shell(page, runtime_server)
    held = []
    page.route('**/api/config?probe=A', lambda route: held.append((route, route.fetch())))
    page.evaluate("""async () => {
      window.results = [];
      const r = await import('/static/request.js');
      void r.read('/api/config?probe=A', 'room', data => results.push('A'), error => results.push('old error'));
    }""")
    page.wait_for_function("true")
    # Processing Playwright events delivers the held route without blocking the page.
    page.wait_for_timeout(150)
    assert held
    page.evaluate("""async () => {
      const r = await import('/static/request.js');
      await r.read('/api/config?probe=B', 'room', data => results.push('B'), error => results.push('B error'));
    }""")
    route, response = held[0]
    if old_error:
        route.fulfill(status=500, content_type='application/json', body=json.dumps({'message_key': 'errors.save_failed'}))
    else:
        route.fulfill(response=response)
    expect(page.get_by_role('heading', name='Overview', exact=True)).to_be_visible()
    page.wait_for_timeout(100)
    assert page.evaluate('results') == ['B']


def test_ac_us02_019_reload_and_clone(context, runtime_server):
    original = context.new_page()
    open_shell(original, runtime_server)
    original.get_by_label('Financial reporting date', exact=True).fill('2024-02-29')
    original.get_by_label('Financial reporting date', exact=True).blur()
    original.get_by_role('link', name='Maintenance', exact=True).click()
    original.reload()
    expect(original.get_by_role('heading', name='Maintenance', exact=True)).to_be_visible()
    original.get_by_role('link', name='Overview', exact=True).click()
    expect(original.get_by_label('Financial reporting date', exact=True)).to_have_value('2024-02-29')
    # Real window.open inherits sessionStorage from its opener; window.name ownership rejects it.
    with original.expect_popup() as popup:
        original.evaluate("url => window.open(url, '_blank')", runtime_server['url'])
    copied = popup.value
    expect(copied.get_by_label('Financial reporting date', exact=True)).to_have_value('2026-10-03')
    # Duplicate-style cloning includes the name, requiring the live ownership handshake.
    saved = original.evaluate("({name: window.name, context: sessionStorage.getItem('hotel.context.v1')})")
    duplicate = context.new_page()
    duplicate.add_init_script(f"window.name={json.dumps(saved['name'])}; sessionStorage.setItem('hotel.context.v1', {json.dumps(saved['context'])});")
    duplicate.goto(runtime_server['url'])
    expect(duplicate.get_by_label('Financial reporting date', exact=True)).to_have_value('2026-10-03')


def test_ac_us02_016_preferences_restart(browser_type, browser_type_launch_args, runtime_server, tmp_path, seeded_store):
    from tests.integration.test_runtime import snapshot
    before = snapshot(seeded_store)
    profile = str(tmp_path / 'browser-profile')
    for iteration in range(2):
        context = browser_type.launch_persistent_context(profile, **browser_type_launch_args)
        page = context.pages[0]
        open_shell(page, runtime_server)
        expect(page.get_by_label('Language', exact=True)).to_have_value('en')
        expect(page.get_by_label('Currency', exact=True)).to_have_value('USD' if iteration == 0 else 'LOCAL')
        if iteration == 0:
            page.get_by_label('Currency', exact=True).select_option('LOCAL')
            expect(page.get_by_label('Language', exact=True)).to_have_value('en')
            page.get_by_label('Language', exact=True).select_option('en')
            expect(page.get_by_label('Currency', exact=True)).to_have_value('LOCAL')
        context.close()
    assert snapshot(seeded_store) == before


def test_ac_demo_002_lifecycle_reload(page, runtime_server, seeded_store):
    from app import create_app
    from fastapi.testclient import TestClient
    from tests.integration.test_runtime import snapshot
    open_shell(page, runtime_server)
    before = snapshot(seeded_store)
    with TestClient(create_app(store_path=seeded_store.path)) as client:
        assert client.get('/api/config').json()['generation_id'] == seeded_store.metadata().generation_id
    page.reload()
    expect(page.get_by_role('heading', name='Overview', exact=True)).to_be_visible()
    assert snapshot(seeded_store) == before


def test_ac_demo_002_process_restart(page, seeded_store):
    from src.db.store import REPOSITORY_ROOT
    from tests.integration.test_runtime import snapshot
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    before = snapshot(seeded_store)
    code = (
        'import sys; from pathlib import Path; '
        'from datetime import datetime, timezone; import uvicorn; from app import create_app; '
        "uvicorn.run(create_app(store_path=Path(sys.argv[1]), clock=lambda: datetime(2026,10,3,8,30,tzinfo=timezone.utc)), "
        "host='127.0.0.1', port=int(sys.argv[2]), workers=1, reload=False, log_level='error')"
    )
    url = f'http://127.0.0.1:{port}'
    for iteration in range(2):
        process = subprocess.Popen([sys.executable, '-c', code, str(seeded_store.path), str(port)],
                                   cwd=REPOSITORY_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                try:
                    if httpx.get(url + '/api/config', timeout=.2).status_code == 200:
                        break
                except httpx.HTTPError:
                    pass
                time.sleep(.05)
            else:
                raise AssertionError('Independent runtime process did not start')
            if iteration == 0:
                open_shell(page, {'url': url})
                page.get_by_label('Financial reporting date', exact=True).fill('2024-02-29')
                page.get_by_label('Financial reporting date', exact=True).blur()
            else:
                page.reload()
                expect(page.get_by_label('Financial reporting date', exact=True)).to_have_value('2024-02-29')
        finally:
            process.terminate()
            process.communicate(timeout=10)
        assert snapshot(seeded_store) == before


def test_ac_us02_019_reset_today(page, runtime_server):
    open_shell(page, runtime_server)
    page.get_by_label('Financial reporting date', exact=True).fill('2024-02-29')
    page.get_by_label('Financial reporting date', exact=True).blur()
    page.get_by_role('button', name='Reset to today', exact=True).click()
    expect(page.get_by_label('Financial reporting date', exact=True)).to_have_value('2026-10-03')
    page.evaluate("const data=JSON.parse(sessionStorage.getItem('hotel.context.v1')); data.financialDate='2026-02-30'; sessionStorage.setItem('hotel.context.v1', JSON.stringify(data))")
    page.reload()
    expect(page.get_by_label('Financial reporting date', exact=True)).to_have_value('2026-10-03')
