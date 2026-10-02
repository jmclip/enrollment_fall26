from playwright.sync_api import sync_playwright
import pathlib
p=pathlib.Path('d65_budget_choices_handout_v3_10_01.html').resolve()
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(); pg.goto(p.as_uri()); pg.wait_for_timeout(500)
    pg.pdf(path='d65_budget_choices_handout_v3_10_01.pdf', format='Letter', print_background=True, margin={'top':'0','bottom':'0','left':'0','right':'0'})
    b.close()
