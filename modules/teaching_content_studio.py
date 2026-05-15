"""
Teaching Content Generator Studio
"""

import streamlit as st
from modules.utils import (
    apply_css, load_sample_inputs, section_header,
    prompt_output_section, global_sidebar_fields,
    studio_tabs, go_to_output,
    template_upload_section, format_template_instruction)


def build_prompt(inputs: dict, settings: dict) -> str:
    selected = []
    if inputs.get("instructor_notes"):  selected.append("1. INSTRUCTOR NOTES\n   Background knowledge, pedagogical tips, common student misconceptions, and how to pace the session.")
    if inputs.get("student_exp"):       selected.append("2. STUDENT-FRIENDLY EXPLANATION\n   Clear, engaging explanation with analogies, real-world connections, and progressive complexity.")
    if inputs.get("slides"):            selected.append("3. SLIDE-BY-SLIDE CONTENT OUTLINE\n   For each slide: title, 3–5 key points, suggested visual, and delivery note.")
    if inputs.get("examples"):          selected.append("4. REAL-WORLD EXAMPLES (minimum 3)\n   Grounded in contexts relevant to {target_students}.".replace("{target_students}", inputs['target_students']))
    if inputs.get("activities"):        selected.append("5. IN-CLASS ACTIVITIES\n   At least 2 activities (think-pair-share, case micro-analysis, data exercise, role play, etc.) with instructions and debrief questions.")
    if inputs.get("discussion_qs"):     selected.append("6. DISCUSSION QUESTIONS\n   5–7 higher-order questions covering application, analysis, and evaluation levels.")
    if inputs.get("quiz"):              selected.append("7. FORMATIVE QUIZ\n   5 MCQs with 4 options each, answer key, and brief explanation per answer.")
    if inputs.get("case_study"):        selected.append("8. MINI CASE STUDY\n   Realistic scenario with background, data/context, 3 discussion questions, and solution hints.")
    if inputs.get("rubric"):            selected.append("9. ASSESSMENT RUBRIC\n   4-level rubric (Excellent / Good / Satisfactory / Needs Improvement) for the main assessment component.")
    if inputs.get("lecture_script"):    selected.append("10. LECTURE SCRIPT\n   Verbatim teaching notes for key segments (at least 3 key moments in the session).")
    if inputs.get("concept_map"):       selected.append("11. CONCEPT MAP\n   Textual description of relationships between key concepts, suitable for diagram conversion.")
    if inputs.get("misconceptions"):    selected.append("12. COMMON MISCONCEPTIONS\n   Top 5 misconceptions students hold about this topic, with correct explanations.")
    if inputs.get("summary"):           selected.append("13. SESSION SUMMARY\n   Concise 200-word summary of key takeaways.")
    if inputs.get("exit_ticket"):       selected.append("14. EXIT TICKET\n   One 1-minute reflection prompt students complete before leaving.")

    content_list = "\n\n".join(selected) if selected else "FULL TEACHING PACKAGE: All components listed above."

    template_block = format_template_instruction(inputs.get("template_text", ""), label="session plan")
    prompt = f"""You are a master educator, instructional designer, and pedagogy specialist. Create complete, classroom-ready teaching material for the following session:

TOPIC: {inputs['topic']}
COURSE: {inputs['course']}
TARGET STUDENTS: {inputs['target_students']}
SESSION DURATION: {inputs['session_duration']}
TEACHING LEVEL: {inputs['teaching_level']}
PREFERRED PEDAGOGY: {inputs['pedagogy']}
CLO ALIGNMENT: {inputs['clo'] if inputs['clo'].strip() else "Not specified — align to general learning outcomes"}

GENERATE THE FOLLOWING CONTENT COMPONENTS:

{content_list}

QUALITY STANDARDS:
- Every example must be realistic and relevant to {inputs['target_students']}.
- Discussion questions must progress from recall → application → evaluation.
- Do not generate generic, textbook-style explanations — make content contextually vivid.
- Instructor notes must include specific "watch out for" moments and timing guidance.
- The lecture script should sound like a real expert speaking, not a formal reader.
- If generating slides, ensure no slide has more than 5 bullet points.

OUTPUT FORMAT: {settings['output_format']}
TONE: {settings['tone']}
LENGTH: {settings['length']}

{template_block}
[Teaching content framework by {settings['author']}]"""

    return prompt


def render():
    apply_css()
    sample = load_sample_inputs()
    settings = global_sidebar_fields(sample, key_prefix="tc")

    st.markdown('<div class="page-title">📚 Teaching Content Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Generate complete, classroom-ready teaching material for any session</div>', unsafe_allow_html=True)

    active = studio_tabs("tc")

    if active == "input":
        section_header("Session Details", "🎓")
        col1, col2 = st.columns(2)
        with col1:
            topic           = st.text_input("Topic", value="Supervised Learning: Classification Algorithms", key="tc_topic")
            course          = st.text_input("Course", value="Big Data Analytics", key="tc_course")
            target_students = st.selectbox("Target Students", sample.get("target_audiences", []), key="tc_aud")
        with col2:
            session_duration= st.selectbox("Session Duration", ["60 min", "75 min", "90 min", "2 hours", "3 hours"], key="tc_dur")
            teaching_level  = st.selectbox("Teaching Level", sample.get("difficulty_levels", []), key="tc_level")
            pedagogy        = st.multiselect(
                "Pedagogy Preference",
                ["Lecture", "Case Discussion", "Flipped Classroom", "Problem-Based Learning",
                 "Demonstration", "Group Activity", "Simulation", "Socratic Method"],
                default=["Lecture", "Case Discussion"],
                key="tc_ped"
            )
        clo = st.text_input("CLO Alignment (optional)", key="tc_clo",
                             placeholder="e.g., CLO2: Analyse ML classification models using Python")

        section_header("Content Components to Generate", "✅")

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            instructor_notes = st.checkbox("Instructor Notes",      value=True,  key="tc_in")
            student_exp      = st.checkbox("Student Explanation",   value=True,  key="tc_se")
            slides           = st.checkbox("Slide Outline",         value=True,  key="tc_sl")
            examples         = st.checkbox("Real-World Examples",   value=True,  key="tc_ex")
            activities       = st.checkbox("In-Class Activities",   value=True,  key="tc_ac")
        with col_b:
            discussion_qs    = st.checkbox("Discussion Questions",  value=True,  key="tc_dq")
            quiz             = st.checkbox("Formative Quiz",        value=True,  key="tc_qz")
            case_study       = st.checkbox("Mini Case Study",       value=True,  key="tc_cs")
            rubric           = st.checkbox("Assessment Rubric",     value=False, key="tc_rb")
        with col_c:
            lecture_script   = st.checkbox("Lecture Script",        value=False, key="tc_ls")
            concept_map      = st.checkbox("Concept Map",           value=False, key="tc_cm")
            misconceptions   = st.checkbox("Common Misconceptions", value=True,  key="tc_ms")
            summary          = st.checkbox("Session Summary",       value=True,  key="tc_sm")
            exit_ticket      = st.checkbox("Exit Ticket",           value=True,  key="tc_et")

        section_header("Session Template", "📐")
        template_text = template_upload_section(
            module_key="teaching_content",
            key_prefix="tc",
            label="Session Plan",
            help_text="Attach your institution's session plan format so generated content fits directly into it.",
        )

        if st.button("🚀 Generate Prompt", use_container_width=True, key="tc_gen"):
            if not topic.strip():
                st.warning("Please enter a topic.")
            else:
                inputs = dict(
                    topic=topic, course=course, target_students=target_students,
                    session_duration=session_duration, teaching_level=teaching_level,
                    pedagogy=", ".join(pedagogy), clo=clo,
                    instructor_notes=instructor_notes, student_exp=student_exp,
                    slides=slides, examples=examples, activities=activities,
                    discussion_qs=discussion_qs, quiz=quiz, case_study=case_study,
                    rubric=rubric, lecture_script=lecture_script, concept_map=concept_map,
                    misconceptions=misconceptions, summary=summary, exit_ticket=exit_ticket,
                    template_text=template_text,
                )
                st.session_state["tc_prompt"] = build_prompt(inputs, settings)
                go_to_output("tc")

    if active == "output":
        if st.session_state.get("tc_prompt"):
            prompt_output_section(st.session_state["tc_prompt"], key_prefix="tc", category="Teaching Content Generator")
        else:
            st.info("Fill in the Inputs tab and click 'Generate Prompt'.")
