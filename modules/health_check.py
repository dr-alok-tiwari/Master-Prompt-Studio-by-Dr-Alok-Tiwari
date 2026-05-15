"""
Production health-check page for Master Productivity Prompt Studio.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import streamlit as st

from modules.utils import apply_css, section_header, DATA_DIR, SAVED_PROMPTS_FILE, SAMPLE_INPUTS_FILE, TEMPLATES_FILE

ROOT = Path(__file__).resolve().parents[1]


def _status_row(name: str, ok: bool, detail: str):
    icon = "✅" if ok else "⚠️"
    colour = "#2E7D52" if ok else "#B65C00"
    st.markdown(
        f"""<div style="background:#FFFFFF;border:1px solid #EDE0D0;border-radius:10px;
        padding:10px 14px;margin:6px 0;display:flex;gap:10px;align-items:flex-start;">
        <span style="font-size:1.1rem;">{icon}</span>
        <div><b style="color:{colour};">{name}</b><br>
        <span style="font-size:0.86rem;color:#4A4A5A;">{detail}</span></div></div>""",
        unsafe_allow_html=True,
    )


def _python_files_compile() -> tuple[bool, str]:
    failures = []
    for path in [ROOT / "app.py", *sorted((ROOT / "modules").glob("*.py"))]:
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            failures.append(f"{path.relative_to(ROOT)}: {exc}")
    if failures:
        return False, "; ".join(failures)
    return True, "All Python files passed syntax parsing."


def _json_ok(path: str) -> tuple[bool, str]:
    p = Path(path)
    if not p.exists():
        return False, f"Missing: {p.relative_to(ROOT)}"
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return True, f"Valid JSON list with {len(data)} item(s)."
        if isinstance(data, dict):
            return True, f"Valid JSON object with {len(data)} top-level key(s)."
        return True, "Valid JSON."
    except Exception as exc:
        return False, f"Invalid JSON: {exc}"


def _file_exists(rel: str) -> tuple[bool, str]:
    p = ROOT / rel
    return p.exists(), f"{rel} {'exists' if p.exists() else 'is missing'}."


def render():
    apply_css()
    st.markdown('<div class="page-title">🩺 Production Health Check</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Validate project files, JSON storage, syntax, and deployment readiness.</div>', unsafe_allow_html=True)

    section_header("Automated Checks", "✅")
    checks = [
        ("Python syntax", *_python_files_compile()),
        ("Local data folder", Path(DATA_DIR).exists(), f"Data folder: {Path(DATA_DIR).relative_to(ROOT)}"),
        ("Saved prompt library", *_json_ok(SAVED_PROMPTS_FILE)),
        ("Sample inputs", *_json_ok(SAMPLE_INPUTS_FILE)),
        ("Prompt templates", *_json_ok(TEMPLATES_FILE)),
        ("Requirements file", *_file_exists("requirements.txt")),
        ("Streamlit config", *_file_exists(".streamlit/config.toml")),
        ("README", *_file_exists("README.md")),
        ("Changelog", *_file_exists("CHANGELOG.md")),
    ]

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    c1, c2, c3 = st.columns(3)
    c1.metric("Checks passed", f"{passed}/{total}")
    c2.metric("Project mode", "Offline")
    c3.metric("Paid APIs", "0")

    for name, ok, detail in checks:
        _status_row(name, ok, detail)

    section_header("Deployment Checklist", "🚀")
    st.markdown(
        """
        - Run `python validate_project.py` before sharing the project.
        - Run `streamlit run app.py` locally and open each major studio once.
        - Confirm `data/saved_prompts.json` is writable if saving prompts is required.
        - For Streamlit Community Cloud, set the main file path to `app.py`.
        - No API keys or paid services are required.
        """
    )

    section_header("Troubleshooting", "🛠")
    st.info("If the app starts but a file upload cannot be read, reinstall optional parsers with `pip install pypdf python-docx`.")
