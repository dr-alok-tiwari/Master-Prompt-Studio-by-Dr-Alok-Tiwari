"""
About page
"""

import streamlit as st
from modules.utils import apply_css, section_header


def render():
    apply_css()
    st.markdown('<div class="page-title">ℹ️ About This Studio</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        section_header("Master Productivity Prompt Studio", "🧠")
        st.markdown("""
        This application is a **fully offline, API-free prompt generation studio** designed for researchers,
        educators, and professionals who regularly work with AI language models.

        Rather than generating AI responses directly, this tool helps you craft *precisely structured master prompts*
        — the kind of high-quality, detailed instructions that consistently produce reliable, usable AI outputs.

        The studio covers the full spectrum of academic and professional productivity workflows:
        from research paper analysis and course design, to job applications, ATS optimisation, and Streamlit app development.
        """)

        section_header("Creator", "👨‍🏫")
        st.markdown("""
        **Dr Alok Tiwari**
        Assistant Professor — Big Data Analytics
        Goa Institute of Management (GIM), Goa, India

        PhD in Biomedical Engineering, IIT-BHU (2023)
        Specialisation: Medical Imaging AI, Transfer Learning, Healthcare Analytics

        *Research | Teaching | Executive Education | AI Applications*
        """)

        section_header("Technical Notes", "🔧")
        st.markdown("""
        - **Framework:** Streamlit (Python)
        - **Storage:** Local JSON files — no database, no cloud sync
        - **API Dependencies:** None — fully offline
        - **External AI calls:** None
        - **Paid services required:** None
        - **Tested on:** Python 3.10+, Streamlit 1.28+
        """)

    with col2:
        section_header("Version", "📋")
        st.markdown("""
        | Property | Value |
        |---|---|
        | Version | 1.0.0 |
        | Release | 2025 |
        | Framework | Streamlit |
        | Python | ≥ 3.10 |
        | Modules | 12 studios |
        | Storage | Local JSON |
        """)

        section_header("Quick Links", "🔗")
        st.markdown("""
        - 📖 [Streamlit Docs](https://docs.streamlit.io)
        - 🐍 [Python Downloads](https://python.org)
        - 📄 [pip install guide](https://pip.pypa.io)
        """)

    st.markdown("---")
    st.markdown(
        """<div class="footer-note">
        Copyright © Dr Alok Tiwari | Master Productivity Prompt Studio | All rights reserved<br>
        Built for academic, research, and professional productivity workflows.
        </div>""",
        unsafe_allow_html=True,
    )
