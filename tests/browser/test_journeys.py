"""F002D independent browser reviews through real local import routes."""

import json
from datetime import timedelta
from pathlib import Path
import sqlite3
import socket
import subprocess
import sys
import time

import httpx

from playwright.sync_api import expect
import pytest

from tests.browser.test_runtime import open_shell
from tests.integration.test_import import (seed_baseline, supplied, workbook_bytes, saved,
                                          invoice_row, target_id, manager_edits)

SAMPLE = Path(__file__).resolve().parents[2] / 'sample' / '2026-10-03'


def open_import(page, server, workflow='ASSETS'):
    open_shell(page, server)
    page.get_by_role('link', name='Import', exact=True).click()
    page.get_by_label('Import workflow', exact=True).select_option(workflow)


def select_file(page, workflow='ASSETS', rows=None, invalid=False):
    filename = 'Assets.xlsx' if workflow == 'ASSETS' else 'Invoices.xlsx'
    if rows is None:
        page.get_by_label('Workbook', exact=True).set_input_files(str(SAMPLE / ('invalid' if invalid else 'valid') / filename))
    else:
        page.get_by_label('Workbook', exact=True).set_input_files({
            'name': filename, 'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'buffer': workbook_bytes(workflow, rows)})


def preview(page, workflow='ASSETS', rows=None, invalid=False):
    select_file(page, workflow, rows, invalid)
    page.get_by_role('button', name='Preview workbook', exact=True).click()
    expect(page.get_by_role('heading', name='Proposed effects — not saved', exact=True)).to_be_visible()


def confirm(page):
    page.get_by_role('button', name='Confirm reviewed import', exact=True).click()
    expect(page.get_by_text('Import saved. Actual committed counts are shown below.', exact=True)).to_be_visible()


def count(page, key, value, actual=False):
    section = page.locator('section[aria-label="' + ('Actual committed effects' if actual else 'Proposed effects — not saved') + '"]')
    expect(section.locator(f'[data-count="{key}"]')).to_have_text(str(value))


def test_ac_us01_001(page, runtime_server):
    before = saved(runtime_server['store'])
    open_import(page, runtime_server)
    preview(page)
    for key, value in [('properties_inserted', 4), ('rooms_inserted', 12), ('assets_inserted', 36)]: count(page, key, value)
    assert saved(runtime_server['store']) == before
    confirm(page)
    for key, value in [('properties_inserted', 4), ('rooms_inserted', 12), ('assets_inserted', 36)]: count(page, key, value, True)
    assert len(saved(runtime_server['store'])['assets']) == 36
    page.get_by_role('link', name='Overview', exact=True).click()
    expect(page.locator('.counts')).to_contain_text('Asset records36')


@pytest.mark.parametrize('subset', [True, False])
def test_ac_us01_002(page, runtime_server, subset):
    seed_baseline(runtime_server['store'])
    before = saved(runtime_server['store'])
    rows = [row.as_dict() for row in supplied('INVOICES').normalized_rows[:2]] if subset else None
    open_import(page, runtime_server, 'INVOICES')
    preview(page, 'INVOICES', rows)
    confirm(page)
    for key in ('invoice_items_inserted', 'assets_updated'): count(page, key, 2 if subset else 36, True)
    after = saved(runtime_server['store'])
    for table in ('properties', 'rooms', 'observations', 'asset_baselines', 'baseline_coordinates'): assert after[table] == before[table]
    if subset:
        targets = {target_id(runtime_server['store'], row) for row in rows}
        assert [row for row in before['assets'] if row[0] not in targets] == [row for row in after['assets'] if row[0] not in targets]


@pytest.mark.parametrize('workflow', ['ASSETS', 'INVOICES'])
def test_ac_ux_007_invalid_supplied(page, runtime_server, workflow):
    if workflow == 'INVOICES': seed_baseline(runtime_server['store'])
    before = saved(runtime_server['store'])
    open_import(page, runtime_server, workflow)
    preview(page, workflow, invalid=True)
    expect(page.get_by_role('button', name='Confirm reviewed import', exact=True)).to_be_disabled()
    expect(page.get_by_role('heading', name='Source diagnostics', exact=True)).to_be_visible()
    expect(page.get_by_text('File / sheet / row', exact=True).first).to_be_visible()
    expect(page.get_by_text('Offending value', exact=True).first).to_be_visible()
    assert saved(runtime_server['store']) == before
    assert page.get_by_role('heading', name='Actual committed effects', exact=True).count() == 0


@pytest.mark.parametrize('case', ['installation', 'zero', 'supplier'])
def test_ac_us01_008(page, runtime_server, case):
    seed_baseline(runtime_server['store'])
    row = invoice_row(**{'installation': {'installation_date': None}, 'zero': {'acquisition_cost': '0'},
                         'supplier': {'supplier_name': None}}[case])
    open_import(page, runtime_server, 'INVOICES')
    preview(page, 'INVOICES', [row])
    expect(page.get_by_text('Warnings remain visible. This valid upload can be confirmed.', exact=True)).to_be_visible()
    expect(page.get_by_role('button', name='Confirm reviewed import', exact=True)).to_be_enabled()
    confirm(page)
    count(page, 'warnings', 1, True)
    assert len(saved(runtime_server['store'])['invoice_items']) == 1


def test_ac_us01_019(page, runtime_server):
    store = runtime_server['store']; seed_baseline(store)
    row = invoice_row(installation_date=None)
    asset = target_id(store, row); manager_edits(store, asset)
    before = saved(store)
    open_import(page, runtime_server, 'INVOICES')
    preview(page, 'INVOICES', [row])
    expect(page.get_by_text('This applied invoice clears the active financial override and records linked history.', exact=True)).to_be_visible()
    assert page.get_by_role('table').locator('tbody tr').count() == 6
    expect(page.get_by_role('row').filter(has_text='Installation date')).to_contain_text('Absent')
    assert saved(store) == before
    confirm(page)
    after = saved(store)
    changed = next(item for item in after['assets'] if item[0] == asset)
    assert changed[5] is None and changed[10:12] == (None, None)
    assert len(after['invoice_updates']) == len(after['override_history']) == 1
    assert after['observations'] == before['observations'] and after['maintenance_tickets'] == before['maintenance_tickets']


@pytest.mark.parametrize('stage', ['asset_baselines', 'invoice_updates', 'override_history', 'command_receipts'])
def test_ac_us01_020(page, runtime_server, stage):
    store = runtime_server['store']; workflow = 'ASSETS'
    if stage != 'asset_baselines':
        seed_baseline(store); manager_edits(store, target_id(store, invoice_row())); workflow = 'INVOICES'
    with store.transaction() as connection:
        connection.execute(f"CREATE TRIGGER fail_import BEFORE INSERT ON {stage} BEGIN SELECT RAISE(ABORT, 'injected'); END")
    before = saved(store)
    open_import(page, runtime_server, workflow); preview(page, workflow)
    commands = []
    page.on('request', lambda request: commands.append(request.post_data_json) if request.url.endswith('/api/imports/confirm') else None)
    summary = page.locator('section[aria-label="Proposed effects — not saved"]').inner_text()
    page.get_by_role('button', name='Confirm reviewed import', exact=True).click()
    expect(page.get_by_role('alert')).to_contain_text('Nothing was saved')
    assert saved(store) == before
    assert page.locator('section[aria-label="Proposed effects — not saved"]').inner_text() == summary
    assert page.get_by_role('heading', name='Actual committed effects', exact=True).count() == 0
    expect(page.get_by_label('Workbook', exact=True)).not_to_have_value('')
    with store.transaction() as connection: connection.execute('DROP TRIGGER fail_import')
    page.get_by_role('button', name='Retry reviewed import', exact=True).click()
    expect(page.get_by_text('Import saved. Actual committed counts are shown below.', exact=True)).to_be_visible()
    assert commands[0] == commands[1]


def test_ac_us01_021(page, runtime_server):
    store = runtime_server['store']; seed_baseline(store)
    row = invoice_row(); asset = target_id(store, row)
    open_import(page, runtime_server, 'INVOICES'); preview(page, 'INVOICES', [row])
    with store.transaction() as connection: connection.execute("UPDATE assets SET asset_name='Changed after preview', version=version+1 WHERE asset_id=?", (asset,))
    before = saved(store)
    page.get_by_role('button', name='Confirm reviewed import', exact=True).click()
    expect(page.get_by_role('alert')).to_contain_text('Review the refreshed preview')
    expect(page.get_by_role('table')).to_contain_text('Changed after preview')
    assert saved(store) == before
    confirm(page)
    count(page, 'assets_updated', 1, True)


@pytest.mark.parametrize('case', ['cancel', 'headers', 'empty_rows'])
def test_ac_us01_022(page, runtime_server, case):
    before = saved(runtime_server['store'])
    open_import(page, runtime_server)
    preview(page, rows=None if case == 'cancel' else [] if case == 'headers' else [{}])
    if case == 'cancel':
        page.get_by_role('button', name='Cancel preview', exact=True).click()
        expect(page.get_by_role('alert')).to_contain_text('Nothing was saved')
        assert saved(runtime_server['store']) == before
        assert page.get_by_role('button', name='Confirm reviewed import', exact=True).count() == 0
    else:
        confirm(page)
        after = saved(runtime_server['store'])
        assert len(after['command_receipts']) == 1
        assert {key: rows for key, rows in after.items() if key != 'command_receipts'} == {key: rows for key, rows in before.items() if key != 'command_receipts'}
        count(page, 'assets_inserted', 0, True)


def test_ac_infra_005(page, runtime_server):
    open_import(page, runtime_server); preview(page)
    second = page.context.new_page(); open_shell(second, runtime_server)
    second.get_by_role('link', name='Debugging - Assumptions', exact=True).click()
    second.get_by_role('button', name='Reset data', exact=True).click()
    second.get_by_role('dialog').get_by_role('button', name='Reset data', exact=True).click()
    expect(second.get_by_role('status')).to_contain_text('Reset saved')
    before = saved(runtime_server['store'])
    page.get_by_role('button', name='Confirm reviewed import', exact=True).click()
    expect(page.get_by_role('alert')).to_contain_text('shared store was reset')
    assert saved(runtime_server['store']) == before
    assert page.get_by_role('button', name='Confirm reviewed import', exact=True).count() == 0
    expect(page.get_by_text('Selected file: Assets.xlsx', exact=True)).to_be_visible()


@pytest.mark.parametrize('case', ['expired', 'evicted', 'lost_response'])
def test_ac_infra_007(page, runtime_server, case):
    open_import(page, runtime_server); preview(page)
    registry = runtime_server['app'].state.preview_registry
    if case == 'expired': registry.clock = lambda: runtime_server['app'].state.clock() + timedelta(minutes=31)
    if case == 'evicted': registry.evict_generation(runtime_server['store'].metadata().generation_id)
    commands = []
    if case == 'lost_response':
        def lose(route):
            commands.append(route.request.post_data_json)
            response = route.fetch(); assert response.ok
            route.abort()
        page.route('**/api/imports/confirm', lose)
    page.get_by_role('button', name='Confirm reviewed import', exact=True).click()
    if case != 'lost_response':
        expect(page.get_by_role('alert')).to_contain_text('Upload and review')
        assert not saved(runtime_server['store'])['assets']
    else:
        expect(page.get_by_role('alert')).to_contain_text('unconfirmed')
        before = saved(runtime_server['store'])
        assert len(before['assets']) == 36
        registry.evict_generation(runtime_server['store'].metadata().generation_id)
        page.unroute('**/api/imports/confirm')
        page.on('request', lambda request: commands.append(request.post_data_json) if request.url.endswith('/api/imports/confirm') else None)
        page.get_by_role('button', name='Retry reviewed import', exact=True).click()
        expect(page.get_by_text('Import saved. Actual committed counts are shown below.', exact=True)).to_be_visible()
        assert commands[0] == commands[1] and saved(runtime_server['store']) == before
        page.get_by_role('link', name='Overview', exact=True).click()
        expect(page.locator('.counts')).to_contain_text('Asset records36')


def test_ac_infra_008(page, runtime_server):
    open_import(page, runtime_server); preview(page)
    store = runtime_server['store']; before = saved(store)
    lock = sqlite3.connect(store.path, isolation_level=None); lock.execute('BEGIN IMMEDIATE')
    try:
        page.get_by_role('button', name='Confirm reviewed import', exact=True).click()
        expect(page.get_by_role('alert')).to_contain_text('store is busy', timeout=10000)
    finally:
        lock.rollback(); lock.close()
    assert saved(store) == before
    page.get_by_role('button', name='Retry reviewed import', exact=True).click()
    expect(page.get_by_text('Import saved. Actual committed counts are shown below.', exact=True)).to_be_visible()


def test_ac_infra_007_committed_retry_process_restart(page, store):
    """Retain the live tab/command while the actual server process restarts."""
    from src.db.store import REPOSITORY_ROOT
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0)); port = sock.getsockname()[1]
    code = ('import sys; from pathlib import Path; import uvicorn; from app import create_app; '
            "uvicorn.run(create_app(store_path=Path(sys.argv[1])), host='127.0.0.1', "
            "port=int(sys.argv[2]), workers=1, reload=False, log_level='error')")
    server = {'url': f'http://127.0.0.1:{port}'}
    commands = []
    committed = None
    for iteration in range(2):
        process = subprocess.Popen([sys.executable, '-c', code, str(store.path), str(port)],
                                   cwd=REPOSITORY_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                try:
                    if httpx.get(server['url'] + '/api/config', timeout=.2).status_code == 200: break
                except httpx.HTTPError: pass
                time.sleep(.05)
            else: raise AssertionError('Independent import server did not start')
            if iteration == 0:
                open_import(page, server); preview(page)
                def lose(route):
                    commands.append(route.request.post_data_json)
                    assert route.fetch().ok
                    route.abort()
                page.route('**/api/imports/confirm', lose)
                page.get_by_role('button', name='Confirm reviewed import', exact=True).click()
                expect(page.get_by_role('alert')).to_contain_text('unconfirmed')
                committed = saved(store)
                assert len(committed['assets']) == 36 and len(committed['command_receipts']) == 1
            else:
                page.unroute('**/api/imports/confirm')
                page.on('request', lambda request: commands.append(request.post_data_json) if request.url.endswith('/api/imports/confirm') else None)
                page.get_by_role('button', name='Retry reviewed import', exact=True).click()
                expect(page.get_by_text('Import saved. Actual committed counts are shown below.', exact=True)).to_be_visible()
                count(page, 'assets_inserted', 36, True)
                assert commands[0] == commands[1] and saved(store) == committed
        finally:
            process.terminate(); process.communicate(timeout=10)
