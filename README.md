# 🧠 Master Productivity Prompt Studio

**Created by:** Dr Alok Tiwari  
**Affiliation:** Goa Institute of Management, Goa  
**Version:** 1.1.0 — Production Readiness Upgrade  
**Mode:** Fully offline, API-free, no paid services required

---

## 1. Purpose

Master Productivity Prompt Studio is a modular Streamlit application for generating high-quality master prompts for academic, research, teaching, productivity, career, and professional writing workflows.

The app does **not** call OpenAI, Gemini, Claude, or any paid API. It prepares structured prompts that users can copy, edit, save, and reuse in their preferred AI tool.

---

## 2. Key Features

| Area | Capability |
|---|---|
| Prompt generation | 12 specialised prompt studios for research, teaching, CVs, workflows, apps, emails, and custom prompts |
| User experience | Clean saffron-themed UI, sidebar navigation, guided inputs, editable outputs, prompt statistics |
| Export | Copy prompt, download TXT, Markdown, and DOCX |
| Prompt library | Save, search, edit, delete, import, and export prompts locally |
| File upload | TXT, PDF, and DOCX extraction for job descriptions, CVs, templates, and source material |
| Template support | Built-in and uploadable templates for structured prompt outputs |
| Production readiness | Health Check page, offline validation script, Streamlit config, robust error boundary |
| Deployment | Ready for local use and Streamlit Community Cloud deployment |

---

## 3. Available Studios

1. 🔬 **Research Paper Intelligence** — paper intake, gap scanning, contradiction analysis, synthesis  
2. 📖 **Handbook Generator** — detailed multi-level handbooks with examples, cases, glossary, exercises  
3. 🎓 **Course Profile Generator** — CLOs, PLO mapping, session plans, rubrics, assessments  
4. 💼 **Job Application Materials** — cover letter, research statement, teaching statement, ATS summaries  
5. 📄 **ATS CV Score Improver** — ATS scoring, keyword gap analysis, CV bullet rewriting  
6. 📚 **Teaching Content Generator** — lecture plans, slides, examples, activities, quizzes  
7. ❓ **Quiz & Case Study Generator** — MCQs, case questions, Bloom’s mapping, answer keys, rubrics  
8. ✉️ **Professional Email Generator** — formal, warm, concise, follow-up, reminder, WhatsApp versions  
9. 🧪 **Research Productivity Generator** — problem statements, gaps, frameworks, abstracts, outlines  
10. ⚙️ **Productivity Workflow Generator** — workflows, checklists, automation points, review cycles  
11. 💻 **Streamlit App Prompt Generator** — prompts for full Streamlit app creation  
12. 🧩 **Custom Prompt Builder** — RCTOFE and other structured prompting frameworks  
13. 📚 **My Prompt Library** — local prompt repository  
14. 🩺 **Health Check** — project readiness and deployment validation dashboard

---

## 4. Folder Structure

```text
master_productivity_prompt_studio/
├── app.py
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── validate_project.py
├── .streamlit/
│   └── config.toml
├── data/
│   ├── prompt_templates.json
│   ├── sample_inputs.json
│   └── saved_prompts.json
└── modules/
    ├── about.py
    ├── ats_cv_studio.py
    ├── course_profile_studio.py
    ├── custom_prompt_builder.py
    ├── email_studio.py
    ├── handbook_studio.py
    ├── health_check.py
    ├── home.py
    ├── job_application_studio.py
    ├── prompt_library.py
    ├── quiz_case_studio.py
    ├── research_productivity_studio.py
    ├── research_prompt_studio.py
    ├── streamlit_app_prompt_studio.py
    ├── teaching_content_studio.py
    ├── utils.py
    └── workflow_studio.py
```

---

## 5. Installation

### Windows PowerShell

```powershell
cd master_productivity_prompt_studio
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux

```bash
cd master_productivity_prompt_studio
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

The app opens at:

```text
http://localhost:8501
```

---

## 6. Recommended Pre-Run Validation

Before classroom use, deployment, or GitHub upload, run:

```bash
python validate_project.py
```

The validator checks:

- Required files
- Python syntax
- JSON validity
- Duplicate literal Streamlit widget keys
- Streamlit form submit-button issues
- Required dependencies in `requirements.txt`

Expected result:

```text
All validation checks passed.
```

---

## 7. Using the App

1. Open the app using `streamlit run app.py`.
2. Select a studio from the sidebar.
3. Fill in the guided fields or use default examples.
4. Click **Generate Prompt**.
5. Edit the generated prompt if required.
6. Copy, download, or save it to the local prompt library.
7. Use **My Prompt Library** to search, edit, export, or import saved prompts.
8. Use **Health Check** before demos or deployment.

---

## 8. Local Storage

Saved prompts are stored in:

```text
data/saved_prompts.json
```

This file remains local to your machine. No cloud storage or external API is used.

The app now includes safer JSON handling. If a local JSON file becomes corrupted, the app attempts to preserve a backup and continue with defaults.

---

## 9. File Upload Support

Supported upload types:

| Type | Use |
|---|---|
| `.txt` | Direct text extraction |
| `.pdf` | Extracted using `pypdf`, with optional `pdfplumber` fallback |
| `.docx` | Extracted using `python-docx`, with optional `docx2txt` fallback |

For scanned PDFs, OCR is not included. Convert the scanned PDF to selectable text before upload.

---

## 10. Streamlit Community Cloud Deployment

1. Push the project folder to GitHub.
2. Go to Streamlit Community Cloud.
3. Create a new app.
4. Select the repository.
5. Set the main file path as:

```text
app.py
```

6. Use the included `requirements.txt` and `.streamlit/config.toml`.
7. Deploy.

No secrets are required because the app uses no paid APIs.

---

## 11. Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: streamlit` | Dependencies not installed | Run `pip install -r requirements.txt` |
| App opens but upload parsing fails | Missing parser package | Run `pip install pypdf python-docx` |
| PDF uploads return blank text | Scanned/image-only PDF | Use OCR externally or paste text manually |
| Saved prompts disappear | Running from a non-writable folder | Move project to a writable directory |
| Streamlit page error | Module-level issue | Open **Health Check** and run `python validate_project.py` |
| Port already in use | Another Streamlit app is running | Run `streamlit run app.py --server.port 8502` |

---

## 12. Production Upgrade Summary

This version includes:

- App-level error handling so one broken page does not crash the whole app.
- Health Check page for production-readiness diagnostics.
- Offline validator script.
- Safer PDF/DOCX/TXT extraction helper.
- Safer HTML escaping in previews.
- Safer clipboard-copy handling.
- TXT, Markdown, and DOCX export options.
- Responsive CSS for classroom/projector use.
- Streamlit deployment configuration.
- Improved README and changelog.

---

## 13. Customisation

| Task | File |
|---|---|
| Add dropdown/sample values | `data/sample_inputs.json` |
| Add or edit base prompt templates | `data/prompt_templates.json` |
| Change theme/CSS | `modules/utils.py` → `apply_css()` |
| Add a new studio | Create a new module in `modules/`, import it in `app.py`, and add it to `PAGES` and `ROUTES` |
| Change Streamlit theme | `.streamlit/config.toml` |

---

## 14. Notes and Limitations

- The app generates prompts, not direct AI responses.
- It does not include OCR for scanned PDFs.
- It does not require API keys.
- It does not use a database; all storage is JSON-based and local.
- DOCX export requires `python-docx`, which is included in `requirements.txt`.

---

## 15. Credits

**Created by:** Dr Alok Tiwari  
**Institution:** Goa Institute of Management, Goa, India  
**Purpose:** Academic, research, teaching, and professional productivity enhancement

Copyright © Dr Alok Tiwari. All rights reserved.
