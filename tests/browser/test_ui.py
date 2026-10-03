"""F001C shell, shared card/dialog primitives and assumptions checks."""

from copy import deepcopy

from playwright.sync_api import expect
import pytest

from src.services.configuration import DEFAULT_CONFIGURATION
from tests.browser.test_runtime import draft, open_shell


def test_ac_ux_001_dirty_navigation(page, runtime_server):
    open_shell(page, runtime_server)
    page.get_by_label('Financial reporting date', exact=True).fill('2024-02-29')
    page.get_by_label('Financial reporting date', exact=True).blur()
    draft(page)
    page.get_by_role('link', name='Maintenance', exact=True).click()
    page.get_by_role('button', name='Continue editing', exact=True).click()
    expect(page.get_by_role('heading', name='Overview', exact=True)).to_be_visible()
    page.get_by_role('link', name='Maintenance', exact=True).click()
    page.get_by_role('button', name='Discard changes', exact=True).click()
    expect(page.get_by_role('heading', name='Maintenance', exact=True)).to_be_visible()
    expect(page.get_by_role('link', name='Maintenance', exact=True)).to_have_attribute('aria-current', 'page')
    page.get_by_role('link', name='Overview', exact=True).click()
    expect(page.get_by_label('Financial reporting date', exact=True)).to_have_value('2024-02-29')


def test_ac_ux_001_dirty_hash_and_reset(page, runtime_server):
    open_shell(page, runtime_server)
    draft(page)
    page.evaluate("location.hash = 'import'")
    page.get_by_role('button', name='Continue editing', exact=True).click()
    assert page.url.endswith('#overview')
    page.get_by_role('link', name='Debugging - Assumptions', exact=True).click()
    page.get_by_role('button', name='Discard changes', exact=True).click()
    draft(page)
    page.get_by_role('button', name='Reset data', exact=True).click()
    expect(page.get_by_role('heading', name='Unsaved changes', exact=True)).to_be_visible()
    page.get_by_role('button', name='Discard changes', exact=True).click()
    expect(page.get_by_role('heading', name='Reset the shared data store?', exact=True)).to_be_visible()
    page.get_by_role('button', name='Cancel', exact=True).click()


def test_ac_us02_017(page, runtime_server):
    open_shell(page, runtime_server)
    assert page.get_by_label('Language', exact=True).locator('option').all_text_contents() == ['English']
    assert page.evaluate("async () => (await import('/static/i18n.js')).translate('reset', 'undelivered')") == 'Reset data'
    assert page.evaluate("async () => {const i = await import('/static/i18n.js'); return Object.keys(i.english).every(key => typeof i.english[key] === 'string' && i.english[key].length > 0);}")
    value = '<script>fictional user text</script>'
    draft(page, value)
    assert page.evaluate("async () => (await import('/static/state.js')).getDraft('record').values.description") == value


def test_ac_ux_013_unavailable_storage(page, runtime_server):
    page.add_init_script("Storage.prototype.getItem = () => {throw new Error('disabled')}; Storage.prototype.setItem = () => {throw new Error('disabled')};")
    open_shell(page, runtime_server)
    expect(page.get_by_role('status')).to_contain_text('Browser storage is unavailable')
    page.get_by_label('Currency', exact=True).select_option('LOCAL')
    expect(page.get_by_label('Currency', exact=True)).to_have_value('LOCAL')


@pytest.mark.parametrize('fx_state', ['valid', 'missing', 'invalid'])
def test_ac_ux_019(page, runtime_server, fx_state):
    config = deepcopy(DEFAULT_CONFIGURATION)
    if fx_state == 'missing':
        config['fx'] = None
    elif fx_state == 'invalid':
        config['fx']['usd_per_unit']['USD'] = '2'
    runtime_server['app'].state.local_config = config
    open_shell(page, runtime_server)
    page.get_by_role('link', name='Debugging - Assumptions', exact=True).click()
    for heading in ('Service anchor and clock', 'Depreciation', 'Effective values', 'Replacement and spending proxies',
                    'Import model', 'Invoice precedence and evidence', 'Conditions and links', 'Maintenance and attribution',
                    'Languages and preferences', 'Prototype and persistence', 'Technical and display decisions'):
        expect(page.get_by_role('heading', name=heading, exact=True)).to_be_visible()
    expect(page.get_by_text('Alex Chan (owner-alex)', exact=True)).to_be_visible()
    expect(page.get_by_text('Mei Wong (owner-mei)', exact=True)).to_be_visible()
    assert 'Manual asset creation under AR-002 remains unmet' in page.locator('main').inner_text()
    if fx_state == 'valid':
        before = page.get_by_role('table').inner_text()
        page.get_by_label('Currency', exact=True).select_option('LOCAL')
        assert page.get_by_role('table').inner_text() == before
        expect(page.get_by_text('Fictional fixed rates', exact=False)).to_be_visible()
    else:
        expect(page.get_by_role('alert')).to_contain_text('not configured or invalid')
        assert page.get_by_role('table').count() == 0


def test_ac_ux_013_duplicate_pending(page, runtime_server):
    open_shell(page, runtime_server)
    page.get_by_role('link', name='Debugging - Assumptions', exact=True).click()
    held = []
    page.route('**/api/reset', lambda route: held.append(route))
    page.get_by_role('button', name='Reset data', exact=True).click()
    confirm = page.get_by_role('dialog').get_by_role('button', name='Reset data', exact=True)
    confirm.click()
    expect(confirm).to_be_disabled()
    expect(page.get_by_role('button', name='Cancel', exact=True)).to_be_disabled()
    expect(page.get_by_role('status')).to_have_text('Resetting data…')
    assert len(held) == 1
    held[0].fulfill(response=held[0].fetch())
    expect(page.get_by_role('status')).to_contain_text('Reset saved')


@pytest.mark.parametrize('width', [1440, 1200, 1199, 1024, 768, 601, 600, 360])
def test_ac_ux_016(page, runtime_server, width):
    page.set_viewport_size({'width': width, 'height': 900})
    open_shell(page, runtime_server)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    expect(page.get_by_label('Language', exact=True)).to_be_visible()
    expect(page.get_by_label('Currency', exact=True)).to_be_visible()
    if width >= 1200:
        assert page.locator('nav').bounding_box()['width'] == 200
    page.evaluate("""async () => {
      const shell = await import('/static/shell.js');
      const content = document.createElement('div');
      content.innerHTML = '<label>Long fictional field<input value="Long fictional validation context"></label><p role="alert">A long fictional validation message remains readable within this bounded card.</p>';
      shell.openCard({heading: 'Long fictional room and property heading', content});
    }""")
    card = page.get_by_label('Long fictional room and property heading', exact=True)
    expect(card).to_be_visible()
    expect(card.get_by_role('button', name='Close', exact=True)).to_be_visible()
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    if width <= 600:
        assert abs(card.bounding_box()['width'] - width) < 1
    elif width >= 1200:
        assert card.bounding_box()['width'] == 400
    card.get_by_role('button', name='Close', exact=True).click()
    expect(card).to_have_count(0)


def test_ac_ux_015(page, runtime_server):
    open_shell(page, runtime_server)
    assert page.evaluate("getComputedStyle(document.documentElement).fontSize") == '16px'
    assert page.evaluate("getComputedStyle(document.body).margin") == '0px'
    css = page.request.get(runtime_server['url'] + '/static/shell.css').text()
    for prohibited in ('box-shadow:', 'linear-gradient(', 'animation:', 'transition:'):
        assert prohibited not in css
    assert '#075bd8' in css and '#f5f2eb' in css


def test_ac_ux_017_keyboard_dialog(page, runtime_server):
    open_shell(page, runtime_server)
    link = page.get_by_role('link', name='Debugging - Assumptions', exact=True)
    link.focus()
    page.keyboard.press('Enter')
    trigger = page.get_by_role('button', name='Reset data', exact=True)
    trigger.focus(); page.keyboard.press('Enter')
    expect(page.get_by_role('heading', name='Reset the shared data store?', exact=True)).to_be_focused()
    page.keyboard.press('Tab')
    expect(page.get_by_role('dialog').get_by_role('button', name='Cancel', exact=True)).to_be_focused()
    page.keyboard.press('Tab')
    expect(page.get_by_role('dialog').get_by_role('button', name='Reset data', exact=True)).to_be_focused()
    page.keyboard.press('Tab')
    # Native modal traps tab focus within itself (heading may participate due to tabindex).
    assert page.evaluate("document.activeElement.closest('dialog') !== null || document.activeElement === document.body")
    page.keyboard.press('Escape')
    expect(trigger).to_be_focused()


def test_ac_ux_017_dirty_card_escape(page, runtime_server):
    page.set_viewport_size({'width': 768, 'height': 900})
    open_shell(page, runtime_server)
    page.evaluate("""async () => {
      const shell = await import('/static/shell.js');
      const content = document.createElement('p'); content.textContent = 'Retained card';
      shell.openCard({heading: 'Fictional card', content});
    }""")
    draft(page)
    page.keyboard.press('Escape')
    expect(page.get_by_role('heading', name='Unsaved changes', exact=True)).to_be_visible()
    page.get_by_role('button', name='Continue editing', exact=True).click()
    expect(page.get_by_label('Fictional card', exact=True)).to_be_visible()
    page.keyboard.press('Escape')
    page.get_by_role('button', name='Discard changes', exact=True).click()
    expect(page.get_by_label('Fictional card', exact=True)).to_have_count(0)


def test_ac_ux_007_import_invalidation(page, runtime_server):
    from tests.browser.test_journeys import open_import, preview, select_file
    from tests.integration.test_import import saved
    before = saved(runtime_server['store'])
    open_import(page, runtime_server)
    preview(page)
    page.get_by_label('Import workflow', exact=True).select_option('INVOICES')
    expect(page.get_by_text('Invoices require existing complete room/category targets. Import an Assets baseline first.', exact=True)).to_be_visible()
    assert page.get_by_role('button', name='Confirm reviewed import', exact=True).count() == 0
    expect(page.get_by_text('Selected file: Assets.xlsx', exact=True)).to_be_visible()
    page.get_by_label('Import workflow', exact=True).select_option('ASSETS')
    preview(page)
    select_file(page, invalid=True)
    assert page.get_by_role('heading', name='Proposed effects — not saved', exact=True).count() == 0
    assert saved(runtime_server['store']) == before


def test_ac_ux_008_import_pending(page, runtime_server):
    from tests.browser.test_journeys import open_import, preview
    open_import(page, runtime_server); preview(page)
    held = []
    page.route('**/api/imports/confirm', lambda route: held.append(route))
    page.get_by_role('button', name='Confirm reviewed import', exact=True).click()
    for name in ('Confirm reviewed import', 'Cancel preview', 'Preview workbook'):
        expect(page.get_by_role('button', name=name, exact=True)).to_be_disabled()
    expect(page.get_by_label('Workbook', exact=True)).to_be_disabled()
    expect(page.get_by_label('Import workflow', exact=True)).to_be_disabled()
    expect(page.get_by_text('Confirming import…', exact=True)).to_be_visible()
    assert len(held) == 1
    assert page.get_by_role('heading', name='Actual committed effects', exact=True).count() == 0
    page.get_by_role('link', name='Overview', exact=True).click()
    expect(page.get_by_role('heading', name='Import', exact=True)).to_be_visible()
    held[0].fulfill(response=held[0].fetch())
    expect(page.get_by_text('Import saved. Actual committed counts are shown below.', exact=True)).to_be_visible()


def test_ac_ux_013_import_loading_and_obsolete(page, runtime_server):
    from tests.browser.test_journeys import open_import, select_file
    open_import(page, runtime_server); select_file(page)
    held = []
    page.route('**/api/imports/preview', lambda route: held.append(route))
    page.get_by_role('button', name='Preview workbook', exact=True).click()
    expect(page.get_by_text('Preparing preview…', exact=True)).to_be_visible()
    assert page.get_by_role('button', name='Confirm reviewed import', exact=True).count() == 0
    page.get_by_role('link', name='Overview', exact=True).click()
    held[0].fulfill(response=held[0].fetch())
    expect(page.get_by_role('heading', name='Overview', exact=True)).to_be_visible()
    page.get_by_role('link', name='Import', exact=True).click()
    expect(page.get_by_role('button', name='Preview workbook', exact=True)).to_be_enabled()
    assert page.get_by_role('heading', name='Proposed effects — not saved', exact=True).count() == 0


@pytest.mark.parametrize('width', [1440, 1200, 1199, 1024, 768, 601, 600, 360])
def test_ac_ux_013_import_keyboard_layout(page, runtime_server, width):
    from tests.browser.test_journeys import open_import, preview
    page.set_viewport_size({'width': width, 'height': 900})
    open_import(page, runtime_server); preview(page, invalid=True)
    expect(page.get_by_role('button', name='Confirm reviewed import', exact=True)).to_be_disabled()
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    cancel = page.get_by_role('button', name='Cancel preview', exact=True)
    cancel.focus(); page.keyboard.press('Enter')
    expect(page.get_by_role('alert')).to_contain_text('Nothing was saved')
    select = page.get_by_label('Import workflow', exact=True)
    select.focus(); expect(select).to_be_focused()


def test_ac_ux_008_success_refresh_retry(page, runtime_server):
    from tests.browser.test_journeys import open_import, preview
    from tests.integration.test_import import saved
    open_import(page, runtime_server); preview(page)
    page.route(runtime_server['url'] + '/', lambda route: route.abort())
    page.get_by_role('button', name='Confirm reviewed import', exact=True).click()
    expect(page.get_by_role('alert')).to_contain_text('Import committed. Portfolio refresh failed')
    before = saved(runtime_server['store'])
    expect(page.get_by_role('heading', name='Actual committed effects', exact=True)).to_be_visible()
    page.unroute(runtime_server['url'] + '/')
    page.get_by_role('button', name='Retry portfolio refresh', exact=True).click()
    expect(page.get_by_role('alert')).to_have_count(0)
    page.get_by_role('link', name='Overview', exact=True).click()
    expect(page.locator('.counts')).to_contain_text('Asset records36')
    assert saved(runtime_server['store']) == before
