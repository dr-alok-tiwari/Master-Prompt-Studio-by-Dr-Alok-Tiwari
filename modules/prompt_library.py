"""
My Prompt Library — save, search, manage, export/import prompts
"""

import json
import streamlit as st
from datetime import datetime
from modules.utils import (
    apply_css, section_header, info_card, escape_html, safe_filename,
    load_saved_prompts, save_prompts_to_disk,
    save_prompt_to_library, delete_prompt_from_library, update_prompt_in_library
)

CATEGORIES = [
    "Research Paper Intelligence", "Handbook Generator", "Course Profile Generator",
    "Job Application Materials", "ATS CV Improver", "Teaching Content Generator",
    "Quiz and Case Study Generator", "Professional Email Generator",
    "Research Productivity Generator", "Productivity Workflow Generator",
    "Streamlit App Prompt Generator", "Custom Prompt Builder", "Other"
]


def render():
    apply_css()
    st.markdown('<div class="page-title">📚 My Prompt Library</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Save, search, manage, and export all your generated prompts</div>', unsafe_allow_html=True)

    prompts = load_saved_prompts()

    # ── Add New Prompt ─────────────────────────────────────────────────────────
    with st.expander("➕ Add New Prompt Manually", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            new_title    = st.text_input("Prompt Title", key="lib_new_title")
            new_category = st.selectbox("Category", CATEGORIES, key="lib_new_cat")
        with col2:
            new_tags_raw = st.text_input("Tags (comma-separated)", key="lib_new_tags")
        new_text = st.text_area("Prompt Text", height=200, key="lib_new_text")
        if st.button("💾 Save Prompt", key="lib_add_btn"):
            if new_title.strip() and new_text.strip():
                tags = [t.strip() for t in new_tags_raw.split(",") if t.strip()]
                save_prompt_to_library(new_title.strip(), new_category, tags, new_text.strip())
                st.success(f"✅ '{new_title}' saved to library!")
                st.rerun()
            else:
                st.warning("Please provide both a title and prompt text.")

    st.markdown("---")

    # ── Stats row ─────────────────────────────────────────────────────────────
    prompts = load_saved_prompts()
    cats = list({p.get("category", "Other") for p in prompts})
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{len(prompts)}</div>
        <div class="metric-label">Total Prompts</div></div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{len(cats)}</div>
        <div class="metric-label">Categories</div></div>""", unsafe_allow_html=True)
    with col_c:
        all_tags = [t for p in prompts for t in p.get("tags", [])]
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{len(set(all_tags))}</div>
        <div class="metric-label">Unique Tags</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Search and filter ─────────────────────────────────────────────────────
    section_header("Search & Filter", "🔍")
    col_s, col_f = st.columns([2, 1])
    with col_s:
        search_q = st.text_input("Search by title, tag, or content", key="lib_search", placeholder="e.g., course profile, ATS, deep learning...")
    with col_f:
        filter_cat = st.selectbox("Filter by Category", ["All"] + CATEGORIES, key="lib_filter")

    # Apply filters
    filtered = prompts
    if search_q.strip():
        q = search_q.lower()
        filtered = [
            p for p in filtered
            if q in p.get("title", "").lower()
            or q in p.get("prompt", "").lower()
            or any(q in t.lower() for t in p.get("tags", []))
        ]
    if filter_cat != "All":
        filtered = [p for p in filtered if p.get("category") == filter_cat]

    # ── Prompt list ───────────────────────────────────────────────────────────
    section_header(f"Saved Prompts ({len(filtered)} found)", "📋")

    if not filtered:
        st.info("No prompts found. Generate prompts using any studio, or add one manually above.")
    else:
        import streamlit.components.v1 as components
        from modules.utils import _copy_button_html

        for i, prompt in enumerate(filtered):
            pid = prompt['id']
            title = prompt.get('title', 'Untitled')
            cat   = prompt.get('category', 'Other')
            raw   = prompt.get('prompt', '')
            wc    = len(raw.split())

            with st.expander(f"📌 {title} — {cat}  ({wc:,} words)", expanded=False):
                # Meta row
                tags_html = "".join([f'<span class="tag-pill">{t}</span>' for t in prompt.get("tags", [])])
                saved_at  = prompt.get('created_at', '')[:16].replace('T', ' ')
                st.markdown(
                    f"**Tags:** {tags_html if tags_html else '<i>None</i>'} &nbsp;|&nbsp; "
                    f"**Saved:** {saved_at} &nbsp;|&nbsp; "
                    f"**{wc:,} words · {len(raw):,} chars**",
                    unsafe_allow_html=True,
                )

                # Edit | Preview tabs
                lib_edit_tab, lib_prev_tab = st.tabs(["✏️ Edit", "👁 Preview"])
                with lib_edit_tab:
                    edited_text = st.text_area(
                        "Prompt text (editable):",
                        value=raw,
                        height=220,
                        key=f"lib_edit_{pid}",
                    )
                with lib_prev_tab:
                    current_text = st.session_state.get(f"lib_edit_{pid}", raw)
                    st.markdown(
                        f"""<div style="background:#FAFAFA;border:1px solid #EDE0D0;
                            border-radius:8px;padding:16px 20px;font-size:0.88rem;
                            line-height:1.7;color:#2C2C2C;white-space:pre-wrap;
                            word-break:break-word;max-height:320px;overflow-y:auto;">
                            {escape_html(current_text)}
                        </div>""",
                        unsafe_allow_html=True,
                    )

                st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)

                # Action row 1: Copy | Save Edits | Delete
                r1c1, r1c2, r1c3 = st.columns([2, 2, 1])
                with r1c1:
                    live = st.session_state.get(f"lib_edit_{pid}", raw)
                    components.html(_copy_button_html(live, btn_key=f"lib_{pid}"), height=46, scrolling=False)
                with r1c2:
                    if st.button("💾 Save Edits", key=f"lib_saveedit_{pid}", use_container_width=True):
                        update_prompt_in_library(pid, {"prompt": st.session_state.get(f"lib_edit_{pid}", raw)})
                        st.success("✅ Updated!")
                        st.rerun()
                with r1c3:
                    if st.button("🗑 Delete", key=f"lib_del_{pid}", use_container_width=True):
                        delete_prompt_from_library(pid)
                        st.warning(f"Deleted: {title}")
                        st.rerun()

                # Action row 2: Download TXT | Download MD
                r2c1, r2c2 = st.columns(2)
                live = st.session_state.get(f"lib_edit_{pid}", raw)
                with r2c1:
                    st.download_button(
                        "⬇ Download .txt", data=live,
                        file_name=f"{safe_filename(title)}.txt",
                        mime="text/plain", key=f"lib_dl_txt_{pid}",
                        use_container_width=True
                    )
                with r2c2:
                    md = f"# {title}\n\n**Category:** {cat}\n\n```\n{live}\n```\n\n---\n*Master Productivity Prompt Studio — Dr Alok Tiwari*"
                    st.download_button(
                        "⬇ Download .md", data=md,
                        file_name=f"{safe_filename(title)}.md",
                        mime="text/markdown", key=f"lib_dl_md_{pid}",
                        use_container_width=True
                    )

    # ── Export / Import ───────────────────────────────────────────────────────
    st.markdown("---")
    section_header("Export / Import Library", "📦")

    col_exp, col_imp = st.columns(2)
    with col_exp:
        st.markdown("**Export Library**")
        all_prompts = load_saved_prompts()
        export_json = json.dumps(all_prompts, indent=2, ensure_ascii=False)
        st.download_button(
            "⬇ Export All Prompts as JSON",
            data=export_json,
            file_name=f"prompt_library_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )

    with col_imp:
        st.markdown("**Import Library**")
        info_card("Importing will MERGE with your existing library (no overwrite).", color="#2E7D52")
        uploaded = st.file_uploader("Upload JSON library file", type=["json"], key="lib_import")
        if uploaded:
            try:
                imported = json.loads(uploaded.read())
                if isinstance(imported, list):
                    existing = load_saved_prompts()
                    existing_ids = {p.get("id") for p in existing}
                    normalised = []
                    for item in imported:
                        if not isinstance(item, dict):
                            continue
                        item.setdefault("id", f"imported_{datetime.now().timestamp()}")
                        item.setdefault("title", "Imported Prompt")
                        item.setdefault("category", "Other")
                        item.setdefault("tags", [])
                        item.setdefault("prompt", "")
                        item.setdefault("created_at", datetime.now().isoformat())
                        item.setdefault("updated_at", datetime.now().isoformat())
                        normalised.append(item)
                    new_entries = [p for p in normalised if p.get("id") not in existing_ids]
                    existing.extend(new_entries)
                    save_prompts_to_disk(existing)
                    st.success(f"✅ Imported {len(new_entries)} new prompts ({len(imported) - len(new_entries)} already existed).")
                    st.rerun()
                else:
                    st.error("Invalid format — expected a JSON array.")
            except Exception as e:
                st.error(f"Import failed: {e}")
