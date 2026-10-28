"""UI self-check: pipeline rows render, detail opens, no console errors."""
import sys
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

port = sys.argv[1] if len(sys.argv) > 1 else "8903"
exe = sys.argv[2] if len(sys.argv) > 2 else None
errors = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path=exe) if exe else p.chromium.launch(headless=True)
    page = browser.new_page()
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(f"http://127.0.0.1:{port}/", wait_until="networkidle")
    rows = page.locator("tr[data-id]").count()
    status = page.locator("#status").inner_text()
    assert rows >= 100, f"expected pipeline rows, got {rows}"
    assert "Live pipeline data" in status, status
    page.locator("tr[data-id]").first.click()
    page.wait_for_selector("#detail h2")
    detail = page.locator("#detail").inner_text()
    assert "Pipeline estimate" in detail, detail
    page.locator(".tabs button[data-t=onb]").click()
    tab = page.locator("#tab").inner_text()
    assert "App Store screenshots" in tab or "No screenshots" in tab, tab
    page.locator(".tabs button[data-t=ads]").click()
    ads = page.locator("#tab").inner_text()
    assert "Meta Ad Library" in ads, ads
    assert "demo" not in ads.lower() or "token required" in ads.lower()
    assert not errors, errors
    page.screenshot(path="data/verify.png", full_page=True)
    # Motion: the spur is a decorative mark, hidden from assistive tech, and
    # reduced motion leaves the hero and the rows still and fully drawn.
    assert page.locator("h1 svg.spur[aria-hidden=true]").count() == 1
    calm = browser.new_page(reduced_motion="reduce")
    calm.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    calm.on("pageerror", lambda e: errors.append(str(e)))
    calm.goto(f"http://127.0.0.1:{port}/", wait_until="networkidle")
    moving = calm.evaluate("""() => document.getAnimations()
        .filter(a => a.playState === 'running' && !(a.effect && a.effect.target
            && a.effect.target.classList && a.effect.target.classList.contains('spin')))
        .length""")
    assert moving == 0, f"{moving} animation(s) run under reduced motion"
    assert calm.locator("tr[data-id]").count() >= 100
    assert calm.locator("tr[data-id]").first.evaluate("e => getComputedStyle(e).opacity") == "1"
    assert not errors, errors
    calm.close()
    # Search and lookup must retain Apple's public genre field.
    fixture = page.request.get(f"http://127.0.0.1:{port}/seed.json").json()[0]
    fixture.update(trackId=900000001, trackName="Chartspur metadata audit", sellerName="Audit fixture")
    assert fixture["primaryGenreName"]
    assert "primaryGenre" not in fixture
    metadata_context = browser.new_context(reduced_motion="reduce")
    metadata_requests = []
    def metadata_request(route):
        url = urlsplit(route.request.url)
        if url.netloc == f"127.0.0.1:{port}":
            return route.continue_()
        if url.netloc == "itunes.apple.com" and url.path in ("/search", "/lookup"):
            metadata_requests.append(url.path)
            print(f"Metadata fixture: {route.request.url}", flush=True)
            return route.fulfill(json={"resultCount": 1, "results": [fixture]},
                                 headers={"Access-Control-Allow-Origin": "*"})
        return route.abort()
    metadata_context.route("**/*", metadata_request)
    metadata = metadata_context.new_page()
    metadata.on("pageerror", lambda e: errors.append(str(e)))
    metadata.goto(f"http://127.0.0.1:{port}/", wait_until="networkidle")
    metadata.locator("#q").fill("Chartspur metadata audit")
    metadata.locator("#go").click()
    result = metadata.locator('tr[data-id="900000001"]')
    result.wait_for()
    assert result.get_by_role("cell", name=fixture["primaryGenreName"], exact=True).count() == 1, "search genre missing"
    metadata.locator("#genre").select_option(label=fixture["primaryGenreName"])
    assert result.count() == 1, "genre filter must retain the matching search result"
    metadata.close()
    metadata = metadata_context.new_page()
    metadata.on("pageerror", lambda e: errors.append(str(e)))
    metadata.goto(f"http://127.0.0.1:{port}/?id=900000001", wait_until="networkidle")
    metadata.locator("#detail h2").wait_for()
    genre_line = f"{fixture['sellerName']} · {fixture['primaryGenreName']} ·"
    assert metadata.locator("#detail").get_by_text(genre_line, exact=False).count() == 1, "lookup genre missing"
    assert set(metadata_requests) == {"/search", "/lookup"}, metadata_requests
    assert not errors, errors
    metadata_context.close()
    browser.close()
print(f"UI OK: {rows} rows, detail renders, no console errors")
