#!/usr/bin/env python3
"""
Quick test to verify X11 forwarding works with Playwright
"""

from playwright.sync_api import sync_playwright

def test_headless():
    """Test headless browser (should always work)"""
    print("Testing headless browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://example.com')
        title = page.title()
        print(f"✓ Headless works! Page title: {title}")
        browser.close()

def test_headed():
    """Test headed browser (requires X11 forwarding)"""
    print("Testing headed browser...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto('https://example.com')
            title = page.title()
            print(f"✓ Headed browser works! Page title: {title}")
            print("You should see a Chrome window on your Windows desktop!")
            input("Press Enter to close the browser...")
            browser.close()
    except Exception as e:
        print(f"✗ Headed browser failed: {e}")
        print("Make sure VcXsrv is running and DISPLAY is set correctly")

if __name__ == "__main__":
    test_headless()
    print()
    test_headed()