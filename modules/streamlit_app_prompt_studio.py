"""
Streamlit App Prompt Generator Studio
"""

import streamlit as st
from modules.utils import (
    apply_css, load_sample_inputs, section_header,
    prompt_output_section, global_sidebar_fields,
    studio_tabs, go_to_output)


def build_prompt(inputs: dict, settings: dict) -> str:
    features_list = "\n".join([f"- {f}" for f in inputs.get("features", [])])

    prompt = f"""You are an expert Streamlit application architect, UI/UX designer, and senior Python developer. Build a complete, production-quality Streamlit application as specified below.

APP SPECIFICATIONS:
- App Title: {inputs['app_title']}
- App Purpose: {inputs['app_purpose']}
- Target Users: {inputs['target_users']}
- UI Theme: {inputs['ui_theme']}
- Modules / Features: {inputs['modules']}

REQUIRED FEATURES:
{features_list if features_list else "- Standard interactive UI\n- Download functionality\n- Error handling"}

GENERATE A COMPLETE STREAMLIT PROJECT WITH THE FOLLOWING STRUCTURE:

FOLDER ARCHITECTURE:
{inputs['app_title'].lower().replace(" ", "_")}/
├── app.py                    (main entry point with sidebar navigation)
├── requirements.txt          (all dependencies, pinned where critical)
├── README.md                 (detailed installation and usage guide)
├── data/
│   ├── sample_data.csv       (realistic sample data if needed)
│   └── config.json           (app configuration)
└── modules/
    └── [one .py file per feature module]

FOR app.py, GENERATE:
- Sidebar navigation (st.sidebar with radio or selectbox)
- Page routing to each module
- Global CSS styling for {inputs['ui_theme']} theme
- Session state initialisation
- Error handling wrapper

FOR EACH MODULE, GENERATE COMPLETE CODE:
- Input widgets (sliders, dropdowns, text areas, file uploaders)
- Processing logic (pure Python, no external API calls)
- Output display (st.dataframe, st.plotly_chart, st.markdown, st.metric)
- Download buttons (CSV, TXT, PNG where applicable)
- Help tooltips and validation messages
- Responsive layout (st.columns, st.expander)

REQUIREMENTS.TXT must include:
streamlit>=1.28.0
pandas
{"plotly" if "Charts" in str(inputs.get("features", [])) else ""}
{"Pillow" if "Image" in str(inputs.get("features", [])) else ""}
python-dateutil

DESIGN STANDARDS:
- No paid API dependencies — zero external AI calls
- No API keys required
- Readable on a classroom projector (font size ≥ 14px)
- Mobile-friendly layout where possible
- Progress indicators for any processing step > 1 second
- Clear section headings and intuitive navigation
- Success / warning / error messages for all user actions

README.md must include:
1. Project title and purpose
2. Features list
3. Installation (pip install -r requirements.txt)
4. Running (streamlit run app.py)
5. Module-by-module usage guide
6. Customisation instructions
7. Credits: Created by {settings['author']}

OUTPUT FORMAT: {settings['output_format']}
TONE: {settings['tone']}

Generate all code files completely — do not truncate or use placeholder comments."""

    return prompt


def render():
    apply_css()
    sample = load_sample_inputs()
    settings = global_sidebar_fields(sample, key_prefix="sa")

    st.markdown('<div class="page-title">💻 Streamlit App Prompt Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Generate a complete Streamlit project prompt — from folder structure to full code</div>', unsafe_allow_html=True)

    active = studio_tabs("sa")

    if active == "input":
        section_header("App Identity", "🖥️")
        col1, col2 = st.columns(2)
        with col1:
            app_title   = st.text_input("App Title", value="Healthcare Analytics Dashboard", key="sa_title")
            target_users= st.selectbox("Target Users", sample.get("target_audiences", []), key="sa_users")
        with col2:
            ui_theme    = st.selectbox("UI Theme", ["Professional Blue", "Saffron / Warm", "Dark / Minimal",
                                                    "Academic / Clean White", "Healthcare Green", "Data Science Purple"], key="sa_theme")
            modules     = st.text_area("Modules / Features Needed (one per line)", height=80, key="sa_mods",
                                       value="Patient data dashboard\nDisease prediction model\nData upload and preprocessing\nInteractive visualisations")

        app_purpose = st.text_area("App Purpose (2–3 sentences)", height=80, key="sa_purpose",
                                   value="A teaching tool for PGDM-HCM students to explore healthcare analytics concepts through interactive dashboards and prediction models.")

        section_header("Feature Checkboxes", "✅")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            q_quizzes   = st.checkbox("Interactive Quizzes",    key="sa_quiz")
            q_downloads = st.checkbox("Download Buttons",       key="sa_dl", value=True)
            q_charts    = st.checkbox("Charts / Visualisations",key="sa_charts", value=True)
        with col_b:
            q_samples   = st.checkbox("Sample Datasets",        key="sa_samp", value=True)
            q_upload    = st.checkbox("File Upload Support",    key="sa_up", value=True)
            q_filter    = st.checkbox("Interactive Filters",    key="sa_filt", value=True)
        with col_c:
            q_storage   = st.checkbox("Local JSON Storage",     key="sa_stor")
            q_readme    = st.checkbox("README.md",              key="sa_readme", value=True)
            q_zip       = st.checkbox("ZIP Package Instructions",key="sa_zip")

        if st.button("🚀 Generate Prompt", use_container_width=True, key="sa_gen"):
            if not app_title.strip():
                st.warning("Please enter an app title.")
            else:
                features = []
                if q_quizzes:   features.append("Interactive quizzes with score tracking")
                if q_downloads: features.append("Download buttons for CSV, TXT, and Markdown outputs")
                if q_charts:    features.append("Charts and visualisations (Plotly / Altair)")
                if q_samples:   features.append("Pre-loaded sample datasets for demo mode")
                if q_upload:    features.append("File upload support (CSV, XLSX, PDF)")
                if q_filter:    features.append("Interactive sidebar filters and controls")
                if q_storage:   features.append("Local JSON-based data persistence")
                if q_readme:    features.append("Detailed README.md with installation guide")
                if q_zip:       features.append("ZIP packaging instructions for distribution")

                inputs = dict(
                    app_title=app_title, app_purpose=app_purpose,
                    target_users=target_users, ui_theme=ui_theme,
                    modules=modules, features=features,
                )
                st.session_state["sa_prompt"] = build_prompt(inputs, settings)
                go_to_output("sa")

    if active == "output":
        if st.session_state.get("sa_prompt"):
            prompt_output_section(st.session_state["sa_prompt"], key_prefix="sa", category="Streamlit App Prompt Generator")
        else:
            st.info("Fill in the Inputs tab and click 'Generate Prompt'.")
