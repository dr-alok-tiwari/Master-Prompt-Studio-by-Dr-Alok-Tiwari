"""
Custom Prompt Builder Studio
"""

import streamlit as st
from modules.utils import (
    apply_css, load_sample_inputs, section_header,
    prompt_output_section, global_sidebar_fields, info_card,
    studio_tabs, go_to_output)

FRAMEWORKS = {
    "RCTOFE (Role-Context-Task-Output-Format-Evaluation)": [
        "role", "context", "task", "output", "output_format_field", "evaluation"
    ],
    "Chain-of-Thought Reasoning": [
        "role", "context", "task", "reasoning_steps", "output"
    ],
    "Academic Writing Prompt": [
        "role", "context", "task", "constraints", "output_format_field", "examples"
    ],
    "Teaching / Instructional Prompt": [
        "role", "context", "objective", "task", "output_format_field", "evaluation"
    ],
    "Research Synthesis Prompt": [
        "role", "context", "task", "constraints", "evaluation", "output"
    ],
    "Coding / Development Prompt": [
        "role", "context", "task", "constraints", "examples", "output"
    ],
    "Email / Communication Prompt": [
        "role", "context", "task", "constraints", "output_format_field"
    ],
    "Job Application Prompt": [
        "role", "context", "task", "constraints", "evaluation", "output"
    ],
    "Streamlit App Prompt": [
        "role", "context", "task", "output_format_field", "constraints", "evaluation"
    ],
    "Blank Canvas (All Fields)": [
        "role", "context", "objective", "task", "output_format_field",
        "constraints", "examples", "evaluation", "final_instruction"
    ],
}

FIELD_LABELS = {
    "role":              ("👤 Role / Persona",        "e.g., You are an expert research analyst specialising in healthcare AI..."),
    "context":           ("🌍 Context / Background",  "e.g., I am preparing a systematic literature review for a Q1 journal..."),
    "objective":         ("🎯 Objective",              "e.g., Identify the top 5 research gaps in deep learning for clinical decision support..."),
    "task":              ("📋 Task",                   "e.g., Analyse the following 8 papers and produce a structured synthesis report..."),
    "output_format_field":("📄 Output Format",         "e.g., Produce a structured report with numbered sections, a summary table, and a gap matrix..."),
    "constraints":       ("⛔ Constraints",             "e.g., Use only information from the provided documents. Do not hallucinate references..."),
    "examples":          ("💡 Examples / Templates",   "e.g., Structure each section like this: [Heading] → [Summary] → [Key insight] → [Evidence]..."),
    "evaluation":        ("✅ Evaluation Criteria",    "e.g., The output is successful if: all 8 papers are covered, gaps are specific, no citations are fabricated..."),
    "final_instruction": ("🚀 Final Instruction",      "e.g., Begin now. Be exhaustive, precise, and scholarly. Do not truncate the response..."),
    "reasoning_steps":   ("🧠 Reasoning Steps",        "e.g., Think step by step: 1) Identify the claim, 2) Examine evidence, 3) Check for contradictions..."),
}


def build_prompt(fields: dict, framework: str, settings: dict) -> str:
    parts = []
    for key, value in fields.items():
        if value and value.strip():
            label = FIELD_LABELS.get(key, (key.replace("_", " ").title(), ""))[0]
            label_clean = label.split(" ", 1)[1] if " " in label else label
            parts.append(f"## {label_clean.upper()}\n{value.strip()}")

    prompt_body = "\n\n".join(parts)

    return f"""[CUSTOM PROMPT — {framework}]

{prompt_body}

---
OUTPUT SPECIFICATIONS:
- Format: {settings['output_format']}
- Tone: {settings['tone']}
- Length: {settings['length']}

[Prompt built using Master Productivity Prompt Studio — {settings['author']}]"""


def render():
    apply_css()
    sample = load_sample_inputs()
    settings = global_sidebar_fields(sample, key_prefix="cpb")

    st.markdown('<div class="page-title">🧩 Custom Prompt Builder</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Build your own master prompt from scratch using proven frameworks</div>', unsafe_allow_html=True)

    info_card("Select a framework to load relevant fields. Fill in as many or as few as you need — empty fields are skipped.", color="#2E7D52")

    active = studio_tabs("cpb")

    if active == "input":
        section_header("Choose a Framework", "🏗️")
        framework = st.selectbox("Prompt Framework", list(FRAMEWORKS.keys()), key="cpb_framework")

        active_fields = FRAMEWORKS[framework]

        section_header("Fill in the Fields", "✍️")
        st.markdown(f"**Active fields for __{framework}__:**")

        field_values = {}
        for field_key in active_fields:
            if field_key in FIELD_LABELS:
                label, placeholder = FIELD_LABELS[field_key]
                # Title is large; others are text_area
                if field_key == "role":
                    field_values[field_key] = st.text_input(
                        label, placeholder=placeholder, key=f"cpb_{field_key}"
                    )
                else:
                    field_values[field_key] = st.text_area(
                        label, placeholder=placeholder, height=100, key=f"cpb_{field_key}"
                    )

        section_header("Prompt Title", "📌")
        prompt_title = st.text_input("Give this prompt a title (for saving to library)", value=f"Custom {framework.split('(')[0].strip()} Prompt", key="cpb_ptitle")

        col_gen, col_clear = st.columns([3, 1])
        with col_gen:
            if st.button("🚀 Build Prompt", use_container_width=True, key="cpb_gen"):
                filled = {k: v for k, v in field_values.items() if v and v.strip()}
                if not filled:
                    st.warning("Please fill in at least one field.")
                else:
                    st.session_state["cpb_prompt"] = build_prompt(filled, framework, settings)
                    st.session_state["cpb_title"] = prompt_title
                    go_to_output("cpb")
        with col_clear:
            if st.button("🗑 Reset", use_container_width=True, key="cpb_reset"):
                for field_key in active_fields:
                    if f"cpb_{field_key}" in st.session_state:
                        del st.session_state[f"cpb_{field_key}"]
                st.session_state["cpb_prompt"] = ""
                st.rerun()

    if active == "output":
        if st.session_state.get("cpb_prompt"):
            prompt_output_section(st.session_state["cpb_prompt"], key_prefix="cpb", category="Custom Prompt Builder")
        else:
            st.info("Build your prompt on the left tab to see it here.")
