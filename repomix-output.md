This file is a merged representation of the entire codebase, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

## Additional Info

# Directory Structure
```
.gitattributes
.github/ISSUE_TEMPLATE/bug_report.yml
.github/ISSUE_TEMPLATE/config.yml
.github/ISSUE_TEMPLATE/docs_issue.yml
.github/ISSUE_TEMPLATE/feature_request.yml
.github/workflows/cloud_evals.yml
.github/workflows/lint.yml
.github/workflows/package.yaml
.github/workflows/publish.yml
.github/workflows/test.yaml
.gitignore
.pre-commit-config.yaml
.python-version
browser_use/__init__.py
browser_use/agent/gif.py
browser_use/agent/memory/__init__.py
browser_use/agent/memory/service.py
browser_use/agent/memory/views.py
browser_use/agent/message_manager/service.py
browser_use/agent/message_manager/tests.py
browser_use/agent/message_manager/utils.py
browser_use/agent/message_manager/views.py
browser_use/agent/playwright_script_generator.py
browser_use/agent/playwright_script_helpers.py
browser_use/agent/prompts.py
browser_use/agent/service.py
browser_use/agent/system_prompt.md
browser_use/agent/tests.py
browser_use/agent/views.py
browser_use/browser/browser.py
browser_use/browser/chrome.py
browser_use/browser/context.py
browser_use/browser/dolphin_service.py
browser_use/browser/tests/screenshot_test.py
browser_use/browser/tests/test_clicks.py
browser_use/browser/utils/screen_resolution.py
browser_use/browser/views.py
browser_use/controller/registry/service.py
browser_use/controller/registry/views.py
browser_use/controller/service.py
browser_use/controller/views.py
browser_use/dom/buildDomTree.js
browser_use/dom/clickable_element_processor/service.py
browser_use/dom/history_tree_processor/service.py
browser_use/dom/history_tree_processor/view.py
browser_use/dom/service.py
browser_use/dom/tests/debug_page_structure.py
browser_use/dom/tests/extraction_test.py
browser_use/dom/tests/process_dom_test.py
browser_use/dom/views.py
browser_use/exceptions.py
browser_use/logging_config.py
browser_use/README.md
browser_use/telemetry/service.py
browser_use/telemetry/views.py
browser_use/utils.py
codebeaver.yml
conftest.py
docs/cloud/implementation.mdx
docs/cloud/quickstart.mdx
docs/customize/agent-settings.mdx
docs/customize/browser-settings.mdx
docs/customize/custom-functions.mdx
docs/customize/hooks.mdx
docs/customize/output-format.mdx
docs/customize/real-browser.mdx
docs/customize/sensitive-data.mdx
docs/customize/supported-models.mdx
docs/customize/system-prompt.mdx
docs/development.mdx
docs/development/contribution-guide.mdx
docs/development/evaluations.mdx
docs/development/local-setup.mdx
docs/development/n8n-integration.mdx
docs/development/observability.mdx
docs/development/roadmap.mdx
docs/development/telemetry.mdx
docs/favicon.svg
docs/introduction.mdx
docs/logo/dark.svg
docs/logo/light.svg
docs/quickstart.mdx
docs/README.md
eval/claude-3.5.py
eval/claude-3.6.py
eval/claude-3.7.py
eval/deepseek-r1.py
eval/deepseek.py
eval/gemini-1.5-flash.py
eval/gemini-2.0-flash.py
eval/gemini-2.5-preview.py
eval/gpt-4.1.py
eval/gpt-4o-no-boundingbox.py
eval/gpt-4o-no-vision.py
eval/gpt-4o-viewport-0.py
eval/gpt-4o.py
eval/gpt-o4-mini.py
eval/grok.py
eval/service.py
examples/browser/real_browser.py
examples/browser/stealth.py
examples/browser/using_cdp.py
examples/custom-functions/action_filters.py
examples/custom-functions/advanced_search.py
examples/custom-functions/clipboard.py
examples/custom-functions/custom_hooks_before_after_step.py
examples/custom-functions/file_upload.py
examples/custom-functions/group_ungroup.py
examples/custom-functions/hover_element.py
examples/custom-functions/notification.py
examples/custom-functions/onepassword_2fa.py
examples/custom-functions/save_to_file_hugging_face.py
examples/features/click_fallback_options.py
examples/features/cross_origin_iframes.py
examples/features/custom_output.py
examples/features/custom_system_prompt.py
examples/features/custom_user_agent.py
examples/features/download_file.py
examples/features/drag_drop.py
examples/features/follow_up_tasks.py
examples/features/initial_actions.py
examples/features/multi-tab_handling.py
examples/features/multiple_agents_same_browser.py
examples/features/outsource_state.py
examples/features/parallel_agents.py
examples/features/pause_agent.py
examples/features/planner.py
examples/features/playwright_script_generation.py
examples/features/restrict_urls.py
examples/features/result_processing.py
examples/features/save_trace.py
examples/features/sensitive_data.py
examples/features/small_model_for_extraction.py
examples/features/task_with_memory.py
examples/features/validate_output.py
examples/integrations/discord/discord_api.py
examples/integrations/discord/discord_example.py
examples/integrations/slack/README.md
examples/integrations/slack/slack_api.py
examples/integrations/slack/slack_example.py
examples/models/_ollama.py
examples/models/azure_openai.py
examples/models/bedrock_claude.py
examples/models/claude-3.7-sonnet.py
examples/models/deepseek-r1.py
examples/models/deepseek.py
examples/models/gemini.py
examples/models/gpt-4o.py
examples/models/grok.py
examples/models/novita.py
examples/models/qwen.py
examples/models/README.md
examples/notebook/agent_browsing.ipynb
examples/simple.py
examples/ui/command_line.py
examples/ui/gradio_demo.py
examples/ui/README.md
examples/ui/streamlit_demo.py
examples/use-cases/captcha.py
examples/use-cases/check_appointment.py
examples/use-cases/find_and_apply_to_jobs.py
examples/use-cases/find_influencer_profiles.py
examples/use-cases/google_sheets.py
examples/use-cases/online_coding_agent.py
examples/use-cases/post-twitter.py
examples/use-cases/README.md
examples/use-cases/scrolling_page.py
examples/use-cases/shopping.py
examples/use-cases/twitter_post_using_cookies.py
examples/use-cases/web_voyager_agent.py
examples/use-cases/wikipedia_banana_to_quantum.py
LICENSE
pyproject.toml
pytest.ini
README.md
SECURITY.md
SPIKE_FLOW_2.md
SPIKE_FLOW.md
SPIKE_LLM_BROWSER_STATE.md
SPIKE_LLM_STATE_MESSAGE_TRANSFORM.md
SPIKE_LLM_STATE_SET.md
SPIKE_LLM_TOUCHPOINT.md
tests/conftest.py
tests/test_action_filters.py
tests/test_agent_actions.py
tests/test_attach_chrome.py
tests/test_browser_config_models.py
tests/test_browser_window_size_height_no_viewport.py
tests/test_browser_window_size_height.py
tests/test_browser.py
tests/test_context.py
tests/test_core_functionality.py
tests/test_dropdown_complex.py
tests/test_dropdown_error.py
tests/test_dropdown.py
tests/test_excluded_actions.py
tests/test_full_screen.py
tests/test_gif_path.py
tests/test_mind2web.py
tests/test_models.py
tests/test_qwen.py
tests/test_react_dropdown.py
tests/test_save_conversation.py
tests/test_self_registered_actions.py
tests/test_service.py
tests/test_stress.py
tests/test_vision.py
tests/test_wait_for_element.py
```

# Files

## File: .gitattributes
````
static/*.gif filter=lfs diff=lfs merge=lfs -text
# static/*.mp4 filter=lfs diff=lfs merge=lfs -text
````

## File: .github/ISSUE_TEMPLATE/bug_report.yml
````yaml
name: 🐛 Bug Report
description: Report a bug in browser-use
labels: ["bug", "triage"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report! Please fill out the form below to help us reproduce and fix the issue.

  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: A clear and concise description of what the bug is.
      placeholder: When I try to... the library...
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Reproduction Steps
      description: Steps to reproduce the behavior
      placeholder: |
        1. Install browser-use...
        2. Run the following task...
        3. See error...
    validations:
      required: true

  - type: textarea
    id: code
    attributes:
      label: Code Sample
      description: Include a minimal code sample that reproduces the issue
      render: python
    validations:
      required: true

  - type: input
    id: version
    attributes:
      label: Version
      description: What version of browser-use are you using? (Run `uv pip show browser-use` to find out)
      placeholder: "e.g., pip 0.1.26, or git main branch"
    validations:
      required: true

  - type: dropdown
    id: model
    attributes:
      label: LLM Model
      description: Which LLM model(s) are you using?
      multiple: true
      options:
        - GPT-4o
        - GPT-4
        - Claude 3.5 Sonnet
        - Claude 3.5 Opus
        - Claude 3.5 Haiku
        - Gemini 1.5 Pro
        - Gemini 1.5 Ultra
        - Fireworks Mixtral
        - DeepSeek Coder
        - Local Model (Specify model in description)
        - Other (specify in description)
    validations:
      required: true

  - type: input
    id: os
    attributes:
      label: Operating System
      description: What operating system are you using?
      placeholder: "e.g., macOS 13.1, Windows 11, Ubuntu 22.04"
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Relevant Log Output
      description: Please copy and paste any relevant log output. This will be automatically formatted into code.
      render: shell
````

## File: .github/ISSUE_TEMPLATE/config.yml
````yaml
blank_issues_enabled: false  # Set to true if you want to allow blank issues
contact_links:
  - name: 🤔 Quickstart Guide
    url: https://docs.browser-use.com/quickstart
    about: Most common issues can be resolved by following our quickstart guide
  - name: 🤔 Questions and Help
    url: https://link.browser-use.com/discord
    about: Please ask questions in our Discord community
  - name: 📖 Documentation
    url: https://docs.browser-use.com
    about: Check our documentation for answers first
````

## File: .github/ISSUE_TEMPLATE/docs_issue.yml
````yaml
name: 📚 Documentation Issue
description: Report an issue in the browser-use documentation
labels: ["documentation"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to improve our documentation! Please fill out the form below to help us understand the issue.

  - type: dropdown
    id: type
    attributes:
      label: Type of Documentation Issue
      description: What type of documentation issue is this?
      options:
        - Missing documentation
        - Incorrect documentation
        - Unclear documentation
        - Broken link
        - Other (specify in description)
    validations:
      required: true

  - type: input
    id: page
    attributes:
      label: Documentation Page
      description: Which page or section of the documentation is this about?
      placeholder: "e.g., https://docs.browser-use.com/getting-started or Installation Guide"
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Issue Description
      description: Describe what's wrong or missing in the documentation
      placeholder: The documentation should...
    validations:
      required: true

  - type: textarea
    id: suggestion
    attributes:
      label: Suggested Changes
      description: If you have specific suggestions for how to improve the documentation, please share them
      placeholder: |
        The documentation could be improved by...

        Example:
        ```python
        # Your suggested code example or text here
        ```
    validations:
      required: true
````

## File: .github/ISSUE_TEMPLATE/feature_request.yml
````yaml
name: 💡 Feature Request
description: Suggest a new feature for browser-use
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to suggest a new feature! Please fill out the form below to help us understand your suggestion.

  - type: textarea
    id: problem
    attributes:
      label: Problem Description
      description: Is your feature request related to a problem? Please describe.
      placeholder: I'm always frustrated when...
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: Describe the solution you'd like to see
      placeholder: It would be great if...
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternative Solutions
      description: Describe any alternative solutions or features you've considered
      placeholder: I've also thought about...

  - type: textarea
    id: context
    attributes:
      label: Additional Context
      description: Add any other context or examples about the feature request here
      placeholder: |
        - Example use cases
        - Screenshots or mockups
        - Related issues or discussions
````

## File: .github/workflows/publish.yml
````yaml
# This workflow will upload a Python Package using Twine when a release is created
# For more information see: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python#publishing-to-package-registries

# This workflow uses actions that are not certified by GitHub.
# They are provided by a third-party and are governed by
# separate terms of service, privacy policy, and support
# documentation.

name: publish

on:
  release:
    types: [published]     # publish full release to PyPI when a release is created on Github
  schedule:
    - cron: "0 17 * * FRI" # tag a pre-release on Github every Friday at 5 PM UTC

permissions:
  contents: write
  id-token: write

jobs:
  tag_pre_release:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create pre-release tag
        run: |
          git fetch --tags
          latest_tag=$(git tag --list --sort=-v:refname | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+rc[0-9]+$' | head -n 1)
          if [ -z "$latest_tag" ]; then
            new_tag="v0.1.0rc1"
          else
            new_tag=$(echo $latest_tag | awk -F'rc' '{print $1 "rc" $2+1}')
          fi
          git tag $new_tag
          git push origin $new_tag

  publish_to_pypi:
    if: github.event_name == 'release'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"
      - uses: astral-sh/setup-uv@v5
      - run: uv run ruff check --no-fix --select PLE # check only for syntax errors
      - run: uv build
      - run: uv run --isolated --no-project --with pytest --with dist/*.whl tests/conftest.py
      - run: uv run --isolated --no-project --with pytest --with dist/*.tar.gz tests/conftest.py
      - run: uv run --with=dotenv pytest \
          --ignore=tests/test_dropdown_error.py \
          --ignore=tests/test_gif_path.py \
          --ignore=tests/test_models.py \
          --ignore=tests/test_react_dropdown.py \
          --ignore=tests/test_save_conversation.py \
          --ignore=tests/test_vision.py \
          --ignore=tests/test_wait_for_element.py || true
      - run: uv publish --trusted-publishing always
      - name: Push to stable branch (if stable release)
        if: startsWith(github.ref_name, 'v') && !contains(github.ref_name, 'rc')
        run: |
          git checkout -b stable
          git push origin stable
````

## File: .gitignore
````
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Saved Trajectories for internal evaluation
saved_trajectories/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/latest/usage/project/#working-with-version-control
.pdm.toml
.pdm-python
.pdm-build/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
test_env/


# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/
temp
tmp


.DS_Store

private_example.py
private_example

browser_cookies.json
cookies.json
AgentHistory.json
cv_04_24.pdf
AgentHistoryList.json
*.gif
gcp-login.json
.vscode
.ruff_cache
.idea
*.txt
*.pdf
*.csv
*.json
*.jsonl

uv.lock
````

## File: .pre-commit-config.yaml
````yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.2
    hooks:
      - id: ruff
      - id: ruff-format
      # see pyproject.toml for more details on ruff config

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-toml
      - id: check-yaml
      - id: check-json
      - id: end-of-file-fixer
      - id: check-merge-conflict
      - id: check-illegal-windows-names
      - id: check-case-conflict
      - id: check-added-large-files
      - id: check-shebang-scripts-are-executable
      - id: check-symlinks
      - id: destroyed-symlinks
      - id: detect-private-key
      - id: mixed-line-ending
      - id: fix-byte-order-marker

  - repo: https://github.com/codespell-project/codespell
    rev: v2.4.1
    hooks:
      - id: codespell # See pyproject.toml for args
        additional_dependencies:
          - tomli
````

## File: .python-version
````
3.11
````

## File: browser_use/__init__.py
````python
from browser_use.logging_config import setup_logging

setup_logging()

from browser_use.agent.prompts import SystemPrompt as SystemPrompt
from browser_use.agent.service import Agent as Agent
from browser_use.agent.views import ActionModel as ActionModel
from browser_use.agent.views import ActionResult as ActionResult
from browser_use.agent.views import AgentHistoryList as AgentHistoryList
from browser_use.browser.browser import Browser as Browser
from browser_use.browser.browser import BrowserConfig as BrowserConfig
from browser_use.browser.context import BrowserContextConfig
from browser_use.controller.service import Controller as Controller
from browser_use.dom.service import DomService as DomService

__all__ = [
	'Agent',
	'Browser',
	'BrowserConfig',
	'Controller',
	'DomService',
	'SystemPrompt',
	'ActionResult',
	'ActionModel',
	'AgentHistoryList',
	'BrowserContextConfig',
]
````

## File: browser_use/agent/memory/__init__.py
````python
from browser_use.agent.memory.service import Memory
from browser_use.agent.memory.views import MemoryConfig

__all__ = ['Memory', 'MemoryConfig']
````

## File: browser_use/agent/memory/views.py
````python
from typing import Any, Literal

from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import BaseModel, ConfigDict, Field


class MemoryConfig(BaseModel):
	"""Configuration for procedural memory."""

	model_config = ConfigDict(
		from_attributes=True, validate_default=True, revalidate_instances='always', validate_assignment=True
	)

	# Memory settings
	agent_id: str = Field(default='browser_use_agent', min_length=1)
	memory_interval: int = Field(default=10, gt=1, lt=100)

	# Embedder settings
	embedder_provider: Literal['openai', 'gemini', 'ollama', 'huggingface'] = 'huggingface'
	embedder_model: str = Field(min_length=2, default='all-MiniLM-L6-v2')
	embedder_dims: int = Field(default=384, gt=10, lt=10000)

	# LLM settings - the LLM instance can be passed separately
	llm_provider: Literal['langchain'] = 'langchain'
	llm_instance: BaseChatModel | None = None

	# Vector store settings
	vector_store_provider: Literal['faiss'] = 'faiss'
	vector_store_base_path: str = Field(default='/tmp/mem0')

	@property
	def vector_store_path(self) -> str:
		"""Returns the full vector store path for the current configuration. e.g. /tmp/mem0_384_faiss"""
		return f'{self.vector_store_base_path}_{self.embedder_dims}_{self.vector_store_provider}'

	@property
	def embedder_config_dict(self) -> dict[str, Any]:
		"""Returns the embedder configuration dictionary."""
		return {
			'provider': self.embedder_provider,
			'config': {'model': self.embedder_model, 'embedding_dims': self.embedder_dims},
		}

	@property
	def llm_config_dict(self) -> dict[str, Any]:
		"""Returns the LLM configuration dictionary."""
		return {'provider': self.llm_provider, 'config': {'model': self.llm_instance}}

	@property
	def vector_store_config_dict(self) -> dict[str, Any]:
		"""Returns the vector store configuration dictionary."""
		return {
			'provider': self.vector_store_provider,
			'config': {
				'embedding_model_dims': self.embedder_dims,
				'path': self.vector_store_path,
			},
		}

	@property
	def full_config_dict(self) -> dict[str, dict[str, Any]]:
		"""Returns the complete configuration dictionary for Mem0."""
		return {
			'embedder': self.embedder_config_dict,
			'llm': self.llm_config_dict,
			'vector_store': self.vector_store_config_dict,
		}
````

## File: browser_use/agent/message_manager/tests.py
````python
import pytest
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI, ChatOpenAI

from browser_use.agent.message_manager.service import MessageManager, MessageManagerSettings
from browser_use.agent.views import ActionResult
from browser_use.browser.views import BrowserState, TabInfo
from browser_use.dom.views import DOMElementNode, DOMTextNode


@pytest.fixture(
	params=[
		ChatOpenAI(model='gpt-4o-mini'),
		AzureChatOpenAI(model='gpt-4o', api_version='2024-02-15-preview'),
		ChatAnthropic(model_name='claude-3-5-sonnet-20240620', timeout=100, temperature=0.0, stop=None),
	],
	ids=['gpt-4o-mini', 'gpt-4o', 'claude-3-5-sonnet'],
)
def message_manager(request: pytest.FixtureRequest):
	task = 'Test task'
	action_descriptions = 'Test actions'
	return MessageManager(
		task=task,
		system_message=SystemMessage(content=action_descriptions),
		settings=MessageManagerSettings(
			max_input_tokens=1000,
			estimated_characters_per_token=3,
			image_tokens=800,
		),
	)


def test_initial_messages(message_manager: MessageManager):
	"""Test that message manager initializes with system and task messages"""
	messages = message_manager.get_messages()
	assert len(messages) == 2
	assert isinstance(messages[0], SystemMessage)
	assert isinstance(messages[1], HumanMessage)
	assert 'Test task' in messages[1].content


def test_add_state_message(message_manager: MessageManager):
	"""Test adding browser state message"""
	state = BrowserState(
		url='https://test.com',
		title='Test Page',
		element_tree=DOMElementNode(
			tag_name='div',
			attributes={},
			children=[],
			is_visible=True,
			parent=None,
			xpath='//div',
		),
		selector_map={},
		tabs=[TabInfo(page_id=1, url='https://test.com', title='Test Page')],
	)
	message_manager.add_state_message(state)

	messages = message_manager.get_messages()
	assert len(messages) == 3
	assert isinstance(messages[2], HumanMessage)
	assert 'https://test.com' in messages[2].content


def test_add_state_with_memory_result(message_manager: MessageManager):
	"""Test adding state with result that should be included in memory"""
	state = BrowserState(
		url='https://test.com',
		title='Test Page',
		element_tree=DOMElementNode(
			tag_name='div',
			attributes={},
			children=[],
			is_visible=True,
			parent=None,
			xpath='//div',
		),
		selector_map={},
		tabs=[TabInfo(page_id=1, url='https://test.com', title='Test Page')],
	)
	result = ActionResult(extracted_content='Important content', include_in_memory=True)

	message_manager.add_state_message(state, [result])
	messages = message_manager.get_messages()

	# Should have system, task, extracted content, and state messages
	assert len(messages) == 4
	assert 'Important content' in messages[2].content
	assert isinstance(messages[2], HumanMessage)
	assert isinstance(messages[3], HumanMessage)
	assert 'Important content' not in messages[3].content


def test_add_state_with_non_memory_result(message_manager: MessageManager):
	"""Test adding state with result that should not be included in memory"""
	state = BrowserState(
		url='https://test.com',
		title='Test Page',
		element_tree=DOMElementNode(
			tag_name='div',
			attributes={},
			children=[],
			is_visible=True,
			parent=None,
			xpath='//div',
		),
		selector_map={},
		tabs=[TabInfo(page_id=1, url='https://test.com', title='Test Page')],
	)
	result = ActionResult(extracted_content='Temporary content', include_in_memory=False)

	message_manager.add_state_message(state, [result])
	messages = message_manager.get_messages()

	# Should have system, task, and combined state+result message
	assert len(messages) == 3
	assert 'Temporary content' in messages[2].content
	assert isinstance(messages[2], HumanMessage)


@pytest.mark.skip('not sure how to fix this')
@pytest.mark.parametrize('max_tokens', [100000, 10000, 5000])
def test_token_overflow_handling_with_real_flow(message_manager: MessageManager, max_tokens):
	"""Test handling of token overflow in a realistic message flow"""
	# Set more realistic token limit
	message_manager.settings.max_input_tokens = max_tokens

	# Create a long sequence of interactions
	for i in range(200):  # Simulate 40 steps of interaction
		# Create state with varying content length
		state = BrowserState(
			url=f'https://test{i}.com',
			title=f'Test Page {i}',
			element_tree=DOMElementNode(
				tag_name='div',
				attributes={},
				children=[
					DOMTextNode(
						text=f'Content {j} ' * (10 + i),  # Increasing content length
						is_visible=True,
						parent=None,
					)
					for j in range(5)  # Multiple DOM items
				],
				is_visible=True,
				parent=None,
				xpath='//div',
			),
			selector_map={j: f'//div[{j}]' for j in range(5)},
			tabs=[TabInfo(page_id=1, url=f'https://test{i}.com', title=f'Test Page {i}')],
		)

		# Alternate between different types of results
		result = None
		if i % 2 == 0:  # Every other iteration
			result = ActionResult(
				extracted_content=f'Important content from step {i}' * 5,
				include_in_memory=i % 4 == 0,  # Include in memory every 4th message
			)

		# Add state message
		if result:
			message_manager.add_state_message(state, [result])
		else:
			message_manager.add_state_message(state)

		try:
			messages = message_manager.get_messages()
		except ValueError as e:
			if 'Max token limit reached - history is too long' in str(e):
				return  # If error occurs, end the test
			else:
				raise e

		assert message_manager.state.history.current_tokens <= message_manager.settings.max_input_tokens + 100

		last_msg = messages[-1]
		assert isinstance(last_msg, HumanMessage)

		if i % 4 == 0:
			assert isinstance(message_manager.state.history.messages[-2].message, HumanMessage)
		if i % 2 == 0 and not i % 4 == 0:
			if isinstance(last_msg.content, list):
				assert 'Current url: https://test' in last_msg.content[0]['text']
			else:
				assert 'Current url: https://test' in last_msg.content

		# Add model output every time
		from browser_use.agent.views import AgentBrain, AgentOutput
		from browser_use.controller.registry.views import ActionModel

		output = AgentOutput(
			current_state=AgentBrain(
				evaluation_previous_goal=f'Success in step {i}',
				memory=f'Memory from step {i}',
				next_goal=f'Goal for step {i + 1}',
			),
			action=[ActionModel()],
		)
		message_manager._remove_last_state_message()
		message_manager.add_model_output(output)

		# Get messages and verify after each addition
		messages = [m.message for m in message_manager.state.history.messages]

		# Verify token limit is respected

		# Verify essential messages are preserved
		assert isinstance(messages[0], SystemMessage)  # System prompt always first
		assert isinstance(messages[1], HumanMessage)  # Task always second
		assert 'Test task' in messages[1].content

		# Verify structure of latest messages
		assert isinstance(messages[-1], AIMessage)  # Last message should be model output
		assert f'step {i}' in messages[-1].content  # Should contain current step info

		# Log token usage for debugging
		token_usage = message_manager.state.history.current_tokens
		token_limit = message_manager.settings.max_input_tokens
		# print(f'Step {i}: Using {token_usage}/{token_limit} tokens')

		# go through all messages and verify that the token count and total tokens is correct
		total_tokens = 0
		real_tokens = []
		stored_tokens = []
		for msg in message_manager.state.history.messages:
			total_tokens += msg.metadata.tokens
			stored_tokens.append(msg.metadata.tokens)
			real_tokens.append(message_manager._count_tokens(msg.message))
		assert total_tokens == sum(real_tokens)
		assert stored_tokens == real_tokens
		assert message_manager.state.history.current_tokens == total_tokens


# pytest -s browser_use/agent/message_manager/tests.py
````

## File: browser_use/agent/message_manager/views.py
````python
from __future__ import annotations

from typing import TYPE_CHECKING, Any
from warnings import filterwarnings

from langchain_core._api import LangChainBetaWarning
from langchain_core.load import dumpd, load
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from pydantic import BaseModel, ConfigDict, Field, model_serializer, model_validator

filterwarnings('ignore', category=LangChainBetaWarning)

if TYPE_CHECKING:
	from browser_use.agent.views import AgentOutput


class MessageMetadata(BaseModel):
	"""Metadata for a message"""

	tokens: int = 0
	message_type: str | None = None


class ManagedMessage(BaseModel):
	"""A message with its metadata"""

	message: BaseMessage
	metadata: MessageMetadata = Field(default_factory=MessageMetadata)

	model_config = ConfigDict(arbitrary_types_allowed=True)

	# https://github.com/pydantic/pydantic/discussions/7558
	@model_serializer(mode='wrap')
	def to_json(self, original_dump):
		"""
		Returns the JSON representation of the model.

		It uses langchain's `dumps` function to serialize the `message`
		property before encoding the overall dict with json.dumps.
		"""
		data = original_dump(self)

		# NOTE: We override the message field to use langchain JSON serialization.
		data['message'] = dumpd(self.message)

		return data

	@model_validator(mode='before')
	@classmethod
	def validate(
		cls,
		value: Any,
		*,
		strict: bool | None = None,
		from_attributes: bool | None = None,
		context: Any | None = None,
	) -> Any:
		"""
		Custom validator that uses langchain's `loads` function
		to parse the message if it is provided as a JSON string.
		"""
		if isinstance(value, dict) and 'message' in value:
			# NOTE: We use langchain's load to convert the JSON string back into a BaseMessage object.
			filterwarnings('ignore', category=LangChainBetaWarning)
			value['message'] = load(value['message'])
		return value


class MessageHistory(BaseModel):
	"""History of messages with metadata"""

	messages: list[ManagedMessage] = Field(default_factory=list)
	current_tokens: int = 0

	model_config = ConfigDict(arbitrary_types_allowed=True)

	def add_message(self, message: BaseMessage, metadata: MessageMetadata, position: int | None = None) -> None:
		"""Add message with metadata to history"""
		if position is None:
			self.messages.append(ManagedMessage(message=message, metadata=metadata))
		else:
			self.messages.insert(position, ManagedMessage(message=message, metadata=metadata))
		self.current_tokens += metadata.tokens

	def add_model_output(self, output: 'AgentOutput') -> None:
		"""Add model output as AI message"""
		tool_calls = [
			{
				'name': 'AgentOutput',
				'args': output.model_dump(mode='json', exclude_unset=True),
				'id': '1',
				'type': 'tool_call',
			}
		]

		msg = AIMessage(
			content='',
			tool_calls=tool_calls,
		)
		self.add_message(msg, MessageMetadata(tokens=100))  # Estimate tokens for tool calls

		# Empty tool response
		tool_message = ToolMessage(content='', tool_call_id='1')
		self.add_message(tool_message, MessageMetadata(tokens=10))  # Estimate tokens for empty response

	def get_messages(self) -> list[BaseMessage]:
		"""Get all messages"""
		return [m.message for m in self.messages]

	def get_total_tokens(self) -> int:
		"""Get total tokens in history"""
		return self.current_tokens

	def remove_oldest_message(self) -> None:
		"""Remove oldest non-system message"""
		for i, msg in enumerate(self.messages):
			if not isinstance(msg.message, SystemMessage):
				self.current_tokens -= msg.metadata.tokens
				self.messages.pop(i)
				break

	def remove_last_state_message(self) -> None:
		"""Remove last state message from history"""
		if len(self.messages) > 2 and isinstance(self.messages[-1].message, HumanMessage):
			self.current_tokens -= self.messages[-1].metadata.tokens
			self.messages.pop()


class MessageManagerState(BaseModel):
	"""Holds the state for MessageManager"""

	history: MessageHistory = Field(default_factory=MessageHistory)
	tool_id: int = 1

	model_config = ConfigDict(arbitrary_types_allowed=True)
````

## File: browser_use/agent/prompts.py
````python
import importlib.resources
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Union

from langchain_core.messages import HumanMessage, SystemMessage

if TYPE_CHECKING:
	from browser_use.agent.views import ActionResult, AgentStepInfo
	from browser_use.browser.views import BrowserState


class SystemPrompt:
	def __init__(
		self,
		action_description: str,
		max_actions_per_step: int = 10,
		override_system_message: Optional[str] = None,
		extend_system_message: Optional[str] = None,
	):
		self.default_action_description = action_description
		self.max_actions_per_step = max_actions_per_step
		prompt = ''
		if override_system_message:
			prompt = override_system_message
		else:
			self._load_prompt_template()
			prompt = self.prompt_template.format(max_actions=self.max_actions_per_step)

		if extend_system_message:
			prompt += f'\n{extend_system_message}'

		self.system_message = SystemMessage(content=prompt)

	def _load_prompt_template(self) -> None:
		"""Load the prompt template from the markdown file."""
		try:
			# This works both in development and when installed as a package
			with importlib.resources.files('browser_use.agent').joinpath('system_prompt.md').open('r') as f:
				self.prompt_template = f.read()
		except Exception as e:
			raise RuntimeError(f'Failed to load system prompt template: {e}')

	def get_system_message(self) -> SystemMessage:
		"""
		Get the system prompt for the agent.

		Returns:
		    SystemMessage: Formatted system prompt
		"""
		return self.system_message


# Functions:
# {self.default_action_description}

# Example:
# {self.example_response()}
# Your AVAILABLE ACTIONS:
# {self.default_action_description}


class AgentMessagePrompt:
	def __init__(
		self,
		state: 'BrowserState',
		result: Optional[List['ActionResult']] = None,
		include_attributes: list[str] | None = None,
		step_info: Optional['AgentStepInfo'] = None,
	):
		self.state = state
		self.result = result
		self.include_attributes = include_attributes or []
		self.step_info = step_info

	def get_user_message(self, use_vision: bool = True) -> HumanMessage:
		elements_text = self.state.element_tree.clickable_elements_to_string(include_attributes=self.include_attributes)

		has_content_above = (self.state.pixels_above or 0) > 0
		has_content_below = (self.state.pixels_below or 0) > 0

		if elements_text != '':
			if has_content_above:
				elements_text = (
					f'... {self.state.pixels_above} pixels above - scroll or extract content to see more ...\n{elements_text}'
				)
			else:
				elements_text = f'[Start of page]\n{elements_text}'
			if has_content_below:
				elements_text = (
					f'{elements_text}\n... {self.state.pixels_below} pixels below - scroll or extract content to see more ...'
				)
			else:
				elements_text = f'{elements_text}\n[End of page]'
		else:
			elements_text = 'empty page'

		if self.step_info:
			step_info_description = f'Current step: {self.step_info.step_number + 1}/{self.step_info.max_steps}'
		else:
			step_info_description = ''
		time_str = datetime.now().strftime('%Y-%m-%d %H:%M')
		step_info_description += f'Current date and time: {time_str}'

		state_description = f"""
[Task history memory ends]
[Current state starts here]
The following is one-time information - if you need to remember it write it to memory:
Current url: {self.state.url}
Available tabs:
{self.state.tabs}
Interactive elements from top layer of the current page inside the viewport:
{elements_text}
{step_info_description}
"""

		if self.result:
			for i, result in enumerate(self.result):
				if result.extracted_content:
					state_description += f'\nAction result {i + 1}/{len(self.result)}: {result.extracted_content}'
				if result.error:
					# only use last line of error
					error = result.error.split('\n')[-1]
					state_description += f'\nAction error {i + 1}/{len(self.result)}: ...{error}'

		if self.state.screenshot and use_vision is True:
			# Format message for vision model
			return HumanMessage(
				content=[
					{'type': 'text', 'text': state_description},
					{
						'type': 'image_url',
						'image_url': {'url': f'data:image/png;base64,{self.state.screenshot}'},  # , 'detail': 'low'
					},
				]
			)

		return HumanMessage(content=state_description)


class PlannerPrompt(SystemPrompt):
	def __init__(self, available_actions: str):
		self.available_actions = available_actions

	def get_system_message(
		self, is_planner_reasoning: bool, extended_planner_system_prompt: Optional[str] = None
	) -> Union[SystemMessage, HumanMessage]:
		"""Get the system message for the planner.

		Args:
		    is_planner_reasoning: If True, return as HumanMessage for chain-of-thought
		    extended_planner_system_prompt: Optional text to append to the base prompt

		Returns:
		    SystemMessage or HumanMessage depending on is_planner_reasoning
		"""

		planner_prompt_text = """
You are a planning agent that helps break down tasks into smaller steps and reason about the current state.
Your role is to:
1. Analyze the current state and history
2. Evaluate progress towards the ultimate goal
3. Identify potential challenges or roadblocks
4. Suggest the next high-level steps to take

Inside your messages, there will be AI messages from different agents with different formats.

Your output format should be always a JSON object with the following fields:
{{
    "state_analysis": "Brief analysis of the current state and what has been done so far",
    "progress_evaluation": "Evaluation of progress towards the ultimate goal (as percentage and description)",
    "challenges": "List any potential challenges or roadblocks",
    "next_steps": "List 2-3 concrete next steps to take",
    "reasoning": "Explain your reasoning for the suggested next steps"
}}

Ignore the other AI messages output structures.

Keep your responses concise and focused on actionable insights.
"""

		if extended_planner_system_prompt:
			planner_prompt_text += f'\n{extended_planner_system_prompt}'

		if is_planner_reasoning:
			return HumanMessage(content=planner_prompt_text)
		else:
			return SystemMessage(content=planner_prompt_text)
````

## File: browser_use/agent/system_prompt.md
````markdown
You are an AI agent designed to automate browser tasks. Your goal is to accomplish the ultimate task following the rules.

# Input Format

Task
Previous steps
Current URL
Open Tabs
Interactive Elements
[index]<type>text</type>

- index: Numeric identifier for interaction
- type: HTML element type (button, input, etc.)
- text: Element description
  Example:
  [33]<div>User form</div>
  \t*[35]*<button aria-label='Submit form'>Submit</button>

- Only elements with numeric indexes in [] are interactive
- (stacked) indentation (with \t) is important and means that the element is a (html) child of the element above (with a lower index)
- Elements with \* are new elements that were added after the previous step (if url has not changed)

# Response Rules

1. RESPONSE FORMAT: You must ALWAYS respond with valid JSON in this exact format:
   {{"current_state": {{"evaluation_previous_goal": "Success|Failed|Unknown - Analyze the current elements and the image to check if the previous goals/actions are successful like intended by the task. Mention if something unexpected happened. Shortly state why/why not",
   "memory": "Description of what has been done and what you need to remember. Be very specific. Count here ALWAYS how many times you have done something and how many remain. E.g. 0 out of 10 websites analyzed. Continue with abc and xyz",
   "next_goal": "What needs to be done with the next immediate action"}},
   "action":[{{"one_action_name": {{// action-specific parameter}}}}, // ... more actions in sequence]}}

2. ACTIONS: You can specify multiple actions in the list to be executed in sequence. But always specify only one action name per item. Use maximum {max_actions} actions per sequence.
Common action sequences:

- Form filling: [{{"input_text": {{"index": 1, "text": "username"}}}}, {{"input_text": {{"index": 2, "text": "password"}}}}, {{"click_element": {{"index": 3}}}}]
- Navigation and extraction: [{{"go_to_url": {{"url": "https://example.com"}}}}, {{"extract_content": {{"goal": "extract the names"}}}}]
- Actions are executed in the given order
- If the page changes after an action, the sequence is interrupted and you get the new state.
- Only provide the action sequence until an action which changes the page state significantly.
- Try to be efficient, e.g. fill forms at once, or chain actions where nothing changes on the page
- only use multiple actions if it makes sense.

3. ELEMENT INTERACTION:

- Only use indexes of the interactive elements

4. NAVIGATION & ERROR HANDLING:

- If no suitable elements exist, use other functions to complete the task
- If stuck, try alternative approaches - like going back to a previous page, new search, new tab etc.
- Handle popups/cookies by accepting or closing them
- Use scroll to find elements you are looking for
- If you want to research something, open a new tab instead of using the current tab
- If captcha pops up, try to solve it - else try a different approach
- If the page is not fully loaded, use wait action

5. TASK COMPLETION:

- Use the done action as the last action as soon as the ultimate task is complete
- Dont use "done" before you are done with everything the user asked you, except you reach the last step of max_steps.
- If you reach your last step, use the done action even if the task is not fully finished. Provide all the information you have gathered so far. If the ultimate task is completely finished set success to true. If not everything the user asked for is completed set success in done to false!
- If you have to do something repeatedly for example the task says for "each", or "for all", or "x times", count always inside "memory" how many times you have done it and how many remain. Don't stop until you have completed like the task asked you. Only call done after the last step.
- Don't hallucinate actions
- Make sure you include everything you found out for the ultimate task in the done text parameter. Do not just say you are done, but include the requested information of the task.

6. VISUAL CONTEXT:

- When an image is provided, use it to understand the page layout
- Bounding boxes with labels on their top right corner correspond to element indexes

7. Form filling:

- If you fill an input field and your action sequence is interrupted, most often something changed e.g. suggestions popped up under the field.

8. Long tasks:

- Keep track of the status and subresults in the memory.
- You are provided with procedural memory summaries that condense previous task history (every N steps). Use these summaries to maintain context about completed actions, current progress, and next steps. The summaries appear in chronological order and contain key information about navigation history, findings, errors encountered, and current state. Refer to these summaries to avoid repeating actions and to ensure consistent progress toward the task goal.

9. Extraction:

- If your task is to find information - call extract_content on the specific pages to get and store the information.
  Your responses must be always JSON with the specified format.
````

## File: browser_use/agent/tests.py
````python
import pytest

from browser_use.agent.views import (
	ActionResult,
	AgentBrain,
	AgentHistory,
	AgentHistoryList,
	AgentOutput,
)
from browser_use.browser.views import BrowserState, BrowserStateHistory, TabInfo
from browser_use.controller.registry.service import Registry
from browser_use.controller.views import ClickElementAction, DoneAction, ExtractPageContentAction
from browser_use.dom.views import DOMElementNode


@pytest.fixture
def sample_browser_state():
	return BrowserState(
		url='https://example.com',
		title='Example Page',
		tabs=[TabInfo(url='https://example.com', title='Example Page', page_id=1)],
		screenshot='screenshot1.png',
		element_tree=DOMElementNode(
			tag_name='root',
			is_visible=True,
			parent=None,
			xpath='',
			attributes={},
			children=[],
		),
		selector_map={},
	)


@pytest.fixture
def action_registry():
	registry = Registry()

	# Register the actions we need for testing
	@registry.action(description='Click an element', param_model=ClickElementAction)
	def click_element(params: ClickElementAction, browser=None):
		pass

	@registry.action(
		description='Extract page content',
		param_model=ExtractPageContentAction,
	)
	def extract_page_content(params: ExtractPageContentAction, browser=None):
		pass

	@registry.action(description='Mark task as done', param_model=DoneAction)
	def done(params: DoneAction):
		pass

	# Create the dynamic ActionModel with all registered actions
	return registry.create_action_model()


@pytest.fixture
def sample_history(action_registry):
	# Create actions with nested params structure
	click_action = action_registry(click_element={'index': 1})

	extract_action = action_registry(extract_page_content={'value': 'text'})

	done_action = action_registry(done={'text': 'Task completed'})

	histories = [
		AgentHistory(
			model_output=AgentOutput(
				current_state=AgentBrain(
					evaluation_previous_goal='None',
					memory='Started task',
					next_goal='Click button',
				),
				action=[click_action],
			),
			result=[ActionResult(is_done=False)],
			state=BrowserStateHistory(
				url='https://example.com',
				title='Page 1',
				tabs=[TabInfo(url='https://example.com', title='Page 1', page_id=1)],
				screenshot='screenshot1.png',
				interacted_element=[{'xpath': '//button[1]'}],
			),
		),
		AgentHistory(
			model_output=AgentOutput(
				current_state=AgentBrain(
					evaluation_previous_goal='Clicked button',
					memory='Button clicked',
					next_goal='Extract content',
				),
				action=[extract_action],
			),
			result=[
				ActionResult(
					is_done=False,
					extracted_content='Extracted text',
					error='Failed to extract completely',
				)
			],
			state=BrowserStateHistory(
				url='https://example.com/page2',
				title='Page 2',
				tabs=[TabInfo(url='https://example.com/page2', title='Page 2', page_id=2)],
				screenshot='screenshot2.png',
				interacted_element=[{'xpath': '//div[1]'}],
			),
		),
		AgentHistory(
			model_output=AgentOutput(
				current_state=AgentBrain(
					evaluation_previous_goal='Extracted content',
					memory='Content extracted',
					next_goal='Finish task',
				),
				action=[done_action],
			),
			result=[ActionResult(is_done=True, extracted_content='Task completed', error=None)],
			state=BrowserStateHistory(
				url='https://example.com/page2',
				title='Page 2',
				tabs=[TabInfo(url='https://example.com/page2', title='Page 2', page_id=2)],
				screenshot='screenshot3.png',
				interacted_element=[{'xpath': '//div[1]'}],
			),
		),
	]
	return AgentHistoryList(history=histories)


def test_last_model_output(sample_history: AgentHistoryList):
	last_output = sample_history.last_action()
	print(last_output)
	assert last_output == {'done': {'text': 'Task completed'}}


def test_get_errors(sample_history: AgentHistoryList):
	errors = sample_history.errors()
	assert len(errors) == 1
	assert errors[0] == 'Failed to extract completely'


def test_final_result(sample_history: AgentHistoryList):
	assert sample_history.final_result() == 'Task completed'


def test_is_done(sample_history: AgentHistoryList):
	assert sample_history.is_done() is True


def test_urls(sample_history: AgentHistoryList):
	urls = sample_history.urls()
	assert 'https://example.com' in urls
	assert 'https://example.com/page2' in urls


def test_all_screenshots(sample_history: AgentHistoryList):
	screenshots = sample_history.screenshots()
	assert len(screenshots) == 3
	assert screenshots == ['screenshot1.png', 'screenshot2.png', 'screenshot3.png']


def test_all_model_outputs(sample_history: AgentHistoryList):
	outputs = sample_history.model_actions()
	print(f'DEBUG: {outputs[0]}')
	assert len(outputs) == 3
	# get first key value pair
	assert dict([next(iter(outputs[0].items()))]) == {'click_element': {'index': 1}}
	assert dict([next(iter(outputs[1].items()))]) == {'extract_page_content': {'value': 'text'}}
	assert dict([next(iter(outputs[2].items()))]) == {'done': {'text': 'Task completed'}}


def test_all_model_outputs_filtered(sample_history: AgentHistoryList):
	filtered = sample_history.model_actions_filtered(include=['click_element'])
	assert len(filtered) == 1
	assert filtered[0]['click_element']['index'] == 1


def test_empty_history():
	empty_history = AgentHistoryList(history=[])
	assert empty_history.last_action() is None
	assert empty_history.final_result() is None
	assert empty_history.is_done() is False
	assert len(empty_history.urls()) == 0


# Add a test to verify action creation
def test_action_creation(action_registry):
	click_action = action_registry(click_element={'index': 1})

	assert click_action.model_dump(exclude_none=True) == {'click_element': {'index': 1}}


# run this with:
# pytest browser_use/agent/tests.py
````

## File: browser_use/browser/dolphin_service.py
````python
import logging
import os
from typing import List, Optional

import aiohttp
from patchright.async_api import Page, async_playwright

from browser_use.browser.service import Browser
from browser_use.browser.views import BrowserState, TabInfo

logger = logging.getLogger(__name__)


class DolphinBrowser(Browser):
	"""A class for managing Dolphin Anty browser sessions using Playwright"""

	def __init__(self, headless: bool = False, keep_open: bool = False):
		"""
		Initialize the DolphinBrowser instance.

		Args:
		    headless (bool): Run browser in headless mode (default: False).
		    keep_open (bool): Keep browser open after finishing tasks (default: False).
		"""
		# Retrieve environment variables for API connection
		self.api_token = os.getenv('DOLPHIN_API_TOKEN')
		self.api_url = os.getenv('DOLPHIN_API_URL', 'http://localhost:3001/v1.0')
		self.profile_id = os.getenv('DOLPHIN_PROFILE_ID')

		# Initialize internal attributes
		self.playwright = None
		self.browser = None
		self.context = None
		self.page = None
		self.headless = headless
		self.keep_open = keep_open
		self._pages: List[Page] = []  # List to store open pages
		self.session = None
		self.cached_state = None

	async def get_current_page(self) -> Page:
		"""
		Get the currently active page.

		Raises:
		    Exception: If no active page is available.
		"""
		if not self.page:
			raise Exception('No active page. Browser might not be connected.')
		return self.page

	async def create_new_tab(self, url: str | None = None) -> None:
		"""
		Create a new tab and optionally navigate to a given URL.

		Args:
		    url (str, optional): URL to navigate to after creating the tab. Defaults to None.

		Raises:
		    Exception: If browser context is not initialized or navigation fails.
		"""
		if not self.context:
			raise Exception('Browser context not initialized')

		# Create new page (tab) in the current browser context
		new_page = await self.context.new_page()
		self._pages.append(new_page)
		self.page = new_page  # Set as current page

		if url:
			try:
				# Navigate to the URL and wait for the page to load
				await new_page.goto(url, wait_until='networkidle')
				await self.wait_for_page_load()
			except Exception as e:
				logger.error(f'Failed to navigate to URL {url}: {str(e)}')
				raise

	async def switch_to_tab(self, page_id: int) -> None:
		"""
		Switch to a specific tab by its page ID.

		Args:
		    page_id (int): The index of the tab to switch to.

		Raises:
		    Exception: If the tab index is out of range or no tabs are available.
		"""
		if not self._pages:
			raise Exception('No tabs available')

		# Handle negative indices (e.g., -1 for last tab)
		if page_id < 0:
			page_id = len(self._pages) + page_id

		if page_id >= len(self._pages) or page_id < 0:
			raise Exception(f'Tab index {page_id} out of range')

		# Set the current page to the selected tab
		self.page = self._pages[page_id]
		await self.page.bring_to_front()  # Bring tab to the front
		await self.wait_for_page_load()

	async def get_tabs_info(self) -> list[TabInfo]:
		"""
		Get information about all open tabs.

		Returns:
		    list: A list of TabInfo objects containing details about each tab.
		"""
		tabs_info = []
		for idx, page in enumerate(self._pages):
			tab_info = TabInfo(
				page_id=idx,
				url=page.url,
				title=await page.title(),  # Fetch the title of the page
			)
			tabs_info.append(tab_info)
		return tabs_info

	async def wait_for_page_load(self, timeout: int = 30000):
		"""
		Wait for the page to load completely.

		Args:
		    timeout (int): Maximum time to wait for page load in milliseconds (default: 30000ms).

		Raises:
		    Exception: If the page fails to load within the specified timeout.
		"""
		if self.page:
			try:
				await self.page.wait_for_load_state('networkidle', timeout=timeout)
			except Exception as e:
				logger.warning(f'Wait for page load timeout: {str(e)}')

	async def get_session(self):
		"""
		Get the current session.

		Returns:
		    DolphinBrowser: The current DolphinBrowser instance.

		Raises:
		    Exception: If the browser is not connected.
		"""
		if not self.browser:
			raise Exception('Browser not connected. Call connect() first.')
		self.session = self
		return self

	async def authenticate(self):
		"""
		Authenticate with Dolphin Anty API using the API token.

		Raises:
		    Exception: If authentication fails.
		"""
		async with aiohttp.ClientSession() as session:
			auth_url = f'{self.api_url}/auth/login-with-token'
			auth_data = {'token': self.api_token}
			async with session.post(auth_url, json=auth_data) as response:
				if not response.ok:
					raise Exception(f'Failed to authenticate with Dolphin Anty: {await response.text()}')
				return await response.json()

	async def get_browser_profiles(self):
		"""
		Get a list of available browser profiles from Dolphin Anty.

		Returns:
		    list: A list of browser profiles.

		Raises:
		    Exception: If fetching the browser profiles fails.
		"""
		# Authenticate before fetching profiles
		await self.authenticate()

		async with aiohttp.ClientSession() as session:
			headers = {'Authorization': f'Bearer {self.api_token}'}
			async with session.get(f'{self.api_url}/browser_profiles', headers=headers) as response:
				if not response.ok:
					raise Exception(f'Failed to get browser profiles: {await response.text()}')
				data = await response.json()
				return data.get('data', [])  # Return the profiles array from the response

	async def start_profile(self, profile_id: Optional[str] = None, headless: bool = False) -> dict:
		"""
		Start a browser profile on Dolphin Anty.

		Args:
		    profile_id (str, optional): Profile ID to start (defaults to the one set in the environment).
		    headless (bool): Run browser in headless mode (default: False).

		Returns:
		    dict: Information about the started profile.

		Raises:
		    ValueError: If no profile ID is provided and no default is set.
		    Exception: If starting the profile fails.
		"""
		# Authenticate before starting the profile
		await self.authenticate()

		profile_id = profile_id or self.profile_id
		if not profile_id:
			raise ValueError('No profile ID provided')

		url = f'{self.api_url}/browser_profiles/{profile_id}/start'
		params = {'automation': 1}
		if headless:
			params['headless'] = 1

		async with aiohttp.ClientSession() as session:
			async with session.get(url, params=params) as response:
				if not response.ok:
					raise Exception(f'Failed to start profile: {await response.text()}')
				return await response.json()

	async def stop_profile(self, profile_id: Optional[str] = None):
		"""
		Stop a browser profile on Dolphin Anty.

		Args:
		    profile_id (str, optional): Profile ID to stop (defaults to the one set in the environment).

		Returns:
		    dict: Information about the stopped profile.

		Raises:
		    ValueError: If no profile ID is provided and no default is set.
		"""
		# Authenticate before stopping the profile
		await self.authenticate()

		profile_id = profile_id or self.profile_id
		if not profile_id:
			raise ValueError('No profile ID provided')

		url = f'{self.api_url}/browser_profiles/{profile_id}/stop'
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				return await response.json()

	async def connect(self, profile_id: Optional[str] = None):
		"""
		Connect to a running browser profile using Playwright.

		Args:
		    profile_id (str, optional): Profile ID to connect to (defaults to the one set in the environment).

		Returns:
		    PlaywrightBrowser: The connected browser instance.

		Raises:
		    Exception: If authentication or profile connection fails.
		"""
		# Authenticate before connecting to the profile
		await self.authenticate()

		# Start the browser profile
		profile_data = await self.start_profile(profile_id)

		if not profile_data.get('success'):
			raise Exception(f'Failed to start profile: {profile_data}')

		automation = profile_data['automation']
		port = automation['port']
		ws_endpoint = automation['wsEndpoint']
		ws_url = f'ws://127.0.0.1:{port}{ws_endpoint}'

		# Use Playwright to connect to the browser's WebSocket endpoint
		self.playwright = await async_playwright().start()
		self.browser = await self.playwright.chromium.connect_over_cdp(ws_url)

		# Get or create a browser context and page
		contexts = self.browser.contexts
		self.context = contexts[0] if contexts else await self.browser.new_context()
		pages = self.context.pages
		self.page = pages[0] if pages else await self.context.new_page()

		self._pages = [self.page]  # Initialize pages list with the first page

		return self.browser

	async def close(self, force: bool = False):
		"""
		Close the browser connection and clean up resources.

		Args:
		    force (bool): If True, forcefully stop the associated profile (default: False).
		"""
		try:
			# Close all open pages
			if self._pages:
				for page in self._pages:
					try:
						await page.close()
					except BaseException:
						pass
				self._pages = []

			# Close the browser and Playwright instance
			if self.browser:
				await self.browser.close()

			if self.playwright:
				await self.playwright.stop()

			if force:
				await self.stop_profile()  # Force stop the profile
		except Exception as e:
			logger.error(f'Error during browser cleanup: {str(e)}')

	async def get_current_state(self) -> BrowserState:
		"""
		Get the current state of the browser (URL, content, viewport size, tabs).

		Returns:
		    BrowserState: The current state of the browser.

		Raises:
		    Exception: If no active page is available.
		"""
		if not self.page:
			raise Exception('No active page')

		# Get page content and viewport size
		content = await self.page.content()
		viewport_size = await self.page.viewport_size()

		# Create and return the current browser state
		state = BrowserState(
			url=self.page.url,
			content=content,
			viewport_height=viewport_size['height'] if viewport_size else 0,
			viewport_width=viewport_size['width'] if viewport_size else 0,
			tabs=await self.get_tabs_info(),
		)

		# Cache and return the state
		self.cached_state = state
		return state

	def __del__(self):
		"""Clean up resources when the DolphinBrowser instance is deleted."""
		# No need to handle session cleanup as we're using self as session
		pass
````

## File: browser_use/browser/tests/screenshot_test.py
````python
import asyncio
import base64

import pytest

from browser_use.browser.browser import Browser, BrowserConfig


async def test_take_full_page_screenshot():
	browser = Browser(config=BrowserConfig(headless=False, disable_security=True))
	try:
		async with await browser.new_context() as context:
			page = await context.get_current_page()
			# Go to a test page
			await page.goto('https://example.com')

			await asyncio.sleep(3)
			# Take full page screenshot
			screenshot_b64 = await context.take_screenshot(full_page=True)
			await asyncio.sleep(3)
			# Verify screenshot is not empty and is valid base64
			assert screenshot_b64 is not None
			assert isinstance(screenshot_b64, str)
			assert len(screenshot_b64) > 0

			# Test we can decode the base64 string
			try:
				base64.b64decode(screenshot_b64)
			except Exception as e:
				pytest.fail(f'Failed to decode base64 screenshot: {str(e)}')
	finally:
		await browser.close()


if __name__ == '__main__':
	asyncio.run(test_take_full_page_screenshot())
````

## File: browser_use/browser/tests/test_clicks.py
````python
import asyncio
import json

import anyio
import pytest

from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.dom.views import DOMBaseNode, DOMElementNode, DOMTextNode
from browser_use.utils import time_execution_sync


class ElementTreeSerializer:
	@staticmethod
	def dom_element_node_to_json(element_tree: DOMElementNode) -> dict:
		def node_to_dict(node: DOMBaseNode) -> dict:
			if isinstance(node, DOMTextNode):
				return {'type': 'text', 'text': node.text}
			elif isinstance(node, DOMElementNode):
				return {
					'type': 'element',
					'tag_name': node.tag_name,
					'attributes': node.attributes,
					'highlight_index': node.highlight_index,
					'children': [node_to_dict(child) for child in node.children],
				}
			return {}

		return node_to_dict(element_tree)


# run with: pytest browser_use/browser/tests/test_clicks.py
@pytest.mark.asyncio
async def test_highlight_elements():
	browser = Browser(config=BrowserConfig(headless=False, disable_security=True))

	async with await browser.new_context() as context:
		page = await context.get_current_page()
		# await page.goto('https://immobilienscout24.de')
		# await page.goto('https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/service-plans')
		# await page.goto('https://google.com/search?q=elon+musk')
		# await page.goto('https://kayak.com')
		# await page.goto('https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_iframe')
		# await page.goto('https://dictionary.cambridge.org')
		# await page.goto('https://github.com')
		await page.goto('https://huggingface.co/')

		await asyncio.sleep(1)

		while True:
			try:
				# await asyncio.sleep(10)
				state = await context.get_state(True)

				async with await anyio.open_file('./tmp/page.json', 'w') as f:
					await f.write(
						json.dumps(
							ElementTreeSerializer.dom_element_node_to_json(state.element_tree),
							indent=1,
						)
					)

				# await time_execution_sync('highlight_selector_map_elements')(
				# 	browser.highlight_selector_map_elements
				# )(state.selector_map)

				# Find and print duplicate XPaths
				xpath_counts = {}
				if not state.selector_map:
					continue
				for selector in state.selector_map.values():
					xpath = selector.xpath
					if xpath in xpath_counts:
						xpath_counts[xpath] += 1
					else:
						xpath_counts[xpath] = 1

				print('\nDuplicate XPaths found:')
				for xpath, count in xpath_counts.items():
					if count > 1:
						print(f'XPath: {xpath}')
						print(f'Count: {count}\n')

				print(list(state.selector_map.keys()), 'Selector map keys')
				print(state.element_tree.clickable_elements_to_string())
				action = input('Select next action: ')

				await time_execution_sync('remove_highlight_elements')(context.remove_highlights)()

				node_element = state.selector_map[int(action)]

				# check if index of selector map are the same as index of items in dom_items

				await context._click_element_node(node_element)

			except Exception as e:
				print(e)
````

## File: browser_use/browser/utils/screen_resolution.py
````python
import sys


def get_screen_resolution():
	if sys.platform == 'darwin':  # macOS
		try:
			from AppKit import NSScreen

			screen = NSScreen.mainScreen().frame()
			return {'width': int(screen.size.width), 'height': int(screen.size.height)}
		except ImportError:
			print('AppKit is not available. Make sure you are running this on macOS with pyobjc installed.')
		except Exception as e:
			print(f'Error retrieving macOS screen resolution: {e}')
		return {'width': 2560, 'height': 1664}

	else:  # Windows & Linux
		try:
			from screeninfo import get_monitors

			monitors = get_monitors()
			if not monitors:
				raise Exception('No monitors detected.')
			monitor = monitors[0]
			return {'width': monitor.width, 'height': monitor.height}
		except ImportError:
			print("screeninfo package not found. Install it using 'pip install screeninfo'.")
		except Exception as e:
			print(f'Error retrieving screen resolution: {e}')

		return {'width': 1920, 'height': 1080}


def get_window_adjustments():
	"""Returns recommended x, y offsets for window positioning"""
	if sys.platform == 'darwin':  # macOS
		return -4, 24  # macOS has a small title bar, no border
	elif sys.platform == 'win32':  # Windows
		return -8, 0  # Windows has a border on the left
	else:  # Linux
		return 0, 0
````

## File: browser_use/browser/views.py
````python
from dataclasses import dataclass, field
from typing import Any, Optional

from pydantic import BaseModel

from browser_use.dom.history_tree_processor.service import DOMHistoryElement
from browser_use.dom.views import DOMState


# Pydantic
class TabInfo(BaseModel):
	"""Represents information about a browser tab"""

	page_id: int
	url: str
	title: str
	parent_page_id: Optional[int] = None  # parent page that contains this popup or cross-origin iframe


class GroupTabsAction(BaseModel):
	tab_ids: list[int]
	title: str
	color: Optional[str] = 'blue'


class UngroupTabsAction(BaseModel):
	tab_ids: list[int]


@dataclass
class BrowserState(DOMState):
	url: str
	title: str
	tabs: list[TabInfo]
	screenshot: Optional[str] = None
	pixels_above: int = 0
	pixels_below: int = 0
	browser_errors: list[str] = field(default_factory=list)


@dataclass
class BrowserStateHistory:
	url: str
	title: str
	tabs: list[TabInfo]
	interacted_element: list[DOMHistoryElement | None] | list[None]
	screenshot: Optional[str] = None

	def to_dict(self) -> dict[str, Any]:
		data = {}
		data['tabs'] = [tab.model_dump() for tab in self.tabs]
		data['screenshot'] = self.screenshot
		data['interacted_element'] = [el.to_dict() if el else None for el in self.interacted_element]
		data['url'] = self.url
		data['title'] = self.title
		return data


class BrowserError(Exception):
	"""Base class for all browser errors"""


class URLNotAllowedError(BrowserError):
	"""Error raised when a URL is not allowed"""
````

## File: browser_use/controller/registry/views.py
````python
from typing import Callable, Dict, Type

from patchright.async_api import Page
from pydantic import BaseModel, ConfigDict


class RegisteredAction(BaseModel):
	"""Model for a registered action"""

	name: str
	description: str
	function: Callable
	param_model: Type[BaseModel]

	# filters: provide specific domains or a function to determine whether the action should be available on the given page or not
	domains: list[str] | None = None  # e.g. ['*.google.com', 'www.bing.com', 'yahoo.*]
	page_filter: Callable[[Page], bool] | None = None

	model_config = ConfigDict(arbitrary_types_allowed=True)

	def prompt_description(self) -> str:
		"""Get a description of the action for the prompt"""
		skip_keys = ['title']
		s = f'{self.description}: \n'
		s += '{' + str(self.name) + ': '
		s += str(
			{
				k: {sub_k: sub_v for sub_k, sub_v in v.items() if sub_k not in skip_keys}
				for k, v in self.param_model.model_json_schema()['properties'].items()
			}
		)
		s += '}'
		return s


class ActionModel(BaseModel):
	"""Base model for dynamically created action models"""

	# this will have all the registered actions, e.g.
	# click_element = param_model = ClickElementParams
	# done = param_model = None
	#
	model_config = ConfigDict(arbitrary_types_allowed=True)

	def get_index(self) -> int | None:
		"""Get the index of the action"""
		# {'clicked_element': {'index':5}}
		params = self.model_dump(exclude_unset=True).values()
		if not params:
			return None
		for param in params:
			if param is not None and 'index' in param:
				return param['index']
		return None

	def set_index(self, index: int):
		"""Overwrite the index of the action"""
		# Get the action name and params
		action_data = self.model_dump(exclude_unset=True)
		action_name = next(iter(action_data.keys()))
		action_params = getattr(self, action_name)

		# Update the index directly on the model
		if hasattr(action_params, 'index'):
			action_params.index = index


class ActionRegistry(BaseModel):
	"""Model representing the action registry"""

	actions: Dict[str, RegisteredAction] = {}

	@staticmethod
	def _match_domains(domains: list[str] | None, url: str) -> bool:
		"""
		Match a list of domain glob patterns against a URL.

		Args:
			domain_patterns: A list of domain patterns that can include glob patterns (* wildcard)
			url: The URL to match against

		Returns:
			True if the URL's domain matches the pattern, False otherwise
		"""

		if domains is None or not url:
			return True

		import fnmatch
		from urllib.parse import urlparse

		# Parse the URL to get the domain
		try:
			parsed_url = urlparse(url)
			if not parsed_url.netloc:
				return False

			domain = parsed_url.netloc
			# Remove port if present
			if ':' in domain:
				domain = domain.split(':')[0]

			for domain_pattern in domains:
				if fnmatch.fnmatch(domain, domain_pattern):  # Perform glob *.matching.*
					return True
			return False
		except Exception:
			return False

	@staticmethod
	def _match_page_filter(page_filter: Callable[[Page], bool] | None, page: Page) -> bool:
		"""Match a page filter against a page"""
		if page_filter is None:
			return True
		return page_filter(page)

	def get_prompt_description(self, page: Page | None = None) -> str:
		"""Get a description of all actions for the prompt

		Args:
			page: If provided, filter actions by page using page_filter and domains.

		Returns:
			A string description of available actions.
			- If page is None: return only actions with no page_filter and no domains (for system prompt)
			- If page is provided: return only filtered actions that match the current page (excluding unfiltered actions)
		"""
		if page is None:
			# For system prompt (no page provided), include only actions with no filters
			return '\n'.join(
				action.prompt_description()
				for action in self.actions.values()
				if action.page_filter is None and action.domains is None
			)

		# only include filtered actions for the current page
		filtered_actions = []
		for action in self.actions.values():
			if not (action.domains or action.page_filter):
				# skip actions with no filters, they are already included in the system prompt
				continue

			domain_is_allowed = self._match_domains(action.domains, page.url)
			page_is_allowed = self._match_page_filter(action.page_filter, page)

			if domain_is_allowed and page_is_allowed:
				filtered_actions.append(action)

		return '\n'.join(action.prompt_description() for action in filtered_actions)
````

## File: browser_use/controller/service.py
````python
import asyncio
import enum
import json
import logging
import re
from typing import Dict, Generic, Optional, Tuple, Type, TypeVar, cast

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import PromptTemplate
from patchright.async_api import ElementHandle, Page

# from lmnr.sdk.laminar import Laminar
from pydantic import BaseModel

from browser_use.agent.views import ActionModel, ActionResult
from browser_use.browser.context import BrowserContext
from browser_use.controller.registry.service import Registry
from browser_use.controller.views import (
	ClickElementAction,
	CloseTabAction,
	DoneAction,
	DragDropAction,
	GoToUrlAction,
	InputTextAction,
	NoParamsAction,
	OpenTabAction,
	Position,
	ScrollAction,
	SearchGoogleAction,
	SendKeysAction,
	SwitchTabAction,
)
from browser_use.utils import time_execution_sync

logger = logging.getLogger(__name__)


Context = TypeVar('Context')


class Controller(Generic[Context]):
	def __init__(
		self,
		exclude_actions: list[str] = [],
		output_model: Optional[Type[BaseModel]] = None,
	):
		self.registry = Registry[Context](exclude_actions)

		"""Register all default browser actions"""

		if output_model is not None:
			# Create a new model that extends the output model with success parameter
			class ExtendedOutputModel(BaseModel):  # type: ignore
				success: bool = True
				data: output_model  # type: ignore

			@self.registry.action(
				'Complete task - with return text and if the task is finished (success=True) or not yet  completely finished (success=False), because last step is reached',
				param_model=ExtendedOutputModel,
			)
			async def done(params: ExtendedOutputModel):
				# Exclude success from the output JSON since it's an internal parameter
				output_dict = params.data.model_dump()

				# Enums are not serializable, convert to string
				for key, value in output_dict.items():
					if isinstance(value, enum.Enum):
						output_dict[key] = value.value

				return ActionResult(is_done=True, success=params.success, extracted_content=json.dumps(output_dict))
		else:

			@self.registry.action(
				'Complete task - with return text and if the task is finished (success=True) or not yet  completely finished (success=False), because last step is reached',
				param_model=DoneAction,
			)
			async def done(params: DoneAction):
				return ActionResult(is_done=True, success=params.success, extracted_content=params.text)

		# Basic Navigation Actions
		@self.registry.action(
			'Search the query in Google in the current tab, the query should be a search query like humans search in Google, concrete and not vague or super long. More the single most important items. ',
			param_model=SearchGoogleAction,
		)
		async def search_google(params: SearchGoogleAction, browser: BrowserContext):
			page = await browser.get_current_page()
			await page.goto(f'https://www.google.com/search?q={params.query}&udm=14')
			await page.wait_for_load_state()
			msg = f'🔍  Searched for "{params.query}" in Google'
			logger.info(msg)
			return ActionResult(extracted_content=msg, include_in_memory=True)

		@self.registry.action('Navigate to URL in the current tab', param_model=GoToUrlAction)
		async def go_to_url(params: GoToUrlAction, browser: BrowserContext):
			page = await browser.get_current_page()
			await page.goto(params.url)
			await page.wait_for_load_state()
			msg = f'🔗  Navigated to {params.url}'
			logger.info(msg)
			return ActionResult(extracted_content=msg, include_in_memory=True)

		@self.registry.action('Go back', param_model=NoParamsAction)
		async def go_back(_: NoParamsAction, browser: BrowserContext):
			await browser.go_back()
			msg = '🔙  Navigated back'
			logger.info(msg)
			return ActionResult(extracted_content=msg, include_in_memory=True)

		# wait for x seconds
		@self.registry.action('Wait for x seconds default 3')
		async def wait(seconds: int = 3):
			msg = f'🕒  Waiting for {seconds} seconds'
			logger.info(msg)
			await asyncio.sleep(seconds)
			return ActionResult(extracted_content=msg, include_in_memory=True)

		# Element Interaction Actions
		@self.registry.action('Click element by index', param_model=ClickElementAction)
		async def click_element_by_index(params: ClickElementAction, browser: BrowserContext):
			session = await browser.get_session()

			if params.index not in await browser.get_selector_map():
				raise Exception(f'Element with index {params.index} does not exist - retry or use alternative actions')

			element_node = await browser.get_dom_element_by_index(params.index)
			initial_pages = len(session.context.pages)

			# if element has file uploader then dont click
			if await browser.is_file_uploader(element_node):
				msg = f'Index {params.index} - has an element which opens file upload dialog. To upload files please use a specific function to upload files '
				logger.info(msg)
				return ActionResult(extracted_content=msg, include_in_memory=True)

			msg = None

			try:
				download_path = await browser._click_element_node(element_node)
				if download_path:
					msg = f'💾  Downloaded file to {download_path}'
				else:
					msg = f'🖱️  Clicked button with index {params.index}: {element_node.get_all_text_till_next_clickable_element(max_depth=2)}'

				logger.info(msg)
				logger.debug(f'Element xpath: {element_node.xpath}')
				if len(session.context.pages) > initial_pages:
					new_tab_msg = 'New tab opened - switching to it'
					msg += f' - {new_tab_msg}'
					logger.info(new_tab_msg)
					await browser.switch_to_tab(-1)
				return ActionResult(extracted_content=msg, include_in_memory=True)
			except Exception as e:
				logger.warning(f'Element not clickable with index {params.index} - most likely the page changed')
				return ActionResult(error=str(e))

		@self.registry.action(
			'Input text into a input interactive element',
			param_model=InputTextAction,
		)
		async def input_text(params: InputTextAction, browser: BrowserContext, has_sensitive_data: bool = False):
			if params.index not in await browser.get_selector_map():
				raise Exception(f'Element index {params.index} does not exist - retry or use alternative actions')

			element_node = await browser.get_dom_element_by_index(params.index)
			await browser._input_text_element_node(element_node, params.text)
			if not has_sensitive_data:
				msg = f'⌨️  Input {params.text} into index {params.index}'
			else:
				msg = f'⌨️  Input sensitive data into index {params.index}'
			logger.info(msg)
			logger.debug(f'Element xpath: {element_node.xpath}')
			return ActionResult(extracted_content=msg, include_in_memory=True)

		# Save PDF
		@self.registry.action(
			'Save the current page as a PDF file',
		)
		async def save_pdf(browser: BrowserContext):
			page = await browser.get_current_page()
			short_url = re.sub(r'^https?://(?:www\.)?|/$', '', page.url)
			slug = re.sub(r'[^a-zA-Z0-9]+', '-', short_url).strip('-').lower()
			sanitized_filename = f'{slug}.pdf'

			await page.emulate_media(media='screen')
			await page.pdf(path=sanitized_filename, format='A4', print_background=False)
			msg = f'Saving page with URL {page.url} as PDF to ./{sanitized_filename}'
			logger.info(msg)
			return ActionResult(extracted_content=msg, include_in_memory=True)

		# Tab Management Actions
		@self.registry.action('Switch tab', param_model=SwitchTabAction)
		async def switch_tab(params: SwitchTabAction, browser: BrowserContext):
			await browser.switch_to_tab(params.page_id)
			# Wait for tab to be ready
			page = await browser.get_current_page()
			await page.wait_for_load_state()
			msg = f'🔄  Switched to tab {params.page_id}'
			logger.info(msg)
			return ActionResult(extracted_content=msg, include_in_memory=True)

		@self.registry.action('Open url in new tab', param_model=OpenTabAction)
		async def open_tab(params: OpenTabAction, browser: BrowserContext):
			await browser.create_new_tab(params.url)
			msg = f'🔗  Opened new tab with {params.url}'
			logger.info(msg)
			return ActionResult(extracted_content=msg, include_in_memory=True)

		@self.registry.action('Close an existing tab', param_model=CloseTabAction)
		async def close_tab(params: CloseTabAction, browser: BrowserContext):
			await browser.switch_to_tab(params.page_id)
			page = await browser.get_current_page()
			url = page.url
			await page.close()
			msg = f'❌  Closed tab #{params.page_id} with url {url}'
			logger.info(msg)
			return ActionResult(extracted_content=msg, include_in_memory=True)

		# Content Actions
		@self.registry.action(
			'Extract page content to retrieve specific information from the page, e.g. all company names, a specific description, all information about, links with companies in structured format or simply links',
		)
		async def extract_content(
			goal: str, should_strip_link_urls: bool, browser: BrowserContext, page_extraction_llm: BaseChatModel
		):
			page = await browser.get_current_page()
			import markdownify

			strip = []
			if should_strip_link_urls:
				strip = ['a', 'img']


			print('page.content() ASS:', page.content())
			content = markdownify.markdownify(await page.content(), strip=strip)

			# manually append iframe text into the content so it's readable by the LLM (includes cross-origin iframes)
			for iframe in page.frames:
				if iframe.url != page.url and not iframe.url.startswith('data:'):
					content += f'\n\nIFRAME {iframe.url}:\n'
					content += markdownify.markdownify(await iframe.content())

			prompt = 'Your task is to extract the content of the page. You will be given a page and a goal and you should extract all relevant information around this goal from the page. If the goal is vague, summarize the page. Respond in json format. Extraction goal: {goal}, Page: {page}'
			template = PromptTemplate(input_variables=['goal', 'page'], template=prompt)
			try:
				output = await page_extraction_llm.ainvoke(template.format(goal=goal, page=content))
				msg = f'📄  Extracted from page\n: {output.content}\n'
				logger.info(msg)
				return ActionResult(extracted_content=msg, include_in_memory=True)
			except Exception as e:
				logger.debug(f'Error extracting content: {e}')
				msg = f'📄  Extracted from page\n: {content}\n'
				logger.info(msg)
				return ActionResult(extracted_content=msg)

		@self.registry.action(
			'Scroll down the page by pixel amount - if no amount is specified, scroll down one page',
			param_model=ScrollAction,
		)
		async def scroll_down(params: ScrollAction, browser: BrowserContext):
			page = await browser.get_current_page()
			if params.amount is not None:
				await page.evaluate(f'window.scrollBy(0, {params.amount});')
			else:
				await page.evaluate('window.scrollBy(0, window.innerHeight);')

			amount = f'{params.amount} pixels' if params.amount is not None else 'one page'
			msg = f'🔍  Scrolled down the page by {amount}'
			logger.info(msg)
			return ActionResult(
				extracted_content=msg,
				include_in_memory=True,
			)

		# scroll up
		@self.registry.action(
			'Scroll up the page by pixel amount - if no amount is specified, scroll up one page',
			param_model=ScrollAction,
		)
		async def scroll_up(params: ScrollAction, browser: BrowserContext):
			page = await browser.get_current_page()
			if params.amount is not None:
				await page.evaluate(f'window.scrollBy(0, -{params.amount});')
			else:
				await page.evaluate('window.scrollBy(0, -window.innerHeight);')

			amount = f'{params.amount} pixels' if params.amount is not None else 'one page'
			msg = f'🔍  Scrolled up the page by {amount}'
			logger.info(msg)
			return ActionResult(
				extracted_content=msg,
				include_in_memory=True,
			)

		# send keys
		@self.registry.action(
			'Send strings of special keys like Escape,Backspace, Insert, PageDown, Delete, Enter, Shortcuts such as `Control+o`, `Control+Shift+T` are supported as well. This gets used in keyboard.press. ',
			param_model=SendKeysAction,
		)
		async def send_keys(params: SendKeysAction, browser: BrowserContext):
			page = await browser.get_current_page()

			try:
				await page.keyboard.press(params.keys)
			except Exception as e:
				if 'Unknown key' in str(e):
					# loop over the keys and try to send each one
					for key in params.keys:
						try:
							await page.keyboard.press(key)
						except Exception as e:
							logger.debug(f'Error sending key {key}: {str(e)}')
							raise e
				else:
					raise e
			msg = f'⌨️  Sent keys: {params.keys}'
			logger.info(msg)
			return ActionResult(extracted_content=msg, include_in_memory=True)

		@self.registry.action(
			description='If you dont find something which you want to interact with, scroll to it',
		)
		async def scroll_to_text(text: str, browser: BrowserContext):  # type: ignore
			page = await browser.get_current_page()
			try:
				# Try different locator strategies
				locators = [
					page.get_by_text(text, exact=False),
					page.locator(f'text={text}'),
					page.locator(f"//*[contains(text(), '{text}')]"),
				]

				for locator in locators:
					try:
						# First check if element exists and is visible
						if await locator.count() > 0 and await locator.first.is_visible():
							await locator.first.scroll_into_view_if_needed()
							await asyncio.sleep(0.5)  # Wait for scroll to complete
							msg = f'🔍  Scrolled to text: {text}'
							logger.info(msg)
							return ActionResult(extracted_content=msg, include_in_memory=True)
					except Exception as e:
						logger.debug(f'Locator attempt failed: {str(e)}')
						continue

				msg = f"Text '{text}' not found or not visible on page"
				logger.info(msg)
				return ActionResult(extracted_content=msg, include_in_memory=True)

			except Exception as e:
				msg = f"Failed to scroll to text '{text}': {str(e)}"
				logger.error(msg)
				return ActionResult(error=msg, include_in_memory=True)

		@self.registry.action(
			description='Get all options from a native dropdown',
		)
		async def get_dropdown_options(index: int, browser: BrowserContext) -> ActionResult:
			"""Get all options from a native dropdown"""
			page = await browser.get_current_page()
			selector_map = await browser.get_selector_map()
			dom_element = selector_map[index]

			try:
				# Frame-aware approach since we know it works
				all_options = []
				frame_index = 0

				for frame in page.frames:
					try:
						options = await frame.evaluate(
							"""
							(xpath) => {
								const select = document.evaluate(xpath, document, null,
									XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
								if (!select) return null;

								return {
									options: Array.from(select.options).map(opt => ({
										text: opt.text, //do not trim, because we are doing exact match in select_dropdown_option
										value: opt.value,
										index: opt.index
									})),
									id: select.id,
									name: select.name
								};
							}
						""",
							dom_element.xpath,
						)

						if options:
							logger.debug(f'Found dropdown in frame {frame_index}')
							logger.debug(f'Dropdown ID: {options["id"]}, Name: {options["name"]}')

							formatted_options = []
							for opt in options['options']:
								# encoding ensures AI uses the exact string in select_dropdown_option
								encoded_text = json.dumps(opt['text'])
								formatted_options.append(f'{opt["index"]}: text={encoded_text}')

							all_options.extend(formatted_options)

					except Exception as frame_e:
						logger.debug(f'Frame {frame_index} evaluation failed: {str(frame_e)}')

					frame_index += 1

				if all_options:
					msg = '\n'.join(all_options)
					msg += '\nUse the exact text string in select_dropdown_option'
					logger.info(msg)
					return ActionResult(extracted_content=msg, include_in_memory=True)
				else:
					msg = 'No options found in any frame for dropdown'
					logger.info(msg)
					return ActionResult(extracted_content=msg, include_in_memory=True)

			except Exception as e:
				logger.error(f'Failed to get dropdown options: {str(e)}')
				msg = f'Error getting options: {str(e)}'
				logger.info(msg)
				return ActionResult(extracted_content=msg, include_in_memory=True)

		@self.registry.action(
			description='Select dropdown option for interactive element index by the text of the option you want to select',
		)
		async def select_dropdown_option(
			index: int,
			text: str,
			browser: BrowserContext,
		) -> ActionResult:
			"""Select dropdown option by the text of the option you want to select"""
			page = await browser.get_current_page()
			selector_map = await browser.get_selector_map()
			dom_element = selector_map[index]

			# Validate that we're working with a select element
			if dom_element.tag_name != 'select':
				logger.error(f'Element is not a select! Tag: {dom_element.tag_name}, Attributes: {dom_element.attributes}')
				msg = f'Cannot select option: Element with index {index} is a {dom_element.tag_name}, not a select'
				return ActionResult(extracted_content=msg, include_in_memory=True)

			logger.debug(f"Attempting to select '{text}' using xpath: {dom_element.xpath}")
			logger.debug(f'Element attributes: {dom_element.attributes}')
			logger.debug(f'Element tag: {dom_element.tag_name}')

			xpath = '//' + dom_element.xpath

			try:
				frame_index = 0
				for frame in page.frames:
					try:
						logger.debug(f'Trying frame {frame_index} URL: {frame.url}')

						# First verify we can find the dropdown in this frame
						find_dropdown_js = """
							(xpath) => {
								try {
									const select = document.evaluate(xpath, document, null,
										XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
									if (!select) return null;
									if (select.tagName.toLowerCase() !== 'select') {
										return {
											error: `Found element but it's a ${select.tagName}, not a SELECT`,
											found: false
										};
									}
									return {
										id: select.id,
										name: select.name,
										found: true,
										tagName: select.tagName,
										optionCount: select.options.length,
										currentValue: select.value,
										availableOptions: Array.from(select.options).map(o => o.text.trim())
									};
								} catch (e) {
									return {error: e.toString(), found: false};
								}
							}
						"""

						dropdown_info = await frame.evaluate(find_dropdown_js, dom_element.xpath)

						if dropdown_info:
							if not dropdown_info.get('found'):
								logger.error(f'Frame {frame_index} error: {dropdown_info.get("error")}')
								continue

							logger.debug(f'Found dropdown in frame {frame_index}: {dropdown_info}')

							# "label" because we are selecting by text
							# nth(0) to disable error thrown by strict mode
							# timeout=1000 because we are already waiting for all network events, therefore ideally we don't need to wait a lot here (default 30s)
							selected_option_values = (
								await frame.locator('//' + dom_element.xpath).nth(0).select_option(label=text, timeout=1000)
							)

							msg = f'selected option {text} with value {selected_option_values}'
							logger.info(msg + f' in frame {frame_index}')

							return ActionResult(extracted_content=msg, include_in_memory=True)

					except Exception as frame_e:
						logger.error(f'Frame {frame_index} attempt failed: {str(frame_e)}')
						logger.error(f'Frame type: {type(frame)}')
						logger.error(f'Frame URL: {frame.url}')

					frame_index += 1

				msg = f"Could not select option '{text}' in any frame"
				logger.info(msg)
				return ActionResult(extracted_content=msg, include_in_memory=True)

			except Exception as e:
				msg = f'Selection failed: {str(e)}'
				logger.error(msg)
				return ActionResult(error=msg, include_in_memory=True)

		@self.registry.action(
			'Drag and drop elements or between coordinates on the page - useful for canvas drawing, sortable lists, sliders, file uploads, and UI rearrangement',
			param_model=DragDropAction,
		)
		async def drag_drop(params: DragDropAction, browser: BrowserContext) -> ActionResult:
			"""
			Performs a precise drag and drop operation between elements or coordinates.
			"""

			async def get_drag_elements(
				page: Page,
				source_selector: str,
				target_selector: str,
			) -> Tuple[Optional[ElementHandle], Optional[ElementHandle]]:
				"""Get source and target elements with appropriate error handling."""
				source_element = None
				target_element = None

				try:
					# page.locator() auto-detects CSS and XPath
					source_locator = page.locator(source_selector)
					target_locator = page.locator(target_selector)

					# Check if elements exist
					source_count = await source_locator.count()
					target_count = await target_locator.count()

					if source_count > 0:
						source_element = await source_locator.first.element_handle()
						logger.debug(f'Found source element with selector: {source_selector}')
					else:
						logger.warning(f'Source element not found: {source_selector}')

					if target_count > 0:
						target_element = await target_locator.first.element_handle()
						logger.debug(f'Found target element with selector: {target_selector}')
					else:
						logger.warning(f'Target element not found: {target_selector}')

				except Exception as e:
					logger.error(f'Error finding elements: {str(e)}')

				return source_element, target_element

			async def get_element_coordinates(
				source_element: ElementHandle,
				target_element: ElementHandle,
				source_position: Optional[Position],
				target_position: Optional[Position],
			) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
				"""Get coordinates from elements with appropriate error handling."""
				source_coords = None
				target_coords = None

				try:
					# Get source coordinates
					if source_position:
						source_coords = (source_position.x, source_position.y)
					else:
						source_box = await source_element.bounding_box()
						if source_box:
							source_coords = (
								int(source_box['x'] + source_box['width'] / 2),
								int(source_box['y'] + source_box['height'] / 2),
							)

					# Get target coordinates
					if target_position:
						target_coords = (target_position.x, target_position.y)
					else:
						target_box = await target_element.bounding_box()
						if target_box:
							target_coords = (
								int(target_box['x'] + target_box['width'] / 2),
								int(target_box['y'] + target_box['height'] / 2),
							)
				except Exception as e:
					logger.error(f'Error getting element coordinates: {str(e)}')

				return source_coords, target_coords

			async def execute_drag_operation(
				page: Page,
				source_x: int,
				source_y: int,
				target_x: int,
				target_y: int,
				steps: int,
				delay_ms: int,
			) -> Tuple[bool, str]:
				"""Execute the drag operation with comprehensive error handling."""
				try:
					# Try to move to source position
					try:
						await page.mouse.move(source_x, source_y)
						logger.debug(f'Moved to source position ({source_x}, {source_y})')
					except Exception as e:
						logger.error(f'Failed to move to source position: {str(e)}')
						return False, f'Failed to move to source position: {str(e)}'

					# Press mouse button down
					await page.mouse.down()

					# Move to target position with intermediate steps
					for i in range(1, steps + 1):
						ratio = i / steps
						intermediate_x = int(source_x + (target_x - source_x) * ratio)
						intermediate_y = int(source_y + (target_y - source_y) * ratio)

						await page.mouse.move(intermediate_x, intermediate_y)

						if delay_ms > 0:
							await asyncio.sleep(delay_ms / 1000)

					# Move to final target position
					await page.mouse.move(target_x, target_y)

					# Move again to ensure dragover events are properly triggered
					await page.mouse.move(target_x, target_y)

					# Release mouse button
					await page.mouse.up()

					return True, 'Drag operation completed successfully'

				except Exception as e:
					return False, f'Error during drag operation: {str(e)}'

			page = await browser.get_current_page()

			try:
				# Initialize variables
				source_x: Optional[int] = None
				source_y: Optional[int] = None
				target_x: Optional[int] = None
				target_y: Optional[int] = None

				# Normalize parameters
				steps = max(1, params.steps or 10)
				delay_ms = max(0, params.delay_ms or 5)

				# Case 1: Element selectors provided
				if params.element_source and params.element_target:
					logger.debug('Using element-based approach with selectors')

					source_element, target_element = await get_drag_elements(
						page,
						params.element_source,
						params.element_target,
					)

					if not source_element or not target_element:
						error_msg = f'Failed to find {"source" if not source_element else "target"} element'
						return ActionResult(error=error_msg, include_in_memory=True)

					source_coords, target_coords = await get_element_coordinates(
						source_element, target_element, params.element_source_offset, params.element_target_offset
					)

					if not source_coords or not target_coords:
						error_msg = f'Failed to determine {"source" if not source_coords else "target"} coordinates'
						return ActionResult(error=error_msg, include_in_memory=True)

					source_x, source_y = source_coords
					target_x, target_y = target_coords

				# Case 2: Coordinates provided directly
				elif all(
					coord is not None
					for coord in [params.coord_source_x, params.coord_source_y, params.coord_target_x, params.coord_target_y]
				):
					logger.debug('Using coordinate-based approach')
					source_x = params.coord_source_x
					source_y = params.coord_source_y
					target_x = params.coord_target_x
					target_y = params.coord_target_y
				else:
					error_msg = 'Must provide either source/target selectors or source/target coordinates'
					return ActionResult(error=error_msg, include_in_memory=True)

				# Validate coordinates
				if any(coord is None for coord in [source_x, source_y, target_x, target_y]):
					error_msg = 'Failed to determine source or target coordinates'
					return ActionResult(error=error_msg, include_in_memory=True)

				# Perform the drag operation
				success, message = await execute_drag_operation(
					page,
					cast(int, source_x),
					cast(int, source_y),
					cast(int, target_x),
					cast(int, target_y),
					steps,
					delay_ms,
				)

				if not success:
					logger.error(f'Drag operation failed: {message}')
					return ActionResult(error=message, include_in_memory=True)

				# Create descriptive message
				if params.element_source and params.element_target:
					msg = f"🖱️ Dragged element '{params.element_source}' to '{params.element_target}'"
				else:
					msg = f'🖱️ Dragged from ({source_x}, {source_y}) to ({target_x}, {target_y})'

				logger.info(msg)
				return ActionResult(extracted_content=msg, include_in_memory=True)

			except Exception as e:
				error_msg = f'Failed to perform drag and drop: {str(e)}'
				logger.error(error_msg)
				return ActionResult(error=error_msg, include_in_memory=True)

	# Register ---------------------------------------------------------------

	def action(self, description: str, **kwargs):
		"""Decorator for registering custom actions

		@param description: Describe the LLM what the function does (better description == better function calling)
		"""
		return self.registry.action(description, **kwargs)

	# Act --------------------------------------------------------------------

	@time_execution_sync('--act')
	async def act(
		self,
		action: ActionModel,
		browser_context: BrowserContext,
		#
		page_extraction_llm: Optional[BaseChatModel] = None,
		sensitive_data: Optional[Dict[str, str]] = None,
		available_file_paths: Optional[list[str]] = None,
		#
		context: Context | None = None,
	) -> ActionResult:
		"""Execute an action"""

		try:
			for action_name, params in action.model_dump(exclude_unset=True).items():
				if params is not None:
					# with Laminar.start_as_current_span(
					# 	name=action_name,
					# 	input={
					# 		'action': action_name,
					# 		'params': params,
					# 	},
					# 	span_type='TOOL',
					# ):
					result = await self.registry.execute_action(
						action_name,
						params,
						browser=browser_context,
						page_extraction_llm=page_extraction_llm,
						sensitive_data=sensitive_data,
						available_file_paths=available_file_paths,
						context=context,
					)

					# Laminar.set_span_output(result)

					if isinstance(result, str):
						return ActionResult(extracted_content=result)
					elif isinstance(result, ActionResult):
						return result
					elif result is None:
						return ActionResult()
					else:
						raise ValueError(f'Invalid action result type: {type(result)} of {result}')
			return ActionResult()
		except Exception as e:
			raise e
````

## File: browser_use/controller/views.py
````python
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


# Action Input Models
class SearchGoogleAction(BaseModel):
	query: str


class GoToUrlAction(BaseModel):
	url: str


class ClickElementAction(BaseModel):
	index: int
	xpath: Optional[str] = None


class InputTextAction(BaseModel):
	index: int
	text: str
	xpath: Optional[str] = None


class DoneAction(BaseModel):
	text: str
	success: bool


class SwitchTabAction(BaseModel):
	page_id: int


class OpenTabAction(BaseModel):
	url: str


class CloseTabAction(BaseModel):
	page_id: int


class ScrollAction(BaseModel):
	amount: Optional[int] = None  # The number of pixels to scroll. If None, scroll down/up one page


class SendKeysAction(BaseModel):
	keys: str


class GroupTabsAction(BaseModel):
	tab_ids: list[int] = Field(..., description='List of tab IDs to group')
	title: str = Field(..., description='Name for the tab group')
	color: Optional[str] = Field(
		'blue',
		description='Color for the group (grey/blue/red/yellow/green/pink/purple/cyan)',
	)


class UngroupTabsAction(BaseModel):
	tab_ids: list[int] = Field(..., description='List of tab IDs to ungroup')


class ExtractPageContentAction(BaseModel):
	value: str


class NoParamsAction(BaseModel):
	"""
	Accepts absolutely anything in the incoming data
	and discards it, so the final parsed model is empty.
	"""

	model_config = ConfigDict(extra='allow')

	@model_validator(mode='before')
	def ignore_all_inputs(cls, values):
		# No matter what the user sends, discard it and return empty.
		return {}


class Position(BaseModel):
	x: int
	y: int


class DragDropAction(BaseModel):
	# Element-based approach
	element_source: Optional[str] = Field(None, description='CSS selector or XPath of the element to drag from')
	element_target: Optional[str] = Field(None, description='CSS selector or XPath of the element to drop onto')
	element_source_offset: Optional[Position] = Field(
		None, description='Precise position within the source element to start drag (in pixels from top-left corner)'
	)
	element_target_offset: Optional[Position] = Field(
		None, description='Precise position within the target element to drop (in pixels from top-left corner)'
	)

	# Coordinate-based approach (used if selectors not provided)
	coord_source_x: Optional[int] = Field(None, description='Absolute X coordinate on page to start drag from (in pixels)')
	coord_source_y: Optional[int] = Field(None, description='Absolute Y coordinate on page to start drag from (in pixels)')
	coord_target_x: Optional[int] = Field(None, description='Absolute X coordinate on page to drop at (in pixels)')
	coord_target_y: Optional[int] = Field(None, description='Absolute Y coordinate on page to drop at (in pixels)')

	# Common options
	steps: Optional[int] = Field(10, description='Number of intermediate points for smoother movement (5-20 recommended)')
	delay_ms: Optional[int] = Field(5, description='Delay in milliseconds between steps (0 for fastest, 10-20 for more natural)')
````

## File: browser_use/dom/buildDomTree.js
````javascript
(
  args = {
    doHighlightElements: true,
    focusHighlightIndex: -1,
    viewportExpansion: 0,
    debugMode: false,
  }
) => {
  const { doHighlightElements, focusHighlightIndex, viewportExpansion, debugMode } = args;
  let highlightIndex = 0; // Reset highlight index

  // Add timing stack to handle recursion
  const TIMING_STACK = {
    nodeProcessing: [],
    treeTraversal: [],
    highlighting: [],
    current: null
  };

  function pushTiming(type) {
    TIMING_STACK[type] = TIMING_STACK[type] || [];
    TIMING_STACK[type].push(performance.now());
  }

  function popTiming(type) {
    const start = TIMING_STACK[type].pop();
    const duration = performance.now() - start;
    return duration;
  }

  // Only initialize performance tracking if in debug mode
  const PERF_METRICS = debugMode ? {
    buildDomTreeCalls: 0,
    timings: {
      buildDomTree: 0,
      highlightElement: 0,
      isInteractiveElement: 0,
      isElementVisible: 0,
      isTopElement: 0,
      isInExpandedViewport: 0,
      isTextNodeVisible: 0,
      getEffectiveScroll: 0,
    },
    cacheMetrics: {
      boundingRectCacheHits: 0,
      boundingRectCacheMisses: 0,
      computedStyleCacheHits: 0,
      computedStyleCacheMisses: 0,
      getBoundingClientRectTime: 0,
      getComputedStyleTime: 0,
      boundingRectHitRate: 0,
      computedStyleHitRate: 0,
      overallHitRate: 0,
    },
    nodeMetrics: {
      totalNodes: 0,
      processedNodes: 0,
      skippedNodes: 0,
    },
    buildDomTreeBreakdown: {
      totalTime: 0,
      totalSelfTime: 0,
      buildDomTreeCalls: 0,
      domOperations: {
        getBoundingClientRect: 0,
        getComputedStyle: 0,
      },
      domOperationCounts: {
        getBoundingClientRect: 0,
        getComputedStyle: 0,
      }
    }
  } : null;

  // Simple timing helper that only runs in debug mode
  function measureTime(fn) {
    if (!debugMode) return fn;
    return function (...args) {
      const start = performance.now();
      const result = fn.apply(this, args);
      const duration = performance.now() - start;
      return result;
    };
  }

  // Helper to measure DOM operations
  function measureDomOperation(operation, name) {
    if (!debugMode) return operation();

    const start = performance.now();
    const result = operation();
    const duration = performance.now() - start;

    if (PERF_METRICS && name in PERF_METRICS.buildDomTreeBreakdown.domOperations) {
      PERF_METRICS.buildDomTreeBreakdown.domOperations[name] += duration;
      PERF_METRICS.buildDomTreeBreakdown.domOperationCounts[name]++;
    }

    return result;
  }

  // Add caching mechanisms at the top level
  const DOM_CACHE = {
    boundingRects: new WeakMap(),
    computedStyles: new WeakMap(),
    clearCache: () => {
      DOM_CACHE.boundingRects = new WeakMap();
      DOM_CACHE.computedStyles = new WeakMap();
    }
  };

  // Cache helper functions
  function getCachedBoundingRect(element) {
    if (!element) return null;

    if (DOM_CACHE.boundingRects.has(element)) {
      if (debugMode && PERF_METRICS) {
        PERF_METRICS.cacheMetrics.boundingRectCacheHits++;
      }
      return DOM_CACHE.boundingRects.get(element);
    }

    if (debugMode && PERF_METRICS) {
      PERF_METRICS.cacheMetrics.boundingRectCacheMisses++;
    }

    let rect;
    if (debugMode) {
      const start = performance.now();
      rect = element.getBoundingClientRect();
      const duration = performance.now() - start;
      if (PERF_METRICS) {
        PERF_METRICS.buildDomTreeBreakdown.domOperations.getBoundingClientRect += duration;
        PERF_METRICS.buildDomTreeBreakdown.domOperationCounts.getBoundingClientRect++;
      }
    } else {
      rect = element.getBoundingClientRect();
    }

    if (rect) {
      DOM_CACHE.boundingRects.set(element, rect);
    }
    return rect;
  }

  function getCachedComputedStyle(element) {
    if (!element) return null;

    if (DOM_CACHE.computedStyles.has(element)) {
      if (debugMode && PERF_METRICS) {
        PERF_METRICS.cacheMetrics.computedStyleCacheHits++;
      }
      return DOM_CACHE.computedStyles.get(element);
    }

    if (debugMode && PERF_METRICS) {
      PERF_METRICS.cacheMetrics.computedStyleCacheMisses++;
    }

    let style;
    if (debugMode) {
      const start = performance.now();
      style = window.getComputedStyle(element);
      const duration = performance.now() - start;
      if (PERF_METRICS) {
        PERF_METRICS.buildDomTreeBreakdown.domOperations.getComputedStyle += duration;
        PERF_METRICS.buildDomTreeBreakdown.domOperationCounts.getComputedStyle++;
      }
    } else {
      style = window.getComputedStyle(element);
    }

    if (style) {
      DOM_CACHE.computedStyles.set(element, style);
    }
    return style;
  }

  /**
   * Hash map of DOM nodes indexed by their highlight index.
   *
   * @type {Object<string, any>}
   */
  const DOM_HASH_MAP = {};

  const ID = { current: 0 };

  const HIGHLIGHT_CONTAINER_ID = "playwright-highlight-container";

  /**
   * Highlights an element in the DOM and returns the index of the next element.
   */
  function highlightElement(element, index, parentIframe = null) {
    if (!element) return index;

    // Store overlays and the single label for updating
    const overlays = [];
    let label = null;
    let labelWidth = 20; // Approximate label width
    let labelHeight = 16; // Approximate label height

    try {
      // Create or get highlight container
      let container = document.getElementById(HIGHLIGHT_CONTAINER_ID);
      if (!container) {
        container = document.createElement("div");
        container.id = HIGHLIGHT_CONTAINER_ID;
        container.style.position = "fixed";
        container.style.pointerEvents = "none";
        container.style.top = "0";
        container.style.left = "0";
        container.style.width = "100%";
        container.style.height = "100%";
        container.style.zIndex = "2147483647";
        container.style.backgroundColor = 'transparent';
        document.body.appendChild(container);
      }

      // Get element client rects
      const rects = element.getClientRects(); // Use getClientRects()

      if (!rects || rects.length === 0) return index; // Exit if no rects

      // Generate a color based on the index
      const colors = [
        "#FF0000",
        "#00FF00",
        "#0000FF",
        "#FFA500",
        "#800080",
        "#008080",
        "#FF69B4",
        "#4B0082",
        "#FF4500",
        "#2E8B57",
        "#DC143C",
        "#4682B4",
      ];
      const colorIndex = index % colors.length;
      const baseColor = colors[colorIndex];
      const backgroundColor = baseColor + "1A"; // 10% opacity version of the color

      // Get iframe offset if necessary
      let iframeOffset = { x: 0, y: 0 };
      if (parentIframe) {
        const iframeRect = parentIframe.getBoundingClientRect(); // Keep getBoundingClientRect for iframe offset
        iframeOffset.x = iframeRect.left;
        iframeOffset.y = iframeRect.top;
      }

      // Create highlight overlays for each client rect
      for (const rect of rects) {
        if (rect.width === 0 || rect.height === 0) continue; // Skip empty rects

        const overlay = document.createElement("div");
        overlay.style.position = "fixed";
        overlay.style.border = `2px solid ${baseColor}`;
        overlay.style.backgroundColor = backgroundColor;
        overlay.style.pointerEvents = "none";
        overlay.style.boxSizing = "border-box";

        const top = rect.top + iframeOffset.y;
        const left = rect.left + iframeOffset.x;

        overlay.style.top = `${top}px`;
        overlay.style.left = `${left}px`;
        overlay.style.width = `${rect.width}px`;
        overlay.style.height = `${rect.height}px`;

        container.appendChild(overlay);
        overlays.push({ element: overlay, initialRect: rect }); // Store overlay and its rect
      }

      // Create and position a single label relative to the first rect
      const firstRect = rects[0];
      label = document.createElement("div");
      label.className = "playwright-highlight-label";
      label.style.position = "fixed";
      label.style.background = baseColor;
      label.style.color = "white";
      label.style.padding = "1px 4px";
      label.style.borderRadius = "4px";
      label.style.fontSize = `${Math.min(12, Math.max(8, firstRect.height / 2))}px`;
      label.textContent = index;

      labelWidth = label.offsetWidth > 0 ? label.offsetWidth : labelWidth; // Update actual width if possible
      labelHeight = label.offsetHeight > 0 ? label.offsetHeight : labelHeight; // Update actual height if possible

      const firstRectTop = firstRect.top + iframeOffset.y;
      const firstRectLeft = firstRect.left + iframeOffset.x;

      let labelTop = firstRectTop + 2;
      let labelLeft = firstRectLeft + firstRect.width - labelWidth - 2;

      // Adjust label position if first rect is too small
      if (firstRect.width < labelWidth + 4 || firstRect.height < labelHeight + 4) {
        labelTop = firstRectTop - labelHeight - 2;
        labelLeft = firstRectLeft + firstRect.width - labelWidth; // Align with right edge
        if (labelLeft < iframeOffset.x) labelLeft = firstRectLeft; // Prevent going off-left
      }

      // Ensure label stays within viewport bounds slightly better
      labelTop = Math.max(0, Math.min(labelTop, window.innerHeight - labelHeight));
      labelLeft = Math.max(0, Math.min(labelLeft, window.innerWidth - labelWidth));


      label.style.top = `${labelTop}px`;
      label.style.left = `${labelLeft}px`;

      container.appendChild(label);

      // Update positions on scroll/resize
      const updatePositions = () => {
        const newRects = element.getClientRects(); // Get fresh rects
        let newIframeOffset = { x: 0, y: 0 };

        if (parentIframe) {
          const iframeRect = parentIframe.getBoundingClientRect(); // Keep getBoundingClientRect for iframe
          newIframeOffset.x = iframeRect.left;
          newIframeOffset.y = iframeRect.top;
        }

        // Update each overlay
        overlays.forEach((overlayData, i) => {
          if (i < newRects.length) { // Check if rect still exists
            const newRect = newRects[i];
            const newTop = newRect.top + newIframeOffset.y;
            const newLeft = newRect.left + newIframeOffset.x;

            overlayData.element.style.top = `${newTop}px`;
            overlayData.element.style.left = `${newLeft}px`;
            overlayData.element.style.width = `${newRect.width}px`;
            overlayData.element.style.height = `${newRect.height}px`;
            overlayData.element.style.display = (newRect.width === 0 || newRect.height === 0) ? 'none' : 'block';
          } else {
            // If fewer rects now, hide extra overlays
            overlayData.element.style.display = 'none';
          }
        });

        // If there are fewer new rects than overlays, hide the extras
        if (newRects.length < overlays.length) {
          for (let i = newRects.length; i < overlays.length; i++) {
            overlays[i].element.style.display = 'none';
          }
        }

        // Update label position based on the first new rect
        if (label && newRects.length > 0) {
          const firstNewRect = newRects[0];
          const firstNewRectTop = firstNewRect.top + newIframeOffset.y;
          const firstNewRectLeft = firstNewRect.left + newIframeOffset.x;

          let newLabelTop = firstNewRectTop + 2;
          let newLabelLeft = firstNewRectLeft + firstNewRect.width - labelWidth - 2;

          if (firstNewRect.width < labelWidth + 4 || firstNewRect.height < labelHeight + 4) {
            newLabelTop = firstNewRectTop - labelHeight - 2;
            newLabelLeft = firstNewRectLeft + firstNewRect.width - labelWidth;
            if (newLabelLeft < newIframeOffset.x) newLabelLeft = firstNewRectLeft;
          }

          // Ensure label stays within viewport bounds
          newLabelTop = Math.max(0, Math.min(newLabelTop, window.innerHeight - labelHeight));
          newLabelLeft = Math.max(0, Math.min(newLabelLeft, window.innerWidth - labelWidth));

          label.style.top = `${newLabelTop}px`;
          label.style.left = `${newLabelLeft}px`;
          label.style.display = 'block';
        } else if (label) {
          // Hide label if element has no rects anymore
          label.style.display = 'none';
        }
      };

      window.addEventListener('scroll', updatePositions, true); // Use capture phase
      window.addEventListener('resize', updatePositions);

      // TODO: Add cleanup logic to remove listeners and elements when done.

      return index + 1;
    } finally {
      // popTiming('highlighting'); // Assuming this was a typo and should be removed or corrected
    }
  }

  function getElementPosition(currentElement) {
    if (!currentElement.parentElement) {
      return 0; // No parent means no siblings
    }
  
    const tagName = currentElement.nodeName.toLowerCase();
  
    const siblings = Array.from(currentElement.parentElement.children)
      .filter((sib) => sib.nodeName.toLowerCase() === tagName);
  
    if (siblings.length === 1) {
      return 0; // Only element of its type
    }
  
    const index = siblings.indexOf(currentElement) + 1; // 1-based index
    return index;
  }

  /**
   * Returns an XPath tree string for an element.
   */
  function getXPathTree(element, stopAtBoundary = true) {
    const segments = [];
    let currentElement = element;

    while (currentElement && currentElement.nodeType === Node.ELEMENT_NODE) {
      // Stop if we hit a shadow root or iframe
      if (
        stopAtBoundary &&
        (currentElement.parentNode instanceof ShadowRoot ||
          currentElement.parentNode instanceof HTMLIFrameElement)
      ) {
        break;
      }

      const position = getElementPosition(currentElement);
      const tagName = currentElement.nodeName.toLowerCase();
      const xpathIndex = position > 0 ? `[${position}]` : "";
      segments.unshift(`${tagName}${xpathIndex}`);

      currentElement = currentElement.parentNode;
    }

    return segments.join("/");
  }

  /**
   * Checks if a text node is visible.
   */
  function isTextNodeVisible(textNode) {
    try {
      const range = document.createRange();
      range.selectNodeContents(textNode);
      const rects = range.getClientRects(); // Use getClientRects for Range

      if (!rects || rects.length === 0) {
        return false;
      }

      let isAnyRectVisible = false;
      let isAnyRectInViewport = false;

      for (const rect of rects) {
        // Check size
        if (rect.width > 0 && rect.height > 0) {
          isAnyRectVisible = true;

          // Viewport check for this rect
          if (!(
            rect.bottom < -viewportExpansion ||
            rect.top > window.innerHeight + viewportExpansion ||
            rect.right < -viewportExpansion ||
            rect.left > window.innerWidth + viewportExpansion
          ) || viewportExpansion === -1) {
            isAnyRectInViewport = true;
            break; // Found a visible rect in viewport, no need to check others
          }
        }
      }

      if (!isAnyRectVisible || !isAnyRectInViewport) {
        return false;
      }

      // Check parent visibility
      const parentElement = textNode.parentElement;
      if (!parentElement) return false;

      try {
        return isInViewport && parentElement.checkVisibility({
          checkOpacity: true,
          checkVisibilityCSS: true,
        });
      } catch (e) {
        // Fallback if checkVisibility is not supported
        const style = window.getComputedStyle(parentElement);
        return isInViewport &&
          style.display !== 'none' &&
          style.visibility !== 'hidden' &&
          style.opacity !== '0';
      }
    } catch (e) {
      console.warn('Error checking text node visibility:', e);
      return false;
    }
  }

  // Helper function to check if element is accepted
  function isElementAccepted(element) {
    if (!element || !element.tagName) return false;

    // Always accept body and common container elements
    const alwaysAccept = new Set([
      "body", "div", "main", "article", "section", "nav", "header", "footer"
    ]);
    const tagName = element.tagName.toLowerCase();

    if (alwaysAccept.has(tagName)) return true;

    const leafElementDenyList = new Set([
      "svg",
      "script",
      "style",
      "link",
      "meta",
      "noscript",
      "template",
    ]);

    return !leafElementDenyList.has(tagName);
  }

  /**
   * Checks if an element is visible.
   */
  function isElementVisible(element) {
    const style = getCachedComputedStyle(element);
    return (
      element.offsetWidth > 0 &&
      element.offsetHeight > 0 &&
      style.visibility !== "hidden" &&
      style.display !== "none"
    );
  }

  /**
   * Checks if an element is interactive.
   * 
   * lots of comments, and uncommented code - to show the logic of what we already tried
   * 
   * One of the things we tried at the beginning was also to use event listeners, and other fancy class, style stuff -> what actually worked best was just combining most things with computed cursor style :)
   */
  function isInteractiveElement(element) {
    if (!element || element.nodeType !== Node.ELEMENT_NODE) {
      return false;
    }

    // Define interactive cursors
    const interactiveCursors = new Set([
      'pointer',    // Link/clickable elements
      'move',       // Movable elements
      'text',       // Text selection
      'grab',       // Grabbable elements
      'grabbing',   // Currently grabbing
      'cell',       // Table cell selection
      'copy',       // Copy operation
      'alias',      // Alias creation
      'all-scroll', // Scrollable content
      'col-resize', // Column resize
      'context-menu', // Context menu available
      'crosshair',  // Precise selection
      'e-resize',   // East resize
      'ew-resize',  // East-west resize
      'help',       // Help available
      'n-resize',   // North resize
      'ne-resize',  // Northeast resize
      'nesw-resize', // Northeast-southwest resize
      'ns-resize',  // North-south resize
      'nw-resize',  // Northwest resize
      'nwse-resize', // Northwest-southeast resize
      'row-resize', // Row resize
      's-resize',   // South resize
      'se-resize',  // Southeast resize
      'sw-resize',  // Southwest resize
      'vertical-text', // Vertical text selection
      'w-resize',   // West resize
      'zoom-in',    // Zoom in
      'zoom-out'    // Zoom out
    ]);

    // Define non-interactive cursors
    const nonInteractiveCursors = new Set([
      'not-allowed', // Action not allowed
      'no-drop',     // Drop not allowed
      'wait',        // Processing
      'progress',    // In progress
      'initial',     // Initial value
      'inherit'      // Inherited value
      //? Let's just include all potentially clickable elements that are not specifically blocked
      // 'none',        // No cursor
      // 'default',     // Default cursor 
      // 'auto',        // Browser default
    ]);

    function doesElementHaveInteractivePointer(element) {
      if (element.tagName.toLowerCase() === "html") return false;
      const style = getCachedComputedStyle(element);

      if (interactiveCursors.has(style.cursor)) return true;

      return false;
    }

    let isInteractiveCursor = doesElementHaveInteractivePointer(element);

    // Genius fix for almost all interactive elements
    if (isInteractiveCursor) {
      return true;
    }

    const interactiveElements = new Set([
      "a",          // Links
      "button",     // Buttons
      "input",      // All input types (text, checkbox, radio, etc.)
      "select",     // Dropdown menus
      "textarea",   // Text areas
      "details",    // Expandable details
      "summary",    // Summary element (clickable part of details)
      "label",      // Form labels (often clickable)
      "option",     // Select options
      "optgroup",   // Option groups
      "fieldset",   // Form fieldsets (can be interactive with legend)
      "legend",     // Fieldset legends
    ]);

    // Define explicit disable attributes and properties
    const explicitDisableTags = new Set([
      'disabled',           // Standard disabled attribute
      // 'aria-disabled',      // ARIA disabled state
      'readonly',          // Read-only state
      // 'aria-readonly',     // ARIA read-only state
      // 'aria-hidden',       // Hidden from accessibility
      // 'hidden',            // Hidden attribute
      // 'inert',             // Inert attribute
      // 'aria-inert',        // ARIA inert state
      // 'tabindex="-1"',     // Removed from tab order
      // 'aria-hidden="true"' // Hidden from screen readers
    ]);

    // handle inputs, select, checkbox, radio, textarea, button and make sure they are not cursor style disabled/not-allowed
    if (interactiveElements.has(element.tagName.toLowerCase())) {
      const style = getCachedComputedStyle(element);

      // Check for non-interactive cursor
      if (nonInteractiveCursors.has(style.cursor)) {
        return false;
      }

      // Check for explicit disable attributes
      for (const disableTag of explicitDisableTags) {
        if (element.hasAttribute(disableTag) ||
          element.getAttribute(disableTag) === 'true' ||
          element.getAttribute(disableTag) === '') {
          return false;
        }
      }

      // Check for disabled property on form elements
      if (element.disabled) {
        return false;
      }

      // Check for readonly property on form elements
      if (element.readOnly) {
        return false;
      }

      // Check for inert property
      if (element.inert) {
        return false;
      }

      return true;
    }

    const tagName = element.tagName.toLowerCase();
    const role = element.getAttribute("role");
    const ariaRole = element.getAttribute("aria-role");

    // Added enhancement to capture dropdown interactive elements
    if (element.classList && (
      element.classList.contains("button") ||
      element.classList.contains('dropdown-toggle') ||
      element.getAttribute('data-index') ||
      element.getAttribute('data-toggle') === 'dropdown' ||
      element.getAttribute('aria-haspopup') === 'true'
    )) {
      return true;
    }

    const interactiveRoles = new Set([
      'button',           // Directly clickable element
      // 'link',            // Clickable link
      // 'menuitem',        // Clickable menu item
      'menuitemradio',   // Radio-style menu item (selectable)
      'menuitemcheckbox', // Checkbox-style menu item (toggleable)
      'radio',           // Radio button (selectable)
      'checkbox',        // Checkbox (toggleable)
      'tab',             // Tab (clickable to switch content)
      'switch',          // Toggle switch (clickable to change state)
      'slider',          // Slider control (draggable)
      'spinbutton',      // Number input with up/down controls
      'combobox',        // Dropdown with text input
      'searchbox',       // Search input field
      'textbox',         // Text input field
      // 'listbox',         // Selectable list
      'option',          // Selectable option in a list
      'scrollbar'        // Scrollable control
    ]);

    // Basic role/attribute checks
    const hasInteractiveRole =
      interactiveElements.has(tagName) ||
      interactiveRoles.has(role) ||
      interactiveRoles.has(ariaRole);

    if (hasInteractiveRole) return true;

    // check whether element has event listeners
    try {
      if (typeof getEventListeners === 'function') {
        const listeners = getEventListeners(element);
        const mouseEvents = ['click', 'mousedown', 'mouseup', 'dblclick'];
        for (const eventType of mouseEvents) {
          if (listeners[eventType] && listeners[eventType].length > 0) {
            return true; // Found a mouse interaction listener
          }
        }
      } else {
        // Fallback: Check common event attributes if getEventListeners is not available
        const commonMouseAttrs = ['onclick', 'onmousedown', 'onmouseup', 'ondblclick'];
        if (commonMouseAttrs.some(attr => element.hasAttribute(attr))) {
          return true;
        }
      }
    } catch (e) {
      // console.warn(`Could not check event listeners for ${element.tagName}:`, e);
      // If checking listeners fails, rely on other checks
    }

    return false
  }


  /**
   * Checks if an element is the topmost element at its position.
   */
  function isTopElement(element) {
    const rects = element.getClientRects(); // Use getClientRects

    if (!rects || rects.length === 0) {
      return false; // No geometry, cannot be top
    }

    let isAnyRectInViewport = false;
    for (const rect of rects) {
      // Use the same logic as isInExpandedViewport check
      if (rect.width > 0 && rect.height > 0 && !( // Only check non-empty rects
        rect.bottom < -viewportExpansion ||
        rect.top > window.innerHeight + viewportExpansion ||
        rect.right < -viewportExpansion ||
        rect.left > window.innerWidth + viewportExpansion
      ) || viewportExpansion === -1) {
        isAnyRectInViewport = true;
        break;
      }
    }

    if (!isAnyRectInViewport) {
      return false; // All rects are outside the viewport area
    }


    // Find the correct document context and root element
    let doc = element.ownerDocument;

    // If we're in an iframe, elements are considered top by default
    if (doc !== window.document) {
      return true;
    }

    // For shadow DOM, we need to check within its own root context
    const shadowRoot = element.getRootNode();
    if (shadowRoot instanceof ShadowRoot) {
      const centerX = rects[Math.floor(rects.length / 2)].left + rects[Math.floor(rects.length / 2)].width / 2;
      const centerY = rects[Math.floor(rects.length / 2)].top + rects[Math.floor(rects.length / 2)].height / 2;

      try {
        const topEl = measureDomOperation(
          () => shadowRoot.elementFromPoint(centerX, centerY),
          'elementFromPoint'
        );
        if (!topEl) return false;

        let current = topEl;
        while (current && current !== shadowRoot) {
          if (current === element) return true;
          current = current.parentElement;
        }
        return false;
      } catch (e) {
        return true;
      }
    }

    // For elements in viewport, check if they're topmost
    const centerX = rects[Math.floor(rects.length / 2)].left + rects[Math.floor(rects.length / 2)].width / 2;
    const centerY = rects[Math.floor(rects.length / 2)].top + rects[Math.floor(rects.length / 2)].height / 2;

    try {
      const topEl = document.elementFromPoint(centerX, centerY);
      if (!topEl) return false;

      let current = topEl;
      while (current && current !== document.documentElement) {
        if (current === element) return true;
        current = current.parentElement;
      }
      return false;
    } catch (e) {
      return true;
    }
  }

  /**
   * Checks if an element is within the expanded viewport.
   */
  function isInExpandedViewport(element, viewportExpansion) {
    return true

    if (viewportExpansion === -1) {
      return true;
    }

    const rects = element.getClientRects(); // Use getClientRects

    if (!rects || rects.length === 0) {
      // Fallback to getBoundingClientRect if getClientRects is empty,
      // useful for elements like <svg> that might not have client rects but have a bounding box.
      const boundingRect = getCachedBoundingRect(element);
      if (!boundingRect || boundingRect.width === 0 || boundingRect.height === 0) {
        return false;
      }
      return !(
        boundingRect.bottom < -viewportExpansion ||
        boundingRect.top > window.innerHeight + viewportExpansion ||
        boundingRect.right < -viewportExpansion ||
        boundingRect.left > window.innerWidth + viewportExpansion
      );
    }


    // Check if *any* client rect is within the viewport
    for (const rect of rects) {
      if (rect.width === 0 || rect.height === 0) continue; // Skip empty rects

      if (!(
        rect.bottom < -viewportExpansion ||
        rect.top > window.innerHeight + viewportExpansion ||
        rect.right < -viewportExpansion ||
        rect.left > window.innerWidth + viewportExpansion
      )) {
        return true; // Found at least one rect in the viewport
      }
    }

    return false; // No rects were found in the viewport
  }

  // Add this new helper function
  function getEffectiveScroll(element) {
    let currentEl = element;
    let scrollX = 0;
    let scrollY = 0;

    return measureDomOperation(() => {
      while (currentEl && currentEl !== document.documentElement) {
        if (currentEl.scrollLeft || currentEl.scrollTop) {
          scrollX += currentEl.scrollLeft;
          scrollY += currentEl.scrollTop;
        }
        currentEl = currentEl.parentElement;
      }

      scrollX += window.scrollX;
      scrollY += window.scrollY;

      return { scrollX, scrollY };
    }, 'scrollOperations');
  }

  // Add these helper functions at the top level
  function isInteractiveCandidate(element) {
    if (!element || element.nodeType !== Node.ELEMENT_NODE) return false;

    const tagName = element.tagName.toLowerCase();

    // Fast-path for common interactive elements
    const interactiveElements = new Set([
      "a", "button", "input", "select", "textarea", "details", "summary"
    ]);

    if (interactiveElements.has(tagName)) return true;

    // Quick attribute checks without getting full lists
    const hasQuickInteractiveAttr = element.hasAttribute("onclick") ||
      element.hasAttribute("role") ||
      element.hasAttribute("tabindex") ||
      element.hasAttribute("aria-") ||
      element.hasAttribute("data-action") ||
      element.getAttribute("contenteditable") == "true";

    return hasQuickInteractiveAttr;
  }

  // --- Define constants for distinct interaction check ---
  const DISTINCT_INTERACTIVE_TAGS = new Set([
    'a', 'button', 'input', 'select', 'textarea', 'summary', 'details', 'label', 'option'
  ]);
  const INTERACTIVE_ROLES = new Set([
    'button', 'link', 'menuitem', 'menuitemradio', 'menuitemcheckbox',
    'radio', 'checkbox', 'tab', 'switch', 'slider', 'spinbutton',
    'combobox', 'searchbox', 'textbox', 'listbox', 'option', 'scrollbar'
  ]);

  /**
   * Checks if an element likely represents a distinct interaction
   * separate from its parent (if the parent is also interactive).
   */
  function isElementDistinctInteraction(element) {
    if (!element || element.nodeType !== Node.ELEMENT_NODE) {
      return false;
    }


    const tagName = element.tagName.toLowerCase();
    const role = element.getAttribute('role');

    // Check if it's an iframe - always distinct boundary
    if (tagName === 'iframe') {
      return true;
    }

    // Check tag name
    if (DISTINCT_INTERACTIVE_TAGS.has(tagName)) {
      return true;
    }
    // Check interactive roles
    if (role && INTERACTIVE_ROLES.has(role)) {
      return true;
    }
    // Check contenteditable
    if (element.isContentEditable || element.getAttribute('contenteditable') === 'true') {
      return true;
    }
    // Check for common testing/automation attributes
    if (element.hasAttribute('data-testid') || element.hasAttribute('data-cy') || element.hasAttribute('data-test')) {
      return true;
    }
    // Check for explicit onclick handler (attribute or property)
    if (element.hasAttribute('onclick') || typeof element.onclick === 'function') {
      return true;
    }
    // Check for other common interaction event listeners
    try {
      if (typeof getEventListeners === 'function') {
        const listeners = getEventListeners(element);
        const interactionEvents = ['mousedown', 'mouseup', 'keydown', 'keyup', 'submit', 'change', 'input', 'focus', 'blur'];
        for (const eventType of interactionEvents) {
          if (listeners[eventType] && listeners[eventType].length > 0) {
            return true; // Found a common interaction listener
          }
        }
      } else {
        // Fallback: Check common event attributes if getEventListeners is not available
        const commonEventAttrs = ['onmousedown', 'onmouseup', 'onkeydown', 'onkeyup', 'onsubmit', 'onchange', 'oninput', 'onfocus', 'onblur'];
        if (commonEventAttrs.some(attr => element.hasAttribute(attr))) {
          return true;
        }
      }
    } catch (e) {
      // console.warn(`Could not check event listeners for ${element.tagName}:`, e);
      // If checking listeners fails, rely on other checks
    }


    // Default to false: if it's interactive but doesn't match above,
    // assume it triggers the same action as the parent.
    return false;
  }
  // --- End distinct interaction check ---

  /**
   * Handles the logic for deciding whether to highlight an element and performing the highlight.
   */
  function handleHighlighting(nodeData, node, parentIframe, isParentHighlighted) {
    if (!nodeData.isInteractive) return false; // Not interactive, definitely don't highlight

    let shouldHighlight = false;
    if (!isParentHighlighted) {
      // Parent wasn't highlighted, this interactive node can be highlighted.
      shouldHighlight = true;
    } else {
      // Parent *was* highlighted. Only highlight this node if it represents a distinct interaction.
      if (isElementDistinctInteraction(node)) {
        shouldHighlight = true;
      } else {
        // console.log(`Skipping highlight for ${nodeData.tagName} (parent highlighted)`);
        shouldHighlight = false;
      }
    }

    if (shouldHighlight) {
      // Check viewport status before assigning index and highlighting
      nodeData.isInViewport = isInExpandedViewport(node, viewportExpansion);
      if (nodeData.isInViewport) {
        nodeData.highlightIndex = highlightIndex++;

        if (doHighlightElements) {
          if (focusHighlightIndex >= 0) {
            if (focusHighlightIndex === nodeData.highlightIndex) {
              highlightElement(node, nodeData.highlightIndex, parentIframe);
            }
          } else {
            highlightElement(node, nodeData.highlightIndex, parentIframe);
          }
          return true; // Successfully highlighted
        }
      } else {
        // console.log(`Skipping highlight for ${nodeData.tagName} (outside viewport)`);
      }
    }

    return false; // Did not highlight
  }

  /**
   * Creates a node data object for a given node and its descendants.
   */
  function buildDomTree(node, parentIframe = null, isParentHighlighted = false) {
    if (debugMode) PERF_METRICS.nodeMetrics.totalNodes++;

    if (!node || node.id === HIGHLIGHT_CONTAINER_ID) {
      if (debugMode) PERF_METRICS.nodeMetrics.skippedNodes++;
      return null;
    }

    // Special handling for root node (body)
    if (node === document.body) {
      const nodeData = {
        tagName: 'body',
        attributes: {},
        xpath: '/body',
        children: [],
      };

      // Process children of body
      for (const child of node.childNodes) {
        const domElement = buildDomTree(child, parentIframe, false); // Body's children have no highlighted parent initially
        if (domElement) nodeData.children.push(domElement);
      }

      const id = `${ID.current++}`;
      DOM_HASH_MAP[id] = nodeData;
      if (debugMode) PERF_METRICS.nodeMetrics.processedNodes++;
      return id;
    }

    // Early bailout for non-element nodes except text
    if (node.nodeType !== Node.ELEMENT_NODE && node.nodeType !== Node.TEXT_NODE) {
      if (debugMode) PERF_METRICS.nodeMetrics.skippedNodes++;
      return null;
    }

    // Process text nodes
    if (node.nodeType === Node.TEXT_NODE) {
      const textContent = node.textContent.trim();
      if (!textContent) {
        if (debugMode) PERF_METRICS.nodeMetrics.skippedNodes++;
        return null;
      }

      // Only check visibility for text nodes that might be visible
      const parentElement = node.parentElement;
      if (!parentElement || parentElement.tagName.toLowerCase() === 'script') {
        if (debugMode) PERF_METRICS.nodeMetrics.skippedNodes++;
        return null;
      }

      const id = `${ID.current++}`;
      DOM_HASH_MAP[id] = {
        type: "TEXT_NODE",
        text: textContent,
        isVisible: isTextNodeVisible(node),
      };
      if (debugMode) PERF_METRICS.nodeMetrics.processedNodes++;
      return id;
    }

    // Quick checks for element nodes
    if (node.nodeType === Node.ELEMENT_NODE && !isElementAccepted(node)) {
      if (debugMode) PERF_METRICS.nodeMetrics.skippedNodes++;
      return null;
    }

    // Early viewport check - only filter out elements clearly outside viewport
    if (viewportExpansion !== -1) {
      const rect = getCachedBoundingRect(node); // Keep for initial quick check
      const style = getCachedComputedStyle(node);

      // Skip viewport check for fixed/sticky elements as they may appear anywhere
      const isFixedOrSticky = style && (style.position === 'fixed' || style.position === 'sticky');

      // Check if element has actual dimensions using offsetWidth/Height (quick check)
      const hasSize = node.offsetWidth > 0 || node.offsetHeight > 0;

      // Use getBoundingClientRect for the quick OUTSIDE check.
      // isInExpandedViewport will do the more accurate check later if needed.
      if (!rect || (!isFixedOrSticky && !hasSize && (
        rect.bottom < -viewportExpansion ||
        rect.top > window.innerHeight + viewportExpansion ||
        rect.right < -viewportExpansion ||
        rect.left > window.innerWidth + viewportExpansion
      ))) {
        // console.log("Skipping node outside viewport (quick check):", node.tagName, rect);
        if (debugMode) PERF_METRICS.nodeMetrics.skippedNodes++;
        return null;
      }
    }

    // Process element node
    const nodeData = {
      tagName: node.tagName.toLowerCase(),
      attributes: {},
      xpath: getXPathTree(node, true),
      children: [],
    };

    // Get attributes for interactive elements or potential text containers
    if (isInteractiveCandidate(node) || node.tagName.toLowerCase() === 'iframe' || node.tagName.toLowerCase() === 'body') {
      const attributeNames = node.getAttributeNames?.() || [];
      for (const name of attributeNames) {
        nodeData.attributes[name] = node.getAttribute(name);
      }
    }

    let nodeWasHighlighted = false;
    // Perform visibility, interactivity, and highlighting checks
    if (node.nodeType === Node.ELEMENT_NODE) {
      nodeData.isVisible = isElementVisible(node); // isElementVisible uses offsetWidth/Height, which is fine
      if (nodeData.isVisible) {
        nodeData.isTopElement = isTopElement(node);
        if (nodeData.isTopElement) {
          nodeData.isInteractive = isInteractiveElement(node);
          // Call the dedicated highlighting function
          nodeWasHighlighted = handleHighlighting(nodeData, node, parentIframe, isParentHighlighted);
        }
      }
    }

    // Process children, with special handling for iframes and rich text editors
    if (node.tagName) {
      const tagName = node.tagName.toLowerCase();

      // Handle iframes
      if (tagName === "iframe") {
        try {
          const iframeDoc = node.contentDocument || node.contentWindow?.document;
          if (iframeDoc) {
            for (const child of iframeDoc.childNodes) {
              const domElement = buildDomTree(child, node, false);
              if (domElement) nodeData.children.push(domElement);
            }
          }
        } catch (e) {
          console.warn("Unable to access iframe:", e);
        }
      }
      // Handle rich text editors and contenteditable elements
      else if (
        node.isContentEditable ||
        node.getAttribute("contenteditable") === "true" ||
        node.id === "tinymce" ||
        node.classList.contains("mce-content-body") ||
        (tagName === "body" && node.getAttribute("data-id")?.startsWith("mce_"))
      ) {
        // Process all child nodes to capture formatted text
        for (const child of node.childNodes) {
          const domElement = buildDomTree(child, parentIframe, nodeWasHighlighted);
          if (domElement) nodeData.children.push(domElement);
        }
      }
      else {
        // Handle shadow DOM
        if (node.shadowRoot) {
          nodeData.shadowRoot = true;
          for (const child of node.shadowRoot.childNodes) {
            const domElement = buildDomTree(child, parentIframe, nodeWasHighlighted);
            if (domElement) nodeData.children.push(domElement);
          }
        }
        // Handle regular elements
        for (const child of node.childNodes) {
          // Pass the highlighted status of the *current* node to its children
          const passHighlightStatusToChild = nodeWasHighlighted || isParentHighlighted;
          const domElement = buildDomTree(child, parentIframe, passHighlightStatusToChild);
          if (domElement) nodeData.children.push(domElement);
        }
      }
    }

    // Skip empty anchor tags
    if (nodeData.tagName === 'a' && nodeData.children.length === 0 && !nodeData.attributes.href) {
      if (debugMode) PERF_METRICS.nodeMetrics.skippedNodes++;
      return null;
    }

    const id = `${ID.current++}`;
    DOM_HASH_MAP[id] = nodeData;
    if (debugMode) PERF_METRICS.nodeMetrics.processedNodes++;
    return id;
  }

  // After all functions are defined, wrap them with performance measurement
  // Remove buildDomTree from here as we measure it separately
  highlightElement = measureTime(highlightElement);
  isInteractiveElement = measureTime(isInteractiveElement);
  isElementVisible = measureTime(isElementVisible);
  isTopElement = measureTime(isTopElement);
  isInExpandedViewport = measureTime(isInExpandedViewport);
  isTextNodeVisible = measureTime(isTextNodeVisible);
  getEffectiveScroll = measureTime(getEffectiveScroll);

  const rootId = buildDomTree(document.body);

  // Clear the cache before starting
  DOM_CACHE.clearCache();

  // Only process metrics in debug mode
  if (debugMode && PERF_METRICS) {
    // Convert timings to seconds and add useful derived metrics
    Object.keys(PERF_METRICS.timings).forEach(key => {
      PERF_METRICS.timings[key] = PERF_METRICS.timings[key] / 1000;
    });

    Object.keys(PERF_METRICS.buildDomTreeBreakdown).forEach(key => {
      if (typeof PERF_METRICS.buildDomTreeBreakdown[key] === 'number') {
        PERF_METRICS.buildDomTreeBreakdown[key] = PERF_METRICS.buildDomTreeBreakdown[key] / 1000;
      }
    });

    // Add some useful derived metrics
    if (PERF_METRICS.buildDomTreeBreakdown.buildDomTreeCalls > 0) {
      PERF_METRICS.buildDomTreeBreakdown.averageTimePerNode =
        PERF_METRICS.buildDomTreeBreakdown.totalTime / PERF_METRICS.buildDomTreeBreakdown.buildDomTreeCalls;
    }

    PERF_METRICS.buildDomTreeBreakdown.timeInChildCalls =
      PERF_METRICS.buildDomTreeBreakdown.totalTime - PERF_METRICS.buildDomTreeBreakdown.totalSelfTime;

    // Add average time per operation to the metrics
    Object.keys(PERF_METRICS.buildDomTreeBreakdown.domOperations).forEach(op => {
      const time = PERF_METRICS.buildDomTreeBreakdown.domOperations[op];
      const count = PERF_METRICS.buildDomTreeBreakdown.domOperationCounts[op];
      if (count > 0) {
        PERF_METRICS.buildDomTreeBreakdown.domOperations[`${op}Average`] = time / count;
      }
    });

    // Calculate cache hit rates
    const boundingRectTotal = PERF_METRICS.cacheMetrics.boundingRectCacheHits + PERF_METRICS.cacheMetrics.boundingRectCacheMisses;
    const computedStyleTotal = PERF_METRICS.cacheMetrics.computedStyleCacheHits + PERF_METRICS.cacheMetrics.computedStyleCacheMisses;

    if (boundingRectTotal > 0) {
      PERF_METRICS.cacheMetrics.boundingRectHitRate = PERF_METRICS.cacheMetrics.boundingRectCacheHits / boundingRectTotal;
    }

    if (computedStyleTotal > 0) {
      PERF_METRICS.cacheMetrics.computedStyleHitRate = PERF_METRICS.cacheMetrics.computedStyleCacheHits / computedStyleTotal;
    }

    if ((boundingRectTotal + computedStyleTotal) > 0) {
      PERF_METRICS.cacheMetrics.overallHitRate =
        (PERF_METRICS.cacheMetrics.boundingRectCacheHits + PERF_METRICS.cacheMetrics.computedStyleCacheHits) /
        (boundingRectTotal + computedStyleTotal);
    }
  }

  return debugMode ?
    { rootId, map: DOM_HASH_MAP, perfMetrics: PERF_METRICS } :
    { rootId, map: DOM_HASH_MAP };
};
````

## File: browser_use/dom/clickable_element_processor/service.py
````python
import hashlib

from browser_use.dom.views import DOMElementNode


class ClickableElementProcessor:
	@staticmethod
	def get_clickable_elements_hashes(dom_element: DOMElementNode) -> set[str]:
		"""Get all clickable elements in the DOM tree"""
		clickable_elements = ClickableElementProcessor.get_clickable_elements(dom_element)
		return {ClickableElementProcessor.hash_dom_element(element) for element in clickable_elements}

	@staticmethod
	def get_clickable_elements(dom_element: DOMElementNode) -> list[DOMElementNode]:
		"""Get all clickable elements in the DOM tree"""
		clickable_elements = list()
		for child in dom_element.children:
			if isinstance(child, DOMElementNode):
				if child.highlight_index:
					clickable_elements.append(child)

				clickable_elements.extend(ClickableElementProcessor.get_clickable_elements(child))

		return list(clickable_elements)

	@staticmethod
	def hash_dom_element(dom_element: DOMElementNode) -> str:
		parent_branch_path = ClickableElementProcessor._get_parent_branch_path(dom_element)
		branch_path_hash = ClickableElementProcessor._parent_branch_path_hash(parent_branch_path)
		attributes_hash = ClickableElementProcessor._attributes_hash(dom_element.attributes)
		xpath_hash = ClickableElementProcessor._xpath_hash(dom_element.xpath)
		# text_hash = DomTreeProcessor._text_hash(dom_element)

		return ClickableElementProcessor._hash_string(f'{branch_path_hash}-{attributes_hash}-{xpath_hash}')

	@staticmethod
	def _get_parent_branch_path(dom_element: DOMElementNode) -> list[str]:
		parents: list[DOMElementNode] = []
		current_element: DOMElementNode = dom_element
		while current_element.parent is not None:
			parents.append(current_element)
			current_element = current_element.parent

		parents.reverse()

		return [parent.tag_name for parent in parents]

	@staticmethod
	def _parent_branch_path_hash(parent_branch_path: list[str]) -> str:
		parent_branch_path_string = '/'.join(parent_branch_path)
		return hashlib.sha256(parent_branch_path_string.encode()).hexdigest()

	@staticmethod
	def _attributes_hash(attributes: dict[str, str]) -> str:
		attributes_string = ''.join(f'{key}={value}' for key, value in attributes.items())
		return ClickableElementProcessor._hash_string(attributes_string)

	@staticmethod
	def _xpath_hash(xpath: str) -> str:
		return ClickableElementProcessor._hash_string(xpath)

	@staticmethod
	def _text_hash(dom_element: DOMElementNode) -> str:
		""" """
		text_string = dom_element.get_all_text_till_next_clickable_element()
		return ClickableElementProcessor._hash_string(text_string)

	@staticmethod
	def _hash_string(string: str) -> str:
		return hashlib.sha256(string.encode()).hexdigest()
````

## File: browser_use/dom/history_tree_processor/service.py
````python
import hashlib
from typing import Optional

from browser_use.dom.history_tree_processor.view import DOMHistoryElement, HashedDomElement
from browser_use.dom.views import DOMElementNode


class HistoryTreeProcessor:
	""" "
	Operations on the DOM elements

	@dev be careful - text nodes can change even if elements stay the same
	"""

	@staticmethod
	def convert_dom_element_to_history_element(dom_element: DOMElementNode) -> DOMHistoryElement:
		from browser_use.browser.context import BrowserContext

		parent_branch_path = HistoryTreeProcessor._get_parent_branch_path(dom_element)
		css_selector = BrowserContext._enhanced_css_selector_for_element(dom_element)
		return DOMHistoryElement(
			dom_element.tag_name,
			dom_element.xpath,
			dom_element.highlight_index,
			parent_branch_path,
			dom_element.attributes,
			dom_element.shadow_root,
			css_selector=css_selector,
			page_coordinates=dom_element.page_coordinates,
			viewport_coordinates=dom_element.viewport_coordinates,
			viewport_info=dom_element.viewport_info,
		)

	@staticmethod
	def find_history_element_in_tree(dom_history_element: DOMHistoryElement, tree: DOMElementNode) -> Optional[DOMElementNode]:
		hashed_dom_history_element = HistoryTreeProcessor._hash_dom_history_element(dom_history_element)

		def process_node(node: DOMElementNode):
			if node.highlight_index is not None:
				hashed_node = HistoryTreeProcessor._hash_dom_element(node)
				if hashed_node == hashed_dom_history_element:
					return node
			for child in node.children:
				if isinstance(child, DOMElementNode):
					result = process_node(child)
					if result is not None:
						return result
			return None

		return process_node(tree)

	@staticmethod
	def compare_history_element_and_dom_element(dom_history_element: DOMHistoryElement, dom_element: DOMElementNode) -> bool:
		hashed_dom_history_element = HistoryTreeProcessor._hash_dom_history_element(dom_history_element)
		hashed_dom_element = HistoryTreeProcessor._hash_dom_element(dom_element)

		return hashed_dom_history_element == hashed_dom_element

	@staticmethod
	def _hash_dom_history_element(dom_history_element: DOMHistoryElement) -> HashedDomElement:
		branch_path_hash = HistoryTreeProcessor._parent_branch_path_hash(dom_history_element.entire_parent_branch_path)
		attributes_hash = HistoryTreeProcessor._attributes_hash(dom_history_element.attributes)
		xpath_hash = HistoryTreeProcessor._xpath_hash(dom_history_element.xpath)

		return HashedDomElement(branch_path_hash, attributes_hash, xpath_hash)

	@staticmethod
	def _hash_dom_element(dom_element: DOMElementNode) -> HashedDomElement:
		parent_branch_path = HistoryTreeProcessor._get_parent_branch_path(dom_element)
		branch_path_hash = HistoryTreeProcessor._parent_branch_path_hash(parent_branch_path)
		attributes_hash = HistoryTreeProcessor._attributes_hash(dom_element.attributes)
		xpath_hash = HistoryTreeProcessor._xpath_hash(dom_element.xpath)
		# text_hash = DomTreeProcessor._text_hash(dom_element)

		return HashedDomElement(branch_path_hash, attributes_hash, xpath_hash)

	@staticmethod
	def _get_parent_branch_path(dom_element: DOMElementNode) -> list[str]:
		parents: list[DOMElementNode] = []
		current_element: DOMElementNode = dom_element
		while current_element.parent is not None:
			parents.append(current_element)
			current_element = current_element.parent

		parents.reverse()

		return [parent.tag_name for parent in parents]

	@staticmethod
	def _parent_branch_path_hash(parent_branch_path: list[str]) -> str:
		parent_branch_path_string = '/'.join(parent_branch_path)
		return hashlib.sha256(parent_branch_path_string.encode()).hexdigest()

	@staticmethod
	def _attributes_hash(attributes: dict[str, str]) -> str:
		attributes_string = ''.join(f'{key}={value}' for key, value in attributes.items())
		return hashlib.sha256(attributes_string.encode()).hexdigest()

	@staticmethod
	def _xpath_hash(xpath: str) -> str:
		return hashlib.sha256(xpath.encode()).hexdigest()

	@staticmethod
	def _text_hash(dom_element: DOMElementNode) -> str:
		""" """
		text_string = dom_element.get_all_text_till_next_clickable_element()
		return hashlib.sha256(text_string.encode()).hexdigest()
````

## File: browser_use/dom/history_tree_processor/view.py
````python
from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel


@dataclass
class HashedDomElement:
	"""
	Hash of the dom element to be used as a unique identifier
	"""

	branch_path_hash: str
	attributes_hash: str
	xpath_hash: str
	# text_hash: str


class Coordinates(BaseModel):
	x: int
	y: int


class CoordinateSet(BaseModel):
	top_left: Coordinates
	top_right: Coordinates
	bottom_left: Coordinates
	bottom_right: Coordinates
	center: Coordinates
	width: int
	height: int


class ViewportInfo(BaseModel):
	scroll_x: int
	scroll_y: int
	width: int
	height: int


@dataclass
class DOMHistoryElement:
	tag_name: str
	xpath: str
	highlight_index: Optional[int]
	entire_parent_branch_path: list[str]
	attributes: dict[str, str]
	shadow_root: bool = False
	css_selector: Optional[str] = None
	page_coordinates: Optional[CoordinateSet] = None
	viewport_coordinates: Optional[CoordinateSet] = None
	viewport_info: Optional[ViewportInfo] = None

	def to_dict(self) -> dict:
		page_coordinates = self.page_coordinates.model_dump() if self.page_coordinates else None
		viewport_coordinates = self.viewport_coordinates.model_dump() if self.viewport_coordinates else None
		viewport_info = self.viewport_info.model_dump() if self.viewport_info else None

		return {
			'tag_name': self.tag_name,
			'xpath': self.xpath,
			'highlight_index': self.highlight_index,
			'entire_parent_branch_path': self.entire_parent_branch_path,
			'attributes': self.attributes,
			'shadow_root': self.shadow_root,
			'css_selector': self.css_selector,
			'page_coordinates': page_coordinates,
			'viewport_coordinates': viewport_coordinates,
			'viewport_info': viewport_info,
		}
````

## File: browser_use/dom/service.py
````python
import json
import logging
from dataclasses import dataclass
from importlib import resources
from typing import TYPE_CHECKING, Optional
from urllib.parse import urlparse

if TYPE_CHECKING:
	from patchright.async_api import Page

from browser_use.dom.views import (
	DOMBaseNode,
	DOMElementNode,
	DOMState,
	DOMTextNode,
	SelectorMap,
)
from browser_use.utils import time_execution_async

logger = logging.getLogger(__name__)


@dataclass
class ViewportInfo:
	width: int
	height: int


class DomService:
	def __init__(self, page: 'Page'):
		self.page = page
		self.xpath_cache = {}

		self.js_code = resources.files('browser_use.dom').joinpath('buildDomTree.js').read_text()

	# region - Clickable elements
	@time_execution_async('--get_clickable_elements')
	async def get_clickable_elements(
		self,
		highlight_elements: bool = True,
		focus_element: int = -1,
		viewport_expansion: int = 0,
	) -> DOMState:
		element_tree, selector_map = await self._build_dom_tree(highlight_elements, focus_element, viewport_expansion)
		return DOMState(element_tree=element_tree, selector_map=selector_map)

	@time_execution_async('--get_cross_origin_iframes')
	async def get_cross_origin_iframes(self) -> list[str]:
		# invisible cross-origin iframes are used for ads and tracking, dont open those
		hidden_frame_urls = await self.page.locator('iframe').filter(visible=False).evaluate_all('e => e.map(e => e.src)')

		is_ad_url = lambda url: any(
			domain in urlparse(url).netloc for domain in ('doubleclick.net', 'adroll.com', 'googletagmanager.com')
		)

		return [
			frame.url
			for frame in self.page.frames
			if urlparse(frame.url).netloc  # exclude data:urls and about:blank
			and urlparse(frame.url).netloc != urlparse(self.page.url).netloc  # exclude same-origin iframes
			and frame.url not in hidden_frame_urls  # exclude hidden frames
			and not is_ad_url(frame.url)  # exclude most common ad network tracker frame URLs
		]

	@time_execution_async('--build_dom_tree')
	async def _build_dom_tree(
		self,
		highlight_elements: bool,
		focus_element: int,
		viewport_expansion: int,
	) -> tuple[DOMElementNode, SelectorMap]:
		if await self.page.evaluate('1+1') != 2:
			raise ValueError('The page cannot evaluate javascript code properly')

		if self.page.url == 'about:blank':
			# short-circuit if the page is a new empty tab for speed, no need to inject buildDomTree.js
			return (
				DOMElementNode(
					tag_name='body',
					xpath='',
					attributes={},
					children=[],
					is_visible=False,
					parent=None,
				),
				{},
			)

		# NOTE: We execute JS code in the browser to extract important DOM information.
		#       The returned hash map contains information about the DOM tree and the
		#       relationship between the DOM elements.
		debug_mode = logger.getEffectiveLevel() == logging.DEBUG
		args = {
			'doHighlightElements': highlight_elements,
			'focusHighlightIndex': focus_element,
			'viewportExpansion': viewport_expansion,
			'debugMode': debug_mode,
		}

		try:
			eval_page: dict = await self.page.evaluate(self.js_code, args)
		except Exception as e:
			logger.error('Error evaluating JavaScript: %s', e)
			raise

		# Only log performance metrics in debug mode
		if debug_mode and 'perfMetrics' in eval_page:
			logger.debug(
				'DOM Tree Building Performance Metrics for: %s\n%s',
				self.page.url,
				json.dumps(eval_page['perfMetrics'], indent=2),
			)

		return await self._construct_dom_tree(eval_page)

	@time_execution_async('--construct_dom_tree')
	async def _construct_dom_tree(
		self,
		eval_page: dict,
	) -> tuple[DOMElementNode, SelectorMap]:
		js_node_map = eval_page['map']
		js_root_id = eval_page['rootId']

		selector_map = {}
		node_map = {}

		for id, node_data in js_node_map.items():
			node, children_ids = self._parse_node(node_data)
			if node is None:
				continue

			node_map[id] = node

			if isinstance(node, DOMElementNode) and node.highlight_index is not None:
				selector_map[node.highlight_index] = node

			# NOTE: We know that we are building the tree bottom up
			#       and all children are already processed.
			if isinstance(node, DOMElementNode):
				for child_id in children_ids:
					if child_id not in node_map:
						continue

					child_node = node_map[child_id]

					child_node.parent = node
					node.children.append(child_node)

		html_to_dict = node_map[str(js_root_id)]

		del node_map
		del js_node_map
		del js_root_id

		if html_to_dict is None or not isinstance(html_to_dict, DOMElementNode):
			raise ValueError('Failed to parse HTML to dictionary')

		return html_to_dict, selector_map

	def _parse_node(
		self,
		node_data: dict,
	) -> tuple[Optional[DOMBaseNode], list[int]]:
		if not node_data:
			return None, []

		# Process text nodes immediately
		if node_data.get('type') == 'TEXT_NODE':
			text_node = DOMTextNode(
				text=node_data['text'],
				is_visible=node_data['isVisible'],
				parent=None,
			)
			return text_node, []

		# Process coordinates if they exist for element nodes

		viewport_info = None

		if 'viewport' in node_data:
			viewport_info = ViewportInfo(
				width=node_data['viewport']['width'],
				height=node_data['viewport']['height'],
			)

		element_node = DOMElementNode(
			tag_name=node_data['tagName'],
			xpath=node_data['xpath'],
			attributes=node_data.get('attributes', {}),
			children=[],
			is_visible=node_data.get('isVisible', False),
			is_interactive=node_data.get('isInteractive', False),
			is_top_element=node_data.get('isTopElement', False),
			is_in_viewport=node_data.get('isInViewport', False),
			highlight_index=node_data.get('highlightIndex'),
			shadow_root=node_data.get('shadowRoot', False),
			parent=None,
			viewport_info=viewport_info,
		)

		children_ids = node_data.get('children', [])

		return element_node, children_ids
````

## File: browser_use/dom/tests/debug_page_structure.py
````python
import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext


async def analyze_page_structure(url: str):
	"""Analyze and print the structure of a webpage with enhanced debugging"""
	browser = Browser(
		config=BrowserConfig(
			headless=False,  # Set to True if you don't need to see the browser
		)
	)

	context = BrowserContext(browser=browser)

	try:
		async with context as ctx:
			# Navigate to the URL
			page = await ctx.get_current_page()
			await page.goto(url)
			await page.wait_for_load_state('networkidle')

			# Get viewport dimensions
			viewport_info = await page.evaluate("""() => {
				return {
					viewport: {
						width: window.innerWidth,
						height: window.innerHeight,
						scrollX: window.scrollX,
						scrollY: window.scrollY
					}
				}
			}""")

			print('\nViewport Information:')
			print(f'Width: {viewport_info["viewport"]["width"]}')
			print(f'Height: {viewport_info["viewport"]["height"]}')
			print(f'ScrollX: {viewport_info["viewport"]["scrollX"]}')
			print(f'ScrollY: {viewport_info["viewport"]["scrollY"]}')

			# Enhanced debug information for cookie consent and fixed position elements
			debug_info = await page.evaluate("""() => {
				function getElementInfo(element) {
					const rect = element.getBoundingClientRect();
					const style = window.getComputedStyle(element);
					return {
						tag: element.tagName.toLowerCase(),
						id: element.id,
						className: element.className,
						position: style.position,
						rect: {
							top: rect.top,
							right: rect.right,
							bottom: rect.bottom,
							left: rect.left,
							width: rect.width,
							height: rect.height
						},
						isFixed: style.position === 'fixed',
						isSticky: style.position === 'sticky',
						zIndex: style.zIndex,
						visibility: style.visibility,
						display: style.display,
						opacity: style.opacity
					};
				}

				// Find cookie-related elements
				const cookieElements = Array.from(document.querySelectorAll('[id*="cookie"], [id*="consent"], [class*="cookie"], [class*="consent"]'));
				const fixedElements = Array.from(document.querySelectorAll('*')).filter(el => {
					const style = window.getComputedStyle(el);
					return style.position === 'fixed' || style.position === 'sticky';
				});

				return {
					cookieElements: cookieElements.map(getElementInfo),
					fixedElements: fixedElements.map(getElementInfo)
				};
			}""")

			print('\nCookie-related Elements:')
			for elem in debug_info['cookieElements']:
				print(f'\nElement: {elem["tag"]}#{elem["id"]} .{elem["className"]}')
				print(f'Position: {elem["position"]}')
				print(f'Rect: {elem["rect"]}')
				print(f'Z-Index: {elem["zIndex"]}')
				print(f'Visibility: {elem["visibility"]}')
				print(f'Display: {elem["display"]}')
				print(f'Opacity: {elem["opacity"]}')

			print('\nFixed/Sticky Position Elements:')
			for elem in debug_info['fixedElements']:
				print(f'\nElement: {elem["tag"]}#{elem["id"]} .{elem["className"]}')
				print(f'Position: {elem["position"]}')
				print(f'Rect: {elem["rect"]}')
				print(f'Z-Index: {elem["zIndex"]}')

			print(f'\nPage Structure for {url}:\n')
			structure = await ctx.get_page_structure()
			print(structure)

			input('Press Enter to close the browser...')
	finally:
		await browser.close()


if __name__ == '__main__':
	# You can modify this URL to analyze different pages

	urls = [
		'https://www.mlb.com/yankees/stats/',
		'https://immobilienscout24.de',
		'https://www.zeiss.com/career/en/job-search.html?page=1',
		'https://www.zeiss.com/career/en/job-search.html?page=1',
		'https://reddit.com',
	]
	for url in urls:
		asyncio.run(analyze_page_structure(url))
````

## File: browser_use/dom/tests/extraction_test.py
````python
import asyncio
import os

import anyio
from langchain_openai import ChatOpenAI

from browser_use.agent.prompts import AgentMessagePrompt
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from browser_use.dom.service import DomService


def count_string_tokens(string: str, model: str) -> tuple[int, float]:
	"""Count the number of tokens in a string using a specified model."""

	def get_price_per_token(model: str) -> float:
		"""Get the price per token for a specified model.

		@todo: move to utils, use a package or sth
		"""
		prices = {
			'gpt-4o': 2.5 / 1e6,
			'gpt-4o-mini': 0.15 / 1e6,
		}
		return prices[model]

	llm = ChatOpenAI(model=model)
	token_count = llm.get_num_tokens(string)
	price = token_count * get_price_per_token(model)
	return token_count, price


TIMEOUT = 60

DEFAULT_INCLUDE_ATTRIBUTES = [
	'id',
	'title',
	'type',
	'name',
	'role',
	'aria-label',
	'placeholder',
	'value',
	'alt',
	'aria-expanded',
	'data-date-format',
]


async def test_focus_vs_all_elements():
	config = BrowserContextConfig(
		# cookies_file='cookies3.json',
		disable_security=True,
		wait_for_network_idle_page_load_time=1,
	)

	browser = Browser(
		config=BrowserConfig(
			# browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
		)
	)
	context = BrowserContext(browser=browser, config=config)  # noqa: F821

	websites = [
		'https://kayak.com/flights',
		# 'https://en.wikipedia.org/wiki/Humanist_Party_of_Ontario',
		# 'https://www.google.com/travel/flights?tfs=CBwQARoJagcIARIDTEpVGglyBwgBEgNMSlVAAUgBcAGCAQsI____________AZgBAQ&tfu=KgIIAw&hl=en-US&gl=US',
		# # 'https://www.concur.com/?&cookie_preferences=cpra',
		# 'https://immobilienscout24.de',
		'https://docs.google.com/spreadsheets/d/1INaIcfpYXlMRWO__de61SHFCaqt1lfHlcvtXZPItlpI/edit',
		'https://www.zeiss.com/career/en/job-search.html?page=1',
		'https://www.mlb.com/yankees/stats/',
		'https://www.amazon.com/s?k=laptop&s=review-rank&crid=1RZCEJ289EUSI&qid=1740202453&sprefix=laptop%2Caps%2C166&ref=sr_st_review-rank&ds=v1%3A4EnYKXVQA7DIE41qCvRZoNB4qN92Jlztd3BPsTFXmxU',
		'https://reddit.com',
		'https://codepen.io/geheimschriftstift/pen/mPLvQz',
		'https://www.google.com/search?q=google+hi&oq=google+hi&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRhA0gEIMjI2NmowajSoAgCwAgE&sourceid=chrome&ie=UTF-8',
		'https://google.com',
		'https://amazon.com',
		'https://github.com',
	]

	async with context as context:
		page = await context.get_current_page()
		dom_service = DomService(page)

		for website in websites:
			# sleep 2
			await page.goto(website)
			asyncio.sleep(1)

			last_clicked_index = None  # Track the index for text input
			while True:
				try:
					print(f'\n{"=" * 50}\nTesting {website}\n{"=" * 50}')

					# Get/refresh the state (includes removing old highlights)
					print('\nGetting page state...')
					all_elements_state = await context.get_state(True)

					selector_map = all_elements_state.selector_map
					total_elements = len(selector_map.keys())
					print(f'Total number of elements: {total_elements}')

					# print(all_elements_state.element_tree.clickable_elements_to_string())
					prompt = AgentMessagePrompt(
						state=all_elements_state,
						result=None,
						include_attributes=DEFAULT_INCLUDE_ATTRIBUTES,
						step_info=None,
					)
					# print(prompt.get_user_message(use_vision=False).content)
					# Write the user message to a file for analysis
					user_message = prompt.get_user_message(use_vision=False).content
					os.makedirs('./tmp', exist_ok=True)
					async with await anyio.open_file('./tmp/user_message.txt', 'w', encoding='utf-8') as f:
						await f.write(user_message)

					token_count, price = count_string_tokens(user_message, model='gpt-4o')
					print(f'Prompt token count: {token_count}, price: {round(price, 4)} USD')
					print('User message written to ./tmp/user_message.txt')

					# also save all_elements_state.element_tree.clickable_elements_to_string() to a file
					# with open('./tmp/clickable_elements.json', 'w', encoding='utf-8') as f:
					# 	f.write(json.dumps(all_elements_state.element_tree.__json__(), indent=2))
					# print('Clickable elements written to ./tmp/clickable_elements.json')

					answer = input("Enter element index to click, 'index,text' to input, or 'q' to quit: ")

					if answer.lower() == 'q':
						break

					try:
						if ',' in answer:
							# Input text format: index,text
							parts = answer.split(',', 1)
							if len(parts) == 2:
								try:
									target_index = int(parts[0].strip())
									text_to_input = parts[1]
									if target_index in selector_map:
										element_node = selector_map[target_index]
										print(
											f"Inputting text '{text_to_input}' into element {target_index}: {element_node.tag_name}"
										)
										await context._input_text_element_node(element_node, text_to_input)
										print('Input successful.')
									else:
										print(f'Invalid index: {target_index}')
								except ValueError:
									print(f'Invalid index format: {parts[0]}')
							else:
								print("Invalid input format. Use 'index,text'.")
						else:
							# Click element format: index
							try:
								clicked_index = int(answer)
								if clicked_index in selector_map:
									element_node = selector_map[clicked_index]
									print(f'Clicking element {clicked_index}: {element_node.tag_name}')
									await context._click_element_node(element_node)
									print('Click successful.')
								else:
									print(f'Invalid index: {clicked_index}')
							except ValueError:
								print(f"Invalid input: '{answer}'. Enter an index, 'index,text', or 'q'.")

					except Exception as action_e:
						print(f'Action failed: {action_e}')

				# No explicit highlight removal here, get_state handles it at the start of the loop

				except Exception as e:
					print(f'Error in loop: {e}')
					# Optionally add a small delay before retrying
					await asyncio.sleep(1)


if __name__ == '__main__':
	asyncio.run(test_focus_vs_all_elements())
	# asyncio.run(test_process_html_file()) # Commented out the other test
````

## File: browser_use/dom/tests/process_dom_test.py
````python
import asyncio
import json
import os
import time

import anyio

from browser_use.browser.browser import Browser, BrowserConfig


async def test_process_dom():
	browser = Browser(config=BrowserConfig(headless=False))

	async with await browser.new_context() as context:
		page = await context.get_current_page()
		await page.goto('https://kayak.com/flights')
		# await page.goto('https://google.com/flights')
		# await page.goto('https://immobilienscout24.de')
		# await page.goto('https://seleniumbase.io/w3schools/iframes')

		await asyncio.sleep(3)

		async with await anyio.open_file('browser_use/dom/buildDomTree.js', 'r') as f:
			js_code = await f.read()

		start = time.time()
		dom_tree = await page.evaluate(js_code)
		end = time.time()

		# print(dom_tree)
		print(f'Time: {end - start:.2f}s')

		os.makedirs('./tmp', exist_ok=True)
		async with await anyio.open_file('./tmp/dom.json', 'w') as f:
			await f.write(json.dumps(dom_tree, indent=1))

		# both of these work for immobilienscout24.de
		# await page.click('.sc-dcJsrY.ezjNCe')
		# await page.click(
		# 	'div > div:nth-of-type(2) > div > div:nth-of-type(2) > div > div:nth-of-type(2) > div > div > div > button:nth-of-type(2)'
		# )

		input('Press Enter to continue...')
````

## File: browser_use/dom/views.py
````python
from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING, Dict, List, Optional

from browser_use.dom.history_tree_processor.view import CoordinateSet, HashedDomElement, ViewportInfo
from browser_use.utils import time_execution_sync

# Avoid circular import issues
if TYPE_CHECKING:
	from .views import DOMElementNode


@dataclass(frozen=False)
class DOMBaseNode:
	is_visible: bool
	# Use None as default and set parent later to avoid circular reference issues
	parent: Optional['DOMElementNode']

	def __json__(self) -> dict:
		raise NotImplementedError('DOMBaseNode is an abstract class')


@dataclass(frozen=False)
class DOMTextNode(DOMBaseNode):
	text: str
	type: str = 'TEXT_NODE'

	def has_parent_with_highlight_index(self) -> bool:
		current = self.parent
		while current is not None:
			# stop if the element has a highlight index (will be handled separately)
			if current.highlight_index is not None:
				return True

			current = current.parent
		return False

	def is_parent_in_viewport(self) -> bool:
		if self.parent is None:
			return False
		return self.parent.is_in_viewport

	def is_parent_top_element(self) -> bool:
		if self.parent is None:
			return False
		return self.parent.is_top_element

	def __json__(self) -> dict:
		return {
			'text': self.text,
			'type': self.type,
		}


@dataclass(frozen=False)
class DOMElementNode(DOMBaseNode):
	"""
	xpath: the xpath of the element from the last root node (shadow root or iframe OR document if no shadow root or iframe).
	To properly reference the element we need to recursively switch the root node until we find the element (work you way up the tree with `.parent`)
	"""

	tag_name: str
	xpath: str
	attributes: Dict[str, str]
	children: List[DOMBaseNode]
	is_interactive: bool = False
	is_top_element: bool = False
	is_in_viewport: bool = False
	shadow_root: bool = False
	highlight_index: Optional[int] = None
	viewport_coordinates: Optional[CoordinateSet] = None
	page_coordinates: Optional[CoordinateSet] = None
	viewport_info: Optional[ViewportInfo] = None

	"""
	### State injected by the browser context.

	The idea is that the clickable elements are sometimes persistent from the previous page -> tells the model which objects are new/_how_ the state has changed
	"""
	is_new: Optional[bool] = None

	def __json__(self) -> dict:
		return {
			'tag_name': self.tag_name,
			'xpath': self.xpath,
			'attributes': self.attributes,
			'is_visible': self.is_visible,
			'is_interactive': self.is_interactive,
			'is_top_element': self.is_top_element,
			'is_in_viewport': self.is_in_viewport,
			'shadow_root': self.shadow_root,
			'highlight_index': self.highlight_index,
			'viewport_coordinates': self.viewport_coordinates,
			'page_coordinates': self.page_coordinates,
			'children': [child.__json__() for child in self.children],
		}

	def __repr__(self) -> str:
		tag_str = f'<{self.tag_name}'

		# Add attributes
		for key, value in self.attributes.items():
			tag_str += f' {key}="{value}"'
		tag_str += '>'

		# Add extra info
		extras = []
		if self.is_interactive:
			extras.append('interactive')
		if self.is_top_element:
			extras.append('top')
		if self.shadow_root:
			extras.append('shadow-root')
		if self.highlight_index is not None:
			extras.append(f'highlight:{self.highlight_index}')
		if self.is_in_viewport:
			extras.append('in-viewport')

		if extras:
			tag_str += f' [{", ".join(extras)}]'

		return tag_str

	@cached_property
	def hash(self) -> HashedDomElement:
		from browser_use.dom.history_tree_processor.service import (
			HistoryTreeProcessor,
		)

		return HistoryTreeProcessor._hash_dom_element(self)

	def get_all_text_till_next_clickable_element(self, max_depth: int = -1) -> str:
		text_parts = []

		def collect_text(node: DOMBaseNode, current_depth: int) -> None:
			if max_depth != -1 and current_depth > max_depth:
				return

			# Skip this branch if we hit a highlighted element (except for the current node)
			if isinstance(node, DOMElementNode) and node != self and node.highlight_index is not None:
				return

			if isinstance(node, DOMTextNode):
				text_parts.append(node.text)
			elif isinstance(node, DOMElementNode):
				for child in node.children:
					collect_text(child, current_depth + 1)

		collect_text(self, 0)
		return '\n'.join(text_parts).strip()

	@time_execution_sync('--clickable_elements_to_string')
	def clickable_elements_to_string(self, include_attributes: list[str] | None = None) -> str:
		"""Convert the processed DOM content to HTML."""
		formatted_text = []

		def process_node(node: DOMBaseNode, depth: int) -> None:
			next_depth = int(depth)
			depth_str = depth * '\t'

			if isinstance(node, DOMElementNode):
				# Add element with highlight_index
				if node.highlight_index is not None:
					next_depth += 1

					text = node.get_all_text_till_next_clickable_element()
					attributes_html_str = ''
					if include_attributes:
						attributes_to_include = {
							key: str(value) for key, value in node.attributes.items() if key in include_attributes
						}

						# Easy LLM optimizations
						# if tag == role attribute, don't include it
						if node.tag_name == attributes_to_include.get('role'):
							del attributes_to_include['role']

						# if aria-label == text of the node, don't include it
						if (
							attributes_to_include.get('aria-label')
							and attributes_to_include.get('aria-label', '').strip() == text.strip()
						):
							del attributes_to_include['aria-label']

						# if placeholder == text of the node, don't include it
						if (
							attributes_to_include.get('placeholder')
							and attributes_to_include.get('placeholder', '').strip() == text.strip()
						):
							del attributes_to_include['placeholder']

						if attributes_to_include:
							# Format as key1='value1' key2='value2'
							attributes_html_str = ' '.join(f"{key}='{value}'" for key, value in attributes_to_include.items())

					# Build the line
					if node.is_new:
						highlight_indicator = f'*[{node.highlight_index}]*'
					else:
						highlight_indicator = f'[{node.highlight_index}]'

					line = f'{depth_str}{highlight_indicator}<{node.tag_name}'

					if attributes_html_str:
						line += f' {attributes_html_str}'

					if text:
						# Add space before >text only if there were NO attributes added before
						if not attributes_html_str:
							line += ' '
						line += f'>{text}'
					# Add space before /> only if neither attributes NOR text were added
					elif not attributes_html_str:
						line += ' '

					line += ' />'  # 1 token
					formatted_text.append(line)

				# Process children regardless
				for child in node.children:
					process_node(child, next_depth)

			elif isinstance(node, DOMTextNode):
				# Add text only if it doesn't have a highlighted parent
				if (
					not node.has_parent_with_highlight_index()
					and node.parent
					and node.parent.is_visible
					and node.parent.is_top_element
				):  # and node.is_parent_top_element()
					formatted_text.append(f'{depth_str}{node.text}')

		process_node(self, 0)
		return '\n'.join(formatted_text)

	def get_file_upload_element(self, check_siblings: bool = True) -> Optional['DOMElementNode']:
		# Check if current element is a file input
		if self.tag_name == 'input' and self.attributes.get('type') == 'file':
			return self

		# Check children
		for child in self.children:
			if isinstance(child, DOMElementNode):
				result = child.get_file_upload_element(check_siblings=False)
				if result:
					return result

		# Check siblings only for the initial call
		if check_siblings and self.parent:
			for sibling in self.parent.children:
				if sibling is not self and isinstance(sibling, DOMElementNode):
					result = sibling.get_file_upload_element(check_siblings=False)
					if result:
						return result

		return None


SelectorMap = dict[int, DOMElementNode]


@dataclass
class DOMState:
	element_tree: DOMElementNode
	selector_map: SelectorMap
````

## File: browser_use/exceptions.py
````python
class LLMException(Exception):
	def __init__(self, status_code, message):
		self.status_code = status_code
		self.message = message
		super().__init__(f'Error {status_code}: {message}')
````

## File: browser_use/logging_config.py
````python
import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()


def addLoggingLevel(levelName, levelNum, methodName=None):
	"""
	Comprehensively adds a new logging level to the `logging` module and the
	currently configured logging class.

	`levelName` becomes an attribute of the `logging` module with the value
	`levelNum`. `methodName` becomes a convenience method for both `logging`
	itself and the class returned by `logging.getLoggerClass()` (usually just
	`logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
	used.

	To avoid accidental clobberings of existing attributes, this method will
	raise an `AttributeError` if the level name is already an attribute of the
	`logging` module or if the method name is already present

	Example
	-------
	>>> addLoggingLevel('TRACE', logging.DEBUG - 5)
	>>> logging.getLogger(__name__).setLevel('TRACE')
	>>> logging.getLogger(__name__).trace('that worked')
	>>> logging.trace('so did this')
	>>> logging.TRACE
	5

	"""
	if not methodName:
		methodName = levelName.lower()

	if hasattr(logging, levelName):
		raise AttributeError('{} already defined in logging module'.format(levelName))
	if hasattr(logging, methodName):
		raise AttributeError('{} already defined in logging module'.format(methodName))
	if hasattr(logging.getLoggerClass(), methodName):
		raise AttributeError('{} already defined in logger class'.format(methodName))

	# This method was inspired by the answers to Stack Overflow post
	# http://stackoverflow.com/q/2183233/2988730, especially
	# http://stackoverflow.com/a/13638084/2988730
	def logForLevel(self, message, *args, **kwargs):
		if self.isEnabledFor(levelNum):
			self._log(levelNum, message, args, **kwargs)

	def logToRoot(message, *args, **kwargs):
		logging.log(levelNum, message, *args, **kwargs)

	logging.addLevelName(levelNum, levelName)
	setattr(logging, levelName, levelNum)
	setattr(logging.getLoggerClass(), methodName, logForLevel)
	setattr(logging, methodName, logToRoot)


def setup_logging():
	# Try to add RESULT level, but ignore if it already exists
	try:
		addLoggingLevel('RESULT', 35)  # This allows ERROR, FATAL and CRITICAL
	except AttributeError:
		pass  # Level already exists, which is fine

	log_type = os.getenv('BROWSER_USE_LOGGING_LEVEL', 'info').lower()

	# Check if handlers are already set up
	if logging.getLogger().hasHandlers():
		return

	# Clear existing handlers
	root = logging.getLogger()
	root.handlers = []

	class BrowserUseFormatter(logging.Formatter):
		def format(self, record):
			if isinstance(record.name, str) and record.name.startswith('browser_use.'):
				record.name = record.name.split('.')[-2]
			return super().format(record)

	# Setup single handler for all loggers
	console = logging.StreamHandler(sys.stdout)

	# adittional setLevel here to filter logs
	if log_type == 'result':
		console.setLevel('RESULT')
		console.setFormatter(BrowserUseFormatter('%(message)s'))
	else:
		console.setFormatter(BrowserUseFormatter('%(levelname)-8s [%(name)s] %(message)s'))

	# Configure root logger only
	root.addHandler(console)

	# switch cases for log_type
	if log_type == 'result':
		root.setLevel('RESULT')  # string usage to avoid syntax error
	elif log_type == 'debug':
		root.setLevel(logging.DEBUG)
	else:
		root.setLevel(logging.INFO)

	# Configure browser_use logger
	browser_use_logger = logging.getLogger('browser_use')
	browser_use_logger.propagate = False  # Don't propagate to root logger
	browser_use_logger.addHandler(console)
	browser_use_logger.setLevel(root.level)  # Set same level as root logger

	logger = logging.getLogger('browser_use')
	logger.info('BrowserUse logging setup complete with level %s', log_type)
	# Silence third-party loggers
	for logger in [
		'WDM',
		'httpx',
		'selenium',
		'playwright',
		'urllib3',
		'asyncio',
		'langchain',
		'openai',
		'httpcore',
		'charset_normalizer',
		'anthropic._base_client',
		'PIL.PngImagePlugin',
		'trafilatura.htmlprocessing',
		'trafilatura',
	]:
		third_party = logging.getLogger(logger)
		third_party.setLevel(logging.ERROR)
		third_party.propagate = False
````

## File: browser_use/README.md
````markdown
# Codebase Structure

> The code structure inspired by https://github.com/Netflix/dispatch.

Very good structure on how to make a scalable codebase is also in [this repo](https://github.com/zhanymkanov/fastapi-best-practices).

Just a brief document about how we should structure our backend codebase.

## Code Structure

```markdown
src/
/<service name>/
models.py
services.py
prompts.py
views.py
utils.py
routers.py

    	/_<subservice name>/
```

### Service.py

Always a single file, except if it becomes too long - more than ~500 lines, split it into \_subservices

### Views.py

Always split the views into two parts

```python
# All
...

# Requests
...

# Responses
...
```

If too long → split into multiple files

### Prompts.py

Single file; if too long → split into multiple files (one prompt per file or so)

### Routers.py

Never split into more than one file
````

## File: browser_use/telemetry/views.py
````python
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, Dict, Sequence


@dataclass
class BaseTelemetryEvent(ABC):
	@property
	@abstractmethod
	def name(self) -> str:
		pass

	@property
	def properties(self) -> Dict[str, Any]:
		return {k: v for k, v in asdict(self).items() if k != 'name'}


@dataclass
class RegisteredFunction:
	name: str
	params: dict[str, Any]


@dataclass
class ControllerRegisteredFunctionsTelemetryEvent(BaseTelemetryEvent):
	registered_functions: list[RegisteredFunction]
	name: str = 'controller_registered_functions'


@dataclass
class AgentStepTelemetryEvent(BaseTelemetryEvent):
	agent_id: str
	step: int
	step_error: list[str]
	consecutive_failures: int
	actions: list[dict]
	name: str = 'agent_step'


@dataclass
class AgentRunTelemetryEvent(BaseTelemetryEvent):
	agent_id: str
	use_vision: bool
	task: str
	model_name: str
	chat_model_library: str
	version: str
	source: str
	name: str = 'agent_run'


@dataclass
class AgentEndTelemetryEvent(BaseTelemetryEvent):
	agent_id: str
	steps: int
	max_steps_reached: bool
	is_done: bool
	success: bool | None
	total_input_tokens: int
	total_duration_seconds: float

	errors: Sequence[str | None]
	name: str = 'agent_end'
````

## File: browser_use/utils.py
````python
import asyncio
import logging
import os
import platform
import signal
import time
from functools import wraps
from sys import stderr
from typing import Any, Callable, Coroutine, List, Optional, ParamSpec, TypeVar

logger = logging.getLogger(__name__)

# Global flag to prevent duplicate exit messages
_exiting = False

# Define generic type variables for return type and parameters
R = TypeVar('R')
P = ParamSpec('P')


class SignalHandler:
	"""
	A modular and reusable signal handling system for managing SIGINT (Ctrl+C), SIGTERM,
	and other signals in asyncio applications.

	This class provides:
	- Configurable signal handling for SIGINT and SIGTERM
	- Support for custom pause/resume callbacks
	- Management of event loop state across signals
	- Standardized handling of first and second Ctrl+C presses
	- Cross-platform compatibility (with simplified behavior on Windows)
	"""

	def __init__(
		self,
		loop: Optional[asyncio.AbstractEventLoop] = None,
		pause_callback: Optional[Callable[[], None]] = None,
		resume_callback: Optional[Callable[[], None]] = None,
		custom_exit_callback: Optional[Callable[[], None]] = None,
		exit_on_second_int: bool = True,
		interruptible_task_patterns: List[str] = None,
	):
		"""
		Initialize the signal handler.

		Args:
			loop: The asyncio event loop to use. Defaults to current event loop.
			pause_callback: Function to call when system is paused (first Ctrl+C)
			resume_callback: Function to call when system is resumed
			custom_exit_callback: Function to call on exit (second Ctrl+C or SIGTERM)
			exit_on_second_int: Whether to exit on second SIGINT (Ctrl+C)
			interruptible_task_patterns: List of patterns to match task names that should be
										 canceled on first Ctrl+C (default: ['step', 'multi_act', 'get_next_action'])
		"""
		self.loop = loop or asyncio.get_event_loop()
		self.pause_callback = pause_callback
		self.resume_callback = resume_callback
		self.custom_exit_callback = custom_exit_callback
		self.exit_on_second_int = exit_on_second_int
		self.interruptible_task_patterns = interruptible_task_patterns or ['step', 'multi_act', 'get_next_action']
		self.is_windows = platform.system() == 'Windows'

		# Initialize loop state attributes
		self._initialize_loop_state()

		# Store original signal handlers to restore them later if needed
		self.original_sigint_handler = None
		self.original_sigterm_handler = None

	def _initialize_loop_state(self) -> None:
		"""Initialize loop state attributes used for signal handling."""
		setattr(self.loop, 'ctrl_c_pressed', False)
		setattr(self.loop, 'waiting_for_input', False)

	def register(self) -> None:
		"""Register signal handlers for SIGINT and SIGTERM."""
		try:
			if self.is_windows:
				# On Windows, use simple signal handling with immediate exit on Ctrl+C
				def windows_handler(sig, frame):
					print('\n\n🛑 Got Ctrl+C. Exiting immediately on Windows...\n', file=stderr)
					# Run the custom exit callback if provided
					if self.custom_exit_callback:
						self.custom_exit_callback()
					os._exit(0)

				self.original_sigint_handler = signal.signal(signal.SIGINT, windows_handler)
			else:
				# On Unix-like systems, use asyncio's signal handling for smoother experience
				self.original_sigint_handler = self.loop.add_signal_handler(signal.SIGINT, lambda: self.sigint_handler())
				self.original_sigterm_handler = self.loop.add_signal_handler(signal.SIGTERM, lambda: self.sigterm_handler())

		except Exception:
			# there are situations where signal handlers are not supported, e.g.
			# - when running in a thread other than the main thread
			# - some operating systems
			# - inside jupyter notebooks
			pass

	def unregister(self) -> None:
		"""Unregister signal handlers and restore original handlers if possible."""
		try:
			if self.is_windows:
				# On Windows, just restore the original SIGINT handler
				if self.original_sigint_handler:
					signal.signal(signal.SIGINT, self.original_sigint_handler)
			else:
				# On Unix-like systems, use asyncio's signal handler removal
				self.loop.remove_signal_handler(signal.SIGINT)
				self.loop.remove_signal_handler(signal.SIGTERM)

				# Restore original handlers if available
				if self.original_sigint_handler:
					signal.signal(signal.SIGINT, self.original_sigint_handler)
				if self.original_sigterm_handler:
					signal.signal(signal.SIGTERM, self.original_sigterm_handler)
		except Exception as e:
			logger.warning(f'Error while unregistering signal handlers: {e}')

	def _handle_second_ctrl_c(self) -> None:
		"""
		Handle a second Ctrl+C press by performing cleanup and exiting.
		This is shared logic used by both sigint_handler and wait_for_resume.
		"""
		global _exiting

		if not _exiting:
			_exiting = True

			# Call custom exit callback if provided
			if self.custom_exit_callback:
				try:
					self.custom_exit_callback()
				except Exception as e:
					logger.error(f'Error in exit callback: {e}')

		# Force immediate exit - more reliable than sys.exit()
		print('\n\n🛑  Got second Ctrl+C. Exiting immediately...\n', file=stderr)
		# write carriage return + newline + ASNI reset to both stdout and stderr to clear any color codes
		print('\r\033[0m', end='', flush=True, file=stderr)
		print('\r\033[0m', end='', flush=True)
		os._exit(0)

	def sigint_handler(self) -> None:
		"""
		SIGINT (Ctrl+C) handler.

		First Ctrl+C: Cancel current step and pause.
		Second Ctrl+C: Exit immediately if exit_on_second_int is True.
		"""
		global _exiting

		if _exiting:
			# Already exiting, force exit immediately
			os._exit(0)

		if getattr(self.loop, 'ctrl_c_pressed', False):
			# If we're in the waiting for input state, let the pause method handle it
			if getattr(self.loop, 'waiting_for_input', False):
				return

			# Second Ctrl+C - exit immediately if configured to do so
			if self.exit_on_second_int:
				self._handle_second_ctrl_c()

		# Mark that Ctrl+C was pressed
		self.loop.ctrl_c_pressed = True

		# Cancel current tasks that should be interruptible - this is crucial for immediate pausing
		self._cancel_interruptible_tasks()

		# Call pause callback if provided - this sets the paused flag
		if self.pause_callback:
			try:
				self.pause_callback()
			except Exception as e:
				logger.error(f'Error in pause callback: {e}')

		# Log pause message after pause_callback is called (not before)
		print('----------------------------------------------------------------------', file=stderr)

	def sigterm_handler(self) -> None:
		"""
		SIGTERM handler.

		Always exits the program completely.
		"""
		global _exiting
		if not _exiting:
			_exiting = True
			print('\n\n🛑 SIGTERM received. Exiting immediately...\n\n', file=stderr)

			# Call custom exit callback if provided
			if self.custom_exit_callback:
				self.custom_exit_callback()

		os._exit(0)

	def _cancel_interruptible_tasks(self) -> None:
		"""Cancel current tasks that should be interruptible."""
		current_task = asyncio.current_task(self.loop)
		for task in asyncio.all_tasks(self.loop):
			if task != current_task and not task.done():
				task_name = task.get_name() if hasattr(task, 'get_name') else str(task)
				# Cancel tasks that match certain patterns
				if any(pattern in task_name for pattern in self.interruptible_task_patterns):
					logger.debug(f'Cancelling task: {task_name}')
					task.cancel()
					# Add exception handler to silence "Task exception was never retrieved" warnings
					task.add_done_callback(lambda t: t.exception() if t.cancelled() else None)

		# Also cancel the current task if it's interruptible
		if current_task and not current_task.done():
			task_name = current_task.get_name() if hasattr(current_task, 'get_name') else str(current_task)
			if any(pattern in task_name for pattern in self.interruptible_task_patterns):
				logger.debug(f'Cancelling current task: {task_name}')
				current_task.cancel()

	def wait_for_resume(self) -> None:
		"""
		Wait for user input to resume or exit.

		This method should be called after handling the first Ctrl+C.
		It temporarily restores default signal handling to allow catching
		a second Ctrl+C directly.
		"""
		# Set flag to indicate we're waiting for input
		setattr(self.loop, 'waiting_for_input', True)

		# Temporarily restore default signal handling for SIGINT
		# This ensures KeyboardInterrupt will be raised during input()
		original_handler = signal.getsignal(signal.SIGINT)
		try:
			signal.signal(signal.SIGINT, signal.default_int_handler)
		except ValueError:
			# we are running in a thread other than the main thread
			# or signal handlers are not supported for some other reason
			pass

		green = '\x1b[32;1m'
		red = '\x1b[31m'
		blink = '\033[33;5m'
		unblink = '\033[0m'
		reset = '\x1b[0m'

		try:  # escape code is to blink the ...
			print(
				f'➡️  Press {green}[Enter]{reset} to resume or {red}[Ctrl+C]{reset} again to exit{blink}...{unblink} ',
				end='',
				flush=True,
				file=stderr,
			)
			input()  # This will raise KeyboardInterrupt on Ctrl+C

			# Call resume callback if provided
			if self.resume_callback:
				self.resume_callback()
		except KeyboardInterrupt:
			# Use the shared method to handle second Ctrl+C
			self._handle_second_ctrl_c()
		finally:
			try:
				# Restore our signal handler
				signal.signal(signal.SIGINT, original_handler)
				setattr(self.loop, 'waiting_for_input', False)
			except Exception:
				pass

	def reset(self) -> None:
		"""Reset state after resuming."""
		# Clear the flags
		if hasattr(self.loop, 'ctrl_c_pressed'):
			self.loop.ctrl_c_pressed = False
		if hasattr(self.loop, 'waiting_for_input'):
			self.loop.waiting_for_input = False


def time_execution_sync(additional_text: str = '') -> Callable[[Callable[P, R]], Callable[P, R]]:
	def decorator(func: Callable[P, R]) -> Callable[P, R]:
		@wraps(func)
		def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
			start_time = time.time()
			result = func(*args, **kwargs)
			execution_time = time.time() - start_time
			logger.debug(f'{additional_text} Execution time: {execution_time:.2f} seconds')
			return result

		return wrapper

	return decorator


def time_execution_async(
	additional_text: str = '',
) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]]:
	def decorator(func: Callable[P, Coroutine[Any, Any, R]]) -> Callable[P, Coroutine[Any, Any, R]]:
		@wraps(func)
		async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
			start_time = time.time()
			result = await func(*args, **kwargs)
			execution_time = time.time() - start_time
			logger.debug(f'{additional_text} Execution time: {execution_time:.2f} seconds')
			return result

		return wrapper

	return decorator


def singleton(cls):
	instance = [None]

	def wrapper(*args, **kwargs):
		if instance[0] is None:
			instance[0] = cls(*args, **kwargs)
		return instance[0]

	return wrapper


def check_env_variables(keys: list[str], any_or_all=all) -> bool:
	"""Check if all required environment variables are set"""
	return any_or_all(os.getenv(key, '').strip() for key in keys)
````

## File: codebeaver.yml
````yaml
environment:
- OPENAI_API_KEY=empty
- AZURE_OPENAI_KEY=empty
from: pytest
````

## File: conftest.py
````python
import os
import sys

from browser_use.logging_config import setup_logging

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

setup_logging()
````

## File: docs/cloud/implementation.mdx
````
---
title: "Implementing the API"
description: "Learn how to implement the Browser Use API in Python"
icon: "code"
---

This guide shows how to implement common API patterns using Python. We'll create a complete example that creates and monitors a browser automation task.

## Basic Implementation

For all settings see [Run Task](cloud/api-v10/run-task).

Here's a simple implementation using Python's `requests` library to stream the task steps:

```python
import json
import time

import requests

API_KEY = 'your_api_key_here'
BASE_URL = 'https://api.browser-use.com/api/v1'
HEADERS = {'Authorization': f'Bearer {API_KEY}'}


def create_task(instructions: str):
	"""Create a new browser automation task"""
	response = requests.post(f'{BASE_URL}/run-task', headers=HEADERS, json={'task': instructions})
	return response.json()['id']


def get_task_status(task_id: str):
	"""Get current task status"""
	response = requests.get(f'{BASE_URL}/task/{task_id}/status', headers=HEADERS)
	return response.json()


def get_task_details(task_id: str):
	"""Get full task details including output"""
	response = requests.get(f'{BASE_URL}/task/{task_id}', headers=HEADERS)
	return response.json()


def wait_for_completion(task_id: str, poll_interval: int = 2):
	"""Poll task status until completion"""
	count = 0
	unique_steps = []
	while True:
		details = get_task_details(task_id)
		new_steps = details['steps']
		# use only the new steps that are not in unique_steps.
		if new_steps != unique_steps:
			for step in new_steps:
				if step not in unique_steps:
					print(json.dumps(step, indent=4))
			unique_steps = new_steps
		count += 1
		status = details['status']

		if status in ['finished', 'failed', 'stopped']:
			return details
		time.sleep(poll_interval)


def main():
	task_id = create_task('Open https://www.google.com and search for openai')
	print(f'Task created with ID: {task_id}')
	task_details = wait_for_completion(task_id)
	print(f"Final output: {task_details['output']}")


if __name__ == '__main__':
	main()

```

## Task Control Example

Here's how to implement task control with pause/resume functionality:

```python
def control_task():
    # Create a new task
    task_id = create_task("Go to google.com and search for Browser Use")

    # Wait for 5 seconds
    time.sleep(5)

    # Pause the task
    requests.put(f"{BASE_URL}/pause-task?task_id={task_id}", headers=HEADERS)
    print("Task paused! Check the live preview.")

    # Wait for user input
    input("Press Enter to resume...")

    # Resume the task
    requests.put(f"{BASE_URL}/resume-task?task_id={task_id}", headers=HEADERS)

    # Wait for completion
    result = wait_for_completion(task_id)
    print(f"Task completed with output: {result['output']}")
```

## Structured Output Example

Here's how to implement a task with structured JSON output:

```python
import json
import os
import time
import requests
from pydantic import BaseModel
from typing import List


API_KEY = os.getenv("API_KEY")
BASE_URL = 'https://api.browser-use.com/api/v1'
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


# Define output schema using Pydantic
class SocialMediaCompany(BaseModel):
    name: str
    market_cap: float
    headquarters: str
    founded_year: int


class SocialMediaCompanies(BaseModel):
    companies: List[SocialMediaCompany]


def create_structured_task(instructions: str, schema: dict):
    """Create a task that expects structured output"""
    payload = {
        "task": instructions,
        "structured_output_json": json.dumps(schema)
    }
    response = requests.post(f"{BASE_URL}/run-task", headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["id"]


def wait_for_task_completion(task_id: str, poll_interval: int = 5):
    """Poll task status until it completes"""
    while True:
        response = requests.get(f"{BASE_URL}/task/{task_id}/status", headers=HEADERS)
        response.raise_for_status()
        status = response.json()
        if status == "finished":
            break
        elif status in ["failed", "stopped"]:
            raise RuntimeError(f"Task {task_id} ended with status: {status}")
        print("Waiting for task to finish...")
        time.sleep(poll_interval)


def fetch_task_output(task_id: str):
    """Retrieve the final task result"""
    response = requests.get(f"{BASE_URL}/task/{task_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()["output"]


def main():
    schema = SocialMediaCompanies.model_json_schema()
    task_id = create_structured_task(
        "Get me the top social media companies by market cap",
        schema
    )
    print(f"Task created with ID: {task_id}")

    wait_for_task_completion(task_id)
    print("Task completed!")

    output = fetch_task_output(task_id)
    print("Raw output:", output)

    try:
        parsed = SocialMediaCompanies.model_validate_json(output)
        print("Parsed output:")
        print(parsed)
    except Exception as e:
        print(f"Failed to parse structured output: {e}")


if __name__ == "__main__":
    main()
```

<Note>
  Remember to handle your API key securely and implement proper error handling
  in production code.
</Note>
````

## File: docs/cloud/quickstart.mdx
````
---
title: "Quickstart"
description: "Learn how to get started with the Browser Use Cloud API"
icon: "cloud"
---

The Browser Use Cloud API lets you create and manage browser automation agents programmatically. Each agent can execute tasks and provide real-time feedback through a live preview URL.

## Prerequisites

<Note>
  You need an active subscription and an API key from
  [cloud.browser-use.com/billing](https://cloud.browser-use.com/billing)
</Note>

## Pricing

The Browser Use Cloud API is priced at <b>$0.05 per step</b> that the agent executes.

<Note>
  Since Browser Use can execute multiple steps at the same time, the price for
  filling out forms is much lower than other services.
</Note>

## Creating Your First Agent

Create a new browser automation task by providing instructions in natural language:

```bash
curl -X POST https://api.browser-use.com/api/v1/run-task \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Go to google.com and search for Browser Use"
  }'
```

The API returns a task ID that you can use to manage the task and check the live preview URL.

<Note>
  The task response includes a `live_url` that you can embed in an iframe to
  watch and control the agent in real-time.
</Note>

## Managing Tasks

Control running tasks with these operations:

<AccordionGroup>
  <Accordion title="Pause/Resume Tasks">
    Temporarily pause task execution with [`/api/v1/pause-task`](/cloud/api-v1/pause-task) and resume with
    [`/api/v1/resume-task`](/cloud/api-v1/resume-task). Useful for manual inspection or intervention.
  </Accordion>

  <Accordion title="Stop Tasks">
    Permanently stop a task using [`/api/v1/stop-task`](/cloud/api-v1/stop-task). The task cannot be
    resumed after being stopped.
  </Accordion>
</AccordionGroup>

For detailed API documentation, see the tabs on the left, which include the full coverage of the API.

## Building your own client (OpenAPI)

<Note>
  We recommend this only if you don't need control and only need to run simple
  tasks.
</Note>

The best way to build your own client is to use our [OpenAPI specification](http://api.browser-use.com/openapi.json) to generate a type-safe client library.

### Python

Use [openapi-python-client](https://github.com/openapi-generators/openapi-python-client) to generate a modern Python client:

```bash
# Install the generator
pipx install openapi-python-client --include-deps

# Generate the client
openapi-python-client generate --url http://api.browser-use.com/openapi.json
```

This will create a Python package with full type hints, modern dataclasses, and async support.

### TypeScript/JavaScript

For TypeScript projects, use [openapi-typescript](https://www.npmjs.com/package/openapi-typescript) to generate type definitions:

```bash
# Install the generator
npm install -D openapi-typescript

# Generate the types
npx openapi-typescript http://api.browser-use.com/openapi.json -o browser-use-api.ts
```

This will create TypeScript definitions you can use with your preferred HTTP client.

<Note>
  Need help? Contact our support team at support@browser-use.com or join our
  [Discord community](https://link.browser-use.com/discord)
</Note>
````

## File: docs/customize/agent-settings.mdx
````
---
title: "Agent Settings"
description: "Learn how to configure the agent"
icon: "gear"
---

## Overview

The `Agent` class is the core component of Browser Use that handles browser automation. Here are the main configuration options you can use when initializing an agent.

## Basic Settings

```python
from browser_use import Agent
from langchain_openai import ChatOpenAI

agent = Agent(
    task="Search for latest news about AI",
    llm=ChatOpenAI(model="gpt-4o"),
)
```

### Required Parameters

- `task`: The instruction for the agent to execute
- `llm`: A LangChain chat model instance. See <a href="/customize/supported-models">LangChain Models</a> for supported models.

## Agent Behavior

Control how the agent operates:

```python
agent = Agent(
    task="your task",
    llm=llm,
    controller=custom_controller,  # For custom tool calling
    use_vision=True,              # Enable vision capabilities
    save_conversation_path="logs/conversation"  # Save chat logs
)
```

### Behavior Parameters

- `controller`: Registry of functions the agent can call. Defaults to base Controller. See <a href="/customize/custom-functions">Custom Functions</a> for details.
- `use_vision`: Enable/disable vision capabilities. Defaults to `True`.
  - When enabled, the model processes visual information from web pages
  - Disable to reduce costs or use models without vision support
  - For GPT-4o, image processing costs approximately 800-1000 tokens (~$0.002 USD) per image (but this depends on the defined screen size)
- `save_conversation_path`: Path to save the complete conversation history. Useful for debugging.
- `override_system_message`: Completely replace the default system prompt with a custom one.
- `extend_system_message`: Add additional instructions to the default system prompt.

<Note>
  Vision capabilities are recommended for better web interaction understanding,
  but can be disabled to reduce costs or when using models without vision
  support.
</Note>

## (Reuse) Browser Configuration

You can configure how the agent interacts with the browser. To see more `Browser` options refer to the <a href="/customize/browser-settings">Browser Settings</a> documentation.

### Reuse Existing Browser

`browser`: A Browser Use Browser instance. When provided, the agent will reuse this browser instance and automatically create new contexts for each `run()`.

```python
from browser_use import Agent, Browser
from browser_use.browser.context import BrowserContext

# Reuse existing browser
browser = Browser()
agent = Agent(
    task=task1,
    llm=llm,
    browser=browser  # Browser instance will be reused
)

await agent.run()

# Manually close the browser
await browser.close()
```

<Note>
  Remember: in this scenario the `Browser` will not be closed automatically.
</Note>

### Reuse Existing Browser Context

`browser_context`: A Playwright browser context. Useful for maintaining persistent sessions. See <a href="/customize/persistent-browser">Persistent Browser</a> for more details.

```python
from browser_use import Agent, Browser
from patchright.async_api import BrowserContext

# Use specific browser context (preferred method)
async with await browser.new_context() as context:
    agent = Agent(
        task=task2,
        llm=llm,
        browser_context=context  # Use persistent context
    )

    # Run the agent
    await agent.run()

    # Pass the context to the next agent
    next_agent = Agent(
        task=task2,
        llm=llm,
        browser_context=context
    )

    ...

await browser.close()
```

For more information about how browser context works, refer to the [Playwright
documentation](https://playwright.dev/docs/api/class-browsercontext).

<Note>
  You can reuse the same context for multiple agents. If you do nothing, the
  browser will be automatically created and closed on `run()` completion.
</Note>

## Running the Agent

The agent is executed using the async `run()` method:

- `max_steps` (default: `100`)
  Maximum number of steps the agent can take during execution. This prevents infinite loops and helps control execution time.

## Agent History

The method returns an `AgentHistoryList` object containing the complete execution history. This history is invaluable for debugging, analysis, and creating reproducible scripts.

```python
# Example of accessing history
history = await agent.run()

# Access (some) useful information
history.urls()              # List of visited URLs
history.screenshots()       # List of screenshot paths
history.action_names()      # Names of executed actions
history.extracted_content() # Content extracted during execution
history.errors()           # Any errors that occurred
history.model_actions()     # All actions with their parameters
```

The `AgentHistoryList` provides many helper methods to analyze the execution:

- `final_result()`: Get the final extracted content
- `is_done()`: Check if the agent completed successfully
- `has_errors()`: Check if any errors occurred
- `model_thoughts()`: Get the agent's reasoning process
- `action_results()`: Get results of all actions

<Note>
  For a complete list of helper methods and detailed history analysis
  capabilities, refer to the [AgentHistoryList source
  code](https://github.com/browser-use/browser-use/blob/main/browser_use/agent/views.py#L111).
</Note>

## Run initial actions without LLM
With [this example](https://github.com/browser-use/browser-use/blob/main/examples/features/initial_actions.py) you can run initial actions without the LLM.
Specify the action as a dictionary where the key is the action name and the value is the action parameters. You can find all our actions in the [Controller](https://github.com/browser-use/browser-use/blob/main/browser_use/controller/service.py) source code.
```python

initial_actions = [
	{'open_tab': {'url': 'https://www.google.com'}},
	{'open_tab': {'url': 'https://en.wikipedia.org/wiki/Randomness'}},
	{'scroll_down': {'amount': 1000}},
]
agent = Agent(
	task='What theories are displayed on the page?',
	initial_actions=initial_actions,
	llm=llm,
)
```

## Run with message context

You can configure the agent and provide a separate message to help the LLM understand the task better.

```python
from langchain_openai import ChatOpenAI

agent = Agent(
    task="your task",
    message_context="Additional information about the task",
    llm = ChatOpenAI(model='gpt-4o')
)
```

## Run with planner model

You can configure the agent to use a separate planner model for high-level task planning:

```python
from langchain_openai import ChatOpenAI

# Initialize models
llm = ChatOpenAI(model='gpt-4o')
planner_llm = ChatOpenAI(model='o3-mini')

agent = Agent(
    task="your task",
    llm=llm,
    planner_llm=planner_llm,           # Separate model for planning
    use_vision_for_planner=False,      # Disable vision for planner
    planner_interval=4                 # Plan every 4 steps
)
```

### Planner Parameters

- `planner_llm`: A LangChain chat model instance used for high-level task planning. Can be a smaller/cheaper model than the main LLM.
- `use_vision_for_planner`: Enable/disable vision capabilities for the planner model. Defaults to `True`.
- `planner_interval`: Number of steps between planning phases. Defaults to `1`.

Using a separate planner model can help:
- Reduce costs by using a smaller model for high-level planning
- Improve task decomposition and strategic thinking
- Better handle complex, multi-step tasks

<Note>
  The planner model is optional. If not specified, the agent will not use the planner model.
</Note>

### Optional Parameters

- `message_context`: Additional information about the task to help the LLM understand the task better.
- `initial_actions`: List of initial actions to run before the main task.
- `max_actions_per_step`: Maximum number of actions to run in a step. Defaults to `10`.
- `max_failures`: Maximum number of failures before giving up. Defaults to `3`.
- `retry_delay`: Time to wait between retries in seconds when rate limited. Defaults to `10`.
- `generate_gif`: Enable/disable GIF generation. Defaults to `False`. Set to `True` or a string path to save the GIF.
## Memory Management

Browser Use includes a procedural memory system using [Mem0](https://mem0.ai) that automatically summarizes the agent's conversation history at regular intervals to optimize context window usage during long tasks.

```python
from browser_use.agent.memory import MemoryConfig

agent = Agent(
    task="your task",
    llm=llm,
    enable_memory=True,
    memory_config=MemoryConfig(
        agent_id="my_custom_agent",
        memory_interval=15
    )
)
```

### Memory Parameters

- `enable_memory`: Enable/disable the procedural memory system. Defaults to `True`.
- `memory_config`: A `MemoryConfig` Pydantic model instance (required). Dictionary format is not supported.

### Using MemoryConfig

You must configure the memory system using the `MemoryConfig` Pydantic model for a type-safe approach:

```python
from browser_use.agent.memory import MemoryConfig

agent = Agent(
    task=task_description,
    llm=llm,
    memory_config=MemoryConfig(
        agent_id="my_agent",
        memory_interval=15,
        embedder_provider="openai",
        embedder_model="text-embedding-3-large",
        embedder_dims=1536,
    )
)
```

The `MemoryConfig` model provides these configuration options:

#### Memory Settings
- `agent_id`: Unique identifier for the agent (default: `"browser_use_agent"`)
- `memory_interval`: Number of steps between memory summarization (default: `10`)

#### Embedder Settings
- `embedder_provider`: Provider for embeddings (`'openai'`, `'gemini'`, `'ollama'`, or `'huggingface'`)
- `embedder_model`: Model name for the embedder
- `embedder_dims`: Dimensions for the embeddings

#### Vector Store Settings
- `vector_store_provider`: Provider for vector storage (currently only `'faiss'` is supported)
- `vector_store_base_path`: Path for storing vector data (e.g. /tmp/mem0)

The model automatically sets appropriate defaults based on the LLM being used:
- For `ChatOpenAI`: Uses OpenAI's `text-embedding-3-small` embeddings
- For `ChatGoogleGenerativeAI`: Uses Gemini's `models/text-embedding-004` embeddings
- For `ChatOllama`: Uses Ollama's `nomic-embed-text` embeddings
- Default: Uses Hugging Face's `all-MiniLM-L6-v2` embeddings

<Note>
  Always pass a properly constructed `MemoryConfig` object to the `memory_config` parameter. 
  Dictionary-based configuration is no longer supported.
</Note>

### How Memory Works

When enabled, the agent periodically compresses its conversation history into concise summaries:

1. Every `memory_interval` steps, the agent reviews its recent interactions
2. It creates a procedural memory summary using the same LLM as the agent
3. The original messages are replaced with the summary, reducing token usage
4. This process helps maintain important context while freeing up the context window

### Disabling Memory

If you want to disable the memory system (for debugging or for shorter tasks), set `enable_memory` to `False`:

```python
agent = Agent(
    task="your task",
    llm=llm,
    enable_memory=False
)
```

<Note>
  Disabling memory may be useful for debugging or short tasks, but for longer
  tasks, it can lead to context window overflow as the conversation history
  grows. The memory system helps maintain performance during extended sessions.
</Note>
````

## File: docs/customize/browser-settings.mdx
````
---
title: "Browser Settings"
description: "Configure browser behavior and context settings"
icon: "globe"
---

Browser Use allows you to customize the browser's behavior through two main configuration classes: `BrowserConfig` and `BrowserContextConfig`. These settings control everything from headless mode to proxy settings and page load behavior.

<Note>
  We are currently working on improving how browser contexts are managed. The
  system will soon transition to a "1 agent, 1 browser, 1 context" model for
  better stability and developer experience.
</Note>

# Browser Configuration

The `BrowserConfig` class controls the core browser behavior and connection settings.

```python
from browser_use import BrowserConfig

# Basic configuration
config = BrowserConfig(
    headless=False,
    disable_security=False
)

browser = Browser(config=config)

agent = Agent(
    browser=browser,
    # ...
)
```

## Core Settings

- **headless** (default: `False`)
  Runs the browser without a visible UI. Note that some websites may detect headless mode.

- **disable_security** (default: `False`)
  Disables browser security features. While this can fix certain functionality issues (like cross-site iFrames), it should be used cautiously, especially when visiting untrusted websites.

### Additional Settings

- **extra_browser_args** (default: `[]`)
  Additional arguments are passed to the browser at launch. See the [full list of available arguments](https://github.com/browser-use/browser-use/blob/main/browser_use/browser/browser.py#L180).

- **proxy** (default: `None`)
  Standard Playwright proxy settings for using external proxy services.

- **new_context_config** (default: `BrowserContextConfig()`)
  Default settings for new browser contexts. See Context Configuration below.

<Note>
  For web scraping tasks on sites that restrict automated access, we recommend
  using external browser or proxy providers for better reliability.
</Note>

## Alternative Initialization

These settings allow you to connect to external browser providers or use a local Chrome instance.

### External Browser Provider (wss)

Connect to cloud-based browser services for enhanced reliability and proxy capabilities.

```python
config = BrowserConfig(
    wss_url="wss://your-browser-provider.com/ws"
)
```

- **wss_url** (default: `None`)
  WebSocket URL for connecting to external browser providers (e.g., [anchorbrowser.io](https://anchorbrowser.io), steel.dev, browserbase.com, browserless.io, [TestingBot](https://testingbot.com/support/ai/integrations/browser-use)).

<Note>
  This overrides local browser settings and uses the provider's configuration.
  Refer to their documentation for settings.
</Note>

### External Browser Provider (cdp)

Connect to cloud or local Chrome instances using Chrome DevTools Protocol (CDP) for use with tools like `headless-shell` or `browserless`.

```python
config = BrowserConfig(
    cdp_url="http://localhost:9222"
)
```

- **cdp_url** (default: `None`)
  URL for connecting to a Chrome instance via CDP. Commonly used for debugging or connecting to locally running Chrome instances.

### Local Chrome Instance (binary)

Connect to your existing Chrome installation to access saved states and cookies.

```python
config = BrowserConfig(
    browser_binary_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)
```

- **browser_binary_path** (default: `None`)
  Path to connect to an existing Browser installation. Particularly useful for workflows requiring existing login states or browser preferences.

<Note>This will overwrite other browser settings.</Note>

# Context Configuration

The `BrowserContextConfig` class controls settings for individual browser contexts.

```python
from browser_use.browser.context import BrowserContextConfig

config = BrowserContextConfig(
    cookies_file="path/to/cookies.json",
    wait_for_network_idle_page_load_time=3.0,
    browser_window_size={'width': 1280, 'height': 1100},
    locale='en-US',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    highlight_elements=True,
    viewport_expansion=500,
    allowed_domains=['google.com', 'wikipedia.org'],
)

browser = Browser()
context = BrowserContext(browser=browser, config=config)


async def run_search():
	agent = Agent(
		browser_context=context,
		task='Your task',
		llm=llm)
```

## Configuration Options

### Page Load Settings

- **minimum_wait_page_load_time** (default: `0.5`)
  Minimum time to wait before capturing page state for LLM input.

- **wait_for_network_idle_page_load_time** (default: `1.0`)
  Time to wait for network activity to cease. Increase to 3-5s for slower websites. This tracks essential content loading, not dynamic elements like videos.

- **maximum_wait_page_load_time** (default: `5.0`)
  Maximum time to wait for page load before proceeding.

### Display Settings

- **browser_window_size** (default: `{'width': 1280, 'height': 1100}`)
  Browser window dimensions. The default size is optimized for general use cases and interaction with common UI elements like cookie banners.

- **locale** (default: `None`)
  Specify user locale, for example en-GB, de-DE, etc. Locale will affect the navigator. Language value, Accept-Language request header value as well as number and date formatting rules. If not provided, defaults to the system default locale.

- **highlight_elements** (default: `True`)
  Highlight interactive elements on the screen with colorful bounding boxes.

- **viewport_expansion** (default: `500`)
  Viewport expansion in pixels. With this you can control how much of the page is included in the context of the LLM. If set to -1, all elements from the entire page will be included (this leads to high token usage). If set to 0, only the elements which are visible in the viewport will be included.
  Default is 500 pixels, that means that we include a little bit more than the visible viewport inside the context.

### Restrict URLs

- **allowed_domains** (default: `None`)
  List of allowed domains that the agent can access. If None, all domains are allowed.
  Example: ['google.com', 'wikipedia.org'] - Here the agent will only be able to access google and wikipedia.

### Debug and Recording

- **save_recording_path** (default: `None`)
  Directory path for saving video recordings.

- **trace_path** (default: `None`)
  Directory path for saving trace files. Files are automatically named as `{trace_path}/{context_id}.zip`.
````

## File: docs/customize/custom-functions.mdx
````
---
title: "Custom Functions"
description: "Extend default agent and write custom function calls"
icon: "function"
---

## Basic Function Registration

Functions can be either `sync` or `async`. Keep them focused and single-purpose.

```python
from browser_use import Controller, ActionResult
# Initialize the controller
controller = Controller()

@controller.action('Ask user for information')
def ask_human(question: str) -> str:
    answer = input(f'\n{question}\nInput: ')
    return ActionResult(extracted_content=answer)
```

<Note>
  Basic `Controller` has all basic functionality you might need to interact with
  the browser already implemented.
</Note>

```python
# ... then pass controller to the agent
agent = Agent(
    task=task,
    llm=llm,
    controller=controller
)
```

<Note>
  Keep the function name and description short and concise. The Agent use the
  function solely based on the name and description. The stringified output of
  the action is passed to the Agent.
</Note>

## Browser-Aware Functions

For actions that need browser access, simply add the `browser` parameter inside the function parameters:

<Note>
  Please note that browser-use’s `Browser` class is a wrapper class around
  Playwright’s `Browser`. The `Browser.playwright_browser` attr can be used
  to directly access the Playwright browser object if needed.
</Note>

```python
from browser_use import Browser, Controller, ActionResult

controller = Controller()
@controller.action('Open website')
async def open_website(url: str, browser: Browser):
    page = await browser.get_current_page()
    await page.goto(url)
    return ActionResult(extracted_content='Website opened')
```

## Structured Parameters with Pydantic

For complex actions, you can define parameter schemas using Pydantic models:

```python
from pydantic import BaseModel
from typing import Optional
from browser_use import Controller, ActionResult, Browser

controller = Controller()

class JobDetails(BaseModel):
    title: str
    company: str
    job_link: str
    salary: Optional[str] = None

@controller.action(
    'Save job details which you found on page',
    param_model=JobDetails
)
async def save_job(params: JobDetails, browser: Browser):
    print(f"Saving job: {params.title} at {params.company}")

    # Access browser if needed
    page = browser.get_current_page()
    await page.goto(params.job_link)
```

## Using Custom Actions with multiple agents

You can use the same controller for multiple agents.

```python
controller = Controller()

# ... register actions to the controller

agent = Agent(
    task="Go to website X and find the latest news",
    llm=llm,
    controller=controller
)

# Run the agent
await agent.run()

agent2 = Agent(
    task="Go to website Y and find the latest news",
    llm=llm,
    controller=controller
)

await agent2.run()
```

<Note>
  The controller is stateless and can be used to register multiple actions and
  multiple agents.
</Note>



## Exclude functions
If you want less actions to be used by the agent, you can exclude them from the controller.
```python
controller = Controller(exclude_actions=['open_tab', 'search_google'])
```


For more examples like file upload or notifications, visit [examples/custom-functions](https://github.com/browser-use/browser-use/tree/main/examples/custom-functions).
````

## File: docs/customize/hooks.mdx
````
---
title: "Lifecycle Hooks"
description: "Customize agent behavior with lifecycle hooks"
icon: "Wrench"
author: "Carlos A. Planchón"
---

# Using Agent Lifecycle Hooks

Browser-Use provides lifecycle hooks that allow you to execute custom code at specific points during the agent's execution. These hooks enable you to capture detailed information about the agent's actions, modify behavior, or integrate with external systems.

## Available Hooks

Currently, Browser-Use provides the following hooks:

| Hook | Description | When it's called |
| ---- | ----------- | ---------------- |
| `on_step_start` | Executed at the beginning of each agent step | Before the agent processes the current state and decides on the next action |
| `on_step_end` | Executed at the end of each agent step | After the agent has executed the action for the current step |

## Using Hooks

Hooks are passed as parameters to the `agent.run()` method. Each hook should be a callable function that accepts the agent instance as its parameter.

### Basic Example

```python
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def my_step_hook(agent):
    # inside a hook you can access all the state and methods under the Agent object:
    #   agent.settings, agent.state, agent.task
    #   agent.controller, agent.llm, agent.browser, agent.browser_context
    #   agent.pause(), agent.resume(), agent.add_new_task(...), etc.
    
    current_page = await agent.browser_context.get_current_page()
    
    visit_log = agent.state.history.urls()
    current_url = current_page.url
    previous_url = visit_log[-2] if len(visit_log) >= 2 else None
    print(f"Agent was last on URL: {previous_url} and is now on {current_url}")
    
    if 'completed' in current_url:
        agent.pause()
        Path('result.txt').write_text(await current_page.content()) 
        input('Saved "completed" page content to result.txt, press [Enter] to resume...')
        agent.resume()
    
agent = Agent(
    task="Search for the latest news about AI",
    llm=ChatOpenAI(model="gpt-4o"),
)

await agent.run(
    on_step_start=my_step_hook,
    # on_step_end=...
    max_steps=10
)
```

## Complete Example: Agent Activity Recording System

This comprehensive example demonstrates a complete implementation for recording and saving Browser-Use agent activity, consisting of both server and client components.

### Setup Instructions

To use this example, you'll need to:

1. Set up the required dependencies:
   ```bash
   pip install fastapi uvicorn prettyprinter pyobjtojson dotenv browser-use langchain-openai
   ```

2. Create two separate Python files:
   - `api.py` - The FastAPI server component
   - `client.py` - The Browser-Use agent with recording hook

3. Run both components:
   - Start the API server first: `python api.py`
   - Then run the client: `python client.py`

### Server Component (api.py)

The server component handles receiving and storing the agent's activity data:

```python
#!/usr/bin/env python3

#
# FastAPI API to record and save Browser-Use activity data.
# Save this code to api.py and run with `python api.py`
# 

import json
import base64
from pathlib import Path

from fastapi import FastAPI, Request
import prettyprinter
import uvicorn

prettyprinter.install_extras()

# Utility function to save screenshots
def b64_to_png(b64_string: str, output_file):
    """
    Convert a Base64-encoded string to a PNG file.
    
    :param b64_string: A string containing Base64-encoded data
    :param output_file: The path to the output PNG file
    """
    with open(output_file, "wb") as f:
        f.write(base64.b64decode(b64_string))

# Initialize FastAPI app
app = FastAPI()


@app.post("/post_agent_history_step")
async def post_agent_history_step(request: Request):
    data = await request.json()
    prettyprinter.cpprint(data)

    # Ensure the "recordings" folder exists using pathlib
    recordings_folder = Path("recordings")
    recordings_folder.mkdir(exist_ok=True)

    # Determine the next file number by examining existing .json files
    existing_numbers = []
    for item in recordings_folder.iterdir():
        if item.is_file() and item.suffix == ".json":
            try:
                file_num = int(item.stem)
                existing_numbers.append(file_num)
            except ValueError:
                # In case the file name isn't just a number
                pass

    if existing_numbers:
        next_number = max(existing_numbers) + 1
    else:
        next_number = 1

    # Construct the file path
    file_path = recordings_folder / f"{next_number}.json"

    # Save the JSON data to the file
    with file_path.open("w") as f:
        json.dump(data, f, indent=2)

    # Optionally save screenshot if needed
    # if "website_screenshot" in data and data["website_screenshot"]:
    #     screenshot_folder = Path("screenshots")
    #     screenshot_folder.mkdir(exist_ok=True)
    #     b64_to_png(data["website_screenshot"], screenshot_folder / f"{next_number}.png")

    return {"status": "ok", "message": f"Saved to {file_path}"}

if __name__ == "__main__":
    print("Starting Browser-Use recording API on http://0.0.0.0:9000")
    uvicorn.run(app, host="0.0.0.0", port=9000)
```

### Client Component (client.py)

The client component runs the Browser-Use agent with a recording hook:

```python
#!/usr/bin/env python3

#
# Client to record and save Browser-Use activity.
# Save this code to client.py and run with `python client.py`
#

import asyncio
import requests
from dotenv import load_dotenv
from pyobjtojson import obj_to_json
from langchain_openai import ChatOpenAI
from browser_use import Agent

# Load environment variables (for API keys)
load_dotenv()


def send_agent_history_step(data):
    """Send the agent step data to the recording API"""
    url = "http://127.0.0.1:9000/post_agent_history_step"
    response = requests.post(url, json=data)
    return response.json()


async def record_activity(agent_obj):
    """Hook function that captures and records agent activity at each step"""
    website_html = None
    website_screenshot = None
    urls_json_last_elem = None
    model_thoughts_last_elem = None
    model_outputs_json_last_elem = None
    model_actions_json_last_elem = None
    extracted_content_json_last_elem = None

    print('--- ON_STEP_START HOOK ---')
    
    # Capture current page state
    website_html = await agent_obj.browser_context.get_page_html()
    website_screenshot = await agent_obj.browser_context.take_screenshot()

    # Make sure we have state history
    if hasattr(agent_obj, "state"):
        history = agent_obj.state.history
    else:
        history = None
        print("Warning: Agent has no state history")
        return

    # Process model thoughts
    model_thoughts = obj_to_json(
        obj=history.model_thoughts(),
        check_circular=False
    )
    if len(model_thoughts) > 0:
        model_thoughts_last_elem = model_thoughts[-1]

    # Process model outputs
    model_outputs = agent_obj.state.history.model_outputs()
    model_outputs_json = obj_to_json(
        obj=model_outputs,
        check_circular=False
    )
    if len(model_outputs_json) > 0:
        model_outputs_json_last_elem = model_outputs_json[-1]

    # Process model actions
    model_actions = agent_obj.state.history.model_actions()
    model_actions_json = obj_to_json(
        obj=model_actions,
        check_circular=False
    )
    if len(model_actions_json) > 0:
        model_actions_json_last_elem = model_actions_json[-1]

    # Process extracted content
    extracted_content = agent_obj.state.history.extracted_content()
    extracted_content_json = obj_to_json(
        obj=extracted_content,
        check_circular=False
    )
    if len(extracted_content_json) > 0:
        extracted_content_json_last_elem = extracted_content_json[-1]

    # Process URLs
    urls = agent_obj.state.history.urls()
    urls_json = obj_to_json(
        obj=urls,
        check_circular=False
    )
    if len(urls_json) > 0:
        urls_json_last_elem = urls_json[-1]

    # Create a summary of all data for this step
    model_step_summary = {
        "website_html": website_html,
        "website_screenshot": website_screenshot,
        "url": urls_json_last_elem,
        "model_thoughts": model_thoughts_last_elem,
        "model_outputs": model_outputs_json_last_elem,
        "model_actions": model_actions_json_last_elem,
        "extracted_content": extracted_content_json_last_elem
    }

    print("--- MODEL STEP SUMMARY ---")
    print(f"URL: {urls_json_last_elem}")
    
    # Send data to the API
    result = send_agent_history_step(data=model_step_summary)
    print(f"Recording API response: {result}")


async def run_agent():
    """Run the Browser-Use agent with the recording hook"""
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    
    try:
        print("Starting Browser-Use agent with recording hook")
        await agent.run(
            on_step_start=record_activity,
            max_steps=30
        )
    except Exception as e:
        print(f"Error running agent: {e}")


if __name__ == "__main__":
    # Check if API is running
    try:
        requests.get("http://127.0.0.1:9000")
        print("Recording API is available")
    except:
        print("Warning: Recording API may not be running. Start api.py first.")
    
    # Run the agent
    asyncio.run(run_agent())
```

### Working with the Recorded Data

After running the agent, you'll find the recorded data in the `recordings` directory. Here's how you can use this data:

1. **View recorded sessions**: Each JSON file contains a snapshot of agent activity for one step
2. **Extract screenshots**: You can modify the API to save screenshots separately
3. **Analyze agent behavior**: Use the recorded data to study how the agent navigates websites

### Extending the Example

You can extend this recording system in several ways:

1. **Save screenshots separately**: Uncomment the screenshot saving code in the API
2. **Add a web dashboard**: Create a simple web interface to view recorded sessions
3. **Add session IDs**: Modify the API to group steps by agent session
4. **Add filtering**: Implement filters to record only specific types of actions

## Data Available in Hooks

When working with agent hooks, you have access to the entire agent instance. Here are some useful data points you can access:

- `agent.state.history.model_thoughts()`: Reasoning from Browser Use's model.
- `agent.state.history.model_outputs()`: Raw outputs from the Browsre Use's model.
- `agent.state.history.model_actions()`: Actions taken by the agent
- `agent.state.history.extracted_content()`: Content extracted from web pages
- `agent.state.history.urls()`: URLs visited by the agent
- `agent.browser_context.get_page_html()`: Current page HTML
- `agent.browser_context.take_screenshot()`: Screenshot of the current page

## Tips for Using Hooks

- **Avoid blocking operations**: Since hooks run in the same execution thread as the agent, try to keep them efficient or use asynchronous patterns.
- **Handle exceptions**: Make sure your hook functions handle exceptions gracefully to prevent interrupting the agent's main flow.
- **Consider storage needs**: When capturing full HTML and screenshots, be mindful of storage requirements.

Contribution by Carlos A. Planchón.
````

## File: docs/customize/output-format.mdx
````
---
title: "Output Format"
description: "The default is text. But you can define a structured output format to make post-processing easier."
icon: "code"
---

## Custom output format
With [this example](https://github.com/browser-use/browser-use/blob/main/examples/features/custom_output.py) you can define what output format the agent should return to you.

```python
from pydantic import BaseModel
# Define the output format as a Pydantic model
class Post(BaseModel):
	post_title: str
	post_url: str
	num_comments: int
	hours_since_post: int


class Posts(BaseModel):
	posts: List[Post]


controller = Controller(output_model=Posts)


async def main():
	task = 'Go to hackernews show hn and give me the first  5 posts'
	model = ChatOpenAI(model='gpt-4o')
	agent = Agent(task=task, llm=model, controller=controller)

	history = await agent.run()

	result = history.final_result()
	if result:
		parsed: Posts = Posts.model_validate_json(result)

		for post in parsed.posts:
			print('\n--------------------------------')
			print(f'Title:            {post.post_title}')
			print(f'URL:              {post.post_url}')
			print(f'Comments:         {post.num_comments}')
			print(f'Hours since post: {post.hours_since_post}')
	else:
		print('No result')


if __name__ == '__main__':
	asyncio.run(main())
```
````

## File: docs/customize/real-browser.mdx
````
---
title: "Connect to your Browser"
description: "With this you can connect to your real browser, where you are logged in with all your accounts."
icon: "computer"
---

## Overview

You can connect the agent to your real Chrome browser instance, allowing it to access your existing browser profile with all your logged-in accounts and settings. This is particularly useful when you want the agent to interact with services where you're already authenticated.

<Note>
  First make sure to close all running Chrome instances.
</Note>

## Basic Configuration

To connect to your real Chrome browser, you'll need to specify the path to your Chrome executable when creating the Browser instance:

```python
from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
import asyncio
# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        # Specify the path to your Chrome executable
        browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS path
        # For Windows, typically: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        # For Linux, typically: '/usr/bin/google-chrome'
    )
)

# Create the agent with your configured browser
agent = Agent(
    task="Your task here",
    llm=ChatOpenAI(model='gpt-4o'),
    browser=browser,
)

async def main():
    await agent.run()

    input('Press Enter to close the browser...')
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
```


<Note>
  When using your real browser, the agent will have access to all your logged-in sessions. Make sure to ALWAYS review the task you're giving to the agent and ensure it aligns with your security requirements!
</Note>
````

## File: docs/customize/sensitive-data.mdx
````
---
title: "Sensitive Data"
description: "Handle sensitive information securely by preventing the model from seeing actual passwords."
icon: "shield"
---

## Handling Sensitive Data

When working with sensitive information like passwords, you can use the `sensitive_data` parameter to prevent the model from seeing the actual values while still allowing it to reference them in its actions.

Here's an example of how to use sensitive data:

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from browser_use import Agent

load_dotenv()

# Initialize the model
llm = ChatOpenAI(
    model='gpt-4o',
    temperature=0.0,
)

# Define sensitive data
# The model will only see the keys (x_name, x_password) but never the actual values
sensitive_data = {'x_name': 'magnus', 'x_password': '12345678'}

# Use the placeholder names in your task description
task = 'go to x.com and login with x_name and x_password then write a post about the meaning of life'

# Pass the sensitive data to the agent
agent = Agent(task=task, llm=llm, sensitive_data=sensitive_data)

async def main():
    await agent.run()

if __name__ == '__main__':
    asyncio.run(main())
```

In this example:
1. The model only sees `x_name` and `x_password` as placeholders.
2. When the model wants to use your password it outputs x_password - and we replace it with the actual value.
3. When your password is visible on the current page, we replace it in the LLM input - so that the model never has it in its state.

Warning: Vision models still see the image of the page - where the sensitive data might be visible.

This approach ensures that sensitive information remains secure while still allowing the agent to perform tasks that require authentication.
````

## File: docs/customize/supported-models.mdx
````
---
title: "Supported Models"
description: "Guide to using different LangChain chat models with Browser Use"
icon: "robot"
---

## Overview

Browser Use supports various LangChain chat models. Here's how to configure and use the most popular ones. The full list is available in the [LangChain documentation](https://python.langchain.com/docs/integrations/chat/).

## Model Recommendations

We have yet to test performance across all models. Currently, we achieve the best results using GPT-4o with an 89% accuracy on the [WebVoyager Dataset](https://browser-use.com/posts/sota-technical-report). DeepSeek-V3 is 30 times cheaper than GPT-4o. Gemini-2.0-exp is also gaining popularity in the community because it is currently free.
We also support local models, like Qwen 2.5, but be aware that small models often return the wrong output structure-which lead to parsing errors. We believe that local models will improve significantly this year.


<Note>
  All models require their respective API keys. Make sure to set them in your
  environment variables before running the agent.
</Note>

## Supported Models

All LangChain chat models, which support tool-calling are available. We will document the most popular ones here.

### OpenAI

OpenAI's GPT-4o models are recommended for best performance.

```python
from langchain_openai import ChatOpenAI
from browser_use import Agent

# Initialize the model
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0,
)

# Create agent with the model
agent = Agent(
    task="Your task here",
    llm=llm
)
```

Required environment variables:

```bash .env
OPENAI_API_KEY=
```

### Anthropic


```python
from langchain_anthropic import ChatAnthropic
from browser_use import Agent

# Initialize the model
llm = ChatAnthropic(
    model_name="claude-3-5-sonnet-20240620",
    temperature=0.0,
    timeout=100, # Increase for complex tasks
)

# Create agent with the model
agent = Agent(
    task="Your task here",
    llm=llm
)
```

And add the variable:

```bash .env
ANTHROPIC_API_KEY=
```

### Azure OpenAI

```python
from langchain_openai import AzureChatOpenAI
from browser_use import Agent
from pydantic import SecretStr
import os

# Initialize the model
llm = AzureChatOpenAI(
    model="gpt-4o",
    api_version='2024-10-21',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
    api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', '')),
)

# Create agent with the model
agent = Agent(
    task="Your task here",
    llm=llm
)
```

Required environment variables:

```bash .env
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_KEY=
```


### Gemini

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from dotenv import load_dotenv

# Read GEMINI_API_KEY into env
load_dotenv()

# Initialize the model
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp')

# Create agent with the model
agent = Agent(
    task="Your task here",
    llm=llm
)
```

Required environment variables:

```bash .env
GEMINI_API_KEY=
```


### DeepSeek-V3
The community likes DeepSeek-V3 for its low price, no rate limits, open-source nature, and good performance.
The example is available [here](https://github.com/browser-use/browser-use/blob/main/examples/models/deepseek.py).

```python
from langchain_openai import ChatOpenAI
from browser_use import Agent
from pydantic import SecretStr
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

# Initialize the model
llm=ChatOpenAI(base_url='https://api.deepseek.com/v1', model='deepseek-chat', api_key=SecretStr(api_key))

# Create agent with the model
agent = Agent(
    task="Your task here",
    llm=llm,
    use_vision=False
)
```

Required environment variables:

```bash .env
DEEPSEEK_API_KEY=
```

### DeepSeek-R1
We support DeepSeek-R1. Its not fully tested yet, more and more functionality will be added, like e.g. the output of it'sreasoning content.
The example is available [here](https://github.com/browser-use/browser-use/blob/main/examples/models/deepseek-r1.py).
It does not support vision. The model is open-source so you could also use it with Ollama, but we have not tested it.
```python
from langchain_openai import ChatOpenAI
from browser_use import Agent
from pydantic import SecretStr
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

# Initialize the model
llm=ChatOpenAI(base_url='https://api.deepseek.com/v1', model='deepseek-reasoner', api_key=SecretStr(api_key))

# Create agent with the model
agent = Agent(
    task="Your task here",
    llm=llm,
    use_vision=False
)
```

Required environment variables:

```bash .env
DEEPSEEK_API_KEY=
```

### Ollama
Many users asked for local models. Here they are.

1. Download Ollama from [here](https://ollama.ai/download)
2. Run `ollama pull model_name`. Pick a model which supports tool-calling from [here](https://ollama.com/search?c=tools)
3. Run `ollama start`

```python
from langchain_ollama import ChatOllama
from browser_use import Agent
from pydantic import SecretStr


# Initialize the model
llm=ChatOllama(model="qwen2.5", num_ctx=32000)

# Create agent with the model
agent = Agent(
    task="Your task here",
    llm=llm
)
```

Required environment variables: None!

### Novita AI
[Novita AI](https://novita.ai) is an LLM API provider that offers a wide range of models. Note: choose a model that supports function calling.

```python
from langchain_openai import ChatOpenAI
from browser_use import Agent
from pydantic import SecretStr
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("NOVITA_API_KEY")

# Initialize the model
llm = ChatOpenAI(base_url='https://api.novita.ai/v3/openai', model='deepseek/deepseek-v3-0324', api_key=SecretStr(api_key))

# Create agent with the model
agent = Agent(
    task="Your task here",
    llm=llm,
    use_vision=False
)
```

Required environment variables:

```bash .env
NOVITA_API_KEY=
```
### X AI
[X AI](https://x.ai) is an LLM API provider that offers a wide range of models. Note: choose a model that supports function calling.

```python
from langchain_openai import ChatOpenAI
from browser_use import Agent
from pydantic import SecretStr
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GROK_API_KEY")

# Initialize the model
llm = ChatOpenAI(
    base_url='https://api.x.ai/v1',
    model='grok-3-beta',
    api_key=SecretStr(api_key)
)

# Create agent with the model
agent = Agent(
    task="Your task here",
    llm=llm,
    use_vision=False
)
```

Required environment variables:

```bash .env
GROK_API_KEY=
```

## Coming soon
(We are working on it)
- Groq
- Github
- Fine-tuned models
````

## File: docs/customize/system-prompt.mdx
````
---
title: "System Prompt"
description: "Customize the system prompt to control agent behavior and capabilities"
icon: "message"
---

## Overview

You can customize the system prompt in two ways:

1. Extend the default system prompt with additional instructions
2. Override the default system prompt entirely

<Note>
  Custom system prompts allow you to modify the agent's behavior at a
  fundamental level. Use this feature carefully as it can significantly impact
  the agent's performance and reliability.
</Note>

### Extend System Prompt (recommended)

To add additional instructions to the default system prompt:

```python
extend_system_message = """
REMEMBER the most important RULE:
ALWAYS open first a new tab and go first to url wikipedia.com no matter the task!!!
"""
```

### Override System Prompt

<Warning>
  Not recommended! If you must override the [default system
  prompt](https://github.com/browser-use/browser-use/blob/main/browser_use/agent/system_prompt.md),
  make sure to test the agent yourself.
</Warning>

Anyway, to override the default system prompt:

```python
# Define your complete custom prompt
override_system_message = """
You are an AI agent that helps users with web browsing tasks.

[Your complete custom instructions here...]
"""

# Create agent with custom system prompt
agent = Agent(
    task="Your task here",
    llm=ChatOpenAI(model='gpt-4'),
    override_system_message=override_system_message
)
```

### Extend Planner System Prompt

You can customize the behavior of the planning agent by extending its system prompt:

```python
extend_planner_system_message = """
PRIORITIZE gathering information before taking any action.
Always suggest exploring multiple options before making a decision.
"""

# Create agent with extended planner system prompt
llm = ChatOpenAI(model='gpt-4o')
planner_llm = ChatOpenAI(model='gpt-4o-mini')

agent = Agent(
	task="Your task here",
	llm=llm,
	planner_llm=planner_llm,
	extend_planner_system_message=extend_planner_system_message
)
```
````

## File: docs/development.mdx
````
---
title: 'Development'
description: 'Preview changes locally to update your docs'
---

<Info>
  **Prerequisite**: Please install Node.js (version 19 or higher) before proceeding.
</Info>

Follow these steps to install and run Mintlify on your operating system:

**Step 1**: Install Mintlify:

<CodeGroup>

  ```bash npm
  npm i -g mintlify
  ```

```bash yarn
yarn global add mintlify
```

</CodeGroup>

**Step 2**: Navigate to the docs directory (where the `mint.json` file is located) and execute the following command:

```bash
mintlify dev
```

A local preview of your documentation will be available at `http://localhost:3000`.

### Custom Ports

By default, Mintlify uses port 3000. You can customize the port Mintlify runs on by using the `--port` flag. To run Mintlify on port 3333, for instance, use this command:

```bash
mintlify dev --port 3333
```

If you attempt to run Mintlify on a port that's already in use, it will use the next available port:

```md
Port 3000 is already in use. Trying 3001 instead.
```

## Mintlify Versions

Please note that each CLI release is associated with a specific version of Mintlify. If your local website doesn't align with the production version, please update the CLI:

<CodeGroup>

```bash npm
npm i -g mintlify@latest
```

```bash yarn
yarn global upgrade mintlify
```

</CodeGroup>

## Validating Links

The CLI can assist with validating reference links made in your documentation. To identify any broken links, use the following command:

```bash
mintlify broken-links
```

## Deployment

<Tip>
  Unlimited editors available under the [Pro
  Plan](https://mintlify.com/pricing) and above.
</Tip>

If the deployment is successful, you should see the following:

<Frame>
  <img src="/images/checks-passed.png" style={{ borderRadius: '0.5rem' }} />
</Frame>

## Code Formatting

We suggest using extensions on your IDE to recognize and format MDX. If you're a VSCode user, consider the [MDX VSCode extension](https://marketplace.visualstudio.com/items?itemName=unifiedjs.vscode-mdx) for syntax highlighting, and [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) for code formatting.

## Troubleshooting

<AccordionGroup>
  <Accordion title='Error: Could not load the "sharp" module using the darwin-arm64 runtime'>

    This may be due to an outdated version of node. Try the following:
    1. Remove the currently-installed version of mintlify: `npm remove -g mintlify`
    2. Upgrade to Node v19 or higher.
    3. Reinstall mintlify: `npm install -g mintlify`
  </Accordion>

  <Accordion title="Issue: Encountering an unknown error">

    Solution: Go to the root of your device and delete the \~/.mintlify folder. Afterwards, run `mintlify dev` again.
  </Accordion>
</AccordionGroup>

Curious about what changed in the CLI version? [Check out the CLI changelog.](https://www.npmjs.com/package/mintlify?activeTab=versions)

# Development Workflow

## Branches
- **`stable`**: Mirrors the latest stable release. This branch is updated only when a new stable release is published (every few weeks).
- **`main`**: The primary development branch. This branch is updated frequently (every hour or more).

## Tags
- **`x.x.x`**: Stable release tags. These are created for stable releases and updated every few weeks.
- **`x.x.xrcXX`**: Pre-release tags. These are created for unstable pre-releases and updated every Friday at 5 PM UTC.

## Workflow Summary
1. **Push to `main`**:
   - Runs pre-commit hooks to fix formatting.
   - Executes tests to ensure code quality.

2. **Release a new version**:
   - If the tag is a pre-release (`x.x.xrcXX`), the package is pushed to PyPI as a pre-release.
   - If the tag is a stable release (`x.x.x`), the package is pushed to PyPI as a stable release, and the `stable` branch is updated to match the release.

3. **Scheduled Pre-Releases**:
   - Every Friday at 5 PM UTC, a new pre-release tag (`x.x.xrcXX`) is created from the `main` branch and pushed to the repository.
````

## File: docs/development/evaluations.mdx
````
---
title: "Evaluations"
description: "Test the Browser Use agent on standardized benchmarks"
icon: "chart-bar"
---

## Prerequisites

Browser Use uses proprietary/private test sets that must never be committed to Github and must be fetched through a authorized api request.
Accessing these test sets requires an approved Browser Use account.
There are currently no publicly available test sets, but some may be released in the future.

## Get an Api Access Key

First, navigate to https://browser-use.tools and log in with an authorized browser use account.

Then, click the "Account" button at the top right of the page, and click the "Cycle New Key" button on that page.

Copy the resulting url and secret key into your `.env` file. It should look like this:

```bash .env
EVALUATION_TOOL_URL= ...
EVALUATION_TOOL_SECRET_KEY= ...
```

## Running Evaluations

First, ensure your file `eval/service.py` is up to date.

Then run the file:

```bash
python eval/service.py
```

## Configuring Evaluations

You can modify the evaluation by providing flags to the evaluation script. For instance:

```bash
python eval/service.py --parallel_runs 5 --parallel_evaluations 5 --max-steps 25 --start 0 --end 100 --model gpt-4o
```

The evaluations webpage has a convenient GUI for generating these commands. To use it, navigate to https://browser-use.tools/dashboard.

Then click the button "New Eval Run" on the left panel. This will open a interface with selectors, inputs, sliders, and switches.

Input your desired configuration into the interface and copy the resulting python command at the bottom. Then run this command as before.
````

## File: docs/development/local-setup.mdx
````
---
title: "Local Setup"
description: "Set up Browser Use development environment locally"
icon: "laptop-code"
---

## Prerequisites

Browser Use requires Python 3.11 or higher. We recommend using [uv](https://docs.astral.sh/uv/) for Python environment management.

## Clone the Repository

First, clone the Browser Use repository:

```bash
git clone https://github.com/browser-use/browser-use
cd browser-use
```

## Environment Setup

1. Create and activate a virtual environment:

```bash
uv venv --python 3.11
source .venv/bin/activate
```

2. Install dependencies:

```bash
# Install the package in editable mode with all development dependencies
uv sync
```

## Configuration

Set up your environment variables:

```bash
# Copy the example environment file
cp .env.example .env
```

Or manually create a `.env` file with the API key for the models you want to use set:

```bash .env
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=
AZURE_ENDPOINT=
AZURE_OPENAI_API_KEY=
GEMINI_API_KEY=
DEEPSEEK_API_KEY=
GROK_API_KEY=
NOVITA_API_KEY=
```

<Note>
  You can use any LLM model supported by LangChain. See 
  [LangChain Models](/customize/supported-models) for available options and their specific
  API key requirements.
</Note>

## Development

After setup, you can:

- Try demos in the example library with `uv run examples/simple.py`
- Run the linter/formatter with `uv run ruff format examples/some/file.py`
- Run tests with `uv run pytest`
- Build the package with `uv build`

## Getting Help

If you run into any issues:

1. Check our [GitHub Issues](https://github.com/browser-use/browser-use/issues)
2. Join our [Discord community](https://link.browser-use.com/discord) for support

<Note>
  We welcome contributions! See our [Contribution Guide](/development/contribution-guide) for guidelines on how to help improve
  Browser Use.
</Note>
````

## File: docs/development/n8n-integration.mdx
````
---
title: 'n8n Integration'
description: 'Learn how to integrate Browser Use with n8n workflows'
---

# Browser Use n8n Integration

Browser Use can be integrated with [n8n](https://n8n.io), a workflow automation platform, using our community node. This integration allows you to trigger browser automation tasks directly from your n8n workflows.

## Installing the n8n Community Node

There are several ways to install the Browser Use community node in n8n:

### Using n8n Desktop or Cloud

1. Navigate to **Settings > Community Nodes**
2. Click on **Install**
3. Enter `n8n-nodes-browser-use` in the **Name** field
4. Click **Install**

### Using a Self-hosted n8n Instance

Run the following command in your n8n installation directory:

```bash
npm install n8n-nodes-browser-use
```

### For Development

If you want to develop with the n8n node:

1. Clone the repository:
   ```bash
   git clone https://github.com/draphonix/n8n-nodes-browser-use.git
   ```
2. Install dependencies:
   ```bash
   cd n8n-nodes-browser-use
   npm install
   ```
3. Build the code:
   ```bash
   npm run build
   ```
4. Link to your n8n installation:
   ```bash
   npm link
   ```
5. In your n8n installation directory:
   ```bash
   npm link n8n-nodes-browser-use
   ```

## Setting Up Browser Use Cloud API Credentials

To use the Browser Use node in n8n, you need to configure API credentials:

1. Sign up for an account at [Browser Use Cloud](https://cloud.browser-use.com)
2. Navigate to the Settings or API section
3. Generate or copy your API key
4. In n8n, create a new credential:
   - Go to **Credentials** tab
   - Click **Create New**
   - Select **Browser Use Cloud API**
   - Enter your API key
   - Save the credential

## Using the Browser Use Node

Once installed, you can add the Browser Use node to your workflows:

1. In your workflow editor, search for "Browser Use" in the nodes panel
2. Add the node to your workflow
3. Set-up the credentials
4. Choose your saved credentials
5. Select an operation:
   - **Run Task**: Execute a browser automation task with natural language instructions
   - **Get Task**: Retrieve task details
   - **Get Task Status**: Check task execution status
   - **Pause/Resume/Stop Task**: Control running tasks
   - **Get Task Media**: Retrieve screenshots, videos, or PDFs
   - **List Tasks**: Get a list of tasks

### Example: Running a Browser Task

Here's a simple example of how to use the Browser Use node to run a browser task:

1. Add the Browser Use node to your workflow
2. Select the "Run Task" operation
3. In the "Instructions" field, enter a natural language description of what you want the browser to do, for example:
   ```
   Go to example.com, take a screenshot of the homepage, and extract all the main heading texts
   ```
4. Optionally enable "Save Browser Data" to preserve cookies and session information
5. Connect the node to subsequent nodes to process the results

## Workflow Examples

The Browser Use n8n node enables various automation scenarios:

- **Web Scraping**: Extract data from websites on a schedule
- **Form Filling**: Automate data entry across web applications
- **Monitoring**: Check website status and capture visual evidence
- **Report Generation**: Generate PDFs or screenshots of web dashboards
- **Multi-step Processes**: Chain browser tasks together using session persistence

## Troubleshooting

If you encounter issues with the Browser Use node:

- Verify your API key is valid and has sufficient credits
- Check that your instructions are clear and specific
- For complex tasks, consider breaking them into multiple steps
- Refer to the [Browser Use documentation](https://docs.browser-use.com) for instruction best practices

## Resources

- [n8n Community Nodes Documentation](https://docs.n8n.io/integrations/community-nodes/)
- [Browser Use Documentation](https://docs.browser-use.com)
- [Browser Use Cloud](https://cloud.browser-use.com)
- [n8n-nodes-browser-use GitHub Repository](https://github.com/draphonix/n8n-nodes-browser-use)
````

## File: docs/development/observability.mdx
````
---
title: "Observability"
description: "Trace Browser Use's agent execution steps and browser sessions"
icon: "eye"
---

## Overview

Browser Use has a native integration with [Laminar](https://lmnr.ai) - open-source platform for tracing, evals and labeling of AI agents.
Read more about Laminar in the [Laminar docs](https://docs.lmnr.ai).

<Note>
  Laminar excels at tracing browser agents by providing unified visibility into both browser session recordings and agent execution steps.
</Note>

## Setup

To setup Laminar, you need to install the `lmnr` package and set the `LMNR_PROJECT_API_KEY` environment variable.

To get your project API key, you can either:
- Register on [Laminar Cloud](https://lmnr.ai) and get the key from your project settings
- Or spin up a local Laminar instance and get the key from the settings page

```bash
pip install 'lmnr[all]'
export LMNR_PROJECT_API_KEY=<your-project-api-key>
```

## Usage

Then, you simply initialize the Laminar at the top of your project and both Browser Use and session recordings will be automatically traced.

```python {5-8}
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio

from lmnr import Laminar
# this line auto-instruments Browser Use and any browser you use (local or remote)
Laminar.initialize(project_api_key="...") # you can also pass project api key here

async def main():
    agent = Agent(
        task="open google, search Laminar AI",
        llm=ChatOpenAI(model="gpt-4o-mini"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

## Viewing Traces

You can view traces in the Laminar UI by going to the traces tab in your project.
When you select a trace, you can see both the browser session recording and the agent execution steps.

Timeline of the browser session is synced with the agent execution steps, timeline highlights indicate the agent's current step synced with the browser session.
In the trace view, you can also see the agent's current step, the tool it's using, and the tool's input and output. Tools are highlighted in the timeline with a yellow color.

<img className="block" src="/images/laminar.png" alt="Laminar" />


## Laminar

To learn more about tracing and evaluating your browser agents, check out the [Laminar docs](https://docs.lmnr.ai).
````

## File: docs/development/roadmap.mdx
````
---
title: "Roadmap"
description: "Future plans and upcoming features for Browser Use"
icon: "road"
---

Big things coming soon!
````

## File: docs/development/telemetry.mdx
````
---
title: "Telemetry"
description: "Understanding Browser Use's telemetry and privacy settings"
icon: "chart-mixed"
---

## Overview

Browser Use collects anonymous usage data to help us understand how the library is being used and to improve the user experience. It also helps us fix bugs faster and prioritize feature development.

## Data Collection

We use [PostHog](https://posthog.com) for telemetry collection. The data is completely anonymized and contains no personally identifiable information.

<Note>
  We never collect personal information, credentials, or specific content from
  your browser automation tasks.
</Note>

## Opting Out

You can disable telemetry by setting an environment variable:

```bash .env
ANONYMIZED_TELEMETRY=false
```

Or in your Python code:

```python
import os
os.environ["ANONYMIZED_TELEMETRY"] = "false"
```

<Note>
  Even when enabled, telemetry has zero impact on the library's performance or
  functionality. Code is available in [Telemetry
  Service](https://github.com/browser-use/browser-use/tree/main/browser_use/telemetry).
</Note>
````

## File: docs/favicon.svg
````
<svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<g clip-path="url(#clip0_7_13)">
<path d="M97.8916 39.0448C82.6177 33.1997 95.2199 10.8169 74.212 11.3849C48.5413 12.0793 8.31528 52.4518 12.4236 78.6851C14.4652 91.6755 24.6096 86.2218 29.3732 88.1154C32.5364 89.3652 36.2792 95.0083 40.3245 95.9047C22.4293 106.193 -0.556809 96.397 0.0102912 74.3423C0.829435 41.86 47.7474 -5.25386 81.1937 0.477571C99.8702 3.68414 102.189 23.5422 97.8916 39.0448Z" fill="white"/>
<path d="M24.8115 57.7541L39.6068 71.7166C49.0332 80.1875 74.061 94.9706 85.403 84.9469C98.774 73.1306 70.495 32.3162 57.4769 25.802L68.9069 20.6639C86.7138 33.6796 113.783 75.9836 91.7294 94.4025C77.5014 106.282 54.5655 96.2204 41.0811 87.3707C30.8103 80.6294 15.9647 70.9591 24.8115 57.7415V57.7541Z" fill="white"/>
<path d="M40.3373 4.75723C35.5485 4.88347 31.8055 11.1199 28.2895 12.2182C25.1642 13.1903 20.8414 10.5266 16.1408 14.0487C11.0495 17.8613 12.7891 36.0655 3.02233 40.5976C-2.98893 22.9362 0.75354 1.8789 22.4672 0.0736228C24.1433 -0.0652445 42.7822 1.17195 40.3373 4.74463V4.75723Z" fill="white"/>
<path d="M76.1025 57.754C84.1175 71.0348 69.5871 86.2092 57.489 74.1025L76.1025 57.754Z" fill="white"/>
</g>
<defs>
<clipPath id="clip0_7_13">
<rect width="100" height="100" fill="white"/>
</clipPath>
</defs>
</svg>
````

## File: docs/introduction.mdx
````
---
title: "Introduction"
description: "Welcome to Browser Use - We enable AI to control your browser"
icon: "book-open"
---

<img className="block" src="/images/browser-use.png" alt="Browser Use" />

## Overview

Browser Use is the easiest way to connect your AI agents with the browser. It makes websites accessible for AI agents by providing a powerful, yet simple interface for browser automation.

<Note>
  If you have used Browser Use for your project, feel free to show it off in our
  [Discord community](https://link.browser-use.com/discord)!
</Note>

## Getting Started

<CardGroup cols={2}>
  <Card title="Quick Start" icon="rocket" href="/quickstart">
    Get up and running with Browser Use in minutes
  </Card>
  <Card
    title="Supported Models"
    icon="robot"
    href="/customize/supported-models"
  >
    Configure different LLMs for your agents
  </Card>
  <Card title="Agent Settings" icon="gear" href="/customize/agent-settings">
    Learn how to configure and customize your agents
  </Card>
  <Card title="Custom Functions" icon="code" href="/customize/custom-functions">
    Extend functionality with custom actions
  </Card>
</CardGroup>

## Fancy Demos

### Writing in Google Docs

Task: Write a letter in Google Docs to my Papa, thanking him for everything, and save the document as a PDF.

<Frame>
  <img src="https://github.com/user-attachments/assets/242ade3e-15bc-41c2-988f-cbc5415a66aa" />
</Frame>

### Job Applications

Task: Read my CV & find ML jobs, save them to a file, and then start applying for them in new tabs.

<Frame>
  <video
    controls
    src="https://github.com/user-attachments/assets/171fb4d6-0355-46f2-863e-edb04a828d04"
  />
</Frame>

### Flight Search

Task: Find flights on kayak.com from Zurich to Beijing.

<Frame>
  <img src="https://github.com/user-attachments/assets/ea605d4a-90e6-481e-a569-f0e0db7e6390" />
</Frame>

### Data Collection

Task: Look up models with a license of cc-by-sa-4.0 and sort by most likes on Hugging Face, save top 5 to file.

<Frame>
  <video
    controls
    src="https://github.com/user-attachments/assets/de73ee39-432c-4b97-b4e8-939fd7f323b3"
  />
</Frame>

## Community & Support

<CardGroup cols={2}>
  <Card
    title="Join Discord"
    icon="discord"
    href="https://link.browser-use.com/discord"
  >
    Join our community for support and showcases
  </Card>
  <Card
    title="GitHub"
    icon="github"
    href="https://github.com/browser-use/browser-use"
  >
    Star us on GitHub and contribute to development
  </Card>
</CardGroup>

<Note>
  Browser Use is MIT licensed and actively maintained. We welcome contributions
  and feedback from the community!
</Note>
````

## File: docs/logo/dark.svg
````
<svg width="1867" height="292" viewBox="0 0 1867 292" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M266.265 106.202C224.72 90.3033 258.998 29.4218 201.857 30.9671C132.032 32.8557 22.6176 142.669 33.7922 214.023C39.3453 249.357 66.9381 234.523 79.8952 239.674C88.499 243.073 98.6794 258.423 109.683 260.861C61.0078 288.846 -1.51452 262.2 0.0279922 202.211C2.25607 113.859 129.873 -14.2905 220.847 1.29899C271.647 10.0209 277.954 64.0347 266.265 106.202Z" fill="white"/>
<path d="M67.4872 157.091L107.73 195.069C133.37 218.11 201.446 258.32 232.296 231.056C268.665 198.915 191.746 87.9001 156.337 70.1817L187.427 56.2061C235.862 91.6086 309.49 206.676 249.504 256.775C210.804 289.087 148.418 261.72 111.741 237.649C83.8041 219.312 43.4241 193.009 67.4872 157.057V157.091Z" fill="white"/>
<path d="M109.717 12.9395C96.6917 13.2829 86.511 30.246 76.9474 33.2334C68.4465 35.8774 56.6886 28.6321 43.9029 38.2125C30.0546 48.5826 34.7861 98.0981 8.22063 110.426C-8.12999 62.3865 2.04951 5.11049 61.1106 0.200137C65.6695 -0.177582 116.367 3.1876 109.717 12.9053V12.9395Z" fill="white"/>
<path d="M206.999 157.091C228.8 193.214 189.277 234.489 156.37 201.559L206.999 157.091Z" fill="white"/>
<path d="M504.359 178.759C504.359 195.08 498.53 206.701 486.872 213.621C475.289 220.54 460.397 224 442.195 224H393.795V67.9692H439.374C456.523 67.9692 470.513 71.053 481.344 77.2205C492.174 83.388 497.59 93.5419 497.59 107.682C497.59 116.708 494.882 124.079 489.467 129.795C484.051 135.511 477.169 139.385 468.821 141.415C478.899 142.995 487.323 146.718 494.092 152.585C500.937 158.451 504.359 167.176 504.359 178.759ZM466.338 110.39C466.338 103.47 464.157 98.4308 459.795 95.2718C455.508 92.1128 449.002 90.5333 440.277 90.5333H424.708V131.713H441.631C450.13 131.713 456.373 130.021 460.359 126.636C464.345 123.251 466.338 117.836 466.338 110.39ZM472.318 177.969C472.318 169.019 469.836 162.701 464.872 159.015C459.908 155.33 452.913 153.487 443.887 153.487H424.708V200.872H442.533C451.409 200.872 458.591 199.255 464.082 196.021C469.573 192.711 472.318 186.694 472.318 177.969ZM619.064 101.251C622.675 101.251 625.946 101.552 628.88 102.154C631.888 102.68 634.859 103.47 637.793 104.523L632.49 151.118H612.634V127.764C605.037 128.366 598.381 131.788 592.664 138.031C587.023 144.274 582.548 152.735 579.239 163.415V203.354H603.044V224H532.644V203.354H549.454V125.056H532.644V104.523H572.131L577.659 131.938C582.097 121.634 587.625 113.962 594.244 108.923C600.938 103.809 609.211 101.251 619.064 101.251ZM716.508 101.138C728.242 101.138 738.283 103.733 746.631 108.923C754.98 114.038 761.298 121.333 765.585 130.81C769.948 140.212 772.129 151.268 772.129 163.979C772.129 176.916 769.948 188.161 765.585 197.713C761.223 207.19 754.83 214.523 746.406 219.713C738.057 224.827 728.054 227.385 716.395 227.385C704.662 227.385 694.621 224.865 686.272 219.826C677.924 214.786 671.568 207.528 667.206 198.051C662.843 188.574 660.662 177.292 660.662 164.205C660.662 151.72 662.843 140.738 667.206 131.262C671.643 121.709 678.036 114.301 686.385 109.036C694.809 103.771 704.85 101.138 716.508 101.138ZM716.508 123.59C708.084 123.59 701.842 126.899 697.78 133.518C693.719 140.062 691.688 150.291 691.688 164.205C691.688 178.27 693.719 188.574 697.78 195.118C701.842 201.662 708.047 204.933 716.395 204.933C724.744 204.933 730.949 201.662 735.011 195.118C739.072 188.499 741.103 178.12 741.103 163.979C741.103 150.215 739.072 140.062 735.011 133.518C730.949 126.899 724.782 123.59 716.508 123.59ZM917.521 104.523L899.244 224H864.27L852.198 141.077L839.337 224H805.039L785.973 104.523H813.952L824.332 205.497L839.111 119.641H866.526L880.065 205.497L890.67 104.523H917.521ZM983.037 205.385C990.182 205.385 995.823 204.181 999.96 201.774C1004.17 199.292 1006.28 195.832 1006.28 191.395C1006.28 188.311 1005.56 185.791 1004.13 183.836C1002.71 181.88 999.96 180.038 995.899 178.308C991.912 176.503 985.858 174.509 977.734 172.328C969.461 170.222 962.541 167.74 956.975 164.882C951.41 161.949 947.085 158.188 944.001 153.6C940.917 148.937 939.375 143.221 939.375 136.451C939.375 129.532 941.331 123.402 945.242 118.062C949.228 112.721 954.945 108.585 962.391 105.651C969.912 102.643 978.787 101.138 989.017 101.138C1007.22 101.138 1022.75 105.802 1035.61 115.128L1023.43 133.292C1012.52 126.373 1001.28 122.913 989.693 122.913C976.305 122.913 969.611 126.749 969.611 134.421C969.611 137.053 970.401 139.234 971.981 140.964C973.635 142.694 976.456 144.349 980.442 145.928C984.504 147.508 990.709 149.463 999.058 151.795C1007.63 154.202 1014.63 156.834 1020.04 159.692C1025.53 162.55 1029.78 166.349 1032.79 171.087C1035.87 175.826 1037.42 181.88 1037.42 189.251C1037.42 197.525 1034.93 204.557 1029.97 210.349C1025.08 216.065 1018.54 220.352 1010.34 223.21C1002.14 225.993 993.078 227.385 983.15 227.385C972.319 227.385 962.654 225.843 954.155 222.759C945.656 219.675 938.322 215.426 932.155 210.01L947.611 192.636C952.5 196.547 957.953 199.668 963.97 202C969.987 204.256 976.343 205.385 983.037 205.385ZM1098.31 173.344C1099.13 184.099 1102.29 192.072 1107.78 197.262C1113.35 202.451 1120.46 205.046 1129.11 205.046C1134.6 205.046 1139.86 204.181 1144.9 202.451C1149.94 200.721 1155.02 198.164 1160.13 194.779L1172.54 211.815C1166.75 216.704 1159.98 220.54 1152.23 223.323C1144.49 226.031 1136.14 227.385 1127.19 227.385C1114.48 227.385 1103.65 224.752 1094.7 219.487C1085.82 214.222 1079.09 206.851 1074.5 197.374C1069.99 187.897 1067.73 176.916 1067.73 164.431C1067.73 152.472 1069.95 141.716 1074.39 132.164C1078.9 122.537 1085.37 114.978 1093.79 109.487C1102.29 103.921 1112.3 101.138 1123.8 101.138C1134.63 101.138 1144.07 103.545 1152.12 108.359C1160.17 113.173 1166.37 120.13 1170.74 129.231C1175.1 138.256 1177.28 149.012 1177.28 161.497C1177.28 165.785 1177.09 169.733 1176.72 173.344H1098.31ZM1123.92 122.123C1116.47 122.123 1110.45 124.793 1105.87 130.133C1101.35 135.398 1098.72 143.446 1097.97 154.277H1148.29C1148.14 143.973 1145.99 136.038 1141.86 130.472C1137.79 124.906 1131.81 122.123 1123.92 122.123ZM1295.82 101.251C1299.43 101.251 1302.7 101.552 1305.64 102.154C1308.65 102.68 1311.62 103.47 1314.55 104.523L1309.25 151.118H1289.39V127.764C1281.79 128.366 1275.14 131.788 1269.42 138.031C1263.78 144.274 1259.31 152.735 1256 163.415V203.354H1279.8V224H1209.4V203.354H1226.21V125.056H1209.4V104.523H1248.89L1254.42 131.938C1258.85 121.634 1264.38 113.962 1271 108.923C1277.7 103.809 1285.97 101.251 1295.82 101.251ZM1584.35 172.328C1584.35 183.084 1582.17 192.636 1577.81 200.985C1573.52 209.258 1567.16 215.726 1558.74 220.39C1550.32 225.053 1540.2 227.385 1528.39 227.385C1516.43 227.385 1506.28 225.091 1497.93 220.503C1489.58 215.915 1483.26 209.484 1478.98 201.21C1474.76 192.937 1472.66 183.309 1472.66 172.328V67.9692H1503.57V163.641C1503.57 172.817 1504.36 180.301 1505.94 186.092C1507.52 191.884 1510.12 196.246 1513.73 199.179C1517.34 202.113 1522.22 203.579 1528.39 203.579C1534.56 203.579 1539.45 202.113 1543.06 199.179C1546.74 196.246 1549.38 191.884 1550.96 186.092C1552.54 180.301 1553.33 172.817 1553.33 163.641V67.9692H1584.35V172.328ZM1659.79 205.385C1666.94 205.385 1672.58 204.181 1676.72 201.774C1680.93 199.292 1683.04 195.832 1683.04 191.395C1683.04 188.311 1682.32 185.791 1680.89 183.836C1679.46 181.88 1676.72 180.038 1672.66 178.308C1668.67 176.503 1662.62 174.509 1654.49 172.328C1646.22 170.222 1639.3 167.74 1633.73 164.882C1628.17 161.949 1623.84 158.188 1620.76 153.6C1617.68 148.937 1616.13 143.221 1616.13 136.451C1616.13 129.532 1618.09 123.402 1622 118.062C1625.99 112.721 1631.7 108.585 1639.15 105.651C1646.67 102.643 1655.55 101.138 1665.77 101.138C1683.98 101.138 1699.51 105.802 1712.37 115.128L1700.18 133.292C1689.28 126.373 1678.03 122.913 1666.45 122.913C1653.06 122.913 1646.37 126.749 1646.37 134.421C1646.37 137.053 1647.16 139.234 1648.74 140.964C1650.39 142.694 1653.21 144.349 1657.2 145.928C1661.26 147.508 1667.47 149.463 1675.82 151.795C1684.39 154.202 1691.38 156.834 1696.8 159.692C1702.29 162.55 1706.54 166.349 1709.55 171.087C1712.63 175.826 1714.17 181.88 1714.17 189.251C1714.17 197.525 1711.69 204.557 1706.73 210.349C1701.84 216.065 1695.3 220.352 1687.1 223.21C1678.9 225.993 1669.84 227.385 1659.91 227.385C1649.08 227.385 1639.41 225.843 1630.91 222.759C1622.41 219.675 1615.08 215.426 1608.91 210.01L1624.37 192.636C1629.26 196.547 1634.71 199.668 1640.73 202C1646.75 204.256 1653.1 205.385 1659.79 205.385ZM1775.06 173.344C1775.89 184.099 1779.05 192.072 1784.54 197.262C1790.11 202.451 1797.21 205.046 1805.86 205.046C1811.35 205.046 1816.62 204.181 1821.66 202.451C1826.7 200.721 1831.78 198.164 1836.89 194.779L1849.3 211.815C1843.51 216.704 1836.74 220.54 1828.99 223.323C1821.25 226.031 1812.9 227.385 1803.95 227.385C1791.24 227.385 1780.4 224.752 1771.45 219.487C1762.58 214.222 1755.85 206.851 1751.26 197.374C1746.75 187.897 1744.49 176.916 1744.49 164.431C1744.49 152.472 1746.71 141.716 1751.15 132.164C1755.66 122.537 1762.13 114.978 1770.55 109.487C1779.05 103.921 1789.05 101.138 1800.56 101.138C1811.39 101.138 1820.83 103.545 1828.88 108.359C1836.93 113.173 1843.13 120.13 1847.5 129.231C1851.86 138.256 1854.04 149.012 1854.04 161.497C1854.04 165.785 1853.85 169.733 1853.47 173.344H1775.06ZM1800.67 122.123C1793.23 122.123 1787.21 124.793 1782.62 130.133C1778.11 135.398 1775.48 143.446 1774.73 154.277H1825.04C1824.89 143.973 1822.75 136.038 1818.61 130.472C1814.55 124.906 1808.57 122.123 1800.67 122.123Z" fill="white"/>
</svg>
````

## File: docs/logo/light.svg
````
<svg width="1867" height="292" viewBox="0 0 1867 292" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M266.265 106.202C224.72 90.3033 258.998 29.4218 201.857 30.9671C132.032 32.8557 22.6176 142.669 33.7922 214.023C39.3453 249.357 66.9381 234.523 79.8952 239.674C88.499 243.073 98.6794 258.423 109.683 260.861C61.0078 288.846 -1.51452 262.2 0.0279922 202.211C2.25607 113.859 129.873 -14.2905 220.847 1.29899C271.647 10.0209 277.954 64.0347 266.265 106.202Z" fill="black"/>
<path d="M67.4872 157.091L107.73 195.069C133.37 218.11 201.446 258.32 232.296 231.056C268.665 198.915 191.746 87.9001 156.337 70.1817L187.427 56.2061C235.862 91.6086 309.49 206.676 249.504 256.775C210.804 289.087 148.418 261.72 111.741 237.649C83.8041 219.312 43.4241 193.009 67.4872 157.057V157.091Z" fill="black"/>
<path d="M109.717 12.9395C96.6917 13.2829 86.511 30.246 76.9474 33.2334C68.4465 35.8774 56.6886 28.6321 43.9029 38.2125C30.0546 48.5826 34.7861 98.0981 8.22063 110.426C-8.12999 62.3865 2.04951 5.11049 61.1106 0.200137C65.6695 -0.177582 116.367 3.1876 109.717 12.9053V12.9395Z" fill="black"/>
<path d="M206.999 157.091C228.8 193.214 189.277 234.489 156.37 201.559L206.999 157.091Z" fill="black"/>
<path d="M504.359 178.759C504.359 195.08 498.53 206.701 486.872 213.621C475.289 220.54 460.397 224 442.195 224H393.795V67.9692H439.374C456.523 67.9692 470.513 71.053 481.344 77.2205C492.174 83.388 497.59 93.5419 497.59 107.682C497.59 116.708 494.882 124.079 489.467 129.795C484.051 135.511 477.169 139.385 468.821 141.415C478.899 142.995 487.323 146.718 494.092 152.585C500.937 158.451 504.359 167.176 504.359 178.759ZM466.338 110.39C466.338 103.47 464.157 98.4308 459.795 95.2718C455.508 92.1128 449.002 90.5333 440.277 90.5333H424.708V131.713H441.631C450.13 131.713 456.373 130.021 460.359 126.636C464.345 123.251 466.338 117.836 466.338 110.39ZM472.318 177.969C472.318 169.019 469.836 162.701 464.872 159.015C459.908 155.33 452.913 153.487 443.887 153.487H424.708V200.872H442.533C451.409 200.872 458.591 199.255 464.082 196.021C469.573 192.711 472.318 186.694 472.318 177.969ZM619.064 101.251C622.675 101.251 625.946 101.552 628.88 102.154C631.888 102.68 634.859 103.47 637.793 104.523L632.49 151.118H612.634V127.764C605.037 128.366 598.381 131.788 592.664 138.031C587.023 144.274 582.548 152.735 579.239 163.415V203.354H603.044V224H532.644V203.354H549.454V125.056H532.644V104.523H572.131L577.659 131.938C582.097 121.634 587.625 113.962 594.244 108.923C600.938 103.809 609.211 101.251 619.064 101.251ZM716.508 101.138C728.242 101.138 738.283 103.733 746.631 108.923C754.98 114.038 761.298 121.333 765.585 130.81C769.948 140.212 772.129 151.268 772.129 163.979C772.129 176.916 769.948 188.161 765.585 197.713C761.223 207.19 754.83 214.523 746.406 219.713C738.057 224.827 728.054 227.385 716.395 227.385C704.662 227.385 694.621 224.865 686.272 219.826C677.924 214.786 671.568 207.528 667.206 198.051C662.843 188.574 660.662 177.292 660.662 164.205C660.662 151.72 662.843 140.738 667.206 131.262C671.643 121.709 678.036 114.301 686.385 109.036C694.809 103.771 704.85 101.138 716.508 101.138ZM716.508 123.59C708.084 123.59 701.842 126.899 697.78 133.518C693.719 140.062 691.688 150.291 691.688 164.205C691.688 178.27 693.719 188.574 697.78 195.118C701.842 201.662 708.047 204.933 716.395 204.933C724.744 204.933 730.949 201.662 735.011 195.118C739.072 188.499 741.103 178.12 741.103 163.979C741.103 150.215 739.072 140.062 735.011 133.518C730.949 126.899 724.782 123.59 716.508 123.59ZM917.521 104.523L899.244 224H864.27L852.198 141.077L839.337 224H805.039L785.973 104.523H813.952L824.332 205.497L839.111 119.641H866.526L880.065 205.497L890.67 104.523H917.521ZM983.037 205.385C990.182 205.385 995.823 204.181 999.96 201.774C1004.17 199.292 1006.28 195.832 1006.28 191.395C1006.28 188.311 1005.56 185.791 1004.13 183.836C1002.71 181.88 999.96 180.038 995.899 178.308C991.912 176.503 985.858 174.509 977.734 172.328C969.461 170.222 962.541 167.74 956.975 164.882C951.41 161.949 947.085 158.188 944.001 153.6C940.917 148.937 939.375 143.221 939.375 136.451C939.375 129.532 941.331 123.402 945.242 118.062C949.228 112.721 954.945 108.585 962.391 105.651C969.912 102.643 978.787 101.138 989.017 101.138C1007.22 101.138 1022.75 105.802 1035.61 115.128L1023.43 133.292C1012.52 126.373 1001.28 122.913 989.693 122.913C976.305 122.913 969.611 126.749 969.611 134.421C969.611 137.053 970.401 139.234 971.981 140.964C973.635 142.694 976.456 144.349 980.442 145.928C984.504 147.508 990.709 149.463 999.058 151.795C1007.63 154.202 1014.63 156.834 1020.04 159.692C1025.53 162.55 1029.78 166.349 1032.79 171.087C1035.87 175.826 1037.42 181.88 1037.42 189.251C1037.42 197.525 1034.93 204.557 1029.97 210.349C1025.08 216.065 1018.54 220.352 1010.34 223.21C1002.14 225.993 993.078 227.385 983.15 227.385C972.319 227.385 962.654 225.843 954.155 222.759C945.656 219.675 938.322 215.426 932.155 210.01L947.611 192.636C952.5 196.547 957.953 199.668 963.97 202C969.987 204.256 976.343 205.385 983.037 205.385ZM1098.31 173.344C1099.13 184.099 1102.29 192.072 1107.78 197.262C1113.35 202.451 1120.46 205.046 1129.11 205.046C1134.6 205.046 1139.86 204.181 1144.9 202.451C1149.94 200.721 1155.02 198.164 1160.13 194.779L1172.54 211.815C1166.75 216.704 1159.98 220.54 1152.23 223.323C1144.49 226.031 1136.14 227.385 1127.19 227.385C1114.48 227.385 1103.65 224.752 1094.7 219.487C1085.82 214.222 1079.09 206.851 1074.5 197.374C1069.99 187.897 1067.73 176.916 1067.73 164.431C1067.73 152.472 1069.95 141.716 1074.39 132.164C1078.9 122.537 1085.37 114.978 1093.79 109.487C1102.29 103.921 1112.3 101.138 1123.8 101.138C1134.63 101.138 1144.07 103.545 1152.12 108.359C1160.17 113.173 1166.37 120.13 1170.74 129.231C1175.1 138.256 1177.28 149.012 1177.28 161.497C1177.28 165.785 1177.09 169.733 1176.72 173.344H1098.31ZM1123.92 122.123C1116.47 122.123 1110.45 124.793 1105.87 130.133C1101.35 135.398 1098.72 143.446 1097.97 154.277H1148.29C1148.14 143.973 1145.99 136.038 1141.86 130.472C1137.79 124.906 1131.81 122.123 1123.92 122.123ZM1295.82 101.251C1299.43 101.251 1302.7 101.552 1305.64 102.154C1308.65 102.68 1311.62 103.47 1314.55 104.523L1309.25 151.118H1289.39V127.764C1281.79 128.366 1275.14 131.788 1269.42 138.031C1263.78 144.274 1259.31 152.735 1256 163.415V203.354H1279.8V224H1209.4V203.354H1226.21V125.056H1209.4V104.523H1248.89L1254.42 131.938C1258.85 121.634 1264.38 113.962 1271 108.923C1277.7 103.809 1285.97 101.251 1295.82 101.251ZM1584.35 172.328C1584.35 183.084 1582.17 192.636 1577.81 200.985C1573.52 209.258 1567.16 215.726 1558.74 220.39C1550.32 225.053 1540.2 227.385 1528.39 227.385C1516.43 227.385 1506.28 225.091 1497.93 220.503C1489.58 215.915 1483.26 209.484 1478.98 201.21C1474.76 192.937 1472.66 183.309 1472.66 172.328V67.9692H1503.57V163.641C1503.57 172.817 1504.36 180.301 1505.94 186.092C1507.52 191.884 1510.12 196.246 1513.73 199.179C1517.34 202.113 1522.22 203.579 1528.39 203.579C1534.56 203.579 1539.45 202.113 1543.06 199.179C1546.74 196.246 1549.38 191.884 1550.96 186.092C1552.54 180.301 1553.33 172.817 1553.33 163.641V67.9692H1584.35V172.328ZM1659.79 205.385C1666.94 205.385 1672.58 204.181 1676.72 201.774C1680.93 199.292 1683.04 195.832 1683.04 191.395C1683.04 188.311 1682.32 185.791 1680.89 183.836C1679.46 181.88 1676.72 180.038 1672.66 178.308C1668.67 176.503 1662.62 174.509 1654.49 172.328C1646.22 170.222 1639.3 167.74 1633.73 164.882C1628.17 161.949 1623.84 158.188 1620.76 153.6C1617.68 148.937 1616.13 143.221 1616.13 136.451C1616.13 129.532 1618.09 123.402 1622 118.062C1625.99 112.721 1631.7 108.585 1639.15 105.651C1646.67 102.643 1655.55 101.138 1665.77 101.138C1683.98 101.138 1699.51 105.802 1712.37 115.128L1700.18 133.292C1689.28 126.373 1678.03 122.913 1666.45 122.913C1653.06 122.913 1646.37 126.749 1646.37 134.421C1646.37 137.053 1647.16 139.234 1648.74 140.964C1650.39 142.694 1653.21 144.349 1657.2 145.928C1661.26 147.508 1667.47 149.463 1675.82 151.795C1684.39 154.202 1691.38 156.834 1696.8 159.692C1702.29 162.55 1706.54 166.349 1709.55 171.087C1712.63 175.826 1714.17 181.88 1714.17 189.251C1714.17 197.525 1711.69 204.557 1706.73 210.349C1701.84 216.065 1695.3 220.352 1687.1 223.21C1678.9 225.993 1669.84 227.385 1659.91 227.385C1649.08 227.385 1639.41 225.843 1630.91 222.759C1622.41 219.675 1615.08 215.426 1608.91 210.01L1624.37 192.636C1629.26 196.547 1634.71 199.668 1640.73 202C1646.75 204.256 1653.1 205.385 1659.79 205.385ZM1775.06 173.344C1775.89 184.099 1779.05 192.072 1784.54 197.262C1790.11 202.451 1797.21 205.046 1805.86 205.046C1811.35 205.046 1816.62 204.181 1821.66 202.451C1826.7 200.721 1831.78 198.164 1836.89 194.779L1849.3 211.815C1843.51 216.704 1836.74 220.54 1828.99 223.323C1821.25 226.031 1812.9 227.385 1803.95 227.385C1791.24 227.385 1780.4 224.752 1771.45 219.487C1762.58 214.222 1755.85 206.851 1751.26 197.374C1746.75 187.897 1744.49 176.916 1744.49 164.431C1744.49 152.472 1746.71 141.716 1751.15 132.164C1755.66 122.537 1762.13 114.978 1770.55 109.487C1779.05 103.921 1789.05 101.138 1800.56 101.138C1811.39 101.138 1820.83 103.545 1828.88 108.359C1836.93 113.173 1843.13 120.13 1847.5 129.231C1851.86 138.256 1854.04 149.012 1854.04 161.497C1854.04 165.785 1853.85 169.733 1853.47 173.344H1775.06ZM1800.67 122.123C1793.23 122.123 1787.21 124.793 1782.62 130.133C1778.11 135.398 1775.48 143.446 1774.73 154.277H1825.04C1824.89 143.973 1822.75 136.038 1818.61 130.472C1814.55 124.906 1808.57 122.123 1800.67 122.123Z" fill="black"/>
</svg>
````

## File: docs/quickstart.mdx
````
---
title: "Quickstart"
description: "Start using Browser Use with this quickstart guide"
icon: "rocket"
---

{/* You can install Browser Use from PyPI or clone it from Github. */}

## Prepare the environment

Browser Use requires Python 3.11 or higher.

First, we recommend using [uv](https://docs.astral.sh/uv/) to setup the Python environment.

```bash
uv venv --python 3.11
```

and activate it with:

```bash
# For Mac/Linux:
source .venv/bin/activate

# For Windows:
.venv\Scripts\activate
```

Install the dependencies:

```bash
uv pip install browser-use
```

Then install patchright:

```bash
uv run patchright install
```

## Create an agent

Then you can use the agent as follows:

```python agent.py
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
load_dotenv()

import asyncio

llm = ChatOpenAI(model="gpt-4o")

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=llm,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

## Set up your LLM API keys

`ChatOpenAI` and other Langchain chat models require API keys. You should store these in your `.env` file. For example, for OpenAI and Anthropic, you can set the API keys in your `.env` file, such as:


```bash .env
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```

For other LLM models you can refer to the [Langchain documentation](https://python.langchain.com/docs/integrations/chat/) to find how to set them up with their specific API keys.
````

## File: docs/README.md
````markdown
# Docs

The official documentation for Browser Use. The docs are published to [Browser Use Docs](https://docs.browser-use.com).

### Development

Install the [Mintlify CLI](https://www.npmjs.com/package/mintlify) to preview the documentation changes locally. To install, use the following command

```
npm i -g mintlify
```

Run the following command at the root of your documentation (where mint.json is)

```
mintlify dev
```
````

## File: eval/claude-3.5.py
````python
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

from browser_use import Agent, Browser

load_dotenv()


async def run_agent(task: str, browser: Browser | None = None, max_steps: int = 38):
	browser = browser or Browser()
	llm = ChatAnthropic(
		model_name='claude-3-5-sonnet-20240620',
		temperature=0.0,
		timeout=100,
		stop=None,
	)
	agent = Agent(task=task, llm=llm, browser=browser)
	result = await agent.run(max_steps=max_steps)
	return result
````

## File: eval/claude-3.6.py
````python
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

from browser_use import Agent, Browser

load_dotenv()


async def run_agent(task: str, browser: Browser | None = None, max_steps: int = 38):
	browser = browser or Browser()
	llm = ChatAnthropic(
		model_name='claude-3-5-sonnet-20241022',
		temperature=0.0,
		timeout=100,
		stop=None,
	)
	agent = Agent(task=task, llm=llm, browser=browser)
	result = await agent.run(max_steps=max_steps)
	return result
````

## File: eval/claude-3.7.py
````python
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

from browser_use import Agent, Browser

load_dotenv()


async def run_agent(task: str, browser: Browser | None = None, max_steps: int = 38):
	browser = browser or Browser()
	llm = ChatAnthropic(
		model_name='claude-3-7-sonnet-20250219',
		temperature=0.0,
		timeout=100,
		stop=None,
	)
	agent = Agent(task=task, llm=llm, browser=browser)
	result = await agent.run(max_steps=max_steps)
	return result
````

## File: eval/deepseek-r1.py
````python
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from browser_use import Agent, Browser

load_dotenv()

api_key_deepseek = os.getenv('DEEPSEEK_API_KEY', '')
if not api_key_deepseek:
	raise ValueError('DEEPSEEK_API_KEY is not set')


async def run_agent(task: str, browser: Browser | None = None, max_steps: int = 38):
	browser = browser or Browser()
	llm = ChatOpenAI(
		base_url='https://api.deepseek.com/v1',
		model='deepseek-reasoner',
		api_key=SecretStr(api_key_deepseek),
	)
	agent = Agent(task=task, llm=llm, use_vision=False, browser=browser)
	result = await agent.run(max_steps=max_steps)
	return result
````

## File: eval/deepseek.py
````python
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from browser_use import Agent, Browser

load_dotenv()

api_key_deepseek = os.getenv('DEEPSEEK_API_KEY', '')
if not api_key_deepseek:
	raise ValueError('DEEPSEEK_API_KEY is not set')


async def run_agent(task: str, browser: Browser | None = None, max_steps: int = 38):
	browser = browser or Browser()
	llm = ChatOpenAI(
		base_url='https://api.deepseek.com/v1',
		model='deepseek-chat',
		api_key=SecretStr(api_key_deepseek),
	)
	agent = Agent(task=task, llm=llm, use_vision=False, browser=browser)
	result = await agent.run(max_steps=max_steps)
	return result
````

## File: eval/gemini-1.5-flash.py
````python
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent, Browser

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY', '')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')


async def run_agent(task: str, browser: Browser | None = None, max_steps: int = 38):
	browser = browser or Browser()
	llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash-latest', api_key=SecretStr(api_key))
	agent = Agent(task=task, llm=llm, browser=browser)
	result = await agent.run(max_steps=max_steps)
	return result
````

## File: eval/gemini-2.0-flash.py
````python
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent, Browser

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY', '')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')


async def run_agent(task: str, browser: Browser | None = None, max_steps: int = 38):
	browser = browser or Browser()
	llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))
	agent = Agent(task=task, llm=llm, browser=browser)
	result = await agent.run(max_steps=max_steps)
	return result
````

## File: eval/gemini-2.5-preview.py
````python
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent, Browser

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY', '')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')


async def run_agent(task: str, browser: Browser | None = None, max_steps: int = 38):
	browser = browser or Browser()
	llm = ChatGoogleGenerativeAI(model='gemini-2.5-pro-preview-03-25', api_key=SecretStr(api_key))
	agent = Agent(task=task, llm=llm, browser=browser)
	result = await agent.run(max_steps=max_steps)
	return result
````

## File: eval/gpt-4.1.py
````python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent, Browser

load_dotenv()


async def run_agent(task: str, browser: Browser | None = None, max_steps: int = 38):
	browser = browser or Browser()
	llm = ChatOpenAI(
		model='gpt-4.1-2025-04-14',
		temperature=0.0,
	)
	agent = Agent(task=task, llm=llm, browser=browser)
	result = await agent.run(max_steps=max_steps)
	return result
````

## File: eval/gpt-4o-no-boundingbox.py
````python
import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent, Browser

load_dotenv()


async def run_agent(task: str, browser: Browser | None = None, max_steps: int = 38):
	browser = browser or Browser()
	browser.config.new_context_config.highlight_elements = False
	llm = ChatOpenAI(
		model='gpt-4o',
		temperature=0.0,
	)
	agent = Agent(task=task, llm=llm, browser=browser)
	result = await agent.run(max_steps=max_steps)
	return result


if __name__ == '__main__':
	task = 'Open 1 random Wikipedia pages in new tab'
	result = asyncio.run(run_agent(task))
````

## File: eval/gpt-4o-no-vision.py
````python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent, Browser

load_dotenv()


async def run_agent(task: str, browser: Browser | None = None, max_steps: int = 38):
	browser = browser or Browser()
	llm = ChatOpenAI(
		model='gpt-4o',
		temperature=0.0,
	)
	agent = Agent(task=task, llm=llm, use_vision=False, browser=browser)
	result = await agent.run(max_steps=max_steps)
	return result
````

## File: eval/gpt-4o-viewport-0.py
````python
import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent, Browser

load_dotenv()


async def run_agent(task: str, browser: Browser | None = None, max_steps: int = 38):
	browser = browser or Browser()
	llm = ChatOpenAI(
		model='gpt-4o',
		temperature=0.0,
	)
	browser.config.new_context_config.viewport_expansion = 0
	agent = Agent(task=task, llm=llm, browser=browser)
	result = await agent.run(max_steps=max_steps)
	return result


if __name__ == '__main__':
	task = 'Go to https://www.google.com and search for "python" and click on the first result'
	result = asyncio.run(run_agent(task))
	print(result)
````

## File: eval/gpt-4o.py
````python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent, Browser

load_dotenv()


async def run_agent(task: str, browser: Browser | None = None, max_steps: int = 38):
	browser = browser or Browser()
	llm = ChatOpenAI(
		model='gpt-4o',
		temperature=0.0,
	)
	agent = Agent(task=task, llm=llm, browser=browser)
	result = await agent.run(max_steps=max_steps)
	return result
````

## File: eval/grok.py
````python
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from browser_use import Agent, Browser

load_dotenv()

api_key = os.getenv('GROK_API_KEY', '')
if not api_key:
	raise ValueError('GROK_API_KEY is not set')


async def run_agent(task: str, browser: Browser | None = None, max_steps: int = 38):
	browser = browser or Browser()
	agent = Agent(
		task=task,
		use_vision=False,
		llm=ChatOpenAI(model='grok-3-beta', base_url='https://api.x.ai/v1', api_key=SecretStr(api_key)),
		browser=browser,
	)

	await agent.run()
````

## File: examples/browser/real_browser.py
````python
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

import dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent, Browser, BrowserConfig

dotenv.load_dotenv()

browser = Browser(
	config=BrowserConfig(
		# NOTE: you need to close your chrome browser - so that this can open your browser in debug mode
		browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
	)
)


async def main():
	agent = Agent(
		task='In docs.google.com write my Papa a quick letter',
		llm=ChatOpenAI(model='gpt-4o'),
		browser=browser,
	)

	await agent.run()
	await browser.close()

	input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/browser/stealth.py
````python
import asyncio
import os
import sys

from langchain_openai import ChatOpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from browser_use import Agent, Browser, BrowserConfig, BrowserContextConfig

llm = ChatOpenAI(model='gpt-4o')
browser = Browser(
	config=BrowserConfig(
		headless=False,
		disable_security=False,
		keep_alive=True,
		new_context_config=BrowserContextConfig(
			keep_alive=True,
			disable_security=False,
		),
	)
)


async def main():
	agent = Agent(
		task="""
            Go to https://bot-detector.rebrowser.net/ and verify that all the bot checks are passed.
        """,
		llm=llm,
		browser=browser,
	)
	await agent.run()
	input('Press Enter to continue to the next test...')

	agent = Agent(
		task="""
            Go to https://www.webflow.com/ and verify that the page is not blocked by a bot check.
        """,
		llm=llm,
		browser=browser,
	)
	await agent.run()
	input('Press Enter to continue to the next test...')

	agent = Agent(
		task="""
            Go to https://www.okta.com/ and verify that the page is not blocked by a bot check.
        """,
		llm=llm,
		browser=browser,
	)
	await agent.run()

	agent = Agent(
		task="""
            Go to https://abrahamjuliot.github.io/creepjs/ and verify that the detection score is >50%.
        """,
		llm=llm,
		browser=browser,
	)
	await agent.run()

	input('Press Enter to close the browser...')

	agent = Agent(
		task="""
            Go to https://nowsecure.nl/ check the "I'm not a robot" checkbox.
        """,
		llm=llm,
		browser=browser,
	)
	await agent.run()

	input('Press Enter to close the browser...')


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/browser/using_cdp.py
````python
"""
Simple demonstration of the CDP feature.

To test this locally, follow these steps:
1. Create a shortcut for the executable Chrome file.
2. Add the following argument to the shortcut:
   - On Windows: `--remote-debugging-port=9222`
3. Open a web browser and navigate to `http://localhost:9222/json/version` to verify that the Remote Debugging Protocol (CDP) is running.
4. Launch this example.

@dev You need to set the `GEMINI_API_KEY` environment variable before proceeding.
"""

import os
import sys

from dotenv import load_dotenv
from pydantic import SecretStr

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from langchain_google_genai import ChatGoogleGenerativeAI

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')

browser = Browser(
	config=BrowserConfig(
		headless=False,
		cdp_url='http://localhost:9222',
	)
)
controller = Controller()


async def main():
	task = 'In docs.google.com write my Papa a quick thank you for everything letter \n - Magnus'
	task += ' and save the document as pdf'
	model = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(str(api_key)))
	agent = Agent(
		task=task,
		llm=model,
		controller=controller,
		browser=browser,
	)

	await agent.run()
	await browser.close()

	input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/custom-functions/action_filters.py
````python
"""
Action filters (domains and page_filter) let you limit actions available to the Agent on a step-by-step/page-by-page basis.

@registry.action(..., domains=['*'], page_filter=lambda page: return True)
async def some_action(browser: BrowserContext):
    ...

This helps prevent the LLM from deciding to use an action that is not compatible with the current page.
It helps limit decision fatique by scoping actions only to pages where they make sense.
It also helps prevent mis-triggering stateful actions or actions that could break other programs or leak secrets.

For example:
    - only run on certain domains @registry.action(..., domains=['example.com', '*.example.com', 'example.co.*']) (supports globs, but no regex)
    - only fill in a password on a specific login page url
    - only run if this action has not run before on this page (e.g. by looking up the url in a file on disk)

During each step, the agent recalculates the actions available specifically for that page, and informs the LLM.
"""

import asyncio

from langchain_openai import ChatOpenAI
from patchright.async_api import Page

from browser_use.agent.service import Agent, Browser, BrowserContext, Controller

# Initialize controller and registry
controller = Controller()
registry = controller.registry


# Action will only be available to Agent on Google domains because of the domain filter
@registry.action(description='Trigger disco mode', domains=['google.com', '*.google.com'])
async def disco_mode(browser: BrowserContext):
	page = await browser.get_current_page()
	await page.evaluate("""() => { 
        // define the wiggle animation
        document.styleSheets[0].insertRule('@keyframes wiggle { 0% { transform: rotate(0deg); } 50% { transform: rotate(10deg); } 100% { transform: rotate(0deg); } }');
        
        document.querySelectorAll("*").forEach(element => {
            element.style.animation = "wiggle 0.5s infinite";
        });
    }""")


# you can create a custom page filter function that determines if the action should be available for a given page
def is_login_page(page: Page) -> bool:
	return 'login' in page.url.lower() or 'signin' in page.url.lower()


# then use it in the action decorator to limit the action to only be available on pages where the filter returns True
@registry.action(description='Use the force, luke', page_filter=is_login_page)
async def use_the_force(browser: BrowserContext):
	# this will only ever run on pages that matched the filter
	page = await browser.get_current_page()
	assert is_login_page(page)

	await page.evaluate("""() => { document.querySelector('body').innerHTML = 'These are not the droids you are looking for';}""")


async def main():
	"""Main function to run the example"""
	browser = Browser()
	llm = ChatOpenAI(model_name='gpt-4o')

	# Create the agent
	agent = Agent(  # disco mode will not be triggered on apple.com because the LLM won't be able to see that action available, it should work on Google.com though.
		task="""
            Go to apple.com and trigger disco mode (if dont know how to do that, then just move on).
            Then go to google.com and trigger disco mode.
            After that, go to the Google login page and Use the force, luke.
        """,
		llm=llm,
		browser=browser,
		controller=controller,
	)

	# Run the agent
	await agent.run(max_steps=10)

	# Cleanup
	await browser.close()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/custom-functions/advanced_search.py
````python
import json
import os
import sys

import httpx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from browser_use import ActionResult, Agent, Controller

load_dotenv()


class Person(BaseModel):
	name: str
	email: str | None = None


class PersonList(BaseModel):
	people: list[Person]


controller = Controller(exclude_actions=['search_google'], output_model=PersonList)
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

if not BEARER_TOKEN:
	# use the api key for ask tessa
	# you can also use other apis like exa, xAI, perplexity, etc.
	raise ValueError('BEARER_TOKEN is not set - go to https://www.heytessa.ai/ and create an api key')


@controller.registry.action('Search the web for a specific query')
async def search_web(query: str):
	keys_to_use = ['url', 'title', 'content', 'author', 'score']
	headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
	async with httpx.AsyncClient() as client:
		response = await client.post('https://asktessa.ai/api/search', headers=headers, json={'query': query})

	final_results = [
		{key: source[key] for key in keys_to_use if key in source}
		for source in response.json()['sources']
		if source['score'] >= 0.8
	]
	# print(json.dumps(final_results, indent=4))
	result_text = json.dumps(final_results, indent=4)
	print(result_text)
	return ActionResult(extracted_content=result_text, include_in_memory=True)


names = [
	'Ruedi Aebersold',
	'Bernd Bodenmiller',
	'Eugene Demler',
	'Erich Fischer',
	'Pietro Gambardella',
	'Matthias Huss',
	'Reto Knutti',
	'Maksym Kovalenko',
	'Antonio Lanzavecchia',
	'Maria Lukatskaya',
	'Jochen Markard',
	'Javier Pérez-Ramírez',
	'Federica Sallusto',
	'Gisbert Schneider',
	'Sonia I. Seneviratne',
	'Michael Siegrist',
	'Johan Six',
	'Tanja Stadler',
	'Shinichi Sunagawa',
	'Michael Bruce Zimmermann',
]


async def main():
	task = 'use search_web with "find email address of the following ETH professor:" for each of the following persons in a list of actions. Finally return the list with name and email if provided'
	task += '\n' + '\n'.join(names)
	model = ChatOpenAI(model='gpt-4o')
	agent = Agent(task=task, llm=model, controller=controller, max_actions_per_step=20)

	history = await agent.run()

	result = history.final_result()
	if result:
		parsed: PersonList = PersonList.model_validate_json(result)

		for person in parsed.people:
			print(f'{person.name} - {person.email}')
	else:
		print('No result')


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/custom-functions/clipboard.py
````python
import os
import sys

from browser_use.agent.views import ActionResult

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

import pyperclip
from langchain_openai import ChatOpenAI

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

browser = Browser(
	config=BrowserConfig(
		headless=False,
	)
)
controller = Controller()


@controller.registry.action('Copy text to clipboard')
def copy_to_clipboard(text: str):
	pyperclip.copy(text)
	return ActionResult(extracted_content=text)


@controller.registry.action('Paste text from clipboard')
async def paste_from_clipboard(browser: BrowserContext):
	text = pyperclip.paste()
	# send text to browser
	page = await browser.get_current_page()
	await page.keyboard.type(text)

	return ActionResult(extracted_content=text)


async def main():
	task = 'Copy the text "Hello, world!" to the clipboard, then go to google.com and paste the text'
	model = ChatOpenAI(model='gpt-4o')
	agent = Agent(
		task=task,
		llm=model,
		controller=controller,
		browser=browser,
	)

	await agent.run()
	await browser.close()

	input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/custom-functions/custom_hooks_before_after_step.py
````python
"""
Description: These Python modules are designed to capture detailed
browser usage datafor analysis, with both server and client
components working together to record and store the information.

Author: Carlos A. Planchón
https://github.com/carlosplanchon/

Adapt this code to your needs.

Feedback is appreciated!
"""

#####################
#                   #
#   --- UTILS ---   #
#                   #
#####################

import base64


def b64_to_png(b64_string: str, output_file):
	"""
	Convert a Base64-encoded string to a PNG file.

	:param b64_string: A string containing Base64-encoded data
	:param output_file: The path to the output PNG file
	"""
	with open(output_file, 'wb') as f:
		f.write(base64.b64decode(b64_string))


###################################################################
#                                                                 #
#   --- FASTAPI API TO RECORD AND SAVE Browser-Use ACTIVITY ---   #
#                                                                 #
###################################################################

# Save to api.py and run with `python api.py`

# ! pip install uvicorn
# ! pip install fastapi
# ! pip install prettyprinter

import json
from pathlib import Path

import prettyprinter
from fastapi import FastAPI, Request

prettyprinter.install_extras()

app = FastAPI()


@app.post('/post_agent_history_step')
async def post_agent_history_step(request: Request):
	data = await request.json()
	prettyprinter.cpprint(data)

	# Ensure the "recordings" folder exists using pathlib
	recordings_folder = Path('recordings')
	recordings_folder.mkdir(exist_ok=True)

	# Determine the next file number by examining existing .json files
	existing_numbers = []
	for item in recordings_folder.iterdir():
		if item.is_file() and item.suffix == '.json':
			try:
				file_num = int(item.stem)
				existing_numbers.append(file_num)
			except ValueError:
				# In case the file name isn't just a number
				...

	if existing_numbers:
		next_number = max(existing_numbers) + 1
	else:
		next_number = 1

	# Construct the file path
	file_path = recordings_folder / f'{next_number}.json'

	# Save the JSON data to the file
	with file_path.open('w') as f:
		json.dump(data, f, indent=2)

	return {'status': 'ok', 'message': f'Saved to {file_path}'}


if __name__ == '__main__':
	import uvicorn

	uvicorn.run(app, host='0.0.0.0', port=9000)


##############################################################
#                                                            #
#   --- CLIENT TO RECORD AND SAVE Browser-Use ACTIVITY ---   #
#                                                            #
##############################################################

"""
pyobjtojson:

A Python library to safely and recursively serialize any Python object
(including Pydantic models and dataclasses) into JSON-ready structures,
gracefully handling circular references.
"""

# ! pip install -U pyobjtojson
# ! pip install -U prettyprinter

import asyncio

import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pyobjtojson import obj_to_json

from browser_use import Agent

# import prettyprinter

# prettyprinter.install_extras()

load_dotenv()


def send_agent_history_step(data):
	url = 'http://127.0.0.1:9000/post_agent_history_step'
	response = requests.post(url, json=data)
	return response.json()


async def record_activity(agent_obj):
	website_html = None
	website_screenshot = None
	urls_json_last_elem = None
	model_thoughts_last_elem = None
	model_outputs_json_last_elem = None
	model_actions_json_last_elem = None
	extracted_content_json_last_elem = None

	print('--- ON_STEP_START HOOK ---')
	website_html: str = await agent_obj.browser_context.get_page_html()
	website_screenshot: str = await agent_obj.browser_context.take_screenshot()

	print('--> History:')
	if hasattr(agent_obj, 'state'):
		history = agent_obj.state.history
	else:
		history = None

	model_thoughts = obj_to_json(obj=history.model_thoughts(), check_circular=False)

	# print("--- MODEL THOUGHTS ---")
	if len(model_thoughts) > 0:
		model_thoughts_last_elem = model_thoughts[-1]
		# prettyprinter.cpprint(model_thoughts_last_elem)

	# print("--- MODEL OUTPUT ACTION ---")
	model_outputs = agent_obj.state.history.model_outputs()
	model_outputs_json = obj_to_json(obj=model_outputs, check_circular=False)

	if len(model_outputs_json) > 0:
		model_outputs_json_last_elem = model_outputs_json[-1]
		# prettyprinter.cpprint(model_outputs_json_last_elem)

	# print("--- MODEL INTERACTED ELEM ---")
	model_actions = agent_obj.state.history.model_actions()
	model_actions_json = obj_to_json(obj=model_actions, check_circular=False)

	if len(model_actions_json) > 0:
		model_actions_json_last_elem = model_actions_json[-1]
		# prettyprinter.cpprint(model_actions_json_last_elem)

	# print("--- EXTRACTED CONTENT ---")
	extracted_content = agent_obj.state.history.extracted_content()
	extracted_content_json = obj_to_json(obj=extracted_content, check_circular=False)
	if len(extracted_content_json) > 0:
		extracted_content_json_last_elem = extracted_content_json[-1]
		# prettyprinter.cpprint(extracted_content_json_last_elem)

	# print("--- URLS ---")
	urls = agent_obj.state.history.urls()
	# prettyprinter.cpprint(urls)
	urls_json = obj_to_json(obj=urls, check_circular=False)

	if len(urls_json) > 0:
		urls_json_last_elem = urls_json[-1]
		# prettyprinter.cpprint(urls_json_last_elem)

	model_step_summary = {
		'website_html': website_html,
		'website_screenshot': website_screenshot,
		'url': urls_json_last_elem,
		'model_thoughts': model_thoughts_last_elem,
		'model_outputs': model_outputs_json_last_elem,
		'model_actions': model_actions_json_last_elem,
		'extracted_content': extracted_content_json_last_elem,
	}

	print('--- MODEL STEP SUMMARY ---')
	# prettyprinter.cpprint(model_step_summary)

	send_agent_history_step(data=model_step_summary)

	# response = send_agent_history_step(data=history)
	# print(response)

	# print("--> Website HTML:")
	# print(website_html[:200])
	# print("--> Website Screenshot:")
	# print(website_screenshot[:200])


agent = Agent(
	task='Compare the price of gpt-4o and DeepSeek-V3',
	llm=ChatOpenAI(model='gpt-4o'),
)


async def run_agent():
	try:
		await agent.run(on_step_start=record_activity, max_steps=30)
	except Exception as e:
		print(e)


asyncio.run(run_agent())
````

## File: examples/custom-functions/group_ungroup.py
````python
import os
import sys

from browser_use.agent.views import ActionResult
from browser_use.browser.views import GroupTabsAction, UngroupTabsAction

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from langchain_openai import ChatOpenAI

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

# async def group_tabs(self, tab_ids: list[int] , title: str, color: str = "blue"):
#     """Reset the browser session
#     Call this when you don't want to kill the context but just kill the state
#     """
#     # close all tabs and clear cached state
#     page = await self.get_current_page()

#     js = f"""
#         chrome.tabs.group({{ tabIds: {tab_ids} }}, (groupId) => {{
#             chrome.tabGroups.update(groupId, {{
#                 title: "{title}",
#                 color: "{color}"
#             }});
#         }});
#         """

#     await page.evaluate(js)

# async def ungroup_tabs(self, tab_ids: list[int]):
#     """Reset the browser session
#     Call this when you don't want to kill the context but just kill the state
#     """
#     # close all tabs and clear cached state
#     page = await self.get_current_page()

#     js = f"""
#             for (const tabId of {tab_ids}) {{
#                 chrome.tabs.ungroup(tabId);
#             }}
#         """

#     await page.evaluate(js)


# Initialize controller first
browser = Browser(
	config=BrowserConfig(
		headless=False,
		chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
	)
)
controller = Controller()


@controller.action('Visually group browser tabs in Chrome', param_model=GroupTabsAction, requires_browser=True)
async def group_tabs(params: GroupTabsAction, browser: BrowserContext):
	try:
		# Get tab IDs from params
		tab_ids = params.tab_ids
		title = params.title
		color = params.color

		# Call the low-level implementation in BrowserContext
		result = await browser.group_tabs(tab_ids, title, color='red')
		return ActionResult(extracted_content=result, include_in_memory=True)
	except Exception as e:
		return ActionResult(error=f'Failed to group tabs: {str(e)}')


# Register ungroup_tabs action
@controller.action('Remove visual grouping from tabs in Chrome', param_model=UngroupTabsAction, requires_browser=True)
async def ungroup_tabs(params: UngroupTabsAction, browser: BrowserContext):
	try:
		# Get tab IDs from params
		tab_ids = params.tab_ids

		# Call the low-level implementation in BrowserContext
		result = await browser.ungroup_tabs(tab_ids)
		return ActionResult(extracted_content=result, include_in_memory=True)
	except Exception as e:
		return ActionResult(error=f'Failed to ungroup tabs: {str(e)}')


async def main():
	task = 'Group tabs 1 and 2 into a "Research" group, then ungroup them.'

	model = ChatOpenAI(model='gpt-4o')
	agent = Agent(
		task=task,
		llm=model,
		controller=controller,
		browser=browser,
	)

	await agent.run()

	await browser.close()

	input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/custom-functions/hover_element.py
````python
import os
import sys
from typing import Optional

from pydantic import BaseModel

from browser_use.agent.views import ActionResult

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from langchain_openai import ChatOpenAI

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext


class HoverAction(BaseModel):
	index: Optional[int] = None
	xpath: Optional[str] = None
	selector: Optional[str] = None


browser = Browser(
	config=BrowserConfig(
		headless=False,
	)
)
controller = Controller()


@controller.registry.action(
	'Hover over an element',
	param_model=HoverAction,  # Define this model with at least "index: int" field
)
async def hover_element(params: HoverAction, browser: BrowserContext):
	"""
	Hovers over the element specified by its index from the cached selector map or by XPath.
	"""
	session = await browser.get_session()
	state = session.cached_state

	if params.xpath:
		# Use XPath to locate the element
		element_handle = await browser.get_locate_element_by_xpath(params.xpath)
		if element_handle is None:
			raise Exception(f'Failed to locate element with XPath {params.xpath}')
	elif params.selector:
		# Use CSS selector to locate the element
		element_handle = await browser.get_locate_element_by_css_selector(params.selector)
		if element_handle is None:
			raise Exception(f'Failed to locate element with CSS Selector {params.selector}')
	elif params.index is not None:
		# Use index to locate the element
		if state is None or params.index not in state.selector_map:
			raise Exception(f'Element index {params.index} does not exist - retry or use alternative actions')
		element_node = state.selector_map[params.index]
		element_handle = await browser.get_locate_element(element_node)
		if element_handle is None:
			raise Exception(f'Failed to locate element with index {params.index}')
	else:
		raise Exception('Either index or xpath must be provided')

	try:
		await element_handle.hover()
		msg = (
			f'🖱️ Hovered over element at index {params.index}'
			if params.index is not None
			else f'🖱️ Hovered over element with XPath {params.xpath}'
		)
		return ActionResult(extracted_content=msg, include_in_memory=True)
	except Exception as e:
		err_msg = f'❌ Failed to hover over element: {str(e)}'
		raise Exception(err_msg)


async def main():
	task = 'Open https://testpages.eviltester.com/styled/csspseudo/css-hover.html and hover the element with the css selector #hoverdivpara, then click on "Can you click me?"'
	# task = 'Open https://testpages.eviltester.com/styled/csspseudo/css-hover.html and hover the element with the xpath //*[@id="hoverdivpara"], then click on "Can you click me?"'
	model = ChatOpenAI(model='gpt-4o')
	agent = Agent(
		task=task,
		llm=model,
		controller=controller,
		browser=browser,
	)

	await agent.run()
	await browser.close()

	input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/custom-functions/notification.py
````python
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import ActionResult, Agent, Controller

load_dotenv()

controller = Controller()


@controller.registry.action('Done with task ')
async def done(text: str):
	import yagmail

	# To send emails use
	# STEP 1: go to https://support.google.com/accounts/answer/185833
	# STEP 2: Create an app password (you can't use here your normal gmail password)
	# STEP 3: Use the app password in the code below for the password
	yag = yagmail.SMTP('your_email@gmail.com', 'your_app_password')
	yag.send(
		to='recipient@example.com',
		subject='Test Email',
		contents=f'result\n: {text}',
	)

	return ActionResult(is_done=True, extracted_content='Email sent!')


async def main():
	task = 'go to brower-use.com and then done'
	model = ChatOpenAI(model='gpt-4o')
	agent = Agent(task=task, llm=model, controller=controller)

	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/custom-functions/onepassword_2fa.py
````python
import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from onepassword.client import Client  # pip install onepassword-sdk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from browser_use import ActionResult, Agent, Controller

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

OP_SERVICE_ACCOUNT_TOKEN = os.getenv('OP_SERVICE_ACCOUNT_TOKEN')
OP_ITEM_ID = os.getenv('OP_ITEM_ID')  # Go to 1Password, right click on the item, click "Copy Secret Reference"


controller = Controller()


@controller.registry.action('Get 2FA code from 1Password for Google Account', domains=['*.google.com', 'google.com'])
async def get_1password_2fa() -> ActionResult:
	"""
	Custom action to retrieve 2FA/MFA code from 1Password using onepassword.client SDK.
	"""
	client = await Client.authenticate(
		# setup instructions: https://github.com/1Password/onepassword-sdk-python/#-get-started
		auth=OP_SERVICE_ACCOUNT_TOKEN,
		integration_name='Browser-Use',
		integration_version='v1.0.0',
	)

	mfa_code = await client.secrets.resolve(f'op://Private/{OP_ITEM_ID}/One-time passcode')

	return ActionResult(extracted_content=mfa_code)


async def main():
	# Example task using the 1Password 2FA action
	task = 'Go to account.google.com, enter username and password, then if prompted for 2FA code, get 2FA code from 1Password for and enter it'

	model = ChatOpenAI(model='gpt-4o')
	agent = Agent(task=task, llm=model, controller=controller)

	result = await agent.run()
	print(f'Task completed with result: {result}')


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/custom-functions/save_to_file_hugging_face.py
````python
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from typing import List

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from browser_use.agent.service import Agent
from browser_use.controller.service import Controller

# Initialize controller first
controller = Controller()


class Model(BaseModel):
	title: str
	url: str
	likes: int
	license: str


class Models(BaseModel):
	models: List[Model]


@controller.action('Save models', param_model=Models)
def save_models(params: Models):
	with open('models.txt', 'a') as f:
		for model in params.models:
			f.write(f'{model.title} ({model.url}): {model.likes} likes, {model.license}\n')


# video: https://preview.screen.studio/share/EtOhIk0P
async def main():
	task = 'Look up models with a license of cc-by-sa-4.0 and sort by most likes on Hugging face, save top 5 to file.'

	model = ChatOpenAI(model='gpt-4o')
	agent = Agent(task=task, llm=model, controller=controller)

	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/features/click_fallback_options.py
````python
import asyncio
import os
import sys

from aiohttp import web  # make sure to install aiohttp: pip install aiohttp
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# from langchain_google_genai import ChatGoogleGenerativeAI


# Adjust path if necessary
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from browser_use import Agent, Controller

# Define a simple HTML page
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Custom Select Div</title>
  <style>
    .custom-select {
      position: relative;
      width: 200px;
      font-family: Arial, sans-serif;
      margin-bottom: 20px;
    }

    .select-display {
      padding: 10px;
      border: 1px solid #ccc;
      background-color: #fff;
      cursor: pointer;
    }

    .select-options {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      border: 1px solid #ccc;
      border-top: none;
      background-color: #fff;
      display: none;
      max-height: 150px;
      overflow-y: auto;
      z-index: 100;
    }

    .select-option {
      padding: 10px;
      cursor: pointer;
    }

    .select-option:hover {
      background-color: #f0f0f0;
    }
  </style>
</head>
<body>
  <div class="custom-select">
    <div class="select-display">Select a fruit</div>
    <div class="select-options">
      <div class="select-option" data-value="option1">Apples</div>
      <div class="select-option" data-value="option2">Oranges</div>
      <div class="select-option" data-value="option3">Pineapples</div>
    </div>
  </div>

  <div class="custom-select">
    <div class="select-display">Select a fruit</div>
    <div class="select-options">
      <div class="select-option" data-value="option1">Apples</div>
      <div class="select-option" data-value="option2">Oranges</div>
      <div class="select-option" data-value="option3">Pineapples</div>
    </div>
  </div>
  
  <div class="custom-select">
    <div class="select-display">Select a fruit</div>
    <div class="select-options">
      <div class="select-option" data-value="option1">Apples</div>
      <div class="select-option" data-value="option2">Oranges</div>
      <div class="select-option" data-value="option3">Pineapples</div>
    </div>
  </div>
  
  <div class="custom-select">
    <div class="select-display">Select a fruit</div>
    <div class="select-options">
      <div class="select-option" data-value="option1">Apples</div>
      <div class="select-option" data-value="option2">Oranges</div>
      <div class="select-option" data-value="option3">Pineapples</div>
    </div>
  </div>

  <label for="cars">Choose a car:</label>
  <select name="cars" id="cars">
    <option value="volvo">Volvo</option>
    <option value="bmw">BMW</option>
    <option value="mercedes">Mercedes</option>
    <option value="audi">Audi</option>
  </select>

  <button onclick="alert('I told you!')">Don't click me</button>

  <script>
    document.querySelectorAll('.custom-select').forEach(customSelect => {
      const selectDisplay = customSelect.querySelector('.select-display');
      const selectOptions = customSelect.querySelector('.select-options');
      const options = customSelect.querySelectorAll('.select-option');

      selectDisplay.addEventListener('click', (e) => {
        // Close all other dropdowns
        document.querySelectorAll('.select-options').forEach(opt => {
          if (opt !== selectOptions) opt.style.display = 'none';
        });

        // Toggle current dropdown
        const isVisible = selectOptions.style.display === 'block';
        selectOptions.style.display = isVisible ? 'none' : 'block';

        e.stopPropagation();
      });

      options.forEach(option => {
        option.addEventListener('click', () => {
          selectDisplay.textContent = option.textContent;
          selectDisplay.dataset.value = option.getAttribute('data-value');
          selectOptions.style.display = 'none';
        });
      });
    });

    // Close all dropdowns if clicking outside
    document.addEventListener('click', () => {
      document.querySelectorAll('.select-options').forEach(opt => {
        opt.style.display = 'none';
      });
    });
  </script>
</body>
</html>

"""


# aiohttp request handler to serve the HTML content
async def handle_root(request):
	return web.Response(text=HTML_CONTENT, content_type='text/html')


# Function to run the HTTP server
async def run_http_server():
	app = web.Application()
	app.router.add_get('/', handle_root)
	runner = web.AppRunner(app)
	await runner.setup()
	site = web.TCPSite(runner, 'localhost', 8000)
	await site.start()
	print('HTTP server running on http://localhost:8000')
	# Keep the server running indefinitely.
	await asyncio.Event().wait()


# Your agent tasks and other logic
load_dotenv()
controller = Controller()


async def main():
	# Start the HTTP server in the background.
	server_task = asyncio.create_task(run_http_server())

	# Example tasks for the agent.
	xpath_task = 'Open http://localhost:8000/, click element with the xpath "/html/body/div/div[1]" and then click on Oranges'
	css_selector_task = 'Open http://localhost:8000/, click element with the selector div.select-display and then click on apples'
	text_task = 'Open http://localhost:8000/, click the third element with the text "Select a fruit" and then click on Apples, then click the second element with the text "Select a fruit" and then click on Oranges'
	select_task = 'Open http://localhost:8000/, choose the car BMW'
	button_task = 'Open http://localhost:8000/, click on the button'

	llm = ChatOpenAI(model='gpt-4o')
	# llm = ChatGoogleGenerativeAI(
	#     model="gemini-2.0-flash-lite",
	# )

	# Run different agent tasks.
	for task in [xpath_task, css_selector_task, text_task, select_task, button_task]:
		agent = Agent(
			task=task,
			llm=llm,
			controller=controller,
		)
		await agent.run()

	# Wait for user input before shutting down.
	input('Press Enter to close...')
	# Cancel the server task once finished.
	server_task.cancel()
	try:
		await server_task
	except asyncio.CancelledError:
		print('HTTP server stopped.')


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/features/cross_origin_iframes.py
````python
"""
Example of how it supports cross-origin iframes.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig

# Load environment variables
load_dotenv()
if not os.getenv('OPENAI_API_KEY'):
	raise ValueError('OPENAI_API_KEY is not set. Please add it to your environment variables.')


browser = Browser(
	config=BrowserConfig(
		browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
	)
)
controller = Controller()


async def main():
	agent = Agent(
		task='Click "Go cross-site (simple page)" button on https://csreis.github.io/tests/cross-site-iframe.html then tell me the text within',
		llm=ChatOpenAI(model='gpt-4o', temperature=0.0),
		controller=controller,
		browser=browser,
	)

	await agent.run()
	await browser.close()

	input('Press Enter to close...')


if __name__ == '__main__':
	try:
		asyncio.run(main())
	except Exception as e:
		print(e)
````

## File: examples/features/custom_output.py
````python
"""
Show how to use custom outputs.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import os
import sys
from typing import List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from browser_use import Agent, Controller

load_dotenv()


class Post(BaseModel):
	post_title: str
	post_url: str
	num_comments: int
	hours_since_post: int


class Posts(BaseModel):
	posts: List[Post]


controller = Controller(output_model=Posts)


async def main():
	task = 'Go to hackernews show hn and give me the first  5 posts'
	model = ChatOpenAI(model='gpt-4o')
	agent = Agent(task=task, llm=model, controller=controller)

	history = await agent.run()

	result = history.final_result()
	if result:
		parsed: Posts = Posts.model_validate_json(result)

		for post in parsed.posts:
			print('\n--------------------------------')
			print(f'Title:            {post.post_title}')
			print(f'URL:              {post.post_url}')
			print(f'Comments:         {post.num_comments}')
			print(f'Hours since post: {post.hours_since_post}')
	else:
		print('No result')


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/features/custom_system_prompt.py
````python
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from langchain_openai import ChatOpenAI

from browser_use import Agent

extend_system_message = (
	'REMEMBER the most important RULE: ALWAYS open first a new tab and go first to url wikipedia.com no matter the task!!!'
)

# or use override_system_message to completely override the system prompt


async def main():
	task = "do google search to find images of Elon Musk's wife"
	model = ChatOpenAI(model='gpt-4o')
	agent = Agent(task=task, llm=model, extend_system_message=extend_system_message)

	print(
		json.dumps(
			agent.message_manager.system_prompt.model_dump(exclude_unset=True),
			indent=4,
		)
	)

	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/features/custom_user_agent.py
````python
import os
import sys

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from browser_use.browser.context import BrowserContext, BrowserContextConfig

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse
import asyncio

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.controller.service import Controller


def get_llm(provider: str):
	if provider == 'anthropic':
		return ChatAnthropic(model_name='claude-3-5-sonnet-20240620', timeout=25, stop=None, temperature=0.0)
	elif provider == 'openai':
		return ChatOpenAI(model='gpt-4o', temperature=0.0)

	else:
		raise ValueError(f'Unsupported provider: {provider}')


# NOTE: This example is to find your current user agent string to use it in the browser_context
task = 'go to https://whatismyuseragent.com and find the current user agent string '


controller = Controller()


parser = argparse.ArgumentParser()
parser.add_argument('--query', type=str, help='The query to process', default=task)
parser.add_argument(
	'--provider',
	type=str,
	choices=['openai', 'anthropic'],
	default='openai',
	help='The model provider to use (default: openai)',
)

args = parser.parse_args()

llm = get_llm(args.provider)


browser = Browser(
	config=BrowserConfig(
		# browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
	)
)

browser_context = BrowserContext(config=BrowserContextConfig(user_agent='foobarfoo'), browser=browser)

agent = Agent(
	task=args.query,
	llm=llm,
	controller=controller,
	# browser=browser,
	browser_context=browser_context,
	use_vision=True,
	max_actions_per_step=1,
)


async def main():
	await agent.run(max_steps=25)

	input('Press Enter to close the browser...')
	await browser_context.close()


asyncio.run(main())
````

## File: examples/features/download_file.py
````python
import asyncio
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))
browser = Browser(
	config=BrowserConfig(
		new_context_config=BrowserContextConfig(save_downloads_path=os.path.join(os.path.expanduser('~'), 'downloads'))
	)
)


async def run_download():
	agent = Agent(
		task=('Go to "https://file-examples.com/" and download the smallest doc file.'),
		llm=llm,
		max_actions_per_step=8,
		use_vision=True,
		browser=browser,
	)
	await agent.run(max_steps=25)
	await browser.close()


if __name__ == '__main__':
	asyncio.run(run_download())
````

## File: examples/features/drag_drop.py
````python
import asyncio
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))


task_1 = """
Navigate to: https://sortablejs.github.io/Sortable/. 
Then scroll down to the first examplw with title "Simple list example". 
Drag the element with name "item 1" to below the element with name "item 3".
"""


task_2 = """
Navigate to: https://excalidraw.com/.
Click on the pencil icon (with index 40).
Then draw a triangle in the canvas.
Draw the triangle starting from coordinate (400,400).
You can use the drag and drop action to draw the triangle.
"""


async def run_search():
	agent = Agent(
		task=task_1,
		llm=llm,
		max_actions_per_step=1,
		use_vision=True,
	)

	await agent.run(max_steps=25)


if __name__ == '__main__':
	asyncio.run(run_search())
````

## File: examples/features/follow_up_tasks.py
````python
import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent, Browser, BrowserConfig, BrowserContextConfig, Controller

load_dotenv()

# Initialize the model
llm = ChatOpenAI(
	model='gpt-4o',
	temperature=0.0,
)
# Get your chrome path
browser = Browser(
	config=BrowserConfig(
		browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
		new_context_config=BrowserContextConfig(
			keep_alive=True,
		),
	),
)

controller = Controller()


task = 'Find the founders of browser-use and draft them a short personalized message'

agent = Agent(task=task, llm=llm, controller=controller, browser=browser)


async def main():
	await agent.run()

	# new_task = input('Type in a new task: ')
	new_task = 'Find an image of the founders'

	agent.add_new_task(new_task)

	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/features/initial_actions.py
````python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent

load_dotenv()
llm = ChatOpenAI(model='gpt-4o')

initial_actions = [
	{'open_tab': {'url': 'https://www.google.com'}},
	{'open_tab': {'url': 'https://en.wikipedia.org/wiki/Randomness'}},
	{'scroll_down': {'amount': 1000}},
]
agent = Agent(
	task='What theories are displayed on the page?',
	initial_actions=initial_actions,
	llm=llm,
)


async def main():
	await agent.run(max_steps=10)


if __name__ == '__main__':
	import asyncio

	asyncio.run(main())
````

## File: examples/features/multi-tab_handling.py
````python
"""
Simple try of the agent.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from langchain_openai import ChatOpenAI

from browser_use import Agent

# video: https://preview.screen.studio/share/clenCmS6
llm = ChatOpenAI(model='gpt-4o')
agent = Agent(
	task='open 3 tabs with elon musk, trump, and steve jobs, then go back to the first and stop',
	llm=llm,
)


async def main():
	await agent.run()


asyncio.run(main())
````

## File: examples/features/multiple_agents_same_browser.py
````python
import os
import sys

from langchain_openai import ChatOpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from browser_use import Agent, Browser


# Video: https://preview.screen.studio/share/8Elaq9sm
async def main():
	# Persist the browser state across agents

	browser = Browser()
	async with await browser.new_context() as context:
		model = ChatOpenAI(model='gpt-4o')
		current_agent = None

		async def get_input():
			return await asyncio.get_event_loop().run_in_executor(
				None, lambda: input('Enter task (p: pause current agent, r: resume, b: break): ')
			)

		while True:
			task = await get_input()

			if task.lower() == 'p':
				# Pause the current agent if one exists
				if current_agent:
					current_agent.pause()
				continue
			elif task.lower() == 'r':
				# Resume the current agent if one exists
				if current_agent:
					current_agent.resume()
				continue
			elif task.lower() == 'b':
				# Break the current agent's execution if one exists
				if current_agent:
					current_agent.stop()
					current_agent = None
				continue

			# If there's a current agent running, pause it before starting new one
			if current_agent:
				current_agent.pause()

			# Create and run new agent with the task
			current_agent = Agent(
				task=task,
				llm=model,
				browser_context=context,
			)

			# Run the agent asynchronously without blocking
			asyncio.create_task(current_agent.run())


asyncio.run(main())

# Now aad the cheapest to the cart
````

## File: examples/features/outsource_state.py
````python
"""
Show how to use custom outputs.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import os
import sys

import anyio

from browser_use.agent.views import AgentState
from browser_use.browser.browser import Browser, BrowserConfig

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent

load_dotenv()


async def main():
	task = 'Go to hackernews show hn and give me the first  5 posts'

	browser = Browser(
		config=BrowserConfig(
			headless=True,
		)
	)

	browser_context = await browser.new_context()

	agent_state = AgentState()

	for i in range(10):
		agent = Agent(
			task=task,
			llm=ChatOpenAI(model='gpt-4o'),
			browser=browser,
			browser_context=browser_context,
			injected_agent_state=agent_state,
			page_extraction_llm=ChatOpenAI(model='gpt-4o-mini'),
		)

		done, valid = await agent.take_step()
		print(f'Step {i}: Done: {done}, Valid: {valid}')

		if done and valid:
			break

		agent_state.history.history = []

		# Save state to file
		async with await anyio.open_file('agent_state.json', 'w') as f:
			serialized = agent_state.model_dump_json(exclude={'history'})
			await f.write(serialized)

		# Load state back from file
		async with await anyio.open_file('agent_state.json', 'r') as f:
			loaded_json = await f.read()
			agent_state = AgentState.model_validate_json(loaded_json)

		break


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/features/parallel_agents.py
````python
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from langchain_openai import ChatOpenAI

from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig

browser = Browser(
	config=BrowserConfig(
		disable_security=True,
		headless=False,
		new_context_config=BrowserContextConfig(save_recording_path='./tmp/recordings'),
	)
)
llm = ChatOpenAI(model='gpt-4o')


async def main():
	agents = [
		Agent(task=task, llm=llm, browser=browser)
		for task in [
			'Search Google for weather in Tokyo',
			'Check Reddit front page title',
			'Look up Bitcoin price on Coinbase',
			'Find NASA image of the day',
			# 'Check top story on CNN',
			# 'Search latest SpaceX launch date',
			# 'Look up population of Paris',
			# 'Find current time in Sydney',
			# 'Check who won last Super Bowl',
			# 'Search trending topics on Twitter',
		]
	]

	await asyncio.gather(*[agent.run() for agent in agents])

	# async with await browser.new_context() as context:
	agentX = Agent(
		task='Go to apple.com and return the title of the page',
		llm=llm,
		browser=browser,
		# browser_context=context,
	)
	await agentX.run()

	await browser.close()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/features/pause_agent.py
````python
import asyncio
import os
import sys

import dotenv

dotenv.load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import threading

from langchain_openai import ChatOpenAI

from browser_use import Agent


class AgentController:
	def __init__(self):
		llm = ChatOpenAI(model='gpt-4o')
		self.agent = Agent(
			task='open in one action https://www.google.com, https://www.wikipedia.org, https://www.youtube.com, https://www.github.com, https://amazon.com',
			llm=llm,
		)
		self.running = False

	async def run_agent(self):
		"""Run the agent"""
		self.running = True
		await self.agent.run()

	def start(self):
		"""Start the agent in a separate thread"""
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop.run_until_complete(self.run_agent())

	def pause(self):
		"""Pause the agent"""
		self.agent.pause()

	def resume(self):
		"""Resume the agent"""
		self.agent.resume()

	def stop(self):
		"""Stop the agent"""
		self.agent.stop()
		self.running = False


def print_menu():
	print('\nAgent Control Menu:')
	print('1. Start')
	print('2. Pause')
	print('3. Resume')
	print('4. Stop')
	print('5. Exit')


async def main():
	controller = AgentController()
	agent_thread = None

	while True:
		print_menu()
		try:
			choice = input('Enter your choice (1-5): ')
		except KeyboardInterrupt:
			choice = '5'

		if choice == '1' and not agent_thread:
			print('Starting agent...')
			agent_thread = threading.Thread(target=controller.start)
			agent_thread.start()

		elif choice == '2':
			print('Pausing agent...')
			controller.pause()

		elif choice == '3':
			print('Resuming agent...')
			controller.resume()

		elif choice == '4':
			print('Stopping agent...')
			controller.stop()
			if agent_thread:
				agent_thread.join()
				agent_thread = None

		elif choice == '5':
			print('Exiting...')
			if controller.running:
				controller.stop()
				if agent_thread:
					agent_thread.join()
			break

		await asyncio.sleep(0.1)  # Small delay to prevent CPU spinning


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/features/planner.py
````python
import asyncio

from langchain_openai import ChatOpenAI

from browser_use import Agent

llm = ChatOpenAI(model='gpt-4o', temperature=0.0)
planner_llm = ChatOpenAI(
	model='o3-mini',
)
task = 'your task'


agent = Agent(task=task, llm=llm, planner_llm=planner_llm, use_vision_for_planner=False, planner_interval=1)


async def main():
	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/features/restrict_urls.py
````python
import os
import sys

from langchain_openai import ChatOpenAI

from browser_use.browser.context import BrowserContextConfig

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig

llm = ChatOpenAI(model='gpt-4o', temperature=0.0)
task = (
	"go to google.com and search for openai.com and click on the first link then extract content and scroll down - what's there?"
)

allowed_domains = ['google.com']

browser = Browser(
	config=BrowserConfig(
		browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
		new_context_config=BrowserContextConfig(
			allowed_domains=allowed_domains,
		),
	),
)

agent = Agent(
	task=task,
	llm=llm,
	browser=browser,
)


async def main():
	await agent.run(max_steps=25)

	input('Press Enter to close the browser...')
	await browser.close()


asyncio.run(main())
````

## File: examples/features/result_processing.py
````python
import os
import sys
from pprint import pprint

from browser_use.browser.browser import Browser, BrowserConfig, BrowserContextConfig

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from langchain_openai import ChatOpenAI

from browser_use import Agent
from browser_use.agent.views import AgentHistoryList

llm = ChatOpenAI(model='gpt-4o')
browser = Browser(
	config=BrowserConfig(
		headless=False,
		disable_security=True,
	)
)


async def main():
	async with await browser.new_context(
		config=BrowserContextConfig(
			trace_path='./tmp/result_processing',
			no_viewport=False,
			browser_window_size={'width': 1280, 'height': 1000},
		)
	) as browser_context:
		agent = Agent(
			task="go to google.com and type 'OpenAI' click search and give me the first url",
			llm=llm,
			browser_context=browser_context,
		)
		history: AgentHistoryList = await agent.run(max_steps=3)

		print('Final Result:')
		pprint(history.final_result(), indent=4)

		print('\nErrors:')
		pprint(history.errors(), indent=4)

		# e.g. xPaths the model clicked on
		print('\nModel Outputs:')
		pprint(history.model_actions(), indent=4)

		print('\nThoughts:')
		pprint(history.model_thoughts(), indent=4)
	# close browser
	await browser.close()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/features/save_trace.py
````python
import os
import sys

from langchain_openai import ChatOpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig

llm = ChatOpenAI(model='gpt-4o', temperature=0.0)


async def main():
	browser = Browser()

	async with await browser.new_context(config=BrowserContextConfig(trace_path='./tmp/traces/')) as context:
		agent = Agent(
			task='Go to hackernews, then go to apple.com and return all titles of open tabs',
			llm=llm,
			browser_context=context,
		)
		await agent.run()

	await browser.close()


asyncio.run(main())
````

## File: examples/features/sensitive_data.py
````python
import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent

load_dotenv()

# Initialize the model
llm = ChatOpenAI(
	model='gpt-4o',
	temperature=0.0,
)
# the model will see x_name and x_password, but never the actual values.
sensitive_data = {'x_name': 'my_x_name', 'x_password': 'my_x_password'}
task = 'go to x.com and login with x_name and x_password then find interesting posts and like them'

agent = Agent(task=task, llm=llm, sensitive_data=sensitive_data)


async def main():
	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/features/small_model_for_extraction.py
````python
import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent

load_dotenv()

llm = ChatOpenAI(model='gpt-4o', temperature=0.0)
small_llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.0)
task = 'Find the founders of browser-use in ycombinator, extract all links and open the links one by one'
agent = Agent(task=task, llm=llm, page_extraction_llm=small_llm)


async def main():
	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/features/task_with_memory.py
````python
import asyncio
import json
from typing import List

import anyio
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from browser_use import Agent, Browser, BrowserConfig, Controller

links = [
	'https://docs.mem0.ai/components/llms/models/litellm',
	'https://docs.mem0.ai/components/llms/models/mistral_AI',
	'https://docs.mem0.ai/components/llms/models/ollama',
	'https://docs.mem0.ai/components/llms/models/openai',
	'https://docs.mem0.ai/components/llms/models/together',
	'https://docs.mem0.ai/components/llms/models/xAI',
	'https://docs.mem0.ai/components/llms/overview',
	'https://docs.mem0.ai/components/vectordbs/config',
	'https://docs.mem0.ai/components/vectordbs/dbs/azure_ai_search',
	'https://docs.mem0.ai/components/vectordbs/dbs/chroma',
	'https://docs.mem0.ai/components/vectordbs/dbs/elasticsearch',
	'https://docs.mem0.ai/components/vectordbs/dbs/milvus',
	'https://docs.mem0.ai/components/vectordbs/dbs/opensearch',
	'https://docs.mem0.ai/components/vectordbs/dbs/pgvector',
	'https://docs.mem0.ai/components/vectordbs/dbs/pinecone',
	'https://docs.mem0.ai/components/vectordbs/dbs/qdrant',
	'https://docs.mem0.ai/components/vectordbs/dbs/redis',
	'https://docs.mem0.ai/components/vectordbs/dbs/supabase',
	'https://docs.mem0.ai/components/vectordbs/dbs/vertex_ai_vector_search',
	'https://docs.mem0.ai/components/vectordbs/dbs/weaviate',
	'https://docs.mem0.ai/components/vectordbs/overview',
	'https://docs.mem0.ai/contributing/development',
	'https://docs.mem0.ai/contributing/documentation',
	'https://docs.mem0.ai/core-concepts/memory-operations',
	'https://docs.mem0.ai/core-concepts/memory-types',
]


class Link(BaseModel):
	url: str
	title: str
	summary: str


class Links(BaseModel):
	links: List[Link]


initial_actions = [
	{'open_tab': {'url': 'https://docs.mem0.ai/'}},
]
controller = Controller(output_model=Links)
task_description = f"""
Visit all the links provided in {links} and summarize the content of the page with url and title. There are {len(links)} links to visit. Make sure to visit all the links. Return a json with the following format: [{{url: <url>, title: <title>, summary: <summary>}}].

Guidelines:
1. Strictly stay on the domain https://docs.mem0.ai
2. Do not visit any other websites.
3. Ignore the links that are hashed (#) or javascript (:), or mailto, or tel, or other protocols
4. Don't visit any other url other than the ones provided above.
5. Capture the unique urls which are not already visited.
6. If you visit any page that doesn't have host name docs.mem0.ai, then do not visit it and come back to the page with host name docs.mem0.ai.
"""


async def main(max_steps=500):
	config = BrowserConfig(headless=True)
	browser = Browser(config=config)

	agent = Agent(
		task=task_description,
		llm=ChatOpenAI(model='gpt-4o-mini'),
		controller=controller,
		initial_actions=initial_actions,
		enable_memory=True,
		browser=browser,
	)
	history = await agent.run(max_steps=max_steps)
	result = history.final_result()
	parsed_result = []
	if result:
		parsed: Links = Links.model_validate_json(result)
		print(f'Total parsed links: {len(parsed.links)}')
		for link in parsed.links:
			parsed_result.append({'title': link.title, 'url': link.url, 'summary': link.summary})
	else:
		print('No result')

	async with await anyio.open_file('result.json', 'w+') as f:
		await f.write(json.dumps(parsed_result, indent=4))


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/features/validate_output.py
````python
"""
Demonstrate output validator.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from browser_use import ActionResult, Agent, Controller

load_dotenv()

controller = Controller()


class DoneResult(BaseModel):
	title: str
	comments: str
	hours_since_start: int


# we overwrite done() in this example to demonstrate the validator
@controller.registry.action('Done with task', param_model=DoneResult)
async def done(params: DoneResult):
	result = ActionResult(is_done=True, extracted_content=params.model_dump_json())
	print(result)
	# NOTE: this is clearly wrong - to demonstrate the validator
	return 'blablabla'


async def main():
	task = 'Go to hackernews hn and give me the top 1 post'
	model = ChatOpenAI(model='gpt-4o')
	agent = Agent(task=task, llm=model, controller=controller, validate_output=True)
	# NOTE: this should fail to demonstrate the validator
	await agent.run(max_steps=5)


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/integrations/discord/discord_api.py
````python
import discord
from discord.ext import commands
from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel

from browser_use import BrowserConfig
from browser_use.agent.service import Agent, Browser

load_dotenv()


class DiscordBot(commands.Bot):
	"""Discord bot implementation for Browser-Use tasks.

	This bot allows users to run browser automation tasks through Discord messages.
	Processes tasks asynchronously and sends the result back to the user in response to the message.
	Messages must start with the configured prefix (default: "$bu") followed by the task description.

	Args:
	    llm (BaseChatModel): Language model instance to use for task processing
	    prefix (str, optional): Command prefix for triggering browser tasks. Defaults to "$bu"
	    ack (bool, optional): Whether to acknowledge task receipt with a message. Defaults to False
	    browser_config (BrowserConfig, optional): Browser configuration settings.
	        Defaults to headless mode

	Usage:
	    ```python
	    from langchain_openai import ChatOpenAI

	    llm = ChatOpenAI()
	    bot = DiscordBot(llm=llm, prefix='$bu', ack=True)
	    bot.run('YOUR_DISCORD_TOKEN')
	    ```

	Discord Usage:
	    Send messages starting with the prefix:
	    "$bu search for python tutorials"
	"""

	def __init__(
		self,
		llm: BaseChatModel,
		prefix: str = '$bu',
		ack: bool = False,
		browser_config: BrowserConfig = BrowserConfig(headless=True),
	):
		self.llm = llm
		self.prefix = prefix.strip()
		self.ack = ack
		self.browser_config = browser_config

		# Define intents.
		intents = discord.Intents.default()
		intents.message_content = True  # Enable message content intent
		intents.members = True  # Enable members intent for user info

		# Initialize the bot with a command prefix and intents.
		super().__init__(command_prefix='!', intents=intents)  # You may not need prefix, just here for flexibility

		# self.tree = app_commands.CommandTree(self) # Initialize command tree for slash commands.

	async def on_ready(self):
		"""Called when the bot is ready."""
		try:
			print(f'We have logged in as {self.user}')
			cmds = await self.tree.sync()  # Sync the command tree with discord

		except Exception as e:
			print(f'Error during bot startup: {e}')

	async def on_message(self, message):
		"""Called when a message is received."""
		try:
			if message.author == self.user:  # Ignore the bot's messages
				return
			if message.content.strip().startswith(f'{self.prefix} '):
				if self.ack:
					try:
						await message.reply(
							'Starting browser use task...',
							mention_author=True,  # Don't ping the user
						)
					except Exception as e:
						print(f'Error sending start message: {e}')

				try:
					agent_message = await self.run_agent(message.content.replace(f'{self.prefix} ', '').strip())
					await message.channel.send(content=f'{agent_message}', reference=message, mention_author=True)
				except Exception as e:
					await message.channel.send(
						content=f'Error during task execution: {str(e)}',
						reference=message,
						mention_author=True,
					)

		except Exception as e:
			print(f'Error in message handling: {e}')

	#    await self.process_commands(message)  # Needed to process bot commands

	async def run_agent(self, task: str) -> str:
		try:
			browser = Browser(config=self.browser_config)
			agent = Agent(task=(task), llm=self.llm, browser=browser)
			result = await agent.run()

			agent_message = None
			if result.is_done():
				agent_message = result.history[-1].result[0].extracted_content

			if agent_message is None:
				agent_message = 'Oops! Something went wrong while running Browser-Use.'

			return agent_message

		except Exception as e:
			raise Exception(f'Browser-use task failed: {str(e)}')
````

## File: examples/integrations/discord/discord_example.py
````python
"""
This examples requires you to have a Discord bot token and the bot already added to a server.

Five Steps to create and invite a Discord bot:

1. Create a Discord Application:
    *   Go to the Discord Developer Portal: https://discord.com/developers/applications
    *   Log in to the Discord website.
    *   Click on "New Application".
    *   Give the application a name and click "Create".
2. Configure the Bot:
    *   Navigate to the "Bot" tab on the left side of the screen.
    *   Make sure "Public Bot" is ticked if you want others to invite your bot.
	*	Generate your bot token by clicking on "Reset Token", Copy the token and save it securely.
        *   Do not share the bot token. Treat it like a password. If the token is leaked, regenerate it.
3. Enable Privileged Intents:
    *   Scroll down to the "Privileged Gateway Intents" section.
    *   Enable the necessary intents (e.g., "Server Members Intent" and "Message Content Intent").
   -->  Note: Enabling privileged intents for bots in over 100 guilds requires bot verification. You may need to contact Discord support to enable privileged intents for verified bots.
4. Generate Invite URL:
    *   Go to "OAuth2" tab and "OAuth2 URL Generator" section.
    *   Under "scopes", tick the "bot" checkbox.
    *   Tick the permissions required for your bot to function under “Bot Permissions”.
		*	e.g. "Send Messages", "Send Messages in Threads", "Read Message History",  "Mention Everyone".
    *   Copy the generated URL under the "GENERATED URL" section at the bottom.
5. Invite the Bot:
    *   Paste the URL into your browser.
    *   Choose a server to invite the bot to.
    *   Click “Authorize”.
   -->  Note: The person adding the bot needs "Manage Server" permissions.
6. Run the code below to start the bot with your bot token.
7. Write e.g. "/bu what's the weather in Tokyo?" to start a browser-use task and get a response inside the Discord channel.
"""

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import BrowserConfig
from examples.integrations.discord.discord_api import DiscordBot

load_dotenv()

# load credentials from environment variables
bot_token = os.getenv('DISCORD_BOT_TOKEN')
if not bot_token:
	raise ValueError('Discord bot token not found in .env file.')

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

bot = DiscordBot(
	llm=llm,  # required; instance of BaseChatModel
	prefix='$bu',  # optional; prefix of messages to trigger browser-use, defaults to "$bu"
	ack=True,  # optional; whether to acknowledge task receipt with a message, defaults to False
	browser_config=BrowserConfig(
		headless=False
	),  # optional; useful for changing headless mode or other browser configs, defaults to headless mode
)

bot.run(
	token=bot_token,  # required; Discord bot token
)
````

## File: examples/integrations/slack/README.md
````markdown
# Slack Integration

Steps to create and configure a Slack bot:

1. Create a Slack App:
    *   Go to the Slack API: https://api.slack.com/apps
    *   Click on "Create New App".
    *   Choose "From scratch" and give your app a name and select the workspace.
    *   Provide a name and description for your bot (these are required fields).
2. Configure the Bot:
    *   Navigate to the "OAuth & Permissions" tab on the left side of the screen.
    *   Under "Scopes", add the necessary bot token scopes (add these "chat:write", "channels:history", "im:history").
3. Enable Event Subscriptions:
    *   Navigate to the "Event Subscriptions" tab.
    *   Enable events and add the necessary bot events (add these "message.channels", "message.im").
    *   Add your request URL (you can use ngrok to expose your local server if needed). [See how to set up ngrok](#installing-and-starting-ngrok).
    *   **Note:** The URL provided by ngrok is ephemeral and will change each time ngrok is started. You will need to update the request URL in the bot's settings each time you restart ngrok. [See how to update the request URL](#updating-the-request-url-in-bots-settings).
4. Add the bot to your Slack workspace:
    *   Navigate to the "OAuth & Permissions" tab.
    *   Under "OAuth Tokens for Your Workspace", click on "Install App to Workspace".
    *   Follow the prompts to authorize the app and add it to your workspace.
5. Set up environment variables:
    *   Obtain the `SLACK_SIGNING_SECRET`:
        *   Go to the Slack API: https://api.slack.com/apps
        *   Select your app.
        *   Navigate to the "Basic Information" tab.
        *   Copy the "Signing Secret".
    *   Obtain the `SLACK_BOT_TOKEN`:
        *   Go to the Slack API: https://api.slack.com/apps
        *   Select your app.
        *   Navigate to the "OAuth & Permissions" tab.
        *   Copy the "Bot User OAuth Token".
    *   Create a `.env` file in the root directory of your project and add the following lines:
        ```env
        SLACK_SIGNING_SECRET=your-signing-secret
        SLACK_BOT_TOKEN=your-bot-token
        ```
6. Invite the bot to a channel:
    *   Use the `/invite @your-bot-name` command in the Slack channel where you want the bot to be active.
7. Run the code in `examples/slack_example.py` to start the bot with your bot token and signing secret.
8. Write e.g. "$bu what's the weather in Tokyo?" to start a browser-use task and get a response inside the Slack channel.

## Installing and Starting ngrok

To expose your local server to the internet, you can use ngrok. Follow these steps to install and start ngrok:

1. Download ngrok from the official website: https://ngrok.com/download
2. Create a free account and follow the official steps to install ngrok.
3. Start ngrok by running the following command in your terminal:
    ```sh
    ngrok http 3000
    ```
    Replace `3000` with the port number your local server is running on.

## Updating the Request URL in Bot's Settings

If you need to update the request URL (e.g., when the ngrok URL changes), follow these steps:

1. Go to the Slack API: https://api.slack.com/apps
2. Select your app.
3. Navigate to the "Event Subscriptions" tab.
4. Update the "Request URL" field with the new ngrok URL. The URL should be something like: `https://<ngrok-id>.ngrok-free.app/slack/events`
5. Save the changes.

## Installing Required Packages

To run this example, you need to install the following packages:

- `fastapi`
- `uvicorn`
- `slack_sdk`

You can install these packages using pip:

```sh
pip install fastapi uvicorn slack_sdk
````

## File: examples/integrations/slack/slack_api.py
````python
import logging
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from langchain_core.language_models.chat_models import BaseChatModel
from slack_sdk.errors import SlackApiError
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web.async_client import AsyncWebClient

from browser_use import BrowserConfig
from browser_use.agent.service import Agent, Browser
from browser_use.logging_config import setup_logging

load_dotenv()

setup_logging()
logger = logging.getLogger('slack')

app = FastAPI()


class SlackBot:
	def __init__(
		self,
		llm: BaseChatModel,
		bot_token: str,
		signing_secret: str,
		ack: bool = False,
		browser_config: BrowserConfig = BrowserConfig(headless=True),
	):
		if not bot_token or not signing_secret:
			raise ValueError('Bot token and signing secret must be provided')

		self.llm = llm
		self.ack = ack
		self.browser_config = browser_config
		self.client = AsyncWebClient(token=bot_token)
		self.signature_verifier = SignatureVerifier(signing_secret)
		self.processed_events = set()
		logger.info('SlackBot initialized')

	async def handle_event(self, event, event_id):
		try:
			logger.info(f'Received event id: {event_id}')
			if not event_id:
				logger.warning('Event ID missing in event data')
				return

			if event_id in self.processed_events:
				logger.info(f'Event {event_id} already processed')
				return
			self.processed_events.add(event_id)

			if 'subtype' in event and event['subtype'] == 'bot_message':
				return

			text = event.get('text')
			user_id = event.get('user')
			if text and text.startswith('$bu '):
				task = text[len('$bu ') :].strip()
				if self.ack:
					try:
						await self.send_message(
							event['channel'], f'<@{user_id}> Starting browser use task...', thread_ts=event.get('ts')
						)
					except Exception as e:
						logger.error(f'Error sending start message: {e}')

				try:
					agent_message = await self.run_agent(task)
					await self.send_message(event['channel'], f'<@{user_id}> {agent_message}', thread_ts=event.get('ts'))
				except Exception as e:
					await self.send_message(event['channel'], f'Error during task execution: {str(e)}', thread_ts=event.get('ts'))
		except Exception as e:
			logger.error(f'Error in handle_event: {str(e)}')

	async def run_agent(self, task: str) -> str:
		try:
			browser = Browser(config=self.browser_config)
			agent = Agent(task=task, llm=self.llm, browser=browser)
			result = await agent.run()

			agent_message = None
			if result.is_done():
				agent_message = result.history[-1].result[0].extracted_content

			if agent_message is None:
				agent_message = 'Oops! Something went wrong while running Browser-Use.'

			return agent_message

		except Exception as e:
			logger.error(f'Error during task execution: {str(e)}')
			return f'Error during task execution: {str(e)}'

	async def send_message(self, channel, text, thread_ts=None):
		try:
			await self.client.chat_postMessage(channel=channel, text=text, thread_ts=thread_ts)
		except SlackApiError as e:
			logger.error(f'Error sending message: {e.response["error"]}')


@app.post('/slack/events')
async def slack_events(request: Request, slack_bot: Annotated[SlackBot, Depends()]):
	try:
		if not slack_bot.signature_verifier.is_valid_request(await request.body(), dict(request.headers)):
			logger.warning('Request verification failed')
			raise HTTPException(status_code=400, detail='Request verification failed')

		event_data = await request.json()
		logger.info(f'Received event data: {event_data}')
		if 'challenge' in event_data:
			return {'challenge': event_data['challenge']}

		if 'event' in event_data:
			try:
				await slack_bot.handle_event(event_data.get('event'), event_data.get('event_id'))
			except Exception as e:
				logger.error(f'Error handling event: {str(e)}')

		return {}
	except Exception as e:
		logger.error(f'Error in slack_events: {str(e)}')
		raise HTTPException(status_code=500, detail='Internal Server Error')
````

## File: examples/integrations/slack/slack_example.py
````python
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import BrowserConfig
from examples.integrations.slack.slack_api import SlackBot, app

load_dotenv()

# load credentials from environment variables
bot_token = os.getenv('SLACK_BOT_TOKEN')
if not bot_token:
	raise ValueError('Slack bot token not found in .env file.')

signing_secret = os.getenv('SLACK_SIGNING_SECRET')
if not signing_secret:
	raise ValueError('Slack signing secret not found in .env file.')

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

slack_bot = SlackBot(
	llm=llm,  # required; instance of BaseChatModel
	bot_token=bot_token,  # required; Slack bot token
	signing_secret=signing_secret,  # required; Slack signing secret
	ack=True,  # optional; whether to acknowledge task receipt with a message, defaults to False
	browser_config=BrowserConfig(
		headless=True
	),  # optional; useful for changing headless mode or other browser configs, defaults to headless mode
)

app.dependency_overrides[SlackBot] = lambda: slack_bot

if __name__ == '__main__':
	import uvicorn

	uvicorn.run('integrations.slack.slack_api:app', host='0.0.0.0', port=3000)
````

## File: examples/models/_ollama.py
````python
# import os

# Optional: Disable telemetry
# os.environ["ANONYMIZED_TELEMETRY"] = "false"

# Optional: Set the OLLAMA host to a remote server
# os.environ["OLLAMA_HOST"] = "http://x.x.x.x:11434"

import asyncio

from langchain_ollama import ChatOllama

from browser_use import Agent
from browser_use.agent.views import AgentHistoryList


async def run_search() -> AgentHistoryList:
	agent = Agent(
		task="Search for a 'browser use' post on the r/LocalLLaMA subreddit and open it.",
		llm=ChatOllama(
			model='qwen2.5:32b-instruct-q4_K_M',
			num_ctx=32000,
		),
	)

	result = await agent.run()
	return result


async def main():
	result = await run_search()
	print('\n\n', result)


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/models/azure_openai.py
````python
"""
Simple try of the agent.

@dev You need to add AZURE_OPENAI_KEY and AZURE_OPENAI_ENDPOINT to your environment variables.
"""

import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from langchain_openai import AzureChatOpenAI

from browser_use import Agent

load_dotenv()

# Retrieve Azure-specific environment variables
azure_openai_api_key = os.getenv('AZURE_OPENAI_KEY')
azure_openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')

if not azure_openai_api_key or not azure_openai_endpoint:
	raise ValueError('AZURE_OPENAI_KEY or AZURE_OPENAI_ENDPOINT is not set')

# Initialize the Azure OpenAI client
llm = AzureChatOpenAI(
	model_name='gpt-4o',
	openai_api_key=azure_openai_api_key,
	azure_endpoint=azure_openai_endpoint,  # Corrected to use azure_endpoint instead of openai_api_base
	deployment_name='gpt-4o',  # Use deployment_name for Azure models
	api_version='2024-08-01-preview',  # Explicitly set the API version here
)

agent = Agent(
	task='Go to amazon.com, search for laptop, sort by best rating, and give me the price of the first result',
	llm=llm,
	enable_memory=True,
)


async def main():
	await agent.run(max_steps=10)
	input('Press Enter to continue...')


asyncio.run(main())
````

## File: examples/models/bedrock_claude.py
````python
"""
Automated news analysis and sentiment scoring using Bedrock.

@dev Ensure AWS environment variables are set correctly for Bedrock access.
"""

import argparse
import asyncio
import os
import sys

import boto3
from botocore.config import Config
from langchain_aws import ChatBedrockConverse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.controller.service import Controller


def get_llm():
	config = Config(retries={'max_attempts': 10, 'mode': 'adaptive'})
	bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1', config=config)

	return ChatBedrockConverse(
		model_id='us.anthropic.claude-3-5-sonnet-20241022-v2:0',
		temperature=0.0,
		max_tokens=None,
		client=bedrock_client,
	)


# Define the task for the agent
task = (
	"Visit cnn.com, navigate to the 'World News' section, and identify the latest headline. "
	'Open the first article and summarize its content in 3-4 sentences. '
	'Additionally, analyze the sentiment of the article (positive, neutral, or negative) '
	'and provide a confidence score for the sentiment. Present the result in a tabular format.'
)

parser = argparse.ArgumentParser()
parser.add_argument('--query', type=str, help='The query for the agent to execute', default=task)
args = parser.parse_args()

llm = get_llm()

browser = Browser(
	config=BrowserConfig(
		# browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
	)
)

agent = Agent(
	task=args.query,
	llm=llm,
	controller=Controller(),
	browser=browser,
	validate_output=True,
)


async def main():
	await agent.run(max_steps=30)
	await browser.close()


asyncio.run(main())
````

## File: examples/models/claude-3.7-sonnet.py
````python
"""
Simple script that runs the task of opening amazon and searching.
@dev Ensure we have a `ANTHROPIC_API_KEY` variable in our `.env` file.
"""

import os
import sys

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

# Load environment variables from .env file
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from browser_use import Agent

llm = ChatAnthropic(model_name='claude-3-7-sonnet-20250219', temperature=0.0, timeout=30, stop=None)

agent = Agent(
	task='Go to amazon.com, search for laptop, sort by best rating, and give me the price of the first result',
	llm=llm,
)


async def main():
	await agent.run(max_steps=10)


asyncio.run(main())
````

## File: examples/models/deepseek-r1.py
````python
import asyncio
import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from pydantic import SecretStr

from browser_use import Agent

# dotenv
load_dotenv()

api_key = os.getenv('DEEPSEEK_API_KEY', '')
if not api_key:
	raise ValueError('DEEPSEEK_API_KEY is not set')


async def run_search():
	agent = Agent(
		task=('go to amazon.com, search for laptop, sort by best rating, and give me the price of the first result'),
		llm=ChatDeepSeek(
			base_url='https://api.deepseek.com/v1',
			model='deepseek-reasoner',
			api_key=SecretStr(api_key),
		),
		use_vision=False,
		max_failures=2,
		max_actions_per_step=1,
	)

	await agent.run()


if __name__ == '__main__':
	asyncio.run(run_search())
````

## File: examples/models/gemini.py
````python
import asyncio
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent, BrowserConfig
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

browser = Browser(
	config=BrowserConfig(
		new_context_config=BrowserContextConfig(
			viewport_expansion=0,
		)
	)
)


async def run_search():
	agent = Agent(
		task='Go to amazon.com, search for laptop, sort by best rating, and give me the price of the first result',
		llm=llm,
		max_actions_per_step=4,
		browser=browser,
	)

	await agent.run(max_steps=25)


if __name__ == '__main__':
	asyncio.run(run_search())
````

## File: examples/models/gpt-4o.py
````python
"""
Simple try of the agent.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from langchain_openai import ChatOpenAI

from browser_use import Agent

llm = ChatOpenAI(model='gpt-4o')
agent = Agent(
	task='Go to amazon.com, search for laptop, sort by best rating, and give me the price of the first result',
	llm=llm,
)


async def main():
	await agent.run(max_steps=10)
	input('Press Enter to continue...')


asyncio.run(main())
````

## File: examples/models/grok.py
````python
import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from browser_use import Agent

# dotenv
load_dotenv()

api_key = os.getenv('GROK_API_KEY', '')
if not api_key:
	raise ValueError('GROK_API_KEY is not set')


async def run_search():
	agent = Agent(
		task=(
			'1. Go to https://www.amazon.com'
			'2. Search for "wireless headphones"'
			'3. Filter by "Highest customer rating"'
			'4. Return the title and price of the first product'
		),
		llm=ChatOpenAI(
			base_url='https://api.x.ai/v1',
			model='grok-3-beta',
			api_key=SecretStr(api_key),
		),
		use_vision=False,
	)

	await agent.run()


if __name__ == '__main__':
	asyncio.run(run_search())
````

## File: examples/models/novita.py
````python
"""
Simple try of the agent.

@dev You need to add NOVITA_API_KEY to your environment variables.
"""

import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from browser_use import Agent

# dotenv
load_dotenv()

api_key = os.getenv('NOVITA_API_KEY', '')
if not api_key:
	raise ValueError('NOVITA_API_KEY is not set')


async def run_search():
	agent = Agent(
		task=(
			'1. Go to https://www.reddit.com/r/LocalLLaMA '
			"2. Search for 'browser use' in the search bar"
			'3. Click on first result'
			'4. Return the first comment'
		),
		llm=ChatOpenAI(
			base_url='https://api.novita.ai/v3/openai',
			model='deepseek/deepseek-v3-0324',
			api_key=SecretStr(api_key),
		),
		use_vision=False,
	)

	await agent.run()


if __name__ == '__main__':
	asyncio.run(run_search())
````

## File: examples/models/qwen.py
````python
import asyncio

from langchain_ollama import ChatOllama

from browser_use import Agent


async def run_search():
	agent = Agent(
		task=(
			"1. Go to https://www.reddit.com/r/LocalLLaMA2. Search for 'browser use' in the search bar3. Click search4. Call done"
		),
		llm=ChatOllama(
			# model='qwen2.5:32b-instruct-q4_K_M',
			# model='qwen2.5:14b',
			model='qwen2.5:latest',
			num_ctx=128000,
		),
		max_actions_per_step=1,
	)

	await agent.run()


if __name__ == '__main__':
	asyncio.run(run_search())
````

## File: examples/models/README.md
````markdown
# Gemini
Detailed video on how to integrate browser-use with Gemini: https://www.youtube.com/watch?v=JluZiWBV_Tc
````

## File: examples/notebook/agent_browsing.ipynb
````
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "id": "ZRGlUb8O4fPV"
   },
   "outputs": [],
   "source": [
    "%pip install -U langgraph langchain_google_genai langchain_community langgraph-checkpoint-postgres  openai langchain_groq"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "id": "cMfPUmHIxqTi"
   },
   "outputs": [],
   "source": [
    "%%capture --no-stderr\n",
    "%pip install --upgrade --quiet  playwright > /dev/null\n",
    "%pip install --upgrade --quiet  lxml browser-use langchain_openai"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "kkZ7jVUOUV7Q"
   },
   "outputs": [],
   "source": [
    "!playwright install"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "-_T1MhnGUl2q"
   },
   "outputs": [],
   "source": [
    "!pip install \"anyio<4\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "yARYirp1UhDR"
   },
   "outputs": [],
   "source": [
    "# This import is required only for jupyter notebooks, since they have their own eventloop\n",
    "import nest_asyncio\n",
    "\n",
    "nest_asyncio.apply()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "id": "jyVP10O_5Qck"
   },
   "outputs": [],
   "source": [
    "from google.colab import userdata\n",
    "from langchain_openai import ChatOpenAI\n",
    "\n",
    "llm = ChatOpenAI(model='gpt-4o-mini', temperature=0, api_key=userdata.get('Open_api_key'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "e9duizdv5cOH",
    "outputId": "a07b1702-d485-4641-c307-601e6ab34b9b"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "AIMessage(content='Hello! How can I assist you today?', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 10, 'prompt_tokens': 8, 'total_tokens': 18, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_bd83329f63', 'finish_reason': 'stop', 'logprobs': None}, id='run-28a9088f-7539-412a-aa80-1663be40e74f-0', usage_metadata={'input_tokens': 8, 'output_tokens': 10, 'total_tokens': 18, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "llm.invoke('hi')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "wS8ouhiVQ2dL",
    "outputId": "653879a8-b3ac-4178-edee-5cd834e3404a"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "🔍  Searched for \"What is Langgraph?\" in Google\n",
      "\n",
      "\n",
      "\n",
      "\n",
      "\n",
      "📄  Extracted page as markdown\n",
      ": ![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac879f622b3cb30dd7_cohere-logos-\n",
      "idbbhgStc3%201.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdacfdbb3072f5258f66_hugging%20face.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdaceb29ce1602beb431_logo.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac5f6f2a8c34e5575b_wblogo.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdade49955197d2a8941_mosaic.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac5092327565075208_aws.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdacb28fe27c7784c797_goggle%20drive.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac325d487977a3398b_milvus.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac6348e83137a80c17_openai.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac0d888384ad7d31f3_redis.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdacf9d2dfca1d2a4c81_google%20cloud.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac76b6b8b79414144f_datastax%20logo.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac15e6989ae752a9b5_notion%20logo.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac485cb9900ddafda3_anthropic-\n",
      "logo.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdade49955197d2a894d_mongodb.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdacaeab9fdc6452063c_supabase.png)\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac879f622b3cb30dd7_cohere-logos-\n",
      "idbbhgStc3%201.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdacfdbb3072f5258f66_hugging%20face.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdaceb29ce1602beb431_logo.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac5f6f2a8c34e5575b_wblogo.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdade49955197d2a8941_mosaic.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac5092327565075208_aws.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdacb28fe27c7784c797_goggle%20drive.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac325d487977a3398b_milvus.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac6348e83137a80c17_openai.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac0d888384ad7d31f3_redis.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdacf9d2dfca1d2a4c81_google%20cloud.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac76b6b8b79414144f_datastax%20logo.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac15e6989ae752a9b5_notion%20logo.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdac485cb9900ddafda3_anthropic-\n",
      "logo.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdade49955197d2a894d_mongodb.png)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c8fdacaeab9fdc6452063c_supabase.png)\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/667b080e4b3ca12dc5d5d439_Langgraph%20UI-2.webp)\n",
      "\n",
      "## Controllable cognitive architecture for any task\n",
      "\n",
      "LangGraph's flexible framework supports diverse control flows – single agent,\n",
      "multi-agent, hierarchical, sequential – and robustly handles realistic,\n",
      "complex scenarios.  \n",
      "  \n",
      "Ensure reliability with easy-to-add moderation and quality loops that prevent\n",
      "agents from veering off course.  \n",
      "  \n",
      "Use LangGraph Platform to templatize your cognitive architecture so that\n",
      "tools, prompts, and models are easily configurable with LangGraph Platform\n",
      "Assistants.\n",
      "\n",
      "[See the docs ](https://langchain-ai.github.io/langgraph/)\n",
      "\n",
      "## Designed for human-agent collaboration\n",
      "\n",
      "With built-in statefulness, LangGraph agents seamlessly collaborate with\n",
      "humans by writing drafts for review and awaiting approval before acting.\n",
      "Easily inspect the agent’s actions and \"time-travel\" to roll back and take a\n",
      "different action to correct course.\n",
      "\n",
      "[Read a conceptual guide ](https://langchain-\n",
      "ai.github.io/langgraph/concepts/agentic_concepts/#human-in-the-loop)\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/667c93d559216bb904fe85a8_gif7%20\\(1\\).gif)\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/667c57f274b66a77e2a26b82_CleanShot2024-06-26at17.08.03-ezgif.com-\n",
      "video-to-gif-converter.gif)\n",
      "\n",
      "## First class streaming support for better UX design\n",
      "\n",
      "Bridge user expectations and agent capabilities with native token-by-token\n",
      "streaming and streaming of intermediate steps, helpful for showing agent\n",
      "reasoning and actions back to the user as they happen. Use LangGraph\n",
      "Platform's API to deliver dynamic and interactive user experiences.\n",
      "\n",
      "[Learn more ](https://langchain-ai.github.io/langgraph/how-tos/streaming-\n",
      "tokens/)\n",
      "\n",
      "## Why choose LangGraph?\n",
      "\n",
      "### Control, moderate, and guide your agent’s actions.\n",
      "\n",
      "Prevent agents from veering off course and ensure reliability with easy-to-add\n",
      "moderation and quality loops. Add human-in-the-loop to steer and approve agent\n",
      "actions.\n",
      "\n",
      "### Expressive and customizable agent and multi-agent workflows.\n",
      "\n",
      "LangGraph’s low level abstractions offer the flexibility needed to create\n",
      "sophisticated agents. Design diverse control flows – single, multi-agent,\n",
      "hierarchical, sequential – all with one framework.\n",
      "\n",
      "### Persisted context for long-term interactions.\n",
      "\n",
      "With its stateful design, LangGraph stores conversation histories and session\n",
      "data to maintain context over time and ensure smooth handoffs in agentic\n",
      "systems.\n",
      "\n",
      "### First-class streaming support for better UX design.\n",
      "\n",
      "Bridge user expectations and agent capabilities with native token-by-token\n",
      "streaming of intermediate steps, helpful for showing agent reasoning and\n",
      "actions back to the user as they happen.\n",
      "\n",
      "## LangGraph Platform:  \n",
      "Deploy & develop agents at scale\n",
      "\n",
      "Craft agent-appropriate UXs using LangGraph Platform's APIs. Quickly deploy\n",
      "and scale your agent with purpose-built infrastructure. Choose from multiple\n",
      "deployment options.\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/67878de387cf10f90c7ad65f_LangGraph---\n",
      "Memory-HQ.gif)\n",
      "\n",
      "## Dynamic APIs for designing agent UXs.\n",
      "\n",
      "Craft personalized experiences with the long-term memory API to recall\n",
      "information across conversation sessions. Expose, update, and rewind your\n",
      "app's state for better user visibility, steering, and interaction. Kick off\n",
      "long-running background jobs for research-style or multi-step work.\n",
      "\n",
      "[See the docs ](https://langchain-ai.github.io/langgraph/how-tos/streaming-\n",
      "tokens/)\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/67879a0dd9100d8e643eb39e_LangGraph%20-%20Fault-\n",
      "tolerant%20scalability.gif)\n",
      "\n",
      "## Fault-tolerant scalability.\n",
      "\n",
      "Handle large workloads gracefully with horizontally-scaling servers, task\n",
      "queues, and built-in persistence. Enhance resilience with intelligent caching\n",
      "and automated retries.\n",
      "\n",
      "[Learn more in the blog ](https://langchain-ai.github.io/langgraph/how-\n",
      "tos/streaming-tokens/)\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/667c93d559216bb904fe85a8_gif7%20\\(1\\).gif)\n",
      "\n",
      "## An end-to-end agent experience.\n",
      "\n",
      "Simplify prototyping, debugging, and sharing of agents in our visual LangGraph\n",
      "Studio. Deploy your application with 1-click deploy with our SaaS offering or\n",
      "within your own VPC. Then, monitor app performance with LangSmith.\n",
      "\n",
      "[Discover LangGraph Studio ](https://langchain-ai.github.io/langgraph/how-\n",
      "tos/streaming-tokens/)\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/66db8c2317fe5b9ad2b84ea0_lcacademylogo.png)\n",
      "\n",
      "## Introduction to LangGraph\n",
      "\n",
      "Learn the basics of LangGraph in this LangChain Academy Course. You'll learn\n",
      "how to build agents that automate real-world tasks with LangGraph\n",
      "orchestration.\n",
      "\n",
      "[Enroll for free](https://academy.langchain.com/courses/intro-to-\n",
      "langgraph)[Book enterprise\n",
      "training](https://airtable.com/appGjCAN6126Jm7K8/pagNAp7niHQzRH8zk/form)\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/6787ae429071ad3575902249_card%201%201.webp)![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/6787ae0bce5c99dd808545ce_card%202.webp)\n",
      "\n",
      "## Deploy agents at scale, monitor carefully, iterate boldly\n",
      "\n",
      "Design agent-driven user experiences with LangGraph Platform's APIs. Quickly\n",
      "deploy and scale your application with infrastructure built for agents. Choose\n",
      "from multiple deployment options.\n",
      "\n",
      "### Fault-tolerant scalability\n",
      "\n",
      "Handle large workloads gracefully with horizontally-scaling servers, task\n",
      "queues, and built-in persistence. Enhance resilience with intelligent caching\n",
      "and automated retries.\n",
      "\n",
      "### Dynamic APIs for designing agent experience\n",
      "\n",
      "Craft personalized user experiences with APIs featuring long-term memory to\n",
      "recall information across conversation sessions. Track, update, and rewind\n",
      "your app's state for easy human steering and interaction. Kick off long-\n",
      "running background jobs for research-style or multi-step work.\n",
      "\n",
      "### Integrated developer experience\n",
      "\n",
      "Simplify prototyping, debugging, and sharing of agents in our visual LangGraph\n",
      "Studio. Deploy your application with 1-click deploy with our SaaS offering or\n",
      "within your own VPC. Then, monitor app performance with LangSmith.\n",
      "\n",
      "### Trusted by companies taking agency in AI innovation:\n",
      "\n",
      "LangGraph helps teams of all sizes, across all industries, from ambitious\n",
      "startups to established enterprises.\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c5308aea1371b447cc4af9_elastic-ar21.png)\n",
      "\n",
      "“LangChain is streets ahead with what they've put forward with LangGraph.\n",
      "LangGraph sets the foundation for how we can build and scale AI workloads —\n",
      "from conversational agents, complex task automation, to custom LLM-backed\n",
      "experiences that 'just work'. The next chapter in building complex production-\n",
      "ready features with LLMs is agentic, and with LangGraph and LangSmith,\n",
      "LangChain delivers an out-of-the-box solution to iterate quickly, debug\n",
      "immediately, and scale effortlessly.”\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/667b26a1b4576291d6a9335b_garrett%20spong%201.webp)\n",
      "\n",
      "Garrett Spong\n",
      "\n",
      "Principal SWE\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/6679de9dc4e7bee218d4b058_Norwegian-Cruise-\n",
      "Line-Logo%202-2.webp)\n",
      "\n",
      "“LangGraph has been instrumental for our AI development. Its robust framework\n",
      "for building stateful, multi-actor applications with LLMs has transformed how\n",
      "we evaluate and optimize the performance of our AI guest-facing solutions.\n",
      "LangGraph enables granular control over the agent's thought process, which has\n",
      "empowered us to make data-driven and deliberate decisions to meet the diverse\n",
      "needs of our guests.”\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/667b265bed5f5a9d26d6b7d6_andres%20torres%201.webp)\n",
      "\n",
      "Andres Torres\n",
      "\n",
      "Sr. Solutions Architect\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/667c6f809f0ebc7b1d72a99b_Replit.png)\n",
      "\n",
      "“It's easy to build the prototype of a coding agent, but deceptively hard to\n",
      "improve its reliability. Replit wants to give a coding agent to millions of\n",
      "users — reliability is our top priority, and will remain so for a long time.\n",
      "LangGraph is giving us the control and ergonomics we need to build and ship\n",
      "powerful coding agents.”\n",
      "\n",
      "“As Ally advances its exploration of Generative AI,\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/667c6fcaaa21bcf2fe006dbe_1690576438641%20\\(1\\)%201.webp)\n",
      "\n",
      "Michele Catasta\n",
      "\n",
      "President\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/6679e1baf7ea357d0763cde1_ally-\n",
      "bank%201-2.png)\n",
      "\n",
      "“As Ally advances its exploration of Generative AI, our tech labs is excited\n",
      "by LangGraph, the new library from LangChain, which is central to our\n",
      "experiments with multi-actor agentic workflows. We are committed to deepening\n",
      "our partnership with LangChain.”\n",
      "\n",
      "“As Ally advances its exploration of Generative AI,\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/6679e2d31352c6bd56c84280_ally.png)\n",
      "\n",
      "Sathish Muthukrishnan\n",
      "\n",
      "Chief Information, Data and Digital Officer\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/65c5308aea1371b447cc4af9_elastic-ar21.png)\n",
      "\n",
      "“LangChain is streets ahead with what they've put forward with LangGraph.\n",
      "LangGraph sets the foundation for how we can build and scale AI workloads —\n",
      "from conversational agents, complex task automation, to custom LLM-backed\n",
      "experiences that 'just work'. The next chapter in building complex production-\n",
      "ready features with LLMs is agentic, and with LangGraph and LangSmith,\n",
      "LangChain delivers an out-of-the-box solution to iterate quickly, debug\n",
      "immediately, and scale effortlessly.”\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/667b26a1b4576291d6a9335b_garrett%20spong%201.webp)\n",
      "\n",
      "Garrett Spong\n",
      "\n",
      "Principal SWE\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/6679de9dc4e7bee218d4b058_Norwegian-Cruise-\n",
      "Line-Logo%202-2.webp)\n",
      "\n",
      "“LangGraph has been instrumental for our AI development. Its robust framework\n",
      "for building stateful, multi-actor applications with LLMs has transformed how\n",
      "we evaluate and optimize the performance of our AI guest-facing solutions.\n",
      "LangGraph enables granular control over the agent's thought process, which has\n",
      "empowered us to make data-driven and deliberate decisions to meet the diverse\n",
      "needs of our guests.”\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/667b265bed5f5a9d26d6b7d6_andres%20torres%201.webp)\n",
      "\n",
      "Andres Torres\n",
      "\n",
      "Sr. Solutions Architect\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/667c6f809f0ebc7b1d72a99b_Replit.png)\n",
      "\n",
      "“It's easy to build the prototype of a coding agent, but deceptively hard to\n",
      "improve its reliability. Replit wants to give a coding agent to millions of\n",
      "users — reliability is our top priority, and will remain so for a long time.\n",
      "LangGraph is giving us the control and ergonomics we need to build and ship\n",
      "powerful coding agents.”\n",
      "\n",
      "“As Ally advances its exploration of Generative AI,\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/667c6fcaaa21bcf2fe006dbe_1690576438641%20\\(1\\)%201.webp)\n",
      "\n",
      "Michele Catasta\n",
      "\n",
      "President\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/6679e1baf7ea357d0763cde1_ally-\n",
      "bank%201-2.png)\n",
      "\n",
      "“As Ally advances its exploration of Generative AI, our tech labs is excited\n",
      "by LangGraph, the new library from LangChain, which is central to our\n",
      "experiments with multi-actor agentic workflows. We are committed to deepening\n",
      "our partnership with LangChain.”\n",
      "\n",
      "“As Ally advances its exploration of Generative AI,\n",
      "\n",
      "![](https://cdn.prod.website-\n",
      "files.com/65b8cd72835ceeacd4449a53/6679e2d31352c6bd56c84280_ally.png)\n",
      "\n",
      "Sathish Muthukrishnan\n",
      "\n",
      "Chief Information, Data and Digital Officer\n",
      "\n",
      "## LangGraph FAQs\n",
      "\n",
      "Do I need to use LangChain to use LangGraph? What’s the difference?\n",
      "\n",
      "No. LangGraph is an orchestration framework for complex agentic systems and is\n",
      "more low-level and controllable than LangChain agents. LangChain provides a\n",
      "standard interface to interact with models and other components, useful for\n",
      "straight-forward chains and retrieval flows.\n",
      "\n",
      "How is LangGraph different from other agent frameworks?\n",
      "\n",
      "Other agentic frameworks can work for simple, generic tasks but fall short for\n",
      "complex tasks bespoke to a company’s needs. LangGraph provides a more\n",
      "expressive framework to handle companies’ unique tasks without restricting\n",
      "users to a single black-box cognitive architecture.\n",
      "\n",
      "Does LangGraph impact the performance of my app?\n",
      "\n",
      "LangGraph will not add any overhead to your code and is specifically designed\n",
      "with streaming workflows in mind.\n",
      "\n",
      "Is LangGraph open source? Is it free?\n",
      "\n",
      "Yes. LangGraph is an MIT-licensed open-source library and is free to use.\n",
      "\n",
      "How are LangGraph and LangGraph Platform different?\n",
      "\n",
      "LangGraph is a stateful, orchestration framework that brings added control to\n",
      "agent workflows. LangGraph Platform is a service for deploying and scaling\n",
      "LangGraph applications, with an opinionated API for building agent UXs, plus\n",
      "an integrated developer studio.\n",
      "\n",
      "LangGraph (open source)\n",
      "\n",
      "LangGraph Platform\n",
      "\n",
      "Features\n",
      "\n",
      "Stateful orchestration framework for agentic applications\n",
      "\n",
      "Scalable infrastructure for deploying LangGraph applications  \n",
      "\n",
      "Python and JavaScript\n",
      "\n",
      "Python and JavaScript  \n",
      "\n",
      "None\n",
      "\n",
      "Yes - useful for retrieving & updating state or long-term memory, or creating\n",
      "a configurable assistant  \n",
      "\n",
      "Basic\n",
      "\n",
      "Dedicated mode for token-by-token messages  \n",
      "\n",
      "Community contributed\n",
      "\n",
      "Supported out-of-the-box  \n",
      "\n",
      "Self-managed\n",
      "\n",
      "Managed Postgres with efficient storage  \n",
      "\n",
      "Self-managed\n",
      "\n",
      "\\- Cloud SaaS  \n",
      "\\- Free self-hosted  \n",
      "\\- Enterprise  \n",
      "(BYOC or paid self-hosted)  \n",
      "\n",
      "Self-managed\n",
      "\n",
      "Auto-scaling of task queues and servers  \n",
      "\n",
      "Self-managed\n",
      "\n",
      "Automated retries  \n",
      "\n",
      "Simple threading\n",
      "\n",
      "Supports double-texting  \n",
      "\n",
      "None\n",
      "\n",
      "Cron scheduling  \n",
      "\n",
      "None\n",
      "\n",
      "Integrated with LangSmith for observability  \n",
      "\n",
      "LangGraph Studio for Desktop\n",
      "\n",
      "LangGraph Studio for Desktop & Cloud  \n",
      "\n",
      "What are my deployment options for LangGraph Platform?\n",
      "\n",
      "We currently have the following deployment options for LangGraph applications:  \n",
      "  \n",
      "‍**Self-Hosted Lite** : A free (up to 1M nodes executed), limited version of\n",
      "LangGraph Platform that you can run locally or in a self-hosted manner. This\n",
      "version requires a LangSmith API key and logs all usage to LangSmith. Fewer\n",
      "features are available than in paid plans.  \n",
      "‍**Cloud SaaS:** Fully managed and hosted as part of LangSmith, with automatic\n",
      "updates and zero maintenance.  \n",
      "‍**Bring Your Own Cloud (BYOC):** Deploy LangGraph Platform within your VPC,\n",
      "provisioned and run as a service. Keep data in your environment while\n",
      "outsourcing the management of the service.  \n",
      "**Self-Hosted Enterprise:** Deploy LangGraph entirely on your own\n",
      "infrastructure.\n",
      "\n",
      "Is LangGraph Platform open source?\n",
      "\n",
      "No. LangGraph Platform is proprietary software.  \n",
      "  \n",
      "There is a free, self-hosted version of LangGraph Platform with access to\n",
      "basic features. The Cloud SaaS deployment option is free while in beta, but\n",
      "will eventually be a paid service. We will always give ample notice before\n",
      "charging for a service and reward our early adopters with preferential\n",
      "pricing. The Bring Your Own Cloud (BYOC) and Self-Hosted Enterprise options\n",
      "are also paid services. [Contact our sales team](/contact-sales) to learn\n",
      "more.  \n",
      "  \n",
      "For more information, see our [LangGraph Platform pricing page](/pricing-\n",
      "langgraph-platform).\n",
      "\n",
      "## Ready to start shipping reliable GenAI apps faster?\n",
      "\n",
      "Get started with LangChain, LangSmith, and LangGraph to enhance your LLM app\n",
      "development, from prototype to production.\n",
      "\n",
      "[Contact Us](/contact-sales)[Sign Up](https://smith.langchain.com/)\n",
      "\n",
      "\n",
      "\n",
      "\n",
      "\n",
      "LangGraph is a flexible framework designed for building and scaling agentic applications. It allows for complex task handling and human-agent collaboration, supporting various control flows such as single-agent, multi-agent, hierarchical, and sequential. Key features include:\n",
      "\n",
      "- **Statefulness**: LangGraph agents maintain context over time, enabling smooth interactions.\n",
      "- **Streaming Support**: It provides native token-by-token streaming for better user experience.\n",
      "- **Moderation and Quality Loops**: These features ensure agents remain reliable and on course.\n",
      "- **Dynamic APIs**: LangGraph offers APIs for crafting personalized user experiences and managing long-term memory.\n",
      "- **Deployment Options**: It supports various deployment methods, including self-hosted and cloud solutions.\n",
      "\n",
      "\n",
      "\n",
      "\n"
     ]
    }
   ],
   "source": [
    "import asyncio\n",
    "\n",
    "from langchain_openai import ChatOpenAI\n",
    "\n",
    "from browser_use import Agent, Browser, BrowserConfig\n",
    "\n",
    "# Basic configuration for the browser\n",
    "config = BrowserConfig(\n",
    "\theadless=True,  # Run in headless mode\n",
    "\t# disable_security=True  # Uncomment if you want to disable security\n",
    ")\n",
    "\n",
    "# Initialize the browser with the specified configuration\n",
    "browser = Browser(config=config)\n",
    "\n",
    "\n",
    "async def main():\n",
    "\t# Initialize the agent with the task and language model\n",
    "\tagent = Agent(\n",
    "\t\ttask='What is Langgraph',\n",
    "\t\tllm=llm,  # Replace with your LLM configuration\n",
    "\t\tbrowser=browser,\n",
    "\t\tgenerate_gif=False,  # Disable GIF generation\n",
    "\t)\n",
    "\n",
    "\t# Run the agent and get results asynchronously\n",
    "\tresult = await agent.run()\n",
    "\n",
    "\t# Process results token-wise\n",
    "\tfor action in result.action_results():\n",
    "\t\tprint(action.extracted_content, end='\\r', flush=True)\n",
    "\t\tprint('\\n\\n')\n",
    "\t\t# if action.is_done:\n",
    "\t\t#     print(action.extracted_content)\n",
    "\n",
    "\t# Close the browser after completion\n",
    "\tawait browser.close()\n",
    "\n",
    "\n",
    "# Run the asynchronous main function\n",
    "asyncio.run(main())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "TFK-fNoLDFcF",
    "outputId": "d78fbeae-c8f0-4c26-e0e3-7a0a683d3fc1"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "AgentHistoryList(all_results=[ActionResult(is_done=False, extracted_content='🔍  Searched for \"What is LangChain?\" in Google', error=None, include_in_memory=True), ActionResult(is_done=False, extracted_content=\"📄  Extracted page as markdown\\n: # Filters and Topics\\n\\n[All](/search?sca_esv=4c6b8dc13bab3e46&q=What+is+LangChain%3F&source=lnms&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWd8nbOJfsBGGB5IQQO6L3JyWp6w6_rxLPe8F8fpm5a55blYtaduielx1say4YCS0EIyvBb6VkaLhDZSOnSC94tp-\\nJuFEDkvqUl_u6quB-Is11hrT6R6Y6jGPIGI0MqGRIdRYfHHK4Fm5f9UNWxYphEnPjChpmH-\\nusjmkJN6Sk444PHRuqJvihdKgoqwGrUjYjqVvmxA&sa=X&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQ0pQJegQIEhAB)\\n\\n[Images](/search?sca_esv=4c6b8dc13bab3e46&q=What+is+LangChain%3F&udm=2&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWd8nbOJfsBGGB5IQQO6L3JyWp6w6_rxLPe8F8fpm5a55blYtaduielx1say4YCS0EIyvBb6VkaLhDZSOnSC94tp-\\nJuFEDkvqUl_u6quB-Is11hrT6R6Y6jGPIGI0MqGRIdRYfHHK4Fm5f9UNWxYphEnPjChpmH-\\nusjmkJN6Sk444PHRuqJvihdKgoqwGrUjYjqVvmxA&sa=X&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQtKgLegQIExAB)\\n\\n[Videos](/search?sca_esv=4c6b8dc13bab3e46&q=What+is+LangChain%3F&udm=7&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWd8nbOJfsBGGB5IQQO6L3JyWp6w6_rxLPe8F8fpm5a55blYtaduielx1say4YCS0EIyvBb6VkaLhDZSOnSC94tp-\\nJuFEDkvqUl_u6quB-Is11hrT6R6Y6jGPIGI0MqGRIdRYfHHK4Fm5f9UNWxYphEnPjChpmH-\\nusjmkJN6Sk444PHRuqJvihdKgoqwGrUjYjqVvmxA&sa=X&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQtKgLegQIERAB)\\n\\n[Forums](/search?sca_esv=4c6b8dc13bab3e46&q=What+is+LangChain%3F&udm=18&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWd8nbOJfsBGGB5IQQO6L3JyWp6w6_rxLPe8F8fpm5a55blYtaduielx1say4YCS0EIyvBb6VkaLhDZSOnSC94tp-\\nJuFEDkvqUl_u6quB-Is11hrT6R6Y6jGPIGI0MqGRIdRYfHHK4Fm5f9UNWxYphEnPjChpmH-\\nusjmkJN6Sk444PHRuqJvihdKgoqwGrUjYjqVvmxA&sa=X&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQs6gLegQIDxAB)\\n\\nWeb\\n\\n[Flights](/travel/flights?sca_esv=4c6b8dc13bab3e46&output=search&q=What+is+LangChain%3F&source=lnms&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWd8nbOJfsBGGB5IQQO6L3JyWp6w6_rxLPe8F8fpm5a55blYtaduielx1say4YCS0EIyvBb6VkaLhDZSOnSC94tp-\\nJuFEDkvqUl_u6quB-Is11hrT6R6Y6jGPIGI0MqGRIdRYfHHK4Fm5f9UNWxYphEnPjChpmH-\\nusjmkJN6Sk444PHRuqJvihdKgoqwGrUjYjqVvmxA&ved=1t:200715&ictx=111)\\n\\n[Finance](/finance?sca_esv=4c6b8dc13bab3e46&output=search&q=What+is+LangChain%3F&source=lnms&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWd8nbOJfsBGGB5IQQO6L3JyWp6w6_rxLPe8F8fpm5a55blYtaduielx1say4YCS0EIyvBb6VkaLhDZSOnSC94tp-\\nJuFEDkvqUl_u6quB-Is11hrT6R6Y6jGPIGI0MqGRIdRYfHHK4Fm5f9UNWxYphEnPjChpmH-\\nusjmkJN6Sk444PHRuqJvihdKgoqwGrUjYjqVvmxA&sa=X&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQ0pQJegQIDBAB)\\n\\nMore\\n\\n[Books](/search?sca_esv=4c6b8dc13bab3e46&q=What+is+LangChain%3F&udm=36&source=lnms&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWd8nbOJfsBGGB5IQQO6L3JyWp6w6_rxLPe8F8fpm5a55blYtaduielx1say4YCS0EIyvBb6VkaLhDZSOnSC94tp-\\nJuFEDkvqUl_u6quB-Is11hrT6R6Y6jGPIGI0MqGRIdRYfHHK4Fm5f9UNWxYphEnPjChpmH-\\nusjmkJN6Sk444PHRuqJvihdKgoqwGrUjYjqVvmxA&sa=X&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQ0pQJegQINxAB)\\n\\n[News](/search?sca_esv=4c6b8dc13bab3e46&q=What+is+LangChain%3F&tbm=nws&source=lnms&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWd8nbOJfsBGGB5IQQO6L3JyWp6w6_rxLPe8F8fpm5a55blYtaduielx1say4YCS0EIyvBb6VkaLhDZSOnSC94tp-\\nJuFEDkvqUl_u6quB-Is11hrT6R6Y6jGPIGI0MqGRIdRYfHHK4Fm5f9UNWxYphEnPjChpmH-\\nusjmkJN6Sk444PHRuqJvihdKgoqwGrUjYjqVvmxA&sa=X&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQ0pQJegQINhAB)\\n\\n[Shopping](/search?sca_esv=4c6b8dc13bab3e46&q=What+is+LangChain%3F&udm=28&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWd8nbOJfsBGGB5IQQO6L3JyWp6w6_rxLPe8F8fpm5a55blYtaduielx1say4YCS0EIyvBb6VkaLhDZSOnSC94tp-\\nJuFEDkvqUl_u6quB-Is11hrT6R6Y6jGPIGI0MqGRIdRYfHHK4Fm5f9UNWxYphEnPjChpmH-\\nusjmkJN6Sk444PHRuqJvihdKgoqwGrUjYjqVvmxA&ved=1t:220175&ictx=111)\\n\\nTools\\n\\nAny time\\n\\nAny time\\n\\n[Past\\nhour](/search?q=What+is+LangChain%3F&sca_esv=4c6b8dc13bab3e46&udm=14&source=lnt&tbs=qdr:h&sa=X&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQpwV6BAgGEAc)\\n\\n[Past 24\\nhours](/search?q=What+is+LangChain%3F&sca_esv=4c6b8dc13bab3e46&udm=14&source=lnt&tbs=qdr:d&sa=X&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQpwV6BAgGEAg)\\n\\n[Past\\nweek](/search?q=What+is+LangChain%3F&sca_esv=4c6b8dc13bab3e46&udm=14&source=lnt&tbs=qdr:w&sa=X&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQpwV6BAgGEAk)\\n\\n[Past\\nmonth](/search?q=What+is+LangChain%3F&sca_esv=4c6b8dc13bab3e46&udm=14&source=lnt&tbs=qdr:m&sa=X&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQpwV6BAgGEAo)\\n\\n[Past\\nyear](/search?q=What+is+LangChain%3F&sca_esv=4c6b8dc13bab3e46&udm=14&source=lnt&tbs=qdr:y&sa=X&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQpwV6BAgGEAs)\\n\\nCustom range...\\n\\nCustom date range\\n\\nFromTo\\n\\nGo\\n\\nAll results\\n\\nAll results\\n\\n[Verbatim](/search?q=What+is+LangChain%3F&sca_esv=4c6b8dc13bab3e46&udm=14&source=lnt&tbs=li:1&sa=X&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQpwV6BAgGEBM)\\n\\n[ Advanced Search\\n](https://www.google.com/advanced_search?q=What+is+LangChain%3F&udm=14)\\n\\nCtrl+Shift+X to select\\n\\n![Google](https://fonts.gstatic.com/s/i/productlogos/googleg/v6/24px.svg)\\n\\n# Search settings\\n\\n[Search CustomizationOff](/history/optout?hl=en)\\n\\n[SafeSearchBlurring\\non](/safesearch?prev=https://www.google.com/search?q%3DWhat%2Bis%2BLangChain?%26udm%3D14&sa=X&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQ8JsIegQIChAH)\\n\\n[LanguageEnglish](/preferences?lang=1&hl=en&prev=https://www.google.com/search?q%3DWhat%2Bis%2BLangChain%253F%26sca_esv%3D4c6b8dc13bab3e46%26udm%3D14#languages)\\n\\n[Dark themeDevice\\ndefault](/setprefs?hl=en&prev=https://www.google.com/search?q%3DWhat%2Bis%2BLangChain?%26udm%3D14%26pccc%3D1&sig=0_jfSkJcafppJyKAIkCWZpHFXzfrs%3D&cs=2&sa=X&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQqsEHegQIChAJ&ictx=1)\\n\\n[More\\nsettings](/preferences?hl=en&prev=https://www.google.com/search?q%3DWhat%2Bis%2BLangChain%253F%26sca_esv%3D4c6b8dc13bab3e46%26udm%3D14)\\n\\nSend feedback\\n\\n[Help](https://support.google.com/websearch/?p=dsrp_search_hc&hl=en) •\\n[Privacy](https://policies.google.com/privacy?hl=en&fg=1) •\\n[Terms](https://policies.google.com/terms?hl=en&fg=1)\\n\\n# Search Results\\n\\n[  \\nLangChain![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAM1BMVEUcPDwRNjYAMC8AKSd2goaZoaapr7T//v/g4ej49/+/xMn8+/8AFRNAVliSm6BUZWfLztSDUJcgAAAAu0lEQVR4AdWRR2JFIQhFLcgF+/5XG54lPZn/M+Qo1b0iPnzBf1LRU/oC+fjuGD/gY4NANUvRSwEUEta/DAXVKtchxSaKbH99gwWaC4Tzrw/NFkTzLvCTDxxiXxbcJlChhYOL85FlRhcTzJEnJ9SxQkuatQpVSkkE3ytBlwy8pdUPA2gCbWxupV0NGRhuVEEnGad483sUgynlScV6Xf/WKHcJhmh5SqEsJ+Hz+iz6Y31n8f0L5ON/J3tB3gAtjgsX/sngiAAAAABJRU5ErkJggg==)LangChainhttps://www.langchain.com](https://www.langchain.com/)\\n\\nLangChain\\n\\nhttps://www.langchain.com\\n\\n _LangChain_ is a composable framework to build with LLMs. LangGraph is the\\norchestration framework for controllable agentic workflows. Run.\\n\\n\\u200e[Docs](https://python.langchain.com/docs/introduction/) ·\\n\\u200e[Products](https://www.langchain.com/langchain) · \\u200e[LangChain\\nAcademy](https://academy.langchain.com/) · \\u200e[Join the LangChain\\nCommunity](https://www.langchain.com/join-community)\\n\\n[  \\nWhat is\\nLangChain?![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAflBMVEUjLz4dKjohLT0NHzFQV2FKUlwAFywnM0IaKDgzPUpWXGUVJDbq6+3i4+X29/jLzc99gogAABubnqP///9yd393fIPY2twAAAAAAB8AACK1t7ujpqsADicAFitiaHGGi5GUmJ1pb3cAFCqJjpQ8RlIuOUZDS1errrEGHC/DxslAWrmhAAAA1UlEQVR4Ad2OhWGFMBBAI0iIlhzuTth/wHqLjPBf5FzQ64Hx10++H8H3GPX8IMQEE8JCGnFC0ImQSps3GVuIE5lCpii6EOQFhFAaHVV1ZvPm1rWSGbSqk3UvvQ70cKlkI8QFUGtMZ3QzxRz4uRPmMBvoFrAlVEVlB4jIpW1S8W6l/SLSjfF93xw6IZPDDCFBvi52Sd2zs+1haSB+OxHhzz2Is3KycKRomtp2mthYyTFr0YlbKwCtTJZp0LWbO4YuEBd09WHMYXlDCWPoAaMuCBzF6BX5AC2JD1u/hbEIAAAAAElFTkSuQmCC)Amazon\\nWeb Serviceshttps://aws.amazon.com › ... › Generative\\nAI](https://aws.amazon.com/what-is/langchain/)\\n\\nAmazon Web Services\\n\\nhttps://aws.amazon.com › ... › Generative AI\\n\\nLangChain _provides AI developers with tools to connect language models with\\nexternal data sources_. It is open-source and supported by an active\\ncommunity.\\n\\n[  \\nWhat Is LangChain and How to Use It: A\\nGuide![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAANlBMVEVHcEwAIkQAIkQAIkQAIkQAIkQAIkQAIkQAIkQAIkQAIkQAIkQAIkQAIkQAIkQAIkQAIkQAIkT2h/2dAAAAEnRSTlMASA176IbPqP9pXzX1LR7fI79igdKzAAAA60lEQVR4Ab2SR2IDMQgAR7BoEYuK///YVHf7msxJojf+g1J4i+hm1Erd3/hsvhVEaCH7wQPh2YAeB4wM7ik+F+uEuacC7c5XMocUCWCYVyHtpjQPSoW278GYFeHGNllCn1W1zjVcaSfOHG7UYBqATSzvlOEFodXzj+V39aivbuzKDz3I4FRuyvCbspCxXG9hDx9xH7Z4nJXdjbRzQdKwxLzftaI+1qzai7FcmdtdRY06B20vsGalud7Gt+WQ6jZgmVdZucnT4DU901NZ08vryo6IA1p6vCx7Wlmr2M/WX8/Ef9hUeEMP1ej8OZ+MHAj3YNWlQgAAAABJRU5ErkJggg==)TechTargethttps://www.techtarget.com\\n› definition ›\\nLangChain](https://www.techtarget.com/searchenterpriseai/definition/LangChain)\\n\\nTechTarget\\n\\nhttps://www.techtarget.com › definition › LangChain\\n\\n _LangChain is an open source framework_ that enables software developers\\nworking with artificial intelligence (AI) and its machine learning subset to\\ncombine ...\\n\\n[  \\nIntroduction | 🦜️ LangChain![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAPFBMVEUdPT1OZGZzg4fT194cPDwUNzf///8dPT0ePj75+P/y8vrAxcw6UlQGMjGSnqMsSEnk5u2Cj5OrtbpgdHaG8/c5AAAACXRSTlPv////////b24kxPwmAAAA1klEQVQokcWS2Y7DIAxFsR3TYhaz/P+/DkvSppFSaR5Gcx+Q4HjjgnludzJPY25hx1/YX0P+0Bkya4CTgm58QFYk+yEqyguyVmfJZ3coZysp8MpM4nKIfV3ypdROZyYD9eCiwe8MPYFYAu4w4kjJLS7qoQdv4gTjgMX2M0mRlSaDFqp1tiw4q5FybCJAhFpH+ITcaPXaQiTpDXGWXz37tGMjtaWSrEesMtvsJoQ6JvKeJI9Lzjr1uCeHdHVoerB7q9DwpAZvb69v8nqW//wmv4bGPO7x4weTRBHU/VcIdwAAAABJRU5ErkJggg==)LangChainhttps://python.langchain.com › docs › introduction](https://python.langchain.com/docs/introduction/)\\n\\nLangChain\\n\\nhttps://python.langchain.com › docs › introduction\\n\\n _LangChain_ is a framework for developing applications powered by large\\nlanguage models (LLMs). LangChain simplifies every stage of the LLM\\napplication lifecycle.\\n\\n\\u200e[Introduction](https://python.langchain.com/v0.1/docs/get_started/introduction/)\\n·\\n\\u200e[Langchain.agents...](https://api.python.langchain.com/en/latest/agents/langchain.agents.tool_calling_agent.base.create_tool_calling_agent.html)\\n· \\u200e[LangChain v0.3](https://python.langchain.com/docs/versions/v0_3/) ·\\n\\u200e[Langchain_core.tools.](https://api.python.langchain.com/en/latest/tools/langchain_core.tools.tool.html)\\n\\n[  \\nWhat Is\\nLangChain?![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAQlBMVEVHcEwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABz07T7AAAAFnRSTlMABWTNoAuOPcGA32tTRXW1FyYt7PT+Xc8YuAAAANZJREFUeAHNx8t1xSAMBcArQCD+AkP/rcYhXiTHKeDNbvC5yFjH5K0hvAWJKZcUJeCtSpFmbJGKN45JmHuKjBdV8AhhMFTxB4Xo5oj2umwc08VAeEBzl0uouqPQnZ4V34ZL0sZlQEw3Jpg1miQ3gLF6YMzNNT4KrwAOfQ1Yj5t4+P3oHC1u3mJNALoVIZsjV9I9AcyFVAB4AVgfDIgDUBKaLSGnCs7SD2mMmlootoGjSDcA+72O7RQwXSQyQGMqbjrHMZV+RviFH/hP20cj/Gd6ET/xwb4A8CUMDSJ3MyIAAAAASUVORK5CYII=)IBMhttps://www.ibm.com\\n› think › topics › langchain](https://www.ibm.com/think/topics/langchain)\\n\\nIBM\\n\\nhttps://www.ibm.com › think › topics › langchain\\n\\nLangChain is essentially _a library of abstractions for Python and Javascript_\\n, representing common steps and concepts necessary to work with language\\nmodels.\\n\\n[  \\nWhat is\\nLangChain?![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAcElEQVR4AWP4//8/RZh6BgCZAkDsAMUNWDFCXgDFACCV8J/B+D8pGKwHRAKRAUyQDEMMQAYEUGBAAsiABpwKHjz4/9/BAZ8BDXgNgIMNGyg04MABkg1AeCEgAK8XKA5EiqORooSELykXEJuUBz43AgAIA1ZhBoG9vwAAAABJRU5ErkJggg==)YouTube\\n· IBM Technology287.6K+ views · 10 months\\nago](https://www.youtube.com/watch?v=1bUy-1hGZpI)\\n\\nYouTube · IBM Technology\\n\\n287.6K+ views · 10 months ago\\n\\nLang chain is _an open-source orchestration framework_ for the development of\\napplications that use large language models.\\n\\n[  \\nWhat is Langchain and why should I care as a\\ndeveloper?![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAQlBMVEVHcEwAAAAAAAAAAAAAAAAAAABxcXGkpKSUlJQeHh5/f3/Q0ND////e3t6rq6taWlrHx8e0tLQsLCw+Pj7u7u62trYTUwO8AAAABnRSTlMAS8D5/5dwkjMFAAAA1klEQVR4AX3TRQLEIAwFUNoGhypz/6vOJ9SFrAIPFyFE03b0iK5tBELSR0j0o89oRPuNrei+sRNUiYJKa20slXAoqBOSDyG4klqkns6oURNLapD2F+x7VA2cjvqOkwWOZfq+oPLTjiN0zh3nibHHGnYcgJpo8cTosIQdZ4pQJIoRpf6MjncTiRFL8H1/oE3YjTEFF972gZR3k2jH/oILL2kfNl2QsBu7Yl7eeEGF8oq8vLSi56NLA+d88D/ofmW5K5vqy5Upj56VqD+T6gOrPs3qo659hz8m8RNl7wTa8QAAAABJRU5ErkJggg==)Medium\\n· Logan Kilpatrick370+ likes · 1 year ago](https://medium.com/around-the-\\nprompt/what-is-langchain-and-why-should-i-care-as-a-developer-b2d952c42b28)\\n\\nMedium · Logan Kilpatrick\\n\\n370+ likes · 1 year ago\\n\\n _Langchain_ makes creating agents using large language models simple through\\ntheir agents API. Developers can use OpenAI functions or other means ...\\n\\n[  \\nLangChain![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAAAnklEQVR4AeTNIQiDQABG4b+u17X1aF6PK3YEO9iMJqPVau82y4FgMezS0oVLhqsHtrcqeqzDXv3CEz/6L4yTtZM3dnHmPTtjzXZAXKYVo4agkU2GI2Lloc6JDez1+flswMu1EQZ3xlE7lK8eKDkjtwE+crBMV+wesKmCiisGGepZIfQJpMj9SNb2MYWrChjVkULuCyCfRvsdmBieyQQAsoDk/9ryhFMAAAAASUVORK5CYII=)Wikipediahttps://en.wikipedia.org\\n› wiki › LangChain](https://en.wikipedia.org/wiki/LangChain)\\n\\nWikipedia\\n\\nhttps://en.wikipedia.org › wiki › LangChain\\n\\nLangChain is a software framework that helps facilitate the integration of\\nlarge language models (LLMs) into applications.\\n\\n\\u200e[History](https://en.wikipedia.org/wiki/LangChain#History) ·\\n\\u200e[Capabilities](https://en.wikipedia.org/wiki/LangChain#Capabilities) ·\\n\\u200e[LangChain tools](https://en.wikipedia.org/wiki/LangChain#LangChain_tools)\\n\\n[  \\nWhat Is LangChain? A Complete Comprehensive\\nOverview![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAMFBMVEX///////////8AAADNzc2/v7+np6eOjo7x8fGenp4mJibe3t5BQUFdXV1oaGh9fX0JTbfNAAAAAnRSTlP8WKsquk8AAAB7SURBVCiR1ZNLDoAgDAWhRSgf8f63lT8GhZULndWjk7ShAcYZTGCcTV2wCxfs76TdMhQLVA5VaiwIAFFzl4eMOCRCJzNdpiawR+mHmRcJrnS1TxKUSaTSTWYE6ia9ipggZUrKoxyvEgbVmbotQWSoZ/vCbr8ll4969R1OiO0IjOTl5agAAAAASUVORK5CYII=)DataStaxhttps://www.datastax.com\\n› guides › what-is-langchain](https://www.datastax.com/guides/what-is-\\nlangchain)\\n\\nDataStax\\n\\nhttps://www.datastax.com › guides › what-is-langchain\\n\\nNov 9, 2023 — LangChain is _a Python framework designed to streamline AI\\napplication development_ , focusing on real-time data processing and\\nintegration with ...\\n\\n[  \\nWhat Is\\nLangChain?![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAABp0lEQVR4AWJwL/ChKx4aFt5K9AFUW5cADYVRGIZxqxRcOu7uVnC33hPuW0+QiHgl4m6ZXnBouP7cDz1czj/X8M53nu26N7I8SICLwmSN0uFFQbKg4TW8h89YBMQwFSINnzUHBHZsKIauCmLFcUHugZGg6RjuK4YuRb729swoEL+SG0rW2TjC43+Y5lEUaG9EnvZ2ngWZf5aNL5/npr7Qe/yI295Af/Xn8RreoxgpSy+IL181xYnbseA32uumeybel4V/pMLQLg+SX4vhL6sugva86InQtVKJDCUQ6S6MBZVBEUpqQJaGB28HpSgDCmOS/MNEAFwUBDZpDMZtPAj/RAKiUQLqXmxYbzzGh+Gyf+mCrY/BJskAikZwgBFbbRYGtatBfhcwLgxnwHYORCUWAMtkYKIavF3027IAuMuAiexG87boIoBGTjXlJs1WhnNhi+TCUA5DdCvVUAz3pXMVInqmTiTN1P4rca6IHjcN7HbwB0TKPzpjMIuA9HT15zICKMEsAgLD7L8gKXGmehBDLQSOGnzGxwYDXBbWCd9Np1KZc1+XOhX4DttSLI3wbnoRAAAAAElFTkSuQmCC)Google\\nCloudhttps://cloud.google.com › use-cases ›\\nlangchain](https://cloud.google.com/use-cases/langchain)\\n\\nGoogle Cloud\\n\\nhttps://cloud.google.com › use-cases › langchain\\n\\n _LangChain_ is a programming language platform that lets developers construct\\nand connect models to access, transform, and share data seamlessly.\\n\\n\\u200e[Langchain And Ai](https://cloud.google.com/use-\\ncases/langchain#:~:text=LangChain%20and%20AI) · \\u200e[How Does Langchain\\nWork?](https://cloud.google.com/use-\\ncases/langchain#:~:text=How%20does%20LangChain%20work%3F) · \\u200e[Key Features Of\\nLangchain](https://cloud.google.com/use-\\ncases/langchain#:~:text=Key%20features%20of%20LangChain)\\n\\n# Page Navigation\\n\\n| 1|\\n[2](/search?q=What+is+LangChain?&sca_esv=4c6b8dc13bab3e46&udm=14&ei=e8iJZ425Mabg0PEP6LmQGQ&start=10&sa=N&sstk=ATObxK4t7c6xZe8J3zQzlUfrNV-\\nBchujCI0GxH83wgy_vu9jEqYrHuTxd0wVBzubCa-bn_k1uK_Zn1BBIfr2yh6eyUzMdvUxFJ-\\nmCw&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQ8tMDegQICBAE)|\\n[3](/search?q=What+is+LangChain?&sca_esv=4c6b8dc13bab3e46&udm=14&ei=e8iJZ425Mabg0PEP6LmQGQ&start=20&sa=N&sstk=ATObxK4t7c6xZe8J3zQzlUfrNV-\\nBchujCI0GxH83wgy_vu9jEqYrHuTxd0wVBzubCa-bn_k1uK_Zn1BBIfr2yh6eyUzMdvUxFJ-\\nmCw&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQ8tMDegQICBAG)|\\n[4](/search?q=What+is+LangChain?&sca_esv=4c6b8dc13bab3e46&udm=14&ei=e8iJZ425Mabg0PEP6LmQGQ&start=30&sa=N&sstk=ATObxK4t7c6xZe8J3zQzlUfrNV-\\nBchujCI0GxH83wgy_vu9jEqYrHuTxd0wVBzubCa-bn_k1uK_Zn1BBIfr2yh6eyUzMdvUxFJ-\\nmCw&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQ8tMDegQICBAI)|\\n[5](/search?q=What+is+LangChain?&sca_esv=4c6b8dc13bab3e46&udm=14&ei=e8iJZ425Mabg0PEP6LmQGQ&start=40&sa=N&sstk=ATObxK4t7c6xZe8J3zQzlUfrNV-\\nBchujCI0GxH83wgy_vu9jEqYrHuTxd0wVBzubCa-bn_k1uK_Zn1BBIfr2yh6eyUzMdvUxFJ-\\nmCw&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQ8tMDegQICBAK)|\\n[6](/search?q=What+is+LangChain?&sca_esv=4c6b8dc13bab3e46&udm=14&ei=e8iJZ425Mabg0PEP6LmQGQ&start=50&sa=N&sstk=ATObxK4t7c6xZe8J3zQzlUfrNV-\\nBchujCI0GxH83wgy_vu9jEqYrHuTxd0wVBzubCa-bn_k1uK_Zn1BBIfr2yh6eyUzMdvUxFJ-\\nmCw&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQ8tMDegQICBAM)|\\n[7](/search?q=What+is+LangChain?&sca_esv=4c6b8dc13bab3e46&udm=14&ei=e8iJZ425Mabg0PEP6LmQGQ&start=60&sa=N&sstk=ATObxK4t7c6xZe8J3zQzlUfrNV-\\nBchujCI0GxH83wgy_vu9jEqYrHuTxd0wVBzubCa-bn_k1uK_Zn1BBIfr2yh6eyUzMdvUxFJ-\\nmCw&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQ8tMDegQICBAO)|\\n[8](/search?q=What+is+LangChain?&sca_esv=4c6b8dc13bab3e46&udm=14&ei=e8iJZ425Mabg0PEP6LmQGQ&start=70&sa=N&sstk=ATObxK4t7c6xZe8J3zQzlUfrNV-\\nBchujCI0GxH83wgy_vu9jEqYrHuTxd0wVBzubCa-bn_k1uK_Zn1BBIfr2yh6eyUzMdvUxFJ-\\nmCw&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQ8tMDegQICBAQ)|\\n[9](/search?q=What+is+LangChain?&sca_esv=4c6b8dc13bab3e46&udm=14&ei=e8iJZ425Mabg0PEP6LmQGQ&start=80&sa=N&sstk=ATObxK4t7c6xZe8J3zQzlUfrNV-\\nBchujCI0GxH83wgy_vu9jEqYrHuTxd0wVBzubCa-bn_k1uK_Zn1BBIfr2yh6eyUzMdvUxFJ-\\nmCw&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQ8tMDegQICBAS)|\\n[10](/search?q=What+is+LangChain?&sca_esv=4c6b8dc13bab3e46&udm=14&ei=e8iJZ425Mabg0PEP6LmQGQ&start=90&sa=N&sstk=ATObxK4t7c6xZe8J3zQzlUfrNV-\\nBchujCI0GxH83wgy_vu9jEqYrHuTxd0wVBzubCa-bn_k1uK_Zn1BBIfr2yh6eyUzMdvUxFJ-\\nmCw&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQ8tMDegQICBAU)|\\n[Next](/search?q=What+is+LangChain?&sca_esv=4c6b8dc13bab3e46&udm=14&ei=e8iJZ425Mabg0PEP6LmQGQ&start=10&sa=N&sstk=ATObxK4t7c6xZe8J3zQzlUfrNV-\\nBchujCI0GxH83wgy_vu9jEqYrHuTxd0wVBzubCa-bn_k1uK_Zn1BBIfr2yh6eyUzMdvUxFJ-\\nmCw&ved=2ahUKEwjN4oy74vuKAxUmMDQIHegcJAMQ8NMDegQICBAW)  \\n---|---|---|---|---|---|---|---|---|---|---|---  \\n  \\n# Footer Links\\n\\nWasco County, Oregon \\\\- From your IP address\\n\\n\\\\-\\n\\nUpdate location\\n\\nCan't update your locationLearn more\\n\\nUpdating location...\\n\\n[Help](https://support.google.com/websearch/?p=ws_results_help&hl=en&fg=1)Send\\nfeedback[Privacy](https://policies.google.com/privacy?hl=en&fg=1)[Terms](https://policies.google.com/terms?hl=en&fg=1)\\n\\n\\n\", error=None, include_in_memory=False), ActionResult(is_done=True, extracted_content='LangChain is a composable framework designed for building applications with large language models (LLMs). It simplifies the integration of language models with external data sources and is open-source, supported by an active community. LangChain provides tools for developers to streamline the application lifecycle of LLMs.', error=None, include_in_memory=False)], all_model_outputs=[{'search_google': {'query': 'What is LangChain?'}}, {'extract_content': {'include_links': True}}, {'done': {'text': 'LangChain is a composable framework designed for building applications with large language models (LLMs). It simplifies the integration of language models with external data sources and is open-source, supported by an active community. LangChain provides tools for developers to streamline the application lifecycle of LLMs.'}}])\n"
     ]
    }
   ],
   "source": [
    "# from browser_use import Agent\n",
    "import asyncio\n",
    "\n",
    "from langchain_openai import ChatOpenAI\n",
    "\n",
    "from browser_use import Browser, BrowserConfig\n",
    "\n",
    "# Basic configuration\n",
    "config = BrowserConfig(\n",
    "\theadless=True,\n",
    "\t# disable_security=True\n",
    ")\n",
    "# Reuse existing browser\n",
    "browser = Browser(config=config)\n",
    "# async def main():\n",
    "agent = Agent(\n",
    "\ttask='what is langchain',\n",
    "\tllm=llm,\n",
    "\tbrowser=browser,\n",
    "\tgenerate_gif=False,  # Browser instance will be reused\n",
    ")\n",
    "\n",
    "result = await agent.run()\n",
    "print(result)\n",
    "# Manually close the browser\n",
    "# asyncio.run(main())\n",
    "await browser.close()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "nKGC936xODry",
    "outputId": "de70d715-c30a-4d5b-9d25-40bd79d410de"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "LangChain is a composable framework designed for building applications with large language models (LLMs). It simplifies the integration of language models with external data sources and is open-source, supported by an active community. LangChain provides tools for developers to streamline the application lifecycle of LLMs.\n"
     ]
    }
   ],
   "source": [
    "# display(result.action_results())\n",
    "for action in result.action_results():\n",
    "\tif action.is_done:\n",
    "\t\tprint(action.extracted_content)"
   ]
  }
 ],
 "metadata": {
  "colab": {
   "provenance": []
  },
  "kernelspec": {
   "display_name": "Python 3",
   "name": "python3"
  },
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}
````

## File: examples/simple.py
````python
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent

load_dotenv()

# Initialize the model
llm = ChatOpenAI(
	model='gpt-4o',
	temperature=0.0,
)
task = 'Go to wikipedia.com and search for deepseek'

agent = Agent(task=task, llm=llm)


async def main():
	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/ui/command_line.py
````python
"""
To Use It:

Example 1: Using OpenAI (default), with default task: 'go to reddit and search for posts about browser-use'
python command_line.py

Example 2: Using OpenAI with a Custom Query
python command_line.py --query "go to google and search for browser-use"

Example 3: Using Anthropic's Claude Model with a Custom Query
python command_line.py --query "find latest Python tutorials on Medium" --provider anthropic

"""

import argparse
import asyncio
import os
import sys

# Ensure local repository (browser_use) is accessible
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.controller.service import Controller

load_dotenv()


def get_llm(provider: str):
	if provider == 'anthropic':
		from langchain_anthropic import ChatAnthropic

		api_key = os.getenv('ANTHROPIC_API_KEY')
		if not api_key:
			raise ValueError('Error: ANTHROPIC_API_KEY is not set. Please provide a valid API key.')

		return ChatAnthropic(model_name='claude-3-5-sonnet-20240620', timeout=25, stop=None, temperature=0.0)
	elif provider == 'openai':
		from langchain_openai import ChatOpenAI

		api_key = os.getenv('OPENAI_API_KEY')
		if not api_key:
			raise ValueError('Error: OPENAI_API_KEY is not set. Please provide a valid API key.')

		return ChatOpenAI(model='gpt-4o', temperature=0.0)

	else:
		raise ValueError(f'Unsupported provider: {provider}')


def parse_arguments():
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(description='Automate browser tasks using an LLM agent.')
	parser.add_argument(
		'--query', type=str, help='The query to process', default='go to reddit and search for posts about browser-use'
	)
	parser.add_argument(
		'--provider',
		type=str,
		choices=['openai', 'anthropic'],
		default='openai',
		help='The model provider to use (default: openai)',
	)
	return parser.parse_args()


def initialize_agent(query: str, provider: str):
	"""Initialize the browser agent with the given query and provider."""
	llm = get_llm(provider)
	controller = Controller()
	browser = Browser(config=BrowserConfig())

	return Agent(
		task=query,
		llm=llm,
		controller=controller,
		browser=browser,
		use_vision=True,
		max_actions_per_step=1,
	), browser


async def main():
	"""Main async function to run the agent."""
	args = parse_arguments()
	agent, browser = initialize_agent(args.query, args.provider)

	await agent.run(max_steps=25)

	input('Press Enter to close the browser...')
	await browser.close()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/ui/gradio_demo.py
````python
import asyncio
import os
from dataclasses import dataclass
from typing import List, Optional

# Third-party imports
import gradio as gr
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Local module imports
from browser_use import Agent

load_dotenv()


@dataclass
class ActionResult:
	is_done: bool
	extracted_content: Optional[str]
	error: Optional[str]
	include_in_memory: bool


@dataclass
class AgentHistoryList:
	all_results: List[ActionResult]
	all_model_outputs: List[dict]


def parse_agent_history(history_str: str) -> None:
	console = Console()

	# Split the content into sections based on ActionResult entries
	sections = history_str.split('ActionResult(')

	for i, section in enumerate(sections[1:], 1):  # Skip first empty section
		# Extract relevant information
		content = ''
		if 'extracted_content=' in section:
			content = section.split('extracted_content=')[1].split(',')[0].strip("'")

		if content:
			header = Text(f'Step {i}', style='bold blue')
			panel = Panel(content, title=header, border_style='blue')
			console.print(panel)
			console.print()


async def run_browser_task(
	task: str,
	api_key: str,
	model: str = 'gpt-4o',
	headless: bool = True,
) -> str:
	if not api_key.strip():
		return 'Please provide an API key'

	os.environ['OPENAI_API_KEY'] = api_key

	try:
		agent = Agent(
			task=task,
			llm=ChatOpenAI(model='gpt-4o'),
		)
		result = await agent.run()
		#  TODO: The result cloud be parsed better
		return result
	except Exception as e:
		return f'Error: {str(e)}'


def create_ui():
	with gr.Blocks(title='Browser Use GUI') as interface:
		gr.Markdown('# Browser Use Task Automation')

		with gr.Row():
			with gr.Column():
				api_key = gr.Textbox(label='OpenAI API Key', placeholder='sk-...', type='password')
				task = gr.Textbox(
					label='Task Description',
					placeholder='E.g., Find flights from New York to London for next week',
					lines=3,
				)
				model = gr.Dropdown(choices=['gpt-4', 'gpt-3.5-turbo'], label='Model', value='gpt-4')
				headless = gr.Checkbox(label='Run Headless', value=True)
				submit_btn = gr.Button('Run Task')

			with gr.Column():
				output = gr.Textbox(label='Output', lines=10, interactive=False)

		submit_btn.click(
			fn=lambda *args: asyncio.run(run_browser_task(*args)),
			inputs=[task, api_key, model, headless],
			outputs=output,
		)

	return interface


if __name__ == '__main__':
	demo = create_ui()
	demo.launch()
````

## File: examples/ui/README.md
````markdown
# **User Interfaces of Browser-Use**

| **File Name**          | **User Interface** | **Description**                           | **Example Usage**                         |
|------------------------|-------------------|-------------------------------------------|-------------------------------------------|
| `command_line.py`      | **Terminal**      | Parses arguments for command-line execution. | `python command_line.py`                  |
| `gradio_demo.py`       | **Gradio**        | Provides a Gradio-based interactive UI.  | `python gradio_demo.py`                   |
| `streamlit_demo.py`    | **Streamlit**     | Runs a Streamlit-based web interface.    | `python -m streamlit run streamlit_demo.py` |
````

## File: examples/ui/streamlit_demo.py
````python
"""
To use it, you'll need to install streamlit, and run with:

python -m streamlit run streamlit_demo.py

"""

import asyncio
import os
import sys

import streamlit as st
from dotenv import load_dotenv

# Ensure local repository (browser_use) is accessible
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.controller.service import Controller

# Load environment variables
load_dotenv()

if os.name == 'nt':
	asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


# Function to get the LLM based on provider
def get_llm(provider: str):
	if provider == 'anthropic':
		from langchain_anthropic import ChatAnthropic

		api_key = os.getenv('ANTHROPIC_API_KEY')
		if not api_key:
			st.error('Error: ANTHROPIC_API_KEY is not set. Please provide a valid API key.')
			st.stop()

		return ChatAnthropic(model_name='claude-3-5-sonnet-20240620', timeout=25, stop=None, temperature=0.0)
	elif provider == 'openai':
		from langchain_openai import ChatOpenAI

		api_key = os.getenv('OPENAI_API_KEY')
		if not api_key:
			st.error('Error: OPENAI_API_KEY is not set. Please provide a valid API key.')
			st.stop()

		return ChatOpenAI(model='gpt-4o', temperature=0.0)
	else:
		st.error(f'Unsupported provider: {provider}')
		st.stop()


# Function to initialize the agent
def initialize_agent(query: str, provider: str):
	llm = get_llm(provider)
	controller = Controller()
	browser = Browser(config=BrowserConfig())

	return Agent(
		task=query,
		llm=llm,
		controller=controller,
		browser=browser,
		use_vision=True,
		max_actions_per_step=1,
	), browser


# Streamlit UI
st.title('Automated Browser Agent with LLMs 🤖')

query = st.text_input('Enter your query:', 'go to reddit and search for posts about browser-use')
provider = st.radio('Select LLM Provider:', ['openai', 'anthropic'], index=0)

if st.button('Run Agent'):
	st.write('Initializing agent...')
	agent, browser = initialize_agent(query, provider)

	async def run_agent():
		with st.spinner('Running automation...'):
			await agent.run(max_steps=25)
		st.success('Task completed! 🎉')

	asyncio.run(run_agent())

	st.button('Close Browser', on_click=lambda: asyncio.run(browser.close()))
````

## File: examples/use-cases/captcha.py
````python
"""
Goal: Automates CAPTCHA solving on a demo website.


Simple try of the agent.
@dev You need to add OPENAI_API_KEY to your environment variables.
NOTE: captchas are hard. For this example it works. But e.g. for iframes it does not.
for this example it helps to zoom in.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent

# Load environment variables
load_dotenv()
if not os.getenv('OPENAI_API_KEY'):
	raise ValueError('OPENAI_API_KEY is not set. Please add it to your environment variables.')


async def main():
	llm = ChatOpenAI(model='gpt-4o')
	agent = Agent(
		task='go to https://captcha.com/demos/features/captcha-demo.aspx and solve the captcha',
		llm=llm,
	)
	await agent.run()
	input('Press Enter to exit')


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/use-cases/check_appointment.py
````python
# Goal: Checks for available visa appointment slots on the Greece MFA website.

import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr

from browser_use.agent.service import Agent
from browser_use.controller.service import Controller

# Load environment variables
load_dotenv()
if not os.getenv('OPENAI_API_KEY'):
	raise ValueError('OPENAI_API_KEY is not set. Please add it to your environment variables.')

controller = Controller()


class WebpageInfo(BaseModel):
	"""Model for webpage link."""

	link: str = 'https://appointment.mfa.gr/en/reservations/aero/ireland-grcon-dub/'


@controller.action('Go to the webpage', param_model=WebpageInfo)
def go_to_webpage(webpage_info: WebpageInfo):
	"""Returns the webpage link."""
	return webpage_info.link


async def main():
	"""Main function to execute the agent task."""
	task = (
		'Go to the Greece MFA webpage via the link I provided you.'
		'Check the visa appointment dates. If there is no available date in this month, check the next month.'
		'If there is no available date in both months, tell me there is no available date.'
	)

	model = ChatOpenAI(model='gpt-4o-mini', api_key=SecretStr(os.getenv('OPENAI_API_KEY', '')))
	agent = Agent(task, model, controller=controller, use_vision=True)

	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/use-cases/find_and_apply_to_jobs.py
````python
"""
Goal: Searches for job listings, evaluates relevance based on a CV, and applies

@dev You need to add OPENAI_API_KEY to your environment variables.
Also you have to install PyPDF2 to read pdf files: pip install PyPDF2
"""

import asyncio
import csv
import logging
import os
import sys
from pathlib import Path
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, SecretStr
from PyPDF2 import PdfReader

from browser_use import ActionResult, Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

# Validate required environment variables
load_dotenv()
required_env_vars = ['AZURE_OPENAI_KEY', 'AZURE_OPENAI_ENDPOINT']
for var in required_env_vars:
	if not os.getenv(var):
		raise ValueError(f'{var} is not set. Please add it to your environment variables.')

logger = logging.getLogger(__name__)
# full screen mode
controller = Controller()

# NOTE: This is the path to your cv file
CV = Path.cwd() / 'cv_04_24.pdf'

if not CV.exists():
	raise FileNotFoundError(f'You need to set the path to your cv file in the CV variable. CV file not found at {CV}')


class Job(BaseModel):
	title: str
	link: str
	company: str
	fit_score: float
	location: Optional[str] = None
	salary: Optional[str] = None


@controller.action('Save jobs to file - with a score how well it fits to my profile', param_model=Job)
def save_jobs(job: Job):
	with open('jobs.csv', 'a', newline='') as f:
		writer = csv.writer(f)
		writer.writerow([job.title, job.company, job.link, job.salary, job.location])

	return 'Saved job to file'


@controller.action('Read jobs from file')
def read_jobs():
	with open('jobs.csv', 'r') as f:
		return f.read()


@controller.action('Read my cv for context to fill forms')
def read_cv():
	pdf = PdfReader(CV)
	text = ''
	for page in pdf.pages:
		text += page.extract_text() or ''
	logger.info(f'Read cv with {len(text)} characters')
	return ActionResult(extracted_content=text, include_in_memory=True)


@controller.action(
	'Upload cv to element - call this function to upload if element is not found, try with different index of the same upload element',
)
async def upload_cv(index: int, browser: BrowserContext):
	path = str(CV.absolute())
	dom_el = await browser.get_dom_element_by_index(index)

	if dom_el is None:
		return ActionResult(error=f'No element found at index {index}')

	file_upload_dom_el = dom_el.get_file_upload_element()

	if file_upload_dom_el is None:
		logger.info(f'No file upload element found at index {index}')
		return ActionResult(error=f'No file upload element found at index {index}')

	file_upload_el = await browser.get_locate_element(file_upload_dom_el)

	if file_upload_el is None:
		logger.info(f'No file upload element found at index {index}')
		return ActionResult(error=f'No file upload element found at index {index}')

	try:
		await file_upload_el.set_input_files(path)
		msg = f'Successfully uploaded file "{path}" to index {index}'
		logger.info(msg)
		return ActionResult(extracted_content=msg)
	except Exception as e:
		logger.debug(f'Error in set_input_files: {str(e)}')
		return ActionResult(error=f'Failed to upload file to index {index}')


browser = Browser(
	config=BrowserConfig(
		browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
		disable_security=True,
	)
)


async def main():
	# ground_task = (
	# 	'You are a professional job finder. '
	# 	'1. Read my cv with read_cv'
	# 	'2. Read the saved jobs file '
	# 	'3. start applying to the first link of Amazon '
	# 	'You can navigate through pages e.g. by scrolling '
	# 	'Make sure to be on the english version of the page'
	# )
	ground_task = (
		'You are a professional job finder. '
		'1. Read my cv with read_cv'
		'find ml internships in and save them to a file'
		'search at company:'
	)
	tasks = [
		ground_task + '\n' + 'Google',
		# ground_task + '\n' + 'Amazon',
		# ground_task + '\n' + 'Apple',
		# ground_task + '\n' + 'Microsoft',
		# ground_task
		# + '\n'
		# + 'go to https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/Taiwan%2C-Remote/Fulfillment-Analyst---New-College-Graduate-2025_JR1988949/apply/autofillWithResume?workerSubType=0c40f6bd1d8f10adf6dae42e46d44a17&workerSubType=ab40a98049581037a3ada55b087049b7 NVIDIA',
		# ground_task + '\n' + 'Meta',
	]
	model = AzureChatOpenAI(
		model='gpt-4o',
		api_version='2024-10-21',
		azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
		api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', '')),
	)

	agents = []
	for task in tasks:
		agent = Agent(task=task, llm=model, controller=controller, browser=browser)
		agents.append(agent)

	await asyncio.gather(*[agent.run() for agent in agents])


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/use-cases/find_influencer_profiles.py
````python
"""
Show how to use custom outputs.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import json
import os
import sys
from typing import List

import httpx

from browser_use.agent.views import ActionResult

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from browser_use import Agent, Controller

load_dotenv()


class Profile(BaseModel):
	platform: str
	profile_url: str


class Profiles(BaseModel):
	profiles: List[Profile]


controller = Controller(exclude_actions=['search_google'], output_model=Profiles)
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

if not BEARER_TOKEN:
	# use the api key for ask tessa
	# you can also use other apis like exa, xAI, perplexity, etc.
	raise ValueError('BEARER_TOKEN is not set - go to https://www.heytessa.ai/ and create an api key')


@controller.registry.action('Search the web for a specific query')
async def search_web(query: str):
	keys_to_use = ['url', 'title', 'content', 'author', 'score']
	headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
	async with httpx.AsyncClient() as client:
		response = await client.post(
			'https://asktessa.ai/api/search',
			headers=headers,
			json={'query': query},
		)

	final_results = [
		{key: source[key] for key in keys_to_use if key in source}
		for source in await response.json()['sources']
		if source['score'] >= 0.2
	]
	# print(json.dumps(final_results, indent=4))
	result_text = json.dumps(final_results, indent=4)
	print(result_text)
	return ActionResult(extracted_content=result_text, include_in_memory=True)


async def main():
	task = (
		'Go to this tiktok video url, open it and extract the @username from the resulting url. Then do a websearch for this username to find all his social media profiles. Return me the links to the social media profiles with the platform name.'
		' https://www.tiktokv.com/share/video/7470981717659110678/  '
	)
	model = ChatOpenAI(model='gpt-4o')
	agent = Agent(task=task, llm=model, controller=controller)

	history = await agent.run()

	result = history.final_result()
	if result:
		parsed: Profiles = Profiles.model_validate_json(result)

		for profile in parsed.profiles:
			print('\n--------------------------------')
			print(f'Platform:         {profile.platform}')
			print(f'Profile URL:      {profile.profile_url}')

	else:
		print('No result')


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/use-cases/google_sheets.py
````python
import os
import sys

from browser_use.browser.context import BrowserContext

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

import pyperclip
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import ActionResult, Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig

browser = Browser(
	config=BrowserConfig(
		browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
	),
)

# Load environment variables
load_dotenv()
if not os.getenv('OPENAI_API_KEY'):
	raise ValueError('OPENAI_API_KEY is not set. Please add it to your environment variables.')


controller = Controller()


def is_google_sheet(page) -> bool:
	return page.url.startswith('https://docs.google.com/spreadsheets/')


@controller.registry.action('Google Sheets: Open a specific Google Sheet')
async def open_google_sheet(browser: BrowserContext, google_sheet_url: str):
	page = await browser.get_current_page()
	if page.url != google_sheet_url:
		await page.goto(google_sheet_url)
		await page.wait_for_load_state()
	if not is_google_sheet(page):
		return ActionResult(error='Failed to open Google Sheet, are you sure you have permissions to access this sheet?')
	return ActionResult(extracted_content=f'Opened Google Sheet {google_sheet_url}', include_in_memory=False)


@controller.registry.action('Google Sheets: Get the contents of the entire sheet', page_filter=is_google_sheet)
async def get_sheet_contents(browser: BrowserContext):
	page = await browser.get_current_page()

	# select all cells
	await page.keyboard.press('Enter')
	await page.keyboard.press('Escape')
	await page.keyboard.press('ControlOrMeta+A')
	await page.keyboard.press('ControlOrMeta+C')

	extracted_tsv = pyperclip.paste()
	return ActionResult(extracted_content=extracted_tsv, include_in_memory=True)


@controller.registry.action('Google Sheets: Select a specific cell or range of cells', page_filter=is_google_sheet)
async def select_cell_or_range(browser: BrowserContext, cell_or_range: str):
	page = await browser.get_current_page()

	await page.keyboard.press('Enter')  # make sure we dont delete current cell contents if we were last editing
	await page.keyboard.press('Escape')  # to clear current focus (otherwise select range popup is additive)
	await asyncio.sleep(0.1)
	await page.keyboard.press('Home')  # move cursor to the top left of the sheet first
	await page.keyboard.press('ArrowUp')
	await asyncio.sleep(0.1)
	await page.keyboard.press('Control+G')  # open the goto range popup
	await asyncio.sleep(0.2)
	await page.keyboard.type(cell_or_range, delay=0.05)
	await asyncio.sleep(0.2)
	await page.keyboard.press('Enter')
	await asyncio.sleep(0.2)
	await page.keyboard.press('Escape')  # to make sure the popup still closes in the case where the jump failed
	return ActionResult(extracted_content=f'Selected cell {cell_or_range}', include_in_memory=False)


@controller.registry.action('Google Sheets: Get the contents of a specific cell or range of cells', page_filter=is_google_sheet)
async def get_range_contents(browser: BrowserContext, cell_or_range: str):
	page = await browser.get_current_page()

	await select_cell_or_range(browser, cell_or_range)

	await page.keyboard.press('ControlOrMeta+C')
	await asyncio.sleep(0.1)
	extracted_tsv = pyperclip.paste()
	return ActionResult(extracted_content=extracted_tsv, include_in_memory=True)


@controller.registry.action('Google Sheets: Clear the currently selected cells', page_filter=is_google_sheet)
async def clear_selected_range(browser: BrowserContext):
	page = await browser.get_current_page()

	await page.keyboard.press('Backspace')
	return ActionResult(extracted_content='Cleared selected range', include_in_memory=False)


@controller.registry.action('Google Sheets: Input text into the currently selected cell', page_filter=is_google_sheet)
async def input_selected_cell_text(browser: BrowserContext, text: str):
	page = await browser.get_current_page()

	await page.keyboard.type(text, delay=0.1)
	await page.keyboard.press('Enter')  # make sure to commit the input so it doesn't get overwritten by the next action
	await page.keyboard.press('ArrowUp')
	return ActionResult(extracted_content=f'Inputted text {text}', include_in_memory=False)


@controller.registry.action('Google Sheets: Batch update a range of cells', page_filter=is_google_sheet)
async def update_range_contents(browser: BrowserContext, range: str, new_contents_tsv: str):
	page = await browser.get_current_page()

	await select_cell_or_range(browser, range)

	# simulate paste event from clipboard with TSV content
	await page.evaluate(f"""
		const clipboardData = new DataTransfer();
		clipboardData.setData('text/plain', `{new_contents_tsv}`);
		document.activeElement.dispatchEvent(new ClipboardEvent('paste', {{clipboardData}}));
	""")

	return ActionResult(extracted_content=f'Updated cell {range} with {new_contents_tsv}', include_in_memory=False)


# many more snippets for keyboard-shortcut based Google Sheets automation can be found here, see:
# - https://github.com/philc/sheetkeys/blob/master/content_scripts/sheet_actions.js
# - https://github.com/philc/sheetkeys/blob/master/content_scripts/commands.js
# - https://support.google.com/docs/answer/181110?hl=en&co=GENIE.Platform%3DDesktop#zippy=%2Cmac-shortcuts

# Tip: LLM is bad at spatial reasoning, don't make it navigate with arrow keys relative to current cell
# if given arrow keys, it will try to jump from G1 to A2 by pressing Down, without realizing needs to go Down+LeftLeftLeftLeft


async def main():
	async with await browser.new_context() as context:
		model = ChatOpenAI(model='gpt-4o')

		eraser = Agent(
			task="""
				Clear all the existing values in columns A through F in this Google Sheet:
				https://docs.google.com/spreadsheets/d/1INaIcfpYXlMRWO__de61SHFCaqt1lfHlcvtXZPItlpI/edit
			""",
			llm=model,
			browser_context=context,
			controller=controller,
		)
		await eraser.run()

		researcher = Agent(
			task="""
				Google to find the full name, nationality, and date of birth of the CEO of the top 10 Fortune 100 companies.
				For each company, append a row to this existing Google Sheet: https://docs.google.com/spreadsheets/d/1INaIcfpYXlMRWO__de61SHFCaqt1lfHlcvtXZPItlpI/edit
				Make sure column headers are present and all existing values in the sheet are formatted correctly.
				Columns:
					A: Company Name
					B: CEO Full Name
					C: CEO Country of Birth
					D: CEO Date of Birth (YYYY-MM-DD)
					E: Source URL where the information was found
			""",
			llm=model,
			browser_context=context,
			controller=controller,
		)
		await researcher.run()

		improvised_continuer = Agent(
			task="""
				Read the Google Sheet https://docs.google.com/spreadsheets/d/1INaIcfpYXlMRWO__de61SHFCaqt1lfHlcvtXZPItlpI/edit
				Add 3 more rows to the bottom continuing the existing pattern, make sure any data you add is sourced correctly.
			""",
			llm=model,
			browser_context=context,
			controller=controller,
		)
		await improvised_continuer.run()

		final_fact_checker = Agent(
			task="""
				Read the Google Sheet https://docs.google.com/spreadsheets/d/1INaIcfpYXlMRWO__de61SHFCaqt1lfHlcvtXZPItlpI/edit
				Fact-check every entry, add a new column F with your findings for each row.
				Make sure to check the source URL for each row, and make sure the information is correct.
			""",
			llm=model,
			browser_context=context,
			controller=controller,
		)
		await final_fact_checker.run()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/use-cases/online_coding_agent.py
````python
# Goal: Implements a multi-agent system for online code editors, with separate agents for coding and execution.

import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent, Browser

# Load environment variables
load_dotenv()
if not os.getenv('OPENAI_API_KEY'):
	raise ValueError('OPENAI_API_KEY is not set. Please add it to your environment variables.')


async def main():
	browser = Browser()
	async with await browser.new_context() as context:
		model = ChatOpenAI(model='gpt-4o')

		# Initialize browser agent
		agent1 = Agent(
			task='Open an online code editor programiz.',
			llm=model,
			browser_context=context,
		)
		executor = Agent(
			task='Executor. Execute the code written by the coder and suggest some updates if there are errors.',
			llm=model,
			browser_context=context,
		)

		coder = Agent(
			task='Coder. Your job is to write and complete code. You are an expert coder. Code a simple calculator. Write the code on the coding interface after agent1 has opened the link.',
			llm=model,
			browser_context=context,
		)
		await agent1.run()
		await executor.run()
		await coder.run()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/use-cases/post-twitter.py
````python
"""
Goal: Provides a template for automated posting on X (Twitter), including new tweets, tagging, and replies.

X Posting Template using browser-use
----------------------------------------

This template allows you to automate posting on X using browser-use.
It supports:
- Posting new tweets
- Tagging users
- Replying to tweets

Add your target user and message in the config section.

target_user="XXXXX"
message="XXXXX"
reply_url="XXXXX"

Any issues, contact me on X @defichemist95
"""

import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataclasses import dataclass

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig

# Load environment variables
load_dotenv()
if not os.getenv('OPENAI_API_KEY'):
	raise ValueError('OPENAI_API_KEY is not set. Please add it to your environment variables.')


# ============ Configuration Section ============
@dataclass
class TwitterConfig:
	"""Configuration for Twitter posting"""

	openai_api_key: str
	chrome_path: str
	target_user: str  # Twitter handle without @
	message: str
	reply_url: str
	headless: bool = False
	model: str = 'gpt-4o-mini'
	base_url: str = 'https://x.com/home'


# Customize these settings
config = TwitterConfig(
	openai_api_key=os.getenv('OPENAI_API_KEY'),
	chrome_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # This is for MacOS (Chrome)
	target_user='XXXXX',
	message='XXXXX',
	reply_url='XXXXX',
	headless=False,
)


def create_twitter_agent(config: TwitterConfig) -> Agent:
	llm = ChatOpenAI(model=config.model, api_key=config.openai_api_key)

	browser = Browser(
		config=BrowserConfig(
			headless=config.headless,
			browser_binary_path=config.chrome_path,
		)
	)

	controller = Controller()

	# Construct the full message with tag
	full_message = f'@{config.target_user} {config.message}'

	# Create the agent with detailed instructions
	return Agent(
		task=f"""Navigate to Twitter and create a post and reply to a tweet.

        Here are the specific steps:

        1. Go to {config.base_url}. See the text input field at the top of the page that says "What's happening?"
        2. Look for the text input field at the top of the page that says "What's happening?"
        3. Click the input field and type exactly this message:
        "{full_message}"
        4. Find and click the "Post" button (look for attributes: 'button' and 'data-testid="tweetButton"')
        5. Do not click on the '+' button which will add another tweet.

        6. Navigate to {config.reply_url}
        7. Before replying, understand the context of the tweet by scrolling down and reading the comments.
        8. Reply to the tweet under 50 characters.

        Important:
        - Wait for each element to load before interacting
        - Make sure the message is typed exactly as shown
        - Verify the post button is clickable before clicking
        - Do not click on the '+' button which will add another tweet
        """,
		llm=llm,
		controller=controller,
		browser=browser,
	)


async def post_tweet(agent: Agent):
	try:
		await agent.run(max_steps=100)
		agent.create_history_gif()
		print('Tweet posted successfully!')
	except Exception as e:
		print(f'Error posting tweet: {str(e)}')


async def main():
	agent = create_twitter_agent(config)
	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/use-cases/README.md
````markdown
# Use Cases of Browser-Use

| File Name | Description |
|-----------|------------|
| `captcha.py` | Automates CAPTCHA solving on a demo website. |
| `check_appointment.py` | Checks for available visa appointment slots on the Greece MFA website. |
| `find_and_apply_to_jobs.py` | Searches for job listings, evaluates relevance based on a CV, and applies automatically. |
| `online_coding_agent.py` | Implements a multi-agent system for online code editors, with separate agents for coding and execution. |
| `post-twitter.py` | Provides a template for automated posting on X (Twitter), including new tweets, tagging, and replies. |
| `scrolling_page.py` | Automates webpage scrolling with various scrolling actions and text search functionality. |
| `twitter_post_using_cookies.py` | Automates posting on X (Twitter) using stored authentication cookies. |
| `web_voyager_agent.py` | A general-purpose web navigation agent for tasks like flight booking and course searching. |
````

## File: examples/use-cases/scrolling_page.py
````python
# Goal: Automates webpage scrolling with various scrolling actions and text search functionality.

import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig

# Load environment variables
load_dotenv()
if not os.getenv('OPENAI_API_KEY'):
	raise ValueError('OPENAI_API_KEY is not set')

"""
Example: Using the 'Scroll down' action.

This script demonstrates how the agent can navigate to a webpage and scroll down the content.
If no amount is specified, the agent will scroll down by one page height.
"""

llm = ChatOpenAI(model='gpt-4o')

agent = Agent(
	# task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and scroll down by one page - then scroll up by 100 pixels - then scroll down by 100 pixels - then scroll down by 10000 pixels.",
	task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and scroll to the string 'The vast majority of computer'",
	llm=llm,
	browser=Browser(config=BrowserConfig(headless=False)),
)


async def main():
	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/use-cases/shopping.py
````python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent, Browser

load_dotenv()

import asyncio

task = """
   ### Prompt for Shopping Agent – Migros Online Grocery Order

**Objective:**
Visit [Migros Online](https://www.migros.ch/en), search for the required grocery items, add them to the cart, select an appropriate delivery window, and complete the checkout process using TWINT.

**Important:**
- Make sure that you don't buy more than it's needed for each article.
- After your search, if you click  the "+" button, it adds the item to the basket.
- if you open the basket sidewindow menu, you can close it by clicking the X button on the top right. This will help you navigate easier.
---

### Step 1: Navigate to the Website
- Open [Migros Online](https://www.migros.ch/en).
- You should be logged in as Nikolaos Kaliorakis

---

### Step 2: Add Items to the Basket

#### Shopping List:

**Meat & Dairy:**
- Beef Minced meat (1 kg)
- Gruyère cheese (grated preferably)
- 2 liters full-fat milk
- Butter (cheapest available)

**Vegetables:**
- Carrots (1kg pack)
- Celery
- Leeks (1 piece)
- 1 kg potatoes

At this stage, check the basket on the top right (indicates the price) and check if you bought the right items.

**Fruits:**
- 2 lemons
- Oranges (for snacking)

**Pantry Items:**
- Lasagna sheets
- Tahini
- Tomato paste (below CHF2)
- Black pepper refill (not with the mill)
- 2x 1L Oatly Barista(oat milk)
- 1 pack of eggs (10 egg package)

#### Ingredients I already have (DO NOT purchase):
- Olive oil, garlic, canned tomatoes, dried oregano, bay leaves, salt, chili flakes, flour, nutmeg, cumin.

---

### Step 3: Handling Unavailable Items
- If an item is **out of stock**, find the best alternative.
- Use the following recipe contexts to choose substitutions:
  - **Pasta Bolognese & Lasagna:** Minced meat, tomato paste, lasagna sheets, milk (for béchamel), Gruyère cheese.
  - **Hummus:** Tahini, chickpeas, lemon juice, olive oil.
  - **Chickpea Curry Soup:** Chickpeas, leeks, curry, lemons.
  - **Crispy Slow-Cooked Pork Belly with Vegetables:** Potatoes, butter.
- Example substitutions:
  - If Gruyère cheese is unavailable, select another semi-hard cheese.
  - If Tahini is unavailable, a sesame-based alternative may work.

---

### Step 4: Adjusting for Minimum Order Requirement
- If the total order **is below CHF 99**, add **a liquid soap refill** to reach the minimum. If it;s still you can buy some bread, dark chockolate.
- At this step, check if you have bought MORE items than needed. If the price is more then CHF200, you MUST remove items.
- If an item is not available, choose an alternative.
- if an age verification is needed, remove alcoholic products, we haven't verified yet.

---

### Step 5: Select Delivery Window
- Choose a **delivery window within the current week**. It's ok to pay up to CHF2 for the window selection.
- Preferably select a slot within the workweek.

---

### Step 6: Checkout
- Proceed to checkout.
- Select **TWINT** as the payment method.
- Check out.
- 
- if it's needed the username is: nikoskalio.dev@gmail.com 
- and the password is : TheCircuit.Migros.dev!
---

### Step 7: Confirm Order & Output Summary
- Once the order is placed, output a summary including:
  - **Final list of items purchased** (including any substitutions).
  - **Total cost**.
  - **Chosen delivery time**.

**Important:** Ensure efficiency and accuracy throughout the process."""

browser = Browser()

agent = Agent(
	task=task,
	llm=ChatOpenAI(model='gpt-4o'),
	browser=browser,
)


async def main():
	await agent.run()
	input('Press Enter to close the browser...')
	await browser.close()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/use-cases/twitter_post_using_cookies.py
````python
# Goal: Automates posting on X (Twitter) using stored authentication cookies.

import asyncio
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))


browser = Browser(
	config=BrowserConfig(
		# browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
	)
)
file_path = os.path.join(os.path.dirname(__file__), 'twitter_cookies.txt')
context = BrowserContext(browser=browser, config=BrowserContextConfig(cookies_file=file_path))


async def main():
	agent = Agent(
		browser_context=context,
		task=('go to https://x.com. write a new post with the text "browser-use ftw", and submit it'),
		llm=llm,
		max_actions_per_step=4,
	)
	await agent.run(max_steps=25)
	input('Press Enter to close the browser...')


if __name__ == '__main__':
	asyncio.run(main())
````

## File: examples/use-cases/wikipedia_banana_to_quantum.py
````python
import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig, BrowserContextConfig

load_dotenv()

# video https://preview.screen.studio/share/vuq91Ej8
llm = ChatOpenAI(
	model='gpt-4o',
	temperature=0.0,
)
task = 'go to https://en.wikipedia.org/wiki/Banana and click on buttons on the wikipedia page to go as fast as possible from banna to Quantum mechanics'

browser = Browser(
	config=BrowserConfig(
		new_context_config=BrowserContextConfig(
			viewport_expansion=-1,
			highlight_elements=False,
		),
	),
)
agent = Agent(task=task, llm=llm, browser=browser, use_vision=False)


async def main():
	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
````

## File: LICENSE
````
MIT License

Copyright (c) 2024 Gregor Zunic

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
````

## File: pyproject.toml
````toml
[project]
name = "browser-use"
description = "Make websites accessible for AI agents"
authors = [{ name = "Gregor Zunic" }]
version = "0.1.41"
readme = "README.md"
requires-python = ">=3.11,<4.0"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
dependencies = [
    "anyio>=4.9.0",
    "httpx>=0.27.2",
    "pydantic>=2.10.4,<2.11.0",
    "python-dotenv>=1.0.1",
    "requests>=2.32.3",
    "posthog>=3.7.0",
    "patchright>=1.51.0",
    "markdownify==1.1.0",
    "langchain-core==0.3.49",
    "langchain-openai==0.3.11",
    "langchain-anthropic==0.3.3",
    "langchain-ollama==0.3.0",
    "langchain-google-genai==2.1.2",
    "langchain-deepseek>=0.1.3",
    "langchain>=0.3.21",
    "langchain-aws>=0.2.11",
    "botocore>=1.37.23",
    "google-api-core>=2.24.0",
    "pyperclip>=1.9.0",
    "pyobjc>=11.0; platform_system == 'darwin'",
    "screeninfo>=0.8.1; platform_system != 'darwin'",
    "typing-extensions>=4.12.2",
    "psutil>=7.0.0",
    "faiss-cpu>=1.10.0",
    "mem0ai==0.1.93",
]
# botocore: only needed for Bedrock Claude boto3 examples/models/bedrock_claude.py 
# pydantic: >2.11 introduces many pydantic deprecation warnings until langchain-core upgrades their pydantic support lets keep it on 2.10
# google-api-core: only used for Google LLM APIs
# pyperclip: only used for examples that use copy/paste
# pyobjc: only used to get screen resolution on macOS
# screeninfo: only used to get screen resolution on Linux/Windows
# markdownify: used for page text content extraction for passing to LLM
# openai: datalib,voice-helpers are actually NOT NEEDED but openai produces noisy errors on exit without them TODO: fix

# Optional dependencies for memory functionality
[project.optional-dependencies]
memory = [
    "sentence-transformers>=4.0.2",
]

[project.urls]
Repository = "https://github.com/browser-use/browser-use"

[tool.codespell]
ignore-words-list = "bu"
skip = "*.json"

[tool.ruff]
line-length = 130
fix = true

[tool.ruff.lint]
select = ["ASYNC", "E", "F", "FAST", "I", "PLE"]
ignore = ["ASYNC109", "E101", "E402", "E501", "F841", "E731"]  # TODO: determine if adding timeouts to all the unbounded async functions is needed / worth-it so we can un-ignore ASYNC109
unfixable = ["E101", "E402", "E501", "F841", "E731"]

[tool.ruff.format]
quote-style = "single"
indent-style = "tab"
docstring-code-format = true

[tool.pyright]
typeCheckingMode = "off"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build]
include = [
    "browser_use/**/*.py",
    "!browser_use/**/tests/*.py",
    "!browser_use/**/tests.py",
    "browser_use/agent/system_prompt.md",
    "browser_use/dom/buildDomTree.js",
]

[tool.uv]
dev-dependencies = [
    "ruff>=0.11.2",
    "tokencost>=0.1.16",
    "build>=1.2.2",
    "pytest>=8.3.5",
    "pytest-asyncio>=0.24.0",
    "fastapi>=0.115.8",
    "inngest>=0.4.19",
    "uvicorn>=0.34.0",
    "langchain-fireworks>=0.2.6",
    "ipdb>=0.13.13",
    "pre-commit>=4.2.0",
    "codespell>=2.4.1",
    "pyright>=1.1.399",
]
````

## File: pytest.ini
````
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    asyncio: mark tests as async tests

testpaths =
    tests

python_files =
    test_*.py
    *_test.py

addopts =
    -v
    --strict-markers
    --tb=short

asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
log_cli = true
; log_cli_level = DEBUG
log_cli_format = %(levelname)-8s [%(name)s] %(message)s
filterwarnings =
    ignore::pytest.PytestDeprecationWarning
    ignore::DeprecationWarning

log_level = INFO
````

## File: SECURITY.md
````markdown
## Reporting Security Issues

If you believe you have found a security vulnerability in browser-use, please report it through coordinated disclosure.

**Please do not report security vulnerabilities through the repository issues, discussions, or pull requests.**

Instead, please open a new [Github security advisory](https://github.com/browser-use/browser-use/security/advisories/new).

Please include as much of the information listed below as you can to help me better understand and resolve the issue:

* The type of issue (e.g., buffer overflow, SQL injection, or cross-site scripting)
* Full paths of source file(s) related to the manifestation of the issue
* The location of the affected source code (tag/branch/commit or direct URL)
* Any special configuration required to reproduce the issue
* Step-by-step instructions to reproduce the issue
* Proof-of-concept or exploit code (if possible)
* Impact of the issue, including how an attacker might exploit the issue

This information will help me triage your report more quickly.
````

## File: SPIKE_FLOW_2.md
````markdown
# Browser-Use System Flow Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Core Components](#core-components)
3. [Execution Flow](#execution-flow)
4. [Component Details](#component-details)
5. [Additional Features](#additional-features)

## System Overview

The browser-use system is a sophisticated automation framework that combines LLM (Large Language Model) capabilities with browser automation to execute complex web tasks. The system follows a modular architecture with clear separation of concerns.

## Core Components

### 1. Agent (`browser_use/agent/service.py`)
- Central orchestrator of the system
- Manages the execution flow
- Coordinates between LLM, browser, and actions
- Handles state management and memory

### 2. Browser (`browser_use/browser/browser.py`)
- Manages browser instance
- Handles browser context
- Controls browser state
- Configurable settings (headless, security, etc.)

### 3. Controller (`browser_use/controller/service.py`)
- Executes browser actions
- Validates action parameters
- Manages action registry
- Handles action results

### 4. Message Manager (`browser_use/agent/message_manager/service.py`)
- Manages conversation history
- Handles system prompts
- Processes LLM inputs/outputs
- Maintains context

## Execution Flow

### 1. Initialization Phase
```python
# browser_use/agent/service.py - Agent.__init__
agent = Agent(
    task=task_description,
    llm=language_model,
    browser=browser_instance,
    # Optional configurations
    use_vision=True,
    enable_memory=True,
    max_steps=38
)
```

#### Key Initialization Steps:
1. Load environment variables
2. Initialize core components:
   - LLM instance
   - Browser instance
   - Message Manager
   - Memory system (optional)
   - Controller
   - State management
3. Verify LLM connection
4. Set up action models
5. Initialize browser context

### 2. Main Execution Loop
```python
# browser_use/agent/service.py - Agent.run()
async def run(self):
    while not done and steps < max_steps:
        # Execute single step
        result = await self.step()
        # Check completion
        if result.is_done:
            break
```

#### Step Execution Flow:
1. **Browser State Collection**
   - Get current URL
   - Capture DOM
   - Take screenshot (if vision enabled)
   - Update selector map
   - Track tab information

2. **LLM Processing**
   - Send current state to LLM
   - Include:
     - System prompt
     - Available actions
     - Browser state
     - Task description
     - Conversation history

3. **Action Generation**
   - LLM outputs:
     - Action type
     - Target selectors
     - Action parameters
   - Parse into `AgentOutput` model

4. **Action Execution**
   - Validate action
   - Execute via Playwright
   - Capture results
   - Update browser state

5. **State Update**
   - Update history
   - Process memory
   - Handle errors
   - Capture telemetry

### 3. Completion Phase
- Save conversation history
- Generate execution GIF (optional)
- Clean up resources
- Return final results

## Component Details

### Browser State Structure
```json
{
  "url": "current_url",
  "title": "page_title",
  "html_content": "raw_html",
  "tree": {
    "type": "document",
    "children": [...]
  },
  "screenshot": "base64_image",
  "selector_map": {},
  "tabs": [...]
}
```

### Action Types
- Navigation
- Click
- Type
- Select
- Scroll
- Wait
- Custom actions

### Tool Calling Methods
- Function calling
- JSON mode
- Raw output
- Auto detection

## Additional Features

### 1. Error Handling
- Retry logic for failed actions
- Error type classification
- Graceful degradation
- Error reporting

### 2. Memory System
- Context maintenance
- Long-term memory
- Procedural memory
- State persistence

### 3. Telemetry
- Step execution tracking
- Performance metrics
- Error logging
- Usage statistics

### 4. Configuration Options
- Browser settings
- LLM parameters
- Memory configuration
- Action customization
- Security settings

### 5. Extensibility
- Custom action support
- Plugin system
- Custom LLM integration
- Browser customization

## Code References

### Main Components
- Agent: `browser_use/agent/service.py`
- Browser: `browser_use/browser/browser.py`
- Controller: `browser_use/controller/service.py`
- Message Manager: `browser_use/agent/message_manager/service.py`
- Memory: `browser_use/agent/memory/service.py`
- DOM Processing: `browser_use/dom/`

### Supporting Files
- Views: `browser_use/agent/views.py`
- Telemetry: `browser_use/telemetry/service.py`
- DOM Views: `browser_use/dom/views.py`
- Controller Registry: `browser_use/controller/registry/views.py`

## Best Practices

1. **Error Handling**
   - Always implement retry logic
   - Use appropriate error types
   - Maintain error context
   - Log detailed error information

2. **State Management**
   - Keep state updates atomic
   - Validate state changes
   - Maintain state history
   - Handle state recovery

3. **Performance**
   - Optimize browser operations
   - Minimize DOM queries
   - Use efficient selectors
   - Implement proper cleanup

4. **Security**
   - Validate all inputs
   - Sanitize selectors
   - Handle sensitive data
   - Implement proper access control

5. **Testing**
   - Unit test components
   - Integration test flows
   - End-to-end testing
   - Performance testing
````

## File: SPIKE_FLOW.md
````markdown
# Execution Flow for `examples/simple.py`

This document outlines the sequence of class, method, and function calls when executing the `examples/simple.py` script using the `browser-use` library.

## 1. Initialization (`examples/simple.py` - Module Level)

1.  **Imports:** Standard Python imports (`os`, `sys`, `asyncio`) and project/library imports (`dotenv`, `langchain_openai.ChatOpenAI`, `browser_use.Agent`).
2.  **Environment Variables:** `dotenv.load_dotenv()` loads API keys and other configurations from a `.env` file.
3.  **LLM Instantiation:** `langchain_openai.ChatOpenAI(...)` creates the language model instance (`llm`) specified (e.g., 'gpt-4o').
4.  **Agent Instantiation:** `browser_use.agent.service.Agent(task=..., llm=...)` creates the main agent object. This triggers the `Agent.__init__` method.

## 2. Agent Initialization (`browser_use.agent.service.Agent.__init__`)

This method sets up the core components of the agent:

1.  **Basic Attributes:** Stores `task`, `llm`.
2.  **Settings:** Instantiates `browser_use.agent.views.AgentSettings`.
3.  **State:** Instantiates `browser_use.agent.views.AgentState`.
4.  **Action Models Setup (`_setup_action_models`):**
    *   Dynamically creates Pydantic models for browser actions using `browser_use.controller.service.Controller.registry.create_action_model()`.
    *   Creates specialized `AgentOutput` types using `browser_use.agent.views.AgentOutput.type_with_custom_actions()`.
5.  **Metadata Setup:**
    *   `_set_browser_use_version_and_source()`: Determines package version/source.
    *   `_set_model_names()`: Extracts model name(s).
    *   `_set_tool_calling_method()`: Determines how the LLM calls actions (e.g., function calling).
6.  **LLM Verification (`_verify_llm_connection`):** Performs a test call to the LLM API.
7.  **Message Context (`_set_message_context`):** Sets up initial context for LLM messages.
8.  **Message Manager:** Instantiates `browser_use.agent.message_manager.service.MessageManager` to handle conversation history and system prompts.
9.  **Memory (Optional):** If `enable_memory` is true, instantiates `browser_use.agent.memory.service.Memory`.
10. **Browser Setup:**
    *   Instantiates `browser_use.browser.browser.Browser` (via `Browser.__init__`).
    *   Instantiates `browser_use.browser.context.BrowserContext` (via `BrowserContext.__init__`), linking it to the `Browser` instance.
11. **Telemetry:** Instantiates `browser_use.telemetry.service.ProductTelemetry`.

## 3. Running the Agent (`examples/simple.py` - `main()` function)

1.  **Start Execution:** `agent.run()` is called within an `asyncio.run()` loop.

## 4. Agent Execution Loop (`browser_use.agent.service.Agent.run`)

1.  **Logging:** `_log_agent_run()` logs the start for telemetry.
2.  **Main Loop:** Iterates until `max_steps` is reached or a `done` action occurs.
    *   **Check State:** `_raise_if_stopped_or_paused()` checks for interruptions.
    *   **Execute Step:** `Agent.step()` performs one cycle of observation, thought, and action.
    *   **Check Completion:** Breaks loop if `result[-1].is_done` is true.
    *   **Handle Interruptions:** Catches `InterruptedError`.
3.  **Post-Loop:**
    *   **Logging:** `log_completion()` logs run outcome.
    *   **GIF Generation (Optional):** `browser_use.agent.gif.create_history_gif()`.
    *   **History Saving (Optional):** `save_history()`.
    *   **Cleanup:** `Agent.close()`.
    *   **Return:** Returns the `AgentHistoryList`.

## 5. Agent Step (`browser_use.agent.service.Agent.step`)

This method executes a single cycle within the main loop:

1.  **Increment Step:** `self.state.n_steps += 1`.
2.  **Get Browser State:** `BrowserContext.get_state(...)` retrieves the current URL, DOM, screenshot (if vision enabled).
    *   *Lazy Initialization:* On the first call, this triggers `Browser.get_playwright_browser()` -> `Browser._init()` which starts Playwright (`async_playwright().start()`) and launches/connects to the browser (`playwright.chromium.launch()`, etc.).
    *   Uses `DOMService` for DOM processing.
3.  **Memory Update (Optional):** `Memory.create_procedural_memory()` if conditions met.
4.  **Check State:** `_raise_if_stopped_or_paused()`.
5.  **Update Actions (Optional):** `_update_action_models_for_page()` based on page content.
6.  **Add State to History:** `MessageManager.add_state_message()` adds browser state for LLM context.
7.  **Planner (Optional):** `_run_planner()` calls LLM for planning, adds result via `MessageManager.add_plan()`.
8.  **Prepare LLM Input:** `MessageManager.get_messages()`.
9.  **Call LLM for Action:** `Agent.get_next_action()` sends history/state to the LLM.
    *   Uses LangChain's `llm.invoke(...)` or similar.
    *   Parses the JSON response into `AgentOutput` (includes the `ActionModel` chosen by the LLM). Handles errors/retries.
10. **Check State:** `_raise_if_stopped_or_paused()`.
11. **Callbacks/Saving:** Executes `register_new_step_callback` and `save_conversation` if configured.
12. **Update History:**
    *   `MessageManager._remove_last_state_message()` (removes verbose state).
    *   `MessageManager.add_model_output()` (adds LLM response).
13. **Execute Actions:** `Agent.multi_act(model_output.action)` runs the action(s) chosen by the LLM.
    *   Iterates through actions in the sequence.
    *   For each action, calls `browser_use.controller.service.Controller.execute(...)`.
        *   The `Controller` maps the action name to the corresponding method (e.g., `navigate_to_url`).
        *   Action methods use `BrowserContext` and Playwright functions (`page.goto`, `page.click`, etc.) to interact with the browser.
        *   Returns an `ActionResult`.
14. **Store Result:** `self.state.last_result = result`.
15. **Error Handling:** `_handle_step_error()` manages exceptions during the step.
16. **Telemetry:** `ProductTelemetry.capture(AgentStepTelemetryEvent(...))`.
17. **Create History Item:** `_make_history_item()` appends detailed step info (`AgentHistory`, `BrowserStateHistory`) to `self.state.history.history`.

## 6. Agent Cleanup (`browser_use.agent.service.Agent.close`)

Called at the end of `agent.run()`:

1.  **Close Context:** `BrowserContext.close()` closes the current Playwright context.
2.  **Close Browser (Conditional):** If `keep_alive` is false, `Browser.close()` is called.
    *   This closes the Playwright browser instance (`playwright_browser.close()`).
    *   Stops the Playwright connection (`playwright.stop()`).
    *   Cleans up any browser subprocesses.
3.  **Garbage Collection:** `gc.collect()`.

## 7. Finalization (`examples/simple.py`)

1.  **Event Loop:** `asyncio.run(main())` completes when `agent.run()` returns.
````

## File: SPIKE_LLM_BROWSER_STATE.md
````markdown
# Initial Browser State for LLM Interaction

This document explains the state of the browser when the agent first retrieves it and provides an example of the data structure passed to the LLM.

## Browser State at Initial Retrieval

**Question:** Is the browser already open when the *initial* browser state is grabbed?

**Answer:** No, not typically. The browser launch/connection is usually **lazy-initialized**. As noted in `SPIKE_FLOW.md` (Section 5, Point 2, Sub-point, Line 60):

> *   *Lazy Initialization:* On the first call, this triggers `Browser.get_playwright_browser()` -> `Browser._init()` which starts Playwright (`async_playwright().start()`) and launches/connects to the browser (`playwright.chromium.launch()`, etc.).

This means the browser instance is created *as part of* the first call to `BrowserContext.get_state()` within the initial `Agent.step()`.

## Data Structure of Browser State

**Question:** What is the exact data output format?

**Answer:** The `BrowserContext.get_state()` method returns a structured object, likely a Pydantic model instance (e.g., `BrowserState`). This object contains key information about the current web page, processed for the LLM. Common fields include:

*   **URL:** Current page URL (`url`).
*   **Title:** Page title (`title`).
*   **DOM Representation:** Often a simplified tree (`tree`) or list of interactive elements, not necessarily the full raw HTML (though raw HTML might also be included `html_content`).
*   **Screenshot:** Base64 encoded image string if vision is enabled (`screenshot`).
*   **Selector Map:** Mapping from simplified IDs used in prompts to actual CSS/XPath selectors (`selector_map`).
*   **Tabs:** Information about open tabs (`tabs`).

## Example: Initial `BrowserState` (Blank Page)

When the browser first launches, it opens to `about:blank`. The initial state object would look something like this:

```json
{
  "url": "about:blank",
  "title": "",
  "html_content": "<html><head></head><body></body></html>",
  "tree": {
    "type": "document",
    "children": [
      {
        "type": "element",
        "name": "html",
        "attributes": {},
        "children": [
          {"type": "element", "name": "head", "attributes": {}, "children": []},
          {"type": "element", "name": "body", "attributes": {}, "children": []}
        ]
      }
    ]
  },
  "screenshot": null, // Or base64 string of a blank image
  "selector_map": {},
  "tabs": [
    {
      "tabId": 1,
      "url": "about:blank",
      "title": "",
      "isActive": true
    }
  ]
}
```

This minimal state is then combined with the task description and sent to the LLM via `Agent.get_next_action()` to determine the first actual browser action (e.g., navigating to a specific URL).
````

## File: SPIKE_LLM_STATE_MESSAGE_TRANSFORM.md
````markdown
# Viewing Raw Browser State Before Message Transformation

The state printed previously (`agent.state.message_manager_state`) reflects the *processed* state after it has been added to the message history managed by `MessageManager`. This includes system prompts, task descriptions, and formatted browser state information.

## The Transformation Point

The raw `BrowserState` object (containing the URL, simplified DOM tree, selector map, etc.) is transformed into LLM-readable messages within the `MessageManager.add_state_message` method.

## How to View the Raw `BrowserState`

To see the raw `BrowserState` data *before* it undergoes transformation by `MessageManager.add_state_message`, you need to intercept it within the `Agent.step` method immediately after it's retrieved.

1.  **File:** `browser_use/agent/service.py`
2.  **Method:** `async def step(self, ...)`
3.  **Location:** Insert a print statement *after* the `BrowserState` object is assigned to the `state` variable and *before* it's passed to `self._message_manager.add_state_message(...)`.

**Code Snippet (Illustrative Location approx. Lines 391-417):**

```python
# browser_use/agent/service.py

# ... inside Agent.step method ...
		try:
			# <<<--- 1. Raw state is retrieved here --->>>
			state = await self.browser_context.get_state(cache_clickable_elements_hashes=True)
			active_page = await self.browser_context.get_current_page()

			# <<<--- !!! INSERT PRINT STATEMENT HERE to see raw state !!! --->>>
			# Example:
			print(">>> RAW BrowserState Object <<<")
			# Use model_dump_json for a readable Pydantic model output
			print(state.model_dump_json(indent=2))
			print("---------------------------------")

			# ... (memory, pause check, action model updates) ...

			# <<<--- 2. Raw state is processed and added to messages here --->>>
			self._message_manager.add_state_message(state, self.state.last_result, step_info, self.settings.use_vision)

            # ... (rest of the step method) ...
```

By printing `state.model_dump_json(indent=2)` at this location, you will see the complete, raw structure of the `BrowserState` object as retrieved from the browser context, before it's formatted for the LLM conversation history.
````

## File: SPIKE_LLM_STATE_SET.md
````markdown
# LLM Message Preparation Locations

This document outlines where the different components of the message list sent to the LLM (System Prompt, Initial Task, Current Browser State) are prepared within the `browser-use` codebase.

The preparation primarily occurs within the `MessageManager` class, orchestrated by the `Agent` class methods.

## 1. System Prompt and Initial Task Setup

*   **When:** During the initialization of the `Agent` object.
*   **Where:** `browser_use/agent/service.py`, inside the `Agent.__init__` method.
*   **How:** The `task` string and a formatted system prompt (generated by `SystemPrompt` class, likely in `browser_use/agent/prompts.py`) are passed to the `MessageManager` constructor.
*   **Code Snippet (approx. Lines 210-223 in `agent/service.py`):
    ```python
    # browser_use/agent/service.py Agent.__init__
    self._message_manager = MessageManager(
        task=task, # Initial task passed here
        system_message=SystemPrompt(
            # ... configuration ...
        ).get_system_message(), # Formatted system instructions
        settings=MessageManagerSettings(
            # ... settings ...
        ),
        state=self.state.message_manager_state,
    )
    # MessageManager.__init__ adds these as the initial messages.
    ```

## 2. Adding the Current Browser State

*   **When:** At the beginning of each execution cycle within `Agent.step()`.
*   **Where:** `browser_use/agent/service.py`, inside the `Agent.step` method.
*   **How:** The `BrowserState` object (retrieved by `BrowserContext.get_state()`) is passed to the `MessageManager.add_state_message` method, which formats it (text, possibly image) and appends it to the message history.
*   **Code Snippet (approx. Line 417 in `agent/service.py`):
    ```python
    # browser_use/agent/service.py Agent.step
    # state = await self.browser_context.get_state(...)
    self._message_manager.add_state_message(state, self.state.last_result, step_info, self.settings.use_vision)
    ```

## 3. Retrieving Prepared Messages for LLM Call

*   **When:** Immediately before the LLM is called within `Agent.step()`.
*   **Where:** `browser_use/agent/service.py`, inside the `Agent.step` method.
*   **How:** The `MessageManager.get_messages()` method is called to retrieve the complete, ordered list of messages (System, Human, AI, State) that have been prepared.
*   **Code Snippet (approx. Line 448 in `agent/service.py`):
    ```python
    # browser_use/agent/service.py Agent.step
    input_messages = self._message_manager.get_messages()
    # ...
    model_output = await self.get_next_action(input_messages) # Prepared messages sent here
    ```

**In Summary:** The `MessageManager` acts as the central hub for constructing the conversation history sent to the LLM. It's initialized with the static components (system prompt, task) and dynamically updated with the current browser state in each step before the full message list is retrieved and passed to the LLM via `Agent.get_next_action()`.
````

## File: SPIKE_LLM_TOUCHPOINT.md
````markdown
# First LLM Touchpoint for Task Execution

This document identifies the initial point in the `browser-use` execution flow (as detailed in `SPIKE_FLOW.md`) where the Large Language Model (LLM) is first contacted to process the user-provided task and determine the initial actions.

## Sequence Leading to First LLM Call:

1.  **Initialization:** The `Agent` is initialized (`Agent.__init__`), potentially including a brief LLM call for connection verification (`_verify_llm_connection` - `SPIKE_FLOW.md`, Line 26), but this call is not for task processing.
2.  **Run Agent:** `agent.run()` begins the execution loop (`SPIKE_FLOW.md`, Line 38).
3.  **First Step:** The `agent.run()` loop calls `Agent.step()` for the first time (`SPIKE_FLOW.md`, Line 46).

## The First Task-Related LLM Call:

Inside the *first execution* of `Agent.step()` (`SPIKE_FLOW.md`, starting Line 56):

*   The agent gathers the initial context: system prompt, the user's task (e.g., "Go to wikipedia.com and search for deepseek"), and the initial browser state.
*   The core interaction occurs at **Point 9: `Call LLM for Action: Agent.get_next_action() sends history/state to the LLM.` (`SPIKE_FLOW.md`, Line 69)**.
*   This `get_next_action` method is responsible for packaging the information and sending it to the configured LLM.
*   The actual API communication happens via the LangChain integration, noted in the sub-point: **`Uses LangChain's llm.invoke(...) or similar.` (`SPIKE_FLOW.md`, Line 70)**.

**In summary:** The first time the LLM is invoked to understand the specific task and decide on the *initial actions* (like navigating to a URL) is during the first call to `Agent.step()`, within the `Agent.get_next_action()` method, referenced on **Line 69** of `SPIKE_FLOW.md`.
````

## File: tests/conftest.py
````python
"""
Test configuration for browser-use.
"""

import logging
import os
import sys

import pytest
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

# Ensure the project root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext


@pytest.fixture(scope='session')
def llm():
	"""
	Fixture to provide a ChatOpenAI instance or a mock for testing.
	Uses a mock if OPENAI_API_KEY is not set.
	"""
	api_key = os.getenv('OPENAI_API_KEY')
	logger.debug(f'API Key present: {bool(api_key)}')
	logger.debug('Using actual ChatOpenAI model')
	return ChatOpenAI(model='gpt-4o', api_key=SecretStr(api_key) if api_key else None)


@pytest.fixture(scope='session')
def browser():
	"""
	Fixture to provide a Browser instance for testing.
	"""
	logger.debug('Creating Browser instance for testing')
	return Browser(config=BrowserConfig(headless=True, disable_security=True))


@pytest.fixture(scope='function')
async def browser_context(browser):
	"""
	Fixture to provide a BrowserContext instance for testing.
	"""
	logger.debug('Creating BrowserContext instance for testing')
	context = BrowserContext(browser=browser)
	yield context
	await context.close()
````

## File: tests/test_action_filters.py
````python
from unittest.mock import MagicMock

import pytest
from patchright.async_api import Page
from pydantic import BaseModel

from browser_use.controller.registry.service import Registry
from browser_use.controller.registry.views import ActionRegistry, RegisteredAction


class EmptyParamModel(BaseModel):
	pass


class TestActionFilters:
	def test_get_prompt_description_no_filters(self):
		"""Test that system prompt only includes actions with no filters"""
		registry = ActionRegistry()

		# Add actions with and without filters
		no_filter_action = RegisteredAction(
			name='no_filter_action',
			description='Action with no filters',
			function=lambda: None,
			param_model=EmptyParamModel,
			domains=None,
			page_filter=None,
		)

		page_filter_action = RegisteredAction(
			name='page_filter_action',
			description='Action with page filter',
			function=lambda: None,
			param_model=EmptyParamModel,
			domains=None,
			page_filter=lambda page: True,
		)

		domain_filter_action = RegisteredAction(
			name='domain_filter_action',
			description='Action with domain filter',
			function=lambda: None,
			param_model=EmptyParamModel,
			domains=['example.com'],
			page_filter=None,
		)

		registry.actions = {
			'no_filter_action': no_filter_action,
			'page_filter_action': page_filter_action,
			'domain_filter_action': domain_filter_action,
		}

		# System prompt (no page) should only include actions with no filters
		system_description = registry.get_prompt_description()
		assert 'no_filter_action' in system_description
		assert 'page_filter_action' not in system_description
		assert 'domain_filter_action' not in system_description

	def test_page_filter_matching(self):
		"""Test that page filters work correctly"""
		registry = ActionRegistry()

		# Create a mock page
		mock_page = MagicMock(spec=Page)
		mock_page.url = 'https://example.com/page'

		# Create actions with different page filters
		matching_action = RegisteredAction(
			name='matching_action',
			description='Action with matching page filter',
			function=lambda: None,
			param_model=EmptyParamModel,
			domains=None,
			page_filter=lambda page: 'example.com' in page.url,
		)

		non_matching_action = RegisteredAction(
			name='non_matching_action',
			description='Action with non-matching page filter',
			function=lambda: None,
			param_model=EmptyParamModel,
			domains=None,
			page_filter=lambda page: 'other.com' in page.url,
		)

		registry.actions = {'matching_action': matching_action, 'non_matching_action': non_matching_action}

		# Page-specific description should only include matching actions
		page_description = registry.get_prompt_description(mock_page)
		assert 'matching_action' in page_description
		assert 'non_matching_action' not in page_description

	def test_domain_filter_matching(self):
		"""Test that domain filters work correctly with glob patterns"""
		registry = ActionRegistry()

		# Create actions with different domain patterns
		actions = {
			'exact_match': RegisteredAction(
				name='exact_match',
				description='Exact domain match',
				function=lambda: None,
				param_model=EmptyParamModel,
				domains=['example.com'],
				page_filter=None,
			),
			'subdomain_match': RegisteredAction(
				name='subdomain_match',
				description='Subdomain wildcard match',
				function=lambda: None,
				param_model=EmptyParamModel,
				domains=['*.example.com'],
				page_filter=None,
			),
			'prefix_match': RegisteredAction(
				name='prefix_match',
				description='Prefix wildcard match',
				function=lambda: None,
				param_model=EmptyParamModel,
				domains=['example*'],
				page_filter=None,
			),
			'non_matching': RegisteredAction(
				name='non_matching',
				description='Non-matching domain',
				function=lambda: None,
				param_model=EmptyParamModel,
				domains=['other.com'],
				page_filter=None,
			),
		}

		registry.actions = actions

		# Test exact domain match
		mock_page = MagicMock(spec=Page)
		mock_page.url = 'https://example.com/page'

		exact_match_description = registry.get_prompt_description(mock_page)
		assert 'exact_match' in exact_match_description
		assert 'non_matching' not in exact_match_description

		# Test subdomain match
		mock_page.url = 'https://sub.example.com/page'
		subdomain_match_description = registry.get_prompt_description(mock_page)
		assert 'subdomain_match' in subdomain_match_description
		assert 'exact_match' not in subdomain_match_description

		# Test prefix match
		mock_page.url = 'https://example123.org/page'
		prefix_match_description = registry.get_prompt_description(mock_page)
		assert 'prefix_match' in prefix_match_description

	def test_domain_and_page_filter_together(self):
		"""Test that actions can be filtered by both domain and page filter"""
		registry = ActionRegistry()

		# Create a mock page
		mock_page = MagicMock(spec=Page)
		mock_page.url = 'https://example.com/admin'

		# Actions with different combinations of filters
		actions = {
			'domain_only': RegisteredAction(
				name='domain_only',
				description='Domain filter only',
				function=lambda: None,
				param_model=EmptyParamModel,
				domains=['example.com'],
				page_filter=None,
			),
			'page_only': RegisteredAction(
				name='page_only',
				description='Page filter only',
				function=lambda: None,
				param_model=EmptyParamModel,
				domains=None,
				page_filter=lambda page: 'admin' in page.url,
			),
			'both_matching': RegisteredAction(
				name='both_matching',
				description='Both filters matching',
				function=lambda: None,
				param_model=EmptyParamModel,
				domains=['example.com'],
				page_filter=lambda page: 'admin' in page.url,
			),
			'both_one_fail': RegisteredAction(
				name='both_one_fail',
				description='One filter fails',
				function=lambda: None,
				param_model=EmptyParamModel,
				domains=['other.com'],
				page_filter=lambda page: 'admin' in page.url,
			),
		}

		registry.actions = actions

		# Check that only actions with matching filters are included
		description = registry.get_prompt_description(mock_page)
		assert 'domain_only' in description  # Domain matches
		assert 'page_only' in description  # Page filter matches
		assert 'both_matching' in description  # Both filters match
		assert 'both_one_fail' not in description  # Domain filter fails

		# Test with different URL where page filter fails
		mock_page.url = 'https://example.com/dashboard'
		description = registry.get_prompt_description(mock_page)
		assert 'domain_only' in description  # Domain matches
		assert 'page_only' not in description  # Page filter fails
		assert 'both_matching' not in description  # Page filter fails
		assert 'both_one_fail' not in description  # Domain filter fails

	@pytest.mark.asyncio
	async def test_registry_action_decorator(self):
		"""Test the action decorator with filters"""
		registry = Registry()

		# Define actions with different filters
		@registry.action(
			description='No filter action',
		)
		def no_filter_action():
			pass

		@registry.action(description='Domain filter action', domains=['example.com'])
		def domain_filter_action():
			pass

		@registry.action(description='Page filter action', page_filter=lambda page: 'admin' in page.url)
		def page_filter_action():
			pass

		# Check that system prompt only includes the no_filter_action
		system_description = registry.get_prompt_description()
		assert 'No filter action' in system_description
		assert 'Domain filter action' not in system_description
		assert 'Page filter action' not in system_description

		# Check that page-specific prompt includes the right actions
		mock_page = MagicMock(spec=Page)
		mock_page.url = 'https://example.com/admin'

		page_description = registry.get_prompt_description(mock_page)
		assert 'Domain filter action' in page_description
		assert 'Page filter action' in page_description

	@pytest.mark.asyncio
	async def test_action_model_creation(self):
		"""Test that action models are created correctly with filters"""
		registry = Registry()

		# Define actions with different filters
		@registry.action(
			description='No filter action',
		)
		def no_filter_action():
			pass

		@registry.action(description='Domain filter action', domains=['example.com'])
		def domain_filter_action():
			pass

		@registry.action(description='Page filter action', page_filter=lambda page: 'admin' in page.url)
		def page_filter_action():
			pass

		@registry.action(description='Both filters action', domains=['example.com'], page_filter=lambda page: 'admin' in page.url)
		def both_filters_action():
			pass

		# Initial action model should only include no_filter_action
		initial_model = registry.create_action_model()
		assert 'no_filter_action' in initial_model.model_fields
		assert 'domain_filter_action' not in initial_model.model_fields
		assert 'page_filter_action' not in initial_model.model_fields
		assert 'both_filters_action' not in initial_model.model_fields

		# Action model with matching page should include all matching actions
		mock_page = MagicMock(spec=Page)
		mock_page.url = 'https://example.com/admin'

		page_model = registry.create_action_model(page=mock_page)
		assert 'no_filter_action' in page_model.model_fields
		assert 'domain_filter_action' in page_model.model_fields
		assert 'page_filter_action' in page_model.model_fields
		assert 'both_filters_action' in page_model.model_fields

		# Action model with non-matching domain should exclude domain-filtered actions
		mock_page.url = 'https://other.com/admin'
		non_matching_domain_model = registry.create_action_model(page=mock_page)
		assert 'no_filter_action' in non_matching_domain_model.model_fields
		assert 'domain_filter_action' not in non_matching_domain_model.model_fields
		assert 'page_filter_action' in non_matching_domain_model.model_fields
		assert 'both_filters_action' not in non_matching_domain_model.model_fields

		# Action model with non-matching page filter should exclude page-filtered actions
		mock_page.url = 'https://example.com/dashboard'
		non_matching_page_model = registry.create_action_model(page=mock_page)
		assert 'no_filter_action' in non_matching_page_model.model_fields
		assert 'domain_filter_action' in non_matching_page_model.model_fields
		assert 'page_filter_action' not in non_matching_page_model.model_fields
		assert 'both_filters_action' not in non_matching_page_model.model_fields
````

## File: tests/test_agent_actions.py
````python
import asyncio
import os

import pytest
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, SecretStr

from browser_use.agent.service import Agent
from browser_use.agent.views import AgentHistoryList
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.views import BrowserState


@pytest.fixture
def llm():
	"""Initialize language model for testing"""

	# return ChatAnthropic(model_name='claude-3-5-sonnet-20240620', timeout=25, stop=None)
	return AzureChatOpenAI(
		model='gpt-4o',
		api_version='2024-10-21',
		azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
		api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', '')),
	)
	# return ChatOpenAI(model='gpt-4o-mini')


@pytest.fixture(scope='session')
def event_loop():
	"""Create an instance of the default event loop for each test case."""
	loop = asyncio.get_event_loop_policy().new_event_loop()
	yield loop
	loop.close()


@pytest.fixture(scope='session')
async def browser(event_loop):
	browser_instance = Browser(
		config=BrowserConfig(
			headless=True,
		)
	)
	yield browser_instance
	await browser_instance.close()


@pytest.fixture
async def context(browser):
	async with await browser.new_context() as context:
		yield context
		# Clean up automatically happens with __aexit__


# pytest tests/test_agent_actions.py -v -k "test_ecommerce_interaction" --capture=no
# @pytest.mark.asyncio
@pytest.mark.skip(reason='Kinda expensive to run')
async def test_ecommerce_interaction(llm, context):
	"""Test complex ecommerce interaction sequence"""
	agent = Agent(
		task="Go to amazon.com, search for 'laptop', filter by 4+ stars, and find the price of the first result",
		llm=llm,
		browser_context=context,
		save_conversation_path='tmp/test_ecommerce_interaction/conversation',
	)

	history: AgentHistoryList = await agent.run(max_steps=20)

	# Verify sequence of actions
	action_sequence = []
	for action in history.model_actions():
		action_name = list(action.keys())[0]
		if action_name in ['go_to_url', 'open_tab']:
			action_sequence.append('navigate')
		elif action_name == 'input_text':
			action_sequence.append('input')
			# Check that the input is 'laptop'
			inp = action['input_text']['text'].lower()  # type: ignore
			if inp == 'laptop':
				action_sequence.append('input_exact_correct')
			elif 'laptop' in inp:
				action_sequence.append('correct_in_input')
			else:
				action_sequence.append('incorrect_input')
		elif action_name == 'click_element':
			action_sequence.append('click')

	# Verify essential steps were performed
	assert 'navigate' in action_sequence  # Navigated to Amazon
	assert 'input' in action_sequence  # Entered search term
	assert 'click' in action_sequence  # Clicked search/filter
	assert 'input_exact_correct' in action_sequence or 'correct_in_input' in action_sequence


# @pytest.mark.asyncio
async def test_error_recovery(llm, context):
	"""Test agent's ability to recover from errors"""
	agent = Agent(
		task='Navigate to nonexistent-site.com and then recover by going to google.com ',
		llm=llm,
		browser_context=context,
	)

	history: AgentHistoryList = await agent.run(max_steps=10)

	actions_names = history.action_names()
	actions = history.model_actions()
	assert 'go_to_url' in actions_names or 'open_tab' in actions_names, f'{actions_names} does not contain go_to_url or open_tab'
	for action in actions:
		if 'go_to_url' in action:
			assert 'url' in action['go_to_url'], 'url is not in go_to_url'
			assert action['go_to_url']['url'].endswith('google.com'), 'url does not end with google.com'
			break


# @pytest.mark.asyncio
async def test_find_contact_email(llm, context):
	"""Test agent's ability to find contact email on a website"""
	agent = Agent(
		task='Go to https://browser-use.com/ and find out the contact email',
		llm=llm,
		browser_context=context,
	)

	history: AgentHistoryList = await agent.run(max_steps=10)

	# Verify the agent found the contact email
	extracted_content = history.extracted_content()
	email = 'info@browser-use.com'
	for content in extracted_content:
		if email in content:
			break
	else:
		pytest.fail(f'{extracted_content} does not contain {email}')


# @pytest.mark.asyncio
async def test_agent_finds_installation_command(llm, context):
	"""Test agent's ability to find the pip installation command for browser-use on the web"""
	agent = Agent(
		task='Find the pip installation command for the browser-use repo',
		llm=llm,
		browser_context=context,
	)

	history: AgentHistoryList = await agent.run(max_steps=10)

	# Verify the agent found the correct installation command
	extracted_content = history.extracted_content()
	install_command = 'pip install browser-use'
	for content in extracted_content:
		if install_command in content:
			break
	else:
		pytest.fail(f'{extracted_content} does not contain {install_command}')


class CaptchaTest(BaseModel):
	name: str
	url: str
	success_text: str
	additional_text: str | None = None


# run 3 test: python -m pytest tests/test_agent_actions.py -v -k "test_captcha_solver" --capture=no --log-cli-level=INFO
# pytest tests/test_agent_actions.py -v -k "test_captcha_solver" --capture=no --log-cli-level=INFO
@pytest.mark.asyncio
@pytest.mark.parametrize(
	'captcha',
	[
		CaptchaTest(
			name='Text Captcha',
			url='https://2captcha.com/demo/text',
			success_text='Captcha is passed successfully!',
		),
		CaptchaTest(
			name='Basic Captcha',
			url='https://captcha.com/demos/features/captcha-demo.aspx',
			success_text='Correct!',
		),
		CaptchaTest(
			name='Rotate Captcha',
			url='https://2captcha.com/demo/rotatecaptcha',
			success_text='Captcha is passed successfully',
			additional_text='Use multiple clicks at once. click done when image is exact correct position.',
		),
		CaptchaTest(
			name='MT Captcha',
			url='https://2captcha.com/demo/mtcaptcha',
			success_text='Verified Successfully',
			additional_text='Stop when you solved it successfully.',
		),
	],
)
async def test_captcha_solver(llm, context, captcha: CaptchaTest):
	"""Test agent's ability to solve different types of captchas"""
	agent = Agent(
		task=f'Go to {captcha.url} and solve the captcha. {captcha.additional_text}',
		llm=llm,
		browser_context=context,
	)
	from browser_use.agent.views import AgentHistoryList

	history: AgentHistoryList = await agent.run(max_steps=7)

	state: BrowserState = await context.get_state()

	all_text = state.element_tree.get_all_text_till_next_clickable_element()

	if not all_text:
		all_text = ''

	if not isinstance(all_text, str):
		all_text = str(all_text)

	solved = captcha.success_text in all_text
	assert solved, f'Failed to solve {captcha.name}'

	# python -m pytest tests/test_agent_actions.py -v --capture=no

	# pytest tests/test_agent_actions.py -v -k "test_captcha_solver" --capture=no --log-cli-level=INFO
````

## File: tests/test_attach_chrome.py
````python
import asyncio

from patchright.async_api import async_playwright


async def test_full_screen(start_fullscreen: bool, maximize: bool):
	async with async_playwright() as p:
		try:
			print('Attempting to connect to Chrome...')
			# run in terminal: /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --no-first-run
			browser = await p.chromium.connect_over_cdp(
				'http://localhost:9222',
				timeout=20000,  # 20 second timeout for connection
			)
			print('Connected to Chrome successfully')

			# Get the first context and page, or create new ones if needed
			if len(browser.contexts) == 0:
				context = await browser.new_context(ignore_https_errors=True)
			else:
				context = browser.contexts[0]

			if len(context.pages) == 0:
				page = await context.new_page()
			else:
				page = context.pages[0]

			print('Attempting to navigate to Gmail...')
			try:
				# First try with a shorter timeout
				await page.goto(
					'https://mail.google.com',
					wait_until='load',  # Changed from domcontentloaded
					timeout=10000,
				)
			except Exception as e:
				print(f'First navigation attempt failed: {e}')
				print('Trying again with different settings...')
				# If that fails, try again with different settings
				await page.goto(
					'https://mail.google.com',
					wait_until='commit',  # Less strict wait condition
					timeout=30000,
				)

			# Wait for the page to stabilize
			await asyncio.sleep(2)

			print(f'Current page title: {await page.title()}')

			# Optional: wait for specific Gmail elements
			try:
				await page.wait_for_selector('div[role="main"]', timeout=5000)
				print('Gmail interface detected')
			except Exception as e:
				print(f'Note: Gmail interface not detected: {e}')

			await asyncio.sleep(30)
		except Exception as e:
			print(f'An error occurred: {e}')
			import traceback

			traceback.print_exc()
		finally:
			await browser.close()


if __name__ == '__main__':
	asyncio.run(test_full_screen(False, False))
````

## File: tests/test_browser_config_models.py
````python
import os

import pytest

from browser_use.browser.browser import Browser, BrowserConfig, ProxySettings
from browser_use.browser.context import BrowserContext, BrowserContextConfig, BrowserContextWindowSize


@pytest.mark.asyncio
async def test_proxy_settings_pydantic_model():
	"""
	Test that ProxySettings as a Pydantic model is correctly converted to a dictionary when used.
	"""
	# Create ProxySettings with Pydantic model
	proxy_settings = ProxySettings(
		server='http://example.proxy:8080', bypass='localhost', username='testuser', password='testpass'
	)

	# Verify the model has correct dict-like access
	assert proxy_settings['server'] == 'http://example.proxy:8080'
	assert proxy_settings.get('bypass') == 'localhost'
	assert proxy_settings.get('nonexistent', 'default') == 'default'

	# Verify model_dump works correctly
	proxy_dict = proxy_settings.model_dump()
	assert isinstance(proxy_dict, dict)
	assert proxy_dict['server'] == 'http://example.proxy:8080'
	assert proxy_dict['bypass'] == 'localhost'
	assert proxy_dict['username'] == 'testuser'
	assert proxy_dict['password'] == 'testpass'

	# We don't launch the actual browser - we just verify the model itself works as expected


@pytest.mark.asyncio
async def test_window_size_pydantic_model():
	"""
	Test that BrowserContextWindowSize as a Pydantic model is correctly converted to a dictionary when used.
	"""
	# Create BrowserContextWindowSize with Pydantic model
	window_size = BrowserContextWindowSize(width=1280, height=1100)

	# Verify the model has correct dict-like access
	assert window_size['width'] == 1280
	assert window_size.get('height') == 1100
	assert window_size.get('nonexistent', 'default') == 'default'

	# Verify model_dump works correctly
	window_dict = window_size.model_dump()
	assert isinstance(window_dict, dict)
	assert window_dict['width'] == 1280
	assert window_dict['height'] == 1100

	# Create a context config with the window size and test initialization
	config = BrowserContextConfig(browser_window_size=window_size)
	assert config.browser_window_size == window_size

	# You can also create from a dictionary
	config2 = BrowserContextConfig(browser_window_size={'width': 1920, 'height': 1080})
	assert isinstance(config2.browser_window_size, BrowserContextWindowSize)
	assert config2.browser_window_size.width == 1920
	assert config2.browser_window_size.height == 1080


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('CI') == 'true', reason='Skip browser test in CI')
async def test_window_size_with_real_browser():
	"""
	Integration test that verifies our window size Pydantic model is correctly
	passed to Playwright and the actual browser window is configured with these settings.
	This test is skipped in CI environments.
	"""
	# Create window size with specific dimensions we can check
	window_size = BrowserContextWindowSize(width=1024, height=768)

	# Create browser config with headless mode
	browser_config = BrowserConfig(
		headless=True,  # Use headless for faster test
	)

	# Create context config with our window size
	context_config = BrowserContextConfig(
		browser_window_size=window_size,
		maximum_wait_page_load_time=2.0,  # Faster timeouts for test
		minimum_wait_page_load_time=0.2,
		no_viewport=True,  # Use actual window size instead of viewport
	)

	# Create browser and context
	browser = Browser(config=browser_config)
	try:
		# Initialize browser
		playwright_browser = await browser.get_playwright_browser()
		assert playwright_browser is not None, 'Browser initialization failed'

		# Create context
		browser_context = BrowserContext(browser=browser, config=context_config)
		try:
			# Initialize session
			await browser_context._initialize_session()

			# Get the current page
			page = await browser_context.get_current_page()
			assert page is not None, 'Failed to get current page'

			# Get the context configuration used for browser window size
			video_size = await page.evaluate("""
                () => {
                    // This returns information about the context recording settings
                    // which should match our configured video size (browser_window_size)
                    try {
                        const settings = window.getPlaywrightContextSettings ? 
                            window.getPlaywrightContextSettings() : null;
                        if (settings && settings.recordVideo) {
                            return settings.recordVideo.size;
                        }
                    } catch (e) {}
                    
                    // Fallback to window dimensions
                    return {
                        width: window.innerWidth,
                        height: window.innerHeight
                    };
                }
            """)

			# Let's also check the viewport size
			viewport_size = await page.evaluate("""
                () => {
                    return {
                        width: window.innerWidth,
                        height: window.innerHeight
                    }
                }
            """)

			print(f'Window size config: {window_size.model_dump()}')
			print(f'Browser viewport size: {viewport_size}')

			# This is a lightweight test to verify that the page has a size (details may vary by browser)
			assert viewport_size['width'] > 0, 'Expected viewport width to be positive'
			assert viewport_size['height'] > 0, 'Expected viewport height to be positive'

			# For browser context creation in record_video_size, this is what truly matters
			# Verify that our window size was properly serialized to a dictionary
			print(f'Content of context session: {browser_context.session.context}')
			print('✅ Browser window size used in the test')
		finally:
			# Clean up context
			await browser_context.close()
	finally:
		# Clean up browser
		await browser.close()


@pytest.mark.asyncio
async def test_proxy_with_real_browser():
	"""
	Integration test that verifies our proxy Pydantic model is correctly
	passed to Playwright without requiring a working proxy server.

	This test:
	1. Creates a ProxySettings Pydantic model
	2. Passes it to BrowserConfig
	3. Verifies browser initialization works (proving the model was correctly serialized)
	4. We don't actually verify proxy functionality (would require a working proxy)
	"""
	# Create proxy settings with a fake proxy server
	proxy_settings = ProxySettings(
		server='http://non.existent.proxy:9999', bypass='localhost', username='testuser', password='testpass'
	)

	# Test model serialization
	proxy_dict = proxy_settings.model_dump()
	assert isinstance(proxy_dict, dict)
	assert proxy_dict['server'] == 'http://non.existent.proxy:9999'

	# Create browser config with proxy
	browser_config = BrowserConfig(
		headless=True,
		proxy=proxy_settings,
	)

	# Create browser
	browser = Browser(config=browser_config)
	try:
		# Initialize browser - this should succeed even with invalid proxy
		# because we're just checking configuration, not actual proxy functionality
		try:
			playwright_browser = await browser.get_playwright_browser()
			assert playwright_browser is not None, 'Browser initialization failed'

			# Success - the browser was initialized with our proxy settings
			# We won't try to make requests (which would fail with non-existent proxy)
			print('✅ Browser initialized with proxy settings successfully')

			# We can inspect browser settings here to verify proxy was passed
			# but the specific API to access these settings depends on the browser

		except Exception as e:
			# Make sure any exception isn't related to the proxy configuration format
			# (Network errors due to non-existent proxy are acceptable, invalid type conversion isn't)
			error_text = str(e).lower()
			assert 'proxy' not in error_text or any(
				term in error_text for term in ['connect', 'connection', 'network', 'timeout', 'unreachable']
			), f'Proxy configuration error (not network error): {e}'
	finally:
		# Clean up browser
		await browser.close()
````

## File: tests/test_context.py
````python
import base64
from unittest.mock import Mock

import pytest

from browser_use.browser.context import BrowserContext, BrowserContextConfig
from browser_use.browser.views import BrowserState
from browser_use.dom.views import DOMElementNode


def test_is_url_allowed():
	"""
	Test the _is_url_allowed method to verify that it correctly checks URLs against
	the allowed domains configuration.
	Scenario 1: When allowed_domains is None, all URLs should be allowed.
	Scenario 2: When allowed_domains is a list, only URLs matching the allowed domain(s) are allowed.
	Scenario 3: When the URL is malformed, it should return False.
	"""
	# Create a dummy Browser mock. Only the 'config' attribute is needed for _is_url_allowed.
	dummy_browser = Mock()
	# Set an empty config for dummy_browser; it won't be used in _is_url_allowed.
	dummy_browser.config = Mock()
	# Scenario 1: allowed_domains is None, any URL should be allowed.
	config1 = BrowserContextConfig(allowed_domains=None)
	context1 = BrowserContext(browser=dummy_browser, config=config1)
	assert context1._is_url_allowed('http://anydomain.com') is True
	assert context1._is_url_allowed('https://anotherdomain.org/path') is True
	# Scenario 2: allowed_domains is provided.
	allowed = ['example.com', 'mysite.org']
	config2 = BrowserContextConfig(allowed_domains=allowed)
	context2 = BrowserContext(browser=dummy_browser, config=config2)
	# URL exactly matching
	assert context2._is_url_allowed('http://example.com') is True
	# URL with subdomain (should be allowed)
	assert context2._is_url_allowed('http://sub.example.com/path') is True
	# URL with different domain (should not be allowed)
	assert context2._is_url_allowed('http://notexample.com') is False
	# URL that matches second allowed domain
	assert context2._is_url_allowed('https://mysite.org/page') is True
	# URL with port number, still allowed (port is stripped)
	assert context2._is_url_allowed('http://example.com:8080') is True
	# Scenario 3: Malformed URL or empty domain
	# urlparse will return an empty netloc for some malformed URLs.
	assert context2._is_url_allowed('notaurl') is False


def test_convert_simple_xpath_to_css_selector():
	"""
	Test the _convert_simple_xpath_to_css_selector method of BrowserContext.
	This verifies that simple XPath expressions (with and without indices) are correctly converted to CSS selectors.
	"""
	# Test empty xpath returns empty string
	assert BrowserContext._convert_simple_xpath_to_css_selector('') == ''
	# Test a simple xpath without indices
	xpath = '/html/body/div/span'
	expected = 'html > body > div > span'
	result = BrowserContext._convert_simple_xpath_to_css_selector(xpath)
	assert result == expected
	# Test xpath with an index on one element: [2] should translate to :nth-of-type(2)
	xpath = '/html/body/div[2]/span'
	expected = 'html > body > div:nth-of-type(2) > span'
	result = BrowserContext._convert_simple_xpath_to_css_selector(xpath)
	assert result == expected
	# Test xpath with indices on multiple elements:
	# For "li[3]" -> li:nth-of-type(3) and for "a[1]" -> a:nth-of-type(1)
	xpath = '/ul/li[3]/a[1]'
	expected = 'ul > li:nth-of-type(3) > a:nth-of-type(1)'
	result = BrowserContext._convert_simple_xpath_to_css_selector(xpath)
	assert result == expected


def test_get_initial_state():
	"""
	Test the _get_initial_state method to verify it returns the correct initial BrowserState.
	The test checks that when a dummy page with a URL is provided,
	the returned state contains that URL and other default values.
	"""
	# Create a dummy browser since only its existence is needed.
	dummy_browser = Mock()
	dummy_browser.config = Mock()
	context = BrowserContext(browser=dummy_browser, config=BrowserContextConfig())

	# Define a dummy page with a 'url' attribute.
	class DummyPage:
		url = 'http://dummy.com'

	dummy_page = DummyPage()
	# Call _get_initial_state with a page: URL should be set from page.url.
	state_with_page = context._get_initial_state(page=dummy_page)
	assert state_with_page.url == dummy_page.url
	# Verify that the element_tree is initialized with tag 'root'
	assert state_with_page.element_tree.tag_name == 'root'
	# Call _get_initial_state without a page: URL should be empty.
	state_without_page = context._get_initial_state()
	assert state_without_page.url == ''


@pytest.mark.asyncio
async def test_execute_javascript():
	"""
	Test the execute_javascript method by mocking the current page's evaluate function.
	This ensures that when execute_javascript is called, it correctly returns the value
	from the page's evaluate method.
	"""

	# Define a dummy page with an async evaluate method.
	class DummyPage:
		async def evaluate(self, script):
			return 'dummy_result'

	# Create a dummy session object with a dummy current_page.
	dummy_session = type('DummySession', (), {})()
	dummy_session.current_page = DummyPage()
	# Create a dummy browser mock with a minimal config.
	dummy_browser = Mock()
	dummy_browser.config = Mock()
	# Initialize the BrowserContext with the dummy browser and config.
	context = BrowserContext(browser=dummy_browser, config=BrowserContextConfig())
	# Manually set the session to our dummy session.
	context.session = dummy_session
	# Call execute_javascript and verify it returns the expected result.
	result = await context.execute_javascript('return 1+1')
	assert result == 'dummy_result'


@pytest.mark.asyncio
async def test_enhanced_css_selector_for_element():
	"""
	Test the _enhanced_css_selector_for_element method to verify that
	it returns the correct CSS selector string for a dummy DOMElementNode.
	The test checks that:
	  - The provided xpath is correctly converted (handling indices),
	  - Class attributes are appended as CSS classes,
	  - Standard and dynamic attributes (including ones with special characters)
	    are correctly added to the selector.
	"""
	# Create a dummy DOMElementNode instance with a complex set of attributes.
	dummy_element = DOMElementNode(
		tag_name='div',
		is_visible=True,
		parent=None,
		xpath='/html/body/div[2]',
		attributes={'class': 'foo bar', 'id': 'my-id', 'placeholder': 'some "quoted" text', 'data-testid': '123'},
		children=[],
	)
	# Call the method with include_dynamic_attributes=True.
	actual_selector = BrowserContext._enhanced_css_selector_for_element(dummy_element, include_dynamic_attributes=True)
	# Expected conversion:
	# 1. The xpath "/html/body/div[2]" converts to "html > body > div:nth-of-type(2)".
	# 2. The class attribute "foo bar" appends ".foo.bar".
	# 3. The "id" attribute is added as [id="my-id"].
	# 4. The "placeholder" attribute contains quotes; it is added as
	#    [placeholder*="some \"quoted\" text"].
	# 5. The dynamic attribute "data-testid" is added as [data-testid="123"].
	expected_selector = (
		'html > body > div:nth-of-type(2).foo.bar[id="my-id"][placeholder*="some \\"quoted\\" text"][data-testid="123"]'
	)
	assert actual_selector == expected_selector, f'Expected {expected_selector}, but got {actual_selector}'


@pytest.mark.asyncio
async def test_get_scroll_info():
	"""
	Test the get_scroll_info method by mocking the page's evaluate method.
	This dummy page returns preset values for window.scrollY, window.innerHeight,
	and document.documentElement.scrollHeight. The test then verifies that the
	computed scroll information (pixels_above and pixels_below) match the expected values.
	"""

	# Define a dummy page with an async evaluate method returning preset values.
	class DummyPage:
		async def evaluate(self, script):
			if 'window.scrollY' in script:
				return 100  # scrollY
			elif 'window.innerHeight' in script:
				return 500  # innerHeight
			elif 'document.documentElement.scrollHeight' in script:
				return 1200  # total scrollable height
			return None

	# Create a dummy session with a dummy current_page.
	dummy_session = type('DummySession', (), {})()
	dummy_session.current_page = DummyPage()
	# We also need a dummy context attribute but it won't be used in this test.
	dummy_session.context = type('DummyContext', (), {})()
	# Create a dummy browser mock.
	dummy_browser = Mock()
	dummy_browser.config = Mock()
	# Initialize BrowserContext with the dummy browser and config.
	context = BrowserContext(browser=dummy_browser, config=BrowserContextConfig())
	# Manually set the session to our dummy session.
	context.session = dummy_session
	# Call get_scroll_info on the dummy page.
	pixels_above, pixels_below = await context.get_scroll_info(dummy_session.current_page)
	# Expected calculations:
	# pixels_above = scrollY = 100
	# pixels_below = total_height - (scrollY + innerHeight) = 1200 - (100 + 500) = 600
	assert pixels_above == 100, f'Expected 100 pixels above, got {pixels_above}'
	assert pixels_below == 600, f'Expected 600 pixels below, got {pixels_below}'


@pytest.mark.asyncio
async def test_reset_context():
	"""
	Test the reset_context method to ensure it correctly closes all existing tabs,
	resets the cached state, and creates a new page.
	"""

	# Dummy Page with close and wait_for_load_state methods.
	class DummyPage:
		def __init__(self, url='http://dummy.com'):
			self.url = url
			self.closed = False

		async def close(self):
			self.closed = True

		async def wait_for_load_state(self):
			pass

	# Dummy Context that holds pages and can create a new page.
	class DummyContext:
		def __init__(self):
			self.pages = []

		async def new_page(self):
			new_page = DummyPage(url='')
			self.pages.append(new_page)
			return new_page

	# Create a dummy session with a context containing two pages.
	dummy_session = type('DummySession', (), {})()
	dummy_context = DummyContext()
	page1 = DummyPage(url='http://page1.com')
	page2 = DummyPage(url='http://page2.com')
	dummy_context.pages.extend([page1, page2])
	dummy_session.context = dummy_context
	dummy_session.current_page = page1
	dummy_session.cached_state = None
	# Create a dummy browser mock.
	dummy_browser = Mock()
	dummy_browser.config = Mock()
	# Initialize BrowserContext using our dummy_browser and config,
	# and manually set its session to our dummy session.
	context = BrowserContext(browser=dummy_browser, config=BrowserContextConfig())
	context.session = dummy_session
	# Confirm session has 2 pages before reset.
	assert len(dummy_session.context.pages) == 2
	# Call reset_context which should close existing pages,
	# reset the cached state, and create a new page as current_page.
	await context.reset_context()
	# Verify that initial pages were closed.
	assert page1.closed is True
	assert page2.closed is True
	# Check that a new page is created and set as current_page.
	assert dummy_session.current_page is not None
	new_page = dummy_session.current_page
	# New page URL should be empty as per _get_initial_state.
	assert new_page.url == ''
	# Verify that cached_state is reset to an initial BrowserState.
	state = dummy_session.cached_state
	assert isinstance(state, BrowserState)
	assert state.url == ''
	assert state.element_tree.tag_name == 'root'


@pytest.mark.asyncio
async def test_take_screenshot():
	"""
	Test the take_screenshot method to verify that it returns a base64 encoded screenshot string.
	A dummy page with a mocked screenshot method is used, returning a predefined byte string.
	"""

	class DummyPage:
		async def screenshot(self, full_page, animations):
			# Verify that parameters are forwarded correctly.
			assert full_page is True, 'full_page parameter was not correctly passed'
			assert animations == 'disabled', 'animations parameter was not correctly passed'
			# Return a test byte string.
			return b'test'

	# Create a dummy session with the DummyPage as the current_page.
	dummy_session = type('DummySession', (), {})()
	dummy_session.current_page = DummyPage()
	dummy_session.context = None  # Not used in this test
	# Create a dummy browser mock.
	dummy_browser = Mock()
	dummy_browser.config = Mock()
	# Initialize the BrowserContext with the dummy browser and config.
	context = BrowserContext(browser=dummy_browser, config=BrowserContextConfig())
	# Manually set the session to our dummy session.
	context.session = dummy_session
	# Call take_screenshot and check that it returns the expected base64 encoded string.
	result = await context.take_screenshot(full_page=True)
	expected = base64.b64encode(b'test').decode('utf-8')
	assert result == expected, f'Expected {expected}, but got {result}'


@pytest.mark.asyncio
async def test_refresh_page_behavior():
	"""
	Test the refresh_page method of BrowserContext to verify that it correctly reloads the current page
	and waits for the page's load state. This is done by creating a dummy page that flags when its
	reload and wait_for_load_state methods are called.
	"""

	class DummyPage:
		def __init__(self):
			self.reload_called = False
			self.wait_for_load_state_called = False

		async def reload(self):
			self.reload_called = True

		async def wait_for_load_state(self):
			self.wait_for_load_state_called = True

	# Create a dummy session with the dummy page as the current_page.
	dummy_page = DummyPage()
	dummy_session = type('DummySession', (), {})()
	dummy_session.current_page = dummy_page
	dummy_session.context = None  # Not required for this test
	# Create a dummy browser mock
	dummy_browser = Mock()
	dummy_browser.config = Mock()
	# Initialize BrowserContext with the dummy browser and config,
	# and manually set its session to our dummy session.
	context = BrowserContext(browser=dummy_browser, config=BrowserContextConfig())
	context.session = dummy_session
	# Call refresh_page and verify that reload and wait_for_load_state were called.
	await context.refresh_page()
	assert dummy_page.reload_called is True, 'Expected the page to call reload()'
	assert dummy_page.wait_for_load_state_called is True, 'Expected the page to call wait_for_load_state()'


@pytest.mark.asyncio
async def test_remove_highlights_failure():
	"""
	Test the remove_highlights method to ensure that if the page.evaluate call fails,
	the exception is caught and does not propagate (i.e. the method handles errors gracefully).
	"""

	# Dummy page that always raises an exception when evaluate is called.
	class DummyPage:
		async def evaluate(self, script):
			raise Exception('dummy error')

	# Create a dummy session with the DummyPage as current_page.
	dummy_session = type('DummySession', (), {})()
	dummy_session.current_page = DummyPage()
	dummy_session.context = None  # Not used in this test
	# Create a dummy browser mock.
	dummy_browser = Mock()
	dummy_browser.config = Mock()
	# Initialize BrowserContext with the dummy browser and configuration.
	context = BrowserContext(browser=dummy_browser, config=BrowserContextConfig())
	context.session = dummy_session
	# Call remove_highlights and verify that no exception is raised.
	try:
		await context.remove_highlights()
	except Exception as e:
		pytest.fail(f'remove_highlights raised an exception: {e}')
````

## File: tests/test_core_functionality.py
````python
import asyncio
import os

import pytest
from langchain_openai import AzureChatOpenAI
from pydantic import SecretStr

from browser_use.agent.service import Agent
from browser_use.agent.views import AgentHistoryList
from browser_use.browser.browser import Browser, BrowserConfig


@pytest.fixture(scope='function')
def event_loop():
	"""Create an instance of the default event loop for each test case."""
	loop = asyncio.get_event_loop_policy().new_event_loop()
	yield loop
	loop.close()


@pytest.fixture(scope='function')
async def browser(event_loop):
	browser_instance = Browser(
		config=BrowserConfig(
			headless=True,
		)
	)
	yield browser_instance
	await browser_instance.close()


@pytest.fixture
async def context(browser):
	async with await browser.new_context() as context:
		yield context


@pytest.fixture
def llm():
	"""Initialize language model for testing"""
	return AzureChatOpenAI(
		model='gpt-4o',
		api_version='2024-10-21',
		azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
		api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', '')),
	)


# pytest -s -k test_search_google
@pytest.mark.asyncio
async def test_search_google(llm, context):
	"""Test 'Search Google' action"""
	agent = Agent(
		task="Search Google for 'OpenAI'.",
		llm=llm,
		browser_context=context,
	)
	history: AgentHistoryList = await agent.run(max_steps=2)
	action_names = history.action_names()
	assert 'search_google' in action_names


@pytest.mark.asyncio
async def test_go_to_url(llm, context):
	"""Test 'Navigate to URL' action"""
	agent = Agent(
		task="Navigate to 'https://www.python.org'.",
		llm=llm,
		browser_context=context,
	)
	history = await agent.run(max_steps=2)
	action_names = history.action_names()
	assert 'go_to_url' in action_names


@pytest.mark.asyncio
async def test_go_back(llm, context):
	"""Test 'Go back' action"""
	agent = Agent(
		task="Go to 'https://www.example.com', then go back.",
		llm=llm,
		browser_context=context,
	)
	history = await agent.run(max_steps=3)
	action_names = history.action_names()
	assert 'go_to_url' in action_names
	assert 'go_back' in action_names


@pytest.mark.asyncio
async def test_click_element(llm, context):
	"""Test 'Click element' action"""
	agent = Agent(
		task="Go to 'https://www.python.org' and click on the first link.",
		llm=llm,
		browser_context=context,
	)
	history = await agent.run(max_steps=4)
	action_names = history.action_names()
	assert 'go_to_url' in action_names or 'open_tab' in action_names
	assert 'click_element_by_index' in action_names


@pytest.mark.asyncio
async def test_input_text(llm, context):
	"""Test 'Input text' action"""
	agent = Agent(
		task="Go to 'https://www.google.com' and input 'OpenAI' into the search box.",
		llm=llm,
		browser_context=context,
	)
	history = await agent.run(max_steps=4)
	action_names = history.action_names()
	assert 'go_to_url' in action_names
	assert 'input_text' in action_names


@pytest.mark.asyncio
async def test_switch_tab(llm, context):
	"""Test 'Switch tab' action"""
	agent = Agent(
		task="Open new tabs with 'https://www.google.com' and 'https://www.wikipedia.org', then switch to the first tab.",
		llm=llm,
		browser_context=context,
	)
	history = await agent.run(max_steps=6)
	action_names = history.action_names()
	open_tab_count = action_names.count('open_tab')
	assert open_tab_count >= 2
	assert 'switch_tab' in action_names


@pytest.mark.asyncio
async def test_open_new_tab(llm, context):
	"""Test 'Open new tab' action"""
	agent = Agent(
		task="Open a new tab and go to 'https://www.example.com'.",
		llm=llm,
		browser_context=context,
	)
	history = await agent.run(max_steps=3)
	action_names = history.action_names()
	assert 'open_tab' in action_names


@pytest.mark.asyncio
async def test_extract_page_content(llm, context):
	"""Test 'Extract page content' action"""
	agent = Agent(
		task="Go to 'https://www.example.com' and extract the page content.",
		llm=llm,
		browser_context=context,
	)
	history = await agent.run(max_steps=3)
	action_names = history.action_names()
	assert 'go_to_url' in action_names
	assert 'extract_content' in action_names


# pytest -k test_done_action
@pytest.mark.asyncio
async def test_done_action(llm, context):
	"""Test 'Complete task' action"""
	agent = Agent(
		task="Navigate to 'https://www.example.com' and signal that the task is done.",
		llm=llm,
		browser_context=context,
	)

	history = await agent.run(max_steps=3)
	action_names = history.action_names()
	assert 'go_to_url' in action_names
	assert 'done' in action_names


# run with: pytest -k test_scroll_down
@pytest.mark.asyncio
async def test_scroll_down(llm, context):
	"""Test 'Scroll down' action and validate that the page actually scrolled"""
	agent = Agent(
		task="Go to 'https://en.wikipedia.org/wiki/Internet' and scroll down the page.",
		llm=llm,
		browser_context=context,
	)
	# Get the browser instance
	page = await context.get_current_page()

	# Navigate to the page and get initial scroll position
	await agent.run(max_steps=1)
	initial_scroll_position = await page.evaluate('window.scrollY;')

	# Perform the scroll down action
	await agent.run(max_steps=2)
	final_scroll_position = await page.evaluate('window.scrollY;')

	# Validate that the scroll position has changed
	assert final_scroll_position > initial_scroll_position, 'Page did not scroll down'

	# Validate that the 'scroll_down' action was executed
	history = agent.history
	action_names = history.action_names()
	assert 'scroll_down' in action_names
````

## File: tests/test_dropdown_complex.py
````python
"""
Test complex dropdown interaction functionality.
"""

import pytest

from browser_use.agent.service import Agent
from browser_use.agent.views import AgentHistoryList


@pytest.mark.asyncio
async def test_dropdown_complex(llm, browser_context):
	"""Test selecting an option from a complex dropdown menu."""
	agent = Agent(
		task=(
			'go to https://codepen.io/shyam-king/pen/pvzpByJ and first get all options for the dropdown and then select the json option'
		),
		llm=llm,
		browser_context=browser_context,
	)

	try:
		history: AgentHistoryList = await agent.run(20)
		result = history.final_result()

		# Verify dropdown interaction
		assert result is not None
		assert 'json' in result.lower(), "Expected 'json' option to be selected"

		# Verify dropdown state
		element = await browser_context.get_element_by_selector('.select-selected')
		assert element is not None, 'Custom dropdown element should exist'

		text = await element.text_content()
		assert 'json' in text.lower(), 'Dropdown should display json option'

		# Verify the selected option's effect
		code_element = await browser_context.get_element_by_selector('pre code')
		assert code_element is not None, 'Code element should be visible when JSON is selected'

	except Exception as e:
		pytest.fail(f'Complex dropdown test failed: {str(e)}')
	finally:
		await browser_context.close()
````

## File: tests/test_dropdown_error.py
````python
"""
Simple try of the agent.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import os
import sys

from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI

from browser_use import Agent, AgentHistoryList

llm = ChatOpenAI(model='gpt-4o')
# browser = Browser(config=BrowserConfig(headless=False))

agent = Agent(
	task=('go to https://codepen.io/shyam-king/pen/emOyjKm and select number "4" and return the output of "selected value"'),
	llm=llm,
	browser_context=BrowserContext(
		browser=Browser(config=BrowserConfig(headless=False, disable_security=True)),
	),
)


async def test_dropdown():
	history: AgentHistoryList = await agent.run(20)
	# await controller.browser.close(force=True)

	result = history.final_result()
	assert result is not None
	assert '4' in result
	print(result)

	# await browser.close()
````

## File: tests/test_dropdown.py
````python
"""
Test dropdown interaction functionality.
"""

import pytest

from browser_use.agent.service import Agent
from browser_use.agent.views import AgentHistoryList


@pytest.mark.asyncio
async def test_dropdown(llm, browser_context):
	"""Test selecting an option from a dropdown menu."""
	agent = Agent(
		task=(
			'go to https://codepen.io/geheimschriftstift/pen/mPLvQz and first get all options for the dropdown and then select the 5th option'
		),
		llm=llm,
		browser_context=browser_context,
	)

	try:
		history: AgentHistoryList = await agent.run(20)
		result = history.final_result()

		# Verify dropdown interaction
		assert result is not None
		assert 'Duck' in result, "Expected 5th option 'Duck' to be selected"

		# Verify dropdown state
		element = await browser_context.get_element_by_selector('select')
		assert element is not None, 'Dropdown element should exist'

		value = await element.evaluate('el => el.value')
		assert value == '5', 'Dropdown should have 5th option selected'

	except Exception as e:
		pytest.fail(f'Dropdown test failed: {str(e)}')
	finally:
		await browser_context.close()
````

## File: tests/test_excluded_actions.py
````python
import asyncio
import os

import pytest
from langchain_openai import AzureChatOpenAI
from pydantic import SecretStr

from browser_use.agent.service import Agent
from browser_use.agent.views import AgentHistoryList
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.controller.service import Controller

# run with:
# python -m pytest tests/test_excluded_actions.py -v -k "test_only_open_tab_allowed" --capture=no


@pytest.fixture(scope='session')
def event_loop():
	"""Create an instance of the default event loop for each test case."""
	loop = asyncio.get_event_loop_policy().new_event_loop()
	yield loop
	loop.close()


@pytest.fixture(scope='session')
async def browser(event_loop):
	browser_instance = Browser(
		config=BrowserConfig(
			headless=True,
		)
	)
	yield browser_instance
	await browser_instance.close()


@pytest.fixture
async def context(browser):
	async with await browser.new_context() as context:
		yield context


@pytest.fixture
def llm():
	"""Initialize language model for testing"""
	return AzureChatOpenAI(
		model='gpt-4o',
		api_version='2024-10-21',
		azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
		api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', '')),
	)


# pytest tests/test_excluded_actions.py -v -k "test_only_open_tab_allowed" --capture=no
@pytest.mark.asyncio
async def test_only_open_tab_allowed(llm, context):
	"""Test that only open_tab action is available while others are excluded"""

	# Create list of all default actions except open_tab
	excluded_actions = [
		'search_google',
		'go_to_url',
		'go_back',
		'click_element',
		'input_text',
		'switch_tab',
		'extract_content',
		'done',
		'scroll_down',
		'scroll_up',
		'send_keys',
		'scroll_to_text',
		'get_dropdown_options',
		'select_dropdown_option',
	]

	# Initialize controller with excluded actions
	controller = Controller(exclude_actions=excluded_actions)

	# Create agent with a task that would normally use other actions
	agent = Agent(
		task="Go to google.com and search for 'python programming'",
		llm=llm,
		browser_context=context,
		controller=controller,
	)

	history: AgentHistoryList = await agent.run(max_steps=2)

	# Verify that only open_tab was used
	action_names = history.action_names()

	# Only open_tab should be in the actions
	assert all(action == 'open_tab' for action in action_names), (
		f'Found unexpected actions: {[a for a in action_names if a != "open_tab"]}'
	)

	# open_tab should be used at least once
	assert 'open_tab' in action_names, 'open_tab action was not used'
````

## File: tests/test_full_screen.py
````python
import asyncio

from patchright.async_api import async_playwright


async def test_full_screen(start_fullscreen: bool, maximize: bool):
	async with async_playwright() as p:
		browser = await p.chromium.launch(
			headless=False,
			args=['--start-maximized'],
		)
		context = await browser.new_context(no_viewport=True, viewport=None)
		page = await context.new_page()
		await page.goto('https://google.com')

		await asyncio.sleep(10)
		await browser.close()


if __name__ == '__main__':
	asyncio.run(test_full_screen(False, False))
````

## File: tests/test_gif_path.py
````python
"""
Simple try of the agent.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import os
import sys

from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI

from browser_use import Agent, AgentHistoryList

llm = ChatOpenAI(model='gpt-4o')

agent = Agent(
	task=('go to google.com and search for text "hi there"'),
	llm=llm,
	browser_context=BrowserContext(
		browser=Browser(config=BrowserConfig(headless=False, disable_security=True)),
	),
	generate_gif='./google.gif',
)


async def test_gif_path():
	if os.path.exists('./google.gif'):
		os.unlink('./google.gif')

	history: AgentHistoryList = await agent.run(20)

	result = history.final_result()
	assert result is not None

	assert os.path.exists('./google.gif'), 'google.gif was not created'
````

## File: tests/test_mind2web.py
````python
"""
Test browser automation using Mind2Web dataset tasks with pytest framework.
"""

import asyncio
import json
import os
from typing import Any, Dict, List

import pytest
from langchain_openai import AzureChatOpenAI
from pydantic import SecretStr

from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.utils import logger

# Constants
MAX_STEPS = 50
TEST_SUBSET_SIZE = 10


@pytest.fixture(scope='session')
def event_loop():
	loop = asyncio.get_event_loop_policy().new_event_loop()
	yield loop
	loop.close()


@pytest.fixture(scope='session')
async def browser(event_loop):
	browser_instance = Browser(
		config=BrowserConfig(
			headless=True,
		)
	)
	yield browser_instance
	await browser_instance.close()


@pytest.fixture
async def context(browser):
	async with await browser.new_context() as new_context:
		yield new_context


@pytest.fixture(scope='session')
def test_cases() -> List[Dict[str, Any]]:
	"""Load test cases from Mind2Web dataset"""
	file_path = os.path.join(os.path.dirname(__file__), 'mind2web_data/processed.json')
	logger.info(f'Loading test cases from {file_path}')

	with open(file_path, 'r') as f:
		data = json.load(f)

	subset = data[:TEST_SUBSET_SIZE]
	logger.info(f'Loaded {len(subset)}/{len(data)} test cases')
	return subset


@pytest.fixture
def llm():
	"""Initialize language model for testing"""

	# return ChatAnthropic(model_name='claude-3-5-sonnet-20240620', timeout=25, stop=None)
	return AzureChatOpenAI(
		model='gpt-4o',
		api_version='2024-10-21',
		azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
		api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', '')),
	)


# run with: pytest -s -v tests/test_mind2web.py:test_random_samples
@pytest.mark.asyncio
async def test_random_samples(test_cases: List[Dict[str, Any]], llm, context, validator):
	"""Test a random sampling of tasks across different websites"""
	import random

	logger.info('=== Testing Random Samples ===')

	# Take random samples
	samples = random.sample(test_cases, 1)

	for i, case in enumerate(samples, 1):
		task = f'Go to {case["website"]}.com and {case["confirmed_task"]}'
		logger.info(f'--- Random Sample {i}/{len(samples)} ---')
		logger.info(f'Task: {task}\n')

		agent = Agent(task, llm, browser_context=context)

		await agent.run()

		logger.info('Validating random sample task...')

		# TODO: Validate the task


def test_dataset_integrity(test_cases):
	"""Test the integrity of the test dataset"""
	logger.info('\n=== Testing Dataset Integrity ===')

	required_fields = ['website', 'confirmed_task', 'action_reprs']
	missing_fields = []

	logger.info(f'Checking {len(test_cases)} test cases for required fields')

	for i, case in enumerate(test_cases, 1):
		logger.debug(f'Checking case {i}/{len(test_cases)}')

		for field in required_fields:
			if field not in case:
				missing_fields.append(f'Case {i}: {field}')
				logger.warning(f"Missing field '{field}' in case {i}")

		# Type checks
		if not isinstance(case.get('confirmed_task'), str):
			logger.error(f"Case {i}: 'confirmed_task' must be string")
			assert False, 'Task must be string'

		if not isinstance(case.get('action_reprs'), list):
			logger.error(f"Case {i}: 'action_reprs' must be list")
			assert False, 'Actions must be list'

		if len(case.get('action_reprs', [])) == 0:
			logger.error(f"Case {i}: 'action_reprs' must not be empty")
			assert False, 'Must have at least one action'

	if missing_fields:
		logger.error('Dataset integrity check failed')
		assert False, f'Missing fields: {missing_fields}'
	else:
		logger.info('✅ Dataset integrity check passed')


if __name__ == '__main__':
	pytest.main([__file__, '-v'])
````

## File: tests/test_models.py
````python
import asyncio
import os

import httpx
import pytest
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from pydantic import SecretStr

from browser_use.agent.service import Agent
from browser_use.agent.views import AgentHistoryList
from browser_use.browser.browser import Browser, BrowserConfig


@pytest.fixture(scope='function')
def event_loop():
	"""Create an instance of the default event loop for each test case."""
	loop = asyncio.get_event_loop_policy().new_event_loop()
	yield loop
	loop.close()


@pytest.fixture(scope='function')
async def browser(event_loop):
	browser_instance = Browser(
		config=BrowserConfig(
			headless=True,
		)
	)
	yield browser_instance
	await browser_instance.close()


@pytest.fixture
async def context(browser):
	async with await browser.new_context() as context:
		yield context


api_key_gemini = SecretStr(os.getenv('GEMINI_API_KEY') or '')
api_key_deepseek = SecretStr(os.getenv('DEEPSEEK_API_KEY') or '')
api_key_anthropic = SecretStr(os.getenv('ANTHROPIC_API_KEY') or '')


# pytest -s -v tests/test_models.py
@pytest.fixture(
	params=[
		ChatOpenAI(model='gpt-4o'),
		ChatOpenAI(model='gpt-4o-mini'),
		AzureChatOpenAI(
			model='gpt-4o',
			api_version='2024-10-21',
			azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
			api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', '')),
		),
		# ChatOpenAI(
		# base_url='https://api.deepseek.com/v1',
		# model='deepseek-reasoner',
		# api_key=api_key_deepseek,
		# ),
		# run: ollama start
		ChatOllama(
			model='qwen2.5:latest',
			num_ctx=128000,
		),
		AzureChatOpenAI(
			model='gpt-4o-mini',
			api_version='2024-10-21',
			azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
			api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', '')),
		),
		ChatAnthropic(
			model_name='claude-3-5-sonnet-20240620',
			timeout=100,
			temperature=0.0,
			stop=None,
			api_key=api_key_anthropic,
		),
		ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=api_key_gemini),
		ChatGoogleGenerativeAI(model='gemini-1.5-pro', api_key=api_key_gemini),
		ChatGoogleGenerativeAI(model='gemini-1.5-flash-latest', api_key=api_key_gemini),
		ChatOpenAI(
			base_url='https://api.deepseek.com/v1',
			model='deepseek-chat',
			api_key=api_key_deepseek,
		),
	],
	ids=[
		'gpt-4o',
		'gpt-4o-mini',
		'azure-gpt-4o',
		#'deepseek-reasoner',
		'qwen2.5:latest',
		'azure-gpt-4o-mini',
		'claude-3-5-sonnet',
		'gemini-2.0-flash-exp',
		'gemini-1.5-pro',
		'gemini-1.5-flash-latest',
		'deepseek-chat',
	],
)
async def llm(request):
	return request.param


@pytest.mark.asyncio
async def test_model_search(llm, context):
	"""Test 'Search Google' action"""
	model_name = llm.model if hasattr(llm, 'model') else llm.model_name
	print(f'\nTesting model: {model_name}')

	use_vision = True
	models_without_vision = ['deepseek-chat', 'deepseek-reasoner']
	if hasattr(llm, 'model') and llm.model in models_without_vision:
		use_vision = False
	elif hasattr(llm, 'model_name') and llm.model_name in models_without_vision:
		use_vision = False

	# require ollama run
	local_models = ['qwen2.5:latest']
	if model_name in local_models:
		# check if ollama is running
		# ping ollama http://127.0.0.1
		try:
			async with httpx.AsyncClient() as client:
				response = await client.get('http://127.0.0.1:11434/')
				if response.status_code != 200:
					raise Exception('Ollama is not running - start with `ollama start`')
		except Exception:
			raise Exception('Ollama is not running - start with `ollama start`')

	agent = Agent(
		task="Search Google for 'elon musk' then click on the first result and scroll down.",
		llm=llm,
		browser_context=context,
		max_failures=2,
		use_vision=use_vision,
	)
	history: AgentHistoryList = await agent.run(max_steps=2)
	done = history.is_done()
	successful = history.is_successful()
	action_names = history.action_names()
	print(f'Actions performed: {action_names}')
	errors = [e for e in history.errors() if e is not None]
	errors = '\n'.join(errors)
	passed = False
	if 'search_google' in action_names:
		passed = True
	elif 'go_to_url' in action_names:
		passed = True
	elif 'open_tab' in action_names:
		passed = True

	else:
		passed = False
	print(f'Model {model_name}: {"✅ PASSED - " if passed else "❌ FAILED - "} Done: {done} Successful: {successful}')

	assert passed, f'Model {model_name} not working\nActions performed: {action_names}\nErrors: {errors}'
````

## File: tests/test_qwen.py
````python
import asyncio

import pytest
from langchain_ollama import ChatOllama

from browser_use.agent.service import Agent
from browser_use.agent.views import AgentHistoryList
from browser_use.browser.browser import Browser, BrowserConfig


@pytest.fixture
def llm():
	"""Initialize language model for testing"""

	# return ChatAnthropic(model_name='claude-3-5-sonnet-20240620', timeout=25, stop=None)
	# NOTE: Make sure to run ollama server with `ollama start'
	return ChatOllama(
		model='qwen2.5:latest',
		num_ctx=128000,
	)


@pytest.fixture(scope='session')
def event_loop():
	"""Create an instance of the default event loop for each test case."""
	loop = asyncio.get_event_loop_policy().new_event_loop()
	yield loop
	loop.close()


@pytest.fixture(scope='session')
async def browser(event_loop):
	browser_instance = Browser(
		config=BrowserConfig(
			headless=True,
		)
	)
	yield browser_instance
	await browser_instance.close()


@pytest.fixture
async def context(browser):
	async with await browser.new_context() as context:
		yield context


# pytest tests/test_qwen.py -v -k "test_qwen_url" --capture=no
# @pytest.mark.asyncio
async def test_qwen_url(llm, context):
	"""Test complex ecommerce interaction sequence"""
	agent = Agent(
		task='go_to_url amazon.com',
		llm=llm,
	)

	history: AgentHistoryList = await agent.run(max_steps=3)

	# Verify sequence of actions
	action_sequence = []
	for action in history.model_actions():
		action_name = list(action.keys())[0]
		if action_name in ['go_to_url', 'open_tab']:
			action_sequence.append('navigate')

	assert 'navigate' in action_sequence  # Navigated to Amazon
````

## File: tests/test_react_dropdown.py
````python
"""
Simple try of the agent.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import os
import sys

from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from langchain_openai import ChatOpenAI

from browser_use import Agent, AgentHistoryList

llm = ChatOpenAI(model='gpt-4o')
# browser = Browser(config=BrowserConfig(headless=False))

agent = Agent(
	task=(
		'go to https://codepen.io/shyam-king/pen/ByBJoOv and select "Tiger" dropdown and read the text given in "Selected Animal" box (it can be empty as well)'
	),
	llm=llm,
	browser_context=BrowserContext(
		browser=Browser(config=BrowserConfig(headless=False, disable_security=True)),
	),
)


async def test_dropdown():
	history: AgentHistoryList = await agent.run(10)
	# await controller.browser.close(force=True)

	result = history.final_result()
	assert result is not None
	print('result: ', result)
	# await browser.close()


if __name__ == '__main__':
	asyncio.run(test_dropdown())
````

## File: tests/test_save_conversation.py
````python
"""
Simple try of the agent.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import os
import shutil
import sys

from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI

from browser_use import Agent, AgentHistoryList

llm = ChatOpenAI(model='gpt-4o')


async def test_save_conversation_contains_slash():
	if os.path.exists('./logs'):
		shutil.rmtree('./logs')

	agent = Agent(
		task=('go to google.com and search for text "hi there"'),
		llm=llm,
		browser_context=BrowserContext(
			browser=Browser(config=BrowserConfig(headless=False, disable_security=True)),
		),
		save_conversation_path='logs/conversation',
	)
	history: AgentHistoryList = await agent.run(20)

	result = history.final_result()
	assert result is not None

	assert os.path.exists('./logs'), 'logs directory was not created'
	assert os.path.exists('./logs/conversation_2.txt'), 'logs file was not created'


async def test_save_conversation_not_contains_slash():
	if os.path.exists('./logs'):
		shutil.rmtree('./logs')

	agent = Agent(
		task=('go to google.com and search for text "hi there"'),
		llm=llm,
		browser_context=BrowserContext(
			browser=Browser(config=BrowserConfig(headless=False, disable_security=True)),
		),
		save_conversation_path='logs',
	)
	history: AgentHistoryList = await agent.run(20)

	result = history.final_result()
	assert result is not None

	assert os.path.exists('./logs'), 'logs directory was not created'
	assert os.path.exists('./logs/_2.txt'), 'logs file was not created'


async def test_save_conversation_deep_directory():
	if os.path.exists('./logs'):
		shutil.rmtree('./logs')

	agent = Agent(
		task=('go to google.com and search for text "hi there"'),
		llm=llm,
		browser_context=BrowserContext(
			browser=Browser(config=BrowserConfig(headless=False, disable_security=True)),
		),
		save_conversation_path='logs/deep/directory/conversation',
	)
	history: AgentHistoryList = await agent.run(20)

	result = history.final_result()
	assert result is not None

	assert os.path.exists('./logs/deep/directory'), 'logs directory was not created'
	assert os.path.exists('./logs/deep/directory/conversation_2.txt'), 'logs file was not created'
````

## File: tests/test_self_registered_actions.py
````python
import asyncio
import os

import pytest
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, SecretStr

from browser_use.agent.service import Agent
from browser_use.agent.views import AgentHistoryList
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.controller.service import Controller


@pytest.fixture(scope='session')
def event_loop():
	loop = asyncio.get_event_loop_policy().new_event_loop()
	yield loop
	loop.close()


@pytest.fixture(scope='session')
async def browser(event_loop):
	browser_instance = Browser(
		config=BrowserConfig(
			headless=True,
		)
	)
	yield browser_instance
	await browser_instance.close()


@pytest.fixture
async def context(browser):
	async with await browser.new_context() as context:
		yield context


@pytest.fixture
async def controller():
	"""Initialize the controller with self-registered actions"""
	controller = Controller()

	# Define custom actions without Pydantic models
	@controller.action('Print a message')
	def print_message(message: str):
		print(f'Message: {message}')
		return f'Printed message: {message}'

	@controller.action('Add two numbers')
	def add_numbers(a: int, b: int):
		result = a + b
		return f'The sum is {result}'

	@controller.action('Concatenate strings')
	def concatenate_strings(str1: str, str2: str):
		result = str1 + str2
		return f'Concatenated string: {result}'

	# Define Pydantic models
	class SimpleModel(BaseModel):
		name: str
		age: int

	class Address(BaseModel):
		street: str
		city: str

	class NestedModel(BaseModel):
		user: SimpleModel
		address: Address

	# Add actions with Pydantic model arguments
	@controller.action('Process simple model', param_model=SimpleModel)
	def process_simple_model(model: SimpleModel):
		return f'Processed {model.name}, age {model.age}'

	@controller.action('Process nested model', param_model=NestedModel)
	def process_nested_model(model: NestedModel):
		user_info = f'{model.user.name}, age {model.user.age}'
		address_info = f'{model.address.street}, {model.address.city}'
		return f'Processed user {user_info} at address {address_info}'

	@controller.action('Process multiple models')
	def process_multiple_models(model1: SimpleModel, model2: Address):
		return f'Processed {model1.name} living at {model2.street}, {model2.city}'

	yield controller


@pytest.fixture
def llm():
	"""Initialize language model for testing"""

	# return ChatAnthropic(model_name='claude-3-5-sonnet-20240620', timeout=25, stop=None)
	return AzureChatOpenAI(
		model='gpt-4o',
		api_version='2024-10-21',
		azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
		api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', '')),
	)


# @pytest.mark.skip(reason="Skipping test for now")
@pytest.mark.asyncio
async def test_self_registered_actions_no_pydantic(llm, controller):
	"""Test self-registered actions with individual arguments"""
	agent = Agent(
		task="First, print the message 'Hello, World!'. Then, add 10 and 20. Next, concatenate 'foo' and 'bar'.",
		llm=llm,
		controller=controller,
	)
	history: AgentHistoryList = await agent.run(max_steps=10)
	# Check that custom actions were executed
	action_names = history.action_names()

	assert 'print_message' in action_names
	assert 'add_numbers' in action_names
	assert 'concatenate_strings' in action_names


# @pytest.mark.skip(reason="Skipping test for now")
@pytest.mark.asyncio
async def test_mixed_arguments_actions(llm, controller):
	"""Test actions with mixed argument types"""

	# Define another action during the test
	# Test for async actions
	@controller.action('Calculate the area of a rectangle')
	async def calculate_area(length: float, width: float):
		area = length * width
		return f'The area is {area}'

	agent = Agent(
		task='Calculate the area of a rectangle with length 5.5 and width 3.2.',
		llm=llm,
		controller=controller,
	)
	history = await agent.run(max_steps=5)

	# Check that the action was executed
	action_names = history.action_names()

	assert 'calculate_area' in action_names
	# check result
	correct = 'The area is 17.6'
	for content in history.extracted_content():
		if correct in content:
			break
	else:
		pytest.fail(f'{correct} not found in extracted content')


@pytest.mark.asyncio
async def test_pydantic_simple_model(llm, controller):
	"""Test action with a simple Pydantic model argument"""
	agent = Agent(
		task="Process a simple model with name 'Alice' and age 30.",
		llm=llm,
		controller=controller,
	)
	history = await agent.run(max_steps=5)

	# Check that the action was executed
	action_names = history.action_names()

	assert 'process_simple_model' in action_names
	correct = 'Processed Alice, age 30'
	for content in history.extracted_content():
		if correct in content:
			break
	else:
		pytest.fail(f'{correct} not found in extracted content')


@pytest.mark.asyncio
async def test_pydantic_nested_model(llm, controller):
	"""Test action with a nested Pydantic model argument"""
	agent = Agent(
		task="Process a nested model with user name 'Bob', age 25, living at '123 Maple St', 'Springfield'.",
		llm=llm,
		controller=controller,
	)
	history = await agent.run(max_steps=5)

	# Check that the action was executed
	action_names = history.action_names()

	assert 'process_nested_model' in action_names
	correct = 'Processed user Bob, age 25 at address 123 Maple St, Springfield'
	for content in history.extracted_content():
		if correct in content:
			break
	else:
		pytest.fail(f'{correct} not found in extracted content')


# run this file with:
# pytest tests/test_self_registered_actions.py --capture=no
````

## File: tests/test_stress.py
````python
import asyncio
import os
import random
import string
import time

import pytest
from langchain_openai import AzureChatOpenAI
from pydantic import SecretStr

from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.controller.service import Controller


@pytest.fixture(scope='session')
def event_loop():
	loop = asyncio.get_event_loop_policy().new_event_loop()
	yield loop
	loop.close()


@pytest.fixture(scope='session')
async def browser(event_loop):
	browser_instance = Browser(
		config=BrowserConfig(
			headless=True,
		)
	)
	yield browser_instance
	await browser_instance.close()


@pytest.fixture
async def context(browser):
	async with await browser.new_context() as context:
		yield context


@pytest.fixture
def llm():
	"""Initialize the language model"""
	model = AzureChatOpenAI(
		api_version='2024-10-21',
		model='gpt-4o',
		azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
		api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', '')),
	)
	return model


def generate_random_text(length: int) -> str:
	"""Generate random text of specified length"""
	return ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=length))


@pytest.fixture
async def controller():
	"""Initialize the controller"""
	controller = Controller()
	large_text = generate_random_text(10000)

	@controller.action('call this magical function to get very special text')
	def get_very_special_text():
		return large_text

	yield controller


@pytest.mark.asyncio
async def test_token_limit_with_multiple_extractions(llm, controller, context):
	"""Test handling of multiple smaller extractions accumulating tokens"""
	agent = Agent(
		task='Call the magical function to get very special text 5 times',
		llm=llm,
		controller=controller,
		browser_context=context,
		max_input_tokens=2000,
		save_conversation_path='tmp/stress_test/test_token_limit_with_multiple_extractions.json',
	)

	history = await agent.run(max_steps=5)

	# check if 5 times called get_special_text
	calls = [a for a in history.action_names() if a == 'get_very_special_text']
	assert len(calls) == 5
	# check the message history should be max 3 messages
	assert len(agent.message_manager.history.messages) > 3


@pytest.mark.slow
@pytest.mark.parametrize('max_tokens', [4000])  # 8000 20000
@pytest.mark.asyncio
async def test_open_3_tabs_and_extract_content(llm, controller, context, max_tokens):
	"""Stress test: Open 3 tabs with urls and extract content"""
	agent = Agent(
		task='Open 3 tabs with https://en.wikipedia.org/wiki/Internet and extract the content from each.',
		llm=llm,
		controller=controller,
		browser_context=context,
		max_input_tokens=max_tokens,
		save_conversation_path='tmp/stress_test/test_open_3_tabs_and_extract_content.json',
	)
	start_time = time.time()
	history = await agent.run(max_steps=7)
	end_time = time.time()

	total_time = end_time - start_time

	print(f'Total time: {total_time:.2f} seconds')
	# Check for errors
	errors = history.errors()
	assert len(errors) == 0, 'Errors occurred during the test'
	# check if 3 tabs were opened
	assert len(context.current_state.tabs) >= 3, '3 tabs were not opened'
````

## File: tests/test_wait_for_element.py
````python
import asyncio
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
	sys.path.insert(0, project_root)

import pytest
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Third-party imports
from browser_use import Agent, Controller

# Local imports
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

# Load environment variables.
load_dotenv()

# Initialize language model and controller.
llm = ChatOpenAI(model='gpt-4o')
controller = Controller()


@pytest.mark.skip(reason='this is for local testing only')
async def test_wait_for_element():
	"""Test 'Wait for element' action."""

	initial_actions = [
		{'open_tab': {'url': 'https://pypi.org/'}},
		# Uncomment the line below to include the wait action in initial actions.
		# {'wait_for_element': {'selector': '#search', 'timeout': 30}},
	]

	# Set up the browser context.
	context = BrowserContext(
		browser=Browser(config=BrowserConfig(headless=False, disable_security=True)),
	)

	# Create the agent with the task.
	agent = Agent(
		task="Wait for element '#search' to be visible with a timeout of 30 seconds.",
		llm=llm,
		browser_context=context,
		initial_actions=initial_actions,
		controller=controller,
	)

	# Run the agent for a few steps to trigger navigation and then the wait action.
	history = await agent.run(max_steps=3)
	action_names = history.action_names()

	# Ensure that the wait_for_element action was executed.
	assert 'wait_for_element' in action_names, 'Expected wait_for_element action to be executed.'

	# Verify that the #search element is visible by querying the page.
	page = await context.get_current_page()
	header_handle = await page.query_selector('#search')
	assert header_handle is not None, 'Expected to find a #search element on the page.'
	is_visible = await header_handle.is_visible()
	assert is_visible, 'Expected the #search element to be visible.'


if __name__ == '__main__':
	asyncio.run(test_wait_for_element())
````

## File: .github/workflows/package.yaml
````yaml
name: package
on:
  push:
    branches:
      - main
      - stable
      - 'releases/**'
    tags:
      - '*'
  pull_request:
  workflow_dispatch:

jobs:
  build:
    name: pip-build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv build --python 3.12
      - uses: actions/upload-artifact@v4
        with:
          name: dist-artifact
          path: |
            dist/*.whl
            dist/*.tar.gz

  build_test:
    name: pip-install-on-${{ matrix.os }}-py-${{ matrix.python-version }}
    needs: build
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - uses: actions/download-artifact@v4
        with:
          name: dist-artifact

      - name: Set up venv and test for OS/Python versions
        shell: bash
        run: |
          uv venv /tmp/testenv --python ${{ matrix.python-version }}
          if [[ "$RUNNER_OS" == "Windows" ]]; then
            . /tmp/testenv/Scripts/activate
          else
            source /tmp/testenv/bin/activate
          fi
          uv pip install *.whl
          python -c 'from browser_use import Agent, Browser, Controller, ActionModel, ActionResult'
````

## File: browser_use/agent/message_manager/service.py
````python
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from langchain_core.messages import (
	AIMessage,
	BaseMessage,
	HumanMessage,
	SystemMessage,
	ToolMessage,
)
from pydantic import BaseModel

from browser_use.agent.message_manager.views import MessageMetadata
from browser_use.agent.prompts import AgentMessagePrompt
from browser_use.agent.views import ActionResult, AgentOutput, AgentStepInfo, MessageManagerState
from browser_use.browser.views import BrowserState
from browser_use.utils import time_execution_sync

logger = logging.getLogger(__name__)


class MessageManagerSettings(BaseModel):
	max_input_tokens: int = 128000
	estimated_characters_per_token: int = 3
	image_tokens: int = 800
	include_attributes: list[str] = []
	message_context: Optional[str] = None
	sensitive_data: Optional[Dict[str, str]] = None
	available_file_paths: Optional[List[str]] = None


class MessageManager:
	def __init__(
		self,
		task: str,
		system_message: SystemMessage,
		settings: MessageManagerSettings = MessageManagerSettings(),
		state: MessageManagerState = MessageManagerState(),
	):
		self.task = task
		self.settings = settings
		self.state = state
		self.system_prompt = system_message

		# Only initialize messages if state is empty
		if len(self.state.history.messages) == 0:
			self._init_messages()

	def _init_messages(self) -> None:
		"""Initialize the message history with system message, context, task, and other initial messages"""
		self._add_message_with_tokens(self.system_prompt, message_type='init')

		if self.settings.message_context:
			context_message = HumanMessage(content='Context for the task' + self.settings.message_context)
			self._add_message_with_tokens(context_message, message_type='init')

		task_message = HumanMessage(
			content=f'Your ultimate task is: """{self.task}""". If you achieved your ultimate task, stop everything and use the done action in the next step to complete the task. If not, continue as usual.'
		)
		self._add_message_with_tokens(task_message, message_type='init')

		if self.settings.sensitive_data:
			info = f'Here are placeholders for sensitive data: {list(self.settings.sensitive_data.keys())}'
			info += 'To use them, write <secret>the placeholder name</secret>'
			info_message = HumanMessage(content=info)
			self._add_message_with_tokens(info_message, message_type='init')

		placeholder_message = HumanMessage(content='Example output:')
		self._add_message_with_tokens(placeholder_message, message_type='init')

		example_tool_call = AIMessage(
			content='',
			tool_calls=[
				{
					'name': 'AgentOutput',
					'args': {
						'current_state': {
							'evaluation_previous_goal': """
							Success - I successfully clicked on the 'Apple' link from the Google Search results page, 
							which directed me to the 'Apple' company homepage. This is a good start toward finding 
							the best place to buy a new iPhone as the Apple website often list iPhones for sale.
						""".strip(),
							'memory': """
							I searched for 'iPhone retailers' on Google. From the Google Search results page, 
							I used the 'click_element_by_index' tool to click on element at index [45] labeled 'Best Buy' but calling 
							the tool did not direct me to a new page. I then used the 'click_element_by_index' tool to click 
							on element at index [82] labeled 'Apple' which redirected me to the 'Apple' company homepage. 
							Currently at step 3/15.
						""".strip(),
							'next_goal': """
							Looking at reported structure of the current page, I can see the item '[127]<h3 iPhone/>' 
							in the content. I think this button will lead to more information and potentially prices 
							for iPhones. I'll click on the link at index [127] using the 'click_element_by_index' 
							tool and hope to see prices on the next page.
						""".strip(),
						},
						'action': [{'click_element_by_index': {'index': 127}}],
					},
					'id': str(self.state.tool_id),
					'type': 'tool_call',
				},
			],
		)
		self._add_message_with_tokens(example_tool_call, message_type='init')
		self.add_tool_message(content='Browser started', message_type='init')

		placeholder_message = HumanMessage(content='[Your task history memory starts here]')
		self._add_message_with_tokens(placeholder_message)

		if self.settings.available_file_paths:
			filepaths_msg = HumanMessage(content=f'Here are file paths you can use: {self.settings.available_file_paths}')
			self._add_message_with_tokens(filepaths_msg, message_type='init')

	def add_new_task(self, new_task: str) -> None:
		content = f'Your new ultimate task is: """{new_task}""". Take the previous context into account and finish your new ultimate task. '
		msg = HumanMessage(content=content)
		self._add_message_with_tokens(msg)
		self.task = new_task

	@time_execution_sync('--add_state_message')
	def add_state_message(
		self,
		state: BrowserState,
		result: Optional[List[ActionResult]] = None,
		step_info: Optional[AgentStepInfo] = None,
		use_vision=True,
	) -> None:
		"""Add browser state as human message"""


		print('add_state_message POOP: ',self.state)
		# if keep in memory, add to directly to history and add state without result
		if result:
			for r in result:
				if r.include_in_memory:
					if r.extracted_content:
						msg = HumanMessage(content='Action result: ' + str(r.extracted_content))
						self._add_message_with_tokens(msg)
					if r.error:
						# if endswith \n, remove it
						if r.error.endswith('\n'):
							r.error = r.error[:-1]
						# get only last line of error
						last_line = r.error.split('\n')[-1]
						msg = HumanMessage(content='Action error: ' + last_line)
						self._add_message_with_tokens(msg)
					result = None  # if result in history, we dont want to add it again

		# otherwise add state message and result to next message (which will not stay in memory)
		state_message = AgentMessagePrompt(
			state,
			result,
			include_attributes=self.settings.include_attributes,
			step_info=step_info,
		).get_user_message(use_vision)
		self._add_message_with_tokens(state_message)

	def add_model_output(self, model_output: AgentOutput) -> None:
		"""Add model output as AI message"""
		tool_calls = [
			{
				'name': 'AgentOutput',
				'args': model_output.model_dump(mode='json', exclude_unset=True),
				'id': str(self.state.tool_id),
				'type': 'tool_call',
			}
		]

		msg = AIMessage(
			content='',
			tool_calls=tool_calls,
		)

		self._add_message_with_tokens(msg)
		# empty tool response
		self.add_tool_message(content='')

	def add_plan(self, plan: Optional[str], position: int | None = None) -> None:
		if plan:
			msg = AIMessage(content=plan)
			self._add_message_with_tokens(msg, position)

	@time_execution_sync('--get_messages')
	def get_messages(self) -> List[BaseMessage]:
		"""Get current message list, potentially trimmed to max tokens"""

		msg = [m.message for m in self.state.history.messages]
		# debug which messages are in history with token count # log
		total_input_tokens = 0
		logger.debug(f'Messages in history: {len(self.state.history.messages)}:')
		for m in self.state.history.messages:
			total_input_tokens += m.metadata.tokens
			logger.debug(f'{m.message.__class__.__name__} - Token count: {m.metadata.tokens}')
		logger.debug(f'Total input tokens: {total_input_tokens}')

		return msg

	def _add_message_with_tokens(
		self, message: BaseMessage, position: int | None = None, message_type: str | None = None
	) -> None:
		"""Add message with token count metadata
		position: None for last, -1 for second last, etc.
		"""

		# filter out sensitive data from the message
		if self.settings.sensitive_data:
			message = self._filter_sensitive_data(message)

		token_count = self._count_tokens(message)
		metadata = MessageMetadata(tokens=token_count, message_type=message_type)
		self.state.history.add_message(message, metadata, position)

	@time_execution_sync('--filter_sensitive_data')
	def _filter_sensitive_data(self, message: BaseMessage) -> BaseMessage:
		"""Filter out sensitive data from the message"""

		def replace_sensitive(value: str) -> str:
			if not self.settings.sensitive_data:
				return value
			for key, val in self.settings.sensitive_data.items():
				if not val:
					continue
				value = value.replace(val, f'<secret>{key}</secret>')
			return value

		if isinstance(message.content, str):
			message.content = replace_sensitive(message.content)
		elif isinstance(message.content, list):
			for i, item in enumerate(message.content):
				if isinstance(item, dict) and 'text' in item:
					item['text'] = replace_sensitive(item['text'])
					message.content[i] = item
		return message

	def _count_tokens(self, message: BaseMessage) -> int:
		"""Count tokens in a message using the model's tokenizer"""
		tokens = 0
		if isinstance(message.content, list):
			for item in message.content:
				if 'image_url' in item:
					tokens += self.settings.image_tokens
				elif isinstance(item, dict) and 'text' in item:
					tokens += self._count_text_tokens(item['text'])
		else:
			msg = message.content
			if hasattr(message, 'tool_calls'):
				msg += str(message.tool_calls)  # type: ignore
			tokens += self._count_text_tokens(msg)
		return tokens

	def _count_text_tokens(self, text: str) -> int:
		"""Count tokens in a text string"""
		tokens = len(text) // self.settings.estimated_characters_per_token  # Rough estimate if no tokenizer available
		return tokens

	def cut_messages(self):
		"""Get current message list, potentially trimmed to max tokens"""
		diff = self.state.history.current_tokens - self.settings.max_input_tokens
		if diff <= 0:
			return None

		msg = self.state.history.messages[-1]

		# if list with image remove image
		if isinstance(msg.message.content, list):
			text = ''
			for item in msg.message.content:
				if 'image_url' in item:
					msg.message.content.remove(item)
					diff -= self.settings.image_tokens
					msg.metadata.tokens -= self.settings.image_tokens
					self.state.history.current_tokens -= self.settings.image_tokens
					logger.debug(
						f'Removed image with {self.settings.image_tokens} tokens - total tokens now: {self.state.history.current_tokens}/{self.settings.max_input_tokens}'
					)
				elif 'text' in item and isinstance(item, dict):
					text += item['text']
			msg.message.content = text
			self.state.history.messages[-1] = msg

		if diff <= 0:
			return None

		# if still over, remove text from state message proportionally to the number of tokens needed with buffer
		# Calculate the proportion of content to remove
		proportion_to_remove = diff / msg.metadata.tokens
		if proportion_to_remove > 0.99:
			raise ValueError(
				f'Max token limit reached - history is too long - reduce the system prompt or task. '
				f'proportion_to_remove: {proportion_to_remove}'
			)
		logger.debug(
			f'Removing {proportion_to_remove * 100:.2f}% of the last message  {proportion_to_remove * msg.metadata.tokens:.2f} / {msg.metadata.tokens:.2f} tokens)'
		)

		content = msg.message.content
		characters_to_remove = int(len(content) * proportion_to_remove)
		content = content[:-characters_to_remove]

		# remove tokens and old long message
		self.state.history.remove_last_state_message()

		# new message with updated content
		msg = HumanMessage(content=content)
		self._add_message_with_tokens(msg)

		last_msg = self.state.history.messages[-1]

		logger.debug(
			f'Added message with {last_msg.metadata.tokens} tokens - total tokens now: {self.state.history.current_tokens}/{self.settings.max_input_tokens} - total messages: {len(self.state.history.messages)}'
		)

	def _remove_last_state_message(self) -> None:
		"""Remove last state message from history"""
		self.state.history.remove_last_state_message()

	def add_tool_message(self, content: str, message_type: str | None = None) -> None:
		"""Add tool message to history"""
		msg = ToolMessage(content=content, tool_call_id=str(self.state.tool_id))
		self.state.tool_id += 1
		self._add_message_with_tokens(msg, message_type=message_type)
````

## File: browser_use/controller/registry/service.py
````python
import asyncio
from inspect import iscoroutinefunction, signature
from typing import Any, Callable, Dict, Generic, Optional, Type, TypeVar

from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import BaseModel, Field, create_model

from browser_use.browser.context import BrowserContext
from browser_use.controller.registry.views import (
	ActionModel,
	ActionRegistry,
	RegisteredAction,
)
from browser_use.telemetry.service import ProductTelemetry
from browser_use.telemetry.views import (
	ControllerRegisteredFunctionsTelemetryEvent,
	RegisteredFunction,
)
from browser_use.utils import time_execution_async

Context = TypeVar('Context')


class Registry(Generic[Context]):
	"""Service for registering and managing actions"""

	def __init__(self, exclude_actions: list[str] | None = None):
		self.registry = ActionRegistry()
		self.telemetry = ProductTelemetry()
		self.exclude_actions = exclude_actions if exclude_actions is not None else []

	# @time_execution_sync('--create_param_model')
	def _create_param_model(self, function: Callable) -> Type[BaseModel]:
		"""Creates a Pydantic model from function signature"""
		sig = signature(function)
		params = {
			name: (param.annotation, ... if param.default == param.empty else param.default)
			for name, param in sig.parameters.items()
			if name != 'browser' and name != 'page_extraction_llm' and name != 'available_file_paths'
		}
		# TODO: make the types here work
		return create_model(
			f'{function.__name__}_parameters',
			__base__=ActionModel,
			**params,  # type: ignore
		)

	def action(
		self,
		description: str,
		param_model: Optional[Type[BaseModel]] = None,
		domains: Optional[list[str]] = None,
		page_filter: Optional[Callable[[Any], bool]] = None,
	):
		"""Decorator for registering actions"""

		def decorator(func: Callable):
			# Skip registration if action is in exclude_actions
			if func.__name__ in self.exclude_actions:
				return func

			# Create param model from function if not provided
			actual_param_model = param_model or self._create_param_model(func)

			# Wrap sync functions to make them async
			if not iscoroutinefunction(func):

				async def async_wrapper(*args, **kwargs):
					return await asyncio.to_thread(func, *args, **kwargs)

				# Copy the signature and other metadata from the original function
				async_wrapper.__signature__ = signature(func)
				async_wrapper.__name__ = func.__name__
				async_wrapper.__annotations__ = func.__annotations__
				wrapped_func = async_wrapper
			else:
				wrapped_func = func

			action = RegisteredAction(
				name=func.__name__,
				description=description,
				function=wrapped_func,
				param_model=actual_param_model,
				domains=domains,
				page_filter=page_filter,
			)
			self.registry.actions[func.__name__] = action
			return func

		return decorator

	@time_execution_async('--execute_action')
	async def execute_action(
		self,
		action_name: str,
		params: dict,
		browser: Optional[BrowserContext] = None,
		page_extraction_llm: Optional[BaseChatModel] = None,
		sensitive_data: Optional[Dict[str, str]] = None,
		available_file_paths: Optional[list[str]] = None,
		#
		context: Context | None = None,
	) -> Any:
		"""Execute a registered action"""
		if action_name not in self.registry.actions:
			raise ValueError(f'Action {action_name} not found')

		action = self.registry.actions[action_name]
		try:
			# Create the validated Pydantic model
			validated_params = action.param_model(**params)

			# Check if the first parameter is a Pydantic model
			sig = signature(action.function)
			parameters = list(sig.parameters.values())
			is_pydantic = parameters and issubclass(parameters[0].annotation, BaseModel)
			parameter_names = [param.name for param in parameters]

			if sensitive_data:
				validated_params = self._replace_sensitive_data(validated_params, sensitive_data)

			# Check if the action requires browser
			if 'browser' in parameter_names and not browser:
				raise ValueError(f'Action {action_name} requires browser but none provided.')
			if 'page_extraction_llm' in parameter_names and not page_extraction_llm:
				raise ValueError(f'Action {action_name} requires page_extraction_llm but none provided.')
			if 'available_file_paths' in parameter_names and not available_file_paths:
				raise ValueError(f'Action {action_name} requires available_file_paths but none provided.')

			if 'context' in parameter_names and not context:
				raise ValueError(f'Action {action_name} requires context but none provided.')

			# Prepare arguments based on parameter type
			extra_args = {}
			if 'context' in parameter_names:
				extra_args['context'] = context
			if 'browser' in parameter_names:
				extra_args['browser'] = browser
			if 'page_extraction_llm' in parameter_names:
				extra_args['page_extraction_llm'] = page_extraction_llm
			if 'available_file_paths' in parameter_names:
				extra_args['available_file_paths'] = available_file_paths
			if action_name == 'input_text' and sensitive_data:
				extra_args['has_sensitive_data'] = True
			if is_pydantic:
				return await action.function(validated_params, **extra_args)
			return await action.function(**validated_params.model_dump(), **extra_args)

		except Exception as e:
			raise RuntimeError(f'Error executing action {action_name}: {str(e)}') from e

	def _replace_sensitive_data(self, params: BaseModel, sensitive_data: Dict[str, str]) -> BaseModel:
		"""Replaces the sensitive data in the params"""
		# if there are any str with <secret>placeholder</secret> in the params, replace them with the actual value from sensitive_data

		import re

		secret_pattern = re.compile(r'<secret>(.*?)</secret>')

		def replace_secrets(value):
			if isinstance(value, str):
				matches = secret_pattern.findall(value)
				for placeholder in matches:
					if placeholder in sensitive_data:
						value = value.replace(f'<secret>{placeholder}</secret>', sensitive_data[placeholder])
				return value
			elif isinstance(value, dict):
				return {k: replace_secrets(v) for k, v in value.items()}
			elif isinstance(value, list):
				return [replace_secrets(v) for v in value]
			return value

		params_dump = params.model_dump()
		processed_params = replace_secrets(params_dump)
		return type(params).model_validate(processed_params)

	# @time_execution_sync('--create_action_model')
	def create_action_model(self, include_actions: Optional[list[str]] = None, page=None) -> Type[ActionModel]:
		"""Creates a Pydantic model from registered actions, used by LLM APIs that support tool calling & enforce a schema"""

		# Filter actions based on page if provided:
		#   if page is None, only include actions with no filters
		#   if page is provided, only include actions that match the page

		available_actions = {}
		for name, action in self.registry.actions.items():
			if include_actions is not None and name not in include_actions:
				continue

			# If no page provided, only include actions with no filters
			if page is None:
				if action.page_filter is None and action.domains is None:
					available_actions[name] = action
				continue

			# Check page_filter if present
			domain_is_allowed = self.registry._match_domains(action.domains, page.url)
			page_is_allowed = self.registry._match_page_filter(action.page_filter, page)

			# Include action if both filters match (or if either is not present)
			if domain_is_allowed and page_is_allowed:
				available_actions[name] = action

		fields = {
			name: (
				Optional[action.param_model],
				Field(default=None, description=action.description),
			)
			for name, action in available_actions.items()
		}

		self.telemetry.capture(
			ControllerRegisteredFunctionsTelemetryEvent(
				registered_functions=[
					RegisteredFunction(name=name, params=action.param_model.model_json_schema())
					for name, action in available_actions.items()
				]
			)
		)

		return create_model('ActionModel', __base__=ActionModel, **fields)  # type:ignore

	def get_prompt_description(self, page=None) -> str:
		"""Get a description of all actions for the prompt

		If page is provided, only include actions that are available for that page
		based on their filter_func
		"""
		return self.registry.get_prompt_description(page=page)
````

## File: browser_use/telemetry/service.py
````python
import logging
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from posthog import Posthog

from browser_use.telemetry.views import BaseTelemetryEvent
from browser_use.utils import singleton

load_dotenv()


logger = logging.getLogger(__name__)


POSTHOG_EVENT_SETTINGS = {
	'process_person_profile': True,
}


def xdg_cache_home() -> Path:
	default = Path.home() / '.cache'
	env_var = os.getenv('XDG_CACHE_HOME')
	if env_var and (path := Path(env_var)).is_absolute():
		return path
	return default


@singleton
class ProductTelemetry:
	"""
	Service for capturing anonymized telemetry data.

	If the environment variable `ANONYMIZED_TELEMETRY=False`, anonymized telemetry will be disabled.
	"""

	USER_ID_PATH = str(xdg_cache_home() / 'browser_use' / 'telemetry_user_id')
	PROJECT_API_KEY = 'phc_F8JMNjW1i2KbGUTaW1unnDdLSPCoyc52SGRU0JecaUh'
	HOST = 'https://eu.i.posthog.com'
	UNKNOWN_USER_ID = 'UNKNOWN'

	_curr_user_id = None

	def __init__(self) -> None:
		telemetry_disabled = os.getenv('ANONYMIZED_TELEMETRY', 'true').lower() == 'false'
		self.debug_logging = os.getenv('BROWSER_USE_LOGGING_LEVEL', 'info').lower() == 'debug'

		if telemetry_disabled:
			self._posthog_client = None
		else:
			logger.info(
				'Anonymized telemetry enabled. See https://docs.browser-use.com/development/telemetry for more information.'
			)
			self._posthog_client = Posthog(
				project_api_key=self.PROJECT_API_KEY,
				host=self.HOST,
				disable_geoip=False,
				enable_exception_autocapture=True,
			)

			# Silence posthog's logging
			if not self.debug_logging:
				posthog_logger = logging.getLogger('posthog')
				posthog_logger.disabled = True

		if self._posthog_client is None:
			logger.debug('Telemetry disabled')

	def capture(self, event: BaseTelemetryEvent) -> None:
		if self._posthog_client is None:
			return

		if self.debug_logging:
			logger.debug(f'Telemetry event: {event.name} {event.properties}')
		self._direct_capture(event)

	def _direct_capture(self, event: BaseTelemetryEvent) -> None:
		"""
		Should not be thread blocking because posthog magically handles it
		"""
		if self._posthog_client is None:
			return

		try:
			self._posthog_client.capture(
				self.user_id,
				event.name,
				{**event.properties, **POSTHOG_EVENT_SETTINGS},
			)
		except Exception as e:
			logger.error(f'Failed to send telemetry event {event.name}: {e}')

	@property
	def user_id(self) -> str:
		if self._curr_user_id:
			return self._curr_user_id

		# File access may fail due to permissions or other reasons. We don't want to
		# crash so we catch all exceptions.
		try:
			if not os.path.exists(self.USER_ID_PATH):
				os.makedirs(os.path.dirname(self.USER_ID_PATH), exist_ok=True)
				with open(self.USER_ID_PATH, 'w') as f:
					new_user_id = str(uuid.uuid4())
					f.write(new_user_id)
				self._curr_user_id = new_user_id
			else:
				with open(self.USER_ID_PATH, 'r') as f:
					self._curr_user_id = f.read()
		except Exception:
			self._curr_user_id = 'UNKNOWN_USER_ID'
		return self._curr_user_id
````

## File: docs/development/contribution-guide.mdx
````
---
title: "Contribution Guide"
description: "Learn how to contribute to Browser Use"
icon: "github"
---


- check out our most active issues or ask in [Discord](https://discord.gg/zXJJHtJf3k) for ideas of what to work on
- get inspiration / share what you build in the [`#showcase-your-work`](https://discord.com/channels/1303749220842340412/1305549200678850642) channel and on [`awesome-browser-use-prompts`](https://github.com/browser-use/awesome-prompts)!
- no typo/style-only nit PRs, you can submit nit fixes but only if part of larger bugfix or new feature PRs
- include a demo screenshot/gif, tests, and ideally an example script demonstrating any changes in your PR
- bump your issues/PRs with comments periodically if you want them to be merged faster
````

## File: eval/service.py
````python
# ==============================================================================================================
# Documentation for this evaluation file.
# The import


# Here is the command to run the evaluation:
# python eval/service.py --parallel_runs 5 --parallel_evaluations 5 --max-steps 25 --start 0 --end 100 --model gpt-4o
# options:
# --parallel_runs: Number of parallel tasks to run
# --max-steps: Maximum steps per task
# --start: Start index
# --end: End index (exclusive)
# --headless: Run in headless mode

# Here is the command to run the evaluation only:
# python eval/service.py --evaluate-only
# options:
# --parallel_evaluations: Number of parallel evaluations to run

# ==============================================================================================================


# ==============================================================================================================
# This is the LLM as a judge evaluation system from the OSU-NLP Group paper
# Any adaptiations made should be explicitly stated here:
# Adaptations:
# We are using our langchain wrapper for the OpenAI API
# This means we changed model.generate to model.invoke. The behavior of the model should be identical.
# Added a Online_Mind2Web_eval_with_retry wrapper with retry logic in case of API rate limiting or other issues.


# @article{xue2025illusionprogressassessingcurrent,
#       title={An Illusion of Progress? Assessing the Current State of Web Agents},
#       author={Tianci Xue and Weijian Qi and Tianneng Shi and Chan Hee Song and Boyu Gou and Dawn Song and Huan Sun and Yu Su},
#       year={2025},
#       eprint={2504.01382},
#       archivePrefix={arXiv},
#       primaryClass={cs.AI},
#       url={https://arxiv.org/abs/2504.01382},
# }

# @inproceedings{deng2023mind2web,
#  author = {Deng, Xiang and Gu, Yu and Zheng, Boyuan and Chen, Shijie and Stevens, Sam and Wang, Boshi and Sun, Huan and Su, Yu},
#  booktitle = {Advances in Neural Information Processing Systems},
#  editor = {A. Oh and T. Naumann and A. Globerson and K. Saenko and M. Hardt and S. Levine},
#  pages = {28091--28114},
#  publisher = {Curran Associates, Inc.},
#  title = {Mind2Web: Towards a Generalist Agent for the Web},
#  url = {https://proceedings.neurips.cc/paper_files/paper/2023/file/5950bf290a1570ea401bf98882128160-Paper-Datasets_and_Benchmarks.pdf},
#  volume = {36},
#  year = {2023}
# }
# ==============================================================================================================
import asyncio
import base64
import io
import logging
import re
import shutil

import anyio
from PIL import Image

MAX_IMAGE = 5

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def encode_image(image):
	"""Convert a PIL image to base64 string."""
	if image.mode == 'RGBA':
		image = image.convert('RGB')
	buffered = io.BytesIO()
	image.save(buffered, format='JPEG')
	return base64.b64encode(buffered.getvalue()).decode('utf-8')


async def identify_key_points(task, model):
	system_msg = """You are an expert tasked with analyzing a given task to identify the key points explicitly stated in the task description.

**Objective**: Carefully analyze the task description and extract the critical elements explicitly mentioned in the task for achieving its goal.

**Instructions**:
1. Read the task description carefully.
2. Identify and extract **key points** directly stated in the task description.
   - A **key point** is a critical element, condition, or step explicitly mentioned in the task description.
   - Do not infer or add any unstated elements.
   - Words such as "best," "highest," "cheapest," "latest," "most recent," "lowest," "closest," "highest-rated," "largest," and "newest" must go through the sort function(e.g., the key point should be "Filter by highest").

**Respond with**:
- **Key Points**: A numbered list of the explicit key points for completing this task, one per line, without explanations or additional details."""
	prompt = """Task: {task}"""
	text = prompt.format(task=task)
	messages = [
		{'role': 'system', 'content': system_msg},
		{
			'role': 'user',
			'content': [{'type': 'text', 'text': text}],
		},
	]
	response = await asyncio.to_thread(model.invoke, messages)
	return response.content


async def judge_image(task, image_path, key_points, model):
	system_msg = """You are an expert evaluator tasked with determining whether an image contains information about the necessary steps to complete a task.

**Objective**: Analyze the provided image and decide if it shows essential steps or evidence required for completing the task. Use your reasoning to explain your decision before assigning a score.

**Instructions**:
1. Provide a detailed description of the image, including its contents, visible elements, text (if any), and any notable features.

2. Carefully examine the image and evaluate whether it contains necessary steps or evidence crucial to task completion:  
- Identify key points that could be relevant to task completion, such as actions, progress indicators, tool usage, applied filters, or step-by-step instructions.  
- Does the image show actions, progress indicators, or critical information directly related to completing the task?  
- Is this information indispensable for understanding or ensuring task success?
- If the image contains partial but relevant information, consider its usefulness rather than dismissing it outright.

3. Provide your response in the following format:  
- **Reasoning**: Explain your thought process and observations. Mention specific elements in the image that indicate necessary steps, evidence, or lack thereof.  
- **Score**: Assign a score based on the reasoning, using the following scale:  
    - **1**: The image does not contain any necessary steps or relevant information.  
    - **2**: The image contains minimal or ambiguous information, unlikely to be essential.  
    - **3**: The image includes some relevant steps or hints but lacks clarity or completeness.  
    - **4**: The image contains important steps or evidence that are highly relevant but not fully comprehensive.  
    - **5**: The image clearly displays necessary steps or evidence crucial for completing the task.

Respond with:  
1. **Reasoning**: [Your explanation]  
2. **Score**: [1-5]"""

	jpg_base64_str = encode_image(Image.open(image_path))

	prompt = """**Task**: {task}

**Key Points for Task Completion**: {key_points}

The snapshot of the web page is shown in the image."""
	text = prompt.format(task=task, key_points=key_points)

	messages = [
		{'role': 'system', 'content': system_msg},
		{
			'role': 'user',
			'content': [
				{'type': 'text', 'text': text},
				{
					'type': 'image_url',
					'image_url': {'url': f'data:image/jpeg;base64,{jpg_base64_str}', 'detail': 'high'},
				},
			],
		},
	]
	response = await asyncio.to_thread(model.invoke, messages)
	return response.content


async def Online_Mind2Web_eval(task, last_actions, images_path, model, score_threshold):
	system_msg = """You are an expert in evaluating the performance of a web navigation agent. The agent is designed to help a human user navigate a website to complete a task. Given the user's task, the agent's action history, key points for task completion, some potentially important web pages in the agent's trajectory and their reasons, your goal is to determine whether the agent has completed the task and achieved all requirements.

Your response must strictly follow the following evaluation criteria!
*Important Evaluation Criteria*:
1: The filtered results must be displayed correctly. If filters were not properly applied (i.e., missing selection, missing confirmation, or no visible effect in results), the task is not considered successful.
2: You must carefully check whether these snapshots and action history meet these key points. Ensure that specific filter conditions, such as "best," "highest," "cheapest," "latest," "most recent," "lowest," "closest," "highest-rated," "largest," and "newest" are correctly applied using the filter function(e.g., sort function).
3: Certain key points or requirements should be applied by the filter. Otherwise, a search with all requirements as input will be deemed a failure since it cannot guarantee that all results meet the requirements!
4: If the task requires filtering by a specific range of money, years, or the number of beds and bathrooms, the applied filter must exactly match the given requirement. Any deviation results in failure. To ensure the task is successful, the applied filter must precisely match the specified range without being too broad or too narrow.
Examples of Failure Cases:
- If the requirement is less than $50, but the applied filter is less than $25, it is a failure.
- If the requirement is $1500-$2500, but the applied filter is $2000-$2500, it is a failure.
- If the requirement is $25-$200, but the applied filter is $0-$200, it is a failure.
- If the required years are 2004-2012, but the filter applied is 2001-2012, it is a failure.
- If the required years are before 2015, but the applied filter is 2000-2014, it is a failure.
- If the task requires exactly 2 beds, but the filter applied is 2+ beds, it is a failure.
5: Some tasks require a submission action or a display of results to be considered successful.
6: If the retrieved information is invalid or empty(e.g., No match was found), but the agent has correctly performed the required action, it should still be considered successful.
7: If the current page already displays all available items, then applying a filter is not necessary. As long as the agent selects items that meet the requirements (e.g., the cheapest or lowest price), the task is still considered successful.

*IMPORTANT*
Format your response into two lines as shown below:

Thoughts: <your thoughts and reasoning process based on double-checking each key points and the evaluation criteria>
Status: "success" or "failure"
"""
	prompt = """User Task: {task}

Key Points: {key_points}

Action History:
{last_actions}

The potentially important snapshots of the webpage in the agent's trajectory and their reasons:
{thoughts}"""

	key_points = await identify_key_points(task, model)
	key_points = key_points.replace('\n\n', '\n')

	try:
		key_points = key_points.split('**Key Points**:')[1]
		key_points = '\n'.join(line.lstrip() for line in key_points.splitlines())
	except IndexError:
		key_points = key_points.split('Key Points:')[-1]
		key_points = '\n'.join(line.lstrip() for line in key_points.splitlines())

	tasks = [judge_image(task, image_path, key_points, model) for image_path in images_path]
	image_responses = await asyncio.gather(*tasks)

	whole_content_img = []
	whole_thoughts = []
	record = []
	pattern = r'[1-5]'
	for response, image_path in zip(image_responses, images_path):
		try:
			score_text = response.split('Score')[1]
			thought = response.split('**Reasoning**:')[-1].strip().lstrip('\n').split('\n\n')[0].replace('\n', ' ')
			score = re.findall(pattern, score_text)[0]
			record.append({'Response': response, 'Score': int(score)})
		except Exception as e:
			logger.error(f'Error processing response: {type(e).__name__}: {e}')
			score = 0
			record.append({'Response': response, 'Score': 0})

		if int(score) >= score_threshold:
			jpg_base64_str = encode_image(Image.open(image_path))
			whole_content_img.append(
				{'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{jpg_base64_str}', 'detail': 'high'}}
			)
			if thought != '':
				whole_thoughts.append(thought)

	whole_content_img = whole_content_img[:MAX_IMAGE]
	whole_thoughts = whole_thoughts[:MAX_IMAGE]
	if len(whole_content_img) == 0:
		prompt = """User Task: {task}

Key Points: {key_points}

Action History:
{last_actions}"""
	text = prompt.format(
		task=task,
		last_actions='\n'.join(f'{i + 1}. {action}' for i, action in enumerate(last_actions)),
		key_points=key_points,
		thoughts='\n'.join(f'{i + 1}. {thought}' for i, thought in enumerate(whole_thoughts)),
	)

	messages = [
		{'role': 'system', 'content': system_msg},
		{'role': 'user', 'content': [{'type': 'text', 'text': text}] + whole_content_img},
	]
	return messages, text, system_msg, record, key_points


async def Online_Mind2Web_eval_with_retry(task, last_actions, images_path, model, score_threshold, max_retries=3):
	"""
	Wrapper for Online_Mind2Web_eval with retry logic.

	Args:
	    task: The task description
	    last_actions: list of actions taken
	    images_path: list of image paths
	    model: The model to use for evaluation
	    score_threshold: Score threshold for image filtering
	    max_retries: Maximum number of retry attempts

	Returns:
	    Tuple of (messages, text, system_msg, record, key_points) or None if all retries fail
	"""
	for attempt in range(max_retries):
		try:
			return await Online_Mind2Web_eval(task, last_actions, images_path, model, score_threshold)
		except Exception as e:
			if attempt == max_retries - 1:  # Last attempt
				logger.error(f'Failed to evaluate after {max_retries} attempts. Error: {type(e).__name__}: {str(e)}')
				raise
			logger.warning(f'Attempt {attempt + 1} failed. Retrying... Error: {type(e).__name__}: {str(e)}')
			await asyncio.sleep(2**attempt)  # Exponential backoff


# ==============================================================================================================


# ==============================================================================================================
# A service for evaluating the performance of the agent
# ==============================================================================================================
import argparse
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import requests
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic.types import SecretStr

from browser_use import Agent, Browser, BrowserConfig

SUPPORTED_MODELS = {
	# Anthropic
	'claude-3.5-sonnet': {
		'provider': 'anthropic',
		'model_name': 'claude-3-5-sonnet-20240620',
		'api_key_env': 'ANTHROPIC_API_KEY',
	},
	'claude-3.5-sonnet-exp': {
		'provider': 'anthropic',
		'model_name': 'claude-3-5-sonnet-20241022',
		'api_key_env': 'ANTHROPIC_API_KEY',
	},
	'claude-3.7-sonnet-exp': {
		'provider': 'anthropic',
		'model_name': 'claude-3-7-sonnet-20250219',
		'api_key_env': 'ANTHROPIC_API_KEY',
	},
	# Deepseek (via OpenAI Compatible API)
	'deepseek-reasoner': {
		'provider': 'openai_compatible',
		'model_name': 'deepseek-reasoner',
		'base_url': 'https://api.deepseek.com/v1',
		'api_key_env': 'DEEPSEEK_API_KEY',
	},
	'deepseek-chat': {
		'provider': 'openai_compatible',
		'model_name': 'deepseek-chat',
		'base_url': 'https://api.deepseek.com/v1',
		'api_key_env': 'DEEPSEEK_API_KEY',
	},
	# Google
	'gemini-1.5-flash': {'provider': 'google', 'model_name': 'gemini-1.5-flash-latest', 'api_key_env': 'GEMINI_API_KEY'},
	'gemini-2.0-flash-exp': {'provider': 'google', 'model_name': 'gemini-2.0-flash-exp', 'api_key_env': 'GEMINI_API_KEY'},
	'gemini-2.5-pro': {'provider': 'google', 'model_name': 'gemini-2.5-pro-preview-03-25', 'api_key_env': 'GEMINI_API_KEY'},
	# OpenAI
	'gpt-4.1': {'provider': 'openai', 'model_name': 'gpt-4.1-2025-04-14', 'api_key_env': 'OPENAI_API_KEY'},
	'gpt-4o': {'provider': 'openai', 'model_name': 'gpt-4o', 'api_key_env': 'OPENAI_API_KEY'},
	'gpt-4o-mini': {'provider': 'openai', 'model_name': 'gpt-4o-mini', 'api_key_env': 'OPENAI_API_KEY'},
	# X.ai (via OpenAI Compatible API)
	'grok-2': {
		'provider': 'openai_compatible',
		'model_name': 'grok-2-1212',
		'base_url': 'https://api.x.ai/v1',
		'api_key_env': 'XAI_API_KEY',
	},
	'grok-3': {
		'provider': 'openai_compatible',
		'model_name': 'grok-3-beta',
		'base_url': 'https://api.x.ai/v1',
		'api_key_env': 'XAI_API_KEY',
	},
}


def get_llm(model_name: str):
	"""Instantiates the correct LangChain ChatModel based on the model name."""
	if model_name not in SUPPORTED_MODELS:
		raise ValueError(f'Unsupported model: {model_name}. Supported models are: {list(SUPPORTED_MODELS.keys())}')

	config = SUPPORTED_MODELS[model_name]
	provider = config['provider']
	api_key_env = config.get('api_key_env')
	api_key = os.getenv(api_key_env) if api_key_env else None

	if not api_key and api_key_env:
		logger.warning(
			f'API key environment variable {api_key_env} not found or empty for model {model_name}. Trying without API key if possible.'
		)
		api_key = None

	api_key_secret = SecretStr(api_key) if api_key else None

	if provider == 'openai':
		kwargs = {
			'model': config['model_name'],
			'temperature': 0.0,
		}
		if api_key_secret:
			kwargs['api_key'] = api_key_secret
		return ChatOpenAI(**kwargs)
	elif provider == 'anthropic':
		# Note: Anthropic client often uses env var ANTHROPIC_API_KEY directly if api_key=None
		kwargs = {
			'model_name': config['model_name'],
			'temperature': 0.0,
			'timeout': 100,
			'stop': None,
		}
		if api_key_secret:
			kwargs['api_key'] = api_key_secret
		return ChatAnthropic(**kwargs)
	elif provider == 'google':
		# Note: Google client often uses env var GOOGLE_API_KEY directly if api_key=None
		kwargs = {
			'model': config['model_name'],
			'temperature': 0.0,
		}
		if api_key_secret:
			kwargs['api_key'] = api_key_secret
		return ChatGoogleGenerativeAI(**kwargs)
	elif provider == 'openai_compatible':
		# Note: OpenAI client often uses env var OPENAI_API_KEY directly if api_key=None and no base_url specified
		# Providing base_url requires explicitly passing the key for that endpoint.
		kwargs = {
			'model': config['model_name'],
			'base_url': config['base_url'],
			'temperature': 0.0,
		}
		if api_key_secret:
			kwargs['api_key'] = api_key_secret
		# Ensure api_key is provided if base_url is set and key exists
		elif config.get('base_url'):
			# If base_url is present but key is missing, we might still error depending on the endpoint's auth requirements.
			# Log a warning here, the constructor will likely raise an error if the key is truly required.
			logger.warning(
				f'API key for {model_name} at {config["base_url"]} is missing, but base_url is specified. Authentication may fail.'
			)
		return ChatOpenAI(**kwargs)
	else:
		raise ValueError(f'Unknown provider: {provider}')


class Task:
	def __init__(self, task_id, confirmed_task, website, reference_length, level):
		self.task_id = task_id
		self.confirmed_task = confirmed_task
		self.website = website
		self.reference_length = reference_length
		self.level = level

	def __str__(self):
		return f'Task(task_id={self.task_id}, confirmed_task={self.confirmed_task}, website={self.website}, reference_length={self.reference_length}, level={self.level})'

	def __repr__(self):
		return self.__str__()


class TaskTracker:
	def __init__(self, task_id: str, task_text: str, run_id: str):
		self.task_id = task_id
		self.task_text = task_text
		self.run_id = run_id
		self.result_folder = Path(f'saved_trajectories/{task_id}')
		self.trajectory_folder = self.result_folder / 'trajectory'
		self.step_results = []
		self.step_counter = 0
		self.screenshots = []
		self.setup_folders()

	def setup_folders(self):
		"""Create the necessary folder structure"""
		self.result_folder.mkdir(parents=True, exist_ok=True)
		self.trajectory_folder.mkdir(parents=True, exist_ok=True)

	async def on_step_start(self, agent):
		"""Record information at the start of a step"""
		self.current_step = {'step_number': self.step_counter, 'start_time': datetime.now().isoformat(), 'actions': []}

	async def on_step_end(self, agent):
		"""Record information at the end of a step"""
		# Take screenshot
		browser_context = agent.browser_context
		screenshot_b64 = await browser_context.take_screenshot()
		screenshot_path = self.trajectory_folder / f'step_{self.step_counter}.png'

		# Save screenshot to file
		async with await anyio.open_file(screenshot_path, 'wb') as f:
			await f.write(base64.b64decode(screenshot_b64))

		# Save screenshot path
		self.screenshots.append(str(screenshot_path))

		# Record action and result
		if agent.state.last_result:
			for result in agent.state.last_result:
				self.current_step['actions'].append(
					{
						'content': result.extracted_content,
						'error': result.error,
						'is_done': result.is_done,
						'success': result.success,
					}
				)

		# Record end time
		self.current_step['end_time'] = datetime.now().isoformat()
		self.current_step['screenshot_path'] = str(screenshot_path)

		# Add to step results
		self.step_results.append(self.current_step)
		self.step_counter += 1

		# Save intermediate results
		self.save_results()  # Save progress after each step

	def save_results(self):
		"""Save the consolidated results"""
		# Create the final result object

		# Ensure action history contains only strings, replacing None with "None"
		action_history = []
		for step in self.step_results:
			if step['actions']:
				content = step['actions'][-1]['content']
				action_history.append(content if content is not None else 'None')
			else:
				action_history.append('None')  # Handle steps with no actions

		formatted_result = {
			'task_id': self.task_id,
			'run_id': self.run_id,
			'task': self.task_text,
			'steps': self.step_results,
			'action_history': action_history,  # Use the cleaned list
			'screenshot_paths': self.screenshots,
			'final_result_response': (
				last_action['content'] if (last_action := self.step_results[-1]['actions'][-1])['is_done'] else None
			),
			'self_report_completed': self.step_results[-1]['actions'][-1]['is_done']
			if self.step_results and self.step_results[-1]['actions']
			else False,
			'self_report_success': self.step_results[-1]['actions'][-1]['success']
			if self.step_results and self.step_results[-1]['actions']
			else None,
		}

		# Save to file
		with open(self.result_folder / 'result.json', 'w') as f:
			json.dump(formatted_result, f, indent=2)

		return formatted_result


async def run_agent_with_tracing(
	task: Task, llm: BaseChatModel, run_id: str, browser: Browser | None = None, max_steps: int = 25, use_vision: bool = True
):
	try:
		# Create task tracker
		tracker = TaskTracker(task.task_id, task.confirmed_task, run_id)

		browser = browser or Browser()

		agent = Agent(
			task=task.confirmed_task,
			llm=llm,
			browser=browser,
			use_vision=use_vision,
			source='eval_platform',  # Override source detection
		)

		# Pass our hook functions
		result = await agent.run(max_steps=max_steps, on_step_start=tracker.on_step_start, on_step_end=tracker.on_step_end)

		# Save final results
		final_results = tracker.save_results()

		return result
	finally:
		# Ensure proper cleanup
		await asyncio.sleep(0.1)  # Give a moment for any pending tasks to complete
		if not browser:
			await agent.close()  # This will close the browser if we created it


async def judge_task_result(model, task_folder: Path, score_threshold: float = 3) -> Dict:
	"""
	Judge a single task result based on the success value of the final action.

	Args:
	    task_folder: Path to the task result folder

	Returns:
	    Dictionary containing judgment results
	"""
	result_file = task_folder / 'result.json'
	if not result_file.exists():
		return {'task_id': task_folder.name, 'judgement': None, 'success': False, 'error': 'No result.json found', 'score': 0.0}

	try:
		async with await anyio.open_file(result_file) as f:
			result = json.loads(await f.read())

		# If a Online_Mind2Web_evaluation is already saved, we can skip the eval
		if result.get('Online_Mind2Web_evaluation'):
			return result.get('Online_Mind2Web_evaluation')

		# Get the screenshot paths, task description, and action history
		screenshot_paths = result.get('screenshot_paths', [])
		task_description = result.get('task')
		action_history = result.get('action_history', [])

		# Use the retry wrapper for evaluation
		try:
			# Await the async function directly instead of using asyncio.run()
			eval_result = await Online_Mind2Web_eval_with_retry(
				task_description, action_history, screenshot_paths, model, score_threshold
			)

			if eval_result is None:
				raise Exception('Evaluation failed after all retries')

			messages, text, system_msg, record, key_points = eval_result

			# Final steps to get judgement - run invoke in a thread
			judgement_msg = await asyncio.to_thread(model.invoke, messages)
			judgement = judgement_msg.content

			if 'success' in judgement.lower().split('status:')[1]:  # This is the official criteria for success
				evaluation = {'task_id': task_folder.name, 'judgement': judgement, 'success': True, 'error': None, 'score': 1.0}
			else:  # This is the official criteria for failure
				evaluation = {'task_id': task_folder.name, 'judgement': judgement, 'success': False, 'error': None, 'score': 0.0}

			# Save the Online_Mind2Web_evaluation into the result.json file
			result['Online_Mind2Web_evaluation'] = evaluation
			with anyio.open_file(result_file, 'w') as f:
				await f.write(json.dumps(result, indent=2))

			return evaluation

		except Exception as err:
			return {
				'task_id': task_folder.name,
				'judgement': None,
				'success': False,
				'error': f'{type(err).__name__}: {err}',
				'score': 0.0,
			}

	except Exception as err:
		return {
			'task_id': task_folder.name,
			'judgement': None,
			'success': False,
			'error': f'{type(err).__name__}: {err}',
			'score': 0.0,
		}


def calculate_local_summary(results_dir: Optional[str] = None) -> Dict:
	"""
	Calculates a summary of task results by reading the saved result.json files.
	Does not make any network requests.

	Args:
		results_dir: Directory where task results are stored (default: 'saved_trajectories')

	Returns:
		Dictionary containing total_tasks, successful_tasks, success_rate, and average_score
	"""
	if results_dir is None:
		results_dir = 'saved_trajectories'

	path = Path(results_dir)
	if not path.is_dir():
		logger.warning(f'Results directory {results_dir} does not exist')
		return {
			'timestamp': datetime.now().isoformat(),
			'total_tasks': 0,
			'successful_tasks': 0,
			'failed_tasks': 0,
			'success_rate': 0,
			'average_score': 0,
		}

	# Collect all task folders
	task_folders = [f for f in path.iterdir() if f.is_dir()]
	total_tasks = len(task_folders)
	successful_tasks = 0
	total_score = 0.0
	results_with_score = 0

	for folder in task_folders:
		result_file = folder / 'result.json'
		if result_file.exists():
			try:
				with open(result_file) as f:
					result_data = json.load(f)

				# Look for evaluation data
				evaluation = result_data.get('Online_Mind2Web_evaluation', {})
				if evaluation:
					if evaluation.get('success', False):
						successful_tasks += 1

					score = evaluation.get('score', 0.0)
					if score > 0:
						total_score += score
						results_with_score += 1
			except Exception as e:
				logger.error(f'Error reading result file {result_file}: {type(e).__name__}: {e}')

	# Calculate statistics
	failed_tasks = total_tasks - successful_tasks
	success_rate = successful_tasks / total_tasks if total_tasks > 0 else 0
	average_score = total_score / results_with_score if results_with_score > 0 else 0

	return {
		'timestamp': datetime.now().isoformat(),
		'total_tasks': total_tasks,
		'successful_tasks': successful_tasks,
		'failed_tasks': failed_tasks,
		'success_rate': success_rate,
		'average_score': average_score,
	}


async def run_task_with_semaphore(
	task: Task,
	run_id: str,
	convex_url: str,
	secret_key: str,
	eval_model: BaseChatModel,
	llm: BaseChatModel,
	max_steps_per_task: int,
	headless: bool,
	use_vision: bool,
	semaphore_runs: asyncio.Semaphore,  # Pass semaphore as argument
) -> dict:
	"""Run a single task with semaphore, sequential execution, and robust error handling"""
	# Acquire semaphore before starting any task-specific logic
	async with semaphore_runs:
		# --- Initialize State & Payload ---
		task_folder = Path(f'saved_trajectories/{task.task_id}')
		result_file = task_folder / 'result.json'

		# Flags to track progress and errors
		execution_needed = True
		execution_succeeded = False
		evaluation_needed = True
		evaluation_succeeded = True  # Default to True, set to False if eval is needed but fails
		local_processing_error = None

		# Initialize the payload with basic info and default failure/unevaluated states
		server_payload = {
			'runId': run_id,
			'taskId': task.task_id,
			'task': task.confirmed_task,
			'actionHistory': [],
			'finalResultResponse': 'None',  # Default if execution doesn't happen or fails early
			'selfReportCompleted': False,
			'selfReportSuccess': None,
			'onlineMind2WebEvaluationJudgement': 'Not Attempted',
			'onlineMind2WebEvaluationError': None,
			'onlineMind2WebEvaluationSuccess': False,
			'onlineMind2WebEvaluationScore': 0.0,
		}

		# Initialize the return value for local processing status
		local_task_status = {'task_id': task.task_id, 'success': False, 'error': None}

		# --- Main Sequential Logic with Error Handling ---
		try:
			# 1. Check for Existing Result
			if result_file.exists():
				logger.info(f'Task {task.task_id}: Found existing result file.')
				try:
					with anyio.open_file(result_file) as f:
						existing_result = json.loads(await f.read())

					# Populate payload from existing file
					server_payload['actionHistory'] = existing_result.get('action_history', [])
					server_payload['finalResultResponse'] = existing_result.get('final_result_response', 'None')
					server_payload['selfReportCompleted'] = existing_result.get('self_report_completed', False)
					server_payload['selfReportSuccess'] = existing_result.get('self_report_success', None)

					# Check if evaluation data is also present
					if existing_eval := existing_result.get('Online_Mind2Web_evaluation'):
						logger.info(f'Task {task.task_id}: Found existing evaluation data.')
						# Ensure judgement is stored as string "None" if it was null/None in cache
						cached_judgement = existing_eval.get('judgement')
						server_payload['onlineMind2WebEvaluationJudgement'] = (
							cached_judgement if cached_judgement is not None else 'None'
						)
						server_payload['onlineMind2WebEvaluationError'] = existing_eval.get('error')
						server_payload['onlineMind2WebEvaluationSuccess'] = existing_eval.get('success', False)
						server_payload['onlineMind2WebEvaluationScore'] = existing_eval.get('score', 0.0)
						evaluation_needed = False  # Don't re-evaluate if already present
						evaluation_succeeded = True  # Assume cached evaluation was successful
					else:
						# Evaluation not found, needs to run
						evaluation_needed = True
						evaluation_succeeded = False  # Mark as needing evaluation initially

					execution_needed = False  # Don't execute if result exists
					execution_succeeded = True  # Mark as "success" in terms of having data
					logger.info(f'Task {task.task_id}: Successfully loaded existing result. Skipping execution.')

				except Exception as e:
					logger.warning(
						f'Task {task.task_id}: Error reading existing result file {result_file}: {type(e).__name__}: {str(e)}. Proceeding with execution.'
					)
					# Keep execution_needed = True, payload defaults remain
					execution_needed = True
					execution_succeeded = False
					evaluation_needed = True  # Might need eval after execution
					evaluation_succeeded = False  # Reset eval status

			# 2. Execute Task (if needed)
			if execution_needed:
				logger.info(f'Task {task.task_id}: Starting execution.')
				browser = None  # Ensure browser is defined for finally block
				try:
					browserConfig = BrowserConfig(headless=headless)
					browser = Browser(config=browserConfig)
					# Pass the llm to run_agent_with_tracing
					result = await run_agent_with_tracing(
						task=task,
						llm=llm,
						browser=browser,
						max_steps=max_steps_per_task,
						use_vision=use_vision,
						run_id=run_id,  # run_agent_with_tracing handles saving result.json
					)
					logger.info(f'Task {task.task_id}: Execution completed.')
					execution_succeeded = True
					evaluation_needed = True  # Need to evaluate the new result
					evaluation_succeeded = False  # Reset eval status

					# Load the result file that should have just been created
					if result_file.exists():
						async with await anyio.open_file(result_file) as f:
							run_result_data = json.loads(await f.read())
						server_payload['actionHistory'] = run_result_data.get('action_history', [])
						server_payload['finalResultResponse'] = run_result_data.get('final_result_response', 'None')
						server_payload['selfReportCompleted'] = run_result_data.get('self_report_completed', False)
						server_payload['selfReportSuccess'] = run_result_data.get('self_report_success', None)
					else:
						# This is unexpected if run_agent_with_tracing succeeded
						logger.error(
							f'Task {task.task_id}: Result file {result_file} missing after presumed successful execution.'
						)
						raise FileNotFoundError(f'Result file not found after execution for task {task.task_id}')

				except Exception as e:
					logger.error(
						f'Task {task.task_id}: Error during execution with Type: {type(e).__name__} and Message: {str(e)}',
						exc_info=True,
					)  # Add stack trace
					execution_succeeded = False
					evaluation_needed = False  # Cannot evaluate if execution failed
					evaluation_succeeded = False  # Evaluation definitely didn't succeed
					# Update payload to reflect execution failure
					server_payload['finalResultResponse'] = f'Execution Error: {type(e).__name__}: {str(e)}'
					server_payload['onlineMind2WebEvaluationJudgement'] = 'Execution Failed'
					server_payload['onlineMind2WebEvaluationError'] = f'Execution Error: {type(e).__name__}'
				finally:
					if browser:
						try:
							await browser.close()
						except Exception as browser_close_e:
							logger.warning(
								f'Task {task.task_id}: Error closing browser: {type(browser_close_e).__name__}: {browser_close_e}'
							)

			# 3. Evaluate Task (if needed and possible)
			if evaluation_needed and execution_succeeded:
				logger.info(f'Task {task.task_id}: Starting evaluation.')
				try:
					# judge_task_result will attempt evaluation and save it back into result.json if successful
					evaluation = await judge_task_result(eval_model, task_folder, score_threshold=3)

					# Update payload directly from the evaluation function's return value
					if evaluation:
						# Ensure judgement is stored as string "None" if the evaluation returned None
						judgement_value = evaluation.get('judgement')
						server_payload['onlineMind2WebEvaluationJudgement'] = (
							judgement_value if judgement_value is not None else 'None'
						)
						server_payload['onlineMind2WebEvaluationError'] = evaluation.get('error')
						server_payload['onlineMind2WebEvaluationSuccess'] = evaluation.get('success', False)
						server_payload['onlineMind2WebEvaluationScore'] = evaluation.get('score', 0.0)
						# Mark evaluation as succeeded only if the evaluation itself didn't report an error
						if evaluation.get('error'):
							logger.warning(
								f'Task {task.task_id}: Evaluation completed but reported an error: {evaluation.get("error")}'
							)
							evaluation_succeeded = False
						else:
							evaluation_succeeded = True  # Mark evaluation as successfully completed
							logger.info(f'Task {task.task_id}: Evaluation successfully completed.')

					else:
						# Should not happen based on judge_task_result structure, but handle defensively
						logger.error(f'Task {task.task_id}: Evaluation function returned None.')
						evaluation_succeeded = False  # Mark as failed if None returned
						server_payload['onlineMind2WebEvaluationJudgement'] = 'Evaluation Returned None'
						server_payload['onlineMind2WebEvaluationError'] = 'Evaluation function returned None'

				except Exception as e:
					logger.error(
						f'Task {task.task_id}: Error during evaluation process: {type(e).__name__}: {str(e)}', exc_info=True
					)  # Add stack trace
					evaluation_succeeded = False
					# Update payload to reflect evaluation failure
					server_payload['onlineMind2WebEvaluationJudgement'] = 'Evaluation Process Error'
					server_payload['onlineMind2WebEvaluationError'] = f'Evaluation Error: {type(e).__name__}: {str(e)}'
					# Keep Success/Score as False/0.0 from defaults

		except Exception as outer_e:
			# Catch any unexpected errors in the flow above (e.g., reading existing file, setup issues)
			logger.critical(f'Task {task.task_id}: CRITICAL UNHANDLED ERROR during processing: {str(outer_e)}', exc_info=True)
			local_processing_error = f'Critical flow error: {str(outer_e)}'
			# Ensure payload reflects a critical failure state
			server_payload['finalResultResponse'] = f'Critical Error: {str(outer_e)}'
			server_payload['onlineMind2WebEvaluationJudgement'] = 'Critical System Error'
			server_payload['onlineMind2WebEvaluationError'] = local_processing_error
			server_payload['onlineMind2WebEvaluationSuccess'] = False
			server_payload['onlineMind2WebEvaluationScore'] = 0.0
			execution_succeeded = False  # Mark stages as failed due to outer error
			evaluation_succeeded = False

		# --- Final Step: Save to Server (Always Attempt) ---
		logger.info(f'Task {task.task_id}: Attempting to save final result to server...')
		try:
			save_success = save_task_result_to_server(convex_url, secret_key, server_payload)
			if save_success:
				logger.info(f'Task {task.task_id}: Successfully saved result to server.')
			else:
				logger.warning(f'Task {task.task_id}: Failed to save result to server (API issue or invalid payload).')
				# Optionally accumulate this failure into local_processing_error
				if local_processing_error:
					local_processing_error += '; Server save failed'
				else:
					local_processing_error = 'Server save failed'

		except Exception as e:
			logger.error(f'Task {task.task_id}: Exception during attempt to save result to server: {type(e).__name__}: {str(e)}')
			# Optionally accumulate this failure
			if local_processing_error:
				local_processing_error += f'; Server save exception: {str(e)}'
			else:
				local_processing_error = f'Server save exception: {str(e)}'

		# --- Return Local Processing Status ---
		# Overall success requires successful execution (or loading existing) AND successful evaluation (if needed).
		local_task_status['success'] = execution_succeeded and evaluation_succeeded
		local_task_status['error'] = local_processing_error  # Report any accumulated local errors

		return local_task_status


async def run_multiple_tasks(
	tasks: list[Task],
	llm: BaseChatModel,
	run_id: str,
	convex_url: str,
	secret_key: str,
	eval_model: BaseChatModel,
	max_parallel_runs: int = 3,
	max_parallel_evaluations: int = 5,
	max_steps_per_task: int = 25,
	start_index: int = 0,
	end_index: Optional[int] = None,
	headless: bool = False,
	use_vision: bool = True,
	fresh_start: bool = True,
) -> Dict:
	"""
	Run multiple tasks in parallel and evaluate results.
	"""
	semaphore_runs = asyncio.Semaphore(max_parallel_runs)
	tasks_to_run = tasks[start_index:end_index] if end_index else tasks[start_index:]

	# Run all tasks in parallel with additional parameters
	task_results = await asyncio.gather(
		*(
			run_task_with_semaphore(
				task=task,
				run_id=run_id,
				convex_url=convex_url,
				secret_key=secret_key,
				eval_model=eval_model,
				llm=llm,  # Pass the agent LLM
				max_steps_per_task=max_steps_per_task,
				headless=headless,
				use_vision=use_vision,
				semaphore_runs=semaphore_runs,  # Pass the semaphore
			)
			for task in tasks_to_run
		)
	)

	# After all tasks are complete, calculate a local summary
	logger.info('All tasks completed. Calculating result summary...')
	summary = calculate_local_summary()

	# Log the summary statistics
	logger.info(f'Completed {summary["total_tasks"]} tasks')
	logger.info(f'Success rate: {summary["success_rate"]:.2%}')
	logger.info(f'Average score: {summary["average_score"]:.2f}')

	return {'task_results': task_results, 'summary': summary}


# Helper function to fetch tasks from the server
def fetch_tasks_from_server(convex_url: str, secret_key: str, test_case_name: str):
	"""Fetches the specified test case file from the Convex HTTP endpoint."""

	if not convex_url:
		logger.error('Error: EVALUATION_TOOL_URL environment variable not set.')
		return None

	if not secret_key:
		logger.error('Error: EVALUATION_TOOL_SECRET_KEY environment variable not set.')
		return None

	endpoint_url = f'{convex_url}/api/getTestCase'
	headers = {
		'Authorization': f'Bearer {secret_key}',
		'Content-Type': 'application/json',
	}
	payload = {'name': test_case_name}

	logger.info(f"Fetching test case '{test_case_name}' from {endpoint_url}...")

	try:
		response = requests.post(endpoint_url, headers=headers, json=payload)

		logger.info(f'Fetch Status Code: {response.status_code}')

		if response.status_code == 200:
			try:
				data = response.json()
				logger.info(f"Successfully fetched test case data for '{test_case_name}'.")
				# Assuming the data is the list of tasks
				if isinstance(data, list):
					return data
				else:
					logger.error(f'Error: Fetched data is not a list. Type: {type(data)}')
					logger.error(f'Raw response: {response.text}')
					return None

			except json.JSONDecodeError:
				logger.error('Error: Failed to decode JSON response.')
				logger.error(f'Raw response text: {response.text}')
				return None
		else:
			logger.error(f"Error: Failed to fetch test case '{test_case_name}'. Status: {response.status_code}")
			logger.error(f'Response: {response.text}')
			return None

	except requests.exceptions.RequestException as e:
		logger.error(f'Error during request to fetch test case: {type(e).__name__}: {e}')
		return None


# Helper function to get git information
def get_git_info():
	"""Retrieves git branch, commit hash, and commit timestamp using subprocess."""
	try:
		branch = subprocess.run(
			['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True, check=True
		).stdout.strip()
		commit_hash = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
		# Get commit timestamp as Unix epoch integer
		commit_timestamp_str = subprocess.run(
			['git', 'log', '-1', '--format=%ct'], capture_output=True, text=True, check=True
		).stdout.strip()
		commit_timestamp = int(commit_timestamp_str)
		return {'branch': branch, 'hash': commit_hash, 'timestamp': commit_timestamp}
	except (subprocess.CalledProcessError, FileNotFoundError, ValueError) as e:
		logger.warning(f'Could not retrieve git info: {type(e).__name__}: {e}. Using defaults.')
		return {
			'branch': 'unknown',
			'hash': 'unknown',
			'timestamp': int(time.time()),  # Fallback to current time
		}


# Helper function to start a new run on the server
def start_new_run(convex_url: str, secret_key: str, run_details: dict):
	"""Sends a request to start a new evaluation run and returns the run ID."""
	if not convex_url or not secret_key:
		logger.error('Error: Convex URL or Secret Key not provided for starting run.')
		return None

	endpoint_url = f'{convex_url}/api/startRun'
	headers = {
		'Authorization': f'Bearer {secret_key}',
		'Content-Type': 'application/json',
	}

	logger.info(f'Sending request to start run at {endpoint_url}...')
	# Avoid logging secret key in run_details if it were ever passed
	loggable_details = {k: v for k, v in run_details.items() if k != 'secret_key'}
	logger.info(f'Run details: {json.dumps(loggable_details, indent=2)}')

	try:
		response = requests.post(endpoint_url, headers=headers, json=run_details)
		logger.info(f'Start Run Status Code: {response.status_code}')

		if response.status_code == 200:
			try:
				data = response.json()
				run_id = data.get('runId')
				if run_id:
					logger.info(f'Successfully started run. Run ID: {run_id}')
					return run_id
				else:
					logger.error("Error: 'runId' not found in successful startRun response.")
					logger.error(f'Raw response: {response.text}')
					return None
			except json.JSONDecodeError:
				logger.error('Error: Failed to decode startRun JSON response.')
				logger.error(f'Raw response text: {response.text}')
				return None
		else:
			logger.error('Error: Failed to start run.')
			logger.error(f'Response: {response.text}')
			return None

	except requests.exceptions.RequestException as e:
		logger.error(f'Error during startRun request: {type(e).__name__}: {e}')
		return None


# Helper function to save a task result to the server
def save_task_result_to_server(convex_url: str, secret_key: str, result_details: dict):
	"""Sends a request to save a single task result to the Convex backend."""

	if not convex_url:
		logger.error('Error: EVALUATION_TOOL_URL environment variable not set for saving task result.')
		return False

	if not secret_key:
		logger.error('Error: EVALUATION_TOOL_SECRET_KEY environment variable not set for saving task result.')
		return False

	# Ensure runId is present in the details being sent
	if 'runId' not in result_details or not result_details['runId']:
		logger.error("Error: 'runId' is missing or empty in result_details for saveTaskResult.")
		return False

	endpoint_url = f'{convex_url}/api/saveTaskResult'
	headers = {
		'Authorization': f'Bearer {secret_key}',
		'Content-Type': 'application/json',
	}

	logger.info(f'Sending request to save task result at {endpoint_url}...')
	logger.debug(f'Result details payload: {json.dumps(result_details, indent=2)}')  # Log details at debug level

	try:
		response = requests.post(endpoint_url, headers=headers, json=result_details)

		logger.info(f'Save Task Result Status Code: {response.status_code}')

		if response.status_code == 200:
			try:
				data = response.json()
				logger.info(f'Successfully saved task result: {data.get("message")}')
				logger.info(f'Result ID: {data.get("resultId")}')
				return True
			except json.JSONDecodeError:
				logger.error('Error: Failed to decode saveTaskResult JSON response.')
				logger.error(f'Raw response text: {response.text}')
				return False
		else:
			logger.error('Error: Failed to save task result.')
			logger.error(f'Response: {response.text}')
			return False

	except requests.exceptions.RequestException as e:
		logger.error(f'Error during saveTaskResult request: {type(e).__name__}: {e}')
		return False


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Run and evaluate browser automation tasks')
	parser.add_argument('--parallel_runs', type=int, default=3, help='Number of parallel tasks to run')
	parser.add_argument('--parallel_evaluations', type=int, default=5, help='Number of parallel evaluations to run')
	parser.add_argument('--max-steps', type=int, default=25, help='Maximum steps per task')
	parser.add_argument('--start', type=int, default=0, help='Start index')
	parser.add_argument('--end', type=int, default=None, help='End index (exclusive)')
	parser.add_argument('--headless', action='store_true', help='Run in headless mode')
	parser.add_argument('--evaluate-only', action='store_true', help='Only evaluate existing results without running new tasks')
	parser.add_argument(
		'--model', type=str, default='gpt-4o', choices=list(SUPPORTED_MODELS.keys()), help='Model to use for the agent'
	)
	parser.add_argument('--no-vision', action='store_true', help='Disable vision capabilities in the agent')
	parser.add_argument(
		'--fresh-start',
		type=lambda x: (str(x).lower() == 'true'),
		default=True,
		help='Clear saved_trajectories before starting. Set to False to keep existing trajectories (default: True)',
	)
	parser.add_argument('--user-message', type=str, default='', help='User message to include in the run')
	args = parser.parse_args()

	# Set up logging - Make sure logger is configured before use in fetch function
	logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
	logger = logging.getLogger(__name__)  # Define logger for the module

	if args.evaluate_only:
		# Just evaluate existing results
		logger.info('Evaluating existing results...')
		summary = calculate_local_summary()

		# Save evaluation results
		timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
		eval_file = f'saved_trajectories/evaluation_summary_{timestamp}.json'
		with open(eval_file, 'w') as f:
			json.dump(summary, f, indent=2)

		logger.info(f'Evaluation complete. Success rate: {summary["success_rate"]:.2%}')
		logger.info(f'Average score: {summary["average_score"]:.2f}')
		logger.info(f'Full results saved to {eval_file}')

	else:
		logger.info('Running tasks...')
		# Run tasks and evaluate
		load_dotenv()

		# --- Clear trajectories if fresh_start is True ---
		results_dir_path = Path('saved_trajectories')
		if args.fresh_start:
			logger.info(f'--fresh-start is True. Clearing {results_dir_path}...')
			if results_dir_path.exists():
				try:
					shutil.rmtree(results_dir_path)
					logger.info(f'Successfully removed {results_dir_path}.')
				except OSError as e:
					logger.error(f'Error removing directory {results_dir_path}: {type(e).__name__}: {e}')
					# Decide if you want to exit or continue
					# exit(1) # Uncomment to exit on error
			else:
				logger.info(f'{results_dir_path} does not exist, no need to clear.')

			# Recreate the directory
			try:
				results_dir_path.mkdir(parents=True, exist_ok=True)
				logger.info(f'Recreated directory {results_dir_path}.')
			except OSError as e:
				logger.error(f'Error creating directory {results_dir_path}: {type(e).__name__}: {e}')
				# exit(1) # Uncomment to exit on error
		else:
			logger.info('--fresh-start is False. Existing trajectories in saved_trajectories will be kept.')
		# -------------------------------------------------

		# --- Fetch Tasks from Server ---
		CONVEX_URL = os.getenv('EVALUATION_TOOL_URL')
		SECRET_KEY = os.getenv('EVALUATION_TOOL_SECRET_KEY')
		TEST_CASE_NAME = 'OnlineMind2Web'  # Name of the test case to fetch

		if not CONVEX_URL or not SECRET_KEY:
			logger.error('Error: EVALUATION_TOOL_URL or EVALUATION_TOOL_SECRET_KEY environment variables not set.')
			exit(1)  # Exit if config is missing

		logger.info(f"Attempting to fetch task list '{TEST_CASE_NAME}' from server...")
		fetched_task_data = fetch_tasks_from_server(CONVEX_URL, SECRET_KEY, TEST_CASE_NAME)

		if fetched_task_data is None:
			logger.error('Failed to fetch tasks from the server. Exiting.')
			exit(1)  # Exit if fetch fails

		try:
			tasks = [Task(**task_data) for task_data in fetched_task_data]
			logger.info(f'Successfully loaded {len(tasks)} tasks from the server.')
		except TypeError as e:
			logger.error(
				f'Error creating Task objects from fetched data. Ensure the data structure matches Task requirements (task_id, confirmed_task, etc.). Error: {type(e).__name__}: {e}'
			)
			logger.error(f'First item in fetched data: {fetched_task_data[0] if fetched_task_data else "None"}')
			exit(1)
		# -----------------------------

		# --- Start Run on Server ---
		logger.info('Attempting to start a new run on the server...')
		git_info = get_git_info()

		# Collect additional data from args to store with the run
		additional_run_data = {
			'max_steps': args.max_steps,
			'parallel_runs': args.parallel_runs,
			'parallel_evaluations': args.parallel_evaluations,
			'start_index': args.start,
			'end_index': args.end,
			'headless': args.headless,
			'use_vision': not args.no_vision,
			'task_source': TEST_CASE_NAME,
		}

		run_data = {
			'model': args.model,
			'gitBranch': git_info['branch'],
			'gitCommitHash': git_info['hash'],
			'gitCommitTimestamp': git_info['timestamp'],
			'userMessage': args.user_message,
			'totalTasks': args.end - args.start,
			'additionalData': additional_run_data,
		}

		run_id = start_new_run(CONVEX_URL, SECRET_KEY, run_data)

		if not run_id:
			logger.error('Failed to start a new run on the server. Exiting.')
			exit(1)

		logger.info(f'Successfully obtained run ID: {run_id}. Proceeding with tasks...')
		# -------------------------

		# Get the selected LLM
		llm = get_llm(args.model)

		results = asyncio.run(
			run_multiple_tasks(
				tasks=tasks,
				llm=llm,  # Pass the instantiated llm
				run_id=run_id,
				convex_url=CONVEX_URL,
				secret_key=SECRET_KEY,
				eval_model=llm,
				max_parallel_runs=args.parallel_runs,
				max_parallel_evaluations=args.parallel_evaluations,
				max_steps_per_task=args.max_steps,
				start_index=args.start,
				end_index=args.end,
				headless=args.headless,
				use_vision=not args.no_vision,
				fresh_start=args.fresh_start,
			)
		)

		logger.info('Task completed. Saving results...')
		# Save results
		timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
		results_file = f'saved_trajectories/eval_results_{timestamp}.json'

		# Convert results to JSON-serializable format
		serializable_results = {'summary': results['summary']}

		with open(results_file, 'w') as f:
			json.dump(serializable_results, f, indent=2)

		# Print summary
		summary = results['summary']
		logger.info(f'Completed {summary["total_tasks"]} tasks.')
		logger.info(f'Success rate: {summary["success_rate"]:.2%}')
		logger.info(f'Average score: {summary["average_score"]:.2f}')
		logger.info(f'Results saved to {results_file}')
````

## File: examples/features/playwright_script_generation.py
````python
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Ensure the project root is in the Python path if running directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from browser_use import Agent, Browser, BrowserConfig

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

# Define the task for the agent
TASK_DESCRIPTION = """
1. Go to amazon.com
2. Search for 'i7 14700k'
4. If there is an 'Add to Cart' button, open the product page and then click add to cart.
5. the open the shopping cart page /cart button/ go to cart button.
6. Scroll down to the bottom of the cart page.
7. Scroll up to the top of the cart page.
8. Finish the task.
"""

# Define the path where the Playwright script will be saved
SCRIPT_DIR = Path('./playwright_scripts')
SCRIPT_PATH = SCRIPT_DIR / 'playwright_amazon_cart_script.py'


# Helper function to stream output from the subprocess
async def stream_output(stream, prefix):
	if stream is None:
		print(f'{prefix}: (No stream available)')
		return
	while True:
		line = await stream.readline()
		if not line:
			break
		print(f'{prefix}: {line.decode().rstrip()}', flush=True)


async def main():
	# Initialize the language model
	llm = ChatOpenAI(model='gpt-4.1', temperature=0.0)

	# Configure the browser
	# Use headless=False if you want to watch the agent visually
	browser_config = BrowserConfig(headless=False)
	browser = Browser(config=browser_config)

	# Configure the agent
	# The 'save_playwright_script_path' argument tells the agent where to save the script
	agent = Agent(
		task=TASK_DESCRIPTION,
		llm=llm,
		browser=browser,
		save_playwright_script_path=str(SCRIPT_PATH),  # Pass the path as a string
	)

	print('Running the agent to generate the Playwright script...')
	history = None  # Initialize history to None
	try:
		history = await agent.run()
		print('Agent finished running.')

		if history and history.is_successful():
			print(f'Agent completed the task successfully. Final result: {history.final_result()}')
		elif history:
			print('Agent finished, but the task might not be fully successful.')
			if history.has_errors():
				print(f'Errors encountered: {history.errors()}')
		else:
			print('Agent run did not return a history object.')

	except Exception as e:
		print(f'An error occurred during the agent run: {e}')
		# Ensure browser is closed even if agent run fails
		if browser:
			await browser.close()
		return  # Exit if agent failed

	# --- Execute the Generated Playwright Script ---
	print(f'\nChecking if Playwright script was generated at: {SCRIPT_PATH}')
	if SCRIPT_PATH.exists():
		print('Playwright script found. Attempting to execute...')
		try:
			# Ensure the script directory exists before running
			SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

			# Execute the generated script using asyncio.create_subprocess_exec
			process = await asyncio.create_subprocess_exec(
				sys.executable,
				str(SCRIPT_PATH),
				stdout=asyncio.subprocess.PIPE,
				stderr=asyncio.subprocess.PIPE,
				cwd=Path.cwd(),  # Run from the current working directory
			)

			print('\n--- Playwright Script Execution ---')
			# Create tasks to stream stdout and stderr concurrently
			stdout_task = asyncio.create_task(stream_output(process.stdout, 'stdout'))
			stderr_task = asyncio.create_task(stream_output(process.stderr, 'stderr'))

			# Wait for both stream tasks and the process to finish
			await asyncio.gather(stdout_task, stderr_task)
			returncode = await process.wait()
			print('-------------------------------------')

			if returncode == 0:
				print('\n✅ Playwright script executed successfully!')
			else:
				print(f'\n⚠️ Playwright script finished with exit code {returncode}.')

		except Exception as e:
			print(f'\n❌ An error occurred while executing the Playwright script: {e}')
	else:
		print(f'\n❌ Playwright script not found at {SCRIPT_PATH}. Generation might have failed.')

	# Close the browser used by the agent (if not already closed by agent.run error handling)
	# Note: The generated script manages its own browser instance.
	if browser:
		await browser.close()
		print("Agent's browser closed.")


if __name__ == '__main__':
	# Ensure the script directory is clean before running (optional)
	if SCRIPT_PATH.exists():
		SCRIPT_PATH.unlink()
		print(f'Removed existing script: {SCRIPT_PATH}')

	# Run the main async function
	asyncio.run(main())
````

## File: examples/models/deepseek.py
````python
import asyncio
import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from pydantic import SecretStr

from browser_use import Agent

# dotenv
load_dotenv()

api_key = os.getenv('DEEPSEEK_API_KEY', '')
if not api_key:
	raise ValueError('DEEPSEEK_API_KEY is not set')


async def run_search():
	agent = Agent(
		task=(
			'1. Go to https://www.reddit.com/r/LocalLLaMA '
			"2. Search for 'browser use' in the search bar"
			'3. Click on first result'
			'4. Return the first comment'
		),
		llm=ChatDeepSeek(
			base_url='https://api.deepseek.com/v1',
			model='deepseek-chat',
			api_key=SecretStr(api_key),
		),
		use_vision=False,
	)

	await agent.run()


if __name__ == '__main__':
	asyncio.run(run_search())
````

## File: examples/use-cases/web_voyager_agent.py
````python
# Goal: A general-purpose web navigation agent for tasks like flight booking and course searching.

import asyncio
import os
import sys

# Adjust Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from pydantic import SecretStr

from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser, BrowserConfig, BrowserContextConfig
from browser_use.browser.context import BrowserContextWindowSize

# Load environment variables
load_dotenv()

# Set LLM based on defined environment variables
if os.getenv('OPENAI_API_KEY'):
	llm = ChatOpenAI(
		model='gpt-4o',
	)
elif os.getenv('AZURE_OPENAI_KEY') and os.getenv('AZURE_OPENAI_ENDPOINT'):
	llm = AzureChatOpenAI(
		model='gpt-4o',
		api_version='2024-10-21',
		azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
		api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', '')),
	)
else:
	raise ValueError('No LLM found. Please set OPENAI_API_KEY or AZURE_OPENAI_KEY and AZURE_OPENAI_ENDPOINT.')


browser = Browser(
	config=BrowserConfig(
		headless=False,  # This is True in production
		disable_security=True,
		new_context_config=BrowserContextConfig(
			disable_security=True,
			minimum_wait_page_load_time=1,  # 3 on prod
			maximum_wait_page_load_time=10,  # 20 on prod
			# no_viewport=True,
			browser_window_size=BrowserContextWindowSize(width=1280, height=1100),
			# trace_path='./tmp/web_voyager_agent',
		),
	)
)

# TASK = """
# Find the lowest-priced one-way flight from Cairo to Montreal on February 21, 2025, including the total travel time and number of stops. on https://www.google.com/travel/flights/
# """
# TASK = """
# Browse Coursera, which universities offer Master of Advanced Study in Engineering degrees? Tell me what is the latest application deadline for this degree? on https://www.coursera.org/"""
TASK = """
Find and book a hotel in Paris with suitable accommodations for a family of four (two adults and two children) offering free cancellation for the dates of February 14-21, 2025. on https://www.booking.com/
"""


async def main():
	agent = Agent(
		task=TASK,
		llm=llm,
		browser=browser,
		validate_output=True,
		enable_memory=False,
	)
	history = await agent.run(max_steps=50)
	history.save_to_file('./tmp/history.json')


if __name__ == '__main__':
	asyncio.run(main())
````

## File: README.md
````markdown
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
````

## File: tests/test_browser_window_size_height_no_viewport.py
````python
import asyncio

from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig, BrowserContextWindowSize


async def test():
	print('Testing browser window sizing with no_viewport=False...')
	browser = Browser(BrowserConfig(headless=False))
	context_config = BrowserContextConfig(browser_window_size=BrowserContextWindowSize(width=1440, height=900), no_viewport=False)
	browser_context = await browser.new_context(config=context_config)
	page = await browser_context.get_current_page()
	await page.goto('https://example.com')
	await asyncio.sleep(2)
	viewport = await page.evaluate('() => ({width: window.innerWidth, height: window.innerHeight})')
	print('Configured size: width=1440, height=900')
	print(f'Actual viewport size: {viewport}')

	# Get the actual window size
	window_size = await page.evaluate("""
        () => ({
            width: window.outerWidth,
            height: window.outerHeight
        })
    """)
	print(f'Actual window size: {window_size}')

	await browser_context.close()
	await browser.close()


if __name__ == '__main__':
	asyncio.run(test())
````

## File: tests/test_browser_window_size_height.py
````python
"""
Example script demonstrating the browser_window_size feature.
This script shows how to set a custom window size for the browser.
"""

import asyncio
import sys
from typing import Any, Dict

from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig, BrowserContextWindowSize


async def main():
	"""Demonstrate setting a custom browser window size"""
	# Create a browser with a specific window size
	window_size = BrowserContextWindowSize(width=800, height=400)  # Small size to clearly demonstrate the fix
	config = BrowserContextConfig(browser_window_size=window_size)

	browser = None
	browser_context = None

	try:
		# Initialize the browser with error handling
		try:
			browser = Browser(
				config=BrowserConfig(
					headless=False,  # Use non-headless mode to see the window
				)
			)
		except Exception as e:
			print(f'Failed to initialize browser: {e}')
			return 1

		# Create a browser context
		try:
			browser_context = await browser.new_context(config=config)
		except Exception as e:
			print(f'Failed to create browser context: {e}')
			return 1

		# Get the current page
		page = await browser_context.get_current_page()

		# Navigate to a test page with error handling
		try:
			await page.goto('https://example.com')
			await page.wait_for_load_state('domcontentloaded')
		except Exception as e:
			print(f'Failed to navigate to example.com: {e}')
			print('Continuing with test anyway...')

		# Wait a bit to see the window
		await asyncio.sleep(2)

		# Get the actual viewport size using JavaScript
		viewport_size = await page.evaluate("""
			() => {
				return {
					width: window.innerWidth,
					height: window.innerHeight
				}
			}
		""")

		print(f'Configured window size: {window_size.model_dump()}')
		print(f'Actual viewport size: {viewport_size}')

		# Validate the window size
		validate_window_size(window_size.model_dump(), viewport_size)

		# Wait a bit more to see the window
		await asyncio.sleep(3)

		return 0

	except Exception as e:
		print(f'Unexpected error: {e}')
		return 1

	finally:
		# Close resources
		if browser_context:
			await browser_context.close()
		if browser:
			await browser.close()


def validate_window_size(configured: Dict[str, Any], actual: Dict[str, Any]) -> None:
	"""Compare configured window size with actual size and report differences"""
	# Allow for small differences due to browser chrome, scrollbars, etc.
	width_diff = abs(configured['width'] - actual['width'])
	height_diff = abs(configured['height'] - actual['height'])

	# Tolerance of 5% or 20px, whichever is greater
	width_tolerance = max(configured['width'] * 0.05, 20)
	height_tolerance = max(configured['height'] * 0.05, 20)

	if width_diff > width_tolerance or height_diff > height_tolerance:
		print('WARNING: Significant difference between configured and actual window size!')
		print(f'Width difference: {width_diff}px, Height difference: {height_diff}px')
	else:
		print('Window size validation passed: actual size matches configured size within tolerance')


if __name__ == '__main__':
	result = asyncio.run(main())
	sys.exit(result)
````

## File: tests/test_browser.py
````python
import asyncio
import subprocess

import psutil
import pytest
import requests

from browser_use.browser.browser import Browser, BrowserConfig, ProxySettings
from browser_use.browser.context import BrowserContext, BrowserContextConfig


@pytest.mark.asyncio
async def test_builtin_browser_launch(monkeypatch):
	"""
	Test that the standard browser is launched correctly:
	When no remote (cdp or wss) or chrome instance is provided, the Browser class uses _setup_builtin_browser.
	This test monkeypatches async_playwright to return dummy objects, and asserts that get_playwright_browser returns the expected DummyBrowser.
	"""

	class DummyBrowser:
		pass

	class DummyChromium:
		async def launch(self, headless, args, proxy=None, handle_sigterm=False, handle_sigint=False):
			return DummyBrowser()

	class DummyPlaywright:
		def __init__(self):
			self.chromium = DummyChromium()

		async def stop(self):
			pass

	class DummyAsyncPlaywrightContext:
		async def start(self):
			return DummyPlaywright()

	monkeypatch.setattr('browser_use.browser.browser.async_playwright', lambda: DummyAsyncPlaywrightContext())
	config = BrowserConfig(headless=True, disable_security=False, extra_browser_args=['--test'])
	browser_obj = Browser(config=config)
	result_browser = await browser_obj.get_playwright_browser()
	assert isinstance(result_browser, DummyBrowser), 'Expected DummyBrowser from _setup_builtin_browser'
	await browser_obj.close()


@pytest.mark.asyncio
async def test_cdp_browser_launch(monkeypatch):
	"""
	Test that when a CDP URL is provided in the configuration, the Browser uses _setup_cdp
	and returns the expected DummyBrowser.
	"""

	class DummyBrowser:
		pass

	class DummyChromium:
		async def connect_over_cdp(self, endpoint_url, timeout=20000):
			assert endpoint_url == 'ws://dummy-cdp-url', 'The endpoint URL should match the configuration.'
			return DummyBrowser()

	class DummyPlaywright:
		def __init__(self):
			self.chromium = DummyChromium()

		async def stop(self):
			pass

	class DummyAsyncPlaywrightContext:
		async def start(self):
			return DummyPlaywright()

	monkeypatch.setattr('browser_use.browser.browser.async_playwright', lambda: DummyAsyncPlaywrightContext())
	config = BrowserConfig(cdp_url='ws://dummy-cdp-url')
	browser_obj = Browser(config=config)
	result_browser = await browser_obj.get_playwright_browser()
	assert isinstance(result_browser, DummyBrowser), 'Expected DummyBrowser from _setup_cdp'
	await browser_obj.close()


@pytest.mark.asyncio
async def test_wss_browser_launch(monkeypatch):
	"""
	Test that when a WSS URL is provided in the configuration,
	the Browser uses setup_wss and returns the expected DummyBrowser.
	"""

	class DummyBrowser:
		pass

	class DummyChromium:
		async def connect(self, wss_url):
			assert wss_url == 'ws://dummy-wss-url', 'WSS URL should match the configuration.'
			return DummyBrowser()

	class DummyPlaywright:
		def __init__(self):
			self.chromium = DummyChromium()

		async def stop(self):
			pass

	class DummyAsyncPlaywrightContext:
		async def start(self):
			return DummyPlaywright()

	monkeypatch.setattr('browser_use.browser.browser.async_playwright', lambda: DummyAsyncPlaywrightContext())
	config = BrowserConfig(wss_url='ws://dummy-wss-url')
	browser_obj = Browser(config=config)
	result_browser = await browser_obj.get_playwright_browser()
	assert isinstance(result_browser, DummyBrowser), 'Expected DummyBrowser from _setup_wss'
	await browser_obj.close()


@pytest.mark.asyncio
async def test_user_provided_browser_launch(monkeypatch):
	"""
	Test that when a browser_binary_path is provided the Browser class uses
	_setup_user_provided_browser branch and returns the expected DummyBrowser object
	by reusing an existing Chrome instance.
	"""

	# Dummy response for requests.get when checking chrome debugging endpoint.
	class DummyResponse:
		status_code = 200

	def dummy_get(url, timeout):
		if url == 'http://localhost:9222/json/version':
			return DummyResponse()
		raise requests.ConnectionError('Connection failed')

	monkeypatch.setattr(requests, 'get', dummy_get)

	class DummyBrowser:
		pass

	class DummyChromium:
		async def connect_over_cdp(self, endpoint_url, timeout=20000):
			assert endpoint_url == 'http://localhost:9222', "Endpoint URL must be 'http://localhost:9222'"
			return DummyBrowser()

	class DummyPlaywright:
		def __init__(self):
			self.chromium = DummyChromium()

		async def stop(self):
			pass

	class DummyAsyncPlaywrightContext:
		async def start(self):
			return DummyPlaywright()

	monkeypatch.setattr('browser_use.browser.browser.async_playwright', lambda: DummyAsyncPlaywrightContext())
	config = BrowserConfig(browser_binary_path='dummy/chrome', extra_browser_args=['--dummy-arg'])
	browser_obj = Browser(config=config)
	result_browser = await browser_obj.get_playwright_browser()
	assert isinstance(result_browser, DummyBrowser), 'Expected DummyBrowser from _setup_user_provided_browser'
	await browser_obj.close()


@pytest.mark.asyncio
async def test_user_provided_browser_launch_on_custom_chrome_remote_debugging_port(monkeypatch):
	"""
	Test that when a browser_binary_path and chrome_remote_debugging_port are provided, the Browser class uses
	_setup_user_provided_browser branch and returns the expected DummyBrowser object
	by launching a new Chrome instance with --remote-debugging-port=chrome_remote_debugging_port argument.
	"""

	# Custom remote debugging port
	custom_chrome_remote_debugging_port = 9223

	# Dummy response for requests.get when checking chrome debugging endpoint.
	class DummyResponse:
		status_code = 200

	def dummy_get(url, timeout):
		if url == f'http://localhost:{custom_chrome_remote_debugging_port}/json/version':
			return DummyResponse()
		raise requests.ConnectionError('Connection failed')

	monkeypatch.setattr(requests, 'get', dummy_get)

	class DummyProcess:
		def __init__(self, *args, **kwargs):
			pass

	class DummySubProcess:
		pid = 1234

	async def dummy_create_subprocess_exec(browser_binary_path, *args, **kwargs):
		assert f'--remote-debugging-port={custom_chrome_remote_debugging_port}' in args, (
			f'Chrome must be started with with --remote-debugging-port={custom_chrome_remote_debugging_port} argument'
		)

		return DummySubProcess()

	monkeypatch.setattr(asyncio, 'create_subprocess_exec', dummy_create_subprocess_exec)
	monkeypatch.setattr(psutil, 'Process', DummyProcess)

	class DummyBrowser:
		pass

	class DummyChromium:
		async def connect_over_cdp(self, endpoint_url, timeout=20000):
			assert endpoint_url == f'http://localhost:{custom_chrome_remote_debugging_port}', (
				f"Endpoint URL must be 'http://localhost:{custom_chrome_remote_debugging_port}'"
			)
			return DummyBrowser()

	class DummyPlaywright:
		def __init__(self):
			self.chromium = DummyChromium()

		async def stop(self):
			pass

	class DummyAsyncPlaywrightContext:
		async def start(self):
			return DummyPlaywright()

	monkeypatch.setattr('browser_use.browser.browser.async_playwright', lambda: DummyAsyncPlaywrightContext())

	config = BrowserConfig(
		browser_binary_path='dummy/chrome',
		chrome_remote_debugging_port=custom_chrome_remote_debugging_port,
		extra_browser_args=['--dummy-arg'],
	)

	browser_obj = Browser(config=config)
	result_browser = await browser_obj.get_playwright_browser()
	assert isinstance(result_browser, DummyBrowser), (
		f'Expected DummyBrowser with remote debugging port {custom_chrome_remote_debugging_port} from _setup_user_provided_browser'
	)
	await browser_obj.close()


@pytest.mark.asyncio
async def test_builtin_browser_disable_security_args(monkeypatch):
	"""
	Test that the standard browser launch includes disable-security arguments when disable_security is True.
	This verifies that _setup_builtin_browser correctly appends the security disabling arguments along with
	the base arguments and any extra arguments provided.
	"""
	# These are the base arguments defined in _setup_builtin_browser.
	base_args = [
		'--no-sandbox',
		'--disable-blink-features=AutomationControlled',
		'--disable-infobars',
		'--disable-background-timer-throttling',
		'--disable-popup-blocking',
		'--disable-backgrounding-occluded-windows',
		'--disable-renderer-backgrounding',
		'--disable-window-activation',
		'--disable-focus-on-load',
		'--no-first-run',
		'--no-default-browser-check',
		'--no-startup-window',
		'--window-position=0,0',
	]
	# When disable_security is True, these arguments should be added.
	disable_security_args = [
		'--disable-web-security',
		'--disable-site-isolation-trials',
		'--disable-features=IsolateOrigins,site-per-process',
	]
	# Additional arbitrary argument for testing extra args
	extra_args = ['--dummy-extra']

	class DummyBrowser:
		pass

	class DummyChromium:
		async def launch(self, headless, args, proxy=None, handle_sigterm=False, handle_sigint=False):
			# Expected args is the base args plus disable security args and the extra args.
			expected_args = base_args + disable_security_args + extra_args
			assert headless is True, 'Expected headless to be True'
			assert args == expected_args, f'Expected args {expected_args}, but got {args}'
			assert proxy is None, 'Expected proxy to be None'
			return DummyBrowser()

	class DummyPlaywright:
		def __init__(self):
			self.chromium = DummyChromium()

		async def stop(self):
			pass

	class DummyAsyncPlaywrightContext:
		async def start(self):
			return DummyPlaywright()

	monkeypatch.setattr('browser_use.browser.browser.async_playwright', lambda: DummyAsyncPlaywrightContext())
	config = BrowserConfig(headless=True, disable_security=True, extra_browser_args=extra_args)
	browser_obj = Browser(config=config)
	result_browser = await browser_obj.get_playwright_browser()
	assert isinstance(result_browser, DummyBrowser), (
		'Expected DummyBrowser from _setup_builtin_browser with disable_security active'
	)
	await browser_obj.close()


@pytest.mark.asyncio
async def test_new_context_creation():
	"""
	Test that the new_context method returns a BrowserContext with the correct attributes.
	This verifies that the BrowserContext is initialized with the provided Browser instance and configuration.
	"""
	config = BrowserConfig()
	browser_obj = Browser(config=config)
	custom_context_config = BrowserContextConfig()
	context = await browser_obj.new_context(custom_context_config)
	assert isinstance(context, BrowserContext), 'Expected new_context to return an instance of BrowserContext'
	assert context.browser is browser_obj, "Expected the context's browser attribute to be the Browser instance"
	assert context.config == custom_context_config, "Expected the context's config attribute to be the provided config"
	await browser_obj.close()


@pytest.mark.asyncio
async def test_user_provided_browser_launch_failure(monkeypatch):
	"""
	Test that when a Chrome instance cannot be started or connected to,
	the Browser._setup_user_provided_browser branch eventually raises a RuntimeError.
	We simulate failure by:
	  - Forcing requests.get to always raise a ConnectionError (so no existing instance is found).
	  - Monkeypatching subprocess.Popen to do nothing.
	  - Replacing asyncio.sleep to avoid delays.
	  - Having the dummy playwright's connect_over_cdp method always raise an Exception.
	"""

	def dummy_get(url, timeout):
		raise requests.ConnectionError('Simulated connection failure')

	monkeypatch.setattr(requests, 'get', dummy_get)
	monkeypatch.setattr(subprocess, 'Popen', lambda args, stdout, stderr: None)

	async def fake_sleep(seconds):
		return

	monkeypatch.setattr(asyncio, 'sleep', fake_sleep)

	class DummyChromium:
		async def connect_over_cdp(self, endpoint_url, timeout=20000):
			raise Exception('Connection failed simulation')

	class DummyPlaywright:
		def __init__(self):
			self.chromium = DummyChromium()

		async def stop(self):
			pass

	class DummyAsyncPlaywrightContext:
		async def start(self):
			return DummyPlaywright()

	monkeypatch.setattr('browser_use.browser.browser.async_playwright', lambda: DummyAsyncPlaywrightContext())
	config = BrowserConfig(browser_binary_path='dummy/chrome', extra_browser_args=['--dummy-arg'])
	browser_obj = Browser(config=config)
	with pytest.raises(RuntimeError, match='To start chrome in Debug mode'):
		await browser_obj.get_playwright_browser()
	await browser_obj.close()


@pytest.mark.asyncio
async def test_get_playwright_browser_caching(monkeypatch):
	"""
	Test that get_playwright_browser returns a cached browser instance.
	On the first call, the browser is initialized; on subsequent calls,
	the same instance is returned.
	"""

	class DummyBrowser:
		pass

	class DummyChromium:
		async def launch(self, headless, args, proxy=None, handle_sigterm=False, handle_sigint=False):
			return DummyBrowser()

	class DummyPlaywright:
		def __init__(self):
			self.chromium = DummyChromium()

		async def stop(self):
			pass

	class DummyAsyncPlaywrightContext:
		async def start(self):
			return DummyPlaywright()

	monkeypatch.setattr('browser_use.browser.browser.async_playwright', lambda: DummyAsyncPlaywrightContext())
	config = BrowserConfig(headless=True, disable_security=False, extra_browser_args=['--test'])
	browser_obj = Browser(config=config)
	first_browser = await browser_obj.get_playwright_browser()
	second_browser = await browser_obj.get_playwright_browser()
	assert first_browser is second_browser, 'Expected the browser to be cached and reused across calls.'
	await browser_obj.close()


@pytest.mark.asyncio
async def test_close_error_handling(monkeypatch):
	"""
	Test that the close method properly handles exceptions thrown by
	playwright_browser.close() and playwright.stop(), ensuring that the
	browser's attributes are set to None even if errors occur.
	"""

	class DummyBrowserWithError:
		async def close(self):
			raise Exception('Close error simulation')

	class DummyPlaywrightWithError:
		async def stop(self):
			raise Exception('Stop error simulation')

	config = BrowserConfig()
	browser_obj = Browser(config=config)
	browser_obj.playwright_browser = DummyBrowserWithError()
	browser_obj.playwright = DummyPlaywrightWithError()
	await browser_obj.close()
	assert browser_obj.playwright_browser is None, 'Expected playwright_browser to be None after close'
	assert browser_obj.playwright is None, 'Expected playwright to be None after close'


@pytest.mark.asyncio
async def test_standard_browser_launch_with_proxy(monkeypatch):
	"""
	Test that when a proxy is provided in the BrowserConfig, the _setup_builtin_browser method
	correctly passes the proxy parameter to the playwright.chromium.launch method.
	This test sets up a dummy async_playwright context and verifies that the dummy proxy is received.
	"""

	class DummyBrowser:
		pass

	# Create a dummy proxy settings instance.
	dummy_proxy = ProxySettings(server='http://dummy.proxy')

	class DummyChromium:
		async def launch(self, headless, args, proxy=None, handle_sigterm=False, handle_sigint=False):
			# Assert that the proxy passed equals the dummy proxy provided in the configuration.
			assert isinstance(proxy, dict) and proxy['server'] == 'http://dummy.proxy', (
				f'Expected proxy {dummy_proxy} but got {proxy}'
			)
			# We can also verify some base parameters if needed (headless, args) but our focus is proxy.
			return DummyBrowser()

	class DummyPlaywright:
		def __init__(self):
			self.chromium = DummyChromium()

		async def stop(self):
			pass

	class DummyAsyncPlaywrightContext:
		async def start(self):
			return DummyPlaywright()

	# Monkeypatch async_playwright to return our dummy async playwright context.
	monkeypatch.setattr('browser_use.browser.browser.async_playwright', lambda: DummyAsyncPlaywrightContext())
	# Create a BrowserConfig with the dummy proxy.
	config = BrowserConfig(headless=False, disable_security=False, proxy=dummy_proxy)
	browser_obj = Browser(config=config)
	# Call get_playwright_browser and verify that the returned browser is as expected.
	result_browser = await browser_obj.get_playwright_browser()
	assert isinstance(result_browser, DummyBrowser), 'Expected DummyBrowser from _setup_builtin_browser with proxy provided'
	await browser_obj.close()


@pytest.mark.asyncio
async def test_browser_window_size(monkeypatch):
	"""
	Test that when a browser_window_size is provided in BrowserContextConfig,
	it's properly converted to a dictionary when passed to Playwright.
	"""

	class DummyPage:
		def __init__(self):
			self.url = 'about:blank'

		async def goto(self, url):
			pass

		async def wait_for_load_state(self, state):
			pass

		async def title(self):
			return 'Test Page'

		async def bring_to_front(self):
			pass

		async def evaluate(self, script):
			return True

		def is_closed(self):
			return False

	class DummyContext:
		def __init__(self):
			self.pages = [DummyPage()]
			self.tracing = self

		async def new_page(self):
			return DummyPage()

		async def add_init_script(self, script):
			pass

		async def start(self):
			pass

		async def stop(self, path=None):
			pass

		def on(self, event, handler):
			pass

		async def close(self):
			pass

	class DummyBrowser:
		def __init__(self):
			self.contexts = []

		async def new_context(self, **kwargs):
			# Assert that record_video_size is a dictionary with expected values
			assert isinstance(kwargs['record_video_size'], dict), (
				f'Expected record_video_size to be a dictionary, got {type(kwargs["record_video_size"])}'
			)
			assert kwargs['record_video_size']['width'] == 1280, (
				f'Expected width to be 1280, got {kwargs["record_video_size"].get("width")}'
			)
			assert kwargs['record_video_size']['height'] == 1100, (
				f'Expected height to be 1100, got {kwargs["record_video_size"].get("height")}'
			)

			context = DummyContext()
			self.contexts.append(context)
			return context

		async def close(self):
			pass

	class DummyPlaywright:
		def __init__(self):
			self.chromium = self

		async def launch(self, **kwargs):
			return DummyBrowser()

		async def stop(self):
			pass

	class DummyAsyncPlaywrightContext:
		async def start(self):
			return DummyPlaywright()

	# Monkeypatch async_playwright to return our dummy async playwright context
	monkeypatch.setattr('browser_use.browser.browser.async_playwright', lambda: DummyAsyncPlaywrightContext())

	# Create browser with default config
	browser_obj = Browser()

	# Get browser instance
	playwright_browser = await browser_obj.get_playwright_browser()

	# Create context config with specific window size
	context_config = BrowserContextConfig(browser_window_size={'width': 1280, 'height': 1100})

	# Create browser context - this will test if browser_window_size is properly converted
	browser_context = BrowserContext(browser=browser_obj, config=context_config)
	await browser_context._initialize_session()

	# Clean up
	await browser_context.close()
	await browser_obj.close()
````

## File: tests/test_vision.py
````python
"""
Simple try of the agent.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import os
import sys
from pprint import pprint

import pytest

from browser_use.browser.browser import Browser, BrowserConfig

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from langchain_openai import ChatOpenAI

from browser_use import Agent, AgentHistoryList, Controller

llm = ChatOpenAI(model='gpt-4o')
controller = Controller()

# use this test to ask the model questions about the page like
# which color do you see for bbox labels, list all with their label
# what's the smallest bboxes with labels and


@controller.registry.action(description='explain what you see on the screen and ask user for input')
async def explain_screen(text: str) -> str:
	pprint(text)
	answer = input('\nuser input next question: \n')
	return answer


@controller.registry.action(description='done')
async def done(text: str) -> str:
	# pprint(text)
	return 'call explain_screen'


@pytest.fixture(scope='function')
def event_loop():
	"""Create an instance of the default event loop for each test case."""
	loop = asyncio.get_event_loop_policy().new_event_loop()
	yield loop
	loop.close()


@pytest.mark.skip(reason='this is for local testing only')
async def test_vision():
	agent = Agent(
		task='call explain_screen all the time the user asks you questions e.g. about the page like bbox which you see are labels  - your task is to explain it and get the next question',
		llm=llm,
		controller=controller,
		browser=Browser(config=BrowserConfig(disable_security=True, headless=False)),
	)
	try:
		history: AgentHistoryList = await agent.run(20)
	finally:
		# Make sure to close the browser
		await agent.browser.close()
````

## File: .github/workflows/cloud_evals.yml
````yaml
name: cloud_evals

on:
  push:
    branches:
      - main
      - 'releases/*'
  workflow_dispatch:
    inputs:
      commit_hash:
        description: Commit hash of the library to build the Cloud eval image for
        required: false

jobs:
  trigger_cloud_eval_image_build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.TRIGGER_CLOUD_BUILD_GH_KEY }}
          script: |
            const result = await github.rest.repos.createDispatchEvent({
              owner: 'browser-use',
              repo: 'cloud',
              event_type: 'trigger-workflow',
              client_payload: {"commit_hash": "${{ github.event.inputs.commit_hash || github.sha }}"}
            })
            console.log(result)
````

## File: browser_use/agent/message_manager/utils.py
````python
from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Optional, Type

from langchain_core.messages import (
	AIMessage,
	BaseMessage,
	HumanMessage,
	SystemMessage,
	ToolMessage,
)

logger = logging.getLogger(__name__)

MODELS_WITHOUT_TOOL_SUPPORT_PATTERNS = [
	'deepseek-reasoner',
	'deepseek-r1',
	'.*gemma.*-it',
]


def is_model_without_tool_support(model_name: str) -> bool:
	return any(re.match(pattern, model_name) for pattern in MODELS_WITHOUT_TOOL_SUPPORT_PATTERNS)


def extract_json_from_model_output(content: str) -> dict:
	"""Extract JSON from model output, handling both plain JSON and code-block-wrapped JSON."""
	try:
		# If content is wrapped in code blocks, extract just the JSON part
		if '```' in content:
			# Find the JSON content between code blocks
			content = content.split('```')[1]
			# Remove language identifier if present (e.g., 'json\n')
			if '\n' in content:
				content = content.split('\n', 1)[1]
		# Parse the cleaned content
		return json.loads(content)
	except json.JSONDecodeError as e:
		logger.warning(f'Failed to parse model output: {content} {str(e)}')
		raise ValueError('Could not parse response.')


def convert_input_messages(input_messages: list[BaseMessage], model_name: Optional[str]) -> list[BaseMessage]:
	"""Convert input messages to a format that is compatible with the planner model"""
	if model_name is None:
		return input_messages

	if is_model_without_tool_support(model_name):
		converted_input_messages = _convert_messages_for_non_function_calling_models(input_messages)
		merged_input_messages = _merge_successive_messages(converted_input_messages, HumanMessage)
		merged_input_messages = _merge_successive_messages(merged_input_messages, AIMessage)
		return merged_input_messages
	return input_messages


def _convert_messages_for_non_function_calling_models(input_messages: list[BaseMessage]) -> list[BaseMessage]:
	"""Convert messages for non-function-calling models"""
	output_messages = []
	for message in input_messages:
		if isinstance(message, HumanMessage):
			output_messages.append(message)
		elif isinstance(message, SystemMessage):
			output_messages.append(message)
		elif isinstance(message, ToolMessage):
			output_messages.append(HumanMessage(content=message.content))
		elif isinstance(message, AIMessage):
			# check if tool_calls is a valid JSON object
			if message.tool_calls:
				tool_calls = json.dumps(message.tool_calls)
				output_messages.append(AIMessage(content=tool_calls))
			else:
				output_messages.append(message)
		else:
			raise ValueError(f'Unknown message type: {type(message)}')
	return output_messages


def _merge_successive_messages(messages: list[BaseMessage], class_to_merge: Type[BaseMessage]) -> list[BaseMessage]:
	"""Some models like deepseek-reasoner dont allow multiple human messages in a row. This function merges them into one."""
	merged_messages = []
	streak = 0
	for message in messages:
		if isinstance(message, class_to_merge):
			streak += 1
			if streak > 1:
				if isinstance(message.content, list):
					merged_messages[-1].content += message.content[0]['text']  # type:ignore
				else:
					merged_messages[-1].content += message.content
			else:
				merged_messages.append(message)
		else:
			merged_messages.append(message)
			streak = 0
	return merged_messages


def save_conversation(input_messages: list[BaseMessage], response: Any, target: str, encoding: Optional[str] = None) -> None:
	"""Save conversation history to file."""

	# create folders if not exists
	if dirname := os.path.dirname(target):
		os.makedirs(dirname, exist_ok=True)

	with open(
		target,
		'w',
		encoding=encoding,
	) as f:
		_write_messages_to_file(f, input_messages)
		_write_response_to_file(f, response)


def _write_messages_to_file(f: Any, messages: list[BaseMessage]) -> None:
	"""Write messages to conversation file"""
	for message in messages:
		f.write(f' {message.__class__.__name__} \n')

		if isinstance(message.content, list):
			for item in message.content:
				if isinstance(item, dict) and item.get('type') == 'text':
					f.write(item['text'].strip() + '\n')
		elif isinstance(message.content, str):
			try:
				content = json.loads(message.content)
				f.write(json.dumps(content, indent=2) + '\n')
			except json.JSONDecodeError:
				f.write(message.content.strip() + '\n')

		f.write('\n')


def _write_response_to_file(f: Any, response: Any) -> None:
	"""Write model response to conversation file"""
	f.write(' RESPONSE\n')
	f.write(json.dumps(json.loads(response.model_dump_json(exclude_unset=True)), indent=2))
````

## File: browser_use/agent/views.py
````python
from __future__ import annotations

import json
import traceback
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Type

from langchain_core.language_models.chat_models import BaseChatModel
from openai import RateLimitError
from pydantic import BaseModel, ConfigDict, Field, ValidationError, create_model

from browser_use.agent.message_manager.views import MessageManagerState
from browser_use.agent.playwright_script_generator import PlaywrightScriptGenerator
from browser_use.browser.browser import BrowserConfig
from browser_use.browser.context import BrowserContextConfig
from browser_use.browser.views import BrowserStateHistory
from browser_use.controller.registry.views import ActionModel
from browser_use.dom.history_tree_processor.service import (
	DOMElementNode,
	DOMHistoryElement,
	HistoryTreeProcessor,
)
from browser_use.dom.views import SelectorMap

ToolCallingMethod = Literal['function_calling', 'json_mode', 'raw', 'auto']
REQUIRED_LLM_API_ENV_VARS = {
	'ChatOpenAI': ['OPENAI_API_KEY'],
	'AzureChatOpenAI': ['AZURE_OPENAI_ENDPOINT', 'AZURE_OPENAI_KEY'],
	'ChatBedrockConverse': ['ANTHROPIC_API_KEY'],
	'ChatAnthropic': ['ANTHROPIC_API_KEY'],
	'ChatGoogleGenerativeAI': ['GEMINI_API_KEY'],
	'ChatDeepSeek': ['DEEPSEEK_API_KEY'],
	'ChatOllama': [],
	'ChatGrok': ['GROK_API_KEY'],
}


class AgentSettings(BaseModel):
	"""Options for the agent"""

	use_vision: bool = True
	use_vision_for_planner: bool = False
	save_conversation_path: Optional[str] = None
	save_conversation_path_encoding: Optional[str] = 'utf-8'
	max_failures: int = 3
	retry_delay: int = 10
	max_input_tokens: int = 128000
	validate_output: bool = False
	message_context: Optional[str] = None
	generate_gif: bool | str = False
	available_file_paths: Optional[list[str]] = None
	override_system_message: Optional[str] = None
	extend_system_message: Optional[str] = None
	include_attributes: list[str] = [
		'title',
		'type',
		'name',
		'role',
		'tabindex',
		'aria-label',
		'placeholder',
		'value',
		'alt',
		'aria-expanded',
	]
	max_actions_per_step: int = 10

	tool_calling_method: Optional[ToolCallingMethod] = 'auto'
	page_extraction_llm: Optional[BaseChatModel] = None
	planner_llm: Optional[BaseChatModel] = None
	planner_interval: int = 1  # Run planner every N steps
	is_planner_reasoning: bool = False  # type: ignore
	extend_planner_system_message: Optional[str] = None

	# Playwright script generation setting
	save_playwright_script_path: Optional[str] = None  # Path to save the generated Playwright script


class AgentState(BaseModel):
	"""Holds all state information for an Agent"""

	agent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
	n_steps: int = 1
	consecutive_failures: int = 0
	last_result: Optional[List['ActionResult']] = None
	history: AgentHistoryList = Field(default_factory=lambda: AgentHistoryList(history=[]))
	last_plan: Optional[str] = None
	paused: bool = False
	stopped: bool = False

	message_manager_state: MessageManagerState = Field(default_factory=MessageManagerState)

	# class Config:
	# 	arbitrary_types_allowed = True


@dataclass
class AgentStepInfo:
	step_number: int
	max_steps: int

	def is_last_step(self) -> bool:
		"""Check if this is the last step"""
		return self.step_number >= self.max_steps - 1


class ActionResult(BaseModel):
	"""Result of executing an action"""

	is_done: Optional[bool] = False
	success: Optional[bool] = None
	extracted_content: Optional[str] = None
	error: Optional[str] = None
	include_in_memory: bool = False  # whether to include in past messages as context or not


class StepMetadata(BaseModel):
	"""Metadata for a single step including timing and token information"""

	step_start_time: float
	step_end_time: float
	input_tokens: int  # Approximate tokens from message manager for this step
	step_number: int

	@property
	def duration_seconds(self) -> float:
		"""Calculate step duration in seconds"""
		return self.step_end_time - self.step_start_time


class AgentBrain(BaseModel):
	"""Current state of the agent"""

	evaluation_previous_goal: str
	memory: str
	next_goal: str


class AgentOutput(BaseModel):
	"""Output model for agent

	@dev note: this model is extended with custom actions in AgentService. You can also use some fields that are not in this model as provided by the linter, as long as they are registered in the DynamicActions model.
	"""

	model_config = ConfigDict(arbitrary_types_allowed=True)

	current_state: AgentBrain
	action: list[ActionModel] = Field(
		...,
		description='List of actions to execute',
		json_schema_extra={'min_items': 1},  # Ensure at least one action is provided
	)

	@staticmethod
	def type_with_custom_actions(custom_actions: Type[ActionModel]) -> Type['AgentOutput']:
		"""Extend actions with custom actions"""
		model_ = create_model(
			'AgentOutput',
			__base__=AgentOutput,
			action=(
				list[custom_actions],
				Field(..., description='List of actions to execute', json_schema_extra={'min_items': 1}),
			),
			__module__=AgentOutput.__module__,
		)
		model_.__doc__ = 'AgentOutput model with custom actions'
		return model_


class AgentHistory(BaseModel):
	"""History item for agent actions"""

	model_output: AgentOutput | None
	result: list[ActionResult]
	state: BrowserStateHistory
	metadata: Optional[StepMetadata] = None

	model_config = ConfigDict(arbitrary_types_allowed=True, protected_namespaces=())

	@staticmethod
	def get_interacted_element(model_output: AgentOutput, selector_map: SelectorMap) -> list[DOMHistoryElement | None]:
		elements = []
		for action in model_output.action:
			index = action.get_index()
			if index is not None and index in selector_map:
				el: DOMElementNode = selector_map[index]
				elements.append(HistoryTreeProcessor.convert_dom_element_to_history_element(el))
			else:
				elements.append(None)
		return elements

	def model_dump(self, **kwargs) -> Dict[str, Any]:
		"""Custom serialization handling circular references"""

		# Handle action serialization
		model_output_dump = None
		if self.model_output:
			action_dump = [action.model_dump(exclude_none=True) for action in self.model_output.action]
			model_output_dump = {
				'current_state': self.model_output.current_state.model_dump(),
				'action': action_dump,  # This preserves the actual action data
			}

		return {
			'model_output': model_output_dump,
			'result': [r.model_dump(exclude_none=True) for r in self.result],
			'state': self.state.to_dict(),
			'metadata': self.metadata.model_dump() if self.metadata else None,
		}


class AgentHistoryList(BaseModel):
	"""List of agent history items"""

	history: list[AgentHistory]

	def total_duration_seconds(self) -> float:
		"""Get total duration of all steps in seconds"""
		total = 0.0
		for h in self.history:
			if h.metadata:
				total += h.metadata.duration_seconds
		return total

	def total_input_tokens(self) -> int:
		"""
		Get total tokens used across all steps.
		Note: These are from the approximate token counting of the message manager.
		For accurate token counting, use tools like LangChain Smith or OpenAI's token counters.
		"""
		total = 0
		for h in self.history:
			if h.metadata:
				total += h.metadata.input_tokens
		return total

	def input_token_usage(self) -> list[int]:
		"""Get token usage for each step"""
		return [h.metadata.input_tokens for h in self.history if h.metadata]

	def __str__(self) -> str:
		"""Representation of the AgentHistoryList object"""
		return f'AgentHistoryList(all_results={self.action_results()}, all_model_outputs={self.model_actions()})'

	def __repr__(self) -> str:
		"""Representation of the AgentHistoryList object"""
		return self.__str__()

	def save_to_file(self, filepath: str | Path) -> None:
		"""Save history to JSON file with proper serialization"""
		try:
			Path(filepath).parent.mkdir(parents=True, exist_ok=True)
			data = self.model_dump()
			with open(filepath, 'w', encoding='utf-8') as f:
				json.dump(data, f, indent=2)
		except Exception as e:
			raise e

	def save_as_playwright_script(
		self,
		output_path: str | Path,
		sensitive_data_keys: Optional[List[str]] = None,
		browser_config: Optional[BrowserConfig] = None,
		context_config: Optional[BrowserContextConfig] = None,
	) -> None:
		"""
		Generates a Playwright script based on the agent's history and saves it to a file.
		Args:
			output_path: The path where the generated Python script will be saved.
			sensitive_data_keys: A list of keys used as placeholders for sensitive data
								 (e.g., ['username_placeholder', 'password_placeholder']).
								 These will be loaded from environment variables in the
								 generated script.
			browser_config: Configuration of the original Browser instance.
			context_config: Configuration of the original BrowserContext instance.
		"""
		try:
			serialized_history = self.model_dump()['history']
			generator = PlaywrightScriptGenerator(serialized_history, sensitive_data_keys, browser_config, context_config)
			script_content = generator.generate_script_content()
			path_obj = Path(output_path)
			path_obj.parent.mkdir(parents=True, exist_ok=True)
			with open(path_obj, 'w', encoding='utf-8') as f:
				f.write(script_content)
		except Exception as e:
			raise e

	def model_dump(self, **kwargs) -> Dict[str, Any]:
		"""Custom serialization that properly uses AgentHistory's model_dump"""
		return {
			'history': [h.model_dump(**kwargs) for h in self.history],
		}

	@classmethod
	def load_from_file(cls, filepath: str | Path, output_model: Type[AgentOutput]) -> 'AgentHistoryList':
		"""Load history from JSON file"""
		with open(filepath, 'r', encoding='utf-8') as f:
			data = json.load(f)
		# loop through history and validate output_model actions to enrich with custom actions
		for h in data['history']:
			if h['model_output']:
				if isinstance(h['model_output'], dict):
					h['model_output'] = output_model.model_validate(h['model_output'])
				else:
					h['model_output'] = None
			if 'interacted_element' not in h['state']:
				h['state']['interacted_element'] = None
		history = cls.model_validate(data)
		return history

	def last_action(self) -> None | dict:
		"""Last action in history"""
		if self.history and self.history[-1].model_output:
			return self.history[-1].model_output.action[-1].model_dump(exclude_none=True)
		return None

	def errors(self) -> list[str | None]:
		"""Get all errors from history, with None for steps without errors"""
		errors = []
		for h in self.history:
			step_errors = [r.error for r in h.result if r.error]

			# each step can have only one error
			errors.append(step_errors[0] if step_errors else None)
		return errors

	def final_result(self) -> None | str:
		"""Final result from history"""
		if self.history and self.history[-1].result[-1].extracted_content:
			return self.history[-1].result[-1].extracted_content
		return None

	def is_done(self) -> bool:
		"""Check if the agent is done"""
		if self.history and len(self.history[-1].result) > 0:
			last_result = self.history[-1].result[-1]
			return last_result.is_done is True
		return False

	def is_successful(self) -> bool | None:
		"""Check if the agent completed successfully - the agent decides in the last step if it was successful or not. None if not done yet."""
		if self.history and len(self.history[-1].result) > 0:
			last_result = self.history[-1].result[-1]
			if last_result.is_done is True:
				return last_result.success
		return None

	def has_errors(self) -> bool:
		"""Check if the agent has any non-None errors"""
		return any(error is not None for error in self.errors())

	def urls(self) -> list[str | None]:
		"""Get all unique URLs from history"""
		return [h.state.url if h.state.url is not None else None for h in self.history]

	def screenshots(self) -> list[str | None]:
		"""Get all screenshots from history"""
		return [h.state.screenshot if h.state.screenshot is not None else None for h in self.history]

	def action_names(self) -> list[str]:
		"""Get all action names from history"""
		action_names = []
		for action in self.model_actions():
			actions = list(action.keys())
			if actions:
				action_names.append(actions[0])
		return action_names

	def model_thoughts(self) -> list[AgentBrain]:
		"""Get all thoughts from history"""
		return [h.model_output.current_state for h in self.history if h.model_output]

	def model_outputs(self) -> list[AgentOutput]:
		"""Get all model outputs from history"""
		return [h.model_output for h in self.history if h.model_output]

	# get all actions with params
	def model_actions(self) -> list[dict]:
		"""Get all actions from history"""
		outputs = []

		for h in self.history:
			if h.model_output:
				for action, interacted_element in zip(h.model_output.action, h.state.interacted_element):
					output = action.model_dump(exclude_none=True)
					output['interacted_element'] = interacted_element
					outputs.append(output)
		return outputs

	def action_results(self) -> list[ActionResult]:
		"""Get all results from history"""
		results = []
		for h in self.history:
			results.extend([r for r in h.result if r])
		return results

	def extracted_content(self) -> list[str]:
		"""Get all extracted content from history"""
		content = []
		for h in self.history:
			content.extend([r.extracted_content for r in h.result if r.extracted_content])
		return content

	def model_actions_filtered(self, include: list[str] | None = None) -> list[dict]:
		"""Get all model actions from history as JSON"""
		if include is None:
			include = []
		outputs = self.model_actions()
		result = []
		for o in outputs:
			for i in include:
				if i == list(o.keys())[0]:
					result.append(o)
		return result

	def number_of_steps(self) -> int:
		"""Get the number of steps in the history"""
		return len(self.history)


class AgentError:
	"""Container for agent error handling"""

	VALIDATION_ERROR = 'Invalid model output format. Please follow the correct schema.'
	RATE_LIMIT_ERROR = 'Rate limit reached. Waiting before retry.'
	NO_VALID_ACTION = 'No valid action found'

	@staticmethod
	def format_error(error: Exception, include_trace: bool = False) -> str:
		"""Format error message based on error type and optionally include trace"""
		message = ''
		if isinstance(error, ValidationError):
			return f'{AgentError.VALIDATION_ERROR}\nDetails: {str(error)}'
		if isinstance(error, RateLimitError):
			return AgentError.RATE_LIMIT_ERROR
		if include_trace:
			return f'{str(error)}\nStacktrace:\n{traceback.format_exc()}'
		return f'{str(error)}'
````

## File: browser_use/browser/chrome.py
````python
CHROME_DEFAULT_USER_AGENT = (
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
)
CHROME_EXTENSIONS = {}  # coming in a separate PR
CHROME_EXTENSIONS_PATH = 'chrome_extensions'
CHROME_PROFILE_PATH = 'chrome_profile'
CHROME_PROFILE_USER = 'Default'
CHROME_DEBUG_PORT = 9222
CHROME_DISABLED_COMPONENTS = [
	'Translate',
	'AcceptCHFrame',
	'OptimizationHints',
	'ProcessPerSiteUpToMainFrameThreshold',
	'InterestFeedContentSuggestions',
	'CalculateNativeWinOcclusion',
	'BackForwardCache',
	'HeavyAdPrivacyMitigations',
	'LazyFrameLoading',
	'ImprovedCookieControls',
	'PrivacySandboxSettings4',
	'AutofillServerCommunication',
	'CertificateTransparencyComponentUpdater',
	'DestroyProfileOnBrowserClose',
	'CrashReporting',
	'OverscrollHistoryNavigation',
	'InfiniteSessionRestore',
	#'LockProfileCookieDatabase',  # disabling allows multiple chrome instances to concurrently modify profile, but might make chrome much slower https://github.com/yt-dlp/yt-dlp/issues/7271  https://issues.chromium.org/issues/40901624
]  # it's always best to give each chrome instance its own exclusive copy of the user profile


CHROME_HEADLESS_ARGS = [
	'--headless=new',
	'--test-type',
	'--test-type=gpu',  # https://github.com/puppeteer/puppeteer/issues/10516
	# '--enable-automation',                            # <- DONT USE THIS, it makes you easily detectable / blocked by cloudflare
]

CHROME_DOCKER_ARGS = [
	# Docker-specific options
	# https://github.com/GoogleChrome/lighthouse-ci/tree/main/docs/recipes/docker-client#--no-sandbox-issues-explained
	'--no-sandbox',  # rely on docker sandboxing in docker, otherwise we need cap_add: SYS_ADM to use host sandboxing
	'--disable-gpu-sandbox',
	'--disable-setuid-sandbox',
	'--disable-dev-shm-usage',  # docker 75mb default shm size is not big enough, disabling just uses /tmp instead
	'--no-xshm',
	# dont try to disable (or install) dbus in docker, its not needed, chrome can work without dbus despite the errors
]

CHROME_DISABLE_SECURITY_ARGS = [
	# DANGER: JS isolation security features (to allow easier tampering with pages during automation)
	# chrome://net-internals
	'--disable-web-security',  # <- WARNING, breaks some sites that expect/enforce strict CORS headers (try webflow.com)
	'--disable-site-isolation-trials',
	'--disable-features=IsolateOrigins,site-per-process',
	# '--allow-file-access-from-files',                     # <- WARNING, dangerous, allows JS to read filesystem using file:// URLs
	# DANGER: Disable HTTPS verification
	'--allow-running-insecure-content',  # Breaks CORS/CSRF/HSTS etc., useful sometimes but very easy to detect
	'--ignore-certificate-errors',
	'--ignore-ssl-errors',
	'--ignore-certificate-errors-spki-list',
	'--allow-insecure-localhost',
]

# flags to make chrome behave more deterministically across different OS's
CHROME_DETERMINISTIC_RENDERING_ARGS = [
	'--deterministic-mode',
	'--js-flags=--random-seed=1157259159',  # make all JS random numbers deterministic by providing a seed
	'--force-device-scale-factor=1',
	'--hide-scrollbars',  # hide scrollbars because otherwise they show up in screenshots
	# GPU, canvas, text, and pdf rendering config
	# chrome://gpu
	'--enable-webgl',  # enable web-gl graphics support
	'--font-render-hinting=none',  # make rendering more deterministic by ignoring OS font hints, may also need css override, try:    * {text-rendering: geometricprecision !important; -webkit-font-smoothing: antialiased;}
	'--force-color-profile=srgb',  # make rendering more deterministic by using consistent color profile, if browser looks weird, try: generic-rgb
	'--disable-partial-raster',  # make rendering more deterministic (TODO: verify if still needed)
	'--disable-skia-runtime-opts',  # make rendering more deterministic by avoiding Skia hot path runtime optimizations
	'--disable-2d-canvas-clip-aa',  # make rendering more deterministic by disabling antialiasing on 2d canvas clips
	# '--disable-gpu',                                  # falls back to more consistent software renderer across all OS's, especially helps linux text rendering look less weird
	# // '--use-gl=swiftshader',                        <- DO NOT USE, breaks M1 ARM64. it makes rendering more deterministic by using simpler CPU renderer instead of OS GPU renderer  bug: https://groups.google.com/a/chromium.org/g/chromium-dev/c/8eR2GctzGuw
	# // '--disable-software-rasterizer',               <- DO NOT USE, harmless, used in tandem with --disable-gpu
	# // '--run-all-compositor-stages-before-draw',     <- DO NOT USE, makes headful chrome hang on startup (tested v121 Google Chrome.app on macOS)
	# // '--disable-gl-drawing-for-tests',              <- DO NOT USE, disables gl output (makes tests run faster if you dont care about canvas)
	# // '--blink-settings=imagesEnabled=false',        <- DO NOT USE, disables images entirely (only sometimes useful to speed up loading)
	# Process management & performance tuning
	# chrome://process-internals
	'--disable-lazy-loading',  # make rendering more deterministic by loading all content up-front instead of on-focus
	'--disable-renderer-backgrounding',  # dont throttle tab rendering based on focus/visibility
	'--disable-background-networking',  # dont throttle tab networking based on focus/visibility
	'--disable-background-timer-throttling',  # dont throttle tab timers based on focus/visibility
	'--disable-backgrounding-occluded-windows',  # dont throttle tab window based on focus/visibility
	'--disable-ipc-flooding-protection',  # dont throttle ipc traffic or accessing big request/response/buffer/etc. objects will fail
	'--disable-extensions-http-throttling',  # dont throttle http traffic based on runtime heuristics
	'--disable-field-trial-config',  # disable shared field trial state between browser processes
	'--disable-back-forward-cache',  # disable browsing navigation cache
]


CHROME_ARGS = [
	# Profile data dir setup
	# chrome://profile-internals
	# f'--user-data-dir={CHROME_PROFILE_PATH}',     # managed by playwright arg instead
	# f'--profile-directory={CHROME_PROFILE_USER}',
	# '--password-store=basic',  # use mock keychain instead of OS-provided keychain (we manage auth.json instead)
	# '--use-mock-keychain',
	'--disable-cookie-encryption',  # we need to be able to write unencrypted cookies to save/load auth.json
	'--disable-sync',  # don't try to use Google account sync features while automation is active
	# Extensions
	# chrome://inspect/#extensions
	# f'--load-extension={CHROME_EXTENSIONS.map(({unpacked_path}) => unpacked_path).join(',')}',  # not needed when using existing profile that already has extensions installed
	# f'--allowlisted-extension-id={",".join(CHROME_EXTENSIONS.keys())}',
	'--allow-legacy-extension-manifests',
	'--allow-pre-commit-input',  # allow JS mutations before page rendering is complete
	'--disable-blink-features=AutomationControlled',  # hide the signatures that announce browser is being remote-controlled
	# f'--proxy-server=https://43.159.28.126:2334:u7ce652b7568805c4-zone-custom-region-us-session-szGWq3FRU-sessTime-60:u7ce652b7568805c4',      # send all network traffic through a proxy https://2captcha.com/proxy
	# f'--proxy-bypass-list=127.0.0.1',
	# Browser window and viewport setup
	# chrome://version
	# f'--user-agent="{DEFAULT_USER_AGENT}"',
	# f'--window-size={DEFAULT_VIEWPORT.width},{DEFAULT_VIEWPORT.height}',
	# '--window-position=0,0',
	# '--start-maximized',
	'--install-autogenerated-theme=0,0,0',  # black border makes it easier to see which chrome window is browser-use's
	#'--virtual-time-budget=60000',  # fast-forward all animations & timers by 60s, dont use this it's unfortunately buggy and breaks screenshot and PDF capture sometimes
	#'--autoplay-policy=no-user-gesture-required',  # auto-start videos so they trigger network requests + show up in outputs
	#'--disable-gesture-requirement-for-media-playback',
	#'--lang=en-US,en;q=0.9',
	# IO: stdin/stdout, debug port config
	# chrome://inspect
	'--log-level=2',  # 1=DEBUG 2=WARNING 3=ERROR
	'--enable-logging=stderr',
	# '--remote-debugging-address=127.0.0.1',         <- never expose to non-localhost, would allow attacker to drive your browser from any machine
	'--enable-experimental-extension-apis',  # add support for tab groups
	'--disable-focus-on-load',  # prevent browser from hijacking focus
	'--disable-window-activation',
	# '--in-process-gpu',                            <- DONT USE THIS, makes headful startup time ~5-10s slower (tested v121 Google Chrome.app on macOS)
	# '--disable-component-extensions-with-background-pages',  # TODO: check this, disables chrome components that only run in background with no visible UI (could lower startup time)
	# uncomment to disable hardware camera/mic/speaker access + present fake devices to websites
	# (faster to disable, but disabling breaks recording browser audio in puppeteer-stream screenrecordings)
	# '--use-fake-device-for-media-stream',
	# '--use-fake-ui-for-media-stream',
	# '--disable-features=GlobalMediaControls,MediaRouter,DialMediaRouteProvider',
	# Output format options (PDF, screenshot, etc.)
	'--export-tagged-pdf',  # include table on contents and tags in printed PDFs
	'--generate-pdf-document-outline',
	# Suppress first-run features, popups, hints, updates, etc.
	# chrome://system
	'--no-pings',
	'--no-first-run',
	'--no-default-browser-check',
	'--no-startup-window',
	'--disable-default-apps',
	'--ash-no-nudges',
	'--disable-infobars',
	'--disable-search-engine-choice-screen',
	'--disable-session-crashed-bubble',
	'--simulate-outdated-no-au="Tue, 31 Dec 2099 23:59:59 GMT"',  # disable browser self-update while automation is active
	'--hide-crash-restore-bubble',
	'--suppress-message-center-popups',
	'--disable-client-side-phishing-detection',
	'--disable-domain-reliability',
	'--disable-component-update',
	'--disable-datasaver-prompt',
	'--disable-hang-monitor',
	'--disable-session-crashed-bubble',
	'--disable-speech-synthesis-api',
	'--disable-speech-api',
	'--disable-print-preview',
	'--safebrowsing-disable-auto-update',
	'--deny-permission-prompts',
	'--disable-external-intent-requests',
	'--disable-notifications',
	'--disable-desktop-notifications',
	'--noerrdialogs',
	'--disable-popup-blocking',
	'--disable-prompt-on-repost',
	'--silent-debugger-extension-api',
	'--block-new-web-contents',
	'--metrics-recording-only',
	'--disable-breakpad',
	# other feature flags
	# chrome://flags        chrome://components
	f'--disable-features={",".join(CHROME_DISABLED_COMPONENTS)}',
	'--enable-features=NetworkService',
]
````

## File: eval/gpt-o4-mini.py
````python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent, Browser

load_dotenv()


async def run_agent(task: str, browser: Browser | None = None, max_steps: int = 38):
	browser = browser or Browser()
	llm = ChatOpenAI(
		model='o4-mini-2025-04-16',
	)
	agent = Agent(task=task, llm=llm, browser=browser)
	result = await agent.run(max_steps=max_steps)
	return result
````

## File: tests/test_service.py
````python
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from browser_use.agent.service import Agent
from browser_use.agent.views import ActionResult
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContext
from browser_use.browser.views import BrowserState
from browser_use.controller.registry.service import Registry
from browser_use.controller.registry.views import ActionModel
from browser_use.controller.service import Controller

# run with python -m pytest tests/test_service.py


# run test with:
# python -m pytest tests/test_service.py
class TestAgent:
	@pytest.fixture
	def mock_controller(self):
		controller = Mock(spec=Controller)
		registry = Mock(spec=Registry)
		registry.registry = MagicMock()
		registry.registry.actions = {'test_action': MagicMock(param_model=MagicMock())}  # type: ignore
		controller.registry = registry
		return controller

	@pytest.fixture
	def mock_llm(self):
		return Mock(spec=BaseChatModel)

	@pytest.fixture
	def mock_browser(self):
		return Mock(spec=Browser)

	@pytest.fixture
	def mock_browser_context(self):
		return Mock(spec=BrowserContext)

	def test_convert_initial_actions(self, mock_controller, mock_llm, mock_browser, mock_browser_context):  # type: ignore
		"""
		Test that the _convert_initial_actions method correctly converts
		dictionary-based actions to ActionModel instances.

		This test ensures that:
		1. The method processes the initial actions correctly.
		2. The correct param_model is called with the right parameters.
		3. The ActionModel is created with the validated parameters.
		4. The method returns a list of ActionModel instances.
		"""
		# Arrange
		agent = Agent(
			task='Test task', llm=mock_llm, controller=mock_controller, browser=mock_browser, browser_context=mock_browser_context
		)
		initial_actions = [{'test_action': {'param1': 'value1', 'param2': 'value2'}}]

		# Mock the ActionModel
		mock_action_model = MagicMock(spec=ActionModel)
		mock_action_model_instance = MagicMock()
		mock_action_model.return_value = mock_action_model_instance
		agent.ActionModel = mock_action_model  # type: ignore

		# Act
		result = agent._convert_initial_actions(initial_actions)

		# Assert
		assert len(result) == 1
		mock_controller.registry.registry.actions['test_action'].param_model.assert_called_once_with(  # type: ignore
			param1='value1', param2='value2'
		)
		mock_action_model.assert_called_once()
		assert isinstance(result[0], MagicMock)
		assert result[0] == mock_action_model_instance

		# Check that the ActionModel was called with the correct parameters
		call_args = mock_action_model.call_args[1]
		assert 'test_action' in call_args
		assert call_args['test_action'] == mock_controller.registry.registry.actions['test_action'].param_model.return_value  # type: ignore

	@pytest.mark.asyncio
	async def test_step_error_handling(self):
		"""
		Test the error handling in the step method of the Agent class.
		This test simulates a failure in the get_next_action method and
		checks if the error is properly handled and recorded.
		"""
		# Mock the LLM
		mock_llm = MagicMock(spec=BaseChatModel)

		# Mock the MessageManager
		with patch('browser_use.agent.service.MessageManager') as mock_message_manager:
			# Create an Agent instance with mocked dependencies
			agent = Agent(task='Test task', llm=mock_llm)

			# Mock the get_next_action method to raise an exception
			agent.get_next_action = AsyncMock(side_effect=ValueError('Test error'))

			# Mock the browser_context
			agent.browser_context = AsyncMock()
			agent.browser_context.get_state = AsyncMock(
				return_value=BrowserState(
					url='https://example.com',
					title='Example',
					element_tree=MagicMock(),  # Mocked element tree
					tabs=[],
					selector_map={},
					screenshot='',
				)
			)

			# Mock the controller
			agent.controller = AsyncMock()

			# Call the step method
			await agent.step()

			# Assert that the error was handled and recorded
			assert agent.consecutive_failures == 1
			assert len(agent._last_result) == 1
			assert isinstance(agent._last_result[0], ActionResult)
			assert 'Test error' in agent._last_result[0].error
			assert agent._last_result[0].include_in_memory is True


class TestRegistry:
	@pytest.fixture
	def registry_with_excludes(self):
		return Registry(exclude_actions=['excluded_action'])

	def test_action_decorator_with_excluded_action(self, registry_with_excludes):
		"""
		Test that the action decorator does not register an action
		if it's in the exclude_actions list.
		"""

		# Define a function to be decorated
		def excluded_action():
			pass

		# Apply the action decorator
		decorated_func = registry_with_excludes.action(description='This should be excluded')(excluded_action)

		# Assert that the decorated function is the same as the original
		assert decorated_func == excluded_action

		# Assert that the action was not added to the registry
		assert 'excluded_action' not in registry_with_excludes.registry.actions

		# Define another function that should be included
		def included_action():
			pass

		# Apply the action decorator to an included action
		registry_with_excludes.action(description='This should be included')(included_action)

		# Assert that the included action was added to the registry
		assert 'included_action' in registry_with_excludes.registry.actions

	@pytest.mark.asyncio
	async def test_execute_action_with_and_without_browser_context(self):
		"""
		Test that the execute_action method correctly handles actions with and without a browser context.
		This test ensures that:
		1. An action requiring a browser context is executed correctly.
		2. An action not requiring a browser context is executed correctly.
		3. The browser context is passed to the action function when required.
		4. The action function receives the correct parameters.
		5. The method raises an error when a browser context is required but not provided.
		"""
		registry = Registry()

		# Define a mock action model
		class TestActionModel(BaseModel):
			param1: str

		# Define mock action functions
		async def test_action_with_browser(param1: str, browser):
			return f'Action executed with {param1} and browser'

		async def test_action_without_browser(param1: str):
			return f'Action executed with {param1}'

		# Register the actions
		registry.registry.actions['test_action_with_browser'] = MagicMock(
			function=AsyncMock(side_effect=test_action_with_browser),
			param_model=TestActionModel,
			description='Test action with browser',
		)

		registry.registry.actions['test_action_without_browser'] = MagicMock(
			function=AsyncMock(side_effect=test_action_without_browser),
			param_model=TestActionModel,
			description='Test action without browser',
		)

		# Mock BrowserContext
		mock_browser = MagicMock()

		# Execute the action with a browser context
		result_with_browser = await registry.execute_action(
			'test_action_with_browser', {'param1': 'test_value'}, browser=mock_browser
		)
		assert result_with_browser == 'Action executed with test_value and browser'

		# Execute the action without a browser context
		result_without_browser = await registry.execute_action('test_action_without_browser', {'param1': 'test_value'})
		assert result_without_browser == 'Action executed with test_value'

		# Test error when browser is required but not provided
		with pytest.raises(RuntimeError, match='Action test_action_with_browser requires browser but none provided'):
			await registry.execute_action('test_action_with_browser', {'param1': 'test_value'})

		# Verify that the action functions were called with correct parameters
		registry.registry.actions['test_action_with_browser'].function.assert_called_once_with(
			param1='test_value', browser=mock_browser
		)
		registry.registry.actions['test_action_without_browser'].function.assert_called_once_with(param1='test_value')


class TestAgentRetry:
	@pytest.fixture
	def mock_llm(self):
		return AsyncMock()

	@pytest.fixture
	def mock_controller(self):
		controller = Mock()
		controller.registry = Mock()
		controller.registry.registry = Mock()
		controller.registry.registry.actions = {}
		return controller

	@pytest.fixture
	def mock_browser_context(self):
		browser_context = Mock()
		browser_context.get_state = AsyncMock(
			return_value=BrowserState(
				url='https://parabank.parasoft.com/parabank/index.htm',
				title='ParaBank',
				element_tree=MagicMock(),
				tabs=[],
				selector_map={},
				screenshot='',
			)
		)
		return browser_context

	@pytest.fixture
	def mock_action_model(self):
		action_model = Mock(spec=ActionModel)
		return action_model

	@pytest.mark.asyncio
	async def test_step_empty_action_retry(self, mock_llm, mock_controller, mock_browser_context, mock_action_model):
		"""
		Test that the step method retries and handles empty actions correctly.
		"""
		# Arrange
		agent = Agent(
			task='Test task',
			llm=mock_llm,
			controller=mock_controller,
			browser=Mock(),
			browser_context=mock_browser_context,
		)
		agent.ActionModel = mock_action_model  # Inject the mock ActionModel

		# Mock get_next_action to return empty action the first time, then a valid action
		empty_model_output = MagicMock()
		empty_model_output.action = []  # Empty action
		valid_model_output = MagicMock()
		valid_action = MagicMock()
		valid_model_output.action = [valid_action]

		mock_llm.return_value.invoke.side_effect = [empty_model_output, valid_model_output]
		agent.get_next_action = mock_llm.return_value.invoke

		# Act
		await agent.step()

		# Assert
		# Check that get_next_action was called twice (initial call + retry)
		assert agent.get_next_action.call_count == 2
		# Check that the LLM was called twice
		assert mock_llm.return_value.invoke.call_count == 2

		# Check that the second call to get_next_action included the clarification message
		_, retry_messages = mock_llm.return_value.invoke.call_args_list[1]
		assert len(retry_messages[0]) == 2  # input_messages + clarification message
		assert isinstance(retry_messages[0][1], HumanMessage)
		assert 'You forgot to return an action' in retry_messages[0][1].content

		# Check that _last_result contains the valid action
		assert len(agent._last_result) == 1
		assert agent._last_result[0].action == valid_action

	@pytest.mark.asyncio
	async def test_step_empty_action_retry_and_fail(self, mock_llm, mock_controller, mock_browser_context, mock_action_model):
		"""
		Test that the step method handles the case where get_next_action returns
		empty actions twice, and inserts a safe noop action.
		"""
		# Arrange
		agent = Agent(
			task='Test task',
			llm=mock_llm,
			controller=mock_controller,
			browser=Mock(),
			browser_context=mock_browser_context,
		)
		agent.ActionModel = mock_action_model  # Inject the mock ActionModel

		# Mock get_next_action to return empty action both times
		empty_model_output = MagicMock()
		empty_model_output.action = []  # Empty action
		mock_llm.return_value.invoke.return_value = empty_model_output
		agent.get_next_action = mock_llm.return_value.invoke

		# Mock the ActionModel instance creation
		mock_action_instance = MagicMock()
		mock_action_model.return_value = mock_action_instance

		# Act
		await agent.step()

		# Assert
		# Check that get_next_action was called twice
		assert agent.get_next_action.call_count == 2
		# Check that the LLM was called twice
		assert mock_llm.return_value.invoke.call_count == 2

		# Check that ActionModel was instantiated with the noop action
		mock_action_model.assert_called_once()
		call_args = mock_action_model.call_args[1]
		assert 'done' in call_args
		assert call_args['done'] == {'success': False, 'text': 'No action returned, safe exit.'}

		# Check that _last_result contains the noop action
		assert len(agent._last_result) == 1
		assert agent._last_result[0].action == mock_action_instance
````

## File: browser_use/agent/playwright_script_helpers.py
````python
from patchright.async_api import Page


# --- Helper Function for Replacing Sensitive Data ---
def replace_sensitive_data(text: str, sensitive_map: dict) -> str:
	"""Replaces sensitive data placeholders in text."""
	if not isinstance(text, str):
		return text
	for placeholder, value in sensitive_map.items():
		replacement_value = str(value) if value is not None else ''
		text = text.replace(f'<secret>{placeholder}</secret>', replacement_value)
	return text


# --- Helper Function for Robust Action Execution ---
class PlaywrightActionError(Exception):
	"""Custom exception for errors during Playwright script action execution."""

	pass


async def _try_locate_and_act(page: Page, selector: str, action_type: str, text: str | None = None, step_info: str = '') -> None:
	"""
	Attempts an action (click/fill) with XPath fallback by trimming prefixes.
	Raises PlaywrightActionError if the action fails after all fallbacks.
	"""
	print(f'Attempting {action_type} ({step_info}) using selector: {repr(selector)}')
	original_selector = selector
	MAX_FALLBACKS = 50  # Increased fallbacks
	# Increased timeouts for potentially slow pages
	INITIAL_TIMEOUT = 10000  # Milliseconds for the first attempt (10 seconds)
	FALLBACK_TIMEOUT = 1000  # Shorter timeout for fallback attempts (1 second)

	try:
		locator = page.locator(selector).first
		if action_type == 'click':
			await locator.click(timeout=INITIAL_TIMEOUT)
		elif action_type == 'fill' and text is not None:
			await locator.fill(text, timeout=INITIAL_TIMEOUT)
		else:
			# This case should ideally not happen if called correctly
			raise PlaywrightActionError(f"Invalid action_type '{action_type}' or missing text for fill. ({step_info})")
		print(f"  Action '{action_type}' successful with original selector.")
		await page.wait_for_timeout(500)  # Wait after successful action
		return  # Successful exit
	except Exception as e:
		print(f"  Warning: Action '{action_type}' failed with original selector ({repr(selector)}): {e}. Starting fallback...")

		# Fallback only works for XPath selectors
		if not selector.startswith('xpath='):
			# Raise error immediately if not XPath, as fallback won't work
			raise PlaywrightActionError(
				f"Action '{action_type}' failed. Fallback not possible for non-XPath selector: {repr(selector)}. ({step_info})"
			)

		xpath_parts = selector.split('=', 1)
		if len(xpath_parts) < 2:
			raise PlaywrightActionError(
				f"Action '{action_type}' failed. Could not extract XPath string from selector: {repr(selector)}. ({step_info})"
			)
		xpath = xpath_parts[1]  # Correctly get the XPath string

		segments = [seg for seg in xpath.split('/') if seg]

		for i in range(1, min(MAX_FALLBACKS + 1, len(segments))):
			trimmed_xpath_raw = '/'.join(segments[i:])
			fallback_xpath = f'xpath=//{trimmed_xpath_raw}'

			print(f'    Fallback attempt {i}/{MAX_FALLBACKS}: Trying selector: {repr(fallback_xpath)}')
			try:
				locator = page.locator(fallback_xpath).first
				if action_type == 'click':
					await locator.click(timeout=FALLBACK_TIMEOUT)
				elif action_type == 'fill' and text is not None:
					try:
						await locator.clear(timeout=FALLBACK_TIMEOUT)
						await page.wait_for_timeout(100)
					except Exception as clear_error:
						print(f'    Warning: Failed to clear field during fallback ({step_info}): {clear_error}')
					await locator.fill(text, timeout=FALLBACK_TIMEOUT)

				print(f"    Action '{action_type}' successful with fallback selector: {repr(fallback_xpath)}")
				await page.wait_for_timeout(500)
				return  # Successful exit after fallback
			except Exception as fallback_e:
				print(f'    Fallback attempt {i} failed: {fallback_e}')
				if i == MAX_FALLBACKS:
					# Raise exception after exhausting fallbacks
					raise PlaywrightActionError(
						f"Action '{action_type}' failed after {MAX_FALLBACKS} fallback attempts. Original selector: {repr(original_selector)}. ({step_info})"
					)

	# This part should not be reachable if logic is correct, but added as safeguard
	raise PlaywrightActionError(f"Action '{action_type}' failed unexpectedly for {repr(original_selector)}. ({step_info})")
````

## File: examples/custom-functions/file_upload.py
````python
import os
import sys
from pathlib import Path

import anyio

from browser_use.agent.views import ActionResult

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
import logging

from langchain_openai import ChatOpenAI

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

logger = logging.getLogger(__name__)

# Initialize controller first
browser = Browser(
	config=BrowserConfig(
		headless=False,
		browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
	)
)
controller = Controller()


@controller.action(
	'Upload file to interactive element with file path ',
)
async def upload_file(index: int, path: str, browser: BrowserContext, available_file_paths: list[str]):
	if path not in available_file_paths:
		return ActionResult(error=f'File path {path} is not available')

	if not os.path.exists(path):
		return ActionResult(error=f'File {path} does not exist')

	dom_el = await browser.get_dom_element_by_index(index)

	file_upload_dom_el = dom_el.get_file_upload_element()

	if file_upload_dom_el is None:
		msg = f'No file upload element found at index {index}'
		logger.info(msg)
		return ActionResult(error=msg)

	file_upload_el = await browser.get_locate_element(file_upload_dom_el)

	if file_upload_el is None:
		msg = f'No file upload element found at index {index}'
		logger.info(msg)
		return ActionResult(error=msg)

	try:
		await file_upload_el.set_input_files(path)
		msg = f'Successfully uploaded file to index {index}'
		logger.info(msg)
		return ActionResult(extracted_content=msg, include_in_memory=True)
	except Exception as e:
		msg = f'Failed to upload file to index {index}: {str(e)}'
		logger.info(msg)
		return ActionResult(error=msg)


@controller.action('Read the file content of a file given a path')
async def read_file(path: str, available_file_paths: list[str]):
	if path not in available_file_paths:
		return ActionResult(error=f'File path {path} is not available')

	async with await anyio.open_file(path, 'r') as f:
		content = await f.read()
	msg = f'File content: {content}'
	logger.info(msg)
	return ActionResult(extracted_content=msg, include_in_memory=True)


def create_file(file_type: str = 'txt'):
	with open(f'tmp.{file_type}', 'w') as f:
		f.write('test')
	file_path = Path.cwd() / f'tmp.{file_type}'
	logger.info(f'Created file: {file_path}')
	return str(file_path)


async def main():
	task = 'Go to https://kzmpmkh2zfk1ojnpxfn1.lite.vusercontent.net/ and - read the file content and upload them to fields'

	available_file_paths = [create_file('txt'), create_file('pdf'), create_file('csv')]

	model = ChatOpenAI(model='gpt-4o')
	agent = Agent(
		task=task,
		llm=model,
		controller=controller,
		browser=browser,
		available_file_paths=available_file_paths,
	)

	await agent.run()

	await browser.close()

	input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(main())
````

## File: browser_use/agent/playwright_script_generator.py
````python
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from browser_use.browser.browser import BrowserConfig
from browser_use.browser.context import BrowserContextConfig

logger = logging.getLogger(__name__)


class PlaywrightScriptGenerator:
	"""Generates a Playwright script from AgentHistoryList."""

	def __init__(
		self,
		history_list: List[Dict[str, Any]],
		sensitive_data_keys: Optional[List[str]] = None,
		browser_config: Optional[BrowserConfig] = None,
		context_config: Optional[BrowserContextConfig] = None,
	):
		"""
		Initializes the script generator.

		Args:
		    history_list: A list of dictionaries, where each dictionary represents an AgentHistory item.
		                 Expected to be raw dictionaries from `AgentHistoryList.model_dump()`.
		    sensitive_data_keys: A list of keys used as placeholders for sensitive data.
		    browser_config: Configuration from the original Browser instance.
		    context_config: Configuration from the original BrowserContext instance.
		"""
		self.history = history_list
		self.sensitive_data_keys = sensitive_data_keys or []
		self.browser_config = browser_config
		self.context_config = context_config
		self._imports_helpers_added = False
		self._page_counter = 0  # Track pages for tab management

		# Dictionary mapping action types to handler methods
		self._action_handlers = {
			'go_to_url': self._map_go_to_url,
			'wait': self._map_wait,
			'input_text': self._map_input_text,
			'click_element': self._map_click_element,
			'click_element_by_index': self._map_click_element,  # Map legacy action
			'scroll_down': self._map_scroll_down,
			'scroll_up': self._map_scroll_up,
			'send_keys': self._map_send_keys,
			'go_back': self._map_go_back,
			'open_tab': self._map_open_tab,
			'close_tab': self._map_close_tab,
			'switch_tab': self._map_switch_tab,
			'search_google': self._map_search_google,
			'drag_drop': self._map_drag_drop,
			'extract_content': self._map_extract_content,
			'click_download_button': self._map_click_download_button,
			'done': self._map_done,
		}

	def _generate_browser_launch_args(self) -> str:
		"""Generates the arguments string for browser launch based on BrowserConfig."""
		if not self.browser_config:
			# Default launch if no config provided
			return 'headless=False'

		args_dict = {
			'headless': self.browser_config.headless,
			# Add other relevant launch options here based on self.browser_config
			# Example: 'proxy': self.browser_config.proxy.model_dump() if self.browser_config.proxy else None
			# Example: 'args': self.browser_config.extra_browser_args # Be careful inheriting args
		}
		if self.browser_config.proxy:
			args_dict['proxy'] = self.browser_config.proxy.model_dump()

		# Filter out None values
		args_dict = {k: v for k, v in args_dict.items() if v is not None}

		# Format as keyword arguments string
		args_str = ', '.join(f'{key}={repr(value)}' for key, value in args_dict.items())
		return args_str

	def _generate_context_options(self) -> str:
		"""Generates the options string for context creation based on BrowserContextConfig."""
		if not self.context_config:
			return ''  # Default context

		options_dict = {}

		# Map relevant BrowserContextConfig fields to Playwright context options
		if self.context_config.user_agent:
			options_dict['user_agent'] = self.context_config.user_agent
		if self.context_config.locale:
			options_dict['locale'] = self.context_config.locale
		if self.context_config.permissions:
			options_dict['permissions'] = self.context_config.permissions
		if self.context_config.geolocation:
			options_dict['geolocation'] = self.context_config.geolocation
		if self.context_config.timezone_id:
			options_dict['timezone_id'] = self.context_config.timezone_id
		if self.context_config.http_credentials:
			options_dict['http_credentials'] = self.context_config.http_credentials
		if self.context_config.is_mobile is not None:
			options_dict['is_mobile'] = self.context_config.is_mobile
		if self.context_config.has_touch is not None:
			options_dict['has_touch'] = self.context_config.has_touch
		if self.context_config.save_recording_path:
			options_dict['record_video_dir'] = self.context_config.save_recording_path
		if self.context_config.save_har_path:
			options_dict['record_har_path'] = self.context_config.save_har_path

		# Handle viewport/window size
		if self.context_config.no_viewport:
			options_dict['no_viewport'] = True
		elif self.context_config.browser_window_size:
			options_dict['viewport'] = {
				'width': self.context_config.browser_window_size.width,
				'height': self.context_config.browser_window_size.height,
			}

		# Note: cookies_file and save_downloads_path are handled separately

		# Filter out None values
		options_dict = {k: v for k, v in options_dict.items() if v is not None}

		# Format as keyword arguments string
		options_str = ', '.join(f'{key}={repr(value)}' for key, value in options_dict.items())
		return options_str

	def _get_imports_and_helpers(self) -> List[str]:
		"""Generates necessary import statements (excluding helper functions)."""
		# Return only the standard imports needed by the main script body
		return [
			'import asyncio',
			'import json',
			'import os',
			'import sys',
			'from pathlib import Path',  # Added Path import
			'import urllib.parse',  # Needed for search_google
			'from patchright.async_api import async_playwright, Page, BrowserContext',  # Added BrowserContext
			'from dotenv import load_dotenv',
			'',
			'# Load environment variables',
			'load_dotenv(override=True)',
			'',
			# Helper function definitions are no longer here
		]

	def _get_sensitive_data_definitions(self) -> List[str]:
		"""Generates the SENSITIVE_DATA dictionary definition."""
		if not self.sensitive_data_keys:
			return ['SENSITIVE_DATA = {}', '']

		lines = ['# Sensitive data placeholders mapped to environment variables']
		lines.append('SENSITIVE_DATA = {')
		for key in self.sensitive_data_keys:
			env_var_name = key.upper()
			default_value_placeholder = f'YOUR_{env_var_name}'
			lines.append(f'    "{key}": os.getenv("{env_var_name}", {json.dumps(default_value_placeholder)}),')
		lines.append('}')
		lines.append('')
		return lines

	def _get_selector_for_action(self, history_item: dict, action_index_in_step: int) -> Optional[str]:
		"""
		Gets the selector (preferring XPath) for a given action index within a history step.
		Formats the XPath correctly for Playwright.
		"""
		state = history_item.get('state')
		if not isinstance(state, dict):
			return None
		interacted_elements = state.get('interacted_element')
		if not isinstance(interacted_elements, list):
			return None
		if action_index_in_step >= len(interacted_elements):
			return None
		element_data = interacted_elements[action_index_in_step]
		if not isinstance(element_data, dict):
			return None

		# Prioritize XPath
		xpath = element_data.get('xpath')
		if isinstance(xpath, str) and xpath.strip():
			if not xpath.startswith('xpath=') and not xpath.startswith('/') and not xpath.startswith('//'):
				xpath_selector = f'xpath=//{xpath}'  # Make relative if not already
			elif not xpath.startswith('xpath='):
				xpath_selector = f'xpath={xpath}'  # Add prefix if missing
			else:
				xpath_selector = xpath
			return xpath_selector

		# Fallback to CSS selector if XPath is missing
		css_selector = element_data.get('css_selector')
		if isinstance(css_selector, str) and css_selector.strip():
			return css_selector  # Use CSS selector as is

		logger.warning(
			f'Could not find a usable XPath or CSS selector for action index {action_index_in_step} (element index {element_data.get("highlight_index", "N/A")}).'
		)
		return None

	def _get_goto_timeout(self) -> int:
		"""Gets the page navigation timeout in milliseconds."""
		default_timeout = 90000  # Default 90 seconds
		if self.context_config and self.context_config.maximum_wait_page_load_time:
			# Convert seconds to milliseconds
			return int(self.context_config.maximum_wait_page_load_time * 1000)
		return default_timeout

	# --- Action Mapping Methods ---
	def _map_go_to_url(self, params: dict, step_info_str: str, **kwargs) -> List[str]:
		url = params.get('url')
		goto_timeout = self._get_goto_timeout()
		script_lines = []
		if url and isinstance(url, str):
			escaped_url = json.dumps(url)
			script_lines.append(f'            print(f"Navigating to: {url} ({step_info_str})")')
			script_lines.append(f'            await page.goto({escaped_url}, timeout={goto_timeout})')
			script_lines.append(f"            await page.wait_for_load_state('load', timeout={goto_timeout})")
			script_lines.append('            await page.wait_for_timeout(1000)')  # Short pause
		else:
			script_lines.append(f'            # Skipping go_to_url ({step_info_str}): missing or invalid url')
		return script_lines

	def _map_wait(self, params: dict, step_info_str: str, **kwargs) -> List[str]:
		seconds = params.get('seconds', 3)
		try:
			wait_seconds = int(seconds)
		except (ValueError, TypeError):
			wait_seconds = 3
		return [
			f'            print(f"Waiting for {wait_seconds} seconds... ({step_info_str})")',
			f'            await asyncio.sleep({wait_seconds})',
		]

	def _map_input_text(
		self, params: dict, history_item: dict, action_index_in_step: int, step_info_str: str, **kwargs
	) -> List[str]:
		index = params.get('index')
		text = params.get('text', '')
		selector = self._get_selector_for_action(history_item, action_index_in_step)
		script_lines = []
		if selector and index is not None:
			clean_text_expression = f'replace_sensitive_data({json.dumps(str(text))}, SENSITIVE_DATA)'
			escaped_selector = json.dumps(selector)
			escaped_step_info = json.dumps(step_info_str)
			script_lines.append(
				f'            await _try_locate_and_act(page, {escaped_selector}, "fill", text={clean_text_expression}, step_info={escaped_step_info})'
			)
		else:
			script_lines.append(
				f'            # Skipping input_text ({step_info_str}): missing index ({index}) or selector ({selector})'
			)
		return script_lines

	def _map_click_element(
		self, params: dict, history_item: dict, action_index_in_step: int, step_info_str: str, action_type: str, **kwargs
	) -> List[str]:
		if action_type == 'click_element_by_index':
			logger.warning(f"Mapping legacy 'click_element_by_index' to 'click_element' ({step_info_str})")
		index = params.get('index')
		selector = self._get_selector_for_action(history_item, action_index_in_step)
		script_lines = []
		if selector and index is not None:
			escaped_selector = json.dumps(selector)
			escaped_step_info = json.dumps(step_info_str)
			script_lines.append(
				f'            await _try_locate_and_act(page, {escaped_selector}, "click", step_info={escaped_step_info})'
			)
		else:
			script_lines.append(
				f'            # Skipping {action_type} ({step_info_str}): missing index ({index}) or selector ({selector})'
			)
		return script_lines

	def _map_scroll_down(self, params: dict, step_info_str: str, **kwargs) -> List[str]:
		amount = params.get('amount')
		script_lines = []
		if amount and isinstance(amount, int):
			script_lines.append(f'            print(f"Scrolling down by {amount} pixels ({step_info_str})")')
			script_lines.append(f"            await page.evaluate('window.scrollBy(0, {amount})')")
		else:
			script_lines.append(f'            print(f"Scrolling down by one page height ({step_info_str})")')
			script_lines.append("            await page.evaluate('window.scrollBy(0, window.innerHeight)')")
		script_lines.append('            await page.wait_for_timeout(500)')
		return script_lines

	def _map_scroll_up(self, params: dict, step_info_str: str, **kwargs) -> List[str]:
		amount = params.get('amount')
		script_lines = []
		if amount and isinstance(amount, int):
			script_lines.append(f'            print(f"Scrolling up by {amount} pixels ({step_info_str})")')
			script_lines.append(f"            await page.evaluate('window.scrollBy(0, -{amount})')")
		else:
			script_lines.append(f'            print(f"Scrolling up by one page height ({step_info_str})")')
			script_lines.append("            await page.evaluate('window.scrollBy(0, -window.innerHeight)')")
		script_lines.append('            await page.wait_for_timeout(500)')
		return script_lines

	def _map_send_keys(self, params: dict, step_info_str: str, **kwargs) -> List[str]:
		keys = params.get('keys')
		script_lines = []
		if keys and isinstance(keys, str):
			escaped_keys = json.dumps(keys)
			script_lines.append(f'            print(f"Sending keys: {keys} ({step_info_str})")')
			script_lines.append(f'            await page.keyboard.press({escaped_keys})')
			script_lines.append('            await page.wait_for_timeout(500)')
		else:
			script_lines.append(f'            # Skipping send_keys ({step_info_str}): missing or invalid keys')
		return script_lines

	def _map_go_back(self, params: dict, step_info_str: str, **kwargs) -> List[str]:
		goto_timeout = self._get_goto_timeout()
		return [
			'            await asyncio.sleep(60)  # Wait 1 minute (important) before going back',
			f'            print(f"Navigating back using browser history ({step_info_str})")',
			f'            await page.go_back(timeout={goto_timeout})',
			f"            await page.wait_for_load_state('load', timeout={goto_timeout})",
			'            await page.wait_for_timeout(1000)',
		]

	def _map_open_tab(self, params: dict, step_info_str: str, **kwargs) -> List[str]:
		url = params.get('url')
		goto_timeout = self._get_goto_timeout()
		script_lines = []
		if url and isinstance(url, str):
			escaped_url = json.dumps(url)
			script_lines.append(f'            print(f"Opening new tab and navigating to: {url} ({step_info_str})")')
			script_lines.append('            page = await context.new_page()')
			script_lines.append(f'            await page.goto({escaped_url}, timeout={goto_timeout})')
			script_lines.append(f"            await page.wait_for_load_state('load', timeout={goto_timeout})")
			script_lines.append('            await page.wait_for_timeout(1000)')
			self._page_counter += 1  # Increment page counter
		else:
			script_lines.append(f'            # Skipping open_tab ({step_info_str}): missing or invalid url')
		return script_lines

	def _map_close_tab(self, params: dict, step_info_str: str, **kwargs) -> List[str]:
		page_id = params.get('page_id')
		script_lines = []
		if page_id is not None:
			script_lines.extend(
				[
					f'            print(f"Attempting to close tab with page_id {page_id} ({step_info_str})")',
					f'            if {page_id} < len(context.pages):',
					f'                target_page = context.pages[{page_id}]',
					'                await target_page.close()',
					'                await page.wait_for_timeout(500)',
					'                if context.pages: page = context.pages[-1]',  # Switch to last page
					'                else:',
					"                    print('  Warning: No pages left after closing tab. Cannot switch.', file=sys.stderr)",
					'                    # Optionally, create a new page here if needed: page = await context.new_page()',
					'                if page: await page.bring_to_front()',  # Bring to front if page exists
					'            else:',
					f'                print(f"  Warning: Tab with page_id {page_id} not found to close ({step_info_str})", file=sys.stderr)',
				]
			)
		else:
			script_lines.append(f'            # Skipping close_tab ({step_info_str}): missing page_id')
		return script_lines

	def _map_switch_tab(self, params: dict, step_info_str: str, **kwargs) -> List[str]:
		page_id = params.get('page_id')
		script_lines = []
		if page_id is not None:
			script_lines.extend(
				[
					f'            print(f"Switching to tab with page_id {page_id} ({step_info_str})")',
					f'            if {page_id} < len(context.pages):',
					f'                page = context.pages[{page_id}]',
					'                await page.bring_to_front()',
					"                await page.wait_for_load_state('load', timeout=15000)",
					'                await page.wait_for_timeout(500)',
					'            else:',
					f'                print(f"  Warning: Tab with page_id {page_id} not found to switch ({step_info_str})", file=sys.stderr)',
				]
			)
		else:
			script_lines.append(f'            # Skipping switch_tab ({step_info_str}): missing page_id')
		return script_lines

	def _map_search_google(self, params: dict, step_info_str: str, **kwargs) -> List[str]:
		query = params.get('query')
		goto_timeout = self._get_goto_timeout()
		script_lines = []
		if query and isinstance(query, str):
			clean_query = f'replace_sensitive_data({json.dumps(query)}, SENSITIVE_DATA)'
			search_url_expression = f'f"https://www.google.com/search?q={{ urllib.parse.quote_plus({clean_query}) }}&udm=14"'
			script_lines.extend(
				[
					f'            search_url = {search_url_expression}',
					f'            print(f"Searching Google for query related to: {{ {clean_query} }} ({step_info_str})")',
					f'            await page.goto(search_url, timeout={goto_timeout})',
					f"            await page.wait_for_load_state('load', timeout={goto_timeout})",
					'            await page.wait_for_timeout(1000)',
				]
			)
		else:
			script_lines.append(f'            # Skipping search_google ({step_info_str}): missing or invalid query')
		return script_lines

	def _map_drag_drop(self, params: dict, step_info_str: str, **kwargs) -> List[str]:
		source_sel = params.get('element_source')
		target_sel = params.get('element_target')
		source_coords = (params.get('coord_source_x'), params.get('coord_source_y'))
		target_coords = (params.get('coord_target_x'), params.get('coord_target_y'))
		script_lines = [f'            print(f"Attempting drag and drop ({step_info_str})")']
		if source_sel and target_sel:
			escaped_source = json.dumps(source_sel)
			escaped_target = json.dumps(target_sel)
			script_lines.append(f'            await page.drag_and_drop({escaped_source}, {escaped_target})')
			script_lines.append(f"            print(f'  Dragged element {escaped_source} to {escaped_target}')")
		elif all(c is not None for c in source_coords) and all(c is not None for c in target_coords):
			sx, sy = source_coords
			tx, ty = target_coords
			script_lines.extend(
				[
					f'            await page.mouse.move({sx}, {sy})',
					'            await page.mouse.down()',
					f'            await page.mouse.move({tx}, {ty})',
					'            await page.mouse.up()',
					f"            print(f'  Dragged from ({sx},{sy}) to ({tx},{ty})')",
				]
			)
		else:
			script_lines.append(
				f'            # Skipping drag_drop ({step_info_str}): requires either element selectors or full coordinates'
			)
		script_lines.append('            await page.wait_for_timeout(500)')
		return script_lines

	def _map_extract_content(self, params: dict, step_info_str: str, **kwargs) -> List[str]:
		goal = params.get('goal', 'content')
		logger.warning(f"Action 'extract_content' ({step_info_str}) cannot be directly translated to Playwright script.")
		return [f'            # Action: extract_content (Goal: {goal}) - Skipped in Playwright script ({step_info_str})']

	def _map_click_download_button(
		self, params: dict, history_item: dict, action_index_in_step: int, step_info_str: str, **kwargs
	) -> List[str]:
		index = params.get('index')
		selector = self._get_selector_for_action(history_item, action_index_in_step)
		download_dir_in_script = "'./files'"  # Default
		if self.context_config and self.context_config.save_downloads_path:
			download_dir_in_script = repr(self.context_config.save_downloads_path)

		script_lines = []
		if selector and index is not None:
			script_lines.append(
				f'            print(f"Attempting to download file by clicking element ({selector}) ({step_info_str})")'
			)
			script_lines.append('            try:')
			script_lines.append(
				'                async with page.expect_download(timeout=120000) as download_info:'
			)  # 2 min timeout
			step_info_for_download = f'{step_info_str} (triggering download)'
			script_lines.append(
				f'                    await _try_locate_and_act(page, {json.dumps(selector)}, "click", step_info={json.dumps(step_info_for_download)})'
			)
			script_lines.append('                download = await download_info.value')
			script_lines.append(f'                configured_download_dir = {download_dir_in_script}')
			script_lines.append('                download_dir_path = Path(configured_download_dir).resolve()')
			script_lines.append('                download_dir_path.mkdir(parents=True, exist_ok=True)')
			script_lines.append(
				"                base, ext = os.path.splitext(download.suggested_filename or f'download_{{len(list(download_dir_path.iterdir())) + 1}}.tmp')"
			)
			script_lines.append('                counter = 1')
			script_lines.append("                download_path_obj = download_dir_path / f'{base}{ext}'")
			script_lines.append('                while download_path_obj.exists():')
			script_lines.append("                    download_path_obj = download_dir_path / f'{base}({{counter}}){ext}'")
			script_lines.append('                    counter += 1')
			script_lines.append('                await download.save_as(str(download_path_obj))')
			script_lines.append("                print(f'  File downloaded successfully to: {str(download_path_obj)}')")
			script_lines.append('            except PlaywrightActionError as pae:')
			script_lines.append('                raise pae')  # Re-raise to stop script
			script_lines.append('            except Exception as download_err:')
			script_lines.append(
				f"                raise PlaywrightActionError(f'Download failed for {step_info_str}: {{download_err}}') from download_err"
			)
		else:
			script_lines.append(
				f'            # Skipping click_download_button ({step_info_str}): missing index ({index}) or selector ({selector})'
			)
		return script_lines

	def _map_done(self, params: dict, step_info_str: str, **kwargs) -> List[str]:
		script_lines = []
		if isinstance(params, dict):
			final_text = params.get('text', '')
			success_status = params.get('success', False)
			escaped_final_text_with_placeholders = json.dumps(str(final_text))
			script_lines.append(f'            print("\\n--- Task marked as Done by agent ({step_info_str}) ---")')
			script_lines.append(f'            print(f"Agent reported success: {success_status}")')
			script_lines.append('            # Final Message from agent (may contain placeholders):')
			script_lines.append(
				f'            final_message = replace_sensitive_data({escaped_final_text_with_placeholders}, SENSITIVE_DATA)'
			)
			script_lines.append('            print(final_message)')
		else:
			script_lines.append(f'            print("\\n--- Task marked as Done by agent ({step_info_str}) ---")')
			script_lines.append('            print("Success: N/A (invalid params)")')
			script_lines.append('            print("Final Message: N/A (invalid params)")')
		return script_lines

	def _map_action_to_playwright(
		self,
		action_dict: dict,
		history_item: dict,
		previous_history_item: Optional[dict],
		action_index_in_step: int,
		step_info_str: str,
	) -> List[str]:
		"""
		Translates a single action dictionary into Playwright script lines using dictionary dispatch.
		"""
		if not isinstance(action_dict, dict) or not action_dict:
			return [f'            # Invalid action format: {action_dict} ({step_info_str})']

		action_type = next(iter(action_dict.keys()), None)
		params = action_dict.get(action_type)

		if not action_type or params is None:
			if action_dict == {}:
				return [f'            # Empty action dictionary found ({step_info_str})']
			return [f'            # Could not determine action type or params: {action_dict} ({step_info_str})']

		# Get the handler function from the dictionary
		handler = self._action_handlers.get(action_type)

		if handler:
			# Call the specific handler method
			return handler(
				params=params,
				history_item=history_item,
				action_index_in_step=action_index_in_step,
				step_info_str=step_info_str,
				action_type=action_type,  # Pass action_type for legacy handling etc.
				previous_history_item=previous_history_item,
			)
		else:
			# Handle unsupported actions
			logger.warning(f'Unsupported action type encountered: {action_type} ({step_info_str})')
			return [f'            # Unsupported action type: {action_type} ({step_info_str})']

	def generate_script_content(self) -> str:
		"""Generates the full Playwright script content as a string."""
		script_lines = []
		self._page_counter = 0  # Reset page counter for new script generation

		if not self._imports_helpers_added:
			script_lines.extend(self._get_imports_and_helpers())
			self._imports_helpers_added = True

		# Read helper script content
		helper_script_path = Path(__file__).parent / 'playwright_script_helpers.py'
		try:
			with open(helper_script_path, 'r', encoding='utf-8') as f_helper:
				helper_script_content = f_helper.read()
		except FileNotFoundError:
			logger.error(f'Helper script not found at {helper_script_path}. Cannot generate script.')
			return '# Error: Helper script file missing.'
		except Exception as e:
			logger.error(f'Error reading helper script {helper_script_path}: {e}')
			return f'# Error: Could not read helper script: {e}'

		script_lines.extend(self._get_sensitive_data_definitions())

		# Add the helper script content after imports and sensitive data
		script_lines.append('\n# --- Helper Functions (from playwright_script_helpers.py) ---')
		script_lines.append(helper_script_content)
		script_lines.append('# --- End Helper Functions ---')

		# Generate browser launch and context creation code
		browser_launch_args = self._generate_browser_launch_args()
		context_options = self._generate_context_options()
		# Determine browser type (defaulting to chromium)
		browser_type = 'chromium'
		if self.browser_config and self.browser_config.browser_class in ['firefox', 'webkit']:
			browser_type = self.browser_config.browser_class

		script_lines.extend(
			[
				'async def run_generated_script():',
				'    global SENSITIVE_DATA',  # Ensure sensitive data is accessible
				'    async with async_playwright() as p:',
				'        browser = None',
				'        context = None',
				'        page = None',
				'        exit_code = 0 # Default success exit code',
				'        try:',
				f"            print('Launching {browser_type} browser...')",
				# Use generated launch args, remove slow_mo
				f'            browser = await p.{browser_type}.launch({browser_launch_args})',
				# Use generated context options
				f'            context = await browser.new_context({context_options})',
				"            print('Browser context created.')",
			]
		)

		# Add cookie loading logic if cookies_file is specified
		if self.context_config and self.context_config.cookies_file:
			cookies_file_path = repr(self.context_config.cookies_file)
			script_lines.extend(
				[
					'            # Load cookies if specified',
					f'            cookies_path = {cookies_file_path}',
					'            if cookies_path and os.path.exists(cookies_path):',
					'                try:',
					"                    with open(cookies_path, 'r', encoding='utf-8') as f_cookies:",
					'                        cookies = json.load(f_cookies)',
					'                        # Validate sameSite attribute',
					"                        valid_same_site = ['Strict', 'Lax', 'None']",
					'                        for cookie in cookies:',
					"                            if 'sameSite' in cookie and cookie['sameSite'] not in valid_same_site:",
					'                                print(f\'  Warning: Fixing invalid sameSite value "{{cookie["sameSite"]}}" to None for cookie {{cookie.get("name")}}\', file=sys.stderr)',
					"                                cookie['sameSite'] = 'None'",
					'                        await context.add_cookies(cookies)',
					"                        print(f'  Successfully loaded {{len(cookies)}} cookies from {{cookies_path}}')",
					'                except Exception as cookie_err:',
					"                    print(f'  Warning: Failed to load or add cookies from {{cookies_path}}: {{cookie_err}}', file=sys.stderr)",
					'            else:',
					'                if cookies_path:',  # Only print if a path was specified but not found
					"                    print(f'  Cookie file not found at: {cookies_path}')",
					'',
				]
			)

		script_lines.extend(
			[
				'            # Initial page handling',
				'            if context.pages:',
				'                page = context.pages[0]',
				"                print('Using initial page provided by context.')",
				'            else:',
				'                page = await context.new_page()',
				"                print('Created a new page as none existed.')",
				"            print('\\n--- Starting Generated Script Execution ---')",
			]
		)

		action_counter = 0
		stop_processing_steps = False
		previous_item_dict = None

		for step_index, item_dict in enumerate(self.history):
			if stop_processing_steps:
				break

			if not isinstance(item_dict, dict):
				logger.warning(f'Skipping step {step_index + 1}: Item is not a dictionary ({type(item_dict)})')
				script_lines.append(f'\n            # --- Step {step_index + 1}: Skipped (Invalid Format) ---')
				previous_item_dict = item_dict
				continue

			script_lines.append(f'\n            # --- Step {step_index + 1} ---')
			model_output = item_dict.get('model_output')

			if not isinstance(model_output, dict) or 'action' not in model_output:
				script_lines.append('            # No valid model_output or action found for this step')
				previous_item_dict = item_dict
				continue

			actions = model_output.get('action')
			if not isinstance(actions, list):
				script_lines.append(f'            # Actions format is not a list: {type(actions)}')
				previous_item_dict = item_dict
				continue

			for action_index_in_step, action_detail in enumerate(actions):
				action_counter += 1
				script_lines.append(f'            # Action {action_counter}')

				step_info_str = f'Step {step_index + 1}, Action {action_index_in_step + 1}'
				action_lines = self._map_action_to_playwright(
					action_dict=action_detail,
					history_item=item_dict,
					previous_history_item=previous_item_dict,
					action_index_in_step=action_index_in_step,
					step_info_str=step_info_str,
				)
				script_lines.extend(action_lines)

				action_type = next(iter(action_detail.keys()), None) if isinstance(action_detail, dict) else None
				if action_type == 'done':
					stop_processing_steps = True
					break

			previous_item_dict = item_dict

		# Updated final block to include sys.exit
		script_lines.extend(
			[
				'        except PlaywrightActionError as pae:',  # Catch specific action errors
				"            print(f'\\n--- Playwright Action Error: {pae} ---', file=sys.stderr)",
				'            exit_code = 1',  # Set exit code to failure
				'        except Exception as e:',
				"            print(f'\\n--- An unexpected error occurred: {e} ---', file=sys.stderr)",
				'            import traceback',
				'            traceback.print_exc()',
				'            exit_code = 1',  # Set exit code to failure
				'        finally:',
				"            print('\\n--- Generated Script Execution Finished ---')",
				"            print('Closing browser/context...')",
				'            if context:',
				'                 try: await context.close()',
				"                 except Exception as ctx_close_err: print(f'  Warning: could not close context: {ctx_close_err}', file=sys.stderr)",
				'            if browser:',
				'                 try: await browser.close()',
				"                 except Exception as browser_close_err: print(f'  Warning: could not close browser: {browser_close_err}', file=sys.stderr)",
				"            print('Browser/context closed.')",
				'            # Exit with the determined exit code',
				'            if exit_code != 0:',
				"                print(f'Script finished with errors (exit code {exit_code}).', file=sys.stderr)",
				'                sys.exit(exit_code)',  # Exit with non-zero code on error
				'',
				'# --- Script Entry Point ---',
				"if __name__ == '__main__':",
				"    if os.name == 'nt':",
				'        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())',
				'    asyncio.run(run_generated_script())',
			]
		)

		return '\n'.join(script_lines)
````

## File: browser_use/browser/context.py
````python
"""
Playwright browser on steroids.
"""

import asyncio
import base64
import gc
import json
import logging
import os
import re
import time
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

import anyio
from patchright._impl._errors import TimeoutError
from patchright.async_api import Browser as PlaywrightBrowser
from patchright.async_api import (
	BrowserContext as PlaywrightBrowserContext,
)
from patchright.async_api import (
	ElementHandle,
	FrameLocator,
	Page,
)
from pydantic import BaseModel, ConfigDict, Field

from browser_use.browser.views import (
	BrowserError,
	BrowserState,
	TabInfo,
	URLNotAllowedError,
)
from browser_use.dom.clickable_element_processor.service import ClickableElementProcessor
from browser_use.dom.service import DomService
from browser_use.dom.views import DOMElementNode, SelectorMap
from browser_use.utils import time_execution_async, time_execution_sync

if TYPE_CHECKING:
	from browser_use.browser.browser import Browser

logger = logging.getLogger(__name__)

import platform

BROWSER_NAVBAR_HEIGHT = {
	'windows': 85,
	'darwin': 80,
	'linux': 90,
}.get(platform.system().lower(), 85)


class BrowserContextWindowSize(BaseModel):
	"""Window size configuration for browser context"""

	width: int
	height: int

	model_config = ConfigDict(
		extra='allow',  # Allow extra fields to ensure compatibility with dictionary
		populate_by_name=True,
		from_attributes=True,
	)

	# Support dict-like behavior for compatibility
	def __getitem__(self, key):
		return getattr(self, key)

	def get(self, key, default=None):
		return getattr(self, key, default)


class BrowserContextConfig(BaseModel):
	"""
	Configuration for the BrowserContext.

	Default values:
	    cookies_file: None
	        Path to cookies file for persistence

		disable_security: False
			Disable browser security features (dangerous, but cross-origin iframe support requires it)

	    minimum_wait_page_load_time: 0.5
	        Minimum time to wait before getting page state for LLM input

		wait_for_network_idle_page_load_time: 1.0
			Time to wait for network requests to finish before getting page state.
			Lower values may result in incomplete page loads.

	    maximum_wait_page_load_time: 5.0
	        Maximum time to wait for page load before proceeding anyway

	    wait_between_actions: 1.0
	        Time to wait between multiple per step actions

	    browser_window_size: BrowserContextWindowSize(width=1280, height=1100)
	        Default browser window size

	    no_viewport: False
	        Disable viewport

	    save_recording_path: None
	        Path to save video recordings

	    save_downloads_path: None
	        Path to save downloads to

	    trace_path: None
	        Path to save trace files. It will auto name the file with the TRACE_PATH/{context_id}.zip

	    locale: None
	        Specify user locale, for example en-GB, de-DE, etc. Locale will affect navigator.language value, Accept-Language request header value as well as number and date formatting rules. If not provided, defaults to the system default locale.

	    user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
	        custom user agent to use.

	    highlight_elements: True
	        Highlight elements in the DOM on the screen

	    viewport_expansion: 0
	        Viewport expansion in pixels. This amount will increase the number of elements which are included in the state what the LLM will see. If set to -1, all elements will be included (this leads to high token usage). If set to 0, only the elements which are visible in the viewport will be included.

	    allowed_domains: None
	        List of allowed domains that can be accessed. If None, all domains are allowed.
	        Example: ['example.com', 'api.example.com']

	    include_dynamic_attributes: bool = True
	        Include dynamic attributes in the CSS selector. If you want to reuse the css_selectors, it might be better to set this to False.

		  http_credentials: None
	  Dictionary with HTTP basic authentication credentials for corporate intranets (only supports one set of credentials for all URLs at the moment), e.g.
	  {"username": "bill", "password": "pa55w0rd"}

	    is_mobile: None
	        Whether the meta viewport tag is taken into account and touch events are enabled.

	    has_touch: None
	        Whether to enable touch events in the browser.

	    geolocation: None
	        Geolocation to be used in the browser context. Example: {'latitude': 59.95, 'longitude': 30.31667}

	    permissions: None
	        Browser permissions to grant. Values might include: ['geolocation', 'notifications']

	    timezone_id: None
	        Changes the timezone of the browser. Example: 'Europe/Berlin'

		force_new_context: False
			Forces a new browser context to be created. Useful when running locally with branded browser (e.g Chrome, Edge) and setting a custom config.
	"""

	model_config = ConfigDict(
		arbitrary_types_allowed=True,
		extra='ignore',
		populate_by_name=True,
		from_attributes=True,
		validate_assignment=True,
		revalidate_instances='subclass-instances',
	)

	cookies_file: str | None = None
	minimum_wait_page_load_time: float = 0.25
	wait_for_network_idle_page_load_time: float = 0.5
	maximum_wait_page_load_time: float = 5
	wait_between_actions: float = 0.5

	disable_security: bool = False  # disable_security=True is dangerous as any malicious URL visited could embed an iframe for the user's bank, and use their cookies to steal money

	browser_window_size: BrowserContextWindowSize = Field(
		default_factory=lambda: BrowserContextWindowSize(width=1280, height=1100)
	)
	no_viewport: Optional[bool] = None

	save_recording_path: str | None = None
	save_downloads_path: str | None = None
	save_har_path: str | None = None
	trace_path: str | None = None
	locale: str | None = None
	user_agent: str | None = None

	highlight_elements: bool = True
	viewport_expansion: int = 0
	allowed_domains: list[str] | None = None
	include_dynamic_attributes: bool = True
	http_credentials: dict[str, str] | None = None

	keep_alive: bool = Field(default=False, alias='_force_keep_context_alive')  # used to be called _force_keep_context_alive
	is_mobile: bool | None = None
	has_touch: bool | None = None
	geolocation: dict | None = None
	permissions: list[str] | None = None
	timezone_id: str | None = None

	force_new_context: bool = False


@dataclass
class CachedStateClickableElementsHashes:
	"""
	Clickable elements hashes for the last state
	"""

	url: str
	hashes: set[str]


class BrowserSession:
	def __init__(self, context: PlaywrightBrowserContext, cached_state: BrowserState | None = None):
		init_script = """
			(() => {
				if (!window.getEventListeners) {
					window.getEventListeners = function (node) {
						return node.__listeners || {};
					};

					// Save the original addEventListener
					const originalAddEventListener = Element.prototype.addEventListener;

					const eventProxy = {
						addEventListener: function (type, listener, options = {}) {
							// Initialize __listeners if not exists
							const defaultOptions = { once: false, passive: false, capture: false };
							if(typeof options === 'boolean') {
								options = { capture: options };
							}
							options = { ...defaultOptions, ...options };
							if (!this.__listeners) {
								this.__listeners = {};
							}

							// Initialize array for this event type if not exists
							if (!this.__listeners[type]) {
								this.__listeners[type] = [];
							}


							// Add the listener to __listeners
							this.__listeners[type].push({
								listener: listener,
								type: type,
								...options
							});

							// Call original addEventListener using the saved reference
							return originalAddEventListener.call(this, type, listener, options);
						}
					};

					Element.prototype.addEventListener = eventProxy.addEventListener;
				}
			})()
			"""
		self.active_tab = None
		self.context = context
		self.cached_state = cached_state

		self.cached_state_clickable_elements_hashes: CachedStateClickableElementsHashes | None = None

		self.context.on('page', lambda page: page.add_init_script(init_script))


@dataclass
class BrowserContextState:
	"""
	State of the browser context
	"""

	target_id: str | None = None  # CDP target ID


class BrowserContext:
	def __init__(
		self,
		browser: 'Browser',
		config: BrowserContextConfig | None = None,
		state: Optional[BrowserContextState] = None,
	):
		self.context_id = str(uuid.uuid4())

		self.config = config or BrowserContextConfig(**(browser.config.model_dump() if browser.config else {}))
		self.browser = browser

		self.state = state or BrowserContextState()

		# Initialize these as None - they'll be set up when needed
		self.session: BrowserSession | None = None
		self.active_tab: Page | None = None

	async def __aenter__(self):
		"""Async context manager entry"""
		await self._initialize_session()
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb):
		"""Async context manager exit"""
		await self.close()

	@time_execution_async('--close')
	async def close(self):
		"""Close the browser instance"""

		try:
			if self.session is None:
				return

			# Then remove CDP protocol listeners
			if self._page_event_handler and self.session.context:
				try:
					# This actually sends a CDP command to unsubscribe
					self.session.context.remove_listener('page', self._page_event_handler)
				except Exception as e:
					logger.debug(f'Failed to remove CDP listener: {e}')
				self._page_event_handler = None

			await self.save_cookies()

			if self.config.trace_path:
				try:
					await self.session.context.tracing.stop(path=os.path.join(self.config.trace_path, f'{self.context_id}.zip'))
				except Exception as e:
					logger.debug(f'Failed to stop tracing: {e}')

			# This is crucial - it closes the CDP connection
			if not self.config.keep_alive:
				logger.debug('Closing browser context')
				try:
					await self.session.context.close()
				except Exception as e:
					logger.debug(f'Failed to close context: {e}')

		finally:
			# Dereference everything
			self.active_tab = None
			self.session = None
			self._page_event_handler = None

	def __del__(self):
		"""Cleanup when object is destroyed"""
		if not self.config.keep_alive and self.session is not None:
			logger.debug('BrowserContext was not properly closed before destruction')
			try:
				# Use sync Playwright method for force cleanup
				if hasattr(self.session.context, '_impl_obj'):
					asyncio.run(self.session.context._impl_obj.close())

				self.session = None
				gc.collect()
			except Exception as e:
				logger.warning(f'Failed to force close browser context: {e}')

	@time_execution_async('--initialize_session')
	async def _initialize_session(self):
		"""Initialize the browser session"""
		logger.debug(f'🌎  Initializing new browser context with id: {self.context_id}')

		playwright_browser = await self.browser.get_playwright_browser()
		context = await self._create_context(playwright_browser)
		self._page_event_handler = None

		# Get or create a page to use
		pages = context.pages

		self.session = BrowserSession(
			context=context,
			cached_state=None,
		)

		active_page = None
		if self.browser.config.cdp_url:
			# If we have a saved target ID, try to find and activate it
			if self.state.target_id:
				targets = await self._get_cdp_targets()
				for target in targets:
					if target['targetId'] == self.state.target_id:
						# Find matching page by URL
						for page in pages:
							if page.url == target['url']:
								active_page = page
								break
						break

		# If no target ID or couldn't find it, use existing page or create new
		if not active_page:
			if (
				pages
				and pages[0].url
				and not pages[0].url.startswith('chrome://')  # skip chrome internal pages e.g. settings, history, etc
				and not pages[0].url.startswith('chrome-extension://')  # skip hidden extension background pages
			):
				active_page = pages[0]
				logger.debug('🔍  Using existing page: %s', active_page.url)
			else:
				active_page = await context.new_page()
				await active_page.goto('about:blank')
				logger.debug('🆕  Created new page: %s', active_page.url)

			# Get target ID for the active page
			if self.browser.config.cdp_url:
				targets = await self._get_cdp_targets()
				for target in targets:
					if target['url'] == active_page.url:
						self.state.target_id = target['targetId']
						break

		# Bring page to front
		logger.debug('🫨  Bringing tab to front: %s', active_page)
		await active_page.bring_to_front()
		await active_page.wait_for_load_state('load')

		# Set the viewport size for the active page
		try:
			await active_page.set_viewport_size(self.config.browser_window_size.model_dump())
			logger.debug(f'Set viewport size to {self.config.browser_window_size.width}x{self.config.browser_window_size.height}')
		except Exception as e:
			logger.debug(f'Failed to set viewport size: {e}')

		self.active_tab = active_page

		return self.session

	def _add_new_page_listener(self, context: PlaywrightBrowserContext):
		async def on_page(page: Page):
			if self.browser.config.cdp_url:
				await page.reload()  # Reload the page to avoid timeout errors
			await page.wait_for_load_state()
			logger.debug(f'📑  New page opened: {page.url}')

			if not page.url.startswith('chrome-extension://') and not page.url.startswith('chrome://'):
				self.active_tab = page

			if self.session is not None:
				self.state.target_id = None

		self._page_event_handler = on_page
		context.on('page', on_page)

	async def get_session(self) -> BrowserSession:
		"""Lazy initialization of the browser and related components"""
		if self.session is None:
			try:
				return await self._initialize_session()
			except Exception as e:
				logger.error(f'❌  Failed to create new browser session: {e} (did the browser process quit?)')
				raise e
		return self.session

	async def get_current_page(self) -> Page:
		"""Get the current page"""
		session = await self.get_session()
		return await self._get_current_page(session)

	async def _create_context(self, browser: PlaywrightBrowser):
		"""Creates a new browser context with anti-detection measures and loads cookies if available."""
		if self.browser.config.cdp_url and len(browser.contexts) > 0 and not self.config.force_new_context:
			context = browser.contexts[0]
			# For existing contexts, we need to set the viewport size manually
			if context.pages and not self.browser.config.headless:
				for page in context.pages:
					await self._set_viewport_size_for_page(page)
		elif self.browser.config.browser_binary_path and len(browser.contexts) > 0 and not self.config.force_new_context:
			# Connect to existing Chrome instance instead of creating new one
			context = browser.contexts[0]
			# For existing contexts, we need to set the viewport size manually
			if context.pages and not self.browser.config.headless:
				for page in context.pages:
					await self._set_viewport_size_for_page(page)
		else:
			kwargs = {}
			# Set viewport for both headless and non-headless modes
			if self.browser.config.headless:
				kwargs['viewport'] = self.config.browser_window_size.model_dump()
				kwargs['no_viewport'] = False
			else:
				# In headful mode, respect user setting for no_viewport if provided, otherwise default to True
				kwargs['viewport'] = self.config.browser_window_size.model_dump()
				kwargs['no_viewport'] = self.config.no_viewport if self.config.no_viewport is not None else True

			if self.config.user_agent is not None:
				kwargs['user_agent'] = self.config.user_agent

			context = await browser.new_context(
				**kwargs,
				java_script_enabled=True,
				**({'bypass_csp': True, 'ignore_https_errors': True} if self.config.disable_security else {}),
				record_video_dir=self.config.save_recording_path,
				record_video_size=self.config.browser_window_size.model_dump(),
				record_har_path=self.config.save_har_path,
				locale=self.config.locale,
				http_credentials=self.config.http_credentials,
				is_mobile=self.config.is_mobile,
				has_touch=self.config.has_touch,
				geolocation=self.config.geolocation,
				permissions=self.config.permissions,
				timezone_id=self.config.timezone_id,
			)

		if self.config.trace_path:
			await context.tracing.start(screenshots=True, snapshots=True, sources=True)

		# Resize the window for non-headless mode
		if not self.browser.config.headless:
			await self._resize_window(context)

		# Load cookies if they exist
		if self.config.cookies_file and os.path.exists(self.config.cookies_file):
			async with await anyio.open_file(self.config.cookies_file, 'r') as f:
				try:
					cookies = json.loads(await f.read())

					valid_same_site_values = ['Strict', 'Lax', 'None']
					for cookie in cookies:
						if 'sameSite' in cookie:
							if cookie['sameSite'] not in valid_same_site_values:
								logger.warning(
									f"Fixed invalid sameSite value '{cookie['sameSite']}' to 'None' for cookie {cookie.get('name')}"
								)
								cookie['sameSite'] = 'None'
					logger.info(f'🍪  Loaded {len(cookies)} cookies from {self.config.cookies_file}')
					await context.add_cookies(cookies)

				except json.JSONDecodeError as e:
					logger.error(f'Failed to parse cookies file: {str(e)}')

		# Expose anti-detection scripts
		await context.add_init_script(
			"""
			// Permissions
			const originalQuery = window.navigator.permissions.query;
			window.navigator.permissions.query = (parameters) => (
				parameters.name === 'notifications' ?
					Promise.resolve({ state: Notification.permission }) :
					originalQuery(parameters)
			);

			"""
		)

		return context

	async def _set_viewport_size_for_page(self, page: Page) -> None:
		"""Helper method to set viewport size for a page"""
		try:
			await page.set_viewport_size(self.config.browser_window_size.model_dump())
		except Exception as e:
			logger.debug(f'Failed to set viewport size for page: {e}')

	async def _wait_for_stable_network(self):
		page = await self.get_current_page()

		pending_requests = set()
		last_activity = asyncio.get_event_loop().time()

		# Define relevant resource types and content types
		RELEVANT_RESOURCE_TYPES = {
			'document',
			'stylesheet',
			'image',
			'font',
			'script',
			'iframe',
		}

		RELEVANT_CONTENT_TYPES = {
			'text/html',
			'text/css',
			'application/javascript',
			'image/',
			'font/',
			'application/json',
		}

		# Additional patterns to filter out
		IGNORED_URL_PATTERNS = {
			# Analytics and tracking
			'analytics',
			'tracking',
			'telemetry',
			'beacon',
			'metrics',
			# Ad-related
			'doubleclick',
			'adsystem',
			'adserver',
			'advertising',
			# Social media widgets
			'facebook.com/plugins',
			'platform.twitter',
			'linkedin.com/embed',
			# Live chat and support
			'livechat',
			'zendesk',
			'intercom',
			'crisp.chat',
			'hotjar',
			# Push notifications
			'push-notifications',
			'onesignal',
			'pushwoosh',
			# Background sync/heartbeat
			'heartbeat',
			'ping',
			'alive',
			# WebRTC and streaming
			'webrtc',
			'rtmp://',
			'wss://',
			# Common CDNs for dynamic content
			'cloudfront.net',
			'fastly.net',
		}

		async def on_request(request):
			# Filter by resource type
			if request.resource_type not in RELEVANT_RESOURCE_TYPES:
				return

			# Filter out streaming, websocket, and other real-time requests
			if request.resource_type in {
				'websocket',
				'media',
				'eventsource',
				'manifest',
				'other',
			}:
				return

			# Filter out by URL patterns
			url = request.url.lower()
			if any(pattern in url for pattern in IGNORED_URL_PATTERNS):
				return

			# Filter out data URLs and blob URLs
			if url.startswith(('data:', 'blob:')):
				return

			# Filter out requests with certain headers
			headers = request.headers
			if headers.get('purpose') == 'prefetch' or headers.get('sec-fetch-dest') in [
				'video',
				'audio',
			]:
				return

			nonlocal last_activity
			pending_requests.add(request)
			last_activity = asyncio.get_event_loop().time()
			# logger.debug(f'Request started: {request.url} ({request.resource_type})')

		async def on_response(response):
			request = response.request
			if request not in pending_requests:
				return

			# Filter by content type if available
			content_type = response.headers.get('content-type', '').lower()

			# Skip if content type indicates streaming or real-time data
			if any(
				t in content_type
				for t in [
					'streaming',
					'video',
					'audio',
					'webm',
					'mp4',
					'event-stream',
					'websocket',
					'protobuf',
				]
			):
				pending_requests.remove(request)
				return

			# Only process relevant content types
			if not any(ct in content_type for ct in RELEVANT_CONTENT_TYPES):
				pending_requests.remove(request)
				return

			# Skip if response is too large (likely not essential for page load)
			content_length = response.headers.get('content-length')
			if content_length and int(content_length) > 5 * 1024 * 1024:  # 5MB
				pending_requests.remove(request)
				return

			nonlocal last_activity
			pending_requests.remove(request)
			last_activity = asyncio.get_event_loop().time()
			# logger.debug(f'Request resolved: {request.url} ({content_type})')

		# Attach event listeners
		page.on('request', on_request)
		page.on('response', on_response)

		try:
			# Wait for idle time
			start_time = asyncio.get_event_loop().time()
			while True:
				await asyncio.sleep(0.1)
				now = asyncio.get_event_loop().time()
				if len(pending_requests) == 0 and (now - last_activity) >= self.config.wait_for_network_idle_page_load_time:
					break
				if now - start_time > self.config.maximum_wait_page_load_time:
					logger.debug(
						f'Network timeout after {self.config.maximum_wait_page_load_time}s with {len(pending_requests)} '
						f'pending requests: {[r.url for r in pending_requests]}'
					)
					break

		finally:
			# Clean up event listeners
			page.remove_listener('request', on_request)
			page.remove_listener('response', on_response)

		logger.debug(f'⚖️  Network stabilized for {self.config.wait_for_network_idle_page_load_time} seconds')

	async def _wait_for_page_and_frames_load(self, timeout_overwrite: float | None = None):
		"""
		Ensures page is fully loaded before continuing.
		Waits for either network to be idle or minimum WAIT_TIME, whichever is longer.
		Also checks if the loaded URL is allowed.
		"""
		# Start timing
		start_time = time.time()

		# Wait for page load
		try:
			await self._wait_for_stable_network()

			# Check if the loaded URL is allowed
			page = await self.get_current_page()
			await self._check_and_handle_navigation(page)
		except URLNotAllowedError as e:
			raise e
		except Exception:
			logger.warning('⚠️  Page load failed, continuing...')
			pass

		# Calculate remaining time to meet minimum WAIT_TIME
		elapsed = time.time() - start_time
		remaining = max((timeout_overwrite or self.config.minimum_wait_page_load_time) - elapsed, 0)

		logger.debug(f'--Page loaded in {elapsed:.2f} seconds, waiting for additional {remaining:.2f} seconds')

		# Sleep remaining time if needed
		if remaining > 0:
			await asyncio.sleep(remaining)

	def _is_url_allowed(self, url: str) -> bool:
		"""Check if a URL is allowed based on the whitelist configuration."""
		if not self.config.allowed_domains:
			return True

		try:
			from urllib.parse import urlparse

			parsed_url = urlparse(url)
			domain = parsed_url.netloc.lower()

			# Special case: Allow 'about:blank' explicitly
			if url == 'about:blank':
				return True

			# Remove port number if present
			if ':' in domain:
				domain = domain.split(':')[0]

			# Check if domain matches any allowed domain pattern
			return any(
				domain == allowed_domain.lower() or domain.endswith('.' + allowed_domain.lower())
				for allowed_domain in self.config.allowed_domains
			)
		except Exception as e:
			logger.error(f'⛔️  Error checking URL allowlist: {str(e)}')
			return False

	async def _check_and_handle_navigation(self, page: Page) -> None:
		"""Check if current page URL is allowed and handle if not."""
		if not self._is_url_allowed(page.url):
			logger.warning(f'⛔️  Navigation to non-allowed URL detected: {page.url}')
			try:
				await self.go_back()
			except Exception as e:
				logger.error(f'⛔️  Failed to go back after detecting non-allowed URL: {str(e)}')
			raise URLNotAllowedError(f'Navigation to non-allowed URL: {page.url}')

	async def navigate_to(self, url: str):
		"""Navigate to a URL"""
		if not self._is_url_allowed(url):
			raise BrowserError(f'Navigation to non-allowed URL: {url}')

		page = await self.get_current_page()
		await page.goto(url)
		await page.wait_for_load_state()

	async def refresh_page(self):
		"""Refresh the current page"""
		page = await self.get_current_page()
		await page.reload()
		await page.wait_for_load_state()

	async def go_back(self):
		"""Navigate back in history"""
		page = await self.get_current_page()
		try:
			# 10 ms timeout
			await page.go_back(timeout=10, wait_until='domcontentloaded')
			# await self._wait_for_page_and_frames_load(timeout_overwrite=1.0)
		except Exception as e:
			# Continue even if its not fully loaded, because we wait later for the page to load
			logger.debug(f'⏮️  Error during go_back: {e}')

	async def go_forward(self):
		"""Navigate forward in history"""
		page = await self.get_current_page()
		try:
			await page.go_forward(timeout=10, wait_until='domcontentloaded')
		except Exception as e:
			# Continue even if its not fully loaded, because we wait later for the page to load
			logger.debug(f'⏭️  Error during go_forward: {e}')

	async def close_current_tab(self):
		"""Close the current tab"""
		session = await self.get_session()
		page = await self._get_current_page(session)
		await page.close()
		self.active_tab = None
		# Switch to the first available tab if any exist
		if session.context.pages:
			await self.switch_to_tab(0)
			self.active_tab = session.context.pages[0]

		# otherwise the browser will be closed

	async def get_page_html(self) -> str:
		"""Get the current page HTML content"""
		page = await self.get_current_page()
		return await page.content()

	async def execute_javascript(self, script: str):
		"""Execute JavaScript code on the page"""
		page = await self.get_current_page()
		return await page.evaluate(script)

	async def get_page_structure(self) -> str:
		"""Get a debug view of the page structure including iframes"""
		debug_script = """(() => {
			function getPageStructure(element = document, depth = 0, maxDepth = 10) {
				if (depth >= maxDepth) return '';

				const indent = '  '.repeat(depth);
				let structure = '';

				// Skip certain elements that clutter the output
				const skipTags = new Set(['script', 'style', 'link', 'meta', 'noscript']);

				// Add current element info if it's not the document
				if (element !== document) {
					const tagName = element.tagName.toLowerCase();

					// Skip uninteresting elements
					if (skipTags.has(tagName)) return '';

					const id = element.id ? `#${element.id}` : '';
					const classes = element.className && typeof element.className === 'string' ?
						`.${element.className.split(' ').filter(c => c).join('.')}` : '';

					// Get additional useful attributes
					const attrs = [];
					if (element.getAttribute('role')) attrs.push(`role="${element.getAttribute('role')}"`);
					if (element.getAttribute('aria-label')) attrs.push(`aria-label="${element.getAttribute('aria-label')}"`);
					if (element.getAttribute('type')) attrs.push(`type="${element.getAttribute('type')}"`);
					if (element.getAttribute('name')) attrs.push(`name="${element.getAttribute('name')}"`);
					if (element.getAttribute('src')) {
						const src = element.getAttribute('src');
						attrs.push(`src="${src.substring(0, 50)}${src.length > 50 ? '...' : ''}"`);
					}

					// Add element info
					structure += `${indent}${tagName}${id}${classes}${attrs.length ? ' [' + attrs.join(', ') + ']' : ''}\\n`;

					// Handle iframes specially
					if (tagName === 'iframe') {
						try {
							const iframeDoc = element.contentDocument || element.contentWindow?.document;
							if (iframeDoc) {
								structure += `${indent}  [IFRAME CONTENT]:\\n`;
								structure += getPageStructure(iframeDoc, depth + 2, maxDepth);
							} else {
								structure += `${indent}  [IFRAME: No access - likely cross-origin]\\n`;
							}
						} catch (e) {
							structure += `${indent}  [IFRAME: Access denied - ${e.message}]\\n`;
						}
					}
				}

				// Get all child elements
				const children = element.children || element.childNodes;
				for (const child of children) {
					if (child.nodeType === 1) { // Element nodes only
						structure += getPageStructure(child, depth + 1, maxDepth);
					}
				}

				return structure;
			}

			return getPageStructure();
		})()"""

		page = await self.get_current_page()
		structure = await page.evaluate(debug_script)
		return structure

	@time_execution_sync('--get_state')  # This decorator might need to be updated to handle async
	async def get_state(self, cache_clickable_elements_hashes: bool) -> BrowserState:
		"""Get the current state of the browser

		cache_clickable_elements_hashes: bool
			If True, cache the clickable elements hashes for the current state. This is used to calculate which elements are new to the llm (from last message) -> reduces token usage.
		"""
		await self._wait_for_page_and_frames_load()
		session = await self.get_session()
		updated_state = await self._get_updated_state()

		# Find out which elements are new
		# Do this only if url has not changed
		if cache_clickable_elements_hashes:
			# if we are on the same url as the last state, we can use the cached hashes
			if (
				session.cached_state_clickable_elements_hashes
				and session.cached_state_clickable_elements_hashes.url == updated_state.url
			):
				# Pointers, feel free to edit in place
				updated_state_clickable_elements = ClickableElementProcessor.get_clickable_elements(updated_state.element_tree)

				for dom_element in updated_state_clickable_elements:
					dom_element.is_new = (
						ClickableElementProcessor.hash_dom_element(dom_element)
						not in session.cached_state_clickable_elements_hashes.hashes  # see which elements are new from the last state where we cached the hashes
					)
			# in any case, we need to cache the new hashes
			session.cached_state_clickable_elements_hashes = CachedStateClickableElementsHashes(
				url=updated_state.url,
				hashes=ClickableElementProcessor.get_clickable_elements_hashes(updated_state.element_tree),
			)

		session.cached_state = updated_state

		# Save cookies if a file is specified
		if self.config.cookies_file:
			asyncio.create_task(self.save_cookies())

		return session.cached_state

	async def _get_updated_state(self, focus_element: int = -1) -> BrowserState:
		"""Update and return state."""
		session = await self.get_session()

		# Check if current page is still valid, if not switch to another available page
		try:
			page = await self.get_current_page()
			# Test if page is still accessible
			await page.evaluate('1')
		except Exception as e:
			logger.debug(f'👋  Current page is no longer accessible: {str(e)}')
			# Get all available pages
			pages = session.context.pages
			if pages:
				self.state.target_id = None
				page = await self._get_current_page(session)
				logger.debug(f'🔄  Switched to page: {await page.title()}')
			else:
				raise BrowserError('Browser closed: no valid pages available')

		try:
			await self.remove_highlights()
			dom_service = DomService(page)
			content = await dom_service.get_clickable_elements(
				focus_element=focus_element,
				viewport_expansion=self.config.viewport_expansion,
				highlight_elements=self.config.highlight_elements,
			)

			tabs_info = await self.get_tabs_info()

			# Get all cross-origin iframes within the page and open them in new tabs
			# mark the titles of the new tabs so the LLM knows to check them for additional content
			# unfortunately too buggy for now, too many sites use invisible cross-origin iframes for ads, tracking, youtube videos, social media, etc.
			# and it distracts the bot by opening a lot of new tabs
			# iframe_urls = await dom_service.get_cross_origin_iframes()
			# for url in iframe_urls:
			# 	if url in [tab.url for tab in tabs_info]:
			# 		continue  # skip if the iframe if we already have it open in a tab
			# 	new_page_id = tabs_info[-1].page_id + 1
			# 	logger.debug(f'Opening cross-origin iframe in new tab #{new_page_id}: {url}')
			# 	await self.create_new_tab(url)
			# 	tabs_info.append(
			# 		TabInfo(
			# 			page_id=new_page_id,
			# 			url=url,
			# 			title=f'iFrame opened as new tab, treat as if embedded inside page #{self.state.target_id}: {page.url}',
			# 			parent_page_id=self.state.target_id,
			# 		)
			# 	)

			screenshot_b64 = await self.take_screenshot()
			pixels_above, pixels_below = await self.get_scroll_info(page)

			self.current_state = BrowserState(
				element_tree=content.element_tree,
				selector_map=content.selector_map,
				url=page.url,
				title=await page.title(),
				tabs=tabs_info,
				screenshot=screenshot_b64,
				pixels_above=pixels_above,
				pixels_below=pixels_below,
			)

			return self.current_state
		except Exception as e:
			logger.error(f'❌  Failed to update state: {str(e)}')
			# Return last known good state if available
			if hasattr(self, 'current_state'):
				return self.current_state
			raise

	# region - Browser Actions
	@time_execution_async('--take_screenshot')
	async def take_screenshot(self, full_page: bool = False) -> str:
		"""
		Returns a base64 encoded screenshot of the current page.
		"""
		page = await self.get_current_page()

		await page.bring_to_front()
		await page.wait_for_load_state()

		screenshot = await page.screenshot(
			full_page=full_page,
			animations='disabled',
		)

		screenshot_b64 = base64.b64encode(screenshot).decode('utf-8')

		# await self.remove_highlights()

		return screenshot_b64

	@time_execution_async('--remove_highlights')
	async def remove_highlights(self):
		"""
		Removes all highlight overlays and labels created by the highlightElement function.
		Handles cases where the page might be closed or inaccessible.
		"""
		try:
			page = await self.get_current_page()
			await page.evaluate(
				"""
                try {
                    // Remove the highlight container and all its contents
                    const container = document.getElementById('playwright-highlight-container');
                    if (container) {
                        container.remove();
                    }

                    // Remove highlight attributes from elements
                    const highlightedElements = document.querySelectorAll('[browser-user-highlight-id^="playwright-highlight-"]');
                    highlightedElements.forEach(el => {
                        el.removeAttribute('browser-user-highlight-id');
                    });
                } catch (e) {
                    console.error('Failed to remove highlights:', e);
                }
                """
			)
		except Exception as e:
			logger.debug(f'⚠  Failed to remove highlights (this is usually ok): {str(e)}')
			# Don't raise the error since this is not critical functionality
			pass

	# endregion

	# region - User Actions

	@classmethod
	def _convert_simple_xpath_to_css_selector(cls, xpath: str) -> str:
		"""Converts simple XPath expressions to CSS selectors."""
		if not xpath:
			return ''

		# Remove leading slash if present
		xpath = xpath.lstrip('/')

		# Split into parts
		parts = xpath.split('/')
		css_parts = []

		for part in parts:
			if not part:
				continue

			# Handle custom elements with colons by escaping them
			if ':' in part and '[' not in part:
				base_part = part.replace(':', r'\:')
				css_parts.append(base_part)
				continue

			# Handle index notation [n]
			if '[' in part:
				base_part = part[: part.find('[')]
				# Handle custom elements with colons in the base part
				if ':' in base_part:
					base_part = base_part.replace(':', r'\:')
				index_part = part[part.find('[') :]

				# Handle multiple indices
				indices = [i.strip('[]') for i in index_part.split(']')[:-1]]

				for idx in indices:
					try:
						# Handle numeric indices
						if idx.isdigit():
							index = int(idx) - 1
							base_part += f':nth-of-type({index + 1})'
						# Handle last() function
						elif idx == 'last()':
							base_part += ':last-of-type'
						# Handle position() functions
						elif 'position()' in idx:
							if '>1' in idx:
								base_part += ':nth-of-type(n+2)'
					except ValueError:
						continue

				css_parts.append(base_part)
			else:
				css_parts.append(part)

		base_selector = ' > '.join(css_parts)
		return base_selector

	@classmethod
	@time_execution_sync('--enhanced_css_selector_for_element')
	def _enhanced_css_selector_for_element(cls, element: DOMElementNode, include_dynamic_attributes: bool = True) -> str:
		"""
		Creates a CSS selector for a DOM element, handling various edge cases and special characters.

		Args:
		        element: The DOM element to create a selector for

		Returns:
		        A valid CSS selector string
		"""
		try:
			# Get base selector from XPath
			css_selector = cls._convert_simple_xpath_to_css_selector(element.xpath)

			# Handle class attributes
			if 'class' in element.attributes and element.attributes['class'] and include_dynamic_attributes:
				# Define a regex pattern for valid class names in CSS
				valid_class_name_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_-]*$')

				# Iterate through the class attribute values
				classes = element.attributes['class'].split()
				for class_name in classes:
					# Skip empty class names
					if not class_name.strip():
						continue

					# Check if the class name is valid
					if valid_class_name_pattern.match(class_name):
						# Append the valid class name to the CSS selector
						css_selector += f'.{class_name}'
					else:
						# Skip invalid class names
						continue

			# Expanded set of safe attributes that are stable and useful for selection
			SAFE_ATTRIBUTES = {
				# Data attributes (if they're stable in your application)
				'id',
				# Standard HTML attributes
				'name',
				'type',
				'placeholder',
				# Accessibility attributes
				'aria-label',
				'aria-labelledby',
				'aria-describedby',
				'role',
				# Common form attributes
				'for',
				'autocomplete',
				'required',
				'readonly',
				# Media attributes
				'alt',
				'title',
				'src',
				# Custom stable attributes (add any application-specific ones)
				'href',
				'target',
			}

			if include_dynamic_attributes:
				dynamic_attributes = {
					'data-id',
					'data-qa',
					'data-cy',
					'data-testid',
				}
				SAFE_ATTRIBUTES.update(dynamic_attributes)

			# Handle other attributes
			for attribute, value in element.attributes.items():
				if attribute == 'class':
					continue

				# Skip invalid attribute names
				if not attribute.strip():
					continue

				if attribute not in SAFE_ATTRIBUTES:
					continue

				# Escape special characters in attribute names
				safe_attribute = attribute.replace(':', r'\:')

				# Handle different value cases
				if value == '':
					css_selector += f'[{safe_attribute}]'
				elif any(char in value for char in '"\'<>`\n\r\t'):
					# Use contains for values with special characters
					# For newline-containing text, only use the part before the newline
					if '\n' in value:
						value = value.split('\n')[0]
					# Regex-substitute *any* whitespace with a single space, then strip.
					collapsed_value = re.sub(r'\s+', ' ', value).strip()
					# Escape embedded double-quotes.
					safe_value = collapsed_value.replace('"', '\\"')
					css_selector += f'[{safe_attribute}*="{safe_value}"]'
				else:
					css_selector += f'[{safe_attribute}="{value}"]'

			return css_selector

		except Exception:
			# Fallback to a more basic selector if something goes wrong
			tag_name = element.tag_name or '*'
			return f"{tag_name}[highlight_index='{element.highlight_index}']"

	@time_execution_async('--get_locate_element')
	async def get_locate_element(self, element: DOMElementNode) -> Optional[ElementHandle]:
		current_frame = await self.get_current_page()

		# Start with the target element and collect all parents
		parents: list[DOMElementNode] = []
		current = element
		while current.parent is not None:
			parent = current.parent
			parents.append(parent)
			current = parent

		# Reverse the parents list to process from top to bottom
		parents.reverse()

		# Process all iframe parents in sequence
		iframes = [item for item in parents if item.tag_name == 'iframe']
		for parent in iframes:
			css_selector = self._enhanced_css_selector_for_element(
				parent,
				include_dynamic_attributes=self.config.include_dynamic_attributes,
			)
			current_frame = current_frame.frame_locator(css_selector)

		css_selector = self._enhanced_css_selector_for_element(
			element, include_dynamic_attributes=self.config.include_dynamic_attributes
		)

		try:
			if isinstance(current_frame, FrameLocator):
				element_handle = await current_frame.locator(css_selector).element_handle()
				return element_handle
			else:
				# Try to scroll into view if hidden
				element_handle = await current_frame.query_selector(css_selector)
				if element_handle:
					is_hidden = await element_handle.is_hidden()
					if not is_hidden:
						await element_handle.scroll_into_view_if_needed()
					return element_handle
				return None
		except Exception as e:
			logger.error(f'❌  Failed to locate element: {str(e)}')
			return None

	@time_execution_async('--get_locate_element_by_xpath')
	async def get_locate_element_by_xpath(self, xpath: str) -> Optional[ElementHandle]:
		"""
		Locates an element on the page using the provided XPath.
		"""
		current_frame = await self.get_current_page()

		try:
			# Use XPath to locate the element
			element_handle = await current_frame.query_selector(f'xpath={xpath}')
			if element_handle:
				is_hidden = await element_handle.is_hidden()
				if not is_hidden:
					await element_handle.scroll_into_view_if_needed()
				return element_handle
			return None
		except Exception as e:
			logger.error(f'❌  Failed to locate element by XPath {xpath}: {str(e)}')
			return None

	@time_execution_async('--get_locate_element_by_css_selector')
	async def get_locate_element_by_css_selector(self, css_selector: str) -> Optional[ElementHandle]:
		"""
		Locates an element on the page using the provided CSS selector.
		"""
		current_frame = await self.get_current_page()

		try:
			# Use CSS selector to locate the element
			element_handle = await current_frame.query_selector(css_selector)
			if element_handle:
				is_hidden = await element_handle.is_hidden()
				if not is_hidden:
					await element_handle.scroll_into_view_if_needed()
				return element_handle
			return None
		except Exception as e:
			logger.error(f'❌  Failed to locate element by CSS selector {css_selector}: {str(e)}')
			return None

	@time_execution_async('--get_locate_element_by_text')
	async def get_locate_element_by_text(
		self, text: str, nth: Optional[int] = 0, element_type: Optional[str] = None
	) -> Optional[ElementHandle]:
		"""
		Locates an element on the page using the provided text.
		If `nth` is provided, it returns the nth matching element (0-based).
		If `element_type` is provided, filters by tag name (e.g., 'button', 'span').
		"""
		current_frame = await self.get_current_page()
		try:
			# handle also specific element type or use any type.
			selector = f'{element_type or "*"}:text("{text}")'
			elements = await current_frame.query_selector_all(selector)
			# considering only visible elements
			elements = [el for el in elements if await el.is_visible()]

			if not elements:
				logger.error(f"No visible element with text '{text}' found.")
				return None

			if nth is not None:
				if 0 <= nth < len(elements):
					element_handle = elements[nth]
				else:
					logger.error(f"Visible element with text '{text}' not found at index {nth}.")
					return None
			else:
				element_handle = elements[0]

			is_hidden = await element_handle.is_hidden()
			if not is_hidden:
				await element_handle.scroll_into_view_if_needed()
			return element_handle
		except Exception as e:
			logger.error(f"❌  Failed to locate element by text '{text}': {str(e)}")
			return None

	@time_execution_async('--input_text_element_node')
	async def _input_text_element_node(self, element_node: DOMElementNode, text: str):
		"""
		Input text into an element with proper error handling and state management.
		Handles different types of input fields and ensures proper element state before input.
		"""
		try:
			# Highlight before typing
			# if element_node.highlight_index is not None:
			# 	await self._update_state(focus_element=element_node.highlight_index)

			element_handle = await self.get_locate_element(element_node)

			if element_handle is None:
				raise BrowserError(f'Element: {repr(element_node)} not found')

			# Ensure element is ready for input
			try:
				await element_handle.wait_for_element_state('stable', timeout=1000)
				is_hidden = await element_handle.is_hidden()
				if not is_hidden:
					await element_handle.scroll_into_view_if_needed(timeout=1000)
			except Exception:
				pass

			# Get element properties to determine input method
			tag_handle = await element_handle.get_property('tagName')
			tag_name = (await tag_handle.json_value()).lower()
			is_contenteditable = await element_handle.get_property('isContentEditable')
			readonly_handle = await element_handle.get_property('readOnly')
			disabled_handle = await element_handle.get_property('disabled')

			readonly = await readonly_handle.json_value() if readonly_handle else False
			disabled = await disabled_handle.json_value() if disabled_handle else False

			if (await is_contenteditable.json_value() or tag_name == 'input') and not (readonly or disabled):
				await element_handle.evaluate('el => {el.textContent = ""; el.value = "";}')
				await element_handle.type(text, delay=5)
			else:
				await element_handle.fill(text)

		except Exception as e:
			logger.debug(f'❌  Failed to input text into element: {repr(element_node)}. Error: {str(e)}')
			raise BrowserError(f'Failed to input text into index {element_node.highlight_index}')

	@time_execution_async('--click_element_node')
	async def _click_element_node(self, element_node: DOMElementNode) -> Optional[str]:
		"""
		Optimized method to click an element using xpath.
		"""
		page = await self.get_current_page()

		try:
			# Highlight before clicking
			# if element_node.highlight_index is not None:
			# 	await self._update_state(focus_element=element_node.highlight_index)

			element_handle = await self.get_locate_element(element_node)

			if element_handle is None:
				raise Exception(f'Element: {repr(element_node)} not found')

			async def perform_click(click_func):
				"""Performs the actual click, handling both download
				and navigation scenarios."""
				if self.config.save_downloads_path:
					try:
						# Try short-timeout expect_download to detect a file download has been been triggered
						async with page.expect_download(timeout=5000) as download_info:
							await click_func()
						download = await download_info.value
						# Determine file path
						suggested_filename = download.suggested_filename
						unique_filename = await self._get_unique_filename(self.config.save_downloads_path, suggested_filename)
						download_path = os.path.join(self.config.save_downloads_path, unique_filename)
						await download.save_as(download_path)
						logger.debug(f'⬇️  Download triggered. Saved file to: {download_path}')
						return download_path
					except TimeoutError:
						# If no download is triggered, treat as normal click
						logger.debug('No download triggered within timeout. Checking navigation...')
						await page.wait_for_load_state()
						await self._check_and_handle_navigation(page)
				else:
					# Standard click logic if no download is expected
					await click_func()
					await page.wait_for_load_state()
					await self._check_and_handle_navigation(page)

			try:
				return await perform_click(lambda: element_handle.click(timeout=1500))
			except URLNotAllowedError as e:
				raise e
			except Exception:
				try:
					return await perform_click(lambda: page.evaluate('(el) => el.click()', element_handle))
				except URLNotAllowedError as e:
					raise e
				except Exception as e:
					raise Exception(f'Failed to click element: {str(e)}')

		except URLNotAllowedError as e:
			raise e
		except Exception as e:
			raise Exception(f'Failed to click element: {repr(element_node)}. Error: {str(e)}')

	@time_execution_async('--get_tabs_info')
	async def get_tabs_info(self) -> list[TabInfo]:
		"""Get information about all tabs"""
		session = await self.get_session()

		tabs_info = []
		for page_id, page in enumerate(session.context.pages):
			try:
				tab_info = TabInfo(page_id=page_id, url=page.url, title=await asyncio.wait_for(page.title(), timeout=1))
			except asyncio.TimeoutError:
				# page.title() can hang forever on tabs that are crashed/disappeared/about:blank
				# we dont want to try automating those tabs because they will hang the whole script
				logger.debug('⚠  Failed to get tab info for tab #%s: %s (ignoring)', page_id, page.url)
				tab_info = TabInfo(page_id=page_id, url='about:blank', title='ignore this tab and do not use it')
			tabs_info.append(tab_info)

		return tabs_info

	@time_execution_async('--switch_to_tab')
	async def switch_to_tab(self, page_id: int) -> None:
		"""Switch to a specific tab by its page_id"""
		session = await self.get_session()
		pages = session.context.pages

		if page_id >= len(pages):
			raise BrowserError(f'No tab found with page_id: {page_id}')

		page = pages[page_id]

		# Check if the tab's URL is allowed before switching
		if not self._is_url_allowed(page.url):
			raise BrowserError(f'Cannot switch to tab with non-allowed URL: {page.url}')

		# Update target ID if using CDP
		if self.browser.config.cdp_url:
			targets = await self._get_cdp_targets()
			for target in targets:
				if target['url'] == page.url:
					self.state.target_id = target['targetId']
					break

		self.active_tab = page
		await page.bring_to_front()
		await page.wait_for_load_state()

		# Set the viewport size for the tab
		try:
			await page.set_viewport_size(self.config.browser_window_size.model_dump())
			logger.debug(f'Set viewport size to {self.config.browser_window_size.width}x{self.config.browser_window_size.height}')
		except Exception as e:
			logger.debug(f'Failed to set viewport size: {e}')

	@time_execution_async('--create_new_tab')
	async def create_new_tab(self, url: str | None = None) -> None:
		"""Create a new tab and optionally navigate to a URL"""
		if url and not self._is_url_allowed(url):
			raise BrowserError(f'Cannot create new tab with non-allowed URL: {url}')

		session = await self.get_session()
		new_page = await session.context.new_page()

		self.active_tab = new_page

		await new_page.wait_for_load_state()

		# Set the viewport size for the new tab
		try:
			await new_page.set_viewport_size(self.config.browser_window_size.model_dump())
			logger.debug(f'Set viewport size to {self.config.browser_window_size.width}x{self.config.browser_window_size.height}')
		except Exception as e:
			logger.debug(f'Failed to set viewport size: {e}')

		if url:
			await new_page.goto(url)
			await self._wait_for_page_and_frames_load(timeout_overwrite=1)

		# Get target ID for new page if using CDP
		if self.browser.config.cdp_url:
			targets = await self._get_cdp_targets()
			for target in targets:
				if target['url'] == new_page.url:
					self.state.target_id = target['targetId']
					break

	# endregion

	# region - Helper methods for easier access to the DOM
	async def _get_current_page(self, session: BrowserSession) -> Page:
		pages = session.context.pages

		# Try to find page by target ID if using CDP
		if self.browser.config.cdp_url and self.state.target_id:
			targets = await self._get_cdp_targets()
			for target in targets:
				if target['targetId'] == self.state.target_id:
					for page in pages:
						if page.url == target['url']:
							return page

		if self.active_tab and self.active_tab in session.context.pages and not self.active_tab.is_closed():
			return self.active_tab

		# fall back to most recently opened non-extension page (extensions are almost always invisible background targets)
		non_extension_pages = [
			page for page in pages if not page.url.startswith('chrome-extension://') and not page.url.startswith('chrome://')
		]
		if non_extension_pages:
			return non_extension_pages[-1]

		# Fallback to opening a new tab in the active window
		try:
			return await session.context.new_page()
		except Exception:
			# there is no browser window available (perhaps the user closed it?)
			# reopen a new window in the browser and try again
			logger.warning('⚠️  No browser window available, opening a new window')
			await self._initialize_session()
			page = await session.context.new_page()
			self.active_tab = page
			return page

	async def get_selector_map(self) -> SelectorMap:
		session = await self.get_session()
		if session.cached_state is None:
			return {}
		return session.cached_state.selector_map

	async def get_element_by_index(self, index: int) -> ElementHandle | None:
		selector_map = await self.get_selector_map()
		element_handle = await self.get_locate_element(selector_map[index])
		return element_handle

	async def get_dom_element_by_index(self, index: int) -> DOMElementNode:
		selector_map = await self.get_selector_map()
		return selector_map[index]

	async def save_cookies(self):
		"""Save current cookies to file"""
		if self.session and self.session.context and self.config.cookies_file:
			try:
				cookies = await self.session.context.cookies()
				logger.debug(f'🍪  Saving {len(cookies)} cookies to {self.config.cookies_file}')

				# Check if the path is a directory and create it if necessary
				dirname = os.path.dirname(self.config.cookies_file)
				if dirname:
					os.makedirs(dirname, exist_ok=True)

				async with await anyio.open_file(self.config.cookies_file, 'w') as f:
					await f.write(json.dumps(cookies))
			except Exception as e:
				logger.warning(f'❌  Failed to save cookies: {str(e)}')

	async def is_file_uploader(self, element_node: DOMElementNode, max_depth: int = 3, current_depth: int = 0) -> bool:
		"""Check if element or its children are file uploaders"""
		if current_depth > max_depth:
			return False

		# Check current element
		is_uploader = False

		if not isinstance(element_node, DOMElementNode):
			return False

		# Check for file input attributes
		if element_node.tag_name == 'input':
			is_uploader = element_node.attributes.get('type') == 'file' or element_node.attributes.get('accept') is not None

		if is_uploader:
			return True

		# Recursively check children
		if element_node.children and current_depth < max_depth:
			for child in element_node.children:
				if isinstance(child, DOMElementNode):
					if await self.is_file_uploader(child, max_depth, current_depth + 1):
						return True

		return False

	async def get_scroll_info(self, page: Page) -> tuple[int, int]:
		"""Get scroll position information for the current page."""
		scroll_y = await page.evaluate('window.scrollY')
		viewport_height = await page.evaluate('window.innerHeight')
		total_height = await page.evaluate('document.documentElement.scrollHeight')
		pixels_above = scroll_y
		pixels_below = total_height - (scroll_y + viewport_height)
		return pixels_above, pixels_below

	async def reset_context(self):
		"""Reset the browser session
		Call this when you don't want to kill the context but just kill the state
		"""
		# close all tabs and clear cached state
		session = await self.get_session()

		pages = session.context.pages
		for page in pages:
			await page.close()

		self.active_tab = None
		session.cached_state = None
		self.state.target_id = None

	async def _get_unique_filename(self, directory, filename):
		"""Generate a unique filename by appending (1), (2), etc., if a file already exists."""
		base, ext = os.path.splitext(filename)
		counter = 1
		new_filename = filename
		while os.path.exists(os.path.join(directory, new_filename)):
			new_filename = f'{base} ({counter}){ext}'
			counter += 1
		return new_filename

	async def _get_cdp_targets(self) -> list[dict]:
		"""Get all CDP targets directly using CDP protocol"""
		if not self.browser.config.cdp_url or not self.session:
			return []

		try:
			pages = self.session.context.pages
			if not pages:
				return []

			cdp_session = await pages[0].context.new_cdp_session(pages[0])
			result = await cdp_session.send('Target.getTargets')
			await cdp_session.detach()
			return result.get('targetInfos', [])
		except Exception as e:
			logger.debug(f'Failed to get CDP targets: {e}')
			return []

	async def _resize_window(self, context: PlaywrightBrowserContext) -> None:
		"""Resize the browser window to match the configured size"""
		try:
			if not context.pages:
				return

			page = context.pages[0]
			window_size = self.config.browser_window_size.model_dump()

			# First, set the viewport size
			try:
				await page.set_viewport_size(window_size)
				logger.debug(f'Set viewport size to {window_size["width"]}x{window_size["height"]}')
			except Exception as e:
				logger.debug(f'Viewport resize failed: {e}')

			# Then, try to set the actual window size using CDP
			try:
				cdp_session = await context.new_cdp_session(page)

				# Get the window ID
				window_id_result = await cdp_session.send('Browser.getWindowForTarget')

				# Set the window bounds
				await cdp_session.send(
					'Browser.setWindowBounds',
					{
						'windowId': window_id_result['windowId'],
						'bounds': {
							'width': window_size['width'],
							'height': window_size['height'] + BROWSER_NAVBAR_HEIGHT,  # Add height for browser chrome
							'windowState': 'normal',  # Ensure window is not minimized/maximized
						},
					},
				)

				await cdp_session.detach()
				logger.debug(f'Set window size to {window_size["width"]}x{window_size["height"] + BROWSER_NAVBAR_HEIGHT}')
			except Exception as e:
				logger.debug(f'CDP window resize failed: {e}')

				# Fallback to using JavaScript
				try:
					await page.evaluate(
						"""
						(width, height) => {
							window.resizeTo(width, height);
						}
						""",
						window_size['width'],
						window_size['height'] + BROWSER_NAVBAR_HEIGHT,
					)
					logger.debug(
						f'Used JavaScript to set window size to {window_size["width"]}x{window_size["height"] + BROWSER_NAVBAR_HEIGHT}'
					)
				except Exception as e:
					logger.debug(f'JavaScript window resize failed: {e}')

			logger.debug(f'Attempted to resize window to {window_size["width"]}x{window_size["height"]}')
		except Exception as e:
			logger.debug(f'Failed to resize browser window: {e}')
			# Non-critical error, continue execution

	async def wait_for_element(self, selector: str, timeout: float) -> None:
		"""
		Waits for an element matching the given CSS selector to become visible.

		Args:
		    selector (str): The CSS selector of the element.
		    timeout (float): The maximum time to wait for the element to be visible (in milliseconds).

		Raises:
		    TimeoutError: If the element does not become visible within the specified timeout.
		"""
		page = await self.get_current_page()
		await page.wait_for_selector(selector, state='visible', timeout=timeout)
````

## File: browser_use/agent/memory/service.py
````python
from __future__ import annotations

import logging
import os
from typing import List, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
	BaseMessage,
	HumanMessage,
)
from langchain_core.messages.utils import convert_to_openai_messages

from browser_use.agent.memory.views import MemoryConfig
from browser_use.agent.message_manager.service import MessageManager
from browser_use.agent.message_manager.views import ManagedMessage, MessageMetadata
from browser_use.utils import time_execution_sync

logger = logging.getLogger(__name__)


class Memory:
	"""
	Manages procedural memory for agents.

	This class implements a procedural memory management system using Mem0 that transforms agent interaction history
	into concise, structured representations at specified intervals. It serves to optimize context window
	utilization during extended task execution by converting verbose historical information into compact,
	yet comprehensive memory constructs that preserve essential operational knowledge.
	"""

	def __init__(
		self,
		message_manager: MessageManager,
		llm: BaseChatModel,
		config: MemoryConfig | None = None,
	):
		self.message_manager = message_manager
		self.llm = llm

		# Initialize configuration with defaults based on the LLM if not provided
		if config is None:
			self.config = MemoryConfig(llm_instance=llm, agent_id=f'agent_{id(self)}')

			# Set appropriate embedder based on LLM type
			llm_class = llm.__class__.__name__
			if llm_class == 'ChatOpenAI':
				self.config.embedder_provider = 'openai'
				self.config.embedder_model = 'text-embedding-3-small'
				self.config.embedder_dims = 1536
			elif llm_class == 'ChatGoogleGenerativeAI':
				self.config.embedder_provider = 'gemini'
				self.config.embedder_model = 'models/text-embedding-004'
				self.config.embedder_dims = 768
			elif llm_class == 'ChatOllama':
				self.config.embedder_provider = 'ollama'
				self.config.embedder_model = 'nomic-embed-text'
				self.config.embedder_dims = 512
		else:
			# Ensure LLM instance is set in the config
			self.config = MemoryConfig(config)  # re-validate user-provided config
			self.config.llm_instance = llm

		# Check for required packages
		try:
			# also disable mem0's telemetry when ANONYMIZED_TELEMETRY=False
			if os.getenv('ANONYMIZED_TELEMETRY', 'true').lower()[0] in 'fn0':
				os.environ['MEM0_TELEMETRY'] = 'False'
			from mem0 import Memory as Mem0Memory
		except ImportError:
			raise ImportError('mem0 is required when enable_memory=True. Please install it with `pip install mem0`.')

		if self.config.embedder_provider == 'huggingface':
			try:
				# check that required package is installed if huggingface is used
				from sentence_transformers import SentenceTransformer  # noqa: F401
			except ImportError:
				raise ImportError(
					'sentence_transformers is required when enable_memory=True and embedder_provider="huggingface". Please install it with `pip install sentence-transformers`.'
				)

		# Initialize Mem0 with the configuration
		self.mem0 = Mem0Memory.from_config(config_dict=self.config.full_config_dict)

	@time_execution_sync('--create_procedural_memory')
	def create_procedural_memory(self, current_step: int) -> None:
		"""
		Create a procedural memory if needed based on the current step.

		Args:
		    current_step: The current step number of the agent
		"""
		logger.info(f'Creating procedural memory at step {current_step}')

		# Get all messages
		all_messages = self.message_manager.state.history.messages

		# Separate messages into those to keep as-is and those to process for memory
		new_messages = []
		messages_to_process = []

		for msg in all_messages:
			if isinstance(msg, ManagedMessage) and msg.metadata.message_type in {'init', 'memory'}:
				# Keep system and memory messages as they are
				new_messages.append(msg)
			else:
				if len(msg.message.content) > 0:
					messages_to_process.append(msg)

		# Need at least 2 messages to create a meaningful summary
		if len(messages_to_process) <= 1:
			logger.info('Not enough non-memory messages to summarize')
			return
		# Create a procedural memory
		memory_content = self._create([m.message for m in messages_to_process], current_step)

		if not memory_content:
			logger.warning('Failed to create procedural memory')
			return

		# Replace the processed messages with the consolidated memory
		memory_message = HumanMessage(content=memory_content)
		memory_tokens = self.message_manager._count_tokens(memory_message)
		memory_metadata = MessageMetadata(tokens=memory_tokens, message_type='memory')

		# Calculate the total tokens being removed
		removed_tokens = sum(m.metadata.tokens for m in messages_to_process)

		# Add the memory message
		new_messages.append(ManagedMessage(message=memory_message, metadata=memory_metadata))

		# Update the history
		self.message_manager.state.history.messages = new_messages
		self.message_manager.state.history.current_tokens -= removed_tokens
		self.message_manager.state.history.current_tokens += memory_tokens
		logger.info(f'Messages consolidated: {len(messages_to_process)} messages converted to procedural memory')

	def _create(self, messages: List[BaseMessage], current_step: int) -> Optional[str]:
		parsed_messages = convert_to_openai_messages(messages)
		try:
			results = self.mem0.add(
				messages=parsed_messages,
				agent_id=self.config.agent_id,
				memory_type='procedural_memory',
				metadata={'step': current_step},
			)
			if len(results.get('results', [])):
				return results.get('results', [])[0].get('memory')
			return None
		except Exception as e:
			logger.error(f'Error creating procedural memory: {e}')
			return None
````

## File: .github/workflows/test.yaml
````yaml
name: test

on:
  push:
    branches:
      - main
      - stable
      - 'releases/**'
    tags:
      - '*'
  pull_request:
  workflow_dispatch:
    
jobs:
  tests:
    name: ${{matrix.test}} 
    runs-on: ubuntu-latest
    strategy:
      matrix:
        test:
        - browser/patchright
        - browser/user_binary
        - browser/remote_cdp
        - models/openai
        - models/google
        - models/anthropic
        - models/azure
        - models/deepseek
        - models/grok
        - functionality/click
        - functionality/tabs
        - functionality/input
        - functionality/scroll
        - functionality/upload
        - functionality/download
        - functionality/save
        - functionality/vision
        - functionality/memory
        - functionality/planner
        - functionality/hooks
        
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv run --with=dotenv pytest tests/${{ matrix.test }}.py || true
````

## File: browser_use/browser/browser.py
````python
"""
Playwright browser on steroids.
"""

import asyncio
import gc
import logging
import os
import socket
import subprocess
from typing import Literal

import httpx
import psutil
from dotenv import load_dotenv
from patchright.async_api import Browser as PlaywrightBrowser
from patchright.async_api import Playwright, async_playwright
from pydantic import AliasChoices, BaseModel, ConfigDict, Field

load_dotenv()

from browser_use.browser.chrome import (
	CHROME_ARGS,
	CHROME_DEBUG_PORT,
	CHROME_DETERMINISTIC_RENDERING_ARGS,
	CHROME_DISABLE_SECURITY_ARGS,
	CHROME_DOCKER_ARGS,
	CHROME_HEADLESS_ARGS,
)
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from browser_use.browser.utils.screen_resolution import get_screen_resolution, get_window_adjustments
from browser_use.utils import time_execution_async

logger = logging.getLogger(__name__)

IN_DOCKER = os.environ.get('IN_DOCKER', 'false').lower()[0] in 'ty1'


class ProxySettings(BaseModel):
	"""the same as playwright.sync_api.ProxySettings, but now as a Pydantic BaseModel so pydantic can validate it"""

	server: str
	bypass: str | None = None
	username: str | None = None
	password: str | None = None

	model_config = ConfigDict(populate_by_name=True, from_attributes=True)

	# Support dict-like behavior for compatibility with Playwright's ProxySettings
	def __getitem__(self, key):
		return getattr(self, key)

	def get(self, key, default=None):
		return getattr(self, key, default)


class BrowserConfig(BaseModel):
	r"""
	Configuration for the Browser.

	Default values:
		headless: False
			Whether to run browser in headless mode (not recommended)

		disable_security: False
			Disable browser security features (required for cross-origin iframe support)

		extra_browser_args: []
			Extra arguments to pass to the browser

		wss_url: None
			Connect to a browser instance via WebSocket

		cdp_url: None
			Connect to a browser instance via CDP

		browser_binary_path: None
			Path to a Browser instance to use to connect to your normal browser
			e.g. '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'

		chrome_remote_debugging_port: 9222
			Chrome remote debugging port to use to when browser_binary_path is supplied.
			This allows running multiple chrome browsers with same browser_binary_path but running on different ports.
			Also, makes it possible to launch new user provided chrome browser without closing already opened chrome instances,
			by providing non-default chrome debugging port.

		keep_alive: False
			Keep the browser alive after the agent has finished running

		deterministic_rendering: False
			Enable deterministic rendering (makes GPU/font rendering consistent across different OS's and docker)
	"""

	model_config = ConfigDict(
		arbitrary_types_allowed=True,
		extra='ignore',
		populate_by_name=True,
		from_attributes=True,
		validate_assignment=True,
		revalidate_instances='subclass-instances',
	)

	wss_url: str | None = None
	cdp_url: str | None = None

	browser_class: Literal['chromium', 'firefox', 'webkit'] = 'chromium'
	browser_binary_path: str | None = Field(
		default=None, validation_alias=AliasChoices('browser_instance_path', 'chrome_instance_path')
	)
	chrome_remote_debugging_port: int | None = CHROME_DEBUG_PORT
	extra_browser_args: list[str] = Field(default_factory=list)

	headless: bool = False
	disable_security: bool = False  # disable_security=True is dangerous as any malicious URL visited could embed an iframe for the user's bank, and use their cookies to steal money
	deterministic_rendering: bool = False
	keep_alive: bool = Field(default=False, alias='_force_keep_browser_alive')  # used to be called _force_keep_browser_alive

	proxy: ProxySettings | None = None
	new_context_config: BrowserContextConfig = Field(default_factory=BrowserContextConfig)


# @singleton: TODO - think about id singleton makes sense here
# @dev By default this is a singleton, but you can create multiple instances if you need to.
class Browser:
	"""
	Playwright browser on steroids.

	This is persistent browser factory that can spawn multiple browser contexts.
	It is recommended to use only one instance of Browser per your application (RAM usage will grow otherwise).
	"""

	def __init__(
		self,
		config: BrowserConfig | None = None,
	):
		logger.debug('🌎  Initializing new browser')
		self.config = config or BrowserConfig()
		self.playwright: Playwright | None = None
		self.playwright_browser: PlaywrightBrowser | None = None

	async def new_context(self, config: BrowserContextConfig | None = None) -> BrowserContext:
		"""Create a browser context"""
		browser_config = self.config.model_dump() if self.config else {}
		context_config = config.model_dump() if config else {}
		merged_config = {**browser_config, **context_config}
		return BrowserContext(config=BrowserContextConfig(**merged_config), browser=self)

	async def get_playwright_browser(self) -> PlaywrightBrowser:
		"""Get a browser context"""
		if self.playwright_browser is None:
			return await self._init()

		return self.playwright_browser

	@time_execution_async('--init (browser)')
	async def _init(self):
		"""Initialize the browser session"""
		playwright = await async_playwright().start()
		self.playwright = playwright

		browser = await self._setup_browser(playwright)
		self.playwright_browser = browser

		return self.playwright_browser

	async def _setup_remote_cdp_browser(self, playwright: Playwright) -> PlaywrightBrowser:
		"""Sets up and returns a Playwright Browser instance with anti-detection measures. Firefox has no longer CDP support."""
		if 'firefox' in (self.config.browser_binary_path or '').lower():
			raise ValueError(
				'CDP has been deprecated for firefox, check: https://fxdx.dev/deprecating-cdp-support-in-firefox-embracing-the-future-with-webdriver-bidi/'
			)
		if not self.config.cdp_url:
			raise ValueError('CDP URL is required')
		logger.info(f'🔌  Connecting to remote browser via CDP {self.config.cdp_url}')
		browser_class = getattr(playwright, self.config.browser_class)
		browser = await browser_class.connect_over_cdp(self.config.cdp_url)
		return browser

	async def _setup_remote_wss_browser(self, playwright: Playwright) -> PlaywrightBrowser:
		"""Sets up and returns a Playwright Browser instance with anti-detection measures."""
		if not self.config.wss_url:
			raise ValueError('WSS URL is required')
		logger.info(f'🔌  Connecting to remote browser via WSS {self.config.wss_url}')
		browser_class = getattr(playwright, self.config.browser_class)
		browser = await browser_class.connect(self.config.wss_url)
		return browser

	async def _setup_user_provided_browser(self, playwright: Playwright) -> PlaywrightBrowser:
		"""Sets up and returns a Playwright Browser instance with anti-detection measures."""
		if not self.config.browser_binary_path:
			raise ValueError('A browser_binary_path is required')

		assert self.config.browser_class == 'chromium', (
			'browser_binary_path only supports chromium browsers (make sure browser_class=chromium)'
		)

		try:
			# Check if browser is already running
			async with httpx.AsyncClient() as client:
				response = await client.get(
					f'http://localhost:{self.config.chrome_remote_debugging_port}/json/version', timeout=2
				)
				if response.status_code == 200:
					logger.info(
						f'🔌  Reusing existing browser found running on http://localhost:{self.config.chrome_remote_debugging_port}'
					)
					browser_class = getattr(playwright, self.config.browser_class)
					browser = await browser_class.connect_over_cdp(
						endpoint_url=f'http://localhost:{self.config.chrome_remote_debugging_port}',
						timeout=20000,  # 20 second timeout for connection
					)
					return browser
		except httpx.RequestError:
			logger.debug('🌎  No existing Chrome instance found, starting a new one')

		# Start a new Chrome instance
		chrome_launch_args = [
			*{  # remove duplicates (usually preserves the order, but not guaranteed)
				f'--remote-debugging-port={self.config.chrome_remote_debugging_port}',
				*CHROME_ARGS,
				*(CHROME_DOCKER_ARGS if IN_DOCKER else []),
				*(CHROME_HEADLESS_ARGS if self.config.headless else []),
				*(CHROME_DISABLE_SECURITY_ARGS if self.config.disable_security else []),
				*(CHROME_DETERMINISTIC_RENDERING_ARGS if self.config.deterministic_rendering else []),
				*self.config.extra_browser_args,
			},
		]
		chrome_sub_process = await asyncio.create_subprocess_exec(
			self.config.browser_binary_path,
			*chrome_launch_args,
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
			shell=False,
		)
		self._chrome_subprocess = psutil.Process(chrome_sub_process.pid)

		# Attempt to connect again after starting a new instance
		for _ in range(10):
			try:
				async with httpx.AsyncClient() as client:
					response = await client.get(
						f'http://localhost:{self.config.chrome_remote_debugging_port}/json/version', timeout=2
					)
					if response.status_code == 200:
						break
			except httpx.RequestError:
				pass
			await asyncio.sleep(1)

		# Attempt to connect again after starting a new instance
		try:
			browser_class = getattr(playwright, self.config.browser_class)
			browser = await browser_class.connect_over_cdp(
				endpoint_url=f'http://localhost:{self.config.chrome_remote_debugging_port}',
				timeout=20000,  # 20 second timeout for connection
			)
			return browser
		except Exception as e:
			logger.error(f'❌  Failed to start a new Chrome instance: {str(e)}')
			raise RuntimeError(
				'To start chrome in Debug mode, you need to close all existing Chrome instances and try again otherwise we can not connect to the instance.'
			)

	async def _setup_builtin_browser(self, playwright: Playwright) -> PlaywrightBrowser:
		"""Sets up and returns a Playwright Browser instance with anti-detection measures."""
		assert self.config.browser_binary_path is None, 'browser_binary_path should be None if trying to use the builtin browsers'

		# Use the configured window size from new_context_config if available
		if (
			not self.config.headless
			and hasattr(self.config, 'new_context_config')
			and hasattr(self.config.new_context_config, 'browser_window_size')
		):
			screen_size = self.config.new_context_config.browser_window_size.model_dump()
			offset_x, offset_y = get_window_adjustments()
		elif self.config.headless:
			screen_size = {'width': 1920, 'height': 1080}
			offset_x, offset_y = 0, 0
		else:
			screen_size = get_screen_resolution()
			offset_x, offset_y = get_window_adjustments()

		chrome_args = {
			f'--remote-debugging-port={self.config.chrome_remote_debugging_port}',
			*CHROME_ARGS,
			*(CHROME_DOCKER_ARGS if IN_DOCKER else []),
			*(CHROME_HEADLESS_ARGS if self.config.headless else []),
			*(CHROME_DISABLE_SECURITY_ARGS if self.config.disable_security else []),
			*(CHROME_DETERMINISTIC_RENDERING_ARGS if self.config.deterministic_rendering else []),
			f'--window-position={offset_x},{offset_y}',
			f'--window-size={screen_size["width"]},{screen_size["height"]}',
			*self.config.extra_browser_args,
		}

		# check if chrome remote debugging port is already taken,
		# if so remove the remote-debugging-port arg to prevent conflicts
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			if s.connect_ex(('localhost', self.config.chrome_remote_debugging_port)) == 0:
				chrome_args.remove(f'--remote-debugging-port={self.config.chrome_remote_debugging_port}')

		browser_class = getattr(playwright, self.config.browser_class)
		args = {
			'chromium': list(chrome_args),
			'firefox': [
				*{
					'-no-remote',
					*self.config.extra_browser_args,
				}
			],
			'webkit': [
				*{
					'--no-startup-window',
					*self.config.extra_browser_args,
				}
			],
		}

		browser = await browser_class.launch(
			headless=self.config.headless,
			channel='chrome',
			args=args[self.config.browser_class],
			proxy=self.config.proxy.model_dump() if self.config.proxy else None,
			handle_sigterm=False,
			handle_sigint=False,
		)
		return browser

	async def _setup_browser(self, playwright: Playwright) -> PlaywrightBrowser:
		"""Sets up and returns a Playwright Browser instance with anti-detection measures."""
		try:
			if self.config.cdp_url:
				return await self._setup_remote_cdp_browser(playwright)
			if self.config.wss_url:
				return await self._setup_remote_wss_browser(playwright)

			if self.config.headless:
				logger.warning('⚠️ Headless mode is not recommended. Many sites will detect and block all headless browsers.')

			if self.config.browser_binary_path:
				return await self._setup_user_provided_browser(playwright)
			else:
				return await self._setup_builtin_browser(playwright)
		except Exception as e:
			logger.error(f'Failed to initialize Playwright browser: {e}')
			raise

	async def close(self):
		"""Close the browser instance"""
		if self.config.keep_alive:
			return

		try:
			if self.playwright_browser:
				await self.playwright_browser.close()
				del self.playwright_browser
			if self.playwright:
				await self.playwright.stop()
				del self.playwright
			if chrome_proc := getattr(self, '_chrome_subprocess', None):
				try:
					# always kill all children processes, otherwise chrome leaves a bunch of zombie processes
					for proc in chrome_proc.children(recursive=True):
						proc.kill()
					chrome_proc.kill()
				except Exception as e:
					logger.debug(f'Failed to terminate chrome subprocess: {e}')

			# Then cleanup httpx clients
			await self.cleanup_httpx_clients()
		except Exception as e:
			if 'OpenAI error' not in str(e):
				logger.debug(f'Failed to close browser properly: {e}')

		finally:
			self.playwright_browser = None
			self.playwright = None
			self._chrome_subprocess = None
			gc.collect()

	def __del__(self):
		"""Async cleanup when object is destroyed"""
		try:
			if self.playwright_browser or self.playwright:
				loop = asyncio.get_running_loop()
				if loop.is_running():
					loop.create_task(self.close())
				else:
					asyncio.run(self.close())
		except Exception as e:
			logger.debug(f'Failed to cleanup browser in destructor: {e}')

	async def cleanup_httpx_clients(self):
		"""Cleanup all httpx clients"""
		import gc

		import httpx

		# Force garbage collection to make sure all clients are in memory
		gc.collect()

		# Get all httpx clients
		clients = [obj for obj in gc.get_objects() if isinstance(obj, httpx.AsyncClient)]

		# Close all clients
		for client in clients:
			if not client.is_closed:
				try:
					await client.aclose()
				except Exception as e:
					logger.debug(f'Error closing httpx client: {e}')
````

## File: .github/workflows/lint.yml
````yaml
name: lint
on:
  push:
    branches:
      - main
      - stable
      - 'releases/**'
    tags:
      - '*'
  pull_request:
  workflow_dispatch:

jobs:
  lint-syntax:
    name: syntax-errors
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv run ruff check --no-fix --select PLE

  lint-style:
    name: code-style
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv run pre-commit run --all-files

  lint-typecheck:
    name: type-checker
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv run pyright
````

## File: browser_use/agent/gif.py
````python
from __future__ import annotations

import base64
import io
import logging
import os
import platform
from typing import TYPE_CHECKING, Optional

from browser_use.agent.views import AgentHistoryList

if TYPE_CHECKING:
	from PIL import Image, ImageFont

logger = logging.getLogger(__name__)


def decode_unicode_escapes_to_utf8(text: str) -> str:
	"""Handle decoding any unicode escape sequences embedded in a string (needed to render non-ASCII languages like chinese or arabic in the GIF overlay text)"""

	if r'\u' not in text:
		# doesn't have any escape sequences that need to be decoded
		return text

	try:
		# Try to decode Unicode escape sequences
		return text.encode('latin1').decode('unicode_escape')
	except (UnicodeEncodeError, UnicodeDecodeError):
		# logger.debug(f"Failed to decode unicode escape sequences while generating gif text: {text}")
		return text


def create_history_gif(
	task: str,
	history: AgentHistoryList,
	#
	output_path: str = 'agent_history.gif',
	duration: int = 3000,
	show_goals: bool = True,
	show_task: bool = True,
	show_logo: bool = False,
	font_size: int = 40,
	title_font_size: int = 56,
	goal_font_size: int = 44,
	margin: int = 40,
	line_spacing: float = 1.5,
) -> None:
	"""Create a GIF from the agent's history with overlaid task and goal text."""
	if not history.history:
		logger.warning('No history to create GIF from')
		return

	from PIL import Image, ImageFont

	images = []

	# if history is empty or first screenshot is None, we can't create a gif
	if not history.history or not history.history[0].state.screenshot:
		logger.warning('No history or first screenshot to create GIF from')
		return

	# Try to load nicer fonts
	try:
		# Try different font options in order of preference
		# ArialUni is a font that comes with Office and can render most non-alphabet characters
		font_options = [
			'Microsoft YaHei',  # 微软雅黑
			'SimHei',  # 黑体
			'SimSun',  # 宋体
			'Noto Sans CJK SC',  # 思源黑体
			'WenQuanYi Micro Hei',  # 文泉驿微米黑
			'Helvetica',
			'Arial',
			'DejaVuSans',
			'Verdana',
		]
		font_loaded = False

		for font_name in font_options:
			try:
				if platform.system() == 'Windows':
					# Need to specify the abs font path on Windows
					font_name = os.path.join(os.getenv('WIN_FONT_DIR', 'C:\\Windows\\Fonts'), font_name + '.ttf')
				regular_font = ImageFont.truetype(font_name, font_size)
				title_font = ImageFont.truetype(font_name, title_font_size)
				goal_font = ImageFont.truetype(font_name, goal_font_size)
				font_loaded = True
				break
			except OSError:
				continue

		if not font_loaded:
			raise OSError('No preferred fonts found')

	except OSError:
		regular_font = ImageFont.load_default()
		title_font = ImageFont.load_default()

		goal_font = regular_font

	# Load logo if requested
	logo = None
	if show_logo:
		try:
			logo = Image.open('./static/browser-use.png')
			# Resize logo to be small (e.g., 40px height)
			logo_height = 150
			aspect_ratio = logo.width / logo.height
			logo_width = int(logo_height * aspect_ratio)
			logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
		except Exception as e:
			logger.warning(f'Could not load logo: {e}')

	# Create task frame if requested
	if show_task and task:
		task_frame = _create_task_frame(
			task,
			history.history[0].state.screenshot,
			title_font,  # type: ignore
			regular_font,  # type: ignore
			logo,
			line_spacing,
		)
		images.append(task_frame)

	# Process each history item
	for i, item in enumerate(history.history, 1):
		if not item.state.screenshot:
			continue

		# Convert base64 screenshot to PIL Image
		img_data = base64.b64decode(item.state.screenshot)
		image = Image.open(io.BytesIO(img_data))

		if show_goals and item.model_output:
			image = _add_overlay_to_image(
				image=image,
				step_number=i,
				goal_text=item.model_output.current_state.next_goal,
				regular_font=regular_font,  # type: ignore
				title_font=title_font,  # type: ignore
				margin=margin,
				logo=logo,
			)

		images.append(image)

	if images:
		# Save the GIF
		images[0].save(
			output_path,
			save_all=True,
			append_images=images[1:],
			duration=duration,
			loop=0,
			optimize=False,
		)
		logger.info(f'Created GIF at {output_path}')
	else:
		logger.warning('No images found in history to create GIF')


def _create_task_frame(
	task: str,
	first_screenshot: str,
	title_font: 'ImageFont.FreeTypeFont',
	regular_font: 'ImageFont.FreeTypeFont',
	logo: Optional[Image.Image] = None,
	line_spacing: float = 1.5,
) -> 'Image.Image':
	"""Create initial frame showing the task."""
	from PIL import Image, ImageDraw, ImageFont

	img_data = base64.b64decode(first_screenshot)
	template = Image.open(io.BytesIO(img_data))
	image = Image.new('RGB', template.size, (0, 0, 0))
	draw = ImageDraw.Draw(image)

	# Calculate vertical center of image
	center_y = image.height // 2

	# Draw task text with dynamic font size based on task length
	margin = 140  # Increased margin
	max_width = image.width - (2 * margin)

	# Dynamic font size calculation based on task length
	# Start with base font size (regular + 16)
	base_font_size = regular_font.size + 16
	min_font_size = max(regular_font.size - 10, 16)  # Don't go below 16pt
	max_font_size = base_font_size  # Cap at the base font size

	# Calculate dynamic font size based on text length and complexity
	# Longer texts get progressively smaller fonts
	text_length = len(task)
	if text_length > 200:
		# For very long text, reduce font size logarithmically
		font_size = max(base_font_size - int(10 * (text_length / 200)), min_font_size)
	else:
		font_size = base_font_size

	larger_font = ImageFont.truetype(regular_font.path, font_size)

	# Generate wrapped text with the calculated font size
	wrapped_text = _wrap_text(task, larger_font, max_width)

	# Calculate line height with spacing
	line_height = larger_font.size * line_spacing

	# Split text into lines and draw with custom spacing
	lines = wrapped_text.split('\n')
	total_height = line_height * len(lines)

	# Start position for first line
	text_y = center_y - (total_height / 2) + 50  # Shifted down slightly

	for line in lines:
		# Get line width for centering
		line_bbox = draw.textbbox((0, 0), line, font=larger_font)
		text_x = (image.width - (line_bbox[2] - line_bbox[0])) // 2

		draw.text(
			(text_x, text_y),
			line,
			font=larger_font,
			fill=(255, 255, 255),
		)
		text_y += line_height

	# Add logo if provided (top right corner)
	if logo:
		logo_margin = 20
		logo_x = image.width - logo.width - logo_margin
		image.paste(logo, (logo_x, logo_margin), logo if logo.mode == 'RGBA' else None)

	return image


def _add_overlay_to_image(
	image: 'Image.Image',
	step_number: int,
	goal_text: str,
	regular_font: 'ImageFont.FreeTypeFont',
	title_font: 'ImageFont.FreeTypeFont',
	margin: int,
	logo: Optional['Image.Image'] = None,
	display_step: bool = True,
	text_color: tuple[int, int, int, int] = (255, 255, 255, 255),
	text_box_color: tuple[int, int, int, int] = (0, 0, 0, 255),
) -> 'Image.Image':
	"""Add step number and goal overlay to an image."""

	from PIL import Image, ImageDraw

	goal_text = decode_unicode_escapes_to_utf8(goal_text)
	image = image.convert('RGBA')
	txt_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
	draw = ImageDraw.Draw(txt_layer)
	if display_step:
		# Add step number (bottom left)
		step_text = str(step_number)
		step_bbox = draw.textbbox((0, 0), step_text, font=title_font)
		step_width = step_bbox[2] - step_bbox[0]
		step_height = step_bbox[3] - step_bbox[1]

		# Position step number in bottom left
		x_step = margin + 10  # Slight additional offset from edge
		y_step = image.height - margin - step_height - 10  # Slight offset from bottom

		# Draw rounded rectangle background for step number
		padding = 20  # Increased padding
		step_bg_bbox = (
			x_step - padding,
			y_step - padding,
			x_step + step_width + padding,
			y_step + step_height + padding,
		)
		draw.rounded_rectangle(
			step_bg_bbox,
			radius=15,  # Add rounded corners
			fill=text_box_color,
		)

		# Draw step number
		draw.text(
			(x_step, y_step),
			step_text,
			font=title_font,
			fill=text_color,
		)

	# Draw goal text (centered, bottom)
	max_width = image.width - (4 * margin)
	wrapped_goal = _wrap_text(goal_text, title_font, max_width)
	goal_bbox = draw.multiline_textbbox((0, 0), wrapped_goal, font=title_font)
	goal_width = goal_bbox[2] - goal_bbox[0]
	goal_height = goal_bbox[3] - goal_bbox[1]

	# Center goal text horizontally, place above step number
	x_goal = (image.width - goal_width) // 2
	y_goal = y_step - goal_height - padding * 4  # More space between step and goal

	# Draw rounded rectangle background for goal
	padding_goal = 25  # Increased padding for goal
	goal_bg_bbox = (
		x_goal - padding_goal,  # Remove extra space for logo
		y_goal - padding_goal,
		x_goal + goal_width + padding_goal,
		y_goal + goal_height + padding_goal,
	)
	draw.rounded_rectangle(
		goal_bg_bbox,
		radius=15,  # Add rounded corners
		fill=text_box_color,
	)

	# Draw goal text
	draw.multiline_text(
		(x_goal, y_goal),
		wrapped_goal,
		font=title_font,
		fill=text_color,
		align='center',
	)

	# Add logo if provided (top right corner)
	if logo:
		logo_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
		logo_margin = 20
		logo_x = image.width - logo.width - logo_margin
		logo_layer.paste(logo, (logo_x, logo_margin), logo if logo.mode == 'RGBA' else None)
		txt_layer = Image.alpha_composite(logo_layer, txt_layer)

	# Composite and convert
	result = Image.alpha_composite(image, txt_layer)
	return result.convert('RGB')


def _wrap_text(text: str, font: 'ImageFont.FreeTypeFont', max_width: int) -> str:
	"""
	Wrap text to fit within a given width.

	Args:
	    text: Text to wrap
	    font: Font to use for text
	    max_width: Maximum width in pixels

	Returns:
	    Wrapped text with newlines
	"""
	text = decode_unicode_escapes_to_utf8(text)
	words = text.split()
	lines = []
	current_line = []

	for word in words:
		current_line.append(word)
		line = ' '.join(current_line)
		bbox = font.getbbox(line)
		if bbox[2] > max_width:
			if len(current_line) == 1:
				lines.append(current_line.pop())
			else:
				current_line.pop()
				lines.append(' '.join(current_line))
				current_line = [word]

	if current_line:
		lines.append(' '.join(current_line))

	return '\n'.join(lines)
````

## File: browser_use/agent/service.py
````python
import asyncio
import gc
import inspect
import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, Generic, List, Optional, TypeVar, Union

from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
	BaseMessage,
	HumanMessage,
	SystemMessage,
)

# from lmnr.sdk.decorators import observe
from pydantic import BaseModel, ValidationError

from browser_use.agent.gif import create_history_gif
from browser_use.agent.memory.service import Memory
from browser_use.agent.memory.views import MemoryConfig
from browser_use.agent.message_manager.service import MessageManager, MessageManagerSettings
from browser_use.agent.message_manager.utils import (
	convert_input_messages,
	extract_json_from_model_output,
	is_model_without_tool_support,
	save_conversation,
)
from browser_use.agent.prompts import AgentMessagePrompt, PlannerPrompt, SystemPrompt
from browser_use.agent.views import (
	REQUIRED_LLM_API_ENV_VARS,
	ActionResult,
	AgentError,
	AgentHistory,
	AgentHistoryList,
	AgentOutput,
	AgentSettings,
	AgentState,
	AgentStepInfo,
	StepMetadata,
	ToolCallingMethod,
)
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContext
from browser_use.browser.views import BrowserState, BrowserStateHistory
from browser_use.controller.registry.views import ActionModel
from browser_use.controller.service import Controller
from browser_use.dom.history_tree_processor.service import (
	DOMHistoryElement,
	HistoryTreeProcessor,
)
from browser_use.exceptions import LLMException
from browser_use.telemetry.service import ProductTelemetry
from browser_use.telemetry.views import (
	AgentEndTelemetryEvent,
	AgentRunTelemetryEvent,
	AgentStepTelemetryEvent,
)
from browser_use.utils import check_env_variables, time_execution_async, time_execution_sync

load_dotenv()
logger = logging.getLogger(__name__)

SKIP_LLM_API_KEY_VERIFICATION = os.environ.get('SKIP_LLM_API_KEY_VERIFICATION', 'false').lower()[0] in 'ty1'


def log_response(response: AgentOutput) -> None:
	"""Utility function to log the model's response."""

	if 'Success' in response.current_state.evaluation_previous_goal:
		emoji = '👍'
	elif 'Failed' in response.current_state.evaluation_previous_goal:
		emoji = '⚠'
	else:
		emoji = '🤷'

	logger.info(f'{emoji} Eval: {response.current_state.evaluation_previous_goal}')
	logger.info(f'🧠 Memory: {response.current_state.memory}')
	logger.info(f'🎯 Next goal: {response.current_state.next_goal}')
	for i, action in enumerate(response.action):
		logger.info(f'🛠️  Action {i + 1}/{len(response.action)}: {action.model_dump_json(exclude_unset=True)}')


Context = TypeVar('Context')

AgentHookFunc = Callable[['Agent'], Awaitable[None]]


class Agent(Generic[Context]):
	@time_execution_sync('--init (agent)')
	def __init__(
		self,
		task: str,
		llm: BaseChatModel,
		# Optional parameters
		browser: Browser | None = None,
		browser_context: BrowserContext | None = None,
		controller: Controller[Context] = Controller(),
		# Initial agent run parameters
		sensitive_data: Optional[Dict[str, str]] = None,
		initial_actions: Optional[List[Dict[str, Dict[str, Any]]]] = None,
		# Cloud Callbacks
		register_new_step_callback: Union[
			Callable[['BrowserState', 'AgentOutput', int], None],  # Sync callback
			Callable[['BrowserState', 'AgentOutput', int], Awaitable[None]],  # Async callback
			None,
		] = None,
		register_done_callback: Union[
			Callable[['AgentHistoryList'], Awaitable[None]],  # Async Callback
			Callable[['AgentHistoryList'], None],  # Sync Callback
			None,
		] = None,
		register_external_agent_status_raise_error_callback: Callable[[], Awaitable[bool]] | None = None,
		# Agent settings
		use_vision: bool = True,
		use_vision_for_planner: bool = False,
		save_conversation_path: Optional[str] = None,
		save_conversation_path_encoding: Optional[str] = 'utf-8',
		max_failures: int = 3,
		retry_delay: int = 10,
		override_system_message: Optional[str] = None,
		extend_system_message: Optional[str] = None,
		max_input_tokens: int = 128000,
		validate_output: bool = False,
		message_context: Optional[str] = None,
		generate_gif: bool | str = False,
		available_file_paths: Optional[list[str]] = None,
		include_attributes: list[str] = [
			'title',
			'type',
			'name',
			'role',
			'aria-label',
			'placeholder',
			'value',
			'alt',
			'aria-expanded',
			'data-date-format',
		],
		max_actions_per_step: int = 10,
		tool_calling_method: Optional[ToolCallingMethod] = 'auto',
		page_extraction_llm: Optional[BaseChatModel] = None,
		planner_llm: Optional[BaseChatModel] = None,
		planner_interval: int = 1,  # Run planner every N steps
		is_planner_reasoning: bool = False,
		extend_planner_system_message: Optional[str] = None,
		injected_agent_state: Optional[AgentState] = None,
		context: Context | None = None,
		save_playwright_script_path: Optional[str] = None,
		enable_memory: bool = True,
		memory_config: Optional[MemoryConfig] = None,
		source: Optional[str] = None,
	):
		if page_extraction_llm is None:
			page_extraction_llm = llm

		# Core components
		self.task = task
		self.llm = llm
		self.controller = controller
		self.sensitive_data = sensitive_data

		self.settings = AgentSettings(
			use_vision=use_vision,
			use_vision_for_planner=use_vision_for_planner,
			save_conversation_path=save_conversation_path,
			save_conversation_path_encoding=save_conversation_path_encoding,
			max_failures=max_failures,
			retry_delay=retry_delay,
			override_system_message=override_system_message,
			extend_system_message=extend_system_message,
			max_input_tokens=max_input_tokens,
			validate_output=validate_output,
			message_context=message_context,
			generate_gif=generate_gif,
			available_file_paths=available_file_paths,
			include_attributes=include_attributes,
			max_actions_per_step=max_actions_per_step,
			tool_calling_method=tool_calling_method,
			page_extraction_llm=page_extraction_llm,
			planner_llm=planner_llm,
			planner_interval=planner_interval,
			is_planner_reasoning=is_planner_reasoning,
			save_playwright_script_path=save_playwright_script_path,
			extend_planner_system_message=extend_planner_system_message,
		)

		# Memory settings
		self.enable_memory = enable_memory
		self.memory_config = memory_config

		# Initialize state
		self.state = injected_agent_state or AgentState()

		# Action setup
		self._setup_action_models()
		self._set_browser_use_version_and_source(source)
		self.initial_actions = self._convert_initial_actions(initial_actions) if initial_actions else None

		# Model setup
		self._set_model_names()
		self.tool_calling_method = self._set_tool_calling_method()

		# Handle users trying to use use_vision=True with DeepSeek models
		if 'deepseek' in self.model_name.lower():
			logger.warning('⚠️ DeepSeek models do not support use_vision=True yet. Setting use_vision=False for now...')
			self.settings.use_vision = False
		if 'deepseek' in (self.planner_model_name or '').lower():
			logger.warning(
				'⚠️ DeepSeek models do not support use_vision=True yet. Setting use_vision_for_planner=False for now...'
			)
			self.settings.use_vision_for_planner = False
		# Handle users trying to use use_vision=True with XAI models
		if 'grok' in self.model_name.lower():
			logger.warning('⚠️ XAI models do not support use_vision=True yet. Setting use_vision=False for now...')
			self.settings.use_vision = False
		if 'grok' in (self.planner_model_name or '').lower():
			logger.warning('⚠️ XAI models do not support use_vision=True yet. Setting use_vision_for_planner=False for now...')
			self.settings.use_vision_for_planner = False

		logger.info(
			f'🧠 Starting an agent with main_model={self.model_name}'
			f'{" +tools" if self.tool_calling_method == "function_calling" else ""}'
			f'{" +rawtools" if self.tool_calling_method == "raw" else ""}'
			f'{" +vision" if self.settings.use_vision else ""}'
			f'{" +memory" if self.enable_memory else ""}, '
			f'planner_model={self.planner_model_name}'
			f'{" +reasoning" if self.settings.is_planner_reasoning else ""}'
			f'{" +vision" if self.settings.use_vision_for_planner else ""}, '
			f'extraction_model={getattr(self.settings.page_extraction_llm, "model_name", None)} '
		)

		# Verify we can connect to the LLM
		self._verify_llm_connection()

		# Initialize available actions for system prompt (only non-filtered actions)
		# These will be used for the system prompt to maintain caching
		self.unfiltered_actions = self.controller.registry.get_prompt_description()

		self.settings.message_context = self._set_message_context()

		# Initialize message manager with state
		# Initial system prompt with all actions - will be updated during each step
		self._message_manager = MessageManager(
			task=task,
			system_message=SystemPrompt(
				action_description=self.unfiltered_actions,
				max_actions_per_step=self.settings.max_actions_per_step,
				override_system_message=override_system_message,
				extend_system_message=extend_system_message,
			).get_system_message(),
			settings=MessageManagerSettings(
				max_input_tokens=self.settings.max_input_tokens,
				include_attributes=self.settings.include_attributes,
				message_context=self.settings.message_context,
				sensitive_data=sensitive_data,
				available_file_paths=self.settings.available_file_paths,
			),
			state=self.state.message_manager_state,
		)

		print('state POOP:', self.state)

		if self.enable_memory:
			try:
				# Initialize memory
				self.memory = Memory(
					message_manager=self._message_manager,
					llm=self.llm,
					config=self.memory_config,
				)
			except ImportError:
				logger.warning(
					'⚠️ Agent(enable_memory=True) is set but missing some required packages, install and re-run to use memory features: pip install browser-use[memory]'
				)
				self.memory = None
				self.enable_memory = False
		else:
			self.memory = None

		# Browser setup
		self.injected_browser = browser is not None
		self.injected_browser_context = browser_context is not None
		self.browser = browser or Browser()
		self.browser.config.new_context_config.disable_security = self.browser.config.disable_security
		self.browser_context = browser_context or BrowserContext(
			browser=self.browser, config=self.browser.config.new_context_config
		)

		# Callbacks
		self.register_new_step_callback = register_new_step_callback
		self.register_done_callback = register_done_callback
		self.register_external_agent_status_raise_error_callback = register_external_agent_status_raise_error_callback

		# Context
		self.context = context

		# Telemetry
		self.telemetry = ProductTelemetry()

		if self.settings.save_conversation_path:
			logger.info(f'Saving conversation to {self.settings.save_conversation_path}')

	def _set_message_context(self) -> str | None:
		if self.tool_calling_method == 'raw':
			# For raw tool calling, only include actions with no filters initially
			if self.settings.message_context:
				self.settings.message_context += f'\n\nAvailable actions: {self.unfiltered_actions}'
			else:
				self.settings.message_context = f'Available actions: {self.unfiltered_actions}'
		return self.settings.message_context

	def _set_browser_use_version_and_source(self, source_override: Optional[str] = None) -> None:
		"""Get the version and source of the browser-use package (git or pip in a nutshell)"""
		try:
			# First check for repository-specific files
			repo_files = ['.git', 'README.md', 'docs', 'examples']
			package_root = Path(__file__).parent.parent.parent

			# If all of these files/dirs exist, it's likely from git
			if all(Path(package_root / file).exists() for file in repo_files):
				try:
					import subprocess

					version = subprocess.check_output(['git', 'describe', '--tags']).decode('utf-8').strip()
				except Exception:
					version = 'unknown'
				source = 'git'
			else:
				# If no repo files found, try getting version from pip
				from importlib.metadata import version

				version = version('browser-use')
				source = 'pip'
		except Exception:
			version = 'unknown'
			source = 'unknown'
		if source_override is not None:
			source = source_override
		logger.debug(f'Version: {version}, Source: {source}')
		self.version = version
		self.source = source

	def _set_model_names(self) -> None:
		self.chat_model_library = self.llm.__class__.__name__
		self.model_name = 'Unknown'
		if hasattr(self.llm, 'model_name'):
			model = self.llm.model_name  # type: ignore
			self.model_name = model if model is not None else 'Unknown'
		elif hasattr(self.llm, 'model'):
			model = self.llm.model  # type: ignore
			self.model_name = model if model is not None else 'Unknown'

		if self.settings.planner_llm:
			if hasattr(self.settings.planner_llm, 'model_name'):
				self.planner_model_name = self.settings.planner_llm.model_name  # type: ignore
			elif hasattr(self.settings.planner_llm, 'model'):
				self.planner_model_name = self.settings.planner_llm.model  # type: ignore
			else:
				self.planner_model_name = 'Unknown'
		else:
			self.planner_model_name = None

	def _setup_action_models(self) -> None:
		"""Setup dynamic action models from controller's registry"""
		# Initially only include actions with no filters
		self.ActionModel = self.controller.registry.create_action_model()
		# Create output model with the dynamic actions
		self.AgentOutput = AgentOutput.type_with_custom_actions(self.ActionModel)

		# used to force the done action when max_steps is reached
		self.DoneActionModel = self.controller.registry.create_action_model(include_actions=['done'])
		self.DoneAgentOutput = AgentOutput.type_with_custom_actions(self.DoneActionModel)

	def _set_tool_calling_method(self) -> Optional[ToolCallingMethod]:
		tool_calling_method = self.settings.tool_calling_method
		if tool_calling_method == 'auto':
			if is_model_without_tool_support(self.model_name):
				return 'raw'
			elif self.chat_model_library == 'ChatGoogleGenerativeAI':
				return None
			elif self.chat_model_library == 'ChatOpenAI':
				return 'function_calling'
			elif self.chat_model_library == 'AzureChatOpenAI':
				return 'function_calling'
			else:
				return None
		else:
			return tool_calling_method

	def add_new_task(self, new_task: str) -> None:
		self._message_manager.add_new_task(new_task)

	async def _raise_if_stopped_or_paused(self) -> None:
		"""Utility function that raises an InterruptedError if the agent is stopped or paused."""

		if self.register_external_agent_status_raise_error_callback:
			if await self.register_external_agent_status_raise_error_callback():
				raise InterruptedError

		if self.state.stopped or self.state.paused:
			# logger.debug('Agent paused after getting state')
			raise InterruptedError

	# @observe(name='agent.step', ignore_output=True, ignore_input=True)
	@time_execution_async('--step (agent)')
	async def step(self, step_info: Optional[AgentStepInfo] = None) -> None:
		"""Execute one step of the task"""
		logger.info(f'📍 Step {self.state.n_steps}')
		state = None
		model_output = None
		result: list[ActionResult] = []
		step_start_time = time.time()
		tokens = 0

		try:
			print('step browser_context CUM:', self.browser_context)
			state = await self.browser_context.get_state(cache_clickable_elements_hashes=True)
			print('step state PEE: ',state)
			active_page = await self.browser_context.get_current_page()

			# generate procedural memory if needed
			if self.enable_memory and self.memory and self.state.n_steps % self.memory.config.memory_interval == 0:
				self.memory.create_procedural_memory(self.state.n_steps)

			await self._raise_if_stopped_or_paused()

			# Update action models with page-specific actions
			await self._update_action_models_for_page(active_page)

			# Get page-specific filtered actions
			page_filtered_actions = self.controller.registry.get_prompt_description(active_page)

			# If there are page-specific actions, add them as a special message for this step only
			if page_filtered_actions:
				page_action_message = f'For this page, these additional actions are available:\n{page_filtered_actions}'
				self._message_manager._add_message_with_tokens(HumanMessage(content=page_action_message))

			# If using raw tool calling method, we need to update the message context with new actions
			if self.tool_calling_method == 'raw':
				# For raw tool calling, get all non-filtered actions plus the page-filtered ones
				all_unfiltered_actions = self.controller.registry.get_prompt_description()
				all_actions = all_unfiltered_actions
				if page_filtered_actions:
					all_actions += '\n' + page_filtered_actions

				context_lines = (self._message_manager.settings.message_context or '').split('\n')
				non_action_lines = [line for line in context_lines if not line.startswith('Available actions:')]
				updated_context = '\n'.join(non_action_lines)
				if updated_context:
					updated_context += f'\n\nAvailable actions: {all_actions}'
				else:
					updated_context = f'Available actions: {all_actions}'
				self._message_manager.settings.message_context = updated_context

			print('agent_inject add_state_message NUT:', self.state)
			self._message_manager.add_state_message(state, self.state.last_result, step_info, self.settings.use_vision)

			# Run planner at specified intervals if planner is configured
			if self.settings.planner_llm and self.state.n_steps % self.settings.planner_interval == 0:
				plan = await self._run_planner()
				# add plan before last state message
				self._message_manager.add_plan(plan, position=-1)

			if step_info and step_info.is_last_step():
				# Add last step warning if needed
				msg = 'Now comes your last step. Use only the "done" action now. No other actions - so here your action sequence must have length 1.'
				msg += '\nIf the task is not yet fully finished as requested by the user, set success in "done" to false! E.g. if not all steps are fully completed.'
				msg += '\nIf the task is fully finished, set success in "done" to true.'
				msg += '\nInclude everything you found out for the ultimate task in the done text.'
				logger.info('Last step finishing up')
				self._message_manager._add_message_with_tokens(HumanMessage(content=msg))
				self.AgentOutput = self.DoneAgentOutput

			input_messages = self._message_manager.get_messages()
			tokens = self._message_manager.state.history.current_tokens

			try:
				model_output = await self.get_next_action(input_messages)
				if (
					not model_output.action
					or not isinstance(model_output.action, list)
					or all(action.model_dump() == {} for action in model_output.action)
				):
					logger.warning('Model returned empty action. Retrying...')

					clarification_message = HumanMessage(
						content='You forgot to return an action. Please respond only with a valid JSON action according to the expected format.'
					)

					retry_messages = input_messages + [clarification_message]
					model_output = await self.get_next_action(retry_messages)

					if not model_output.action or all(action.model_dump() == {} for action in model_output.action):
						logger.warning('Model still returned empty after retry. Inserting safe noop action.')
						action_instance = self.ActionModel(
							done={
								'success': False,
								'text': 'No next action returned by LLM!',
							}
						)
						model_output.action = [action_instance]

				# Check again for paused/stopped state after getting model output
				# This is needed in case Ctrl+C was pressed during the get_next_action call
				await self._raise_if_stopped_or_paused()

				self.state.n_steps += 1

				if self.register_new_step_callback:
					if inspect.iscoroutinefunction(self.register_new_step_callback):
						await self.register_new_step_callback(state, model_output, self.state.n_steps)
					else:
						self.register_new_step_callback(state, model_output, self.state.n_steps)
				if self.settings.save_conversation_path:
					target = self.settings.save_conversation_path + f'_{self.state.n_steps}.txt'
					save_conversation(input_messages, model_output, target, self.settings.save_conversation_path_encoding)

				self._message_manager._remove_last_state_message()  # we dont want the whole state in the chat history

				# check again if Ctrl+C was pressed before we commit the output to history
				await self._raise_if_stopped_or_paused()

				self._message_manager.add_model_output(model_output)
			except asyncio.CancelledError:
				# Task was cancelled due to Ctrl+C
				self._message_manager._remove_last_state_message()
				raise InterruptedError('Model query cancelled by user')
			except InterruptedError:
				# Agent was paused during get_next_action
				self._message_manager._remove_last_state_message()
				raise  # Re-raise to be caught by the outer try/except
			except Exception as e:
				# model call failed, remove last state message from history
				self._message_manager._remove_last_state_message()
				raise e

			result: list[ActionResult] = await self.multi_act(model_output.action)

			self.state.last_result = result

			if len(result) > 0 and result[-1].is_done:
				logger.info(f'📄 Result: {result[-1].extracted_content}')

			self.state.consecutive_failures = 0

		except InterruptedError:
			# logger.debug('Agent paused')
			self.state.last_result = [
				ActionResult(
					error='The agent was paused mid-step - the last action might need to be repeated', include_in_memory=False
				)
			]
			return
		except asyncio.CancelledError:
			# Directly handle the case where the step is cancelled at a higher level
			# logger.debug('Task cancelled - agent was paused with Ctrl+C')
			self.state.last_result = [ActionResult(error='The agent was paused with Ctrl+C', include_in_memory=False)]
			raise InterruptedError('Step cancelled by user')
		except Exception as e:
			result = await self._handle_step_error(e)
			self.state.last_result = result

		finally:
			step_end_time = time.time()
			actions = [a.model_dump(exclude_unset=True) for a in model_output.action] if model_output else []
			self.telemetry.capture(
				AgentStepTelemetryEvent(
					agent_id=self.state.agent_id,
					step=self.state.n_steps,
					actions=actions,
					consecutive_failures=self.state.consecutive_failures,
					step_error=[r.error for r in result if r.error] if result else ['No result'],
				)
			)
			if not result:
				return

			if state:
				metadata = StepMetadata(
					step_number=self.state.n_steps,
					step_start_time=step_start_time,
					step_end_time=step_end_time,
					input_tokens=tokens,
				)
				self._make_history_item(model_output, state, result, metadata)

	@time_execution_async('--handle_step_error (agent)')
	async def _handle_step_error(self, error: Exception) -> list[ActionResult]:
		"""Handle all types of errors that can occur during a step"""
		include_trace = logger.isEnabledFor(logging.DEBUG)
		error_msg = AgentError.format_error(error, include_trace=include_trace)
		prefix = f'❌ Result failed {self.state.consecutive_failures + 1}/{self.settings.max_failures} times:\n '
		self.state.consecutive_failures += 1

		if 'Browser closed' in error_msg:
			logger.error('❌  Browser is closed or disconnected, unable to proceed')
			return [ActionResult(error='Browser closed or disconnected, unable to proceed', include_in_memory=False)]

		if isinstance(error, (ValidationError, ValueError)):
			logger.error(f'{prefix}{error_msg}')
			if 'Max token limit reached' in error_msg:
				# cut tokens from history
				self._message_manager.settings.max_input_tokens = self.settings.max_input_tokens - 500
				logger.info(
					f'Cutting tokens from history - new max input tokens: {self._message_manager.settings.max_input_tokens}'
				)
				self._message_manager.cut_messages()
			elif 'Could not parse response' in error_msg:
				# give model a hint how output should look like
				error_msg += '\n\nReturn a valid JSON object with the required fields.'

		else:
			from anthropic import RateLimitError as AnthropicRateLimitError
			from google.api_core.exceptions import ResourceExhausted
			from openai import RateLimitError

			# Define a tuple of rate limit error types for easier maintenance
			RATE_LIMIT_ERRORS = (
				RateLimitError,  # OpenAI
				ResourceExhausted,  # Google
				AnthropicRateLimitError,  # Anthropic
			)

			if isinstance(error, RATE_LIMIT_ERRORS):
				logger.warning(f'{prefix}{error_msg}')
				await asyncio.sleep(self.settings.retry_delay)
			else:
				logger.error(f'{prefix}{error_msg}')

		return [ActionResult(error=error_msg, include_in_memory=True)]

	def _make_history_item(
		self,
		model_output: AgentOutput | None,
		state: BrowserState,
		result: list[ActionResult],
		metadata: Optional[StepMetadata] = None,
	) -> None:
		"""Create and store history item"""

		if model_output:
			interacted_elements = AgentHistory.get_interacted_element(model_output, state.selector_map)
		else:
			interacted_elements = [None]

		state_history = BrowserStateHistory(
			url=state.url,
			title=state.title,
			tabs=state.tabs,
			interacted_element=interacted_elements,
			screenshot=state.screenshot,
		)

		history_item = AgentHistory(model_output=model_output, result=result, state=state_history, metadata=metadata)

		self.state.history.history.append(history_item)

	THINK_TAGS = re.compile(r'<think>.*?</think>', re.DOTALL)
	STRAY_CLOSE_TAG = re.compile(r'.*?</think>', re.DOTALL)

	def _remove_think_tags(self, text: str) -> str:
		# Step 1: Remove well-formed <think>...</think>
		text = re.sub(self.THINK_TAGS, '', text)
		# Step 2: If there's an unmatched closing tag </think>,
		#         remove everything up to and including that.
		text = re.sub(self.STRAY_CLOSE_TAG, '', text)
		return text.strip()

	def _convert_input_messages(self, input_messages: list[BaseMessage]) -> list[BaseMessage]:
		"""Convert input messages to the correct format"""
		if is_model_without_tool_support(self.model_name):
			return convert_input_messages(input_messages, self.model_name)
		else:
			return input_messages

	@time_execution_async('--get_next_action (agent)')
	async def get_next_action(self, input_messages: list[BaseMessage]) -> AgentOutput:
		"""Get next action from LLM based on current state"""
		input_messages = self._convert_input_messages(input_messages)

		if self.tool_calling_method == 'raw':
			logger.debug(f'Using {self.tool_calling_method} for {self.chat_model_library}')
			try:
				output = self.llm.invoke(input_messages)
				response = {'raw': output, 'parsed': None}
			except Exception as e:
				logger.error(f'Failed to invoke model: {str(e)}')
				raise LLMException(401, 'LLM API call failed') from e
			# TODO: currently invoke does not return reasoning_content, we should override invoke
			output.content = self._remove_think_tags(str(output.content))
			try:
				parsed_json = extract_json_from_model_output(output.content)
				parsed = self.AgentOutput(**parsed_json)
				response['parsed'] = parsed
			except (ValueError, ValidationError) as e:
				logger.warning(f'Failed to parse model output: {output} {str(e)}')
				raise ValueError('Could not parse response.')

		elif self.tool_calling_method is None:
			structured_llm = self.llm.with_structured_output(self.AgentOutput, include_raw=True)
			try:
				response: dict[str, Any] = await structured_llm.ainvoke(input_messages)  # type: ignore
				parsed: AgentOutput | None = response['parsed']

			except Exception as e:
				logger.error(f'Failed to invoke model: {str(e)}')
				raise LLMException(401, 'LLM API call failed') from e

		else:
			logger.debug(f'Using {self.tool_calling_method} for {self.chat_model_library}')
			structured_llm = self.llm.with_structured_output(self.AgentOutput, include_raw=True, method=self.tool_calling_method)
			response: dict[str, Any] = await structured_llm.ainvoke(input_messages)  # type: ignore

		# Handle tool call responses
		if response.get('parsing_error') and 'raw' in response:
			raw_msg = response['raw']
			if hasattr(raw_msg, 'tool_calls') and raw_msg.tool_calls:
				# Convert tool calls to AgentOutput format

				tool_call = raw_msg.tool_calls[0]  # Take first tool call

				# Create current state
				tool_call_name = tool_call['name']
				tool_call_args = tool_call['args']

				current_state = {
					'page_summary': 'Processing tool call',
					'evaluation_previous_goal': 'Executing action',
					'memory': 'Using tool call',
					'next_goal': f'Execute {tool_call_name}',
				}

				# Create action from tool call
				action = {tool_call_name: tool_call_args}

				parsed = self.AgentOutput(current_state=current_state, action=[self.ActionModel(**action)])
			else:
				parsed = None
		else:
			parsed = response['parsed']

		if not parsed:
			try:
				parsed_json = extract_json_from_model_output(response['raw'].content)
				parsed = self.AgentOutput(**parsed_json)
			except Exception as e:
				logger.warning(f'Failed to parse model output: {response["raw"].content} {str(e)}')
				raise ValueError('Could not parse response.')

		# cut the number of actions to max_actions_per_step if needed
		if len(parsed.action) > self.settings.max_actions_per_step:
			parsed.action = parsed.action[: self.settings.max_actions_per_step]

		if not (hasattr(self.state, 'paused') and (self.state.paused or self.state.stopped)):
			log_response(parsed)

		return parsed

	def _log_agent_run(self) -> None:
		"""Log the agent run"""
		logger.info(f'🚀 Starting task: {self.task}')

		logger.debug(f'Version: {self.version}, Source: {self.source}')
		self.telemetry.capture(
			AgentRunTelemetryEvent(
				agent_id=self.state.agent_id,
				use_vision=self.settings.use_vision,
				task=self.task,
				model_name=self.model_name,
				chat_model_library=self.chat_model_library,
				version=self.version,
				source=self.source,
			)
		)

	async def take_step(self) -> tuple[bool, bool]:
		"""Take a step

		Returns:
			Tuple[bool, bool]: (is_done, is_valid)
		"""
		await self.step()

		if self.state.history.is_done():
			if self.settings.validate_output:
				if not await self._validate_output():
					return True, False

			await self.log_completion()
			if self.register_done_callback:
				if inspect.iscoroutinefunction(self.register_done_callback):
					await self.register_done_callback(self.state.history)
				else:
					self.register_done_callback(self.state.history)
			return True, True

		return False, False

	# @observe(name='agent.run', ignore_output=True)
	@time_execution_async('--run (agent)')
	async def run(
		self, max_steps: int = 100, on_step_start: AgentHookFunc | None = None, on_step_end: AgentHookFunc | None = None
	) -> AgentHistoryList:
		"""Execute the task with maximum number of steps"""

		loop = asyncio.get_event_loop()

		# Set up the Ctrl+C signal handler with callbacks specific to this agent
		from browser_use.utils import SignalHandler

		signal_handler = SignalHandler(
			loop=loop,
			pause_callback=self.pause,
			resume_callback=self.resume,
			custom_exit_callback=None,  # No special cleanup needed on forced exit
			exit_on_second_int=True,
		)
		signal_handler.register()

		try:
			self._log_agent_run()

			# Execute initial actions if provided
			if self.initial_actions:
				result = await self.multi_act(self.initial_actions, check_for_new_elements=False)
				self.state.last_result = result

			for step in range(max_steps):
				# Check if waiting for user input after Ctrl+C
				if self.state.paused:
					signal_handler.wait_for_resume()
					signal_handler.reset()

				# Check if we should stop due to too many failures
				if self.state.consecutive_failures >= self.settings.max_failures:
					logger.error(f'❌ Stopping due to {self.settings.max_failures} consecutive failures')
					break

				# Check control flags before each step
				if self.state.stopped:
					logger.info('Agent stopped')
					break

				while self.state.paused:
					await asyncio.sleep(0.2)  # Small delay to prevent CPU spinning
					if self.state.stopped:  # Allow stopping while paused
						break

				if on_step_start is not None:
					await on_step_start(self)

				step_info = AgentStepInfo(step_number=step, max_steps=max_steps)
				await self.step(step_info)

				if on_step_end is not None:
					await on_step_end(self)

				if self.state.history.is_done():
					if self.settings.validate_output and step < max_steps - 1:
						if not await self._validate_output():
							continue

					await self.log_completion()
					break
			else:
				error_message = 'Failed to complete task in maximum steps'

				self.state.history.history.append(
					AgentHistory(
						model_output=None,
						result=[ActionResult(error=error_message, include_in_memory=True)],
						state=BrowserStateHistory(
							url='',
							title='',
							tabs=[],
							interacted_element=[],
							screenshot=None,
						),
						metadata=None,
					)
				)

				logger.info(f'❌ {error_message}')

			return self.state.history

		except KeyboardInterrupt:
			# Already handled by our signal handler, but catch any direct KeyboardInterrupt as well
			logger.info('Got KeyboardInterrupt during execution, returning current history')
			return self.state.history

		finally:
			# Unregister signal handlers before cleanup
			signal_handler.unregister()

			self.telemetry.capture(
				AgentEndTelemetryEvent(
					agent_id=self.state.agent_id,
					is_done=self.state.history.is_done(),
					success=self.state.history.is_successful(),
					steps=self.state.n_steps,
					max_steps_reached=self.state.n_steps >= max_steps,
					errors=self.state.history.errors(),
					total_input_tokens=self.state.history.total_input_tokens(),
					total_duration_seconds=self.state.history.total_duration_seconds(),
				)
			)

			if self.settings.save_playwright_script_path:
				logger.info(
					f'Agent run finished. Attempting to save Playwright script to: {self.settings.save_playwright_script_path}'
				)
				try:
					# Extract sensitive data keys if sensitive_data is provided
					keys = list(self.sensitive_data.keys()) if self.sensitive_data else None
					# Pass browser and context config to the saving method
					self.state.history.save_as_playwright_script(
						self.settings.save_playwright_script_path,
						sensitive_data_keys=keys,
						browser_config=self.browser.config,
						context_config=self.browser_context.config,
					)
				except Exception as script_gen_err:
					# Log any error during script generation/saving
					logger.error(f'Failed to save Playwright script: {script_gen_err}', exc_info=True)

			await self.close()

			if self.settings.generate_gif:
				output_path: str = 'agent_history.gif'
				if isinstance(self.settings.generate_gif, str):
					output_path = self.settings.generate_gif

				create_history_gif(task=self.task, history=self.state.history, output_path=output_path)

	# @observe(name='controller.multi_act')
	@time_execution_async('--multi-act (agent)')
	async def multi_act(
		self,
		actions: list[ActionModel],
		check_for_new_elements: bool = True,
	) -> list[ActionResult]:
		"""Execute multiple actions"""
		results = []

		cached_selector_map = await self.browser_context.get_selector_map()
		cached_path_hashes = set(e.hash.branch_path_hash for e in cached_selector_map.values())

		await self.browser_context.remove_highlights()

		for i, action in enumerate(actions):
			if action.get_index() is not None and i != 0:
				new_state = await self.browser_context.get_state(cache_clickable_elements_hashes=False)
				new_selector_map = new_state.selector_map

				# Detect index change after previous action
				orig_target = cached_selector_map.get(action.get_index())  # type: ignore
				orig_target_hash = orig_target.hash.branch_path_hash if orig_target else None
				new_target = new_selector_map.get(action.get_index())  # type: ignore
				new_target_hash = new_target.hash.branch_path_hash if new_target else None
				if orig_target_hash != new_target_hash:
					msg = f'Element index changed after action {i} / {len(actions)}, because page changed.'
					logger.info(msg)
					results.append(ActionResult(extracted_content=msg, include_in_memory=True))
					break

				new_path_hashes = set(e.hash.branch_path_hash for e in new_selector_map.values())
				if check_for_new_elements and not new_path_hashes.issubset(cached_path_hashes):
					# next action requires index but there are new elements on the page
					msg = f'Something new appeared after action {i} / {len(actions)}'
					logger.info(msg)
					results.append(ActionResult(extracted_content=msg, include_in_memory=True))
					break

			try:
				await self._raise_if_stopped_or_paused()

				result = await self.controller.act(
					action,
					self.browser_context,
					self.settings.page_extraction_llm,
					self.sensitive_data,
					self.settings.available_file_paths,
					context=self.context,
				)

				results.append(result)

				logger.debug(f'Executed action {i + 1} / {len(actions)}')
				if results[-1].is_done or results[-1].error or i == len(actions) - 1:
					break

				await asyncio.sleep(self.browser_context.config.wait_between_actions)
				# hash all elements. if it is a subset of cached_state its fine - else break (new elements on page)

			except asyncio.CancelledError:
				# Gracefully handle task cancellation
				logger.info(f'Action {i + 1} was cancelled due to Ctrl+C')
				if not results:
					# Add a result for the cancelled action
					results.append(ActionResult(error='The action was cancelled due to Ctrl+C', include_in_memory=True))
				raise InterruptedError('Action cancelled by user')

		return results

	async def _validate_output(self) -> bool:
		"""Validate the output of the last action is what the user wanted"""
		system_msg = (
			f'You are a validator of an agent who interacts with a browser. '
			f'Validate if the output of last action is what the user wanted and if the task is completed. '
			f'If the task is unclear defined, you can let it pass. But if something is missing or the image does not show what was requested dont let it pass. '
			f'Try to understand the page and help the model with suggestions like scroll, do x, ... to get the solution right. '
			f'Task to validate: {self.task}. Return a JSON object with 2 keys: is_valid and reason. '
			f'is_valid is a boolean that indicates if the output is correct. '
			f'reason is a string that explains why it is valid or not.'
			f' example: {{"is_valid": false, "reason": "The user wanted to search for "cat photos", but the agent searched for "dog photos" instead."}}'
		)

		if self.browser_context.session:
			state = await self.browser_context.get_state(cache_clickable_elements_hashes=False)
			content = AgentMessagePrompt(
				state=state,
				result=self.state.last_result,
				include_attributes=self.settings.include_attributes,
			)
			msg = [SystemMessage(content=system_msg), content.get_user_message(self.settings.use_vision)]
		else:
			# if no browser session, we can't validate the output
			return True

		class ValidationResult(BaseModel):
			"""
			Validation results.
			"""

			is_valid: bool
			reason: str

		validator = self.llm.with_structured_output(ValidationResult, include_raw=True)
		response: dict[str, Any] = await validator.ainvoke(msg)  # type: ignore
		parsed: ValidationResult = response['parsed']
		is_valid = parsed.is_valid
		if not is_valid:
			logger.info(f'❌ Validator decision: {parsed.reason}')
			msg = f'The output is not yet correct. {parsed.reason}.'
			self.state.last_result = [ActionResult(extracted_content=msg, include_in_memory=True)]
		else:
			logger.info(f'✅ Validator decision: {parsed.reason}')
		return is_valid

	async def log_completion(self) -> None:
		"""Log the completion of the task"""
		logger.info('✅ Task completed')
		if self.state.history.is_successful():
			logger.info('✅ Successfully')
		else:
			logger.info('❌ Unfinished')

		total_tokens = self.state.history.total_input_tokens()
		logger.info(f'📝 Total input tokens used (approximate): {total_tokens}')

		if self.register_done_callback:
			if inspect.iscoroutinefunction(self.register_done_callback):
				await self.register_done_callback(self.state.history)
			else:
				self.register_done_callback(self.state.history)

	async def rerun_history(
		self,
		history: AgentHistoryList,
		max_retries: int = 3,
		skip_failures: bool = True,
		delay_between_actions: float = 2.0,
	) -> list[ActionResult]:
		"""
		Rerun a saved history of actions with error handling and retry logic.

		Args:
				history: The history to replay
				max_retries: Maximum number of retries per action
				skip_failures: Whether to skip failed actions or stop execution
				delay_between_actions: Delay between actions in seconds

		Returns:
				List of action results
		"""
		# Execute initial actions if provided
		if self.initial_actions:
			result = await self.multi_act(self.initial_actions)
			self.state.last_result = result

		results = []

		for i, history_item in enumerate(history.history):
			goal = history_item.model_output.current_state.next_goal if history_item.model_output else ''
			logger.info(f'Replaying step {i + 1}/{len(history.history)}: goal: {goal}')

			if (
				not history_item.model_output
				or not history_item.model_output.action
				or history_item.model_output.action == [None]
			):
				logger.warning(f'Step {i + 1}: No action to replay, skipping')
				results.append(ActionResult(error='No action to replay'))
				continue

			retry_count = 0
			while retry_count < max_retries:
				try:
					result = await self._execute_history_step(history_item, delay_between_actions)
					results.extend(result)
					break

				except Exception as e:
					retry_count += 1
					if retry_count == max_retries:
						error_msg = f'Step {i + 1} failed after {max_retries} attempts: {str(e)}'
						logger.error(error_msg)
						if not skip_failures:
							results.append(ActionResult(error=error_msg))
							raise RuntimeError(error_msg)
					else:
						logger.warning(f'Step {i + 1} failed (attempt {retry_count}/{max_retries}), retrying...')
						await asyncio.sleep(delay_between_actions)

		return results

	async def _execute_history_step(self, history_item: AgentHistory, delay: float) -> list[ActionResult]:
		"""Execute a single step from history with element validation"""
		state = await self.browser_context.get_state(cache_clickable_elements_hashes=False)
		if not state or not history_item.model_output:
			raise ValueError('Invalid state or model output')
		updated_actions = []
		for i, action in enumerate(history_item.model_output.action):
			updated_action = await self._update_action_indices(
				history_item.state.interacted_element[i],
				action,
				state,
			)
			updated_actions.append(updated_action)

			if updated_action is None:
				raise ValueError(f'Could not find matching element {i} in current page')

		result = await self.multi_act(updated_actions)

		await asyncio.sleep(delay)
		return result

	async def _update_action_indices(
		self,
		historical_element: Optional[DOMHistoryElement],
		action: ActionModel,  # Type this properly based on your action model
		current_state: BrowserState,
	) -> Optional[ActionModel]:
		"""
		Update action indices based on current page state.
		Returns updated action or None if element cannot be found.
		"""
		if not historical_element or not current_state.element_tree:
			return action

		current_element = HistoryTreeProcessor.find_history_element_in_tree(historical_element, current_state.element_tree)

		if not current_element or current_element.highlight_index is None:
			return None

		old_index = action.get_index()
		if old_index != current_element.highlight_index:
			action.set_index(current_element.highlight_index)
			logger.info(f'Element moved in DOM, updated index from {old_index} to {current_element.highlight_index}')

		return action

	async def load_and_rerun(self, history_file: Optional[str | Path] = None, **kwargs) -> list[ActionResult]:
		"""
		Load history from file and rerun it.

		Args:
				history_file: Path to the history file
				**kwargs: Additional arguments passed to rerun_history
		"""
		if not history_file:
			history_file = 'AgentHistory.json'
		history = AgentHistoryList.load_from_file(history_file, self.AgentOutput)
		return await self.rerun_history(history, **kwargs)

	def save_history(self, file_path: Optional[str | Path] = None) -> None:
		"""Save the history to a file"""
		if not file_path:
			file_path = 'AgentHistory.json'
		self.state.history.save_to_file(file_path)

	def pause(self) -> None:
		"""Pause the agent before the next step"""
		print('\n\n⏸️  Got Ctrl+C, paused the agent and left the browser open.')
		self.state.paused = True

		# The signal handler will handle the asyncio pause logic for us
		# No need to duplicate the code here

	def resume(self) -> None:
		"""Resume the agent"""
		print('----------------------------------------------------------------------')
		print('▶️  Got Enter, resuming agent execution where it left off...\n')
		self.state.paused = False

		# The signal handler should have already reset the flags
		# through its reset() method when called from run()

		# playwright browser is always immediately killed by the first Ctrl+C (no way to stop that)
		# so we need to restart the browser if user wants to continue
		if self.browser:
			logger.info('🌎 Restarting/reconnecting to browser...')
			loop = asyncio.get_event_loop()
			loop.create_task(self.browser._init())
			loop.create_task(asyncio.sleep(5))

	def stop(self) -> None:
		"""Stop the agent"""
		logger.info('⏹️ Agent stopping')
		self.state.stopped = True

	def _convert_initial_actions(self, actions: List[Dict[str, Dict[str, Any]]]) -> List[ActionModel]:
		"""Convert dictionary-based actions to ActionModel instances"""
		converted_actions = []
		action_model = self.ActionModel
		for action_dict in actions:
			# Each action_dict should have a single key-value pair
			action_name = next(iter(action_dict))
			params = action_dict[action_name]

			# Get the parameter model for this action from registry
			action_info = self.controller.registry.registry.actions[action_name]
			param_model = action_info.param_model

			# Create validated parameters using the appropriate param model
			validated_params = param_model(**params)

			# Create ActionModel instance with the validated parameters
			action_model = self.ActionModel(**{action_name: validated_params})
			converted_actions.append(action_model)

		return converted_actions

	def _verify_llm_connection(self) -> bool:
		"""
		Verify that the LLM API keys are setup and the LLM API is responding properly.
		Helps prevent errors due to running out of API credits, missing env vars, or network issues.
		"""
		logger.debug(f'Verifying the {self.llm.__class__.__name__} LLM knows the capital of France...')

		if getattr(self.llm, '_verified_api_keys', None) is True or SKIP_LLM_API_KEY_VERIFICATION:
			# skip roundtrip connection test for speed in cloud environment
			# If the LLM API keys have already been verified during a previous run, skip the test
			self.llm._verified_api_keys = True
			return True

		# show a warning if it looks like any required environment variables are missing
		required_keys = REQUIRED_LLM_API_ENV_VARS.get(self.llm.__class__.__name__, [])
		if required_keys and not check_env_variables(required_keys, any_or_all=all):
			error = f'Expected LLM API Key environment variables might be missing for {self.llm.__class__.__name__}: {" ".join(required_keys)}'
			logger.warning(f'❌ {error}')

		# send a basic sanity-test question to the LLM and verify the response
		test_prompt = 'What is the capital of France? Respond with a single word.'
		test_answer = 'paris'
		try:
			# dont convert this to async! it *should* block any subsequent llm calls from running
			response = self.llm.invoke([HumanMessage(content=test_prompt)])  # noqa: RUF006
			response_text = str(response.content).lower()

			if test_answer in response_text:
				logger.debug(
					f'🪪 LLM API keys {", ".join(required_keys)} work, {self.llm.__class__.__name__} model is connected & responding correctly.'
				)
				self.llm._verified_api_keys = True
				return True
			else:
				logger.warning(
					'❌  Got bad LLM response to basic sanity check question: \n\t  %s\n\t\tEXPECTING: %s\n\t\tGOT: %s',
					test_prompt,
					test_answer,
					response,
				)
				raise Exception('LLM responded to a simple test question incorrectly')
		except Exception as e:
			self.llm._verified_api_keys = False
			if required_keys:
				logger.error(
					f'\n\n❌  LLM {self.llm.__class__.__name__} connection test failed. Check that {", ".join(required_keys)} is set correctly in .env and that the LLM API account has sufficient funding.\n\n{e}\n'
				)
				return False
			else:
				pass

	async def _run_planner(self) -> Optional[str]:
		"""Run the planner to analyze state and suggest next steps"""
		# Skip planning if no planner_llm is set
		if not self.settings.planner_llm:
			return None

		# Get current state to filter actions by page
		page = await self.browser_context.get_current_page()

		# Get all standard actions (no filter) and page-specific actions
		standard_actions = self.controller.registry.get_prompt_description()  # No page = system prompt actions
		page_actions = self.controller.registry.get_prompt_description(page)  # Page-specific actions

		# Combine both for the planner
		all_actions = standard_actions
		if page_actions:
			all_actions += '\n' + page_actions

		# Create planner message history using full message history with all available actions
		planner_messages = [
			PlannerPrompt(all_actions).get_system_message(
				is_planner_reasoning=self.settings.is_planner_reasoning,
				extended_planner_system_prompt=self.settings.extend_planner_system_message,
			),
			*self._message_manager.get_messages()[1:],  # Use full message history except the first
		]

		if not self.settings.use_vision_for_planner and self.settings.use_vision:
			last_state_message: HumanMessage = planner_messages[-1]
			# remove image from last state message
			new_msg = ''
			if isinstance(last_state_message.content, list):
				for msg in last_state_message.content:
					if msg['type'] == 'text':  # type: ignore
						new_msg += msg['text']  # type: ignore
					elif msg['type'] == 'image_url':  # type: ignore
						continue  # type: ignore
			else:
				new_msg = last_state_message.content

			planner_messages[-1] = HumanMessage(content=new_msg)

		planner_messages = convert_input_messages(planner_messages, self.planner_model_name)

		# Get planner output
		try:
			response = await self.settings.planner_llm.ainvoke(planner_messages)
		except Exception as e:
			logger.error(f'Failed to invoke planner: {str(e)}')
			raise LLMException(401, 'LLM API call failed') from e

		plan = str(response.content)
		# if deepseek-reasoner, remove think tags
		if self.planner_model_name and (
			'deepseek-r1' in self.planner_model_name or 'deepseek-reasoner' in self.planner_model_name
		):
			plan = self._remove_think_tags(plan)
		try:
			plan_json = json.loads(plan)
			logger.info(f'Planning Analysis:\n{json.dumps(plan_json, indent=4)}')
		except json.JSONDecodeError:
			logger.info(f'Planning Analysis:\n{plan}')
		except Exception as e:
			logger.debug(f'Error parsing planning analysis: {e}')
			logger.info(f'Plan: {plan}')

		return plan

	@property
	def message_manager(self) -> MessageManager:
		return self._message_manager

	async def close(self):
		"""Close all resources"""
		try:
			# First close browser resources
			if self.browser_context and not self.injected_browser_context:
				await self.browser_context.close()
			if self.browser and not self.injected_browser:
				await self.browser.close()

			# Force garbage collection
			gc.collect()

		except Exception as e:
			logger.error(f'Error during cleanup: {e}')

	async def _update_action_models_for_page(self, page) -> None:
		"""Update action models with page-specific actions"""
		# Create new action model with current page's filtered actions
		self.ActionModel = self.controller.registry.create_action_model(page=page)
		# Update output model with the new actions
		self.AgentOutput = AgentOutput.type_with_custom_actions(self.ActionModel)

		# Update done action model too
		self.DoneActionModel = self.controller.registry.create_action_model(include_actions=['done'], page=page)
		self.DoneAgentOutput = AgentOutput.type_with_custom_actions(self.DoneActionModel)
````
