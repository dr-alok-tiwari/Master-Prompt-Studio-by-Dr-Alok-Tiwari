"""
Master Productivity Prompt Studio
Created by: Dr Alok Tiwari
Goa Institute of Management

Run with: streamlit run app.py
"""

import streamlit as st
import sys
import os

# Ensure modules directory is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ─── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Master Productivity Prompt Studio",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "Master Productivity Prompt Studio — Created by Dr Alok Tiwari",
    },
)

# ─── Imports ───────────────────────────────────────────────────────────────────
from modules import (
    home,
    research_prompt_studio,
    handbook_studio,
    course_profile_studio,
    job_application_studio,
    ats_cv_studio,
    teaching_content_studio,
    quiz_case_studio,
    email_studio,
    research_productivity_studio,
    workflow_studio,
    streamlit_app_prompt_studio,
    custom_prompt_builder,
    prompt_library,
    health_check,
    about,
)
from modules.utils import apply_css, ensure_data_files

ensure_data_files()

# ─── Session state defaults ────────────────────────────────────────────────────
_defaults = {
    "rps_prompt": "", "hb_prompt": "", "cp_prompt": "", "ja_prompt": "",
    "ats_prompt": "", "tc_prompt": "", "qc_prompt": "", "em_prompt": "",
    "rp_prompt": "", "wf_prompt": "", "sa_prompt": "", "cpb_prompt": "",
    "rps_show_save": False, "hb_show_save": False, "cp_show_save": False,
    "ja_show_save": False, "ats_show_save": False, "tc_show_save": False,
    "qc_show_save": False, "em_show_save": False, "rp_show_save": False,
    "wf_show_save": False, "sa_show_save": False, "cpb_show_save": False,
    # Navigation intent — home buttons write here; app.py reads before widget creation
    "_nav_target": None,
}
for key, val in _defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ─── Sidebar navigation ────────────────────────────────────────────────────────
apply_css()

PAGES = {
    "🏠 Home": "home",
    "🔬 Research Paper Intelligence": "research",
    "📖 Handbook Generator": "handbook",
    "🎓 Course Profile Generator": "course_profile",
    "💼 Job Application Materials": "job_application",
    "📄 ATS CV Score Improver": "ats_cv",
    "📚 Teaching Content Generator": "teaching",
    "❓ Quiz & Case Study Generator": "quiz_case",
    "✉️ Professional Email Generator": "email",
    "🧪 Research Productivity Generator": "research_productivity",
    "⚙️ Productivity Workflow Generator": "workflow",
    "💻 Streamlit App Prompt Generator": "streamlit_app",
    "🧩 Custom Prompt Builder": "custom_prompt",
    "📚 My Prompt Library": "prompt_library",
    "🩺 Health Check": "health_check",
    "ℹ️ About": "about",
}
PAGE_LABELS = list(PAGES.keys())

# Resolve navigation intent BEFORE the radio widget is instantiated
_nav_target = st.session_state.pop("_nav_target", None)
if _nav_target and _nav_target in PAGE_LABELS:
    _default_index = PAGE_LABELS.index(_nav_target)
else:
    _default_index = st.session_state.get("_nav_index", 0)

st.sidebar.markdown(
    """
    <div style="text-align:center;padding:16px 0 8px;">
        <div style="font-size:2.2rem;">🧠</div>
        <div style="font-family:'Georgia',serif;font-size:1.05rem;
             color:#F5E6D3;font-weight:700;line-height:1.4;letter-spacing:0.01em;">
            Master Productivity<br>Prompt Studio
        </div>
        <div style="font-size:0.78rem;color:#F5A623;margin-top:6px;font-weight:600;">
            Dr Alok Tiwari
        </div>
        <div style="font-size:0.7rem;color:#C8A882;margin-top:2px;">
            Goa Institute of Management
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

selected_label = st.sidebar.radio(
    "Navigate to",
    PAGE_LABELS,
    index=_default_index,
    label_visibility="collapsed",
    key="nav_radio",
)

# Persist the current index so normal sidebar clicks are remembered across reruns
st.session_state["_nav_index"] = PAGE_LABELS.index(selected_label)

page = PAGES[selected_label]

st.sidebar.markdown("---")
st.sidebar.markdown(
    """<div style="font-size:0.72rem;color:#C8A882;text-align:center;padding:6px 4px;">
    Copyright © Dr Alok Tiwari<br>
    <span style="color:#A08060;">All rights reserved</span>
    </div>""",
    unsafe_allow_html=True,
)

# ─── Page routing ──────────────────────────────────────────────────────────────
ROUTES = {
    "home": home.render,
    "research": research_prompt_studio.render,
    "handbook": handbook_studio.render,
    "course_profile": course_profile_studio.render,
    "job_application": job_application_studio.render,
    "ats_cv": ats_cv_studio.render,
    "teaching": teaching_content_studio.render,
    "quiz_case": quiz_case_studio.render,
    "email": email_studio.render,
    "research_productivity": research_productivity_studio.render,
    "workflow": workflow_studio.render,
    "streamlit_app": streamlit_app_prompt_studio.render,
    "custom_prompt": custom_prompt_builder.render,
    "prompt_library": prompt_library.render,
    "health_check": health_check.render,
    "about": about.render,
}

try:
    ROUTES.get(page, home.render)()
except Exception as exc:
    st.error("This page could not be rendered safely. The app is still running.")
    with st.expander("Developer details", expanded=False):
        st.exception(exc)
    st.info("Open the 🩺 Health Check page, run `python validate_project.py`, or restart Streamlit after installing requirements.")
