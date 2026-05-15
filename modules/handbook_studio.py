"""
Handbook Generator Prompt Studio
"""

import streamlit as st
from modules.utils import (
    apply_css, load_sample_inputs, section_header,
    info_card, prompt_output_section, global_sidebar_fields,
    studio_tabs, go_to_output,
    template_upload_section, format_template_instruction)


def build_prompt(inputs: dict, settings: dict) -> str:
    optional_sections = []
    if inputs.get("examples"):      optional_sections.append("- At least 3 worked examples per chapter, grounded in realistic contexts")
    if inputs.get("case_studies"):  optional_sections.append("- Contextualised case studies illustrating key concepts in applied settings")
    if inputs.get("exercises"):     optional_sections.append("- Practice exercises with varying difficulty (application, analysis, synthesis)")
    if inputs.get("answer_key"):    optional_sections.append("- Complete answer key with explanatory rationale, not just correct answers")
    if inputs.get("glossary"):      optional_sections.append("- Glossary of at least 30 key terms, defined precisely and concisely")
    if inputs.get("roadmap"):       optional_sections.append("- Mastery roadmap: a self-assessment guide for learners to gauge progress")

    diff_levels = ", ".join(inputs.get("diff_levels", ["Beginner", "Intermediate", "Advanced"]))
    opt_text = "\n".join(optional_sections) if optional_sections else "- Standard explanations and summary"

    template_block = format_template_instruction(inputs.get("template_text", ""), label="handbook")
    prompt = f"""You are an expert instructional designer, domain specialist, and academic author. Create a comprehensive, publication-ready handbook titled:

"{inputs['topic']}"

TARGET LEARNER: {inputs['target_learner']}
DIFFICULTY LEVELS COVERED: {diff_levels}
NUMBER OF CHAPTERS: {inputs['num_chapters']}
FORMAT: {settings['output_format']}
TONE: {settings['tone']}
LENGTH: {settings['length']}

REQUIRED HANDBOOK STRUCTURE:

1. TITLE PAGE
   - Full title and subtitle
   - Author name: {settings['author']}
   - Institution / affiliation
   - Edition number and date
   - Brief tagline

2. PREFACE
   - Purpose and scope of the handbook
   - Who this is for and how to use it
   - Acknowledgements

3. LEARNING OBJECTIVES
   - 5–8 overarching objectives, written with measurable action verbs
   - Chapter-specific objectives at the start of each chapter

4. CHAPTER ARCHITECTURE ({inputs['num_chapters']} chapters)
   For each chapter, provide:
   a. BEGINNER LEVEL: Core concept explained in plain language with analogies
   b. INTERMEDIATE LEVEL: Technical depth, formal definitions, worked mechanics
   c. ADVANCED LEVEL: Nuanced theory, edge cases, exceptions, practitioner notes
   d. EXPERT LEVEL: Current research frontiers, open debates, future directions

5. OPTIONAL ENRICHMENT CONTENT:
{opt_text}

6. ASSESSMENT SECTION
   - Chapter-end review questions (recall, application, analysis)
   - Cumulative end-of-handbook assessment

7. GLOSSARY (if selected above)

8. MASTERY ROADMAP
   A self-assessment progression guide for learners

QUALITY STANDARDS:
- Every section must be substantive and precise — no generic filler content.
- Use real-world examples relevant to {inputs['target_learner']}.
- Maintain consistent terminology throughout.
- Ensure conceptual progression from chapter to chapter.
- Do not invent statistics or fabricate citations.
- If referencing literature, note it as [CITATION NEEDED] for the author to verify.

{template_block}
Begin generating the handbook now. Use clear chapter and section headings throughout."""

    return prompt


def render():
    apply_css()
    sample = load_sample_inputs()
    settings = global_sidebar_fields(sample, key_prefix="hb")

    st.markdown('<div class="page-title">📖 Handbook Generator Prompt</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Generate a prompt for creating detailed, multi-level learning handbooks</div>', unsafe_allow_html=True)

    active = studio_tabs("hb")

    if active == "input":
        section_header("Handbook Configuration", "📘")
        col1, col2 = st.columns(2)
        with col1:
            topic = st.text_input("Handbook Topic", value="Big Data Analytics for Business Decision-Making", key="hb_topic")
            target_learner = st.selectbox("Target Learner", sample.get("target_audiences", []), key="hb_learner")
            num_chapters = st.slider("Number of Chapters", 3, 20, 8, key="hb_chaps")
        with col2:
            diff_levels = st.multiselect(
                "Difficulty Levels to Include",
                ["Beginner", "Intermediate", "Advanced", "Expert"],
                default=["Beginner", "Intermediate", "Advanced"],
                key="hb_diff"
            )

        section_header("Optional Sections", "✅")
        col_a, col_b = st.columns(2)
        with col_a:
            examples    = st.checkbox("Worked Examples",    value=True,  key="hb_ex")
            case_studies= st.checkbox("Case Studies",       value=True,  key="hb_cs")
            exercises   = st.checkbox("Exercises",          value=True,  key="hb_exer")
        with col_b:
            answer_key  = st.checkbox("Answer Key",         value=True,  key="hb_ak")
            glossary    = st.checkbox("Glossary",           value=True,  key="hb_gloss")
            roadmap     = st.checkbox("Mastery Roadmap",    value=True,  key="hb_road")

        template_text = template_upload_section(
            module_key="handbook",
            key_prefix="hb",
            label="Handbook",
            help_text="Use this when the handbook must follow a fixed institutional or publication structure.",
        )

        col_gen, col_ex = st.columns([2, 1])
        with col_gen:
            generate = st.button("🚀 Generate Prompt", use_container_width=True, key="hb_gen")
        with col_ex:
            if st.button("📂 Load Example", use_container_width=True, key="hb_load"):
                st.session_state["hb_topic"] = "Machine Learning for Healthcare Professionals"
                st.rerun()

        if generate:
            if not topic.strip():
                st.warning("Please enter a handbook topic.")
            else:
                inputs = dict(
                    topic=topic, target_learner=target_learner,
                    diff_levels=diff_levels, num_chapters=num_chapters,
                    examples=examples, case_studies=case_studies,
                    exercises=exercises, answer_key=answer_key,
                    glossary=glossary, roadmap=roadmap,
                    template_text=template_text,
                )
                st.session_state["hb_prompt"] = build_prompt(inputs, settings)
                go_to_output("hb")

    if active == "output":
        if st.session_state.get("hb_prompt"):
            prompt_output_section(st.session_state["hb_prompt"], key_prefix="hb", category="Handbook Generator")
        else:
            st.info("Your generated prompt will appear here. Fill in the Inputs tab and click 'Generate Prompt'.")
