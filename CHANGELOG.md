# Changelog

## Version 1.1.0 — Production Readiness Upgrade

### Added
- Production Health Check page inside the app.
- Offline `validate_project.py` smoke-test script.
- Streamlit deployment configuration under `.streamlit/config.toml`.
- DOCX export option for generated prompts.
- Safer file extraction helper for TXT, PDF, and DOCX uploads.
- Corrupt JSON recovery behavior for local prompt storage.
- Stronger responsive CSS for projector, classroom, and smaller screens.

### Improved
- More robust app-level error boundary so one page failure does not stop the full app.
- Safer clipboard-copy JavaScript generation.
- Safer HTML escaping in prompt previews and prompt library previews.
- Cleaner filename handling for prompt-library downloads.
- Better validation flow so empty required inputs do not navigate to the output tab.
- README updated for local use, deployment, troubleshooting, and production operations.

### Fixed
- Hidden/brittle file-upload extraction behavior.
- Potential unsafe HTML rendering in previews.
- Missing production validation workflow.
- Missing deployment configuration.

## Visual Hotfix - Tab Selector Polish
- Replaced the custom div-plus-button studio tab layout with a single accessible radio-based segmented control.
- Removed emoji icons from the main studio tabs to avoid missing-glyph rendering on some Windows/browser/projector setups.
- Fixed the duplicate “Final Prompt” label/button issue visible when the Inputs tab was active.
- Added responsive CSS for the new tab selector.

## Navigation Hotfix - Generate to Final Prompt
- Fixed the Generate Prompt action not switching automatically to the Final Prompt tab.
- Added safe pending-tab navigation so Streamlit widget state is not modified after radio widget creation.
- Preserved the clean single-row tab selector introduced in the visual hotfix.
