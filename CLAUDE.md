# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important: Project Rules

The `.cursor/rules/` directory contains important project-specific rules that should be loaded as context for every interaction. These rules define coding standards, testing practices, and development workflows specific to this project.

### 🔴 CRITICAL: Core Rules (ALWAYS LOAD FIRST)

**`core_rules.mdc`** - This is the MOST CRUCIAL rule file that must ALWAYS be remembered and applied in every interaction. It contains:
- Fundamental coding principles (preserve existing code, minimal modifications)
- Code modification guidelines (adapt don't rebuild, leverage proven logic)
- Debugging strategies and fallback tactics
- File/folder structure requirements
- Environment setup rules
- Comment preservation requirements

### Additional Rule Files:

- `cursor_rules.mdc` - Guidelines for creating and maintaining Cursor rules
- `test_rules.mdc` - Comprehensive testing framework rules
- `python_websockets_guidelines.mdc` - WebSocket implementation patterns
- `chrome_extension_content_readiness.mdc` - Chrome extension development rules
- `pydantic_model_guidelines.mdc` - Pydantic model best practices

These rules should be included in your system context to ensure consistent code generation and modifications that align with project standards. Always prioritize `core_rules.mdc` as the foundation for all development work.

## Project Overview

This is the browser-use project, an AI-powered browser automation framework that enables AI agents to control browsers. The project has two main components:

1. **browser_use/** - Main Python package for browser automation using Playwright
2. **browser_use_ext/** - Python backend for Chrome extension-based browser automation (experimental)

## Architecture

### Main Package (browser_use/)
- **agent/** - Core agent logic with memory, message management, and prompts
- **browser/** - Browser control layer (Chrome, context management, Dolphin service)
- **controller/** - Action dispatch and registry system
- **dom/** - DOM processing and element extraction
- **telemetry/** - Usage tracking and analytics

### Extension Package (browser_use_ext/)
- **extension_interface/** - WebSocket server for Chrome extension communication
- **agent/**, **browser/**, **controller/**, **dom/** - Parallel architecture to main package
- **extension/** - Chrome extension files (background.js, content.js, manifest.json)

## Common Development Commands

### Python Environment Setup
```bash
# The project uses Poetry or UV for dependency management
# Install dependencies (check which is available)
poetry install  # or
uv pip install -e .

# Install Playwright browsers
patchright install chromium  # or
playwright install chromium
```

### Running Tests

#### JavaScript Tests (Jest)
```bash
# Run all Jest tests (unit + integration)
npm test

# Run specific test file
npm test -- test_action_execution_unit.js

# Run specific test directory
npm test -- browser_use_ext/tests/unit/javascript/
npm test -- browser_use_ext/tests/integration/javascript/

# Run with coverage report
npm test -- --coverage

# Run in watch mode (re-runs on file changes)
npm test -- --watch

# Run with verbose output
npm test -- --verbose
```

**Jest Test Statistics:**
- **Total Tests**: 76 tests across 8 test suites
- **Unit Tests**: 65 tests (7 suites)
- **Integration Tests**: 11 tests (1 suite)
- **Execution Time**: ~3-6 seconds
- **Expected Pass Rate**: 100%

#### Python Tests
```bash
# Run all tests (using Poetry virtual environment)
poetry run pytest

# Run specific test directory
poetry run pytest browser_use_ext/tests/unit/python/
poetry run pytest browser_use_ext/tests/integration/python/

# Run with coverage
poetry run pytest --cov=browser_use_ext --cov-report=html

# Run a single test
poetry run pytest -v browser_use_ext/tests/unit/python/test_browser.py::TestBrowser::test_browser_initialization

# Run E2E tests (requires browser setup)
poetry run pytest browser_use_ext/tests/e2e/python/ -m e2e

# Run performance tests
poetry run pytest browser_use_ext/tests/performance/ -m performance
```

#### Comprehensive Test Runner
```bash
# Run all tests (Jest + Python)
python3 run_all_tests.py

# Run only Jest tests
python3 run_all_tests.py --only-jest

# Run only Python tests
python3 run_all_tests.py --only-python

# Run performance monitoring
python3 run_all_tests.py --performance

# Include E2E tests (requires manual browser setup)
python3 run_all_tests.py --include-e2e
```

### Code Quality Checks
```bash
# Python linting and formatting
ruff check .
ruff format .

# TypeScript/JavaScript checks (if npm is available)
npm run check  # Runs all static analysis
npm run check-lint  # ESLint
npm run check-types  # TypeScript
```

### Running the Extension Interface
```bash
# Start the WebSocket server for Chrome extension (using Poetry)
poetry run python -m browser_use_ext.extension_interface.service
# Server runs on ws://localhost:8765
```

## Testing Strategy

The project follows a testing pyramid approach:
- **Unit Tests** (70%) - Test individual components in isolation
- **Integration Tests** (20%) - Test component interactions
- **E2E Tests** (10%) - Test complete user workflows

Test files follow these naming patterns:
- Python: `test_*.py` or `*_test.py`
- JavaScript: `*_test.js` or `*_unit.js`

Test locations:
- **JavaScript Unit Tests**: `browser_use_ext/tests/unit/javascript/`
- **JavaScript Integration Tests**: `browser_use_ext/tests/integration/javascript/`
- **Python Unit Tests**: `browser_use_ext/tests/unit/python/`
- **Python Integration Tests**: `browser_use_ext/tests/integration/python/`
- **E2E Tests**: `browser_use_ext/tests/e2e/python/`
- **Performance Tests**: `browser_use_ext/tests/performance/`

## Key Implementation Notes

### Browser State Management
When the Python WebSocket server and Chrome extension are running together, browser states are automatically logged on page load to `browser_states_json_logs/` directory.

### Async Pattern
Most browser operations are async. Use `async/await` patterns:
```python
async def main():
    agent = Agent(task="...", llm=...)
    await agent.run()
```

### Error Handling
The codebase uses custom exceptions in `exceptions.py`. Always handle browser-specific errors appropriately.

### DOM Processing
The DOM extraction uses a JavaScript file (`buildDomTree.js`) injected into pages. This provides structured element data for the AI agent.

## Project Description (from README.md)

🌐 Browser-use is the easiest way to connect your AI agents with the browser.

### Key Features
- Enable AI to control your browser automatically
- Support for multiple LLM providers (OpenAI, Anthropic, Google, DeepSeek, etc.)
- Vision capabilities for screenshot-based interactions
- Memory functionality for complex multi-step tasks
- Real browser automation (not just headless)

### Quick Start
```bash
pip install browser-use
patchright install chromium

# Basic usage
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    await agent.run()

asyncio.run(main())
```

### Supported API Keys
Add to your `.env` file:
```bash
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_KEY=
GEMINI_API_KEY=
DEEPSEEK_API_KEY=
GROK_API_KEY=
NOVITA_API_KEY=
```

## Browser Extension Sub-system (browser_use_ext/)

### Architecture
The `browser_use_ext/` package provides an alternative Chrome extension-based approach:

1. **Python WebSocket Server** (`browser_use_ext/extension_interface/service.py`)
   - Handles communication with Chrome extension
   - Processes browser action requests
   - Receives detailed browser state data

2. **Chrome Extension** (`browser_use_ext/extension/`)
   - Injects content scripts into web pages
   - Extracts DOM data and performs actions
   - Communicates via WebSocket with Python backend

### Project Structure
```
browser_use_ext/
├── agent/                  # Agent logic (memory, message_manager, prompts)
├── browser/                # Browser interaction layer
├── controller/             # Action dispatch system
├── dom/                    # DOM element representations
├── extension_interface/    # WebSocket server
├── extension/              # Chrome extension files
└── tests/                  # Unit, integration, and e2e tests
```

### Extension Setup
1. **Start Python WebSocket Server:**
   ```bash
   python -m browser_use_ext.extension_interface.service
   # Runs on ws://localhost:8765
   ```

2. **Load Chrome Extension:**
   - Open Chrome → `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select `browser_use_ext/extension` directory

### Automatic State Logging
When both server and extension are running:
- Browser state is automatically captured on page loads
- Detailed JSON logs saved to `browser_states_json_logs/`
- Files named: `browser_state_tab<ID>_<URL>_<TIMESTAMP>.json`
- Useful for debugging and development

### Alternative Setup (WSL/Poetry)
```bash
sudo apt update && sudo apt install python3 python3-venv -y
curl -sSL https://install.python-poetry.org | python3 -
cd /path/to/project/root
/home/ballsac/.local/bin/poetry install
```

## Important Files

- **pyproject.toml** - Python project configuration and dependencies
- **pytest.ini** - Test configuration
- **jest.config.js** - JavaScript test configuration
- **browser_use/agent/system_prompt.md** - Core agent system prompt
- **browser_use_ext/README.md** - Extension system documentation
- **README.md** - Main project documentation
- **PROJECT_DOCS/test_rules.md** - Comprehensive testing guidelines

## E2E Test Goals & Learnings Summary

### Core Testing Philosophy
**Use Chrome Extension for ALL browser interactions - NO Playwright navigation**

### Key Goals Achieved

1. **Launch Chrome with Playwright WITHOUT navigating**
   - Playwright only creates the browser instance and blank tab
   - Do NOT use `page.goto()` or any Playwright navigation methods
   - The extension is the source of truth for all browser state

2. **Accept and work with blank tabs (`about:blank`)**
   - Modified extension's tab scoring to accept blank tabs
   - Added special handling in background.js for navigating blank tabs via `chrome.tabs.update`
   - Skip content script readiness checks for navigation actions in Python interface

3. **Navigate using Chrome Extension DOM injection**
   - All navigation happens through `extension_interface.execute_action("navigate", {"url": "..."})`
   - For blank tabs, use direct Chrome API (`chrome.tabs.update`) instead of content script
   - Navigation is successful even if Playwright page object doesn't update

4. **Retrieve browser state through extension messaging**
   - State comes from content script → background.js → Python via WebSocket
   - Console logs from Playwright are nice-to-have but NOT required
   - The extension's ability to get state proves content script injection worked

### Technical Fixes Applied

1. **Extension Changes:**
   ```javascript
   // Accept blank tabs in scoring
   if (tab.url === "about:blank" || tab.url === "chrome://newtab/" || !tab.url) {
       score += 5;  // Small positive score for blank tabs
       factors.push("blank_tab");
   }
   
   // Direct navigation for blank tabs
   if (tab.url === "about:blank" || tab.url === "chrome://newtab/" || !tab.url) {
       await chrome.tabs.update(activeTabId, { url: subActionParams.url });
   }
   
   // Don't clear content script ready status on page load complete
   // (Fixed race condition)
   ```

2. **Python Interface Changes:**
   ```python
   # Skip content script check for navigate actions
   if action_name != "navigate":
       # ... wait for content script ready
   ```

3. **Test Pattern:**
   ```python
   # 1. Setup console logging (optional - won't work after extension navigation)
   # 2. Wait for extension to detect active tab
   # 3. Navigate using extension
   # 4. Wait for content script injection
   # 5. Get state through extension (proves everything works)
   ```

### Important Learnings

1. **Playwright limitations with extension navigation:**
   - Playwright page object stays on `about:blank` when extension navigates
   - Console logs can't be captured after extension navigation
   - This is OK - the extension is the source of truth

2. **Race conditions to watch for:**
   - Content script sends ready signal
   - Page load complete event might clear ready status
   - Solution: Don't clear ready status on page load

3. **Success criteria:**
   - Navigation returns success
   - Extension can get state (URL, title, actionable elements)
   - This proves content script injected and is working

### Test Implementation Template
```python
# 1. Wait for active tab (might be blank)
await extension_interface.wait_for_active_tab(timeout_seconds=5.0)

# 2. Navigate using extension (NOT Playwright)
nav_result = await extension_interface.execute_action("navigate", {"url": "https://example.com"})
assert nav_result.get("success"), "Navigation should succeed"

# 3. Wait for content script
await asyncio.sleep(5.0)  # Or implement better waiting logic

# 4. Get state to verify everything works
state = await extension_interface.get_state(for_vision=False)
assert state.url == "https://example.com/"
assert len(state.actionable_elements) > 0
```

### Summary
**The extension is the browser automation tool, Playwright is just the launcher.** All navigation, state retrieval, and actions go through the Chrome extension's DOM injection capabilities, not Playwright's CDP interface.