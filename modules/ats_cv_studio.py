"""
ATS CV Score Improver Studio
"""

import streamlit as st
from modules.utils import (
    apply_css, load_sample_inputs, section_header,
    prompt_output_section, global_sidebar_fields, info_card, file_upload_field,
    studio_tabs, go_to_output)


def build_prompt(inputs: dict, settings: dict) -> str:
    prompt = f"""You are an expert ATS (Applicant Tracking System) optimisation specialist, HR technology consultant, and professional CV writer.

TARGET ROLE: {inputs['target_role']}
INDUSTRY: {inputs['industry']}
COUNTRY: {inputs['country']}
DESIRED ATS SCORE: {inputs['desired_score']}%
PRESERVE ACADEMIC STYLE: {inputs['preserve_academic']}
COMPRESS CV: {inputs['compress']}
FORMAT PREFERENCE: {inputs['cv_format']}

JOB DESCRIPTION:
{inputs['job_description'] if inputs['job_description'].strip() else "[Paste the job description here before using this prompt]"}

EXISTING CV:
{inputs['existing_cv'] if inputs['existing_cv'].strip() else "[Paste the existing CV text here before using this prompt]"}

PERFORM THE FOLLOWING ATS OPTIMISATION ANALYSIS AND REWRITE:

1. ESTIMATED CURRENT ATS SCORE
   - Provide a percentage estimate with clear reasoning
   - List the main factors reducing the current score

2. MISSING HIGH-VALUE KEYWORDS
   Present as a table:
   | Keyword / Phrase | Priority (High/Med/Low) | Recommended Section |

3. WEAK SECTIONS ANALYSIS
   - Identify the 3–5 weakest sections with specific explanations
   - Explain why ATS systems penalise these sections

4. IMPROVED PROFESSIONAL SUMMARY
   - Rewrite as a 4–6 line keyword-dense summary
   - Lead with years of experience, domain, and top 2 credentials
   - Incorporate the highest-frequency JD keywords naturally

5. IMPROVED SKILLS SECTION
   - Reorganise into categories (Technical, Analytical, Leadership, Domain)
   - Ensure all JD-required skills appear verbatim

6. IMPROVED EXPERIENCE BULLETS (for top 3 positions)
   - Rewrite each bullet using: Action Verb + Task + Quantified Outcome
   - Embed relevant keywords naturally
   - Remove passive voice, vague claims, and duty-listing language

7. KEYWORD PLACEMENT STRATEGY TABLE
   | Keyword | Original Location | Recommended Location | Frequency |

8. BEFORE–AFTER BULLET COMPARISON TABLE
   | # | Original Bullet | Improved Bullet | Improvement Reason |
   (Provide 5 examples covering different roles/responsibilities)

9. FINAL ATS-OPTIMISED CV STRUCTURE
   - Recommended section order for {inputs['cv_format']} format
   - File format recommendation (PDF vs DOCX for this context)
   - Header and font guidance for ATS parsing

10. FORMATTING COMPLIANCE TIPS
    - Specific formatting elements to add or remove
    - Table, column, and graphic usage guidance for ATS systems
    - Header formatting best practices

SPECIAL REQUIREMENTS:
{"- Preserve academic publications section, conference presentations, and research profile structure." if inputs['preserve_academic'] else "- Prioritise industry-facing language and quantified business impact over academic framing."}
{"- Compress the CV to 2 pages maximum while retaining critical impact statements." if inputs['compress'] else "- Maintain the current CV length while improving density and relevance."}

OUTPUT FORMAT: {settings['output_format']}
TONE: {settings['tone']}

[Prompt framework authored by {settings['author']}]"""

    return prompt


def render():
    apply_css()
    sample = load_sample_inputs()
    settings = global_sidebar_fields(sample, key_prefix="ats")

    st.markdown('<div class="page-title">📄 ATS CV Score Improver</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Generate a prompt to analyse, score, and rewrite your CV for ATS systems</div>', unsafe_allow_html=True)

    active = studio_tabs("ats")

    if active == "input":
        section_header("Role & Context", "🎯")
        col1, col2 = st.columns(2)
        with col1:
            target_role   = st.text_input("Target Role", value="Assistant Professor (AI/ML) — IIM", key="ats_role")
            industry      = st.selectbox("Industry", ["Academia / Higher Education", "Healthcare & Biotech",
                "Finance & FinTech", "Technology / IT", "Consulting", "Manufacturing", "Government / PSU",
                "Research & Development", "E-Commerce", "Other"], key="ats_ind")
        with col2:
            country       = st.text_input("Country", value="India", key="ats_country")
            desired_score = st.slider("Desired ATS Score (%)", 70, 99, 90, key="ats_score")
            cv_format     = st.selectbox("Preferred CV Format", ["Reverse Chronological", "Functional", "Hybrid / Combination", "Academic CV"], key="ats_fmt")

        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            preserve_academic = st.checkbox("Preserve Academic Style", value=True, key="ats_acad")
        with col_opt2:
            compress = st.checkbox("Compress to 2 Pages", value=False, key="ats_comp")

        section_header("Job Description", "📋")
        info_card("Upload a PDF/DOCX/TXT file or paste the JD for targeted ATS keyword extraction.")
        job_description = file_upload_field(
            label="Job Description",
            key="ats_jd_file",
            fallback_key="ats_jd",
            placeholder="Paste the job description here...",
            height=180,
        )

        section_header("Your Existing CV", "📄")
        existing_cv = file_upload_field(
            label="Existing CV",
            key="ats_cv_file",
            fallback_key="ats_cv",
            placeholder="Paste your current CV content here (plain text, no formatting needed)...",
            height=220,
        )

        if st.button("🚀 Generate Prompt", use_container_width=True, key="ats_gen"):
            inputs = dict(
                target_role=target_role, industry=industry, country=country,
                desired_score=desired_score, cv_format=cv_format,
                preserve_academic=preserve_academic, compress=compress,
                job_description=job_description, existing_cv=existing_cv,
            )
            st.session_state["ats_prompt"] = build_prompt(inputs, settings)
            go_to_output("ats")

    if active == "output":
        if st.session_state.get("ats_prompt"):
            prompt_output_section(st.session_state["ats_prompt"], key_prefix="ats", category="ATS CV Improver")
        else:
            st.info("Fill in the Inputs tab and click 'Generate Prompt'.")
