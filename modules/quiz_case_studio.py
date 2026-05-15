"""
Quiz and Case Study Generator Studio
"""

import streamlit as st
from modules.utils import (
    apply_css, load_sample_inputs, section_header,
    prompt_output_section, global_sidebar_fields,
    studio_tabs, go_to_output,
    template_upload_section, format_template_instruction)


def build_prompt(inputs: dict, settings: dict) -> str:
    blooms = ", ".join(inputs.get("blooms_levels", ["Remember", "Understand", "Apply", "Analyse"]))

    template_block = format_template_instruction(inputs.get("template_text", ""), label="assessment")
    prompt = f"""You are an expert assessment designer with deep mastery of Bloom's Revised Taxonomy, question-writing best practices, and higher-education assessment standards.

ASSESSMENT BRIEF:
- Topic: {inputs['topic']}
- Target Students: {inputs['target_students']}
- Difficulty Level: {inputs['difficulty']}
- Bloom's Levels to Cover: {blooms}
- CLO Alignment: {inputs['clo'] if inputs['clo'].strip() else "Not specified — design to assess general topic mastery"}

GENERATE THE FOLLOWING ASSESSMENT PACKAGE:

1. MULTIPLE CHOICE QUESTIONS ({inputs['num_mcq']} MCQs)
   For each MCQ:
   - Clear, unambiguous stem
   - 4 plausible options (A–D), with only one clearly correct answer
   - No "all of the above" or "none of the above" options
   - Vary difficulty across the set
   {"- Include explanation for the correct answer" if inputs.get("include_explanations") else ""}

2. CASE-BASED QUESTIONS ({inputs['num_case']} questions)
   - One realistic, data-rich scenario (150–250 words)
   - {inputs['num_case']} analytical questions based on the scenario
   - Questions must require application and analysis, not just recall
   {"- Include model answer / marking scheme" if inputs.get("answer_key") else ""}

3. SHORT-ANSWER QUESTIONS ({inputs['num_short']} questions)
   - Each requires 3–5 sentence response
   - Cover different Bloom's levels
   - Include word limit guidance
   {"- Include model answers and marking criteria" if inputs.get("answer_key") else ""}

4. APPLIED SCENARIO QUESTIONS (2 questions)
   - Complex, multi-part questions requiring synthesis and evaluation
   - Based on realistic professional or research scenarios
   - Clearly indicate marks allocation per sub-question

5. BLOOM'S TAXONOMY MAPPING TABLE
   | Q# | Type | Bloom's Level | Difficulty | CLO | Marks |

6. DIFFICULTY DISTRIBUTION SUMMARY
   Easy: __% | Medium: __% | Hard: __% | Very Hard: __%

{"7. COMPLETE ANSWER KEY" if inputs.get("answer_key") else ""}
{"   - MCQ answers with detailed explanations" if inputs.get("answer_key") and inputs.get("include_explanations") else ("   - MCQ answers (with rationale for correct option)" if inputs.get("answer_key") else "")}
{"   - Model answers for all open-ended questions" if inputs.get("answer_key") else ""}

{"8. MARKING RUBRIC (for open-ended questions)" if inputs.get("rubric") else ""}
{"   4-level rubric: Excellent / Good / Satisfactory / Needs Improvement" if inputs.get("rubric") else ""}
{"   Include mark allocation per criterion" if inputs.get("rubric") else ""}

QUALITY STANDARDS:
- Do NOT recycle textbook questions — create original, contextually grounded items.
- Ensure all distractors in MCQs are plausible but unambiguously incorrect.
- Higher-order questions must genuinely require reasoning, not just recall.
- The case scenario must feel realistic and discipline-appropriate.

OUTPUT FORMAT: {settings['output_format']}
TONE: {settings['tone']}

{template_block}
[Assessment design framework by {settings['author']}]"""

    return prompt


def render():
    apply_css()
    sample = load_sample_inputs()
    settings = global_sidebar_fields(sample, key_prefix="qc")

    st.markdown('<div class="page-title">❓ Quiz and Case Study Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Generate comprehensive assessment packages with Bloom\'s mapping</div>', unsafe_allow_html=True)

    active = studio_tabs("qc")

    if active == "input":
        section_header("Assessment Context", "🎯")
        col1, col2 = st.columns(2)
        with col1:
            topic           = st.text_input("Topic", value="Decision Tree Classification and Random Forests", key="qc_topic")
            target_students = st.selectbox("Target Students", sample.get("target_audiences", []), key="qc_aud")
            difficulty      = st.selectbox("Overall Difficulty", sample.get("difficulty_levels", []), key="qc_diff")
        with col2:
            clo = st.text_input("CLO to Assess (optional)", key="qc_clo",
                                 placeholder="e.g., CLO3: Apply decision tree models to real datasets")
            blooms_levels = st.multiselect(
                "Bloom's Taxonomy Levels",
                ["Remember", "Understand", "Apply", "Analyse", "Evaluate", "Create"],
                default=["Remember", "Understand", "Apply", "Analyse"],
                key="qc_blooms"
            )

        section_header("Question Counts", "🔢")
        col3, col4, col5 = st.columns(3)
        with col3:
            num_mcq   = st.number_input("MCQs", 3, 30, 10, key="qc_mcq")
        with col4:
            num_case  = st.number_input("Case Questions", 1, 10, 3, key="qc_case")
        with col5:
            num_short = st.number_input("Short Answer Qs", 1, 10, 3, key="qc_short")

        section_header("Output Options", "⚙️")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            answer_key          = st.checkbox("Include Answer Key",       value=True,  key="qc_ak")
        with col_b:
            include_explanations= st.checkbox("Include Explanations",      value=True,  key="qc_exp")
        with col_c:
            rubric              = st.checkbox("Include Marking Rubric",    value=True,  key="qc_rub")

        section_header("Assessment Template", "📐")
        template_text = template_upload_section(
            module_key="quiz_case",
            key_prefix="qc",
            label="Question / Rubric",
            help_text="Attach a question bank format or rubric template so the AI generates assessments in your preferred layout.",
        )

        if st.button("🚀 Generate Prompt", use_container_width=True, key="qc_gen"):
            if not topic.strip():
                st.warning("Please enter a topic.")
            else:
                inputs = dict(
                    topic=topic, target_students=target_students,
                    difficulty=difficulty, clo=clo,
                    blooms_levels=blooms_levels, num_mcq=num_mcq,
                    num_case=num_case, num_short=num_short,
                    answer_key=answer_key, include_explanations=include_explanations,
                    rubric=rubric,
                    template_text=template_text,
                )
                st.session_state["qc_prompt"] = build_prompt(inputs, settings)
                go_to_output("qc")

    if active == "output":
        if st.session_state.get("qc_prompt"):
            prompt_output_section(st.session_state["qc_prompt"], key_prefix="qc", category="Quiz and Case Study Generator")
        else:
            st.info("Fill in the Inputs tab and click 'Generate Prompt'.")
