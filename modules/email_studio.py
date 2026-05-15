"""
Professional Email Generator Studio
"""

import streamlit as st
from modules.utils import (
    apply_css, load_sample_inputs, section_header,
    prompt_output_section, global_sidebar_fields, info_card, file_upload_field,
    studio_tabs, go_to_output)


def build_prompt(inputs: dict, settings: dict) -> str:
    versions = []
    if inputs.get("formal"):          versions.append("1. FORMAL VERSION\n   Highest formality, suitable for senior officials, VCs, deans, or government officers. Impeccable language, complete structure.")
    if inputs.get("warm_pro"):        versions.append("2. WARM PROFESSIONAL VERSION\n   Formal but personable — suitable for known contacts, collaborators, or faculty peers.")
    if inputs.get("concise"):         versions.append("3. CONCISE VERSION\n   Under 150 words, direct, action-oriented. No pleasantries beyond a brief opener.")
    if inputs.get("institutional"):   versions.append("4. INSTITUTIONAL VERSION\n   Appropriate for official letterhead correspondence or formal institutional communication.")
    if inputs.get("followup"):        versions.append("5. FOLLOW-UP VERSION\n   For situations where no reply has been received after 5 business days. Polite, non-pushy.")
    if inputs.get("reminder"):        versions.append("6. REMINDER VERSION\n   For a second follow-up (7–10 days after the first follow-up). Still respectful, with gentle urgency.")

    version_text = "\n\n".join(versions) if versions else "FORMAL VERSION and WARM PROFESSIONAL VERSION"

    prompt = f"""You are an expert professional communicator, institutional correspondence specialist, and academic writing consultant.

COMMUNICATION BRIEF:
- Purpose: {inputs['purpose']}
- Recipient: {inputs['recipient']}
- Recipient's Role / Relationship: {inputs['recipient_role']}
- Context: {inputs['context']}
- Primary Tone: {settings['tone']}
- Desired Length: {settings['length']}
- Sender: {settings['author']}

GENERATE THE FOLLOWING EMAIL VERSIONS:

{version_text}

FOR EACH VERSION, PROVIDE:
- Subject Line (clear, specific, not clickbait)
- Salutation (appropriate to relationship and formality)
- Opening (context-setting, purpose-stating)
- Body (core message, clearly structured)
- Closing (call-to-action, if any)
- Sign-off and signature block

ADDITIONAL REQUIREMENTS:
{"- Include a subject line A/B test option for each version" if inputs.get("ab_subject") else ""}
{"- Add a WhatsApp-compatible short version (under 80 words)" if inputs.get("whatsapp") else ""}

TONE STANDARDS FOR ALL VERSIONS:
- Polite and respectful throughout — never aggressive, demanding, or sycophantic
- Clear and unambiguous — no vague language or passive-aggressive phrasing
- Non-confrontational even when addressing a delay, problem, or difficult situation
- Suitable for Indian professional and academic institutional contexts
- No filler phrases like "Hope this finds you well" — open with substance

QUALITY CHECK:
Before finalising each version, verify:
□ Subject line is specific and informative
□ Purpose is clear within the first 2 sentences
□ No unnecessary pleasantries
□ Closing includes a clear next step or request
□ Appropriate level of formality for the relationship

[Communication framework by {settings['author']}]"""

    return prompt


def render():
    apply_css()
    sample = load_sample_inputs()
    settings = global_sidebar_fields(sample, key_prefix="em")

    st.markdown('<div class="page-title">✉️ Professional Email Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Generate polished, context-appropriate emails in multiple tone variants</div>', unsafe_allow_html=True)

    active = studio_tabs("em")

    if active == "input":
        section_header("Communication Details", "📧")
        col1, col2 = st.columns(2)
        with col1:
            purpose      = st.text_input("Email Purpose", value="Request for faculty seminar slot consideration", key="em_purpose")
            recipient    = st.text_input("Recipient Name / Role", value="Prof. XYZ, Chairperson — Faculty Search Committee", key="em_recip")
        with col2:
            recipient_role = st.selectbox("Relationship to Recipient",
                                          ["Senior academic / dean", "Peer / collaborator", "Industry professional",
                                           "Government official", "Journal editor", "Recruiter / HR", "Student",
                                           "Conference chair", "Unknown / cold contact"], key="em_rel")

        info_card("The more context you provide, the more tailored and effective the generated email prompt will be.")
        context = file_upload_field(
            label="Context / Background Document",
            key="em_ctx_file",
            fallback_key="em_ctx",
            placeholder="Describe the situation in 2–5 sentences. Or upload a relevant document (e.g. application acknowledgement, meeting notes, previous email)...",
            height=130,
        )

        section_header("Email Versions to Generate", "📋")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            formal      = st.checkbox("Formal Version",             value=True,  key="em_f")
            warm_pro    = st.checkbox("Warm Professional Version",   value=True,  key="em_wp")
        with col_b:
            concise     = st.checkbox("Concise Version",            value=True,  key="em_c")
            institutional= st.checkbox("Institutional Version",     value=False, key="em_i")
        with col_c:
            followup    = st.checkbox("Follow-Up Version",          value=True,  key="em_fu")
            reminder    = st.checkbox("Reminder Version",           value=False, key="em_r")

        col_extra1, col_extra2 = st.columns(2)
        with col_extra1:
            ab_subject  = st.checkbox("Subject Line A/B Test Options", value=False, key="em_ab")
        with col_extra2:
            whatsapp    = st.checkbox("WhatsApp Short Version",      value=False, key="em_wa")

        if st.button("🚀 Generate Prompt", use_container_width=True, key="em_gen"):
            if not purpose.strip():
                st.warning("Please describe the email purpose.")
            else:
                inputs = dict(
                    purpose=purpose, recipient=recipient, recipient_role=recipient_role,
                    context=context, formal=formal, warm_pro=warm_pro, concise=concise,
                    institutional=institutional, followup=followup, reminder=reminder,
                    ab_subject=ab_subject, whatsapp=whatsapp,
                )
                st.session_state["em_prompt"] = build_prompt(inputs, settings)
                go_to_output("em")

    if active == "output":
        if st.session_state.get("em_prompt"):
            prompt_output_section(st.session_state["em_prompt"], key_prefix="em", category="Professional Email Generator")
        else:
            st.info("Fill in the Inputs tab and click 'Generate Prompt'.")
