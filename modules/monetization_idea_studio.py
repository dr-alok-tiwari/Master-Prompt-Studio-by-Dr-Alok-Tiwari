"""
Monetization Idea Studio
Created by: Dr Alok Tiwari
"""

import streamlit as st
from modules.utils import (
    apply_css,
    load_sample_inputs,
    section_header,
    prompt_output_section,
    global_sidebar_fields,
    studio_tabs,
    go_to_output,
)


BASE_PROMPT = r'''Act as an elite digital product strategist, market researcher, monetization architect, and AI business operator.

Your objective is to identify, validate, package, launch, and scale at least one highly profitable digital product opportunity ($5K–$50K+ potential) based on:
- my skills,
- expertise,
- experience,
- existing assets,
- interests,
- audience,
- previous conversations,
- and current market demand.

Think like a combination of:
- YC startup advisor,
- Gumroad top seller,
- SaaS founder,
- creator economy strategist,
- AI automation consultant,
- and behavioral economist.

Do not provide generic ideas. Focus on:
- fast-to-build,
- high-margin,
- AI-leveraged,
- scalable,
- low-cost,
- defensible,
- and realistically executable opportunities.

Your output must be deeply analytical, commercially aware, and immediately actionable.

==================================================
PHASE 1 — PERSONAL ASSET ANALYSIS
==================================================

1. Analyze my likely strengths, unfair advantages, domain expertise, and monetizable knowledge.
2. Infer:
   - high-value skills,
   - rare combinations of expertise,
   - credibility markers,
   - audience fit,
   - and asymmetric opportunities.
3. Identify:
   - problems I can solve faster than most people,
   - problems people already pay for,
   - and problems becoming more valuable because of AI disruption.
4. Detect recurring themes that indicate hidden product opportunities.

Output:
- Top 10 monetizable strengths
- Top 10 audience pain points
- Top 5 fastest-to-monetize opportunities

==================================================
PHASE 2 — MARKET OPPORTUNITY SELECTION
==================================================

Generate 10 digital product ideas ranked by:
- profitability,
- speed of launch,
- scalability,
- competition level,
- AI leverage,
- and long-term defensibility.

For each idea provide:
- target audience,
- pain point,
- why now,
- estimated pricing,
- estimated effort,
- estimated monthly revenue potential,
- saturation risk,
- and competitive edge.

Then select the SINGLE BEST opportunity and justify the decision using:
- demand,
- urgency,
- market timing,
- creator-product fit,
- and monetization potential.

==================================================
PHASE 3 — PRODUCT DESIGN
==================================================

Design the product in detail.

Include:
- exact product format,
- modules/components,
- deliverables,
- transformation promised,
- onboarding flow,
- customer journey,
- and retention mechanism.

Recommend the ideal format:
- toolkit,
- prompt pack,
- AI system,
- dashboard,
- template library,
- mini-course,
- subscription,
- SaaS-lite,
- cohort,
- consulting hybrid,
- or automation service.

Create:
1. Product Name
2. Premium Positioning Statement
3. Unique Selling Proposition
4. Offer Stack
5. Pricing Strategy
6. Value Ladder
7. Risk Reversal Strategy
8. Sample Sales Page Headline
9. 30-second Elevator Pitch

==================================================
PHASE 4 — BUILD & LAUNCH EXECUTION
==================================================

Create a step-by-step launch roadmap.

Requirements:
- beginner friendly,
- low-cost,
- AI-first,
- fast execution,
- no-code or low-code preferred.

Use mostly free tools.

Cover:
- product creation,
- branding,
- landing page,
- payments,
- hosting,
- automation,
- lead generation,
- email collection,
- analytics,
- and customer delivery.

Provide:
- exact tools,
- workflows,
- timelines,
- and automation sequences.

Create:
- 7-day MVP launch plan
- 30-day growth roadmap
- 90-day scaling roadmap

==================================================
PHASE 5 — AI AUTOMATION & CONTENT ENGINE
==================================================

Design a repeatable AI-powered content engine that drives traffic automatically.

Include:
- content pillars,
- short-form strategy,
- LinkedIn/X/Instagram strategy,
- SEO ideas,
- lead magnets,
- email sequences,
- repurposing workflows,
- and viral hooks.

Generate:
- 20 content ideas,
- 10 viral hooks,
- 5 lead magnet ideas,
- 5 authority-building strategies.

Explain:
- how AI can automate 60–80% of operations,
- what should remain human-driven,
- and how to create a scalable solo-business system.

==================================================
PHASE 6 — REVENUE EXPANSION
==================================================

Design:
- upsells,
- subscriptions,
- recurring revenue,
- consulting extensions,
- licensing opportunities,
- affiliate systems,
- certification models,
- community models,
- and B2B expansion paths.

Show how to evolve:
- from a single product,
- to a portfolio,
- to a scalable business ecosystem.

Include:
- realistic income scenarios,
- compounding strategy,
- and moat-building mechanisms.

==================================================
PHASE 7 — RISK & REALITY CHECK
==================================================

Critically evaluate:
- execution risks,
- market risks,
- dependency risks,
- AI commoditization risks,
- pricing risks,
- and sustainability risks.

Identify:
- what will likely fail,
- beginner mistakes,
- unrealistic assumptions,
- and hidden operational bottlenecks.

Provide mitigation strategies.

==================================================
OUTPUT REQUIREMENTS
==================================================

- Use structured sections and sub-sections.
- Use tables wherever useful.
- Prioritize execution over theory.
- Avoid generic startup clichés.
- Be commercially realistic.
- Think strategically, not motivationally.
- Include frameworks, comparisons, and decision criteria.
- Make the response detailed enough to execute immediately without clarification.
- Optimize for profitability, leverage, speed, scalability, and long-term defensibility simultaneously.'''


PROMPT_TYPES = {
    "Digital Product Monetization": "Identify and launch profitable digital products, toolkits, templates, mini-courses, SaaS-lite systems, and AI-assisted offers.",
    "AI Startup / SaaS-Lite": "Focus on lean AI tools, micro-SaaS, Streamlit apps, automation products, and founder-led productized solutions.",
    "Creator Economy / Personal Brand": "Build monetizable offers from expertise, posts, teaching content, frameworks, and audience trust.",
    "Consulting / Productized Service": "Convert skills into high-ticket consulting, diagnostics, implementation systems, retainers, and B2B services.",
    "Academic / Research Commercialization": "Transform research, teaching, analytics, AI, and domain expertise into commercial products, courses, tools, and advisory offers.",
}


SAMPLE_CONTEXTS = {
    "Academic AI Expert": "I am an academic and AI/analytics educator with experience in machine learning, healthcare analytics, research writing, MDP/FDP training, Streamlit tools, and student mentoring. Identify commercially viable digital products I can launch quickly.",
    "Creator / Educator": "I create educational content, prompts, tutorials, dashboards, and practical AI learning tools. Identify scalable products for learners, professionals, and institutions.",
    "Consultant / Trainer": "I deliver training programs and advisory sessions for managers, faculty, and working professionals. Identify productized consulting and recurring revenue opportunities.",
    "Streamlit App Builder": "I build no-code/low-code educational Streamlit apps, prompt studios, dashboards, and AI productivity tools. Identify monetizable app-based products and launch paths.",
    "Blank Custom Context": "",
}


def build_prompt(inputs: dict, settings: dict) -> str:
    selected_phases = "\n".join([f"- {phase}" for phase in inputs.get("phases", [])])
    constraints = "\n".join([f"- {item}" for item in inputs.get("constraints", [])])

    context_block = f"""
USER CONTEXT
- Name / Creator: {settings['author']}
- Prompt Type: {inputs['prompt_type']}
- Strategic Focus: {PROMPT_TYPES.get(inputs['prompt_type'], '')}
- Target Audience: {inputs['target_audience']}
- Existing Skills / Assets / Notes: {inputs['user_context']}
- Preferred Product Formats: {inputs['product_formats']}
- Launch Budget: {inputs['budget']}
- Launch Timeline: {inputs['timeline']}
- Revenue Target: {inputs['revenue_target']}
- Risk Tolerance: {inputs['risk_tolerance']}
- Tone: {settings['tone']}
- Output Format: {settings['output_format']}
- Desired Length: {settings['length']}

MANDATORY CONSTRAINTS
{constraints if constraints else '- Use realistic, low-cost, ethical, and execution-ready recommendations.'}

PHASES TO EMPHASIZE
{selected_phases if selected_phases else '- Use all phases in the master framework.'}
"""

    return f"""{BASE_PROMPT}

==================================================
CUSTOMIZATION CONTEXT FOR THIS RUN
==================================================
{context_block}

Before producing the final answer, apply a strict reality check. Remove ideas that are attractive but unrealistic, too generic, too saturated, too expensive to build, or weakly matched to the user's credibility and execution capacity.
"""


def render():
    apply_css()
    sample = load_sample_inputs()
    settings = global_sidebar_fields(sample, key_prefix="mi")

    st.markdown('<div class="page-title">💰 Monetization Idea Studio</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Convert expertise, prompts, notes, apps, courses, and research into commercially viable digital products.</div>',
        unsafe_allow_html=True,
    )

    active = studio_tabs("mi")

    if active == "input":
        section_header("Opportunity Context", "🧭")
        col1, col2 = st.columns(2)
        with col1:
            prompt_type = st.selectbox("Prompt Type", list(PROMPT_TYPES.keys()), key="mi_type")
            context_template = st.selectbox("Quick Context Template", list(SAMPLE_CONTEXTS.keys()), key="mi_context_template")
            target_audience = st.text_input(
                "Target Audience",
                value="students, working professionals, faculty members, founders, consultants, and AI learners",
                key="mi_audience",
            )
        with col2:
            budget = st.selectbox("Launch Budget", ["₹0–₹5,000", "₹5,000–₹25,000", "₹25,000–₹1,00,000", "Flexible if ROI is clear"], key="mi_budget")
            timeline = st.selectbox("Launch Timeline", ["7 days", "30 days", "90 days", "6 months"], key="mi_timeline")
            revenue_target = st.selectbox("Revenue Target", ["$5K", "$10K", "$25K", "$50K+", "Build long-term recurring revenue"], key="mi_revenue")

        default_context = SAMPLE_CONTEXTS.get(context_template, "")
        user_context = st.text_area(
            "Skills, Notes, Assets, Audience, Previous Conversations, or Product Ideas",
            value=default_context,
            height=150,
            key="mi_context",
            help="Paste your skills, notes, CV summary, audience details, product ideas, app concepts, or recurring problems people ask you to solve.",
        )

        section_header("Product Direction", "📦")
        col_a, col_b = st.columns(2)
        with col_a:
            product_formats = st.multiselect(
                "Preferred Product Formats",
                [
                    "Prompt Pack", "Toolkit", "Template Library", "Mini-Course", "Streamlit App",
                    "Dashboard", "SaaS-Lite", "Subscription", "Consulting Hybrid", "Workshop",
                    "Newsletter", "Certification", "Community", "Automation Service",
                ],
                default=["Toolkit", "Prompt Pack", "Streamlit App", "Mini-Course", "Consulting Hybrid"],
                key="mi_formats",
            )
        with col_b:
            risk_tolerance = st.selectbox("Risk Tolerance", ["Conservative", "Balanced", "Aggressive but realistic"], key="mi_risk")

        section_header("Analysis Depth", "🧠")
        phases = st.multiselect(
            "Emphasize Phases",
            [
                "Personal Asset Analysis",
                "Market Opportunity Selection",
                "Product Design",
                "Build & Launch Execution",
                "AI Automation & Content Engine",
                "Revenue Expansion",
                "Risk & Reality Check",
            ],
            default=[
                "Personal Asset Analysis",
                "Market Opportunity Selection",
                "Product Design",
                "Build & Launch Execution",
                "AI Automation & Content Engine",
                "Risk & Reality Check",
            ],
            key="mi_phases",
        )

        constraints = []
        col_x, col_y, col_z = st.columns(3)
        with col_x:
            if st.checkbox("Use free/beginner-friendly tools", value=True, key="mi_free_tools"):
                constraints.append("Use free or beginner-friendly tools wherever possible.")
            if st.checkbox("No paid API dependency", value=True, key="mi_no_api"):
                constraints.append("Avoid paid APIs and mandatory paid software.")
        with col_y:
            if st.checkbox("Prioritize fast launch", value=True, key="mi_fast"):
                constraints.append("Prioritize ideas that can be launched quickly as an MVP.")
            if st.checkbox("Prefer AI leverage", value=True, key="mi_ai"):
                constraints.append("Prefer AI-assisted creation, automation, personalization, and delivery.")
        with col_z:
            if st.checkbox("Include B2B expansion", value=True, key="mi_b2b"):
                constraints.append("Include B2B, institutional, or consulting expansion paths.")
            if st.checkbox("Be brutally realistic", value=True, key="mi_realistic"):
                constraints.append("Reject weak ideas and explain risks, saturation, and execution bottlenecks.")

        if st.button("🚀 Generate Monetization Prompt", use_container_width=True, key="mi_gen"):
            if not user_context.strip():
                st.warning("Please provide at least a short context about your skills, assets, audience, or idea.")
            else:
                inputs = {
                    "prompt_type": prompt_type,
                    "target_audience": target_audience,
                    "user_context": user_context,
                    "product_formats": ", ".join(product_formats),
                    "budget": budget,
                    "timeline": timeline,
                    "revenue_target": revenue_target,
                    "risk_tolerance": risk_tolerance,
                    "phases": phases,
                    "constraints": constraints,
                }
                st.session_state["mi_prompt"] = build_prompt(inputs, settings)
                go_to_output("mi")

    if active == "output":
        if st.session_state.get("mi_prompt"):
            prompt_output_section(st.session_state["mi_prompt"], key_prefix="mi", category="Monetization Idea Studio")
        else:
            st.info("Fill in the Inputs tab and click 'Generate Monetization Prompt'.")
