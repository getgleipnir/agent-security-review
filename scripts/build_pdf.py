#!/usr/bin/env python3
"""Print site/index.html to site/downloads/agent-security-review-kit.pdf with every question expanded.

Needs Playwright with Chromium: pip install playwright && playwright install chromium
Run after scripts/build.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "site" / "index.html"
OUT = ROOT / "site" / "downloads" / "agent-security-review-kit.pdf"


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(PAGE.as_uri())
        page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
        page.emulate_media(media="print")
        page.pdf(
            path=str(OUT),
            format="A4",
            margin={"top": "18mm", "bottom": "18mm", "left": "16mm", "right": "16mm"},
            display_header_footer=True,
            header_template="<span></span>",
            footer_template=(
                '<div style="font-size:8px;width:100%;padding:0 16mm;color:#555;display:flex;'
                'justify-content:space-between"><span>Agent Security Review Kit, '
                'github.com/getgleipnir/agent-security-review, CC BY 4.0</span>'
                '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>'
            ),
        )
        browser.close()
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
