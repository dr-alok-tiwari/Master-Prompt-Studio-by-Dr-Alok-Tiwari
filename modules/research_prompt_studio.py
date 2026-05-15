"""
Research Paper Intelligence Studio
"""

import streamlit as st
from modules.utils import (
    apply_css, load_sample_inputs, section_header,
    info_card, prompt_output_section, global_sidebar_fields, file_upload_field,
    studio_tabs, go_to_output,
    template_upload_section, format_template_instruction)


def build_prompt(inputs: dict, settings: dict) -> str:
    tasks = []
    if inputs.get("intake"):        tasks.append("1. INTAKE PROTOCOL: Summarise each paper — title, authors, year, core methodology, key findings, and stated limitations.")
    if inputs.get("contradictions"): tasks.append("2. CONTRADICTION FINDER: Identify direct contradictions, conflicting results, or unresolved disagreements across the papers. Present as a comparative table where appropriate.")
    if inputs.get("citation_chain"): tasks.append("3. CITATION CHAIN: Map inter-paper citations within the set. Identify the most influential references cited across multiple papers.")
    if inputs.get("gap_scanner"):   tasks.append("4. GAP SCANNER: Identify research gaps, under-explored angles, and open questions not addressed by any paper in the set.")
    if inputs.get("methodology"):   tasks.append("5. METHODOLOGY AUDIT: Evaluate each paper's research design, sample characteristics, analytical techniques, and potential biases or threats to validity.")
    if inputs.get("synthesis"):     tasks.append("6. MASTER SYNTHESIS: Integrate the collective evidence into a coherent narrative. Identify convergences, tensions, and the overall state of knowledge.")
    if inputs.get("assumptions"):   tasks.append("7. ASSUMPTION KILLER: Surface implicit assumptions made by authors. Critically examine whether these assumptions are justified given the evidence.")
    if inputs.get("knowledge_map"): tasks.append("8. KNOWLEDGE MAP BUILDER: Produce a structured textual concept map of key themes, constructs, relationships, and hierarchies across the papers.")
    if inputs.get("so_what"):       tasks.append("9. SO WHAT? TEST: Articulate why this body of research matters — for theory, for practice, and for the direction of future inquiry.")
    if inputs.get("non_expert"):    tasks.append("10. NON-EXPERT SUMMARY: Write a plain-language, 200-word summary of the key takeaway for a non-specialist audience.")

    task_text = "\n".join(tasks) if tasks else "1. FULL ANALYSIS: Conduct a comprehensive multi-dimensional analysis of all uploaded papers."

    template_block = format_template_instruction(inputs.get("template_text", ""), label="research analysis")
    prompt = f"""You are an expert research analyst and systematic reviewer. Analyse the {inputs['num_papers']} uploaded research paper(s) on the topic of {inputs['topic']} in the domain of {inputs['domain']}.

CRITICAL RULE: Use ONLY the provided documents. Do not invent citations, fabricate statistics, or import knowledge from external sources not present in the uploads. If information is absent from the uploaded papers, state this explicitly.

YOUR ANALYSIS MUST COVER THE FOLLOWING:

{task_text}

OUTPUT SPECIFICATIONS:
- Format: {settings['output_format']}
- Tone: {settings['tone']}
- Length: {settings['length']}
- Citation style: {inputs['citation_style']}

QUALITY STANDARDS:
- Flag any claims you cannot verify from the provided documents.
- Clearly distinguish between what the papers state and your analytical interpretation.
- Do not hallucinate author names, publication years, or journal names.
- Avoid vague summarisation; prioritise analytical depth over descriptive breadth.
- Where papers are contradictory, present the tension explicitly rather than smoothing it over.

{template_block}
Begin your analysis now. Structure your response with clear section headers matching the tasks above.

[Authored prompt framework by {settings['author']}]"""

    return prompt


def render():
    apply_css()
    sample = load_sample_inputs()
    settings = global_sidebar_fields(sample, key_prefix="rps")

    st.markdown('<div class="page-title">🔬 Research Paper Intelligence Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Generate a rigorous master prompt for multi-paper research analysis</div>', unsafe_allow_html=True)

    active = studio_tabs("rps", has_preview=True)

    if active == "input":
        section_header("Paper Details", "📄")
        col1, col2 = st.columns(2)
        with col1:
            num_papers = st.number_input("Number of papers to analyse", min_value=1, max_value=100, value=5, key="rps_num")
            topic = st.text_input("Research topic / question", value="Machine Learning in Healthcare Diagnostics", key="rps_topic")
        with col2:
            domain = st.selectbox("Domain / Field", ["Healthcare AI", "Big Data Analytics", "Natural Language Processing", "Computer Vision", "Sustainability", "Education Technology", "Finance", "Operations", "Other"], key="rps_domain")
            citation_style = st.selectbox("Citation style", ["APA 7", "IEEE", "MLA", "Chicago", "Vancouver", "Harvard"], key="rps_cite")

        section_header("Analysis Components", "🔍")
        info_card("Select the analysis tasks you want the AI to perform on the uploaded papers.")

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            intake        = st.checkbox("📋 Intake Protocol",          value=True,  key="rps_intake")
            contradictions= st.checkbox("⚡ Contradiction Finder",    value=True,  key="rps_contra")
            citation_chain= st.checkbox("🔗 Citation Chain",           value=True,  key="rps_chain")
        with col_b:
            gap_scanner   = st.checkbox("🕳 Gap Scanner",              value=True,  key="rps_gap")
            methodology   = st.checkbox("🔬 Methodology Audit",        value=True,  key="rps_method")
            synthesis     = st.checkbox("🧩 Master Synthesis",         value=True,  key="rps_synth")
        with col_c:
            assumptions   = st.checkbox("💥 Assumption Killer",        value=False, key="rps_assume")
            knowledge_map = st.checkbox("🗺 Knowledge Map Builder",    value=False, key="rps_kmap")
            so_what       = st.checkbox("❓ 'So What?' Test",           value=True,  key="rps_sowhat")
        non_expert    = st.checkbox("🧑‍💼 Non-Expert Summary (plain language)",  value=False, key="rps_nonexp")

        section_header("Special Instructions", "📝")
        with st.expander("📎 Attach Paper Notes / Abstracts (optional)", expanded=False):
            paper_notes = file_upload_field(
                label="Paper Notes or Abstracts",
                key="rps_notes_file",
                fallback_key="rps_notes_text",
                placeholder="Paste paper abstracts, notes, or any text context here...",
                height=150,
            )
        special = st.text_area("Additional instructions (optional)", height=80, key="rps_special",
                               placeholder="e.g., Focus on quantitative studies only; exclude grey literature...")

        section_header("Paper / Protocol Template", "📐")
        template_text = template_upload_section(
            module_key="research_paper",
            key_prefix="rps",
            label="Paper / Review Protocol",
            help_text="Attach a systematic review protocol, paper outline template, or journal author guidelines.",
        )

        col_gen, col_ex = st.columns([2, 1])
        with col_gen:
            generate = st.button("🚀 Generate Prompt", use_container_width=True, key="rps_gen")
        with col_ex:
            if st.button("📂 Load Example", use_container_width=True, key="rps_load"):
                st.session_state["rps_topic"] = "Deep Learning for COVID-19 Chest X-Ray Classification"
                st.session_state["rps_num"] = 8
                st.rerun()

        if generate:
            inputs = dict(
                num_papers=num_papers, topic=topic, domain=domain,
                citation_style=citation_style, intake=intake,
                contradictions=contradictions, citation_chain=citation_chain,
                gap_scanner=gap_scanner, methodology=methodology,
                synthesis=synthesis, assumptions=assumptions,
                knowledge_map=knowledge_map, so_what=so_what,
                non_expert=non_expert, special=special,
                template_text=template_text,
            )
            st.session_state["rps_prompt"] = build_prompt(inputs, settings)
            go_to_output("rps")
            st.session_state["rps_inputs"] = inputs

    if active == "preview":
        if st.session_state.get("rps_prompt"):
            st.markdown("**Prompt summary:**")
            inp = st.session_state.get("rps_inputs", {})
            st.markdown(f"""
            | Parameter | Value |
            |---|---|
            | Papers | {inp.get('num_papers', '—')} |
            | Topic | {inp.get('topic', '—')} |
            | Domain | {inp.get('domain', '—')} |
            | Tone | {settings['tone']} |
            | Format | {settings['output_format']} |
            """)
        else:
            st.info("Generate a prompt on the Inputs tab to see a preview here.")

    if active == "output":
        if st.session_state.get("rps_prompt"):
            prompt_output_section(
                st.session_state["rps_prompt"],
                key_prefix="rps",
                category="Research Paper Intelligence",
            )
        else:
            st.info("Your generated prompt will appear here. Go to the Inputs tab and click 'Generate Prompt'.")
