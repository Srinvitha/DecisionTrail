"""
DecisionTrail - presentation/UI helpers.

This module contains ONLY presentation: CSS, sidebar layout, hero text,
and rendering helpers for citations / the memory-reconstruction card.
No Hindsight calls, no business logic - keeping this separate means
UI tweaks can't accidentally break retain/recall/reflect wiring in app.py.

Public functions (signatures unchanged from previous version, so app.py
does not need to change):
    render_page_setup()
    render_sidebar() -> answer_mode (str)
    render_hero()
    render_citation_card(citation: dict)
    render_citations_expander(citations: list)
    render_reconstruction_card(citations: list)
"""

import streamlit as st

CUSTOM_CSS = """
<style>
.stChatMessage { font-size: 1.02rem; }

/* ---- Hero ---- */
.hero-card {
    background: linear-gradient(135deg, #6c63ff 0%, #4834d4 100%);
    color: #ffffff;
    padding: 1.6rem 2rem;
    border-radius: 14px;
    margin-bottom: 1.2rem;
}
.hero-card h1 {
    margin: 0;
    font-size: 2.1rem;
    color: #ffffff;
}
.hero-card .hero-sub {
    margin: 0.3rem 0 0.8rem 0;
    font-size: 1.05rem;
    opacity: 0.95;
}
.hero-card .hero-tagline {
    margin: 0;
    font-size: 0.95rem;
    opacity: 0.9;
    line-height: 1.5;
}
.badge-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}
.badge {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.35);
    border-radius: 20px;
    padding: 0.3rem 0.85rem;
    font-size: 0.8rem;
    color: #ffffff;
    white-space: nowrap;
}

/* ---- Sidebar stat cards ---- */
.stat-card {
    background: #f5f6f8;
    border: 1px solid #e3e5e8;
    border-radius: 10px;
    padding: 0.6rem 0.4rem;
    text-align: center;
}
.stat-number {
    font-size: 1.4rem;
    font-weight: 700;
    color: #6c63ff;
    line-height: 1.2;
}
.stat-label {
    font-size: 0.65rem;
    color: #777;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-top: 0.1rem;
}

/* ---- Example question labels ---- */
.example-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #6c63ff;
    margin: 0.4rem 0 0.1rem 0;
}

/* ---- Citations ---- */
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

/* ---- Memory Reconstruction box ---- */
.reconstruction-box {
    background: #f0f1ff;
    border: 1px solid #d9d6ff;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
}
.reconstruction-title {
    font-weight: 700;
    color: #4834d4;
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
}
.reconstruction-row {
    display: flex;
    justify-content: space-between;
    padding: 0.12rem 0;
    font-size: 0.88rem;
    color: #333;
}
.reconstruction-footer {
    margin-top: 0.4rem;
    font-size: 0.75rem;
    color: #777;
}

/* ---- Live learning box ---- */
.learn-box-header {
    font-weight: 700;
    color: #4834d4;
}

/* ---- Memory impact preview ---- */
.impact-box {
    background: #eafff1;
    border: 1px solid #b9f0cc;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-top: 0.6rem;
}
.impact-title {
    font-weight: 700;
    color: #1f9d55;
    margin-bottom: 0.4rem;
    font-size: 0.95rem;
}

/* ---- Session timeline ---- */
.timeline-item {
    font-size: 0.8rem;
    padding: 0.25rem 0;
    border-left: 2px solid #d9d6ff;
    padding-left: 0.6rem;
    margin-bottom: 0.2rem;
}
.timeline-step {
    font-weight: 600;
    color: #6c63ff;
}
</style>
"""

EXAMPLE_QUESTIONS = [
    "Why was dark mode postponed?",
    "Who might oppose revisiting dark mode today?",
    "How has Sarah's position on dark mode changed over time?",
    "What patterns do you see across leadership decisions?",
]

# (capability label, question) - drives the labeled example buttons
EXAMPLE_QUESTIONS_WITH_LABELS = [
    ("🏛 Decision Reconstruction", "Why was dark mode postponed?"),
    ("⚖️ Stakeholder Tension", "Who might oppose revisiting dark mode today?"),
    ("👥 Stakeholder Evolution", "How has Sarah's position on dark mode changed over time?"),
    ("📈 Pattern Discovery", "What patterns do you see across leadership decisions?"),
]

# Capability badges shown under the hero title
CAPABILITY_BADGES = [
    "🏛 Decision Reconstruction",
    "👥 Stakeholder Evolution",
    "📈 Pattern Discovery",
    "🧠 Organizational Learning",
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

# Icons shown next to each category in the Memory Reconstruction box
SOURCE_ICONS = {
    "Customer Feedback": "🗣️",
    "Engineering Discussions": "⚙️",
    "Leadership Decisions": "🏛️",
    "Investor Feedback": "💰",
    "Internal Discussions": "💬",
    "Support Tickets": "🎫",
    "Internal Analytics": "📊",
    "Live Updates": "🆕",
    "Synthesized Insight": "🧠",
}
DEFAULT_SOURCE_ICON = "📄"


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

        st.markdown("**📖 About this demo**")
        st.write(
            "DecisionTrail remembers every customer request, engineering "
            "estimate, roadmap discussion, and investor note across "
            "BuildTrack's history — then reconstructs *why* decisions were "
            "made, who was involved, and how opinions changed over time."
        )

        st.markdown("---")
        st.markdown("**📊 Memory Bank Stats**")
        col1, col2, col3 = st.columns(3)
        for col, number, label in (
            (col1, "69", "Memories"),
            (col2, "28", "Observations"),
            (col3, "982", "Links"),
        ):
            with col:
                st.markdown(
                    f"""<div class="stat-card">
                    <div class="stat-number">{number}</div>
                    <div class="stat-label">{label}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        st.markdown("**⚙️ Analysis Mode**")
        answer_mode = st.radio(
            "Analysis Mode",
            ANALYSIS_MODES,
            index=1,
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**💡 Try asking**")
        for label, q in EXAMPLE_QUESTIONS_WITH_LABELS:
            st.markdown(f'<div class="example-label">{label}</div>', unsafe_allow_html=True)
            if st.button(q, use_container_width=True, key=f"example_{q}"):
                st.session_state["pending_question"] = q

        st.markdown("---")
        st.caption("Powered by Hindsight")

        render_session_timeline(st.session_state.get("investigation_trail", []))

    return answer_mode


def render_hero():
    """Gradient hero card with title, tagline, and capability badges."""
    badges_html = "".join(f'<span class="badge">{b}</span>' for b in CAPABILITY_BADGES)
    st.markdown(
        f"""<div class="hero-card">
        <h1>🧠 DecisionTrail</h1>
        <p class="hero-sub">Institutional Knowledge Engine</p>
        <p class="hero-tagline">
            Transform fragmented company history into institutional knowledge.
            Discover why decisions were made, how stakeholder opinions evolved,
            and what patterns drive organizational strategy.
        </p>
        <div class="badge-row">{badges_html}</div>
        </div>""",
        unsafe_allow_html=True,
    )


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


def render_memory_impact_card(text: str):
    """Show what DecisionTrail just learned and how it might affect
    future analysis, after a live 'Teach DecisionTrail' save."""
    st.markdown(
        f"""<div class="impact-box">
        <div class="impact-title">✓ Memory Added — Here's what changed</div>
        {text}
        </div>""",
        unsafe_allow_html=True,
    )


def render_session_timeline(trail: list):
    """Render the 'Today's Investigation Trail' in the sidebar.

    trail: list of (label, question) tuples, in order asked.
    """
    if not trail:
        return
    st.markdown("---")
    st.markdown("**🧭 Today's Investigation Trail**")
    for i, (label, question) in enumerate(trail, start=1):
        st.markdown(
            f"""<div class="timeline-item">
            <span class="timeline-step">{i}. {label}</span><br/>{question}
            </div>""",
            unsafe_allow_html=True,
        )


def label_for_question(question: str) -> str:
    """Best-effort capability label for a question, for the timeline."""
    for label, q in EXAMPLE_QUESTIONS_WITH_LABELS:
        if q == question:
            return label
    return "🔍 Custom Investigation"


def render_reconstruction_card(citations: list):
    """Show a 'memory reconstruction' summary in a styled box: which
    source categories were consulted, based on the metadata stored
    with each memory.

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

    rows_html = "".join(
        f'<div class="reconstruction-row">'
        f'<span>{SOURCE_ICONS.get(label, DEFAULT_SOURCE_ICON)} {label}</span>'
        f'<span><b>{n}</b></span>'
        f'</div>'
        for label, n in counts.items()
    )

    st.markdown(
        f"""<div class="reconstruction-box">
        <div class="reconstruction-title">🧠 Memory Reconstruction</div>
        {rows_html}
        <div class="reconstruction-footer">{len(citations)} memories analyzed</div>
        </div>""",
        unsafe_allow_html=True,
    )