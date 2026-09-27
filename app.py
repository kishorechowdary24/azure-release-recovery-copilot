import streamlit as st

from llm import create_investigation_advice
from memory import find_similar_incidents, retain_resolved_incident

st.set_page_config(
    page_title="Azure Release Recovery Copilot",
    page_icon="🛠️",
    layout="centered",
)

st.title("Azure Release Recovery Copilot")
st.caption("Investigate deployment failures using lessons from past incidents.")

if "investigation" not in st.session_state:
    st.session_state.investigation = None

if "resolution_saved" not in st.session_state:
    st.session_state.resolution_saved = False

st.subheader("New deployment incident")

service = st.text_input("Service name")
error = st.text_area("Paste the deployment error or relevant log")
recent_change = st.text_input("What changed recently? (optional)")
use_hindsight = st.checkbox(
    "Use Hindsight memory (leave unchecked for baseline)",
    value=False,
    key="use_hindsight_toggle_v2",
)

if st.button("Investigate", type="primary"):
    if not error.strip():
        st.warning("Paste a deployment error before investigating.")
    else:
        st.session_state.investigation = None
        st.session_state.resolution_saved = False

        query = error.strip()

        try:
            memories = find_similar_incidents(query) if use_hindsight else []
            advice = create_investigation_advice(
                service=service,
                error=error,
                recent_change=recent_change,
                memories=memories,
            )
        except Exception:
            st.error(
                "The investigation failed. Check the Hindsight and Groq "
                "settings, then try again."
            )
        else:
            st.session_state.investigation = {
                "service": service,
                "error": error,
                "recent_change": recent_change,
                "memories": memories,
                "use_hindsight": use_hindsight,
                "advice": advice,
            }

investigation = st.session_state.investigation

if investigation:
    st.subheader("Investigation advice")
    st.markdown(investigation["advice"])

    st.subheader("Hindsight memories used")
    if not investigation["use_hindsight"]:
        st.info("Hindsight memory was off for this investigation.")
    elif investigation["memories"]:
        for memory in investigation["memories"]:
            st.markdown(f"- {memory}")
    else:
        st.info("No relevant past incidents were found.")

    st.divider()
    st.subheader("Record the resolution")

    with st.form("resolution_form"):
        cause = st.text_area("What was the actual cause?")
        fix = st.text_area("What fix did you apply?")
        outcome = st.selectbox(
            "What was the outcome?",
            ["Select one", "Resolved", "Partially resolved", "Not resolved"],
        )
        submitted = st.form_submit_button("Save outcome to Hindsight")

    if submitted:
        if not cause.strip() or not fix.strip():
            st.warning("Enter the actual cause and the fix you applied.")
        elif outcome == "Select one":
            st.warning("Choose the outcome before saving.")
        else:
            try:
                retain_resolved_incident(
                    service=investigation["service"],
                    error=investigation["error"],
                    recent_change=investigation["recent_change"],
                    cause=cause,
                    fix=fix,
                    outcome=outcome,
                )
            except Exception:
                st.error("Could not save the outcome to Hindsight.")
            else:
                st.session_state.resolution_saved = True
                st.success("Resolution saved to Hindsight.")

    if st.session_state.resolution_saved:
        st.info("This outcome is now available as memory for future incidents.")