<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./static/browser-use-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="./static/browser-use.png">
  <img alt="Shows a black Browser Use Logo in light color mode and a white one in dark color mode." src="./static/browser-use.png"  width="full">
</picture>

<h1 align="center">Enable AI to control your browser 🤖</h1>

[![GitHub stars](https://img.shields.io/github/stars/gregpr07/browser-use?style=social)](https://github.com/gregpr07/browser-use/stargazers)
[![Discord](https://img.shields.io/discord/1303749220842340412?color=7289DA&label=Discord&logo=discord&logoColor=white)](https://link.browser-use.com/discord)
[![Cloud](https://img.shields.io/badge/Cloud-☁️-blue)](https://cloud.browser-use.com)
[![Documentation](https://img.shields.io/badge/Documentation-📕-blue)](https://docs.browser-use.com)
[![Twitter Follow](https://img.shields.io/twitter/follow/Gregor?style=social)](https://x.com/gregpr07)
[![Twitter Follow](https://img.shields.io/twitter/follow/Magnus?style=social)](https://x.com/mamagnus00)
[![Weave Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fapp.workweave.ai%2Fapi%2Frepository%2Fbadge%2Forg_T5Pvn3UBswTHIsN1dWS3voPg%2F881458615&labelColor=#EC6341)](https://app.workweave.ai/reports/repository/org_T5Pvn3UBswTHIsN1dWS3voPg/881458615)

🌐 Browser-use is the easiest way to connect your AI agents with the browser.

💡 See what others are building and share your projects in our [Discord](https://link.browser-use.com/discord)! Want Swag? Check out our [Merch store](https://browsermerch.com).

🌤️ Skip the setup - try our <b>hosted version</b> for instant browser automation! <b>[Try the cloud ☁︎](https://cloud.browser-use.com)</b>.

# Quick start

With pip (Python>=3.11):

```bash
pip install browser-use
```

For memory functionality (requires Python<3.13 due to PyTorch compatibility):  

```bash
pip install "browser-use[memory]"
```

Install Patchright:
```bash
patchright install chromium
```

Spin up your agent:

```python
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    await agent.run()

asyncio.run(main())
```

Add your API keys for the provider you want to use to your `.env` file.

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

For other settings, models, and more, check out the [documentation 📕](https://docs.browser-use.com).

### Test with UI

You can test [browser-use with a UI repository](https://github.com/browser-use/web-ui)

Or simply run the gradio example:

```
uv pip install gradio
```

```bash
python examples/ui/gradio_demo.py
```

# Demos

<br/><br/>

[Task](https://github.com/browser-use/browser-use/blob/main/examples/use-cases/shopping.py): Add grocery items to cart, and checkout.

[![AI Did My Groceries](https://github.com/user-attachments/assets/d9359085-bde6-41d4-aa4e-6520d0221872)](https://www.youtube.com/watch?v=L2Ya9PYNns8)

<br/><br/>

Prompt: Add my latest LinkedIn follower to my leads in Salesforce.

![LinkedIn to Salesforce](https://github.com/user-attachments/assets/1440affc-a552-442e-b702-d0d3b277b0ae)

<br/><br/>

[Prompt](https://github.com/browser-use/browser-use/blob/main/examples/use-cases/find_and_apply_to_jobs.py): Read my CV & find ML jobs, save them to a file, and then start applying for them in new tabs, if you need help, ask me.'

https://github.com/user-attachments/assets/171fb4d6-0355-46f2-863e-edb04a828d04

<br/><br/>

[Prompt](https://github.com/browser-use/browser-use/blob/main/examples/browser/real_browser.py): Write a letter in Google Docs to my Papa, thanking him for everything, and save the document as a PDF.

![Letter to Papa](https://github.com/user-attachments/assets/242ade3e-15bc-41c2-988f-cbc5415a66aa)

<br/><br/>

[Prompt](https://github.com/browser-use/browser-use/blob/main/examples/custom-functions/save_to_file_hugging_face.py): Look up models with a license of cc-by-sa-4.0 and sort by most likes on Hugging face, save top 5 to file.

https://github.com/user-attachments/assets/de73ee39-432c-4b97-b4e8-939fd7f323b3

<br/><br/>

## More examples

For more examples see the [examples](examples) folder or join the [Discord](https://link.browser-use.com/discord) and show off your project.

# Vision

Tell your computer what to do, and it gets it done.

## Roadmap

### Agent

- [ ] Improve agent memory (summarize, compress, RAG, etc.)
- [ ] Enhance planning capabilities (load website specific context)
- [ ] Reduce token consumption (system prompt, DOM state)

### DOM Extraction

- [ ] Improve extraction for datepickers, dropdowns, special elements
- [ ] Improve state representation for UI elements

### Rerunning tasks

- [ ] LLM as fallback
- [ ] Make it easy to define workflow templates where LLM fills in the details
- [ ] Return playwright script from the agent

### Datasets

- [ ] Create datasets for complex tasks
- [ ] Benchmark various models against each other
- [ ] Fine-tuning models for specific tasks

### User Experience

- [ ] Human-in-the-loop execution
- [ ] Improve the generated GIF quality
- [ ] Create various demos for tutorial execution, job application, QA testing, social media, etc.

## Contributing

We love contributions! Feel free to open issues for bugs or feature requests. To contribute to the docs, check out the `/docs` folder.

## Local Setup

To learn more about the library, check out the [local setup 📕](https://docs.browser-use.com/development/local-setup).


`main` is the primary development branch with frequent changes. For production use, install a stable [versioned release](https://github.com/browser-use/browser-use/releases) instead.

## Browser Interaction Sub-system (`browser_use_ext`)

This section is for developers working with or contributing to the core browser interaction capabilities of `browser-use`. It details how to run the underlying Python WebSocket server and the accompanying Chrome extension, which together enable direct browser control and detailed state extraction.

This system is responsible for fetching the `BrowserState` from active web pages, which includes the DOM structure, tab information, page metadata, and more.

### Components

1.  **Python WebSocket Server:**
    *   Located at: `browser_use_ext/extension_interface/service.py`
    *   Handles communication with the Chrome extension, processes requests for browser actions, and receives browser state data.
2.  **Chrome Extension:**
    *   Located at: `browser_use_ext/extension/`
    *   Injects content scripts into web pages to extract data and perform actions.
    *   Communicates with the Python WebSocket server.

### Setup and Running

**1. Python WebSocket Server:**

*   **Prerequisites:** Ensure you have Python (>=3.11 recommended) and the necessary dependencies installed (e.g., `websockets`, `pydantic`). If you've followed the main project's local setup, these should be covered.
*   **Running:**
    Navigate to the root directory of the `browser-use` project in your terminal and run:
    ```bash
    python -m browser_use_ext.extension_interface.service
    ```
    The server will start and listen on `ws://localhost:8765` by default. You should see log output in your console indicating it's running.

**2. Chrome Extension:**

*   **Loading the Extension:**
    1.  Open Google Chrome.
    2.  Navigate to `chrome://extensions/`.
    3.  Ensure "Developer mode" (usually a toggle in the top-right corner) is **enabled**.
    4.  Click the "Load unpacked" button.
    5.  In the file dialog, select the `browser_use_ext/extension` directory from this project.
*   The extension should now appear in your list of extensions and automatically attempt to connect to the Python WebSocket server. You can check its background console for connection status (Right-click extension icon -> Inspect popup (if any) or look for "Service worker" link on `chrome://extensions/` details page).

### Automatic Browser State Logging

Once both the Python server is running and the Chrome extension is loaded and connected:

*   **Trigger:** Every time a web page fully loads in your browser (or you switch to an already loaded tab), the extension will notify the Python server.
*   **Action:** The Python server will then request the complete current `BrowserState` from that tab.
*   **Output:** This `BrowserState` (including the DOM tree, URL, title, open tabs, etc.) is saved as a JSON file.
    *   **Location:** These JSON files are stored in a directory named `browser_states_json_logs/` which will be created at the root of your project (where you ran the Python server).
    *   **Filename Convention:** Files are named dynamically to ensure uniqueness, following a pattern like: `browser_state_tab<TAB_ID>_<SANITIZED_URL>_<TIMESTAMP>.json`. For example: `browser_state_tab123_google_com_search_q_example_20231105_153000_123.json`.

**Purpose of these JSON State Logs:**

These detailed JSON logs are invaluable for:
*   Debugging issues related to browser interaction and control.
*   Understanding the precise structure and content of the data available from web pages.
*   Developing and testing new features that rely on browser state information.
*   Analyzing how web pages are perceived by the system.

---

## Swag

Want to show off your Browser-use swag? Check out our [Merch store](https://browsermerch.com). Good contributors will receive swag for free 👀.

## Citation

If you use Browser Use in your research or project, please cite:

```bibtex
@software{browser_use2024,
  author = {Müller, Magnus and Žunič, Gregor},
  title = {Browser Use: Enable AI to control your browser},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/browser-use/browser-use}
}
```

 <div align="center"> <img src="https://github.com/user-attachments/assets/06fa3078-8461-4560-b434-445510c1766f" width="400"/> 
 
[![Twitter Follow](https://img.shields.io/twitter/follow/Gregor?style=social)](https://x.com/gregpr07)
[![Twitter Follow](https://img.shields.io/twitter/follow/Magnus?style=social)](https://x.com/mamagnus00)
 
 </div>

<div align="center">
Made with ❤️ in Zurich and San Francisco
 </div>

## Testing

After installing dependencies from `requirements.txt`, you must also install the necessary Playwright browser binaries by running:

```bash
playwright install chromium
```
