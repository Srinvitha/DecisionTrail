"""
DecisionTrail - Streamlit demo UI

A simple chat interface over a Hindsight memory bank: ask a question,
get a synthesized answer (via reflect), and see the supporting memories
that were recalled (citations panel).

Run:
    streamlit run app.py
"""

import os
import traceback
import streamlit as st
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

BANK_ID = "buildtrack-demo"
BASE_URL = os.environ.get("HINDSIGHT_BASE_URL", "http://localhost:8888")
API_KEY = os.environ.get("HINDSIGHT_API_KEY")

EXAMPLE_QUESTIONS = [
    "Why was dark mode postponed?",
    "Who might oppose revisiting dark mode today?",
    "How has Sarah's position on dark mode changed over time?",
    "What patterns do you see across leadership decisions?",
]


def get_client():
    kwargs = {"base_url": BASE_URL}
    if API_KEY:
        kwargs["api_key"] = API_KEY
    return Hindsight(**kwargs)


def ask(client, question: str):
    """Run recall (for citations) and reflect (for the answer)."""
    recall_results = client.recall(bank_id=BANK_ID, query=question, max_tokens=2048)
    answer = client.reflect(bank_id=BANK_ID, query=question, budget="mid")
    return answer.text, recall_results.results


# ----------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------
st.set_page_config(page_title="DecisionTrail", page_icon="🧠", layout="wide")

st.markdown(
    """
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
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🧠 DecisionTrail")
    st.caption("BuildTrack — Organizational Decision Memory")
    st.markdown("---")

    st.markdown("**About this demo**")
    st.write(
        "DecisionTrail remembers every customer request, engineering "
        "estimate, roadmap discussion, and investor note across "
        "BuildTrack's history — then reconstructs *why* decisions were "
        "made, who was involved, and how opinions changed over time."
    )

    st.markdown("---")
    st.markdown("**Memory bank stats**")
    col1, col2, col3 = st.columns(3)
    col1.metric("Memories", "69")
    col2.metric("Observations", "28")
    col3.metric("Links", "982")

    st.markdown("---")
    st.markdown("**Try asking:**")
    for q in EXAMPLE_QUESTIONS:
        if st.button(q, use_container_width=True, key=f"example_{q}"):
            st.session_state["pending_question"] = q

    st.markdown("---")
    st.caption("Powered by Hindsight + Groq")

# ----------------------------------------------------------------
# Main chat area
# ----------------------------------------------------------------
st.title("DecisionTrail")
st.subheader("Ask why your company made a decision")
st.markdown(
    "New product managers spend weeks reconstructing old decisions. "
    "**DecisionTrail** remembers customer feedback, engineering "
    "discussions, investor concerns, and roadmap debates — so teams "
    "never lose context."
)
st.divider()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Render chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and msg.get("citations"):
            with st.expander(f"📎 Supporting memories ({len(msg['citations'])})"):
                for c in msg["citations"]:
                    st.markdown(
                        f"""<div class="citation-card">
                        <div class="citation-type">{c['type']}</div>
                        {c['text']}
                        </div>""",
                        unsafe_allow_html=True,
                    )

# Handle a question coming from a sidebar example button
pending = st.session_state.pop("pending_question", None)
typed = st.chat_input("Ask about a decision, stakeholder, or trend...")
question = pending or typed

if question:
    st.session_state["messages"].append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Reconstructing from memory..."):
            try:
                client = get_client()
                answer_text, recall_results = ask(client, question)
            except Exception as e:
                traceback.print_exc()
                answer_text = None
                recall_results = []
                st.error(f"Memory retrieval failed: {e}")

        if answer_text is None:
            citations = []
        else:
            st.write(answer_text)
            citations = [{"type": r.type, "text": r.text} for r in recall_results[:8]]
            if citations:
                with st.expander(f"📎 Supporting memories ({len(citations)})"):
                    for c in citations:
                        st.markdown(
                            f"""<div class="citation-card">
                            <div class="citation-type">{c['type']}</div>
                            {c['text']}
                            </div>""",
                            unsafe_allow_html=True,
                        )

    st.session_state["messages"].append(
        {"role": "assistant", "content": answer_text or "(no response)", "citations": citations}
    )