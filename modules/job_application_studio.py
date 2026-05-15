"""
Job Application Material Generator Studio
"""

import streamlit as st
from modules.utils import (
    apply_css, load_sample_inputs, section_header,
    prompt_output_section, global_sidebar_fields, info_card, file_upload_field,
    studio_tabs, go_to_output,
    template_upload_section, format_template_instruction)


def build_prompt(inputs: dict, settings: dict) -> str:
    template_block = format_template_instruction(inputs.get("template_text", ""), label="application package")
    academic_sections = ""
    if inputs.get("is_academic"):
        template_block = format_template_instruction(inputs.get("template_text", ""), label="application package")
    academic_sections = """
8. RESEARCH STATEMENT (Academic roles)
   - Current research programme and its significance
   - Methodological identity
   - Key publications and their impact
   - Future research agenda (3–5 years)
   - Funding ambitions

9. TEACHING STATEMENT (Academic roles)
   - Teaching philosophy (genuine, not formulaic)
   - Courses you can teach and those you aspire to develop
   - Pedagogical innovations and evidence of effectiveness
   - Student mentoring philosophy"""

    required_docs = ", ".join(inputs.get("required_docs", ["Cover Letter", "CV Summary"]))

    prompt = f"""You are an expert career strategist, academic recruitment consultant, and professional writer. Generate a comprehensive job application package for the following opportunity.

JOB DETAILS:
- Job Title: {inputs['job_title']}
- Organisation: {inputs['organization']}
- Country: {inputs['country']}
- Application Type: {inputs['application_type']}
- Required Documents: {required_docs}

JOB DESCRIPTION:
{inputs['job_description'] if inputs['job_description'].strip() else "[Paste the full job description here before using this prompt]"}

APPLICANT PROFILE:
{inputs['applicant_profile'] if inputs['applicant_profile'].strip() else "[Paste the applicant's CV or profile summary here before using this prompt]"}

GENERATE THE FOLLOWING COMPLETE APPLICATION PACKAGE:

1. ROLE-FIT ANALYSIS
   - Compatibility assessment (estimate a match percentage with clear reasoning)
   - Key alignment points between the applicant's profile and the JD
   - Areas of strong fit

2. STRENGTH MAPPING
   - Top 5 strengths directly aligned to the job description
   - For each: specific evidence from the applicant's profile

3. GAP ANALYSIS
   - Honest identification of gaps or areas not covered by the profile
   - Strategic framing suggestions for each gap

4. ATS-OPTIMISED CV SUMMARY
   - 4–6 lines, keyword-rich, tailored to this specific role
   - Incorporate high-frequency terms from the JD

5. COVER LETTER ({settings['tone']} tone, {settings['length']} length)
   - Opening: Hook that connects the applicant's identity to the role
   - Body: Evidence-backed case for fit (specific achievements, not generic claims)
   - Closing: Clear, confident call-to-action
   - Suitable for {inputs['country']} academic/professional conventions
{academic_sections}

{len("8. RESEARCH STATEMENT" if inputs.get("is_academic") else "7")}. SELECTION CRITERIA RESPONSES
   - Structured STAR-format responses for each key selection criterion

{len("10." if inputs.get("is_academic") else "8.")} LINKEDIN CONNECTION MESSAGE
   - Under 100 words, warm and professional

{len("11." if inputs.get("is_academic") else "9.")} HR / PANEL FOLLOW-UP EMAIL
   - Post-application follow-up, 72-hour version

{len("12." if inputs.get("is_academic") else "10.")} LIKELY INTERVIEW QUESTIONS (10)
   - With suggested answer frameworks (not scripted answers)

{len("13." if inputs.get("is_academic") else "11.")} QUESTIONS TO ASK THE EMPLOYER (5)
   - Insightful, role-specific questions that demonstrate genuine interest

{len("14." if inputs.get("is_academic") else "12.")} FINAL APPLICATION CHECKLIST
   - Document-by-document confirmation list before submission

STRICT PROFESSIONAL STANDARDS:
- Do NOT invent publications, awards, projects, or achievements not stated in the applicant profile.
- Do NOT use generic filler phrases like "passionate team player" or "results-driven professional."
- Tailor every element specifically to {inputs['organization']} and the role as described.
- Maintain {settings['tone']} tone throughout.
- Flag wherever the applicant needs to insert specific details.

{template_block}
[Prompt framework authored by {settings['author']}]"""

    return prompt


def render():
    apply_css()
    sample = load_sample_inputs()
    settings = global_sidebar_fields(sample, key_prefix="ja")

    st.markdown('<div class="page-title">💼 Job Application Material Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Generate a complete, tailored job application package prompt</div>', unsafe_allow_html=True)

    active = studio_tabs("ja")

    if active == "input":
        section_header("Role Details", "🏢")
        col1, col2 = st.columns(2)
        with col1:
            job_title   = st.text_input("Job Title", value="Assistant Professor — AI/ML", key="ja_title")
            organization= st.text_input("Organisation", value="IIM Lucknow", key="ja_org")
        with col2:
            country     = st.text_input("Country", value="India", key="ja_country")
            application_type = st.selectbox("Application Type", ["Academic Faculty", "Industry / Corporate", "Government / PSU", "Research / Postdoc", "Startup / SME"], key="ja_type")

        is_academic = st.checkbox("This is an academic role (adds Research & Teaching Statements)", value=True, key="ja_acad")

        required_docs = st.multiselect(
            "Required Documents",
            ["Cover Letter", "CV Summary", "Research Statement", "Teaching Statement",
             "Selection Criteria", "Reference List", "Publication List", "LinkedIn Message"],
            default=["Cover Letter", "CV Summary", "Research Statement", "Teaching Statement"],
            key="ja_docs"
        )

        section_header("Job Description", "📋")
        info_card("Upload a PDF/DOCX/TXT file or paste the full JD below — the more detail, the better the prompt output.")
        job_description = file_upload_field(
            label="Job Description",
            key="ja_jd_file",
            fallback_key="ja_jd",
            placeholder="Paste the full job description here...",
            height=200,
        )

        section_header("Applicant Profile / CV", "👤")
        applicant_profile = file_upload_field(
            label="CV / Applicant Profile",
            key="ja_profile_file",
            fallback_key="ja_profile",
            placeholder="Paste your CV or profile summary here...",
            height=200,
        )

        section_header("Application Template", "📐")
        template_text = template_upload_section(
            module_key="job_application",
            key_prefix="ja",
            label="Application",
            help_text="Attach the institution's official application form or selection criteria document.",
        )

        if st.button("🚀 Generate Prompt", use_container_width=True, key="ja_gen"):
            inputs = dict(
                job_title=job_title, organization=organization,
                country=country, application_type=application_type,
                is_academic=is_academic, required_docs=required_docs,
                job_description=job_description, applicant_profile=applicant_profile,
                template_text=template_text,
            )
            st.session_state["ja_prompt"] = build_prompt(inputs, settings)
            go_to_output("ja")

    if active == "output":
        if st.session_state.get("ja_prompt"):
            prompt_output_section(st.session_state["ja_prompt"], key_prefix="ja", category="Job Application Materials")
        else:
            st.info("Fill in the Inputs tab and click 'Generate Prompt'.")
