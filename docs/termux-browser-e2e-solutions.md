# Termux Browser E2E Testing Solutions

This document outlines working solutions for running E2E browser tests in Termux proot-distro environments.

## Table of Contents
1. [Working Browser Solutions](#working-browser-solutions)
2. [Headless Browser Automation](#headless-browser-automation)
3. [GUI Browser Access Methods](#gui-browser-access-methods)
4. [Minimal Browser Options](#minimal-browser-options)
5. [Recommended E2E Testing Setup](#recommended-e2e-testing-setup)

## Working Browser Solutions

### 1. Firefox ESR in proot-distro (Recommended)

Firefox ESR works in proot-distro environments with proper configuration:

```bash
# Install proot-distro
pkg install proot-distro

# Install Ubuntu or Debian
proot-distro install ubuntu

# Login with --shared-tmp flag (crucial!)
proot-distro login ubuntu --shared-tmp

# For Ubuntu 24.04 (avoid snap packages)
apt-get update && apt-get upgrade -y
apt-get install software-properties-common
add-apt-repository ppa:mozillateam/firefox-next
cat <<EOF | tee /etc/apt/preferences.d/pin-mozilla-ppa
Package: *
Pin: release o=LP-PPA-mozillateam-firefox-next
Pin-Priority: 9999
EOF
apt-get update
apt-get install firefox

# Run with display
DISPLAY=:0 firefox --headless
```

### 2. Chromium in Alpine Linux (Puppeteer Compatible)

This is a proven working setup from [puppeteer-on-termux](https://github.com/rishabhrpg/puppeteer-on-termux):

```bash
# Install Alpine Linux
proot-distro install alpine
proot-distro login alpine

# Install Chromium
apk update && apk add --no-cache nmap && \
echo @edge http://nl.alpinelinux.org/alpine/edge/community >> /etc/apk/repositories && \
echo @edge http://nl.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories && \
apk update && \
apk add --no-cache chromium

# Clone working example
git clone https://github.com/rishabhrpg/puppeteer-on-termux.git
cd puppeteer-on-termux
yarn install
node index.js
```

**Note**: Works on arm64 devices. No armv7 build available.

## Headless Browser Automation

### Working Puppeteer Configuration

```javascript
const browser = await puppeteer.launch({
  executablePath: '/usr/bin/chromium-browser',
  headless: true,
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-accelerated-2d-canvas',
    '--no-first-run',
    '--no-zygote',
    '--single-process',
    '--disable-gpu'
  ]
});
```

### Python Selenium Setup

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
```

## GUI Browser Access Methods

### 1. Termux X11 (Best Performance)

```bash
# Install Termux X11
pkg update
pkg install x11-repo
pkg install termux-x11-nightly

# Login to proot with shared tmp
proot-distro login --user user debian --shared-tmp

# Launch with X11
termux-x11 :0 -xstartup "dbus-launch --exit-with-session xfce4-session"
```

### 2. VNC Server

```bash
# Install VNC
pkg install tigervnc

# Start VNC server
vncserver

# Configure ~/.vnc/xstartup
#!/data/data/com.termux/files/usr/bin/sh
fluxbox-generate_menu
fluxbox &
```

### 3. XRDP for Remote Desktop

```bash
# In proot-distro
apt install xrdp xfce4
echo "xfce4-session" > ~/.xsession
sudo service xrdp start
```

## Minimal Browser Options

### 1. Text-Based Browsers (Native Termux)

```bash
# Install text browsers
pkg install lynx w3m links elinks

# Usage
lynx https://example.com
w3m https://example.com
```

### 2. Surf Browser (Lightweight WebKit)

```bash
# In Termux (if packaged)
pkg install surf

# In proot-distro
apt install surf
```

### 3. Qutebrowser (Keyboard-driven)

```bash
# In proot-distro (with caveats)
export QTWEBENGINE_DISABLE_SANDBOX=1
apt install qutebrowser
```

## Recommended E2E Testing Setup

### For Your Project (browser-use)

Given your project's requirements, here's the recommended approach:

1. **Use Alpine Linux with Chromium**
   - Proven to work with Puppeteer
   - Lightweight and fast
   - Good for headless automation

2. **Setup Script**
```bash
#!/bin/bash
# setup-e2e-termux.sh

# Install proot-distro if not present
command -v proot-distro >/dev/null 2>&1 || pkg install proot-distro

# Install Alpine
proot-distro install alpine

# Create automation script
cat > run-e2e-tests.sh << 'EOF'
#!/bin/bash
proot-distro login alpine -- sh -c '
  # Ensure Chromium is installed
  if ! command -v chromium-browser >/dev/null 2>&1; then
    apk update
    echo @edge http://nl.alpinelinux.org/alpine/edge/community >> /etc/apk/repositories
    echo @edge http://nl.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories
    apk update
    apk add --no-cache chromium nodejs npm
  fi
  
  # Run your tests
  cd /path/to/your/project
  npm test
'
EOF

chmod +x run-e2e-tests.sh
```

3. **Alternative: Firefox Headless**
```bash
proot-distro login ubuntu --shared-tmp -- bash -c "
  export DISPLAY=:99
  Xvfb :99 -screen 0 1024x768x24 &
  firefox --headless https://example.com
"
```

### Testing Strategies

1. **For Unit/Integration Tests**: Use headless Chromium in Alpine
2. **For Visual Testing**: Use Termux X11 with Firefox/Chromium
3. **For Minimal Testing**: Use lynx/w3m for basic HTTP verification
4. **For CI/CD**: Stick to headless browsers with proper flags

### Important Notes

- Always use `--no-sandbox` flag for Chromium/Chrome
- The `--shared-tmp` flag is crucial for proot-distro
- Export `DISPLAY=:0` for GUI applications
- Consider using Xvfb for headless GUI testing
- Text browsers (lynx, w3m) are most reliable for basic automation

This setup provides multiple fallback options for E2E testing in Termux environments, from full GUI browsers to minimal text-based solutions.