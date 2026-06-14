"""
DecisionTrail - presentation/UI helpers.

This module contains ONLY presentation: CSS, sidebar layout, hero text,
and rendering helpers for citations / the memory-reconstruction card.
No Hindsight calls, no business logic - keeping this separate means
UI tweaks can't accidentally break retain/recall/reflect wiring in app.py.
"""

import streamlit as st

CUSTOM_CSS = """
<style>
.stChatMessage { font-size: 1.02rem; }
.citation-card {
    background-color: #f5f6f8;
    border-left: 3px solid #6c63ff;
    border-radius: 6px;
    padding: 0.6rem 0.9rem;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
}
.citation-type {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #6c63ff;
    margin-bottom: 0.2rem;
}
</style>
"""

EXAMPLE_QUESTIONS = [
    "Why was dark mode postponed?",
    "Who might oppose revisiting dark mode today?",
    "How has Sarah's position on dark mode changed over time?",
    "What patterns do you see across leadership decisions?",
]

ANALYSIS_MODES = ["⚡ Executive Summary", "📊 Standard Analysis", "🔍 Deep Investigation"]

MODE_INSTRUCTIONS = {
    "⚡ Executive Summary": (
        "Answer concisely in 3-5 bullet points, under 100 words total. "
        "Focus only on the key findings, no preamble."
    ),
    "📊 Standard Analysis": (
        "Provide a clear, well-organized analysis with the key reasoning "
        "and evidence behind the answer."
    ),
    "🔍 Deep Investigation": (
        "Provide a thorough investigation covering: 1) key findings, "
        "2) stakeholders involved, 3) timeline of relevant events, "
        "4) supporting evidence from memory, and 5) strategic implications."
    ),
}

SOURCE_LABELS = {
    "customer": "Customer Feedback",
    "engineering": "Engineering Discussions",
    "meeting": "Leadership Decisions",
    "investor": "Investor Feedback",
    "slack": "Internal Discussions",
    "support": "Support Tickets",
    "internal_report": "Internal Analytics",
    "live_demo": "Live Updates",
}


def render_page_setup():
    """Page config + global CSS. Call once, first thing."""
    st.set_page_config(page_title="DecisionTrail", page_icon="🧠", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar. Returns the selected analysis mode string.

    Clicking an example question sets st.session_state['pending_question']
    as a side effect (read by app.py's main loop).
    """
    with st.sidebar:
        st.markdown("## 🧠 DecisionTrail")
        st.caption("BuildTrack — Organizational Decision Memory")
        st.markdown("---")

        st.markdown("**About this demo**")
        st.write(
            "DecisionTrail reconstructs institutional knowledge from scattered customer feedback, engineering discussions, leadership decisions, and investor conversations — uncovering the hidden patterns, tradeoffs, and reasoning that shape organizational decisions over time."
        )

        st.markdown("---")
        st.markdown("**Memory bank stats**")
        col1, col2, col3 = st.columns(3)
        col1.metric("Memories", "69")
        col2.metric("Observations", "28")
        col3.metric("Links", "982")

        st.markdown("---")
        st.markdown("**Analysis Mode**")
        answer_mode = st.radio(
            "Analysis Mode",
            ANALYSIS_MODES,
            index=1,
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**Try asking:**")
        for q in EXAMPLE_QUESTIONS:
            if st.button(q, use_container_width=True, key=f"example_{q}"):
                st.session_state["pending_question"] = q

        st.markdown("---")
        st.caption("Powered by Hindsight")

    return answer_mode


def render_hero():
    """Title + subtitle + intro blurb for the main area."""
    st.title("DecisionTrail")
    st.subheader("Ask why your company made a decision")
    st.markdown(
        "New product managers spend weeks reconstructing old decisions. "
        "**DecisionTrail** remembers customer feedback, engineering "
        "discussions, investor concerns, and roadmap debates — so teams "
        "never lose context."
    )
    st.divider()


def render_citation_card(citation: dict):
    """Render a single supporting-memory card."""
    st.markdown(
        f"""<div class="citation-card">
        <div class="citation-type">{citation['type']}</div>
        {citation['text']}
        </div>""",
        unsafe_allow_html=True,
    )


def render_citations_expander(citations: list):
    """Render the '📎 Supporting memories (N)' expander, if any citations."""
    if not citations:
        return
    with st.expander(f"📎 Supporting memories ({len(citations)})"):
        for c in citations:
            render_citation_card(c)


def render_reconstruction_card(citations: list):
    """Show a 'memory reconstruction' summary: which source categories
    were consulted, based on the metadata stored with each memory.

    Observation-type results without a 'source' in metadata are labeled
    'Synthesized Insight' (Hindsight's own derived facts), rather than
    'Unknown'.
    """
    counts = {}
    for c in citations:
        if c.get("type") == "observation" and not (c.get("metadata") or {}).get("source"):
            label = "Synthesized Insight"
        else:
            source = (c.get("metadata") or {}).get("source", "unknown")
            label = SOURCE_LABELS.get(source, source.replace("_", " ").title())
        counts[label] = counts.get(label, 0) + 1

    if not counts:
        return

    st.markdown("**🧠 Memory Reconstruction**")
    lines = "\n".join(f"- ✓ {label} ({n})" for label, n in counts.items())
    st.markdown(lines)
    st.caption(f"Supporting memories: {len(citations)}")