"""
Home page — Master Prompt Studio
"""

import streamlit as st
from modules.utils import apply_css, load_saved_prompts

# Map module card labels → sidebar radio keys (must match app.py PAGES keys exactly)
NAV_MAP = {
    "Research Paper Intelligence":  "🔬 Research Paper Intelligence",
    "Handbook Generator":           "📖 Handbook Generator",
    "Course Profile Generator":     "🎓 Course Profile Generator",
    "Job Application Materials":    "💼 Job Application Materials",
    "ATS CV Score Improver":        "📄 ATS CV Score Improver",
    "Teaching Content Generator":   "📚 Teaching Content Generator",
    "Quiz & Case Study Generator":  "❓ Quiz & Case Study Generator",
    "Professional Email Generator": "✉️ Professional Email Generator",
    "Research Productivity":        "🧪 Research Productivity Generator",
    "Productivity Workflow":        "⚙️ Productivity Workflow Generator",
    "Streamlit App Prompt":         "💻 Streamlit App Prompt Generator",
    "Custom Prompt Builder":        "🧩 Custom Prompt Builder",
}


def render():
    apply_css()

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center;padding:36px 20px 16px;">
            <div style="font-size:3.2rem;margin-bottom:8px;">🧠</div>
            <div class="page-title" style="font-size:2.5rem;text-align:center;">
                Master Prompt Studio
            </div>
            <div class="page-subtitle" style="font-size:1.05rem;max-width:640px;
                 margin:8px auto 0;text-align:center;color:#5A5A6A;">
                A fully offline, API-free prompt-generation studio for researchers,
                educators, and professionals. Craft precise master prompts in seconds.
            </div>
            <div style="margin-top:10px;font-size:0.88rem;color:#C4500F;font-weight:600;">
                Created by Dr Alok Tiwari &nbsp;|&nbsp; Goa Institute of Management, Goa
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Stats row ─────────────────────────────────────────────────────────────
    saved = load_saved_prompts()
    stats = [
        ("12", "Prompt Studios"),
        (str(len(saved)), "Saved Prompts"),
        ("100+", "Pre-built Templates"),
        ("0", "API Keys Required"),
    ]
    cols = st.columns(4)
    for col, (val, label) in zip(cols, stats):
        with col:
            st.markdown(
                f"""<div class="metric-card">
                    <div class="metric-value">{val}</div>
                    <div class="metric-label">{label}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── How it works ──────────────────────────────────────────────────────────
    st.markdown(
        '<div style="font-family:\'Playfair Display\',serif;font-size:1.5rem;'
        'color:#C4500F;font-weight:700;margin-bottom:12px;">🔄 How It Works</div>',
        unsafe_allow_html=True,
    )
    steps = [
        ("1️⃣", "Select a Studio",       "Pick from 12 specialised prompt modules below or in the sidebar."),
        ("2️⃣", "Fill or Select Inputs", "Use pre-filled examples or type your own values."),
        ("3️⃣", "Generate Prompt",        "Click Generate Prompt to build your master prompt instantly."),
        ("4️⃣", "Edit & Refine",          "Edit the generated prompt directly in the output panel."),
        ("5️⃣", "Save & Export",          "Save to your library, download as TXT or Markdown."),
    ]
    cols = st.columns(5)
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(
                f"""<div class="studio-card" style="text-align:center;min-height:155px;padding:16px 14px;">
                    <div style="font-size:1.7rem;">{num}</div>
                    <div style="font-weight:700;color:#C4500F;margin:6px 0 4px;font-size:0.9rem;">{title}</div>
                    <div style="font-size:0.8rem;color:#5A5A6A;line-height:1.4;">{desc}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Clickable Studio Cards ─────────────────────────────────────────────────
    st.markdown(
        '<div style="font-family:\'Playfair Display\',serif;font-size:1.5rem;'
        'color:#C4500F;font-weight:700;margin-bottom:4px;">🛠 Available Prompt Studios</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="color:#5A5A6A;font-size:0.9rem;margin-bottom:16px;">'
        'Click any <b>Open</b> button to launch that studio directly.</div>',
        unsafe_allow_html=True,
    )

    modules = [
        ("🔬", "Research Paper Intelligence", "Intake, contradiction finding, gap scanning, synthesis"),
        ("📖", "Handbook Generator",           "Multi-level handbooks with examples, cases, glossary"),
        ("🎓", "Course Profile Generator",     "CLOs, PLO mapping, session plans, rubrics"),
        ("💼", "Job Application Materials",    "Cover letters, research & teaching statements"),
        ("📄", "ATS CV Score Improver",        "Keyword analysis, bullet rewrites, ATS scoring"),
        ("📚", "Teaching Content Generator",   "Slide outlines, scripts, activities, exit tickets"),
        ("❓", "Quiz & Case Study Generator",  "MCQs, scenarios, Bloom's mapping, rubrics"),
        ("✉️", "Professional Email Generator", "6 tone variants, follow-ups, subject lines"),
        ("🧪", "Research Productivity",        "Problem statements, frameworks, abstracts, outlines"),
        ("⚙️", "Productivity Workflow",        "Step-by-step systems, tools, checklists, automations"),
        ("💻", "Streamlit App Prompt",         "Full project structure prompts for Streamlit apps"),
        ("🧩", "Custom Prompt Builder",        "RCTOFE and other frameworks, fully customisable"),
    ]

    for row_start in range(0, len(modules), 3):
        cols = st.columns(3)
        for col, (icon, name, desc) in zip(cols, modules[row_start: row_start + 3]):
            with col:
                st.markdown(
                    f"""<div style="background:#FFFFFF;border:1px solid #EDE0D0;border-radius:12px;
                        padding:14px 16px 12px;margin-bottom:4px;
                        box-shadow:0 2px 8px rgba(232,101,26,0.07);">
                        <div style="font-size:1.45rem;margin-bottom:4px;">{icon}</div>
                        <div style="font-weight:700;color:#C4500F;font-size:0.92rem;margin-bottom:3px;">{name}</div>
                        <div style="font-size:0.8rem;color:#5A5A6A;line-height:1.35;margin-bottom:10px;">{desc}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
                nav_key = NAV_MAP.get(name)
                btn_key = f"home_nav_{name.replace(' ', '_').replace('&', 'and').replace('/', '_')}"
                if st.button(f"Open {icon}", key=btn_key, use_container_width=True):
                    if nav_key:
                        st.session_state["_nav_target"] = nav_key
                        st.rerun()

        st.markdown("<div style='margin-bottom:4px;'></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Suggested Use Cases ───────────────────────────────────────────────────
    st.markdown(
        '<div style="font-family:\'Playfair Display\',serif;font-size:1.5rem;'
        'color:#C4500F;font-weight:700;margin-bottom:12px;">💡 Suggested Use Cases</div>',
        unsafe_allow_html=True,
    )
    use_cases = [
        "Analyse 10 papers for your literature review with one structured prompt",
        "Generate a complete course profile for a new PGDM elective in minutes",
        "Improve your CV's ATS score before applying to IIM faculty positions",
        "Create a 16-session teaching handbook for Big Data Analytics",
        "Build a Streamlit quiz app for your students — prompt it in seconds",
        "Draft a targeted cover letter + research statement for IIT applications",
        "Design a full research productivity workflow for your PhD scholars",
        "Generate MCQs with Bloom's mapping for end-term assessments",
    ]
    cols = st.columns(2)
    for i, uc in enumerate(use_cases):
        with cols[i % 2]:
            st.markdown(
                f"""<div style="background:#FFF3E8;border-left:3px solid #E8651A;
                border-radius:6px;padding:9px 13px;margin:5px 0;font-size:0.88rem;
                color:#2C2C2C;line-height:1.4;">✅ {uc}</div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Library quick-access ──────────────────────────────────────────────────
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown(
            """<div style="background:linear-gradient(135deg,#FFF3E8,#FDE8D0);
            border:1.5px solid #E8651A;border-radius:10px;padding:16px 20px;text-align:center;">
            <div style="font-size:1.05rem;font-weight:700;color:#C4500F;margin-bottom:6px;">
                📚 My Prompt Library
            </div>
            <div style="font-size:0.85rem;color:#5A5A6A;">
                All saved prompts are stored locally. Export, import, search, and manage
                your entire collection from the Prompt Library module.
            </div>
            </div>""",
            unsafe_allow_html=True,
        )
        st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
        if st.button("📚 Open Prompt Library", use_container_width=True, key="home_goto_library"):
            st.session_state["_nav_target"] = "📚 My Prompt Library"
            st.rerun()

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown(
        """<div class="footer-note">
        Copyright © Dr Alok Tiwari &nbsp;|&nbsp; Master Prompt Studio
        &nbsp;|&nbsp; All rights reserved
        </div>""",
        unsafe_allow_html=True,
    )
