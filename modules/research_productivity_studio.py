"""
Research Productivity Generator Studio
"""

import streamlit as st
from modules.utils import (
    apply_css, load_sample_inputs, section_header,
    prompt_output_section, global_sidebar_fields, info_card, file_upload_field,
    studio_tabs, go_to_output,
    template_upload_section, format_template_instruction)


def build_prompt(inputs: dict, settings: dict) -> str:
    selected = []
    if inputs.get("problem_stmt"):    selected.append("1. PROBLEM STATEMENT (3–5 lines, precise, gap-anchored, and significance-grounded)")
    if inputs.get("gap"):             selected.append("2. RESEARCH GAP STATEMENT (evidence-based gap articulation, referencing what existing literature overlooks or gets wrong)")
    if inputs.get("rqs"):             selected.append("3. RESEARCH QUESTIONS (3–5 specific, focused, answerable questions — not broad or vague)")
    if inputs.get("objectives"):      selected.append("4. RESEARCH OBJECTIVES (action-verb-based, directly aligned to each research question)")
    if inputs.get("framework"):       selected.append("5. CONCEPTUAL / THEORETICAL FRAMEWORK (description of the guiding theory or model, with diagram layout described in text)")
    if inputs.get("hypotheses"):      selected.append("6. HYPOTHESES (formally stated as H1, H2 etc., in null and alternate form where applicable)")
    if inputs.get("methodology"):     selected.append("7. METHODOLOGY DRAFT (research design, sampling strategy, data collection method, analytical technique, validation approach)")
    if inputs.get("dataset"):         selected.append("8. DATASET REQUIREMENTS AND SOURCES (data type, size, source, access method, preprocessing notes)")
    if inputs.get("analysis_plan"):   selected.append("9. ANALYSIS PLAN (statistical/ML techniques, software, model validation, robustness checks)")
    if inputs.get("contributions"):   selected.append("10. EXPECTED CONTRIBUTIONS (theoretical contribution, practical implications, methodological novelty)")
    if inputs.get("implications"):    selected.append("11. IMPLICATIONS FOR PRACTICE AND POLICY (specific actionable takeaways for practitioners, policymakers, institutions)")
    if inputs.get("limitations"):     selected.append("12. LIMITATIONS (honest scholarly framing — not defensive, not dismissive)")
    if inputs.get("future_research"): selected.append("13. FUTURE RESEARCH DIRECTIONS (concrete, specific directions building on this study)")
    if inputs.get("journal_strategy"):selected.append(f"14. JOURNAL TARGETING STRATEGY\n    Primary target: {inputs['target_journal']}\n    Provide 2 alternative journals with rationale. Include typical impact factor range, Scopus/ABDC ranking, and submission fit assessment.")
    if inputs.get("abstract"):        selected.append("15. ABSTRACT DRAFT (250 words, structured: Background → Gap → Objective → Method → Expected Findings → Implications)")
    if inputs.get("outline"):         selected.append("16. FULL PAPER OUTLINE (section headings + key content per section, word count guidance)")

    content_text = "\n\n".join(selected) if selected else "FULL RESEARCH DEVELOPMENT PACKAGE: all components listed above."

    template_block = format_template_instruction(inputs.get("template_text", ""), label="research output")
    prior_note = ""
    if inputs.get("prior_work", "").strip():
        prior_note = f"""
PRIOR WORK / EXISTING DRAFT PROVIDED:
{inputs['prior_work'].strip()}

Use the above as context. Build upon it rather than repeating it verbatim. Identify gaps and improvements.
"""

    prompt = f"""You are an expert research consultant, academic writing coach, and methodology specialist. Develop a comprehensive research development package for the following study:

RESEARCH BRIEF:
- Topic: {inputs['research_topic']}
- Domain / Discipline: {inputs['domain']}
- Target Journal: {inputs['target_journal']}
- Methodology Type: {inputs['methodology']}
- Dataset Availability: {inputs['dataset_status']}
{prior_note}
GENERATE THE FOLLOWING RESEARCH DEVELOPMENT COMPONENTS:

{content_text}

STRICT ACADEMIC STANDARDS:
- Do NOT invent citations, fabricate statistics, or generate unsupported empirical claims.
- Where literature references are needed, insert [CITATION NEEDED: topic/year] as placeholders.
- All research questions must be genuinely novel — not variations of textbook examples.
- The methodology must match the epistemological stance implied by the research questions.
- Hypotheses must be falsifiable and empirically testable.
- Journal targeting must be realistic — do not suggest Q1 journals for work that would not meet their threshold.

OUTPUT FORMAT: {settings['output_format']}
TONE: {settings['tone']}
LENGTH: {settings['length']}

{template_block}
[Research productivity framework by {settings['author']}]"""

    return prompt


def render():
    apply_css()
    sample = load_sample_inputs()
    settings = global_sidebar_fields(sample, key_prefix="rp")

    st.markdown('<div class="page-title">🧪 Research Productivity Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Generate a complete research development package — from gap to outline</div>', unsafe_allow_html=True)

    active = studio_tabs("rp")

    if active == "input":
        section_header("Research Details", "🔬")
        col1, col2 = st.columns(2)
        with col1:
            research_topic = st.text_input("Research Topic", value="Explainable AI for Clinical Decision Support in Emergency Medicine", key="rp_topic")
            domain = st.text_input("Domain / Discipline", value="Healthcare AI / Biomedical Informatics", key="rp_domain")
        with col2:
            target_journal = st.selectbox("Primary Target Journal", sample.get("journals", []), key="rp_journal")
            methodology    = st.selectbox("Methodology Type", [
                "Quantitative (survey-based)", "Quantitative (experimental)",
                "Machine Learning / Deep Learning", "Mixed Methods",
                "Qualitative (interviews/case study)", "Systematic Literature Review",
                "Meta-Analysis", "Simulation / Agent-Based Modelling",
                "Secondary Data Analysis", "Action Research"
            ], key="rp_method")
            dataset_status = st.selectbox("Dataset Availability", [
                "Public dataset available", "Proprietary dataset available",
                "Dataset to be collected (primary)", "Simulation data required",
                "Not yet determined"
            ], key="rp_data")

        section_header("Components to Generate", "✅")
        info_card("Select all components you need for your research development workflow.")

        # Optional: upload prior work / existing draft
        with st.expander("📎 Attach Prior Work or Existing Draft (optional)", expanded=False):
            prior_work = file_upload_field(
                label="Prior Work / Existing Draft",
                key="rp_prior_file",
                fallback_key="rp_prior_text",
                placeholder="Paste any existing draft, abstract, or notes here for context...",
                height=150,
            )
        if "rp_prior_text" not in st.session_state:
            prior_work = ""
        else:
            prior_work = st.session_state.get("rp_prior_text", "")

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            problem_stmt  = st.checkbox("Problem Statement",        value=True,  key="rp_ps")
            gap           = st.checkbox("Research Gap",             value=True,  key="rp_gap")
            rqs           = st.checkbox("Research Questions",       value=True,  key="rp_rq")
            objectives    = st.checkbox("Research Objectives",      value=True,  key="rp_obj")
            framework     = st.checkbox("Conceptual Framework",     value=True,  key="rp_fw")
            hypotheses    = st.checkbox("Hypotheses",               value=False, key="rp_hyp")
        with col_b:
            methodology_c = st.checkbox("Methodology Draft",        value=True,  key="rp_mc")
            dataset       = st.checkbox("Dataset Requirements",     value=True,  key="rp_ds")
            analysis_plan = st.checkbox("Analysis Plan",            value=True,  key="rp_ap")
            contributions = st.checkbox("Contributions",            value=True,  key="rp_ct")
        with col_c:
            implications  = st.checkbox("Implications",             value=True,  key="rp_im")
            limitations   = st.checkbox("Limitations",              value=True,  key="rp_lm")
            future_research=st.checkbox("Future Research",          value=True,  key="rp_fr")
            journal_strategy=st.checkbox("Journal Targeting",       value=True,  key="rp_js")
            abstract      = st.checkbox("Abstract Draft",           value=True,  key="rp_ab")
            outline       = st.checkbox("Full Paper Outline",       value=True,  key="rp_ol")

        section_header("Research Template", "📐")
        template_text = template_upload_section(
            module_key="research_productivity",
            key_prefix="rp",
            label="Research Proposal",
            help_text="Attach a grant proposal form, research proposal template, or journal submission guideline.",
        )

        if st.button("🚀 Generate Prompt", use_container_width=True, key="rp_gen"):
            if not research_topic.strip():
                st.warning("Please enter a research topic.")
            else:
                inputs = dict(
                    research_topic=research_topic, domain=domain,
                    target_journal=target_journal, methodology=methodology,
                    dataset_status=dataset_status, prior_work=prior_work,
                    problem_stmt=problem_stmt, gap=gap, rqs=rqs, objectives=objectives,
                    framework=framework, hypotheses=hypotheses, methodology_check=methodology_c,
                    dataset=dataset, analysis_plan=analysis_plan, contributions=contributions,
                    implications=implications, limitations=limitations,
                    future_research=future_research, journal_strategy=journal_strategy,
                    abstract=abstract, outline=outline,
                    template_text=template_text,
                )
                st.session_state["rp_prompt"] = build_prompt(inputs, settings)
                go_to_output("rp")

    if active == "output":
        if st.session_state.get("rp_prompt"):
            prompt_output_section(st.session_state["rp_prompt"], key_prefix="rp", category="Research Productivity Generator")
        else:
            st.info("Fill in the Inputs tab and click 'Generate Prompt'.")
