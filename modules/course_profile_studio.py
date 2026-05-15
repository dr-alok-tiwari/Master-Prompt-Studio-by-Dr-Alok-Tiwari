"""
Course Profile Generator Prompt Studio
"""

import streamlit as st
from modules.utils import (
    apply_css, load_sample_inputs, section_header,
    prompt_output_section, global_sidebar_fields,
    studio_tabs, go_to_output,
    template_upload_section, format_template_instruction)


def build_prompt(inputs: dict, settings: dict) -> str:
    latex_note = "\n- Provide a LaTeX-ready version using \\documentclass{article} formatting." if inputs.get("latex") else ""
    word_note  = "\n- Provide a clean, Word-compatible Markdown version in addition to the main output." if inputs.get("word") else ""
    template_block = format_template_instruction(inputs.get("template_text", ""), label="course profile")

    prompt = f"""You are an experienced curriculum designer, faculty developer, and accreditation specialist. Create a complete, accreditation-ready course profile for the following:

COURSE DETAILS:
- Course Title: {inputs['course_title']}
- Credits: {inputs['credits']}
- Total Sessions: {inputs['num_sessions']} sessions × {inputs['session_duration']} each
- Target Students: {inputs['target_students']}
- Course Type: {inputs['course_type']}
- Programme: {inputs['programme']}
- Pedagogy Preference: {inputs['pedagogy']}
- Tools / Software: {inputs['tools']}

REQUIRED COURSE PROFILE COMPONENTS:

1. COURSE DESCRIPTION (3–5 sentences, precise and motivating)

2. COURSE RATIONALE
   - Why this course is essential for {inputs['target_students']}
   - Industry/research relevance
   - Fit within the programme curriculum

3. COURSE OBJECTIVES (5–7 measurable, action-verb-based objectives)

4. COURSE LEARNING OUTCOMES / CLOs
   Generate exactly {inputs['clo_count']} CLOs.
   Each CLO must:
   - Begin with a Bloom's Taxonomy action verb
   - Be directly assessable
   - Be specific and unambiguous

5. CLO–PLO MAPPING TABLE
   Map each CLO to the programme-level outcomes (PLOs).
   Format as a matrix table: CLOs as rows, PLOs as columns.
   Mark cells with ✓ (primary alignment) or △ (secondary alignment).

6. SESSION-WISE TEACHING PLAN
   Create a plan for all {inputs['num_sessions']} sessions.
   For each session, provide:
   | Session # | Topic | Subtopics | Pedagogy | Activity | CLO(s) |

7. PEDAGOGY AND TEACHING METHODS
   Detail the primary and supplementary teaching approaches,
   with rationale for each method chosen.

8. ASSESSMENT STRUCTURE
   - Component name | Weightage | CLO alignment | Assessment week
   - Total must equal 100%
   - Include: {inputs['assessment_structure']}

9. GRADING RUBRICS
   Provide detailed rubrics for the two highest-weighted assessments.
   Use a 4-level scale: Excellent / Good / Satisfactory / Unsatisfactory.

10. READING LIST
    - 3–5 core textbooks (with edition and author)
    - 5–8 journal articles (indicate [peer-reviewed])
    - 2–3 online resources or datasets

11. SOFTWARE AND TOOL REQUIREMENTS
    Tools: {inputs['tools']}
    Include installation guidance and free alternatives where available.

12. AI USAGE POLICY
    Define acceptable and unacceptable uses of AI tools in this course.
    Specify disclosure requirements and academic integrity implications.

13. ACADEMIC INTEGRITY STATEMENT
    Institutional-standard statement covering plagiarism, collusion,
    and AI-assisted work.
{latex_note}{word_note}
{template_block}
FORMAT: {settings['output_format']}
TONE: {settings['tone']}
AUTHOR: {settings['author']}

Ensure every CLO is clearly measurable and the CLO–PLO mapping is logically coherent. Do not generate vague objectives."""

    return prompt


def render():
    apply_css()
    sample = load_sample_inputs()
    settings = global_sidebar_fields(sample, key_prefix="cp")

    st.markdown('<div class="page-title">🎓 Course Profile Generator Prompt</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Generate a complete accreditation-ready course profile prompt</div>', unsafe_allow_html=True)

    active = studio_tabs("cp")

    if active == "input":
        section_header("Course Identity", "📘")
        col1, col2, col3 = st.columns(3)
        with col1:
            course_title = st.text_input("Course Title", value="Big Data Analytics", key="cp_title")
            credits      = st.number_input("Credits", 1, 6, 3, key="cp_cred")
        with col2:
            num_sessions     = st.number_input("Total Sessions", 8, 60, 16, key="cp_sess")
            session_duration = st.selectbox("Session Duration", ["60 min", "75 min", "90 min", "2 hours", "3 hours"], key="cp_dur")
        with col3:
            programme    = st.text_input("Programme", value="PGDM-BDA", key="cp_prog")
            course_type  = st.selectbox("Course Type", ["Core", "Elective", "Lab", "Project", "Seminar"], key="cp_type")

        section_header("Students & Pedagogy", "🧑‍🎓")
        col4, col5 = st.columns(2)
        with col4:
            target_students = st.selectbox("Target Students", sample.get("target_audiences", []), key="cp_aud")
            clo_count       = st.slider("Number of CLOs", 3, 10, 5, key="cp_clo")
        with col5:
            pedagogy = st.multiselect(
                "Pedagogy Methods",
                ["Case Discussion", "Lecture", "Flipped Classroom", "Problem-Based Learning",
                 "Live Projects", "Simulation", "Guest Lectures", "Hands-on Labs", "Debates"],
                default=["Lecture", "Case Discussion", "Hands-on Labs"],
                key="cp_ped"
            )
            tools = st.multiselect(
                "Tools / Software",
                sample.get("tool_categories", []),
                default=["Python (pandas, scikit-learn, matplotlib)", "Power BI"],
                key="cp_tools"
            )

        section_header("Assessment Structure", "📊")
        assessment_structure = st.text_area(
            "Describe assessment components and weightages",
            value="Quizzes: 15%, Mid-term Project: 25%, End-term Exam: 40%, Case Presentation: 20%",
            height=80, key="cp_assess"
        )

        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            latex = st.checkbox("Include LaTeX-ready version", value=True, key="cp_latex")
        with col_opt2:
            word  = st.checkbox("Include Word/Markdown version", value=True, key="cp_word")

        section_header("Course Profile Template", "📐")
        template_text = template_upload_section(
            module_key="course_profile",
            key_prefix="cp",
            label="Course Profile",
            help_text="Select your institution's course profile format (GIM, PGDM standard, or custom) "
                      "so the AI outputs content that fits directly into your official template.",
        )

        if st.button("🚀 Generate Prompt", use_container_width=True, key="cp_gen"):
            inputs = dict(
                course_title=course_title, credits=credits,
                num_sessions=num_sessions, session_duration=session_duration,
                target_students=target_students, course_type=course_type,
                programme=programme, clo_count=clo_count,
                pedagogy=", ".join(pedagogy), tools=", ".join(tools),
                assessment_structure=assessment_structure,
                latex=latex, word=word,
                template_text=template_text,
            )
            st.session_state["cp_prompt"] = build_prompt(inputs, settings)
            go_to_output("cp")

    if active == "output":
        if st.session_state.get("cp_prompt"):
            prompt_output_section(st.session_state["cp_prompt"], key_prefix="cp", category="Course Profile Generator")
        else:
            st.info("Fill in the Inputs tab and click 'Generate Prompt'.")
