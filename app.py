import streamlit as st

from src.classifier import classify_persona
from src.generator import generate_response
from src.escalator import (
    should_escalate,
    generate_handoff_summary
)
from src.rag_pipeline import LocalRAGPipeline

st.set_page_config(
    page_title="Persona Support Agent",
    page_icon="🤖"
)

st.title("Persona-Adaptive Customer Support Agent")

rag = LocalRAGPipeline()

query = st.text_area(
    "Enter Customer Query"
)

if st.button("Submit"):

    if query.strip():

        persona_result = classify_persona(query)

        persona = persona_result["persona"]
        confidence = persona_result["confidence"]
        reasoning = persona_result["reasoning"]

        retrieved = rag.retrieve_context(query)
        st.write("DEBUG RETRIEVED:")
        st.write(retrieved)

        escalated = should_escalate(
            query,
            retrieved
        )

        st.subheader("Detected Persona")
        st.success(persona)

        st.subheader("Confidence Score")
        st.info(f"{confidence:.2f}")

        st.subheader("Reasoning")
        st.write(reasoning)

        st.subheader("Retrieved Sources")

        for item in retrieved:
            st.write(f"• {item['source']}")

        if escalated:

            st.error("ESCALATION REQUIRED")

            st.subheader("Human Handoff Summary")

            st.json(
                generate_handoff_summary(
                    persona,
                    query,
                    retrieved
                )
            )

        else:

            response = generate_response(
                query,
                persona,
                retrieved
            )

            st.subheader("Generated Response")

            st.write(response)
            st.write("Collection Count:", rag.collection.count())
