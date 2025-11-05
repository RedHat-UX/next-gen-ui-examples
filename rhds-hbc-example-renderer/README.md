# Next Gen UI Red Hat Hand Build Component Example Renderer extension for RHDS

This package provides an example implementation of how to extend the Red Hat Design System (RHDS) renderer to support custom Hand Build Components (HBC) for the Next Gen UI Agent.

## Installation

### Prerequisites

- Python 3.12 or higher
- Access to the `next_gen_ui_agent`, `next_gen_ui_rhds_renderer`, and `next_gen_ui_testing` packages

### Install from source

1. Navigate to this directory:
   ```sh
   cd rhds-hbc-example-renderer
   ```

2. Create a virtual environment (recommended):
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Install this package in editable mode:
   ```sh
   pip install -e .
   ```

### Local Development Setup

If you're developing alongside the `next-gen-ui-agent` repository:

```sh
# Uninstall any existing versions
pip uninstall -y next_gen_ui_agent next_gen_ui_rhds_renderer next_gen_ui_testing rhds_hbc_example_renderer

# Install local builds from next-gen-ui-agent
pip install ../../next-gen-ui-agent/dist/next_gen_ui*.whl

# Install this package in editable mode
pip install -e .
```

## Usage

Once installed, the renderer is automatically discovered by Next Gen UI Agent through the entry point system. To use it, configure your Next Gen UI Agent to use `hbc-example-rhds` as the component system.

Example:
```python
from next_gen_ui_agent import NextGenUIAgent

agent = NextGenUIAgent()
# Use "hbc-example-rhds" as the component system name
rendition = agent.design_system_handler(components, "hbc-example-rhds")
```

## Supported Components

This example renderer supports:
- `hbc-example-component` - A simple example hand-build component
- All standard dynamic components supported by the base RHDS renderer (one-card, image, video-player, etc.)

## Customization

To create your own HBC renderer based on this example:

1. Copy this directory
2. Update the `CUSTOM_HBC_COMPONENTS` list in `hbc_renderer.py` with your component names
3. Create Jinja templates in the `templates/` directory matching your component names
4. Update the `get_component_system_name()` method to return your renderer name
5. Update `setup.py` with your package name and entry points

## Testing

Run the tests using pytest:
```sh
pytest hbc_renderer_test.py
```

## Package Structure

```
rhds-hbc-example-renderer/
  ├── __init__.py                    # Package initialization
  ├── hbc_renderer.py                # Main renderer implementation
  ├── hbc_renderer_test.py           # Test suite
  ├── setup.py                       # Package configuration
  ├── requirements.txt               # Dependencies
  ├── README.md                      # This file
  └── templates/                     # Jinja templates
      ├── hbc-example-component.jinja
      └── DUMMY_COMPONENT_TYPE.jinja
```

