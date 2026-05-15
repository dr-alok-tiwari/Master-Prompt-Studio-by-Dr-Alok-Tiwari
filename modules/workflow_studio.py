"""
Productivity Workflow Generator Studio
"""

import streamlit as st
from modules.utils import (
    apply_css, load_sample_inputs, section_header,
    prompt_output_section, global_sidebar_fields,
    studio_tabs, go_to_output)


def build_prompt(inputs: dict, settings: dict) -> str:
    prompt = f"""You are an expert productivity systems designer, workflow architect, and knowledge management specialist.

WORKFLOW DESIGN BRIEF:
- Domain: {inputs['domain']}
- Goal: {inputs['goal']}
- Current Problem / Pain Point: {inputs['current_problem']}
- Available Tools: {inputs['tools']}
- Preferred Free Tools: {inputs['free_tools']}
- Time Frame: {inputs['time_frame']}
- Desired Automation Level: {inputs['automation_level']}
- Output Type Required: {inputs['output_type']}

DESIGN A COMPLETE PRODUCTIVITY WORKFLOW SYSTEM COVERING:

1. GOAL STATEMENT
   Restate the goal in SMART format (Specific, Measurable, Achievable, Relevant, Time-bound).

2. REQUIRED INPUTS
   What resources, data, tools, or information must be ready before starting this workflow?

3. STEP-BY-STEP WORKFLOW
   - Number each step clearly
   - Mark decision points with [DECISION: condition → path A / path B]
   - Mark automation points with [AUTOMATE: tool + method]
   - Mark quality checks with [QC: what to verify]
   - Include estimated time per step

4. RECOMMENDED TOOLS
   | Step | Primary Tool | Free Alternative | Notes |

5. AUTOMATION OPPORTUNITIES
   For each automatable step, specify:
   - What can be automated
   - How (tool, script, trigger, scheduler)
   - Level of technical skill required
   - Time saved per cycle

6. TEMPLATES
   Describe the key templates needed (naming conventions, structure, fields).

7. CHECKLISTS
   - Daily checklist (if applicable)
   - Weekly review checklist
   - Milestone completion checklist

8. QUALITY CONTROL POINTS
   Where in the workflow should output be reviewed? What criteria define "good enough to proceed"?

9. COMMON ERRORS AND HOW TO AVOID THEM
   Top 5 errors people make in this type of workflow, with prevention strategies.

10. REVIEW AND ITERATION CYCLE
    How often should this workflow be reviewed and updated? What triggers a revision?

11. SCALING PLAN
    How to expand this workflow as team size, data volume, or complexity grows?

OUTPUT FORMAT: {settings['output_format']}
TONE: {settings['tone']}
LENGTH: {settings['length']}

[Workflow design framework by {settings['author']}]"""

    return prompt


def render():
    apply_css()
    sample = load_sample_inputs()
    settings = global_sidebar_fields(sample, key_prefix="wf")

    st.markdown('<div class="page-title">⚙️ Productivity Workflow Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Design complete, actionable productivity systems with tools, checklists, and automations</div>', unsafe_allow_html=True)

    active = studio_tabs("wf")

    if active == "input":
        section_header("Workflow Context", "🔧")
        col1, col2 = st.columns(2)
        with col1:
            domain          = st.text_input("Domain", value="Academic Research and Publication", key="wf_dom")
            goal            = st.text_input("Goal", value="Publish 3 peer-reviewed papers in 12 months", key="wf_goal")
            time_frame      = st.selectbox("Time Frame", ["Daily", "Weekly", "Monthly", "Quarterly", "Annual", "Project-based"], key="wf_tf")
        with col2:
            automation_level = st.selectbox("Automation Level Needed", [
                "Manual (checklists only)", "Semi-automated (some tools)",
                "Moderately automated (scripts + tools)", "Highly automated (pipelines + scheduling)"
            ], key="wf_auto")
            output_type = st.selectbox("Primary Output Type", sample.get("output_formats", []), key="wf_out")

        current_problem = st.text_area("Current Problem / Pain Point", height=80, key="wf_prob",
                                       placeholder="e.g., I lose track of multiple manuscript deadlines and struggle to move papers from draft to submission systematically...")

        section_header("Tools & Resources", "🛠")
        col3, col4 = st.columns(2)
        with col3:
            tools      = st.multiselect("Tools You Have Access To", sample.get("tool_categories", []) + ["Notion", "Trello", "Google Docs", "Zotero", "Overleaf", "GitHub"], key="wf_tools")
        with col4:
            free_tools = st.multiselect("Preferred Free Tools", ["Google Docs", "Notion (free)", "Trello (free)", "Zotero", "Obsidian", "GitHub", "VS Code", "Python scripts", "Google Sheets"], key="wf_free")

        if st.button("🚀 Generate Prompt", use_container_width=True, key="wf_gen"):
            if not goal.strip():
                st.warning("Please enter a goal.")
            else:
                inputs = dict(
                    domain=domain, goal=goal, current_problem=current_problem,
                    tools=", ".join(tools) if tools else "General productivity tools",
                    free_tools=", ".join(free_tools) if free_tools else "Open-source alternatives",
                    time_frame=time_frame, automation_level=automation_level, output_type=output_type,
                )
                st.session_state["wf_prompt"] = build_prompt(inputs, settings)
                go_to_output("wf")

    if active == "output":
        if st.session_state.get("wf_prompt"):
            prompt_output_section(st.session_state["wf_prompt"], key_prefix="wf", category="Productivity Workflow Generator")
        else:
            st.info("Fill in the Inputs tab and click 'Generate Prompt'.")
