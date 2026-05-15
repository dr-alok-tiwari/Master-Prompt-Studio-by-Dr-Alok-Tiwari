"""
Offline validation script for Master Productivity Prompt Studio.
Run from the project root:
    python validate_project.py
"""

from __future__ import annotations

import ast
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY_FILES = [ROOT / "app.py", *sorted((ROOT / "modules").glob("*.py"))]
REQUIRED_FILES = [
    "app.py",
    "requirements.txt",
    "README.md",
    "CHANGELOG.md",
    ".streamlit/config.toml",
    "data/sample_inputs.json",
    "data/prompt_templates.json",
    "data/saved_prompts.json",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def check_required_files() -> list[str]:
    errors = []
    for item in REQUIRED_FILES:
        if not (ROOT / item).exists():
            errors.append(f"Missing required file: {item}")
    return errors


def check_python_syntax() -> list[str]:
    errors = []
    for path in PY_FILES:
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"Syntax error in {rel(path)}: line {exc.lineno}: {exc.msg}")
    return errors


def check_json_files() -> list[str]:
    errors = []
    for path in sorted((ROOT / "data").glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"Invalid JSON in {rel(path)}: {exc}")
    return errors


def _literal_key(node: ast.AST):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return None  # Dynamic keys are allowed; inspect manually if needed.
    return None


def check_duplicate_static_streamlit_keys() -> list[str]:
    """Detect duplicate literal Streamlit widget keys within the codebase."""
    occurrences = defaultdict(list)
    for path in PY_FILES:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                for kw in node.keywords:
                    if kw.arg == "key":
                        key = _literal_key(kw.value)
                        if key:
                            occurrences[key].append(f"{rel(path)}:{getattr(node, 'lineno', '?')}")
    errors = []
    for key, places in sorted(occurrences.items()):
        if len(places) > 1:
            errors.append(f"Duplicate literal Streamlit key '{key}' at {', '.join(places)}")
    return errors


def check_forms_have_submit_buttons() -> list[str]:
    warnings = []
    for path in PY_FILES:
        text = path.read_text(encoding="utf-8")
        if "st.form(" in text and "form_submit_button" not in text:
            warnings.append(f"Potential Streamlit form without submit button in {rel(path)}")
    return warnings


def check_requirements() -> list[str]:
    req = ROOT / "requirements.txt"
    if not req.exists():
        return ["requirements.txt missing"]
    text = req.read_text(encoding="utf-8").lower()
    required = ["streamlit", "python-docx", "pypdf"]
    return [f"requirements.txt missing dependency: {name}" for name in required if name not in text]


def main() -> int:
    checks = {
        "required files": check_required_files(),
        "python syntax": check_python_syntax(),
        "json validity": check_json_files(),
        "duplicate widget keys": check_duplicate_static_streamlit_keys(),
        "form submit buttons": check_forms_have_submit_buttons(),
        "requirements": check_requirements(),
    }

    print("\nMaster Productivity Prompt Studio — validation report")
    print("=" * 64)
    failed = False
    for name, issues in checks.items():
        if issues:
            failed = True
            print(f"\n[{name.upper()}] {len(issues)} issue(s)")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"[OK] {name}")

    print("\n" + "=" * 64)
    if failed:
        print("Validation completed with issues. Review the messages above.")
        return 1
    print("All validation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
