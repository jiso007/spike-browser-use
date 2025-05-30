# WSL X11 Setup for Playwright Browser Testing

This guide documents how to set up X11 forwarding on Windows 10 WSL to enable visible browser windows (non-headless) when running Playwright tests.

## Prerequisites

- Windows 10 with WSL installed
- Ubuntu or similar Linux distribution in WSL
- Python environment (we used Poetry in this example)

## Step 1: Install X Server on Windows

1. Download and install VcXsrv from: https://sourceforge.net/projects/vcxsrv/
2. Run XLaunch (VcXsrv) with these settings:
   - Display number: 0
   - Start no client
   - **IMPORTANT**: Check "Disable access control" in Extra settings
   - Save the configuration for easy future launches

## Step 2: Configure WSL Environment

1. Install X11 utilities in WSL:
   ```bash
   sudo apt update
   sudo apt install x11-apps
   ```

2. Set the DISPLAY environment variable:
   ```bash
   export DISPLAY=:0.0
   ```

3. Add to your shell configuration file (e.g., `~/.bashrc`):
   ```bash
   echo 'export DISPLAY=:0.0' >> ~/.bashrc
   source ~/.bashrc
   ```

## Step 3: Test X11 Forwarding

Run a simple X11 application to verify the setup:
```bash
xeyes
```

You should see a pair of eyes appear on your Windows desktop that follow your mouse cursor.

## Step 4: Set Up Poetry Environment

If using Poetry for dependency management:

1. Ensure Poetry is in your PATH:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

2. Add to `~/.bashrc` for persistence:
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. Verify Poetry is accessible:
   ```bash
   which poetry
   ```

## Step 5: Install Playwright Browsers

1. Navigate to your project directory:
   ```bash
   cd /path/to/your/project
   ```

2. Install project dependencies:
   ```bash
   poetry install
   ```

3. Install Playwright browser binaries:
   ```bash
   poetry run playwright install chromium
   ```

4. Install system dependencies if prompted:
   ```bash
   sudo apt install libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libdbus-1-3 libatspi2.0-0 libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libgbm1 libxcb1 libxkbcommon0 libpango-1.0-0 libcairo2 libasound2
   ```

## Step 6: Test Browser Automation

Create a test script (`test_x11_browser.py`):

```python
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
```

Run the test:
```bash
poetry run python test_x11_browser.py
```

## Running Project Tests

Once X11 is configured, you can run Playwright tests with visible browsers:

```bash
# Run all tests
poetry run pytest

# Run specific test files
poetry run pytest browser_use_ext/tests/unit/python/test_browser.py

# Run integration tests
poetry run pytest browser_use_ext/tests/integration/

# Run with coverage
poetry run pytest --cov=browser_use_ext --cov-report=html
```

## Troubleshooting

### X11 Connection Issues

If you see "cannot open display" errors:

1. Verify VcXsrv is running on Windows
2. Check DISPLAY variable: `echo $DISPLAY` (should show `:0.0`)
3. Ensure "Disable access control" was checked in VcXsrv settings
4. Try alternative DISPLAY values:
   ```bash
   export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0
   ```

### Missing Dependencies

If Playwright complains about missing libraries:
```bash
# Get the full list of dependencies
poetry run playwright install-deps chromium
```

### Poetry Not Found

If `poetry: command not found` after installation:
1. Check installation path: `ls -la ~/.local/bin/poetry`
2. Ensure PATH includes Poetry: `export PATH="$HOME/.local/bin:$PATH"`
3. Reload shell configuration: `source ~/.bashrc`

## Security Note

The "Disable access control" setting in VcXsrv allows any client to connect to your X server. This is fine for local development but should not be used in production or sensitive environments.