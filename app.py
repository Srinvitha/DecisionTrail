"""
DecisionTrail - Streamlit demo app (logic + flow).

All presentation (CSS, sidebar, hero, citation/reconstruction rendering)
lives in ui.py. This file owns: Hindsight client creation, the
retain/recall/reflect calls, and the chat/session-state flow.

Run:
    streamlit run app.py
"""

import os
import traceback
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from hindsight_client import Hindsight

import ui

load_dotenv(Path(__file__).resolve().parent / ".env")

BANK_ID = "buildtrack-demo"
BASE_URL = os.environ.get("HINDSIGHT_BASE_URL", "http://localhost:8888")
API_KEY = os.environ.get("HINDSIGHT_API_KEY")


def get_client():
    kwargs = {"base_url": BASE_URL}
    if API_KEY:
        kwargs["api_key"] = API_KEY
    return Hindsight(**kwargs)


def ask(client, question: str, mode: str):
    """Run recall (for citations) and reflect (for the answer)."""
    with client:
        recall_results = client.recall(bank_id=BANK_ID, query=question, max_tokens=2048)
        instruction = ui.MODE_INSTRUCTIONS.get(mode, "")
        wrapped_query = f"{instruction}\n\nQuestion: {question}"
        answer = client.reflect(bank_id=BANK_ID, query=wrapped_query, budget="mid")
        return answer.text, recall_results.results


# ----------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------
ui.render_page_setup()
answer_mode = ui.render_sidebar()
ui.render_hero()

# ----------------------------------------------------------------
# Live learning: let the user retain a new memory on the spot
# ----------------------------------------------------------------
with st.expander("➕ Teach DecisionTrail something new", expanded=False):
    st.caption(
        "Add a new piece of information — a customer comment, meeting "
        "note, or decision — and watch it become part of the agent's "
        "memory. Then re-ask a question to see the answer update."
    )
    new_memory = st.text_area(
        "New information",
        placeholder="e.g. Acme Corp told their account manager they will "
        "churn next quarter unless dark mode ships by July.",
        key="new_memory_input",
    )
    col_a, col_b = st.columns([1, 4])
    with col_a:
        submit_memory = st.button("Save to memory", type="primary")
    if submit_memory and new_memory.strip():
        try:
            learn_client = get_client()
            with learn_client:
                learn_client.retain(
                    bank_id=BANK_ID,
                    content=new_memory.strip(),
                    context="live_demo_input",
                    metadata={"source": "live_demo", "thread": "live"},
                )
                impact_query = (
                    f'New information was just added to memory: "{new_memory.strip()}"\n\n'
                    "In 2-4 short bullet points, explain what DecisionTrail just "
                    "learned and how it might affect related analyses. Then on a "
                    "final line, suggest one follow-up question a product leader "
                    "might ask next, prefixed with 'Next: '. Keep the whole thing "
                    "under 80 words."
                )
                impact = learn_client.reflect(bank_id=BANK_ID, query=impact_query, budget="low")
            ui.render_memory_impact_card(impact.text)
        except Exception as e:
            traceback.print_exc()
            st.error(f"Could not save memory: {e}")

st.divider()

# ----------------------------------------------------------------
# Chat
# ----------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "investigation_trail" not in st.session_state:
    st.session_state["investigation_trail"] = []

# Render chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and msg.get("citations"):
            ui.render_reconstruction_card(msg["citations"])
            st.markdown("---")
        st.write(msg["content"])
        if msg["role"] == "assistant":
            ui.render_citations_expander(msg.get("citations", []))

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
                answer_text, recall_results = ask(client, question, answer_mode)
            except Exception as e:
                traceback.print_exc()
                answer_text = None
                recall_results = []
                st.error(f"Memory retrieval failed: {e}")

        if answer_text is None:
            citations = []
        else:
            citations = [
                {"type": r.type, "text": r.text, "metadata": getattr(r, "metadata", {}) or {}}
                for r in recall_results[:8]
            ]
            ui.render_reconstruction_card(citations)
            st.markdown("---")
            st.write(answer_text)
            ui.render_citations_expander(citations)

    st.session_state["messages"].append(
        {"role": "assistant", "content": answer_text or "(no response)", "citations": citations}
    )
    if answer_text is not None:
        st.session_state["investigation_trail"].append(
            (ui.label_for_question(question), question)
        )