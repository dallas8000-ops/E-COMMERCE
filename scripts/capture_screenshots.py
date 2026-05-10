"""
Capture storefront screenshots into images/screenshots/ for README / docs.

Requires: playwright, Chromium (`python -m playwright install chromium`)
Usage: run Django first — python backend/manage.py runserver 127.0.0.1:8000
       then: python scripts/capture_screenshots.py

Optional env:
  SCREENSHOT_BASE_URL — default http://127.0.0.1:8000
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "images" / "screenshots"

# Shop lives at /inventory/ (URL name ``inventory``); /catalog/ redirects here with query preserved.
ROUTES = [
    ("/", "home.png"),
    ("/inventory/", "shop.png"),
    ("/about/", "about.png"),
    ("/contact/", "contact.png"),
    ("/terms/", "terms.png"),
    ("/cart/", "cart.png"),
    ("/login/", "login.png"),
    ("/signup/", "signup.png"),
    ("/staff/login/", "staff-login.png"),
    ("/admin/login/", "admin-login.png"),
]


def main() -> int:
    base = os.environ.get("SCREENSHOT_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Install playwright: pip install playwright && playwright install chromium", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1,
        )
        page = context.new_page()
        page.set_default_navigation_timeout(60_000)

        for path, name in ROUTES:
            url = f"{base}{path}"
            target = OUT_DIR / name
            try:
                page.goto(url, wait_until="networkidle")
                page.wait_for_timeout(500)
                page.screenshot(path=str(target), full_page=True)
                print(f"OK {url} -> {target.relative_to(REPO_ROOT)}")
            except Exception as exc:
                print(f"FAIL {url}: {exc}", file=sys.stderr)
                browser.close()
                return 1

        browser.close()

    print(f"\nDone. Screenshots in {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
